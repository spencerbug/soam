"""Ordinary inference first; privileged code scoring has no model access."""

import time

import numpy as np
import torch

from soam.acquisition.models import Core
from soam.retrieval import data
from soam.retrieval.models import RetrievalMemory, decode, encode
from soam.temporal.runner import tensor_hash

NAMESPACE = "soam-study-d-r2-v1"
ARMS = ("PH-FULL", "KV", "REG-LIFT")


def stream_root(root):
    return f"{NAMESPACE}:{root}"


def acquired_code(core, record):
    """Evaluator reconstruction from actual observations, without a target."""
    value = core.advance(record.features, -record.angle)
    return torch.cat((encode(record.key, 4), encode(value, 1.5)))


def predict(memory, cue, actions):
    """The entire learner path: no evaluator identity, code, or truth arguments."""
    before = memory.fingerprint()
    memory.reset(len(cue.features))
    started = time.perf_counter()
    value, score, _ = memory.recall(cue)
    elapsed = time.perf_counter() - started
    state = memory.state.detach().numpy().copy()
    values = [value.clone()]
    for action in actions.T:
        value = memory.core.advance(value, action)
        values.append(value.clone())
    if memory.fingerprint() != before:
        raise RuntimeError("Ordinary prediction changed persistent memory")
    return torch.stack(values, 1).numpy(), score.numpy(), state, elapsed


def diagnostic(states, codes, masks, truth, denominator):
    """Pure array evaluator. Never returns an input to a learner operation."""
    # Every acquired snapshot receives equal weight; no target-based code choice.
    exact = codes[:-1, :, 512:].astype(np.float64).reshape(len(states), -1, 8, 32)
    exact = exact.mean(-1) * 1.5
    exact_error = ((exact[:, None] - truth[:, :, None]) ** 2).mean(-1) / denominator
    same, other = [], []
    for index, state in enumerate(states):
        free = np.ones_like(state, dtype=bool)
        free[:, :512] = ~np.repeat(masks[index], 32, axis=1)
        distances = (
            (state[:, None, None] - codes[None].astype(np.float64)) ** 2 * free[:, None, None]
        ).sum(-1) / (4 * free.sum(-1)[:, None, None])
        same.append(distances[:, index].min(-1))
        alternatives = np.arange(len(codes)) != index
        other.append(distances[:, alternatives].min((1, 2)))
    relation = states[..., 512:].reshape(*states.shape[:-1], 8, 32)
    nonmonotone = (np.diff(relation, axis=-1) > 0).any((-1, -2))
    return {
        "exact_values": exact,
        "exact_error": exact_error,
        "same_code_discrepancy": np.stack(same),
        "other_code_discrepancy": np.stack(other),
        "nonmonotone": nonmonotone,
    }


def metrics(arrays, denominator):
    result = {}
    for name in ARMS:
        errors = ((arrays[f"{name}_pred"] - arrays["truth"]) ** 2).mean(-1) / denominator
        result[f"{name}_accuracy"] = float((errors[..., 0] <= 0.1).mean())
        result[f"{name}_canonical_nmse"] = float(errors[..., 0].mean())
        result[f"{name}_free1_nmse"] = float(errors[..., 1].mean())
        result[f"{name}_free8_nmse"] = float(errors[..., 1:].mean())
    result["exact_accuracy"] = float((arrays["exact_error"] <= 0.1).mean())
    result["exact_nmse"] = float(arrays["exact_error"].mean())
    result["gap"] = result["exact_accuracy"] - result["PH-FULL_accuracy"]
    for key in ("same_code_discrepancy", "other_code_discrepancy", "nonmonotone", "cycles"):
        result[key] = float(arrays[key].mean())
    result["nonconvergence"] = float((~arrays["converged"]).mean())
    result["wrong_object_closer"] = float(
        (arrays["other_code_discrepancy"] < arrays["same_code_discrepancy"]).mean()
    )
    return result


