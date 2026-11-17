"""Finite source-frozen execution of Study D. Existing phase paths refuse overwrite."""

import argparse
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import torch

from soam.temporal.runner import Budget, digest, dump, size, tensor_hash
from soam.temporal.statistics import interval

from .data import training
from .engine import array_hash, core_error, evaluate
from .models import Core

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "runs/study-d-v1"
REPORT = ROOT / "reports/study-d"
MANIFEST = ROOT / "docs/protocols/study_d_v1.json"
NAMES = ("NOWRITE", "KV", "REG", "FAST")


def source():
    paths = sorted(
        [
            *ROOT.glob("soam/**/*.py"),
            *ROOT.glob("tests/*.py"),
            ROOT / "pyproject.toml",
            ROOT / "uv.lock",
            MANIFEST,
            ROOT / "docs/STUDY_D_PROTOCOL.md",
        ]
    )
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    return {
        "hashes": hashes,
        "aggregate": digest(hashes),
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "dirty": subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True
        ).splitlines(),
        "python": sys.version,
        "torch": torch.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "threads": torch.get_num_threads(),
        "dtype": "float64",
        "device": "cpu",
        "deterministic": torch.are_deterministic_algorithms_enabled(),
    }


def snapshot(dest):
    identity = source()
    dump(dest / "source.json", identity)
    for relative in identity["hashes"]:
        target = dest / "source" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    return identity


def fit(dest, root, ridge, budget):
    dest.mkdir(parents=True, exist_ok=False)
    dump(dest / "fit-status.json", {"status": "running"})
    if len(list(OUT.glob("**/fit-status.json"))) > budget.m["max_fit_attempts"]:
        raise RuntimeError("Offline fit ceiling")
    started = time.process_time()
    data = training(root)
    core = Core.fit(data, ridge)
    denominator = max(float(data[0].square().mean()), 1e-8)
    checkpoint = {"a": core.a, "b": core.b}
    torch.save(checkpoint, dest / "core.pt")
    arrays = {str(i): x.numpy() for i, x in enumerate(data)}
    np.savez_compressed(dest / "training.npz", **arrays)
    result = {
        "root": root,
        "ridge": ridge,
        "normalization": denominator,
        "input_hash": array_hash(arrays),
        "core_hash": tensor_hash(checkpoint),
        "core_probe": core_error(core, root, denominator),
        "cpu_seconds": time.process_time() - started,
        "transition_records": 2048,
        "feature_snapshots": 4096,
    }
    dump(dest / "fit.json", result)
    if result["core_probe"] > 0.02:
        raise RuntimeError("Offline core competence failed")
    dump(dest / "fit-status.json", {"status": "complete"})
    budget.check(force=True)
    return core, denominator, result


def trial(dest, name, core, setting, root, split, denominator, threshold, budget):
    dest.mkdir(parents=True, exist_ok=False)
    dump(dest / "status.json", {"status": "running", "started_utc": now()})
    start = time.process_time()
    try:
        result, arrays, inputs, memory = evaluate(
            name, core, setting, root, split, denominator, threshold, budget.check
        )
        result.update(
            name=name,
            setting=setting,
            threshold=threshold,
            root=root,
            split=split,
            cpu_seconds=time.process_time() - start,
        )
        np.savez_compressed(dest / "arrays.npz", **arrays)
        np.savez_compressed(dest / "inputs.npz", **inputs)
        torch.save(memory, dest / "last-memory.pt")
        dump(dest / "result.json", result)
        dump(dest / "status.json", {"status": "complete", "ended_utc": now()})
        budget.check(force=True)
        return result
    except Exception as exc:
        dump(dest / "status.json", {"status": "failed", "error": repr(exc), "ended_utc": now()})
        raise


def now():
    return datetime.now(UTC).isoformat()


def read(path):
    return json.loads(path.read_text())


def fixture(dest, m, budget):
    start = time.process_time()
    core, den, _ = fit(dest / "fit", m["fixture_root"], m["core_ridges"][0], budget)
    for name in NAMES:
        trial(
            dest / name,
            name,
            core,
            0.1 if name == "REG" else 1.0,
            m["fixture_root"],
            "fixture",
            den,
            1e30,
            budget,
        )
    elapsed = time.process_time() - start
    # Full fixture inventory repeated 24 times upper-bounds 88 planned model evaluations,
    # plus separate fit snapshots, reductions and rendering with a further 2x factor.
    estimate = {
        "fixture_cpu_seconds": elapsed,
        "projected_remaining_cpu_seconds_with_2x": elapsed * 24 * 2,
        "projected_artifacts_bytes_with_2x": size(dest) * 24 * 2,
        "planned_offline_fits": 16,
        "planned_model_evaluations": 88,
    }
    estimate["pass"] = (
        estimate["projected_remaining_cpu_seconds_with_2x"] < 6480
        and estimate["projected_artifacts_bytes_with_2x"] < 2147483648
    )
    dump(dest / "projection.json", estimate)
    if not estimate["pass"]:
        raise RuntimeError("Fixture projection exceeds fixed resource envelope")


