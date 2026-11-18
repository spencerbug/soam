"""Evaluator-owned paired tasks, snapshots and reductions for frozen D-R1."""

import time

import numpy as np
import torch

from soam.acquisition.data import Cue
from soam.acquisition.engine import array_hash
from soam.temporal.runner import tensor_hash

from .data import core_probes, objects, queries, records, rng, tensor
from .models import RetrievalMemory

CONDITIONS = ("full", "partial")
BUDGETS = (0, 1, 2, 4, 8)


def core_error(core, root, denominator):
    y, actions, truth = core_probes(root)
    pred = []
    for action in actions.T:
        y = core.advance(y, action)
        pred.append(y.clone())
    return float(np.mean((torch.stack(pred, 1).numpy() - truth[:, 1:]) ** 2) / denominator)


def rollout(core, value, actions):
    pred = [value.clone()]
    for action in actions.T:
        value = core.advance(value, action)
        pred.append(value.clone())
    return torch.stack(pred, 1).numpy()


def empty_arrays():
    arrays = {}
    for pre, leading in (("d1", (5, 24)), ("d2", (4, 8, 8)), ("unknown", (4, 8))):
        arrays[pre + "_pred"] = np.zeros((2, *leading, 8, 9, 8))
        arrays[pre + "_scores"] = np.zeros((2, *leading, 8))
    arrays["d1_truth"] = np.zeros((24, 8, 9, 8))
    arrays["d2_truth"] = np.zeros((4, 8, 8, 9, 8))
    arrays["unknown_truth"] = np.zeros((4, 8, 8, 9, 8))
    arrays["d2_valid"] = np.tri(8, dtype=bool)
    return arrays


def reduce(arrays, thresholds=None):
    thresholds = thresholds or {c: 1e30 for c in CONDITIONS}
    result = {}
    for ci, condition in enumerate(CONDITIONS):
        d1, d2 = arrays["d1_error"][ci], arrays["d2_error"][ci]
        final = d2[:, -1, :-1, :, 1:].mean((2, 3))
        initial = np.stack([d2[:, i, i, :, 1:].mean((1, 2)) for i in range(7)], 1)
        known_error = d2[:, -1, :-1, :, 0]
        known_scores = arrays["d2_scores"][ci, :, -1, :-1]
        accepted = (known_scores <= thresholds[condition]) & (known_scores < np.finfo(float).max)
        unknown_scores = arrays["unknown_scores"][ci]
        unknown = (unknown_scores <= thresholds[condition]) & (unknown_scores < np.finfo(float).max)
        wrong = known_error > 0.1
        n_accept = int(accepted.sum())
        result[condition] = {
            "J": float(d1[1:, :, :, 1:].mean()),
            "one_shot": float(d1[1, :, :, 1:].mean()),
            "error8": float(d1[-1, :, :, 1:].mean()),
            "accuracy8": float((d1[-1, :, :, 0] <= 0.1).mean()),
            "old_error": float(final.mean()),
            "old_accuracy": float((~wrong).mean()),
            "retention": float((final - initial).mean()),
            "known_coverage": float(accepted.mean()),
            "accepted_wrong": float((accepted & wrong).mean()),
            "unknown_acceptance": float(unknown.mean()),
            "accepted_accuracy": float((accepted & ~wrong).sum() / n_accept) if n_accept else None,
            "conditional_wrong": float((accepted & wrong).sum() / n_accept) if n_accept else None,
            "known_queries": int(wrong.size),
            "accepted_queries": n_accept,
            "unknown_queries": int(unknown.size),
            "curves": {
                str(b): {
                    "canonical": float(d1[i, :, :, 0].mean()),
                    "free1": float(d1[i, :, :, 1].mean()),
                    "free4": float(d1[i, :, :, 1:5].mean()),
                    "free8": float(d1[i, :, :, 1:].mean()),
                    "accuracy": float((d1[i, :, :, 0] <= 0.1).mean()),
                }
                for i, b in enumerate(BUDGETS)
            },
        }
    return result


