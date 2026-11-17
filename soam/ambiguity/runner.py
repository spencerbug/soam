"""Finite Study C phases; fresh streams, immutable receipts and bounded execution."""

import argparse
import hashlib
import json
import platform
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch

from soam.temporal.models import Linear
from soam.temporal.runner import Budget, digest, dump, size, tensor_hash

from .data import PRIMARY, SECONDARY, generate, input_hash, normalization, seed, training_data
from .engine import arrays, fit_linear, fit_neural, headline, metrics, rollout
from .models import Conventional, Recurrent

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "runs/study-c-v1"
REPORT = ROOT / "reports/study-c"
MANIFEST = ROOT / "docs/protocols/study_c_v1.json"
ARCHITECTURES = ("PC16", "PC32", "PC40", "TWO16")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source():
    paths = sorted(
        [
            *ROOT.glob("soam/**/*.py"),
            *ROOT.glob("tests/*.py"),
            *ROOT.glob("scripts/*study_c*.py"),
            ROOT / "pyproject.toml",
            ROOT / "uv.lock",
            ROOT / "docs/STUDY_C_PROTOCOL.md",
            MANIFEST,
        ]
    )
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    return {
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "dirty": subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True
        ).splitlines(),
        "hashes": hashes,
        "aggregate": digest(hashes),
        "python": sys.version,
        "torch": torch.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "torch_build": torch.__config__.show(),
        "threads": torch.get_num_threads(),
        "deterministic": torch.are_deterministic_algorithms_enabled(),
        "numerics": "CPU only; float32 neural/FILTER2; float64 simulation/robust algebra/reductions",
    }


def snapshot(dest):
    identity = source()
    dump(dest / "source.json", identity)
    for relative in identity["hashes"]:
        target = dest / "source" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    return identity


def new_neural(name, root):
    return Recurrent(
        16 if name == "TWO16" else int(name[2:]),
        name == "TWO16",
        seed("train", root, component="initialization"),
    )


def fit_one(dest, name, root, data, lr, budget, development=None):
    dest.mkdir(parents=True, exist_ok=False)
    dump(dest / "fit-status.json", {"status": "running"})
    attempts = len(list(OUT.glob("**/fit-status.json")))
    if attempts > 70:
        raise RuntimeError("fit count ceiling")
    start = time.process_time()
    try:
        if name == "BASE":
            model = fit_linear(data)
            record = {"trace": [], "learning": {}}
        else:
            model = new_neural(name, root)
            record = fit_neural(model, data, lr, budget.check, development)
        budget.check(force=True)
        torch.save(model.state_dict(), dest / "model.pt")
        record.update(
            name=name,
            root=root,
            lr=lr,
            input_hash=digest([input_hash(b) for b in data]),
            checkpoint_hash=tensor_hash(model.state_dict()),
            trace_hash=digest(record["trace"]),
            cpu_seconds=time.process_time() - start,
            exposure={
                "episodes": sum(b.target.shape[1] for b in data),
                "clean_feature_records": sum(b.target.shape[0] * b.target.shape[1] for b in data),
                "regime_labels": sum(b.labels.numel() for b in data),
                "grounded_records": sum(int(b.evidence.mask.any(-1).sum()) for b in data),
                "updates": len(data) if name != "BASE" else 0,
                "replay": 0,
                "variance_calibration_reused_batches": 24 if name != "BASE" else 0,
            },
        )
        dump(dest / "fit.json", record)
        dump(dest / "fit-status.json", {"status": "complete"})
        print(
            json.dumps({"fit": str(dest.relative_to(OUT)), "cpu_seconds": record["cpu_seconds"]}),
            flush=True,
        )
        return model
    except Exception as error:
        dump(dest / "fit-status.json", {"status": "failed", "error": str(error)})
        raise


def load_neural(path, name, root):
    model = new_neural(name, root)
    model.load_state_dict(torch.load(path / "model.pt", weights_only=True))
    return model


def load_base(path):
    model = Linear("FILTER2")
    model.load_state_dict(torch.load(path / "model.pt", weights_only=True))
    return model


def filters(base, selection=None):
    selection = selection or {}
    result = []
    for kind in ("ADAPT1", "FILTER2", "NISEMP"):
        for multiple in (False, True):
            name = kind + ("-M" if multiple else "-C")
            threshold = selection.get("thresholds", {}).get(name, [16.811894, 26.216967])
            model = Conventional(base, kind, multiple, tuple(threshold))
            model.temperature = selection.get("temperatures", {}).get(name, 1.0)
            result.append(model)
    return result