def development(dest, m, budget):
    all_results, fit_results = [], []
    for root in m["development_roots"]:
        for ci, ridge in enumerate(m["core_ridges"]):
            core, den, fit_result = fit(dest / str(root) / f"core{ci}", root, ridge, budget)
            fit_results.append({**fit_result, "core_index": ci})
            for name in NAMES:
                settings = (
                    m["reg_ridges"]
                    if name == "REG"
                    else (m["fast_rates"] if name == "FAST" else [1.0])
                )
                for setting in settings:
                    result = trial(
                        dest / str(root) / f"core{ci}" / name / str(setting),
                        name,
                        core,
                        setting,
                        root,
                        "development-selection",
                        den,
                        1e30,
                        budget,
                    )
                    all_results.append({**result, "core_index": ci})
    core_index = min(
        range(2),
        key=lambda i: np.mean([r["core_probe"] for r in fit_results if r["core_index"] == i]),
    )
    selected = {
        "core_index": core_index,
        "core_ridge": m["core_ridges"][core_index],
        "settings": {},
        "thresholds": {},
        "selection_scores": {},
    }
    for name in NAMES:
        rows = [r for r in all_results if r["core_index"] == core_index and r["name"] == name]
        options = list(dict.fromkeys(r["setting"] for r in rows))
        scores = {
            str(s): float(
                np.mean([0.5 * (r["J"] + r["old_error"]) for r in rows if r["setting"] == s])
            )
            for s in options
        }
        setting = min(options, key=lambda s: scores[str(s)])
        selected["settings"][name] = setting
        selected["selection_scores"][name] = scores
    selected["conventional_reference"] = min(
        ("KV", "REG"), key=lambda n: selected["selection_scores"][n][str(selected["settings"][n])]
    )
    for name in NAMES:
        scores = []
        for root in m["development_roots"]:
            base = dest / str(root) / f"core{core_index}"
            checkpoint = torch.load(base / "core.pt", weights_only=True)
            core = Core(checkpoint["a"], checkpoint["b"])
            den = read(base / "fit.json")["normalization"]
            target = dest / "calibration" / str(root) / name
            trial(
                target,
                name,
                core,
                selected["settings"][name],
                root,
                "development-calibration",
                den,
                1e30,
                budget,
            )
            with np.load(target / "arrays.npz") as arrays:
                scores.extend(arrays["d2_scores"][:, -1].ravel().tolist())
        selected["thresholds"][name] = float(np.quantile(scores, 0.95))
    dump(dest / "all-candidates.json", all_results)
    dump(dest / "selection.json", selected)


def frozen():
    receipt = read(OUT / "freeze/receipt.json")
    if receipt["source"]["hashes"] != source()["hashes"]:
        raise RuntimeError("Frozen scientific source changed")
    if receipt["manifest"] != read(MANIFEST):
        raise RuntimeError("Frozen manifest changed")
    return receipt


def confirmation(dest, m, budget, repeat=False):
    receipt = frozen()
    s = receipt["selection"]
    roots = [m["repeat_root"]] if repeat else m["confirmation_roots"]
    for root in roots:
        core, den, _ = fit(dest / str(root) / "fit", root, s["core_ridge"], budget)
        for name in NAMES:
            trial(
                dest / str(root) / name,
                name,
                core,
                s["settings"][name],
                root,
                "confirmation",
                den,
                s["thresholds"][name],
                budget,
            )