def evaluate(name, core, setting, root, split, denominator, check=lambda: None):
    """PH-1 is read from the same PH trace, with no independent acquired state."""
    names = [name, "PH-1"] if name == "PH-FULL" else [name]
    arrays = {n: empty_arrays() for n in names}
    inputs, memory_hashes, write_ns, recall_ns = {}, {}, [], []
    core_before = tensor_hash({"a": core.a, "b": core.b})
    traces = {
        k: []
        for k in (
            "values",
            "energy",
            "scores",
            "changes",
            "cycles",
            "converged",
            "truth",
            "ids",
            "elapsed",
            "perturb_values",
            "perturb_counts",
            "perturb_cycles",
            "perturb_converged",
            "perturb_energy",
        )
    }
    saturation = {
        "acquired_key_outside": 0,
        "acquired_value_outside": 0,
        "acquired_key_coordinates": 0,
        "acquired_value_coordinates": 0,
        "query_key_outside": 0,
        "query_visible_coordinates": 0,
    }
    ranks = []

    def write(memory, recs, identity):
        for j, record in recs:
            inputs[f"{identity}/record{j}"] = np.r_[
                record.key.numpy(), record.features.numpy(), record.angle
            ]
            value = core.advance(record.features, -record.angle)
            saturation["acquired_key_outside"] += int((record.key.abs() > 4).sum())
            saturation["acquired_value_outside"] += int((value.abs() > 1.5).sum())
            saturation["acquired_key_coordinates"] += 16
            saturation["acquired_value_coordinates"] += 8
            start = time.perf_counter_ns()
            memory.acquire(record, grounded=True)
            write_ns.append(time.perf_counter_ns() - start)
            if name == "PH-FULL":
                ranks.append(int(memory.buffers["rank"]))

    def query(memory, obj, ident, pre, index, final=False):
        cues, actions, truth = queries(obj, root, split, ident)
        before = memory.fingerprint()
        for ci, condition in enumerate(CONDITIONS):
            cue = cues[condition]
            inputs[f"{ident}/{condition}/cue"] = cue.features.numpy()
            inputs[f"{ident}/{condition}/mask"] = cue.mask.numpy()
            inputs[f"{ident}/actions"] = actions.numpy()
            saturation["query_key_outside"] += int((cue.features[cue.mask].abs() > 4).sum())
            saturation["query_visible_coordinates"] += int(cue.mask.sum())
            start = time.perf_counter_ns()
            value, scores, _ = memory.recall(cue)
            recall_ns.append(time.perf_counter_ns() - start)
            outputs = {name: (value, scores)}
            if name == "PH-FULL":
                outputs["PH-1"] = (memory.trace["values"][0], memory.trace["scores"][0])
                for k in ("values", "energy", "scores", "changes", "elapsed"):
                    item = memory.trace[k].numpy()
                    padded = np.repeat(item[-1:], 32, axis=0)
                    padded[: len(item)] = item
                    traces[k].append(padded)
                traces["cycles"].append(memory.trace["cycles"].numpy())
                traces["converged"].append(memory.trace["converged"].numpy())
                traces["truth"].append(truth[:, 0])
                traces["ids"].append(
                    np.array(
                        [
                            {"d1": 0, "d2": 1, "unknown": 2}[pre],
                            ci,
                            *(list(index) + [-1] * (3 - len(index))),
                        ]
                    )
                )
            for n, (val, score) in outputs.items():
                arrays[n][pre + "_pred"][(ci, *index)] = rollout(core, val, actions)
                # Empty memory always rejects even at a very large diagnostic threshold.
                score = score.numpy().copy()
                if name == "NOWRITE" or int(memory.buffers["count"]) == 0:
                    score[:] = np.finfo(np.float64).max
                arrays[n][pre + "_scores"][(ci, *index)] = score
            if name == "PH-FULL" and final:
                uniform = tensor(
                    rng(root, split, "perturbation", ident, condition).random((8, 768))
                )
                val, _, _ = memory.recall(cue, perturb_uniform=uniform)
                traces["perturb_values"].append(val.numpy())
                traces["perturb_counts"].append(memory.trace["perturb_count"].numpy())
                traces["perturb_cycles"].append(memory.trace["cycles"].numpy())
                traces["perturb_converged"].append(memory.trace["converged"].numpy())
                energy = memory.trace["energy"].numpy()
                padded = np.repeat(energy[-1:], 32, axis=0)
                padded[: len(energy)] = energy
                traces["perturb_energy"].append(padded)
                # Dedicated prefix keeps intervention targets explicit, without giving them to memory.
                inputs[f"{ident}/{condition}/perturb_uniform"] = uniform.numpy()
        if memory.fingerprint() != before:
            raise RuntimeError("Query/rollout changed persistent tensors")
        return truth

    for i in range(24):
        obj = objects(root, split + "/d1", i, 1)[0]
        recs = records(obj, root, split, ("d1", i))
        memory = RetrievalMemory(name, core, setting)
        previous = 0
        for bi, budget in enumerate(BUDGETS):
            write(memory, list(enumerate(recs))[previous:budget], ("d1", i))
            previous = budget
            truth = query(memory, obj, ("d1", i), "d1", (bi, i))
            for a in arrays.values():
                a["d1_truth"][i] = truth
        memory_hashes[f"d1/{i}"] = memory.fingerprint()
        check()
    for sequence in range(4):
        objs = objects(root, split + "/d2", sequence, 16)
        memory = RetrievalMemory(name, core, setting)
        for stage, obj in enumerate(objs[:8]):
            write(
                memory,
                list(enumerate(records(obj, root, split, ("d2", sequence, stage)))),
                ("d2", sequence, stage),
            )
            for old, other in enumerate(objs[: stage + 1]):
                truth = query(
                    memory,
                    other,
                    ("d2", sequence, old),
                    "d2",
                    (sequence, stage, old),
                    final=stage == 7,
                )
                for a in arrays.values():
                    a["d2_truth"][sequence, old] = truth
            check()
        for i, obj in enumerate(objs[8:]):
            truth = query(memory, obj, ("unknown", sequence, i), "unknown", (sequence, i))
            for a in arrays.values():
                a["unknown_truth"][sequence, i] = truth
        memory_hashes[f"d2/{sequence}"] = memory.fingerprint()
        check()
    for n, a in arrays.items():
        a["d1_error"] = ((a["d1_pred"] - a["d1_truth"][None, None]) ** 2).mean(-1) / denominator
        a["d2_error"] = ((a["d2_pred"] - a["d2_truth"][None, :, None]) ** 2).mean(-1) / denominator
        a["d2_error"][:, :, ~a["d2_valid"]] = 0
        a["unknown_error"] = ((a["unknown_pred"] - a["unknown_truth"][None]) ** 2).mean(
            -1
        ) / denominator
        if not all(np.isfinite(x).all() for x in a.values()):
            raise RuntimeError("Nonfinite output")
    if name == "PH-FULL":
        arrays[name].update({"trace_" + k: np.stack(v) for k, v in traces.items()})
        arrays[name]["write_ranks"] = np.array(ranks)
    # Measured serial latency on existing observations, not extra data or writes.
    cues, _, _ = queries(objs[0], root, split, ("profile", 0))
    timings = []
    for condition in CONDITIONS:
        cue = cues[condition]
        single = Cue(cue.features[:1], cue.mask[:1])
        for i in range(8):
            start = time.perf_counter_ns()
            memory.recall(single)
            timings.append((time.perf_counter_ns() - start) / 1000)
    if core_before != tensor_hash({"a": core.a, "b": core.b}):
        raise RuntimeError("Core changed")
    # Grounded predictions are evaluated in a separate path on already saved current observations.
    truth = arrays[name]["d1_truth"]
    action_arrays = np.stack([inputs[f"{('d1', i)}/actions"] for i in range(24)])
    grounded = core.advance(tensor(truth[:, :, :-1]), tensor(action_arrays)).numpy()
    common = {
        "input_hash": array_hash({k: v for k, v in inputs.items() if "perturb_uniform" not in k}),
        "memory_hashes": memory_hashes,
        "resources": memory.resources(),
        "write_us_mean": float(np.mean(write_ns) / 1000),
        "write_us_p95": float(np.quantile(write_ns, 0.95) / 1000),
        "recall_batch_us_mean": float(np.mean(recall_ns) / 1000),
        "serial_recall_us_mean": float(np.mean(timings)),
        "serial_recall_us_p95": float(np.quantile(timings, 0.95)),
        "serial_queries_per_second": float(1e6 / np.mean(timings)),
        "distinct_grounded_snapshots": len(write_ns),
        "query_count_per_arm": 4736,
        "normalization": denominator,
        "core_probe": core_error(core, root, denominator),
        "grounded_one_step_nmse": float(((grounded - truth[:, :, 1:]) ** 2).mean() / denominator),
        "saturation": saturation,
        "core_hash": core_before,
    }
    results = {}
    for n, a in arrays.items():
        results[n] = {
            **common,
            "metrics": reduce(a),
            "numeric_hash": array_hash({k: v for k, v in a.items() if k != "trace_elapsed"}),
        }
        if n == "PH-1":
            results[n]["latency_note"] = (
                "Acquired state shared; per-cycle elapsed values in PH-FULL trace."
            )
    return results, arrays, inputs, memory.snapshot()
