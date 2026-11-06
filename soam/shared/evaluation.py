"""E1 interventions and scoring on isolated prediction snapshots."""

import copy
from dataclasses import dataclass

import numpy as np
import torch

from soam.platform.core import (
    Intervention,
    fingerprint,
    freeze,
    model_fingerprint,
    predict,
    storage,
)
from soam.platform.evaluation import assimilate_checked
from soam.shared.data import stream
from soam.shared.fitting import parameter_check


@dataclass(frozen=True)
class Probe:
    kind: str = "intact"
    units: tuple = ()
    seed: int = 0

    def validate(self, model, role):
        allowed = {
            "intact",
            "full_clamp",
            "readout_clamp",
            "action_shift",
            "zero_A",
            "zero_cue",
            "perturb",
            "zero_S",
            "zero_S_perturb",
        }
        if self.kind not in allowed:
            raise ValueError("unsupported E1 probe")
        lesion = self.kind in ("full_clamp", "readout_clamp")
        if bool(self.units) != lesion or len(set(self.units)) != len(self.units):
            raise ValueError("probe units required only for lesions")
        if any(type(i) is not int or not 0 <= i < model.spec.width - 2 for i in self.units):
            raise ValueError("invalid neural unit; role flags cannot be probed")
        if self.kind not in ("intact", "full_clamp", "readout_clamp") and model.spec.kind != "S32":
            raise ValueError("this mechanism probe is defined only for S32")
        if self.kind in ("action_shift", "zero_A") and role != "transition":
            raise ValueError("direction probe requires transition")
        if self.kind in ("zero_cue", "perturb", "zero_S", "zero_S_perturb") and role != "recall":
            raise ValueError("recovery/cue probe requires recall")
        if type(self.seed) is not int or self.seed < 0:
            raise ValueError("nonnegative perturbation seed required")
        return self


class ReadoutMask(torch.nn.Module):
    """Readout-only lesion leaves recurrence and assimilation untouched."""

    def __init__(self, model, units):
        super().__init__()
        self.model, self.spec = model, model.spec
        self.units = units

    def check_state(self, state):
        self.model.check_state(state)

    def advance(self, state, command, *, clamp_units=None):
        return self.model.advance(state, command, clamp_units=clamp_units)

    def readout(self, state):
        masked = state.clone()
        masked[:, self.units] = 0
        return self.model.readout(masked)


def perturb(state, seed):
    rng = np.random.Generator(np.random.PCG64(seed))
    delta = torch.from_numpy(rng.normal(size=state[:, :-2].shape)).float()
    delta = 0.1 * delta / delta.square().mean(1, keepdim=True).sqrt()
    out = state.clone()
    out[:, :-2] += delta
    return out, delta


def work_per_call(model, role):
    """Dense linear MAC estimates; assembly/nonlinear/hash/copy costs excluded.

    Skew contraction counts four dense matvecs plus coefficient weighting, an
    algebraic estimate independent of einsum's backend contraction scheduling.
    """
    n, name = model.n, model.spec.kind
    if name == "L12":
        return {"assimilate_macs": 300, "advance_macs": 624, "readout_macs": 0}
    if name.startswith("G"):
        advance = 3 * n * (n + 5)
    elif name.startswith("D") and role == "recall":
        advance = n * n
    elif name == "SYM32":
        advance = n * n + 3 * n
    else:
        advance = 5 * n * n + 7 * n
    return {"assimilate_macs": 24 * n, "advance_macs": advance, "readout_macs": 12 * n}


