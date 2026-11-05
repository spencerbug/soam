"""Observed-only interaction and copy/resource ledgers for the fixture runner."""

import torch

from soam.platform.core import fingerprint, freeze, model_fingerprint, predict, storage
from soam.platform.tasks import EvaluationTargets


def assimilate_checked(model, state, observation):
    state, observation = state.clone(), observation.clone()
    inputs = {
        "state": state,
        "z": observation.z,
        "valid": observation.valid,
        "cue": observation.cue,
        "cue_valid": observation.cue_valid,
    }
    before = fingerprint(inputs)
    try:
        return model.assimilate(state, observation)
    finally:
        if fingerprint(inputs) != before:
            raise RuntimeError("assimilation mutated its inputs")


def evaluate(model, task, episode):
    """Only this orchestration/scoring layer has access to the full episode."""
    if len(episode.observations) != len(episode.commands) + 1:
        raise ValueError("one more observation than command required")
    before = model_fingerprint(model)
    source_before = fingerprint(episode.observed_arrays())
    try:
        with torch.no_grad():
            h = model.initial_state(episode.observations[0].z.shape[0])
            h = assimilate_checked(model, h, episode.observations[0])
            anchor = h.detach().clone()
            anchor_hash = fingerprint({"state": h})
            snapshot = freeze(model, h)
            free = predict(snapshot, episode.commands)
            if fingerprint({"state": h}) != anchor_hash:
                raise RuntimeError("prediction mutated live state")
            grounded, live_states = [], [h.clone()]
            for t, command in enumerate(episode.commands):
                state_in, command_in = h.clone(), command.clone()
                inputs = fingerprint({"state": state_in, "action": command_in.action})
                prior = model.advance(state_in, command_in)
                if fingerprint({"state": state_in, "action": command_in.action}) != inputs:
                    raise RuntimeError("backend mutated live inputs")
                prior_hash = fingerprint({"state": prior})
                grounded.append(model.readout(prior).detach().clone())
                if fingerprint({"state": prior}) != prior_hash:
                    raise RuntimeError("readout mutated state")
                # The next observation is first made available after its prediction.
                h = assimilate_checked(model, prior, episode.observations[t + 1])
                live_states.append(h.detach().clone())
            grounded = torch.stack(grounded)
            target = EvaluationTargets(episode.targets.features[1:], episode.targets.world[1:])
            metrics = {
                "free": task.score(free.features, target),
                "grounded": task.score(grounded, target),
            }
    finally:
        if model_fingerprint(model) != before:
            raise RuntimeError("persistent write during evaluation")
        if fingerprint(episode.observed_arrays()) != source_before:
            raise RuntimeError("source observations mutated")
    d, a, n, t = model.spec.features, model.spec.actions, model.spec.width, len(episode.commands)
    buffers = list(model.state_dict().values())
    arrays = {
        "anchor_state": anchor,
        "free_features": free.features,
        "free_states": free.states,
        "grounded_features": grounded,
        "live_states": torch.stack(live_states),
    }
    return arrays, {
        "metrics": metrics,
        "model_fingerprint": before,
        "energy": None,
        "energy_reason": "backend has no declared energy function",
        "work": {
            "live_assimilation_calls": t + 1,
            "live_advance_calls": t,
            "live_readout_calls": t,
            "live_state_input_copies": 2 * t + 1,
            "live_command_copies": t,
            "observation_packet_copies": t + 1,
            "snapshot_model_copies": 1,
            "snapshot_state_copies": 1,
            "anchor_state_copies": 1,
            "live_trajectory_state_copies": t + 1,
            "live_trajectory_feature_copies": t,
            "live_linear_macs": (t + 1) * n * d + t * (n * n + n * a + d * n),
            "live_tanh_elements": (t + 1) * n + (t * n if model.spec.kind == "leaky" else 0),
            "prediction": free.work,
        },
        "resources": {
            "trained_parameters": sum(p.numel() for p in model.parameters()),
            "supplied_buffer_scalars": sum(v.numel() for v in buffers),
            "persistent": storage(buffers),
            "live_state": storage([h]),
            "snapshot_state": storage([snapshot._state]),
            "prediction_initial_state_bytes": h.numel() * h.element_size(),
            "prediction_model_bytes": storage(buffers)["unique_storage_bytes"],
            "snapshot_model": storage(list(snapshot._model.state_dict().values())),
            "peak_coexisting_model_copies": 3,
            "returned_arrays": storage(arrays.values()),
            "observations": storage(episode.observed_arrays().values()),
            "evaluator_targets": storage([episode.targets.features, episode.targets.world]),
            "fixed_encoder": storage(task.encoder.buffers()),
            "workspace_policy": "temporary matmul/stack/hash copies included in process peak RSS; logical inventories are not process peak",
        },
        "exposure": {
            "distinct_observations": t + 1,
            "executed_transitions": t,
            "grounded_assimilations": t + 1,
            "free_future_observation_reads": 0,
            "target_uses_for_scoring": 2 * t,
            "fitting_updates": 0,
        },
    }
