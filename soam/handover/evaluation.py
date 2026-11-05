"""History controls, observation-only interaction, and evaluator-owned scoring."""

import math
import time
from dataclasses import replace

import numpy as np
import torch

from soam.handover.models import Work
from soam.handover.protocol import rng


class Interaction:
    """Runner-owned prefix and control policy; the model cannot access an Episode."""

    def __init__(self, model, mode="pretracking"):
        if mode not in ("pretracking", "cold", "equal_history_replay", "source_transport"):
            raise ValueError("unknown history mode")
        if mode != "pretracking" and model.variant not in ("A2", "G2"):
            raise ValueError("history modes require independent banks")
        if mode == "source_transport" and model.variant != "A2":
            raise ValueError("transport is an analytic control")
        self.model, self.mode = model, mode
        self.state = model.initial_state()
        self.history = []
        self.accumulated_action = 0.0

    def reconstruct(self, bank):
        pose = self.model.initial_state().pose[bank].clone()
        work = Work(state_resets=1, state_copies=1)
        for t, packet in enumerate(self.history):
            pose, extra = self.model.pose_transition(pose, packet, t > 0, bank)
            work.add(extra)
            work.replay_packets += 1
        return pose, work

    @torch.no_grad()
    def step(self, packet):
        model, old = self.model, self.state
        self.accumulated_action += packet.executed_action_previous
        if self.mode == "equal_history_replay":
            self.history.append(packet.clone())
        active = None
        if self.mode != "pretracking":
            active = [False, False]
            # Initial acquisition precedes a handover: warm the leading live candidate.
            bank = old.attended if old.attended >= 0 else int(old.weights[:2].argmax())
            active[bank] = True
        start = time.perf_counter()
        new, estimates, work, updated = model.advance(old, packet, active)
        work.history_packet_copies += int(self.mode == "equal_history_replay")
        core_seconds = time.perf_counter() - start
        start = time.perf_counter()
        events, replay_seconds = [], 0.0
        candidate = model.eligible(new, estimates, ignore_norm=self.mode != "pretracking")
        if (
            self.mode != "pretracking"
            and old.attended >= 0
            and candidate >= 0
            and candidate != old.attended
        ):
            if self.mode == "equal_history_replay":
                began = time.perf_counter()
                new.pose[candidate], extra = self.reconstruct(candidate)
                replay_seconds = time.perf_counter() - began
                work.add(extra)
                events.append({"kind": "replay", "bank": candidate, "packets": len(self.history)})
            elif self.mode == "cold":
                prior = model.initial_state().pose[candidate]
                new.pose[candidate], extra = model.pose_transition(prior, packet, False, candidate)
                work.add(extra)
                work.state_resets += 1
                events.append({"kind": "cold_reset", "bank": candidate})
            else:
                angle = (
                    math.pi / 3 + float(model.gains[1] - model.gains[0]) * self.accumulated_action
                )
                if candidate == 0:
                    angle = -angle
                source = new.pose[old.attended]
                new.pose[candidate] = math.cos(angle) * (model.plane @ source) + math.sin(angle) * (
                    model.quarter_turn @ source
                )
                work.state_copies += 1
                work.linear_macs += 288
                # Current destination evidence is assimilated once after the control copy.
                new.pose[candidate], extra = model.pose_transition(
                    new.pose[candidate], packet, False, candidate
                )
                work.add(extra)
                events.append(
                    {"kind": "source_transport", "bank": candidate, "source": old.attended}
                )
            estimates, extra = model.estimates(new)
            work.add(extra)
            # A reconstruction is not continuous online tracking.
            updated[candidate] = False
            if self.mode == "cold":
                new.attended = candidate  # Declared cold readiness exception, bad output is scored.
            else:
                model.select(new, estimates)
        else:
            model.select(new, estimates)
        if new.attended != old.attended:
            events.append({"kind": "commit", "source": old.attended, "bank": new.attended})
        selection_seconds = time.perf_counter() - start
        model.check_state(new)
        diagnostics = model.diagnostics(new, updated)
        work.linear_macs += 9
        diagnostics.update(
            events=events,
            work=work.to_dict(),
            core_seconds=core_seconds,
            selection_seconds=selection_seconds,
            replay_seconds=replay_seconds,
            **work.timings(),
        )
        self.state = new
        return new, estimates.clone(), diagnostics


def effective_packet(packet, index, intervention):
    if intervention == "no_sensing_after_15" and index > 15:
        return replace(packet, z=torch.zeros_like(packet.z), valid=torch.zeros_like(packet.valid))
    return packet