def run_root(root, manifest, dest, check):
    """One fixed root, sharing its training and grounded acquisitions across arms."""
    started = time.process_time()
    key = stream_root(root)
    training = data.training(key)
    core = Core.fit(training, manifest["core_ridge"])
    denominator = max(float(training[0].square().mean()), 1e-8)
    core_hash = tensor_hash({"a": core.a, "b": core.b})
    torch.save({"a": core.a, "b": core.b}, dest / "core.pt")
    np.savez_compressed(
        dest / "training.npz", **{str(i): v.numpy() for i, v in enumerate(training)}
    )
    fit_cpu = time.process_time() - started
    y, actions, targets = data.core_probes(key)
    grounded = core.advance(data.tensor(targets[:, :-1]), actions)
    grounded_error = float(((grounded.numpy() - targets[:, 1:]) ** 2).mean() / denominator)
    free = y.clone()
    pred = []
    for action in actions.T:
        free = core.advance(free, action)
        pred.append(free.clone())
    core_error = float(((torch.stack(pred, 1).numpy() - targets[:, 1:]) ** 2).mean() / denominator)
    if max(core_error, grounded_error) > manifest["checks"]["core_nmse_max"]:
        raise RuntimeError("Fixed core failed competence invariant")
    np.savez_compressed(
        dest / "core-probes.npz",
        truth=targets,
        actions=actions.numpy(),
        grounded=grounded.numpy(),
        free=torch.stack(pred, 1).numpy(),
    )
    saved, audits, resources = {}, [], {}
    timing = {name: {"write_seconds": 0.0, "recall_seconds": 0.0} for name in ARMS}
    task = manifest["task"]
    for sequence in range(task["sequences"]):
        check()
        objects = data.objects(key, "evaluation", sequence, task["objects"])
        memories = {name: RetrievalMemory(name, core, manifest["settings"][name]) for name in ARMS}
        codes, observations = [], []
        for index, obj in enumerate(objects):
            recs = data.records(obj, key, "evaluation", (sequence, index), task["snapshots"])
            codes.append(torch.stack([acquired_code(core, r) for r in recs]).numpy())
            observations.append(
                np.stack([np.r_[r.key.numpy(), r.features.numpy(), r.angle] for r in recs])
            )
            for name, memory in memories.items():
                tick = time.perf_counter()
                for record in recs:
                    memory.acquire(record, grounded=True)
                timing[name]["write_seconds"] += time.perf_counter() - tick
            check()
        codes = np.stack(codes).astype(np.int8)
        seq = {"codes": codes, "observations": np.stack(observations)}
        p = memories["PH-FULL"].buffers["projector"]
        x = data.tensor(codes.reshape(-1, 768))
        audit = {
            "preservation": float((x @ p.T - x).abs().max()),
            "symmetry": float((p - p.T).abs().max()),
            "idempotence": float((p @ p - p).abs().max()),
            "rank": int(memories["PH-FULL"].buffers["rank"]),
            "sequence": sequence,
        }
        if max(audit[k] for k in ("preservation", "symmetry", "idempotence")) > 1e-8:
            raise RuntimeError("Projector audit failed")
        audits.append(audit)
        for name, memory in memories.items():
            torch.save(memory.snapshot(), dest / f"sequence-{sequence}-{name}.pt")
            resources[name] = memory.resources()
            if resources[name]["persistent_bytes"] > manifest["limits"]["persistent_bytes_per_arm"]:
                raise RuntimeError("Persistent memory ceiling")
        rows = {}
        for index, obj in enumerate(objects[:-1]):
            cues, actions, truth = data.queries(
                obj, key, "evaluation", (sequence, index), task["queries"]
            )
            cue = cues["partial"]
            row = {
                "cue": cue.features.numpy(),
                "mask": cue.mask.numpy(),
                "actions": actions.numpy(),
                "truth": truth,
            }
            for name, memory in memories.items():
                pred, scores, state, elapsed = predict(memory, cue, actions)
                timing[name]["recall_seconds"] += elapsed
                row[f"{name}_pred"], row[f"{name}_scores"] = pred, scores
                if name == "PH-FULL":
                    row["states"] = state
                    row["cycles"] = memory.trace["cycles"].numpy().copy()
                    row["converged"] = memory.trace["converged"].numpy().copy()
                    if not np.array_equal(
                        decode(data.tensor(state[:, 512:]), 1.5).numpy(), pred[:, 0]
                    ):
                        raise RuntimeError("Archived state does not decode to ordinary output")
            for name, value in row.items():
                rows.setdefault(name, []).append(value)
            check()
        seq.update({name: np.stack(values) for name, values in rows.items()})
        # Report the actual batch of eight active queries, not the post-write reset.
        for name, memory in memories.items():
            resources[name] = memory.resources()
        # Save the ordinary path before accessing codes/targets in the diagnostic.
        np.savez_compressed(dest / f"sequence-{sequence}-ordinary.npz", **seq)
        seq.update(
            diagnostic(
                seq["states"].copy(),
                codes.copy(),
                seq["mask"].copy(),
                seq["truth"][..., 0, :].copy(),
                denominator,
            )
        )
        for name, value in seq.items():
            saved.setdefault(name, []).append(value)
        check()
    arrays = {name: np.stack(values) for name, values in saved.items()}
    np.savez_compressed(dest / "arrays.npz", **arrays)
    if tensor_hash({"a": core.a, "b": core.b}) != core_hash:
        raise RuntimeError("Common core changed")
    return {
        "root": root,
        "stream_root": key,
        "normalization": denominator,
        "core_hash": core_hash,
        "fit_cpu_seconds": fit_cpu,
        "grounded_one_step_nmse": grounded_error,
        "core_free8_nmse": core_error,
        "metrics": metrics(arrays, denominator),
        "projector_audits": audits,
        "resources": resources,
        "timing": timing,
        "exposure": {
            "training_transitions": 2048,
            "acquisition_snapshots": 256,
            "earlier_object_query_cues": 224,
            "replay": 0,
            "writes_per_arm": 256,
            "independent_unit": "root",
        },
        "evaluator_array_bytes": sum(v.nbytes for v in arrays.values()),
        "resident_models": list(ARMS),
        "resource_note": "All three arms coexist during evaluation; core tensors are shared. RSS includes evaluator arrays and dense workspaces.",
    }
