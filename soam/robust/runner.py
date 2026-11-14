"""Serial, finite B2 phases with immutable receipts and cumulative accounting."""

import argparse
import dataclasses
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

from soam.robust.data import normalization, seed, training_data
from soam.robust.engine import batches, evaluate, headline, latency, operation_profile
from soam.robust.models import Config, Robust, phase1
from soam.temporal.data import input_hash
from soam.temporal.engine import fit
from soam.temporal.models import make
from soam.temporal.runner import Budget, digest, dump, tensor_hash

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "runs/study-b2-v1"
MANIFEST = ROOT / "docs/protocols/study_b2_v1.json"


def source():
    paths = sorted(
        [
            *ROOT.glob("soam/**/*.py"),
            *ROOT.glob("tests/test_robust*.py"),
            *ROOT.glob("scripts/*study_b2*.py"),
            MANIFEST,
            ROOT / "docs/STUDY_B2_PROTOCOL.md",
            ROOT / "pyproject.toml",
            ROOT / "uv.lock",
        ]
    )
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    return {
        "hashes": hashes,
        "aggregate": digest(hashes),
        "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty": subprocess.check_output(["git", "status", "--porcelain"], text=True).splitlines(),
        "python": sys.version,
        "numpy": np.__version__,
        "torch": torch.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
        ).strip()
        if sys.platform == "darwin"
        else platform.processor(),
        "torch_build": torch.__config__.show(),
        "threads": torch.get_num_threads(),
        "deterministic": torch.are_deterministic_algorithms_enabled(),
        "numerics": "CPU float32 historical/PC16, float64 robust algebra and all reductions; no GPU",
    }


def snapshot(dest):
    identity = source()
    dump(dest / "source.json", identity)
    for p in identity["hashes"]:
        target = dest / "source" / p
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / p, target)
    return identity


def model_fit(dest, root, m, budget, fixture=False):
    dest.mkdir(parents=True, exist_ok=False)
    data = training_data(
        root,
        updates=20 if fixture else m["updates"],
        batch=4 if fixture else m["train_batch"],
        horizon=m["train_horizon"],
        split="fixture" if fixture else "train",
    )
    result = {}
    for name in ("FILTER2", "PC16"):
        budget.check(force=True)
        marker = dest / f"{name}-status.json"
        dump(marker, {"status": "running"})
        if len(list(OUT.glob("**/*-status.json"))) > m["max_fit_attempts"]:
            raise RuntimeError("fit attempt cap")
        model = make(name, seed("train", root, component="initialization"))
        try:
            record = fit(
                model,
                data,
                m["filter_penalty"] if name == "FILTER2" else m["pc16_learning_rate"],
                budget.check,
            )
            record.update(
                input_hash=input_hash(data),
                checkpoint_hash=tensor_hash(model.state_dict()),
                trace_hash=digest(record["trace"]),
                resources=model.resources(),
                exposure={
                    "episodes": sum(len(b.target[0]) for b in data),
                    "clean_supervisory_observations": sum(
                        b.target.shape[0] * b.target.shape[1] for b in data
                    ),
                    "sensory_events": sum(int(b.evidence.mask.any(-1).sum()) for b in data),
                    "feature_values": sum(int(b.evidence.mask.sum()) for b in data),
                    "offline_updates": 0 if name == "FILTER2" else len(data),
                    "replay": 0,
                },
            )
            torch.save(model.state_dict(), dest / f"{name}.pt")
            dump(dest / f"{name}-fit.json", record)
            dump(marker, {"status": "complete"})
            result[name] = model
        except BaseException as e:
            dump(marker, {"status": "failed", "error": repr(e)})
            raise
    return result


def load_models(dest):
    result = {}
    for name in ("FILTER2", "PC16"):
        model = make(name, 0)
        model.load_state_dict(torch.load(dest / f"{name}.pt", weights_only=True))
        result[name] = model
    return result