@torch.no_grad()
def evaluate(model, batches, variance, budget, dest=None, detail=False):
    original = tensor_hash(model.state_dict())
    rows, hashes = {}, {}
    for batch in batches:
        budget.check()
        path = rollout(model, batch.evidence, detail=detail)
        if any(not torch.isfinite(v).all() for v in path.values()):
            raise FloatingPointError("nonfinite inference")
        a = arrays(path, batch, variance)
        rows[batch.condition] = metrics(path, batch, variance)
        if "state" in path and isinstance(model, Conventional):
            c = path["state"][..., 2:6].reshape(-1, 2, 2)
            rows[batch.condition]["minimum_covariance_eigenvalue"] = float(
                torch.linalg.eigvalsh(c).min()
            )
            if rows[batch.condition]["minimum_covariance_eigenvalue"] <= 0:
                raise FloatingPointError("nonpositive covariance")
        hashes[batch.condition] = input_hash(batch)
        if dest:
            dest.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(dest / (batch.condition + ".npz"), **a)
    if original != tensor_hash(model.state_dict()):
        raise RuntimeError("inference modified persistent tensors")
    result = {
        "rows": rows,
        "headline": headline(rows),
        "inputs": hashes,
        "resources": model.resources(),
        "temperature": model.temperature,
    }
    if dest:
        dump(dest / "results.json", result)
    return result


def batches(split, root, pairs=16, secondary=True):
    return [
        generate(split, root, pairs=pairs, condition=c)
        for c in PRIMARY + (SECONDARY if secondary else ())
    ]


def fixture(dest, m, budget, variance):
    root = m["fixture_root"]
    data = training_data(root, m["fixture_updates"], split="fixture")
    models, fit_seconds = [], []
    for name in ARCHITECTURES:
        path = dest / "fits" / name
        models.append(fit_one(path, name, root, data, 0.003, budget))
        fit_seconds.append(json.loads((path / "fit.json").read_text())["cpu_seconds"])
    base = fit_one(dest / "fits/BASE", "BASE", root, data, None, budget)
    models += filters(base)
    start = time.process_time()
    for model in models:
        evaluate(
            model,
            batches("fixture", root, pairs=2),
            variance,
            budget,
            dest / "evaluation" / model.name,
            detail=True,
        )
    eval_seconds = time.process_time() - start
    fit_projection = max(fit_seconds) / m["fixture_updates"] * m["train_updates"] * 49
    evaluation_projection = eval_seconds * 8 * 20  # batch scaling and calibration/report reserve
    storage_projection = size(dest / "evaluation") * 8 * 14 + size(dest) * 5
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (
        1 if sys.platform == "darwin" else 1024
    )
    projection = {
        "neural_seconds_per_full_fit_max": max(fit_seconds) / 40 * 1200,
        "cpu_with_margin": 1.5 * (fit_projection + evaluation_projection),
        "storage_with_margin": 1.5 * storage_projection,
        "rss_with_margin": 1.25 * rss,
        "fit_count_planned": 67,
        "fixture_evaluation_cpu": eval_seconds,
    }
    projection["passes"] = (
        projection["cpu_with_margin"] < 0.9 * m["limits"]["cpu_seconds"]
        and projection["storage_with_margin"] < m["limits"]["artifact_bytes"]
        and projection["rss_with_margin"] < m["limits"]["rss_bytes"]
    )
    dump(dest / "projection.json", projection)
    dump(REPORT / "fixture-projection.json", projection)
    print(json.dumps(projection), flush=True)
    if not projection["passes"]:
        raise RuntimeError("fixture feasibility projection failed; no development authorized")


def development(dest, m, budget, variance):
    projection = json.loads((OUT / "fixture/projection.json").read_text())
    if not projection["passes"]:
        raise RuntimeError("missing passing fixture")
    for root in m["development_roots"]:
        data = training_data(root)
        dev = batches("development", root, secondary=False)
        fit_one(dest / str(root) / "BASE", "BASE", root, data, None, budget)
        for name in ARCHITECTURES:
            for lr in m["learning_rates"]:
                fit_one(dest / str(root) / name / str(lr), name, root, data, lr, budget, dev)