@torch.no_grad()
def run_episode(model, episode, mode="pretracking", intervention="none"):
    before = model.persistent_fingerprint()
    interaction = Interaction(model, mode)
    records, snapshots, events = [], {}, []
    total_work, prediction_work = Work(), Work()
    timings = {
        "core_seconds": 0.0,
        "selection_seconds": 0.0,
        "replay_seconds": 0.0,
        "prediction_seconds": 0.0,
        "diagnostic_seconds": 0.0,
        "key_seconds": 0.0,
        "pose_seconds": 0.0,
        "readout_seconds": 0.0,
    }
    wall_start, cpu_start = time.perf_counter(), time.process_time()
    max_history_bytes = 0
    for t, raw in enumerate(episode.packets):
        packet = effective_packet(raw, t, intervention)
        state, estimates, diag = interaction.step(packet)
        if t == 40 and intervention in ("perturb_A_at_40", "perturb_B_at_40"):
            bank = 0 if intervention == "perturb_A_at_40" else 1
            if model.analytic:
                state.pose[bank] *= 0.5
            else:
                generator = rng(episode.seed, episode.split, 0, episode.index, "perturbations")
                noise = torch.tensor(
                    generator.normal(size=state.pose[bank].shape), dtype=torch.float32
                )
                magnitude = 0.5 * max(float(state.pose[bank].norm()), 0.1)
                state.pose[bank] += magnitude * noise / noise.norm()
            estimates, extra = model.estimates(state)
            total_work.add(extra)
            diag["events"].append({"kind": "diagnostic_perturbation", "bank": bank})
            model.check_state(state)
        for key in (
            "core_seconds",
            "selection_seconds",
            "replay_seconds",
            "key_seconds",
            "pose_seconds",
            "readout_seconds",
        ):
            timings[key] += diag[key]
        total_work.add(Work(**diag["work"]))
        events.extend({"frame": t, **event} for event in diag["events"])
        began = time.perf_counter()
        one_step = None
        if t < len(episode.actions):
            one_step, extra = model.predict(state, episode.actions[t : t + 1], return_work=True)
            prediction_work.add(extra)
        if t in model.protocol["evaluation"]["prediction_anchors"]:
            for horizon in model.protocol["evaluation"]["free_horizons"]:
                prediction, extra = model.predict(
                    state, episode.actions[t : t + horizon], return_work=True
                )
                snapshots[f"anchor{t}_h{horizon}"] = prediction
                prediction_work.add(extra)
        timings["prediction_seconds"] += time.perf_counter() - began
        began = time.perf_counter()
        records.append(
            {
                "estimate": estimates,
                "key": state.key.clone(),
                "pose": state.pose.clone(),
                "weights": state.weights.clone(),
                "priming": diag["priming"].clone(),
                "attended": state.attended,
                "age": state.evidence_age.clone(),
                "localized": state.localized.clone(),
                "updated": diag["updated_banks"].clone(),
                "roles": diag["roles"],
                "one_step": one_step,
                "key_energy": float(model.key_energy(state.key)) if model.analytic else None,
            }
        )
        if interaction.history:
            # Actual logical tensor storage; scalar/Python overhead is represented by RSS.
            max_history_bytes = len(interaction.history) * (24 * 4 + 2 + 16 * 4 + 8 + 1)
        timings["diagnostic_seconds"] += time.perf_counter() - began
    if model.persistent_fingerprint() != before:
        raise RuntimeError("inference changed persistent state")
    arrays = {
        name: torch.stack([row[name] for row in records])
        for name in ("estimate", "key", "pose", "weights", "priming", "age", "localized", "updated")
    }
    arrays["attended"] = torch.tensor([r["attended"] for r in records])
    arrays["one_step"] = torch.cat([r["one_step"] for r in records[:-1]])
    role_ids = {"inactive": 0, "primed": 1, "tracking": 2, "attended": 3}
    arrays["roles"] = torch.tensor([[role_ids[role] for role in r["roles"]] for r in records])
    arrays["key_energy"] = torch.tensor(
        [r["key_energy"] for r in records if r["key_energy"] is not None], dtype=torch.float64
    )
    arrays.update(snapshots)
    metrics = score(model, episode, arrays, events)
    return {
        "arrays": arrays,
        "data_exposure": {
            "observation_packets": len(episode.packets),
            "available_valid_feature_observations": sum(
                int(p.valid.sum()) for p in episode.packets
            ),
            "effective_valid_feature_observations": sum(
                int(effective_packet(p, t, intervention).valid.sum())
                for t, p in enumerate(episode.packets)
            ),
            "cue_presentations": sum(p.cue_present for p in episode.packets),
            "sensory_corrections_including_replay": total_work.sensory_corrections,
            "replayed_packets": total_work.replay_packets,
        },
        "events": events,
        "metrics": metrics,
        "live_work": total_work.to_dict(),
        "prediction_work": prediction_work.to_dict(),
        "timings": {
            **timings,
            **{f"prediction_{k}": v for k, v in prediction_work.timings().items()},
            "wall_seconds": time.perf_counter() - wall_start,
            "cpu_seconds": time.process_time() - cpu_start,
        },
        "history_peak_logical_bytes": max_history_bytes,
        "trajectory_tensor_bytes": sum(t.numel() * t.element_size() for t in arrays.values()),
        "persistent_fingerprint_before": before,
        "persistent_fingerprint_after": before,
    }