def eval_one(dest, model, data, var, budget, detail=False):
    dest.mkdir(parents=True, exist_ok=False)
    dump(dest / "status.json", {"status": "running"})
    try:
        rows, arrays, cpu = evaluate(model, data, var, budget.check, detail)
        record = {
            "headline": headline(rows),
            "rows": rows,
            "evaluation_cpu_seconds": cpu,
            "resources": model.resources(),
            "array_hash": tensor_hash({k: torch.from_numpy(v) for k, v in arrays.items()}),
            "config": dataclasses.asdict(model.config)
            if isinstance(model, Robust)
            else {"name": model.name},
        }
        dump(dest / "results.json", record)
        np.savez_compressed(dest / "arrays.npz", **arrays)
        dump(dest / "status.json", {"status": "complete"})
        budget.check(force=True)
        print(
            json.dumps({"cell": str(dest.relative_to(OUT)), "headline": record["headline"]}),
            flush=True,
        )
        return record
    except BaseException as e:
        dump(dest / "status.json", {"status": "failed", "error": repr(e)})
        raise


def audit(dest, m, budget):
    from soam.temporal.data import normalization as old_norm
    from soam.temporal.data import training_data as historical_data
    from soam.temporal.engine import evaluate as old_evaluate
    from soam.temporal.engine import fit_linear

    oldpath = ROOT / "runs/study-b-v1/confirmation/12007/FILTER2/0.0001"
    old = make("FILTER2", 0)
    old.load_state_dict(torch.load(oldpath / "checkpoint.pt", weights_only=True))
    data = historical_data(12007)
    refit = make("FILTER2", 0)
    fit_linear(refit, data, 0.0001)
    fit_exact = tensor_hash(old.state_dict()) == tensor_hash(refit.state_dict())
    _rows, arrays, _ = old_evaluate(old, "confirmation", 12007, old_norm(), check=budget.check)
    saved = np.load(oldpath / "errors.npz")
    equal = {k: bool(np.array_equal(arrays[k], saved[k])) for k in arrays}
    # Attribution of fitted Q to clean-target jump residuals, no refitting intervention.
    from soam.gating.models import bilinear

    contributions = {}
    for b in data:
        moving = b.evidence.roles[..., 1].bool()
        x = (b.target[:-1] - old.mean) @ old.P
        y = (b.target[1:] - old.mean) @ old.P
        r = y - bilinear(x, b.evidence.actions) @ old.B.T
        val = contributions.setdefault(b.condition, {"sse": 0.0, "count": 0})
        val["sse"] += float(r[moving].double().square().sum())
        val["count"] += int(moving.sum())
    record = {
        "historical_root": 12007,
        "fit_exact": fit_exact,
        "prediction_arrays_exact": equal,
        "input_hash": input_hash(data),
        "checkpoint_hash": tensor_hash(old.state_dict()),
        "source_matches_historical": all(
            hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == h
            for p, h in json.loads((ROOT / "reports/study-b/source.json").read_text())[
                "hashes"
            ].items()
        ),
        "process": old.process.tolist(),
        "process_eigenvalues": torch.linalg.eigvalsh(old.process).tolist(),
        "training_process_residual_by_condition": contributions,
        "baseline": json.loads((oldpath / "evaluation.json").read_text())["headline"],
        "defect": "No baseline scientific defect found. Explicit inverses are a numerical engineering limitation; stable control tested separately.",
        "updates": "Cprior=F Cpost F.T+Q even during recall; R=1e-4 per observed channel; inverse information correction; missing returns prior.",
    }
    assert fit_exact and all(equal.values()) and record["source_matches_historical"]
    dump(dest / "baseline-audit.json", record)


