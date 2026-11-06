"""Unfitted, shape-equivalent E1 calibration. Never performs optimizer updates."""

import io
import json
import time

import numpy as np
import torch

from soam.platform.core import model_fingerprint
from soam.shared.data import SharedTask, observed_batch
from soam.shared.evaluation import Probe, evaluate
from soam.shared.fitting import RidgeMoments, bilinear_inputs, losses
from soam.shared.models import Candidate, TiedStateCandidate, manifest


def calibrate(path, budget, *, archive_revision="v1"):
    protocol = manifest()
    task = SharedTask()
    timings = {}

    def time_operation(name, operation):
        cpu, wall = [], []
        for index in range(11):
            budget.check()
            c, w = time.process_time(), time.perf_counter()
            operation()
            elapsed_cpu, elapsed_wall = time.process_time() - c, time.perf_counter() - w
            budget.check()
            if index:
                cpu.append(elapsed_cpu)
                wall.append(elapsed_wall)
        timings[name] = {
            "cpu_samples": cpu,
            "wall_samples": wall,
            "warmup_operations": 1,
            "measured_operations": 10,
            "cpu_max": max(cpu),
            "wall_max": max(wall),
        }

    # Full batch/horizon shapes, exclusively isolated engineering stream keys.
    if archive_revision not in ("v1", "a1"):
        raise ValueError("unknown archive revision")
    packet_sets = {}
    for role, update in (("recall", 0), ("transition", 100)):

        def generate(role=role, update=update):
            return tuple(
                task.episode("fixture/train", 9001, update * 16 + i, role) for i in range(16)
            )

        time_operation(f"generate-{role}", generate)
        packet_sets[role] = generate()
    recall, transition = (observed_batch(packet_sets[r], r) for r in ("recall", "transition"))
    eval_episodes = {
        r: task.episode("fixture/evaluation", 9001, 0, r) for r in ("recall", "transition")
    }
    models = {r["id"]: Candidate(r["id"], 9001) for r in protocol["models"]}

    for family, model in models.items():
        before = model_fingerprint(model)
        if family != "L12":
            for stage in ("recall", "joint"):

                def backward(model=model, stage=stage):
                    model.zero_grad(set_to_none=True)
                    terms = losses(model, recall, transition if stage == "joint" else None)
                    total = terms["recall"] + terms.get("free", 0) + 0.3 * terms.get("grounded", 0)
                    total.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
                    model.zero_grad(set_to_none=True)

                time_operation(f"backward-{family}-{stage}", backward)
        else:
            for role in ("recall", "transition"):

                def ridge(role=role):
                    moments = RidgeMoments(25 if role == "recall" else 52)
                    if role == "recall":
                        z = recall.initial.z
                        x = torch.cat(
                            (z, recall.initial.valid.float(), torch.ones_like(z[:, :1])), 1
                        )
                        moments.add(x, recall.clean[0])
                    else:
                        moments.add(
                            bilinear_inputs(transition.clean[:-1], transition.actions),
                            transition.clean[1:],
                        )
                    # Includes a solve per batch, conservatively exceeding actual two-stage solves.
                    moments.solve(0.0001)

                time_operation(f"ridge-{role}", ridge)
        for role, episode in eval_episodes.items():
            time_operation(
                f"evaluate-{family}-{role}",
                lambda model=model, episode=episode: evaluate(model, episode, 0.04),
            )
        if model_fingerprint(model) != before:
            raise RuntimeError("preflight mutated parameters")
    tied = TiedStateCandidate(models["S32"])
    for role, episode in eval_episodes.items():
        for kind in ("intact", "full_clamp", "readout_clamp"):
            model = models["S32"] if kind == "readout_clamp" else tied
            probe = Probe(kind, (0, 1, 2, 3)) if kind != "intact" else Probe()
            time_operation(
                f"diagnostic-{kind}-{role}",
                lambda model=model, episode=episode, probe=probe: evaluate(
                    model, episode, 0.04, probe
                ),
            )

    # Measure actual archive preparation, serialization AND bounded disk writes.
    # Batch records include all stream keys, observed packets, clean records and truth.
    from soam.shared.runner import archive_episodes

    for role, episodes in packet_sets.items():
        counter = [0]

        def write_batch(role=role, episodes=episodes, counter=counter):
            counter[0] += 1
            if archive_revision == "a1":
                from soam.shared.archive import InputStore, verify_contract

                verify_contract()
                # Fresh store each operation: measure hashing and physical writes.
                store = InputStore(path / "calibration-objects" / f"{role}-{counter[0]}", budget)
                store.write(path / "calibration-data" / f"{role}-{counter[0]}", episodes)
            else:
                archive_episodes(path / "calibration-data" / role, episodes, budget)

        time_operation(f"archive-batch-{role}", write_batch)
    arrays, record = evaluate(tied, eval_episodes["transition"], 0.04)

    def archive_cell():
        budget.arrays(path / "calibration-cell.npz", arrays)
        budget.json(path / "calibration-cell.json", record)

    time_operation("archive-cell", archive_cell)

    # Uncompressed sizes avoid optimistic compression estimates for learned arrays.
    def npz_size(values):
        out = io.BytesIO()
        np.savez(out, **{k: v.detach().numpy() for k, v in values.items()})
        return len(out.getvalue())

    batch_bytes = {}
    for role, episodes in packet_sets.items():
        observed = {
            k: torch.cat([e.observed_arrays()[k] for e in episodes], 1)
            for k in episodes[0].observed_arrays()
        }
        batch_bytes[role] = sum(
            (
                npz_size(observed),
                npz_size({"features": torch.cat([e.clean_records for e in episodes], 1)}),
                npz_size(
                    {
                        "features": torch.cat([e.targets.features for e in episodes], 1),
                        "world": torch.stack([e.targets.world for e in episodes], 1),
                    }
                ),
                len(json.dumps([e.stream_seeds for e in episodes], indent=2).encode()),
            )
        )
    # One maximum-width transition payload plus corresponding observations, truth,
    # stream keys and metadata for EVERY cell, including short recall paths.
    cell_bytes = npz_size(arrays) + batch_bytes["transition"] + 8192
    checkpoint_bytes = (
        max(sum(p.numel() * 4 for p in m.parameters()) for m in models.values()) * 8 + 65536
    )
    per_fit_bytes = (
        400 * batch_bytes["recall"]
        + 300 * batch_bytes["transition"]
        + checkpoint_bytes
        + 400 * 1024
    )

    def cost(name, clock):
        return timings[name][clock + "_max"]

    projections = {}
    for clock in ("cpu", "wall"):
        fit_cost = {}
        for family in models:
            if family == "L12":
                pre = cost("ridge-recall", clock)
                joint = pre + cost("ridge-transition", clock)
            else:
                pre = cost(f"backward-{family}-recall", clock)
                joint = cost(f"backward-{family}-joint", clock)
            data_r = cost("generate-recall", clock) + cost("archive-batch-recall", clock)
            data_t = cost("generate-transition", clock) + cost("archive-batch-transition", clock)
            # Explicit allowance for Adam/bookkeeping/checkpoint work not exercised
            # by unfitted backward calibration, then the global 2x margin applies.
            fit_cost[family] = (
                100 * pre + 300 * joint + 400 * data_r + 300 * data_t + 400 * 0.005 + 1.0
            )
        eval_max = max(
            value[clock + "_max"]
            for key, value in timings.items()
            if key.startswith(("evaluate-", "diagnostic-"))
        ) + cost("archive-cell", clock)
        phase = {}
        for name, per_family, diagnostics in (
            ("development", 6, 0),
            ("confirmation", 10, 18800),
            ("repeat", 1, 1880),
        ):
            phase[name] = 2 * (
                sum(fit_cost.values()) * per_family + (per_family * 7 * 60 + diagnostics) * eval_max
            )
        # Full normalization + aggregation, construction, bootstrap, filesystem and
        # metadata work: reserve the complete frozen overhead allocation.
        phase["overhead"] = 1200.0
        projections[clock] = {
            "per_fit_with_margin": {k: 2 * v for k, v in fit_cost.items()},
            "phases_with_margin": phase,
            "total_with_margin": sum(phase.values()),
            "evaluation_cell_max_plus_archive": eval_max,
        }
    artifact_bytes = 2 * (119 * per_fit_bytes + 27820 * cell_bytes + 64 * 1024**2)
    if archive_revision == "a1":
        training_bytes = 400 * batch_bytes["recall"] + 300 * batch_bytes["transition"]
        unique_inputs = 13 * (training_bytes + 700 * 4096)
        per_fit_outputs = checkpoint_bytes + 400 * 1024 + 700 * 1024
        artifact_bytes = 2 * (
            unique_inputs + 119 * per_fit_outputs + 27820 * cell_bytes + 64 * 1024**2
        )
    current = budget.measurements()
    cpu = projections["cpu"]
    checks = {
        "per_fit": all(v <= 90 for v in cpu["per_fit_with_margin"].values()),
        "development": cpu["phases_with_margin"]["development"] <= 4000,
        "confirmation": cpu["phases_with_margin"]["confirmation"] <= 8000,
        "repeat": cpu["phases_with_margin"]["repeat"] <= 1200,
        "total_cpu": cpu["total_with_margin"] <= 14400,
        "total_wall": projections["wall"]["total_with_margin"] <= 28800,
        "artifact_bytes": artifact_bytes <= 8 * 1024**3,
        "peak_rss_with_margin": 2 * current["peak_rss_bytes"] <= 2 * 1024**3,
    }
    ledger = {
        "engineering_only": True,
        "archive_revision": archive_revision,
        "optimizer_updates": 0,
        "study_fits": 0,
        "timings": timings,
        "projections": projections,
        "projected_artifact_bytes_with_margin": artifact_bytes,
        "observed_peak_rss_bytes": current["peak_rss_bytes"],
        "peak_rss_projection_safety_factor": 2,
        "checks": checks,
        "feasible": all(checks.values()),
        "safety_factor": 2,
        "inventory": protocol["inventory"],
        "batch_bytes_uncompressed": batch_bytes,
        "cell_bytes_upper_estimate": cell_bytes,
        "timing_statistic": "maximum of ten after one warmup",
        "scope": "shape-equivalent calibration; full-study runtime must still enforce all ceilings",
        "failure_action": "new protocol decision/version before fitting; no silent reduction",
    }
    budget.json(path / "cost-ledger.json", ledger)
    return {k: v for k, v in ledger.items() if k != "timings"}