@torch.no_grad()
def calibrate(dest, m, budget, variance):
    roots = m["development_roots"]
    selection = {
        "thresholds": {},
        "temperatures": {},
        "learning_rates": {},
        "convergence": {},
        "inventory": [],
    }
    # Thresholds use all ordinary, true-regime pre-gating FILTER2 innovations.
    for multiple in (False, True):
        values = []
        for root in roots:
            base = load_base(OUT / "development" / str(root) / "BASE")
            model = Conventional(base, "FILTER2", multiple)
            for batch in batches("development", root, secondary=False):
                if batch.condition == "misleading":
                    continue
                budget.check()
                out = rollout(model, batch.evidence)
                index = batch.labels[1:].long()[..., None]
                nis = out["nis"].gather(2, index)[..., 0]
                values.extend(nis[batch.evidence.mask[1:].sum(-1) == 6].tolist())
        selection["thresholds"]["NISEMP-M" if multiple else "NISEMP-C"] = [
            float(np.quantile(values, 0.99)),
            26.216967,
        ]
    records = []
    names = list(ARCHITECTURES) + [
        f"{kind}-{suffix}" for kind in ("ADAPT1", "FILTER2", "NISEMP") for suffix in ("C", "M")
    ]
    for name in names:
        candidates = m["learning_rates"] if name in ARCHITECTURES else [None]
        for lr in candidates:
            for temperature in m["temperatures"]:
                rows = []
                for root in roots:
                    if name in ARCHITECTURES:
                        model = load_neural(
                            OUT / "development" / str(root) / name / str(lr), name, root
                        )
                    else:
                        base = load_base(OUT / "development" / str(root) / "BASE")
                        model = next(x for x in filters(base, selection) if x.name == name)
                    model.temperature = temperature
                    result = evaluate(
                        model, batches("development", root, secondary=False), variance, budget
                    )
                    rows.append(result["headline"])
                record = {
                    "name": name,
                    "lr": lr,
                    "temperature": temperature,
                    "root_headlines": rows,
                    "brier": float(np.mean([r["brier"] for r in rows])),
                }
                records.append(record)
        choices = [r for r in records if r["name"] == name]
        best = min(choices, key=lambda r: (r["brier"], r["lr"] or 0, r["temperature"]))
        selection["temperatures"][name] = best["temperature"]
        if name in ARCHITECTURES:
            selection["learning_rates"][name] = best["lr"]
            early, late = [], []
            for root in roots:
                rec = json.loads(
                    (
                        OUT / "development" / str(root) / name / str(best["lr"]) / "fit.json"
                    ).read_text()
                )
                early.append(rec["learning"]["1050"])
                late.append(rec["learning"]["1200"])
            selection["convergence"][name] = {
                "early": early,
                "late": late,
                "relative_late_improvement": float(
                    (np.mean(early) - np.mean(late)) / max(np.mean(early), 1e-6)
                ),
            }
        print(
            json.dumps(
                {
                    "selected": name,
                    "lr": best["lr"],
                    "temperature": best["temperature"],
                    "development_brier": best["brier"],
                }
            ),
            flush=True,
        )

    def best_score(name):
        return min(r["brier"] for r in records if r["name"] == name)

    selection["r2"] = min(("PC32", "PC40"), key=lambda n: (best_score(n), int(n[2:])))
    selection["inventory"] = ["PC16", selection["r2"], "TWO16"] + names[4:]
    adequacy = {}
    for name in selection["inventory"]:
        values = []
        for root in roots:
            if name in ARCHITECTURES:
                model = load_neural(
                    OUT / "development" / str(root) / name / str(selection["learning_rates"][name]),
                    name,
                    root,
                )
            else:
                model = next(
                    x
                    for x in filters(load_base(OUT / "development" / str(root) / "BASE"), selection)
                    if x.name == name
                )
            model.temperature = selection["temperatures"][name]
            for batch in batches("development", root, secondary=False):
                if batch.condition == "misleading":
                    continue
                budget.check()
                out = rollout(model, batch.evidence)
                values.extend(
                    out["misfit"].min(-1).values[batch.evidence.mask[1:].any(-1)].tolist()
                )
        adequacy[name] = float(np.quantile(values, 0.99))
    selection["adequacy_thresholds"] = adequacy
    dump(dest / "selection.json", selection)
    dump(dest / "all-settings.json", records)
    dump(REPORT / "development-selection.json", selection)
    dump(REPORT / "development-settings.json", records)