def fixture(dest, m, budget, var):
    models = model_fit(dest / "fits", m["fixture_root"], m, budget, fixture=True)
    data = batches("fixture", m["fixture_root"], 4)
    timings = {}
    for model in [
        models["FILTER2"],
        models["PC16"],
        *[Robust(models["FILTER2"], c) for c in phase1()],
    ]:
        rows, arrays, cpu = evaluate(model, data, var, budget.check)
        timings[model.name] = {
            "evaluation_cpu_seconds": cpu,
            "artifact_uncompressed_bytes": sum(v.nbytes for v in arrays.values()),
            "resources": model.resources(),
        }
        assert all(v.get("min_eigenvalue", 1) > 0 for v in rows.values())
        budget.check()
    # Generous bounds for three confirmation challengers plus constituents and numerical control.
    fit_cost = (
        sum(
            json.loads((dest / "fits" / f"{n}-fit.json").read_text())["fit_cpu_seconds"]
            for n in models
        )
        * 1200
        / 20
    )
    eval_cost = max(v["evaluation_cpu_seconds"] for v in timings.values())
    projection = 1.5 * (15 * fit_cost + 200 * eval_cost)
    artifact = 1.5 * 160 * max(v["artifact_uncompressed_bytes"] for v in timings.values())
    rss = __import__("resource").getrusage(__import__("resource").RUSAGE_SELF).ru_maxrss * (
        1 if sys.platform == "darwin" else 1024
    )
    record = {
        "timings": timings,
        "projected_cpu_seconds": projection,
        "projected_artifact_bytes": artifact,
        "projected_peak_rss_bytes": rss * 1.25,
        "projection_pass": projection < m["cpu_seconds"] * 0.9
        and artifact < m["artifact_bytes"]
        and rss * 1.25 < m["rss_bytes"],
        "note": "1.5x time/storage and1.25x memory; bounded maximum160 evals plus40screen equivalent; full detail retained only first confirmation root. Compressed storage expected smaller.",
    }
    dump(dest / "projection.json", record)
    assert record["projection_pass"], "fixture exceeds allocation; do not start screening"


def screen1(dest, m, budget, var):
    if not json.loads((OUT / "fixture-storage-a1/projection.json").read_text())["projection_pass"]:
        raise RuntimeError("fixture required")
    base = {}
    thresholds = {6: [], 12: []}
    for root in m["development_roots"]:
        models = model_fit(dest / str(root) / "fits", root, m, budget)
        data = batches("development", root, m["development_batch"])
        base[root] = (models, data)
        for name in ("FILTER2", "PC16"):
            eval_one(dest / str(root) / name, models[name], data, var, budget)
        arrays = np.load(dest / str(root) / "FILTER2/arrays.npz")
        for c in ("clean", "partial", "missing", "noise"):
            for s in SENSED:
                prefix = f"{c}__{s}__"
                mask = arrays[prefix + "sensed"]
                thresholds[12 if c == "clean" else 6].extend(arrays[prefix + "nis"][mask].tolist())
    calibrated = {d: float(np.quantile(x, 0.99)) for d, x in thresholds.items()}
    dump(
        dest / "nis-calibration.json",
        {
            "quantile": 0.99,
            "thresholds": calibrated,
            "counts": {d: len(x) for d, x in thresholds.items()},
            "selection": "All pre-gating nominal innovations, not accepted-only",
        },
    )
    configs = [
        dataclasses.replace(c, empirical6=calibrated[6], empirical12=calibrated[12])
        if c.mode == "nis_emp"
        else c
        for c in phase1()
    ]
    dump(dest / "configs.json", [dataclasses.asdict(c) for c in configs])
    for root, (models, data) in base.items():
        for c in configs:
            eval_one(dest / str(root) / c.name, Robust(models["FILTER2"], c), data, var, budget)
    summary = {
        name: {
            k: float(
                np.mean(
                    [
                        json.loads((dest / str(r) / name / "results.json").read_text())["headline"][
                            k
                        ]
                        for r in m["development_roots"]
                    ]
                )
            )
            for k in (
                "J",
                "C",
                "corrupt",
                "change",
                "coherent",
                "sustained",
                "channels",
                "noise",
                "dynamics",
                "gap",
            )
        }
        for name in ["FILTER2", "PC16"] + [c.name for c in configs]
    }
    dump(dest / "summary.json", summary)


def screen_extensions(dest, m, budget, var, hybrid=False):
    configs = (
        [Config("HYBRID", "hybrid")]
        if hybrid
        else [
            Config("ADAPT1", "adaptive"),
            Config("ADAPT05", "adaptive", alpha=0.5),
            Config("TEMP2", "temporal"),
            Config("TEMP3", "temporal", persistence=3),
        ]
    )
    dump(dest / "configs.json", [dataclasses.asdict(c) for c in configs])
    results = {}
    for root in m["development_roots"]:
        models = load_models(OUT / "screen1" / str(root) / "fits")
        data = batches("development", root, m["development_batch"])
        for cfg in configs:
            record = eval_one(
                dest / str(root) / cfg.name, Robust(models["FILTER2"], cfg), data, var, budget
            )
            results.setdefault(cfg.name, []).append(record["headline"])
    dump(
        dest / "summary.json",
        {
            n: {k: float(np.mean([v[k] for v in values])) for k in values[0]}
            for n, values in results.items()
        },
    )


