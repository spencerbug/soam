"""Paired D1/D2 execution; evaluation owns targets and never writes memory."""

import hashlib
import time

import numpy as np
import torch

from .data import Cue, core_probes, objects, queries, records
from .models import Memory


def array_hash(arrays):
    h = hashlib.sha256()
    for key, value in sorted(arrays.items()):
        x = np.ascontiguousarray(value)
        h.update(key.encode())
        h.update(str(x.dtype).encode())
        h.update(str(x.shape).encode())
        h.update(x.tobytes())
    return h.hexdigest()


def core_error(core, root, denominator):
    y, actions, truth = core_probes(root)
    predicted = []
    for a in actions.T:
        y = core.advance(y, a)
        predicted.append(y.clone())
    return float(np.mean((torch.stack(predicted, 1).numpy() - truth[:, 1:]) ** 2) / denominator)


def reduce(arrays):
    d1, d2 = arrays["d1_error"], arrays["d2_error"]
    final = d2[:, -1, :-1, :, 1:].mean((2, 3))
    initial = np.stack([d2[:, i, i, :, 1:].mean((1, 2)) for i in range(7)], 1)
    return {
        "J": float(d1[1:, :, :, 1:].mean()),
        "one_shot": float(d1[1, :, :, 1:].mean()),
        "error8": float(d1[-1, :, :, 1:].mean()),
        "accuracy8": float((d1[-1, :, :, 0] <= 0.1).mean()),
        "retention": float((final - initial).mean()),
        "old_error": float(final.mean()),
        "old_accuracy": float((d2[:, -1, :-1, :, 0] <= 0.1).mean()),
        "known_acceptance": float(arrays["d2_accept"][:, -1].mean()),
        "accepted_wrong": float((arrays["d2_accept"][:, -1] & (d2[:, -1, :, :, 0] > 0.1)).mean()),
        "false_familiarity": float(arrays["unknown_accept"].mean()),
        "curves": {
            str(b): {
                "canonical": float(d1[i, :, :, 0].mean()),
                "free1": float(d1[i, :, :, 1].mean()),
                "free4": float(d1[i, :, :, 1:5].mean()),
                "free8": float(d1[i, :, :, 1:].mean()),
                "accuracy": float((d1[i, :, :, 0] <= 0.1).mean()),
            }
            for i, b in enumerate((0, 1, 2, 4, 8))
        },
    }


def evaluate(name, core, setting, root, split, denominator, threshold=1e30, check=lambda: None):
    a = {}
    for prefix, leading in (("d1", (5, 24)), ("d2", (4, 8, 8)), ("unknown", (4, 8))):
        a[prefix + "_pred"] = np.zeros((*leading, 8, 9, 8))
        a[prefix + "_scores"] = np.zeros((*leading, 8))
        a[prefix + "_accept"] = np.zeros((*leading, 8), dtype=bool)
    a["d1_truth"] = np.zeros((24, 8, 9, 8))
    a["d2_truth"] = np.zeros((4, 8, 8, 9, 8))
    a["unknown_truth"] = np.zeros((4, 8, 8, 9, 8))
    inputs, end_memories, write_ns = {}, {}, []

    def query(memory, obj, ident, prefix, index):
        cue, action, truth = queries(obj, root, split, ident)
        pred, scores, accepted = memory.rollout(cue, action)
        a[prefix + "_pred"][index] = pred.numpy()
        a[prefix + "_scores"][index] = scores.numpy()
        a[prefix + "_accept"][index] = accepted.numpy()
        inputs[str(ident) + "/cue"] = cue.features.numpy()
        inputs[str(ident) + "/mask"] = cue.mask.numpy()
        inputs[str(ident) + "/actions"] = action.numpy()
        return truth

    def write(memory, recs, identity):
        for j, rec in recs:
            inputs[str(identity) + f"/record{j}"] = np.r_[
                rec.key.numpy(), rec.features.numpy(), rec.angle
            ]
            start = time.perf_counter_ns()
            memory.acquire(rec, grounded=True)
            write_ns.append(time.perf_counter_ns() - start)

    for i in range(24):
        obj = objects(root, split + "/d1", i, 1)[0]
        recs = records(obj, root, split, ("d1", i))
        memory = Memory(name, core, setting, threshold)
        previous = 0
        for bi, budget in enumerate((0, 1, 2, 4, 8)):
            write(memory, list(enumerate(recs))[previous:budget], ("d1", i))
            previous = budget
            a["d1_truth"][i] = query(memory, obj, ("d1", i), "d1", (bi, i))
        end_memories[f"d1/{i}"] = memory.fingerprint()
        check()
    for sequence in range(4):
        objs = objects(root, split + "/d2", sequence, 16)
        memory = Memory(name, core, setting, threshold)
        for stage, obj in enumerate(objs[:8]):
            recs = records(obj, root, split, ("d2", sequence, stage))
            write(memory, list(enumerate(recs)), ("d2", sequence, stage))
            for old, other in enumerate(objs[: stage + 1]):
                a["d2_truth"][sequence, old] = query(
                    memory, other, ("d2", sequence, old), "d2", (sequence, stage, old)
                )
            check()
        for i, obj in enumerate(objs[8:]):
            a["unknown_truth"][sequence, i] = query(
                memory, obj, ("unknown", sequence, i), "unknown", (sequence, i)
            )
        end_memories[f"d2/{sequence}"] = memory.fingerprint()
    a["d1_error"] = ((a["d1_pred"] - a["d1_truth"][None]) ** 2).mean(-1) / denominator
    a["d2_error"] = ((a["d2_pred"] - a["d2_truth"][:, None]) ** 2).mean(-1) / denominator
    # Unacquired cells are structurally absent, not failed/zero-error trials.
    valid = np.tri(8, dtype=bool)
    a["d2_valid"] = valid
    a["d2_error"][:, ~valid] = 0
    a["unknown_error"] = ((a["unknown_pred"] - a["unknown_truth"]) ** 2).mean(-1) / denominator
    if not all(np.isfinite(x).all() for x in a.values()):
        raise RuntimeError("Nonfinite scientific output")
    cue, _, _ = queries(objs[0], root, split, ("profile", 0))
    times = []
    single = Cue(cue.features[:1], cue.mask[:1])
    for j in range(23):
        start = time.perf_counter_ns()
        memory.recall(single)
        if j >= 3:
            times.append((time.perf_counter_ns() - start) / 1000)
    result = reduce(a)
    result.update(
        {
            "input_hash": array_hash(inputs),
            "numeric_hash": array_hash(a),
            "memory_hashes": end_memories,
            "resources": memory.resources(),
            "write_us_mean": float(np.mean(write_ns) / 1000),
            "write_us_p95": float(np.quantile(write_ns, 0.95) / 1000),
            "recall_us_mean": float(np.mean(times)),
            "recall_us_p95": float(np.quantile(times, 0.95)),
            "grounded_snapshots": len(write_ns),
            "query_count": 2368,
            "normalization": denominator,
            "core_probe": core_error(core, root, denominator),
        }
    )
    return result, a, inputs, memory.snapshot()