def evaluate(model, episode, variance, probe=None):
    """Evaluator owns targets; dynamics see only allowed observation packets."""
    probe = Probe() if probe is None else probe
    role = "recall" if episode.observations[0].cue[0, 0] == 1 else "transition"
    if len(episode.commands) != (10 if role == "recall" else 32):
        raise ValueError("evaluation horizon must be ten recall or 32 transition updates")
    probe.validate(model, role)
    if not np.isfinite(float(variance)) or float(variance) < 1e-6:
        raise ValueError("finite frozen normalization variance required")
    original = model_fingerprint(model)
    observed_before = fingerprint(episode.observed_arrays())
    local = copy.deepcopy(model).eval().requires_grad_(False)
    if probe.kind == "zero_A":
        local.bank.A.zero_()
    if probe.kind in ("zero_S", "zero_S_perturb"):
        local.bank.S.zero_()
    parameter_check(local)
    prepared = model_fingerprint(local)
    commands = episode.commands
    if probe.kind == "action_shift":
        commands = commands[-1:] + commands[:-1]
    clamp = None
    if probe.kind == "full_clamp":
        clamp = torch.zeros(local.spec.width, dtype=torch.bool)
        clamp[list(probe.units)] = True
    read_model = ReadoutMask(local, probe.units) if probe.kind == "readout_clamp" else local
    try:
        with torch.no_grad():
            obs = episode.observations[0].clone()
            if probe.kind == "zero_cue":
                obs.z.zero_()
                obs.valid.zero_()
            h = assimilate_checked(local, local.initial_state(len(obs.z)), obs)
            if clamp is not None:
                h = h.masked_fill(clamp.unsqueeze(0), 0)
            injected = torch.zeros_like(h[:, :-2])
            if probe.kind in ("perturb", "zero_S_perturb"):
                h, injected = perturb(h, probe.seed)
            anchor = h.clone()
            intervention = Intervention("state_clamp", probe.units) if clamp is not None else None
            free = predict(freeze(read_model, h), commands, intervention)
            arrays = {
                "anchor_state": anchor,
                "injected_delta": injected,
                "free_features": free.features,
                "free_states": free.states,
            }
            if role == "transition":
                outputs, states = [], [h.clone()]
                for t, cmd in enumerate(commands):
                    # Single-step snapshots check input ownership and parameter writes too.
                    predicted = predict(freeze(read_model, h), (cmd,), intervention)
                    outputs.append(predicted.features[0])
                    h = assimilate_checked(local, predicted.states[0], episode.observations[t + 1])
                    if clamp is not None:
                        h = h.masked_fill(clamp.unsqueeze(0), 0)
                    states.append(h.clone())
                arrays.update(
                    grounded_features=torch.stack(outputs), live_states=torch.stack(states)
                )
            target = episode.targets.features[1:].double()
            squared = (free.features.double() - target).square().mean((1, 2)) / float(variance)
            metrics = {"per_step_free_nmse": squared.tolist()}
            if role == "recall":
                metrics["recall_nmse"] = squared[-1].item()
            else:
                metrics.update(
                    free8_nmse=squared[:8].mean().item(), free32_nmse=squared.mean().item()
                )
                grounded = (arrays["grounded_features"].double() - target).square().mean(
                    (1, 2)
                ) / float(variance)
                metrics.update(
                    grounded32_nmse=grounded.mean().item(), per_step_grounded_nmse=grounded.tolist()
                )
    finally:
        if model_fingerprint(model) != original or model_fingerprint(local) != prepared:
            raise RuntimeError("persistent write during E1 evaluation")
        if fingerprint(episode.observed_arrays()) != observed_before:
            raise RuntimeError("source observation mutation")
    steps = len(commands)
    paths = 2 if role == "transition" else 1
    calls = {
        "assimilate": steps + 1 if role == "transition" else 1,
        "advance": paths * steps,
        "readout": paths * steps,
    }
    per_call = work_per_call(model, role)
    weights = list(model.state_dict().values())
    return arrays, {
        "role": role,
        "probe": probe.kind,
        "units": list(probe.units),
        "metrics": metrics,
        "model_sha256": original,
        "probe_model_sha256": prepared,
        "work": {
            **calls,
            "linear_macs": sum(calls[k] * per_call[k + "_macs"] for k in calls),
            "mac_scope": "dense linear forward estimate; excludes packing/nonlinear/backward/hash/copies",
            "snapshot_model_copies": 1 + (steps if role == "transition" else 0),
            "prediction_model_copies": 1 + (steps if role == "transition" else 0),
            "probe_model_copies": 1,
        },
        "resources": {
            "parameters": sum(p.numel() for p in model.parameters()),
            "persistent": storage(weights),
            "state": storage([anchor]),
            "available_neural_units": model.spec.width - 2,
            "active_neural_units": model.n,
            "role_flags": 2,
            "returned_arrays": storage(arrays.values()),
            "peak_model_copies": 4,
            "workspace_policy": "matrix expansion/copy/hash temporaries measured in process RSS separately",
        },
        "exposure": {
            "distinct_clean_source_records": steps + 1 if role == "transition" else 1,
            "free_future_observation_reads": 0,
            "fitting_updates": 0,
            "target_feature_vectors_scored": paths * steps,
        },
    }


def select_units(model, task, variance, *, archive_cell, budget_check, fixture=False):
    """Development-only singleton ranking; never reads confirmation streams."""
    split = "fixture/evaluation" if fixture else "development_diagnostic"
    count = 2 if fixture else 20
    errors = {role: [] for role in ("recall", "transition")}
    for role, role_errors in errors.items():
        episodes = [
            task.episode(split, 401, i, role, component=f"lesion-selection/{role}")
            for i in range(count)
        ]
        metric = "recall_nmse" if role == "recall" else "free8_nmse"
        for units in ((), *((i,) for i in range(32))):
            probe = Probe("full_clamp", units) if units else Probe()
            values = []
            for i, episode in enumerate(episodes):
                budget_check()
                arrays, record = evaluate(model, episode, variance, probe)
                archive_cell(role, units, i, episode, arrays, record)
                values.append(record["metrics"][metric])
                budget_check()
            role_errors.append(float(np.mean(values)))
    relative = [
        np.maximum(np.array(errors[r][1:]) - errors[r][0], 0) / max(errors[r][0], 1e-6)
        for r in errors
    ]
    scores = np.minimum(*relative)
    selected = sorted(range(32), key=lambda i: (-scores[i], i))[:4]
    return tuple(selected), {"errors": errors, "scores": scores.tolist(), "selection_split": split}


def random_masks(root, *, fixture=False):
    split = "fixture/evaluation" if fixture else "confirmation"
    seed = stream(split, root, 0, "random-lesions")
    rng = np.random.Generator(np.random.PCG64(seed))
    return [tuple(sorted(rng.choice(32, 4, replace=False).tolist())) for _ in range(4)], seed