def freeze(dest, m, budget, variance):
    selection = json.loads((OUT / "calibrate/selection.json").read_text())
    if (OUT / "confirmation").exists():
        raise RuntimeError("confirmation already exposed")
    receipt = {
        "selection": selection,
        "manifest": m,
        "source": source(),
        "normalization": variance,
        "development_sha256": sha(OUT / "calibrate/all-settings.json"),
        "budget_before_confirmation": budget.ledger,
        "review": "C-H1 only; all mandatory controls retained; no post-confirmation tuning",
    }
    receipt["sha256"] = digest(receipt)
    dump(dest / "receipt.json", receipt)
    dump(REPORT / "confirmation-receipt.json", receipt)


def receipt_check():
    receipt = json.loads((OUT / "freeze/receipt.json").read_text())
    original = receipt.pop("sha256")
    if digest(receipt) != original:
        raise RuntimeError("receipt changed")
    receipt["sha256"] = original
    for path, expected in receipt["source"]["hashes"].items():
        if sha(ROOT / path) != expected:
            raise RuntimeError("frozen source changed: " + path)
    return receipt


def confirmation(dest, m, budget, variance, repeat=False):
    receipt = receipt_check()
    selection = receipt["selection"]
    roots = m["confirmation_roots"][:1] if repeat else m["confirmation_roots"]
    for root in roots:
        data = training_data(root)
        base = fit_one(dest / str(root) / "fits/BASE", "BASE", root, data, None, budget)
        models = []
        for name in selection["inventory"][:3]:
            model = fit_one(
                dest / str(root) / "fits" / name,
                name,
                root,
                data,
                selection["learning_rates"][name],
                budget,
            )
            model.temperature = selection["temperatures"][name]
            models.append(model)
        del data
        models += filters(base, selection)
        results = {}
        for model in models:
            results[model.name] = evaluate(
                model,
                batches("confirmation", root),
                variance,
                budget,
                dest / str(root) / model.name,
                detail=True,
            )
        dump(dest / str(root) / "results.json", results)
        print(
            json.dumps({"root": root, "headlines": {n: r["headline"] for n, r in results.items()}}),
            flush=True,
        )
    if repeat:
        root = roots[0]
        checks = {}
        for name in ["BASE"] + selection["inventory"][:3]:
            paths = [
                OUT / phase / str(root) / "fits" / name / "fit.json"
                for phase in ("confirmation", "repeat")
            ]
            a, b = [json.loads(p.read_text()) for p in paths]
            checks[name] = {
                k: a[k] == b[k] for k in ("input_hash", "checkpoint_hash", "trace_hash")
            }
        for name in selection["inventory"]:
            equal = True
            count = 0
            for condition in PRIMARY + SECONDARY:
                paths = [
                    OUT / phase / str(root) / name / (condition + ".npz")
                    for phase in ("confirmation", "repeat")
                ]
                with np.load(paths[0]) as a, np.load(paths[1]) as b:
                    for key in a.files:
                        count += 1
                        equal &= np.array_equal(a[key], b[key])
            checks[name + "-arrays"] = {"exact": bool(equal), "arrays": count}
        dump(REPORT / "reproduction.json", checks)
        if not all(all(v for k, v in row.items() if k != "arrays") for row in checks.values()):
            raise RuntimeError("prescribed repeat failed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "phase",
        choices=[
            "fixture",
            "development",
            "calibrate",
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
    OUT.mkdir(exist_ok=True, parents=True)
    REPORT.mkdir(exist_ok=True, parents=True)
    dest = OUT / args.phase
    dest.mkdir(exist_ok=False)
    budget = Budget(OUT, m["limits"], args.phase)
    try:
        snapshot(dest)
        variance = normalization()
        if args.phase == "report":
            from .report import report

            report(dest, m, budget, variance)
        elif args.phase == "repeat":
            confirmation(dest, m, budget, variance, repeat=True)
        else:
            globals()[args.phase](dest, m, budget, variance)
        budget.check(force=True)
        budget.finish("complete")
    except Exception as error:
        budget.finish("failed", repr(error))
        raise


if __name__ == "__main__":
    main()