def freeze(dest, m, budget, var):
    for phase in ("audit", "fixture", "screen1", "screen2", "hybrid"):
        assert json.loads((OUT / phase / "status.json").read_text())["status"] == "complete"
    assert json.loads((OUT / "fixture-storage-a1/projection.json").read_text())["projection_pass"]
    configs = json.loads((OUT / "screen1/configs.json").read_text()) + json.loads(
        (OUT / "screen2/configs.json").read_text()
    )
    keep = {"STABLE", "R100", "NIS99", "CHANNEL2", "NISEMP", "ADAPT1"}
    selected = {c["name"]: c for c in configs if c["name"] in keep}
    receipt = {
        "inventory": ["FILTER2", "STABLE", "PC16", "R100", "NIS99", "CHANNEL2", "NISEMP", "ADAPT1"],
        "challengers": ["ADAPT1", "NISEMP"],
        "configs": selected,
        "confirmation_roots": m["confirmation_roots"],
        "normalization": var,
        "manifest": digest(m),
        "source": json.loads((dest / "source.json").read_text()),
        "development": {
            phase: digest(json.loads((OUT / phase / "summary.json").read_text()))
            for phase in ("screen1", "screen2", "hybrid")
        },
        "family_size": 12,
        "spent_cpu_seconds": budget.spent_cpu,
        "review": "Targets unchanged; two eligible distinct mechanisms, all mandatory baselines and simple controls; temporal/hybrid development failures preserved; fresh confirmation; no oracle metadata; no C activation.",
    }
    receipt["sha256"] = digest(receipt)
    dump(dest / "confirmation-receipt.json", receipt)