def nmse(predicted, truth):
    return float(
        (predicted.double() - truth.double()).square().sum()
        / truth.double().square().sum().clamp_min(1e-12)
    )


def angular_rmse(predicted, phase, projection):
    planar = predicted.double() @ projection.double()
    angles = torch.atan2(planar[..., 1], planar[..., 0])
    errors = torch.remainder(angles - phase + math.pi, 2 * math.pi) - math.pi
    errors = torch.where(planar.norm(dim=-1) < 1e-6, math.pi, errors)
    return float(errors.square().mean().sqrt())


def first_capture(weights, target, onset, last, threshold=0.9, consecutive=3):
    count = 0
    for t in range(onset, min(last + 1, len(weights))):
        count = count + 1 if weights[t, target] >= threshold else 0
        if count >= consecutive:
            return t
    return None


def score(model, episode, arrays, events):
    """All target identities, future observations, and phase truth stop at this boundary."""
    estimates, attended, weights = arrays["estimate"], arrays["attended"], arrays["weights"]
    per_event = []
    for onset, name in model.protocol["environment"]["requests"][1:]:
        target = "AB".index(name)
        source = 1 - target
        commits = [
            e["frame"]
            for e in events
            if e["kind"] == "commit" and e["bank"] == target and onset <= e["frame"] <= onset + 16
        ]
        commit = commits[0] if commits else None
        capture = first_capture(weights, target, onset, onset + 16)
        success = bool(
            attended[onset - 1] == source
            and commit is not None
            and commit - onset <= 8
            and torch.all(attended[commit : commit + 8] == target)
        )
        prediction, truth = (
            estimates[onset : onset + 8, target],
            episode.true_features[onset : onset + 8, target],
        )
        per_event.append(
            {
                "onset": onset,
                "source": source,
                "target": target,
                "success": success,
                "commit_delay": None if commit is None else commit - onset,
                "censored_delay": 16 if commit is None else commit - onset,
                "key_capture_delay": None if capture is None else capture - onset,
                "key_capture_success": capture is not None,
                "key_retained_after_cue": bool(
                    torch.all(weights[onset + 4 : onset + 12, target] >= 0.9)
                ),
                "continuity_nmse": nmse(prediction, truth),
                "continuity_angular_rmse": angular_rmse(
                    prediction, episode.phases[onset : onset + 8, target], model.encoder.matrix
                ),
                "source_retention": {
                    str(offset): {
                        "nmse": nmse(
                            estimates[onset + offset, source],
                            episode.true_features[onset + offset, source],
                        ),
                        "angular_rmse": angular_rmse(
                            estimates[onset + offset, source],
                            episode.phases[onset + offset, source],
                            model.encoder.matrix,
                        ),
                        "source_readout_available": model.variant != "A1",
                        "separate_state_banks": model.variant in ("A2", "G2"),
                    }
                    for offset in (8, 16)
                },
            }
        )
    outside = torch.arange(len(attended)) >= 16
    for onset in (48, 96, 144):
        outside[onset : onset + 16] = False
    false = (attended >= 0) & (attended != episode.requested)
    prediction = {
        "grounded_one_step_nmse": [
            nmse(arrays["one_step"][:, i], episode.true_features[1:, i]) for i in range(2)
        ]
    }
    for anchor in model.protocol["evaluation"]["prediction_anchors"]:
        for horizon in model.protocol["evaluation"]["free_horizons"]:
            key = f"anchor{anchor}_h{horizon}"
            prediction[key] = [
                nmse(arrays[key][:, i], episode.true_features[anchor + 1 : anchor + horizon + 1, i])
                for i in range(2)
            ]
    role_window = arrays["roles"][20:44]
    desired = torch.tensor([3, 2, 1])
    return {
        "events": per_event,
        "event_success_fraction": np.mean([e["success"] for e in per_event]).item(),
        "false_committed_occupancy": float(false[outside].float().mean()),
        "unsupported_commits": sum(e["kind"] == "commit" and e["bank"] == 2 for e in events),
        "abstention_frames": int((attended < 0).sum()),
        "role_concurrency_fraction": float(torch.all(role_window == desired, dim=1).float().mean()),
        "prediction": prediction,
        "feature_motion_energy": float((estimates[1:] - estimates[:-1]).double().square().mean()),
        "spontaneous_key_transitions": int(
            (
                (weights.argmax(1)[1:] != weights.argmax(1)[:-1])
                & ~torch.tensor([p.cue_present for p in episode.packets[1:]])
            ).sum()
        ),
        "mixed_key_frames": int((weights.max(1).values < 0.9).sum()),
        "key_template_distance_mean": (arrays["key"][:, None, :] - model.patterns.T[None])
        .norm(dim=-1)
        .mean(0)
        .tolist()
        if model.analytic
        else None,
        "winner_margin_mean": float(
            (weights.topk(2, dim=1).values[:, 0] - weights.topk(2, dim=1).values[:, 1]).mean()
        ),
    }