def report(dest, m, budget):
    from .report import render

    receipt = frozen()
    rows = {
        name: [
            read(OUT / "confirmation" / str(root) / name / "result.json")
            for root in m["confirmation_roots"]
        ]
        for name in NAMES
    }
    stats = {}

    def ci(values, adjusted=True):
        return interval(
            values,
            alpha=0.05 / 20 if adjusted else 0.05,
            resamples=m["bootstrap_draws"],
            seed=m["bootstrap_seed"],
        )

    def vals(name, key):
        return np.array([r[key] for r in rows[name]])

    for name in NAMES[1:]:
        stats[name] = {}
        for key in ("J", "one_shot"):
            stats[name][key + "_gain"] = ci(
                (vals("NOWRITE", key) - vals(name, key)) / np.maximum(vals("NOWRITE", key), 1e-6)
            )
        for key in ("retention", "old_accuracy", "accuracy8", "error8"):
            stats[name][key] = ci(vals(name, key))
        s = stats[name]
        s["acquisition_supported"] = bool(
            s["J_gain"]["mean"] >= 0.2
            and s["J_gain"]["lo"] > 0
            and s["J_gain"]["width"] <= 0.4
            and s["retention"]["hi"] <= 0.02
            and s["old_accuracy"]["lo"] >= 0.8
            and s["accuracy8"]["lo"] >= 0.8
            and s["error8"]["hi"] <= 0.15
        )
        s["one_shot_supported"] = bool(
            s["acquisition_supported"]
            and s["one_shot_gain"]["mean"] >= 0.2
            and s["one_shot_gain"]["lo"] > 0
        )
    contrasts = {}
    for name in ("KV", "REG"):
        v = ci((vals(name, "J") - vals("FAST", "J")) / np.maximum(vals(name, "J"), 1e-6))
        floor = bool(np.any(vals(name, "J") < 1e-6))
        v["floor_limited"] = floor
        if floor:
            v["outcome"] = "uninformative relative comparison"
        elif v["hi"] < 0.1 and v["width"] <= 0.4:
            v["outcome"] = "negative practical advantage"
        elif v["mean"] >= 0.1 and v["lo"] > 0 and v["width"] <= 0.4:
            v["outcome"] = "supported primary benefit"
        else:
            v["outcome"] = "inconclusive"
        v["absolute_difference_descriptive"] = ci(vals("FAST", "J") - vals(name, "J"), False)
        contrasts[name] = v
    stats["fast_comparisons"] = contrasts
    stats["fast_advantage_supported"] = bool(
        stats["FAST"]["acquisition_supported"]
        and all(v["outcome"] == "supported primary benefit" for v in contrasts.values())
    )
    stats["descriptive"] = {
        n: {
            k: ci(vals(n, k), False)
            for k in (
                "J",
                "one_shot",
                "error8",
                "old_error",
                "retention",
                "old_accuracy",
                "false_familiarity",
                "accepted_wrong",
                "known_acceptance",
                "core_probe",
                "write_us_mean",
                "write_us_p95",
                "recall_us_mean",
                "recall_us_p95",
            )
        }
        for n in NAMES
    }
    verified = {
        "repeat_arrays": 0,
        "independent_values": 0,
        "max_reduction_error": 0.0,
        "historical_c_source_files": 0,
    }
    for root in m["confirmation_roots"]:
        hashes = []
        for name in NAMES:
            target = OUT / "confirmation" / str(root) / name
            result = read(target / "result.json")
            hashes.append(result["input_hash"])
            with np.load(target / "arrays.npz") as stored:
                arrays = dict(stored)
            if array_hash(arrays) != result["numeric_hash"]:
                raise RuntimeError("Array hash mismatch")
            # Independent reduction rebuilds errors from saved predictions/targets.
            rebuilt = dict(arrays)
            rebuilt["d1_error"] = np.square(arrays["d1_pred"] - arrays["d1_truth"][None]).mean(-1)
            rebuilt["d1_error"] /= result["normalization"]
            rebuilt["d2_error"] = np.square(arrays["d2_pred"] - arrays["d2_truth"][:, None]).mean(
                -1
            )
            rebuilt["d2_error"] /= result["normalization"]
            rebuilt["d2_error"][:, ~arrays["d2_valid"]] = 0
            d1, d2 = rebuilt["d1_error"], rebuilt["d2_error"]
            # Separate audit formulas: reconstruct root endpoints from individual object cells.
            retained = [
                float(d2[s, 7, o, :, 1:].mean() - d2[s, o, o, :, 1:].mean())
                for s in range(4)
                for o in range(7)
            ]
            check = {
                "J": float(
                    np.mean([d1[b, o, :, 1:].mean() for b in range(1, 5) for o in range(24)])
                ),
                "one_shot": float(d1[1, ..., 1:].mean()),
                "error8": float(d1[4, ..., 1:].mean()),
                "accuracy8": float(np.count_nonzero(d1[4, ..., 0] <= 0.1) / (24 * 8)),
                "retention": float(np.mean(retained)),
                "old_error": float(
                    np.mean([d2[s, 7, o, :, 1:].mean() for s in range(4) for o in range(7)])
                ),
                "old_accuracy": float(np.count_nonzero(d2[:, 7, :7, :, 0] <= 0.1) / (4 * 7 * 8)),
            }
            for key, value in check.items():
                err = abs(value - result[key])
                verified["max_reduction_error"] = max(verified["max_reduction_error"], err)
                verified["independent_values"] += 1
                if err > 1e-12:
                    raise RuntimeError("Reduction mismatch")
            if root == m["repeat_root"]:
                repeated = read(OUT / "repeat" / str(root) / name / "result.json")
                if any(
                    repeated[k] != result[k]
                    for k in ("numeric_hash", "input_hash", "memory_hashes")
                ):
                    raise RuntimeError("Prescribed repeat mismatch")
                verified["repeat_arrays"] += len(arrays)
            if result["core_probe"] > 0.02:
                raise RuntimeError("Core competence failed")
        if len(set(hashes)) != 1:
            raise RuntimeError("Unequal acquisition/query information")
    root = str(m["repeat_root"])
    a, b = (
        read(OUT / "confirmation" / root / "fit/fit.json"),
        read(OUT / "repeat" / root / "fit/fit.json"),
    )
    assert a["core_hash"] == b["core_hash"] and a["input_hash"] == b["input_hash"]
    historic = read(ROOT / "reports/study-c/confirmation-receipt.json")["source"]["hashes"]
    for relative, expected in historic.items():
        if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Historical C file changed: {relative}")
        verified["historical_c_source_files"] += 1
    verified["status"] = "pass"
    dump(dest / "statistics.json", stats)
    dump(dest / "verification.json", verified)
    dump(dest / "root-results.json", rows)
    REPORT.mkdir(parents=True, exist_ok=True)
    for path in dest.glob("*.json"):
        shutil.copyfile(path, REPORT / path.name)
    shutil.copyfile(OUT / "freeze/receipt.json", REPORT / "confirmation-receipt.json")
    render(rows, stats, receipt, OUT, REPORT)
    budget.check(force=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "phase", choices=("fixture", "development", "freeze", "confirmation", "repeat", "report")
    )
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    m = read(MANIFEST)
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / args.phase
    dest.mkdir(exist_ok=False)
    budget = Budget(OUT, m["limits"], args.phase)
    dump(dest / "phase-status.json", {"status": "running", "started_utc": now()})
    snapshot(dest)
    try:
        if args.phase == "fixture":
            fixture(dest, m, budget)
        elif args.phase == "development":
            if not read(OUT / "fixture/projection.json")["pass"]:
                raise RuntimeError("Fixture has not passed")
            development(dest, m, budget)
        elif args.phase == "freeze":
            receipt = {
                "manifest": m,
                "source": source(),
                "selection": read(OUT / "development/selection.json"),
                "ledger_before_confirmation": read(OUT / "ledger.json"),
                "frozen_utc": now(),
            }
            receipt["sha256"] = digest(receipt)
            dump(dest / "receipt.json", receipt)
        elif args.phase in {"confirmation", "repeat"}:
            confirmation(dest, m, budget, args.phase == "repeat")
        else:
            report(dest, m, budget)
        dump(dest / "phase-status.json", {"status": "complete", "ended_utc": now()})
        budget.finish("complete")
        if args.phase == "report":
            ledger = read(OUT / "ledger.json")
            if size(OUT) + size(REPORT) > m["limits"]["artifact_bytes"]:
                raise RuntimeError("Total run plus report artifacts exceed ceiling")
            dump(
                REPORT / "resource-final.json",
                {
                    "phases": ledger,
                    "cpu_seconds": sum(r["cpu_seconds"] for r in ledger),
                    "wall_seconds": sum(r["wall_seconds"] for r in ledger),
                    "peak_rss_bytes": max(r["peak_rss_bytes"] for r in ledger),
                    "artifact_bytes_including_reports": size(OUT) + size(REPORT),
                    "fits": len(list(OUT.glob("**/fit-status.json"))),
                },
            )
    except Exception as exc:
        dump(
            dest / "phase-status.json", {"status": "failed", "error": repr(exc), "ended_utc": now()}
        )
        budget.finish("failed", repr(exc))
        raise


if __name__ == "__main__":
    main()