def receipt_check():
    receipt = json.loads((OUT / "freeze/confirmation-receipt.json").read_text())
    assert digest({k: v for k, v in receipt.items() if k != "sha256"}) == receipt["sha256"]
    assert digest(json.loads(MANIFEST.read_text())) == receipt["manifest"]
    for path, expected in receipt["source"]["hashes"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, (
            f"frozen source changed: {path}"
        )
    return receipt


def confirmation(dest, m, budget, var, repeat=False):
    receipt = receipt_check()
    roots = [m["repeat_root"]] if repeat else receipt["confirmation_roots"]
    matches = {}
    for root in roots:
        models = model_fit(dest / str(root) / "fits", root, m, budget)
        data = batches("confirmation", root, m["eval_batch"])
        for name in receipt["inventory"]:
            model = (
                models[name]
                if name in models
                else Robust(models["FILTER2"], Config(**receipt["configs"][name]))
            )
            record = eval_one(
                dest / str(root) / name, model, data, var, budget, detail=root == m["repeat_root"]
            )
            if repeat:
                original = json.loads(
                    (OUT / "confirmation" / str(root) / name / "results.json").read_text()
                )
                matches[name] = {
                    "arrays": record["array_hash"] == original["array_hash"],
                    "headline": record["headline"] == original["headline"],
                    "inputs": all(
                        v["input_hash"] == original["rows"][k]["input_hash"]
                        for k, v in record["rows"].items()
                    ),
                }
            elif root == roots[0]:
                dump(dest / str(root) / name / "latency.json", latency(model))
                dump(dest / str(root) / name / "operations.json", operation_profile(model))
        if repeat:
            for name in models:
                actual = json.loads((dest / str(root) / "fits" / f"{name}-fit.json").read_text())
                original = json.loads(
                    (OUT / "confirmation" / str(root) / "fits" / f"{name}-fit.json").read_text()
                )
                matches[name].update(
                    {
                        k: actual[k] == original[k]
                        for k in ("input_hash", "checkpoint_hash", "trace_hash")
                    }
                )
            dump(dest / "reproduction.json", matches)
            assert all(all(v.values()) for v in matches.values()), "prescribed repeat failed"


def reduction(dest, m, budget):
    from soam.robust.statistics import summarize

    receipt = receipt_check()
    results = {
        str(r): {
            n: json.loads((OUT / "confirmation" / str(r) / n / "results.json").read_text())
            for n in receipt["inventory"]
        }
        for r in receipt["confirmation_roots"]
    }
    dump(
        dest / "root-results.json",
        {r: {n: v["headline"] for n, v in models.items()} for r, models in results.items()},
    )
    dump(dest / "statistics.json", summarize(results, receipt, m))
    # Independent array reduction: intentionally does not call headline/evaluate.
    checked = 0
    maximum = 0.0
    for root in receipt["confirmation_roots"]:
        for name in receipt["inventory"]:
            budget.check()
            arrays = np.load(OUT / "confirmation" / str(root) / name / "arrays.npz")
            stored = results[str(root)][name]["headline"]
            condition_means = {}
            for condition in (
                "corrupt",
                "isolated",
                "channels",
                "coherent",
                "sustained",
                "heavy",
                "biased",
                "change",
                "clean",
                "gap",
            ):
                schedules = (
                    ("every1", "every2", "every4", "every8", "irregular")
                    if condition in ("corrupt", "change", "clean", "gap")
                    else ("every2", "every4", "every8", "irregular")
                )
                condition_means[condition] = sum(
                    float(arrays[f"{condition}__{s}__prior"].sum())
                    / arrays[f"{condition}__{s}__prior"].size
                    for s in schedules
                ) / len(schedules)
            actual = {
                **condition_means,
                "C": sum(
                    condition_means[c]
                    for c in (
                        "corrupt",
                        "isolated",
                        "channels",
                        "coherent",
                        "sustained",
                        "heavy",
                        "biased",
                    )
                )
                / 7,
                "J": sum(
                    float(arrays[f"{c}__{s}__prior"].sum()) / arrays[f"{c}__{s}__prior"].size
                    for c in ("partial", "missing", "noise")
                    for s in ("every2", "every4", "every8", "irregular")
                )
                / 12,
                "free32": float(arrays["partial__initial__prior"][:32].mean()),
            }
            for metric, value in actual.items():
                error = abs(value - stored[metric])
                maximum = max(maximum, error)
                checked += 1
                assert error < 1e-12, (root, name, metric, error)
    dump(
        dest / "independent-reduction.json",
        {
            "checked_values": checked,
            "maximum_absolute_error": maximum,
            "tolerance": 1e-12,
            "independent_implementation": True,
        },
    )


# Late-stage phases are gated by the written development decisions.


def main():
    from soam.robust.data import SENSED as schedules

    global SENSED
    SENSED = schedules
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "phase",
        choices=[
            "audit",
            "fixture",
            "screen1",
            "screen2",
            "hybrid",
            "freeze",
            "confirmation",
            "repeat",
            "report",
        ],
    )
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    m = json.loads(MANIFEST.read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / args.phase
    dest.mkdir(parents=True, exist_ok=False)
    budget = Budget(OUT, m, args.phase)
    try:
        snapshot(dest)
        var = normalization()
        dump(dest / "normalization.json", {"variance": var})
        if args.phase == "audit":
            audit(dest, m, budget)
        elif args.phase == "fixture":
            fixture(dest, m, budget, var)
        elif args.phase == "screen1":
            screen1(dest, m, budget, var)
        elif args.phase in {"screen2", "hybrid"}:
            screen_extensions(dest, m, budget, var, hybrid=args.phase == "hybrid")
        elif args.phase == "freeze":
            freeze(dest, m, budget, var)
        elif args.phase in {"confirmation", "repeat"}:
            confirmation(dest, m, budget, var, repeat=args.phase == "repeat")
        elif args.phase == "report":
            reduction(dest, m, budget)
        budget.check(force=True)
        dump(dest / "status.json", {"status": "complete"})
        budget.finish("complete")
    except BaseException as e:
        dump(dest / "status.json", {"status": "failed", "error": repr(e)})
        budget.finish("failed", repr(e))
        raise


if __name__ == "__main__":
    main()
