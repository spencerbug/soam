"""One frozen Study B supplement: explicit residual/action magnitudes, fresh streams."""

import argparse
import hashlib
import json
import resource
import shutil
import sys
from pathlib import Path

import numpy as np
import torch
from torch import nn

from soam.platform.core import derived_seed
from soam.temporal.data import input_hash, normalization, seed, training_data
from soam.temporal.engine import evaluate, fit, headline, primary_batches, primary_score
from soam.temporal.models import Neural, make
from soam.temporal.runner import ROOT, Budget, digest, dump, size, source_identity, tensor_hash
from soam.temporal.statistics import interval

MANIFEST = ROOT / "docs/protocols/study_b_magnitude_v1.json"
PROTOCOL = ROOT / "docs/STUDY_B_MAGNITUDE_PROTOCOL.md"


def mapped_root(root):
    return derived_seed("soam-study-b-magnitude", 1, "root", root, 0, "mapping")


class Magnitude(Neural):
    def __init__(self, name, initialization):
        super().__init__("AM32" if name == "AMN32" else "GA32", initialization)
        self.name = name
        self.gate = nn.Linear(27 + self.n + 2 + (name == "GMN32"), 1)
        nn.init.zeros_(self.gate.weight)
        nn.init.zeros_(self.gate.bias)
        if name == "AMN32":
            self.motion = nn.Linear(self.n + 6, 1)
            nn.init.zeros_(self.motion.weight)
            nn.init.zeros_(self.motion.bias)

    def predict(self, h, a, q):
        if self.name != "AMN32":
            return super().predict(h, a, q)
        norm = torch.linalg.vector_norm(a, dim=-1, keepdim=True)
        beta = 2 * torch.sigmoid(self.motion(torch.cat((h, a, q, norm), -1)))
        return 0.5 * h + 0.5 * torch.tanh(self.W(h) + beta * self.A(a) + self.Q(q)), beta

    def gate_features(self, prior, a, z, mask, sd):
        residual = (z - self.readout(prior)) * mask
        rms = (
            residual.square().sum(-1, keepdim=True) / mask.sum(-1, keepdim=True).clamp_min(1)
            + 1e-12
        ).sqrt()
        norm = torch.linalg.vector_norm(a, dim=-1, keepdim=True)
        values = [mask.float(), residual, prior, a, rms, norm]
        if self.name == "GMN32":
            values.append(sd)
        return torch.cat(values, -1), residual

    def correct(self, prior, previous, a, q, z, m, sd, *, metadata=False):
        features, residual = self.gate_features(prior, a, z, m, sd)
        gamma = torch.sigmoid(self.gate(features))
        updated = prior + gamma * torch.tanh(self.E(torch.cat((residual, m.float()), -1)))
        present = m.any(-1, keepdim=True)
        return torch.where(present, updated, prior), gamma * present

    def resources(self):
        r = super().resources()
        if self.name == "AMN32":
            r["predict_macs"] += 1
        r["nonlinear_note"] += (
            "; sensory residual RMS and action norm (squares, sums, sqrt), motion norm additionally for AMN32"
        )
        return r


def candidate(name, root):
    initialization = seed("train", mapped_root(root), 0, "initialization")
    return (
        Magnitude(name, initialization)
        if name in {"GN32", "GMN32", "AMN32"}
        else make(name, initialization)
    )


def identity():
    source = source_identity()
    for p in (MANIFEST, PROTOCOL):
        source["hashes"][str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    source["aggregate"] = digest(source["hashes"])
    return source


def decision(heads, unresolved=()):
    contrasts = {}
    gains = []
    guards = []
    for control in ("PC32", "GA32"):
        c = np.array([h["J"] for h in heads[control]])
        x = np.array([h["J"] for h in heads["GN32"]])
        ci = interval((c - x) / np.maximum(c, 1e-6), alpha=0.005, seed=15307)
        contrasts[control + "/gain"] = ci
        gains.append(ci)
        for key in ("clean", "corrupt", "change", "free32"):
            ci = interval(
                [a[key] - b[key] for a, b in zip(heads["GN32"], heads[control], strict=True)],
                alpha=0.005,
                seed=15307,
            )
            contrasts[control + "/" + key] = ci
            guards.append(ci)
    competent = np.mean([h["J"] for h in heads["GN32"]]) <= 0.15
    if unresolved or not competent or any(c["width"] > 0.4 for c in gains):
        outcome = "inconclusive"
    elif all(c["mean"] >= 0.1 and c["lo"] > 0 for c in gains) and all(
        c["hi"] <= 0.01 for c in guards
    ):
        outcome = "supported"
    elif any(c["lo"] > 0.01 for c in guards):
        outcome = "tradeoff"
    elif any(c["hi"] < 0.1 for c in gains):
        outcome = "negative practical advantage"
    else:
        outcome = "inconclusive"
    return {
        "outcome": outcome,
        "competent": bool(competent),
        "optimization_unresolved": list(unresolved),
        "comparisons": contrasts,
    }


def fit_one(output, phase, name, root, setting, data, budget, variance, development=None):
    dest = output / phase / str(root) / name / str(setting)
    dest.mkdir(parents=True, exist_ok=False)
    dump(dest / "status.json", {"status": "running"})
    if len(list(output.glob("**/status.json"))) > 112:
        raise RuntimeError("Supplement fit ceiling")
    try:
        model = candidate(name, root)
        result = fit(model, data, setting, budget.check, development=development, variance=variance)
        result.update(
            name=name,
            root=root,
            effective_root=mapped_root(root),
            setting=setting,
            input_hash=input_hash(data),
            checkpoint_hash=tensor_hash(model.state_dict()),
            resources=model.resources(),
        )
        result["trace_hash"] = digest(result["trace"])
        torch.save(model.state_dict(), dest / "checkpoint.pt")
        dump(dest / "fit.json", result)
        dump(dest / "status.json", {"status": "fit complete"})
        budget.check(force=True)
        return model, dest, result
    except BaseException as error:
        dump(dest / "status.json", {"status": "failed", "error": repr(error)})
        raise


def run_phase(phase, output, m, budget, variance):
    if phase == "fixture":
        data = training_data(mapped_root(m["fixture_root"]), updates=20, batch=4, split="fixture")
        rows = []
        for name in m["candidates"]:
            setting = 0.0001 if name == "FILTER2" else 0.003
            model, dest, result = fit_one(
                output, phase, name, m["fixture_root"], setting, data, budget, variance
            )
            _, _, cpu = evaluate(
                model,
                "fixture",
                mapped_root(m["fixture_root"]),
                variance,
                full=False,
                check=budget.check,
            )
            rows.append({"name": name, "fit_cpu": result["fit_cpu_seconds"], "cell_cpu": cpu})
        projection = 1.5 * sum(r["fit_cpu"] * 60 * 15 + r["cell_cpu"] * 54 * 15 for r in rows)
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (
            1 if sys.platform == "darwin" else 1024
        )
        record = {
            "rows": rows,
            "remaining_projected_cpu": projection,
            "projected_artifact_bytes": 300000000,
            "peak_rss_bytes": rss,
            "pass": bool(
                projection < 0.9 * m["cpu_seconds"] - budget.spent_cpu
                and rss * 1.25 < m["rss_bytes"]
                and 300000000 < m["artifact_bytes"]
            ),
        }
        dump(output / "fixture-projection.json", record)
        if not record["pass"]:
            raise RuntimeError("Supplement feasibility failed")
    elif phase == "development":
        if not json.loads((output / "fixture-projection.json").read_text())["pass"]:
            raise RuntimeError("Fixture required")
        for root in m["development_roots"]:
            data = training_data(mapped_root(root))
            dev = primary_batches("development", mapped_root(root))
            for name in m["candidates"]:
                for setting in m["ridge_penalties"] if name == "FILTER2" else m["learning_rates"]:
                    model, dest, result = fit_one(
                        output, phase, name, root, setting, data, budget, variance, dev
                    )
                    score = primary_score(model, dev, variance, k=0)
                    dump(dest / "score.json", {"J": score})
                    print(
                        json.dumps({"root": root, "name": name, "setting": setting, "J": score}),
                        flush=True,
                    )
    elif phase == "freeze":
        selected = {}
        unresolved = []
        times = []
        for name in m["candidates"]:
            choices = []
            for setting in m["ridge_penalties"] if name == "FILTER2" else m["learning_rates"]:
                dirs = [
                    output / "development" / str(r) / name / str(setting)
                    for r in m["development_roots"]
                ]
                choices.append(
                    (
                        np.mean([json.loads((d / "score.json").read_text())["J"] for d in dirs]),
                        setting,
                        dirs,
                    )
                )
            j, setting, dirs = min(choices, key=lambda x: (x[0], x[1]))
            fs = [json.loads((d / "fit.json").read_text()) for d in dirs]
            late = (
                0.0
                if name == "FILTER2"
                else float(
                    1
                    - np.mean([f["learning"]["1200"] for f in fs])
                    / np.mean([f["learning"]["1050"] for f in fs])
                )
            )
            if name in {"GN32", "PC32", "GA32"} and late > 0.2:
                unresolved.append(name)
            selected[name] = {"setting": setting, "J": float(j), "late_improvement": late}
            times.append(np.mean([f["fit_cpu_seconds"] for f in fs]))
        projection = (
            1.5
            * 11
            * (
                sum(times)
                + 54
                * sum(
                    r["cell_cpu"]
                    for r in json.loads((output / "fixture-projection.json").read_text())["rows"]
                )
            )
        )
        receipt = {
            "source": identity()["aggregate"],
            "manifest": digest(m),
            "selection": selected,
            "optimization_unresolved": unresolved,
            "projected_remaining_cpu": float(projection),
            "spent_cpu": budget.spent_cpu,
            "normalization": variance,
            "root_mapping": {str(r): mapped_root(r) for r in m["confirmation_roots"]},
            "prior_v1_receipt": json.loads(
                (ROOT / "runs/study-b-v1/confirmation-receipt.json").read_text()
            )["sha256"],
        }
        if projection > 0.9 * m["cpu_seconds"] - budget.spent_cpu:
            raise RuntimeError("Remaining supplement allocation fails")
        receipt["sha256"] = digest(receipt)
        with (output / "confirmation-receipt.json").open("x") as f:
            json.dump(receipt, f, indent=2, sort_keys=True)
        print(json.dumps(receipt), flush=True)
    elif phase in {"confirmation", "repeat"}:
        receipt = json.loads((output / "confirmation-receipt.json").read_text())
        assert receipt["sha256"] == digest({k: v for k, v in receipt.items() if k != "sha256"})
        assert receipt["source"] == identity()["aggregate"] and receipt["manifest"] == digest(m)
        for root in [m["repeat_root"]] if phase == "repeat" else m["confirmation_roots"]:
            data = training_data(mapped_root(root))
            for name in m["candidates"]:
                setting = receipt["selection"][name]["setting"]
                model, dest, result = fit_one(
                    output, phase, name, root, setting, data, budget, variance
                )
                rows, arrays, cpu = evaluate(
                    model, "confirmation", mapped_root(root), variance, check=budget.check
                )
                e = {
                    "headline": headline(rows),
                    "rows": rows,
                    "inference_cpu": cpu,
                    "prediction_hash": tensor_hash(
                        {k: torch.from_numpy(v) for k, v in arrays.items()}
                    ),
                }
                dump(dest / "evaluation.json", e)
                np.savez_compressed(dest / "errors.npz", **arrays)
                dump(dest / "status.json", {"status": "complete"})
                budget.check(force=True)
                print(json.dumps({"root": root, "name": name, **e["headline"]}), flush=True)
        if phase == "repeat":
            checks = {}
            for name in m["candidates"]:
                relative = (
                    Path(str(m["repeat_root"])) / name / str(receipt["selection"][name]["setting"])
                )
                a, b = [
                    json.loads((output / p / relative / "fit.json").read_text())
                    for p in ("confirmation", "repeat")
                ]
                es = [
                    json.loads((output / p / relative / "evaluation.json").read_text())
                    for p in ("confirmation", "repeat")
                ]
                checks[name] = {
                    k: a[k] == b[k] for k in ("input_hash", "checkpoint_hash", "trace_hash")
                }
                checks[name]["predictions"] = es[0]["prediction_hash"] == es[1]["prediction_hash"]
            dump(output / "reproduction.json", checks)
            assert all(all(v.values()) for v in checks.values())
    elif phase == "report":
        report(output, m, budget)


def report(output, m, budget):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    receipt = json.loads((output / "confirmation-receipt.json").read_text())
    dest = ROOT / "reports/study-b-magnitude"
    dest.mkdir(exist_ok=True)
    heads = {}
    resources = {}
    audit = []
    gain = {}
    for name in m["candidates"]:
        heads[name] = []
        fs = []
        es = []
        for root in m["confirmation_roots"]:
            d = (
                output
                / "confirmation"
                / str(root)
                / name
                / str(receipt["selection"][name]["setting"])
            )
            f = json.loads((d / "fit.json").read_text())
            e = json.loads((d / "evaluation.json").read_text())
            fs.append(f)
            es.append(e)
            heads[name].append(e["headline"])
            with np.load(d / "errors.npz") as arrays:
                j = np.mean(
                    [
                        arrays[f"{c}__{s}__prior"].astype(float).mean()
                        for c in ("partial", "missing", "noise")
                        for s in ("every2", "every4", "every8", "irregular")
                    ]
                )
            assert abs(j - e["headline"]["J"]) < 1e-7
            audit.append({"root": root, "name": name, "J": float(j), "match": True})
        resources[name] = {
            **fs[0]["resources"],
            "mean_fit_cpu": float(np.mean([f["fit_cpu_seconds"] for f in fs])),
            "mean_evaluation_cpu": float(np.mean([e["inference_cpu"] for e in es])),
        }
        gain[name] = {
            c: {
                key: interval(
                    [np.mean(e["rows"][c + "/every1"][key][23:31]) for e in es], seed=15307
                )
                for key in ("gamma_curve", "beta_curve")
            }
            for c in ("partial", "noise", "corrupt", "contradict", "change", "motion")
        }
    stats = {
        name: {key: interval([h[key] for h in hs], seed=15307) for key in hs[0]}
        for name, hs in heads.items()
    }
    result = decision(heads, receipt["optimization_unresolved"])
    comparisons = {}
    for candidate_name, control in [
        ("GN32", "GA32"),
        ("GMN32", "GN32"),
        ("AMN32", "GN32"),
        ("GN32", "PC16"),
    ]:
        comparisons[candidate_name + "-" + control] = {
            key: interval(
                [
                    a[key] - b[key]
                    for a, b in zip(heads[candidate_name], heads[control], strict=True)
                ],
                seed=15307,
            )
            for key in ("J", "corrupt", "change", "free32")
        }
    for name, value in [
        ("root-results", heads),
        ("statistics", stats),
        ("primary-decision", result),
        ("resources", resources),
        ("audit", audit),
        ("gain-summaries", gain),
        ("secondary-comparisons", comparisons),
    ]:
        dump(dest / (name + ".json"), value)
    table = [
        "# Study B magnitude supplement",
        "",
        "Fresh confirmation roots; ordinary 95% root intervals. No pooling with v1.",
        "",
        "| Model | J [95% CI] | Corrupt | True change | Free32 | MAC/step | Fitted scalars |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name, s in stats.items():
        j = s["J"]
        table.append(
            f"| {name} | {j['mean']:.5f} [{j['lo']:.5f}, {j['hi']:.5f}] | {s['corrupt']['mean']:.5f} | {s['change']['mean']:.5f} | {s['free32']['mean']:.5f} | {s['macs']['mean']:.0f} | {resources[name]['fitted_scalars']} |"
        )
    (dest / "tables.md").write_text("\n".join(table) + "\n")
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
    for name, s in stats.items():
        axes[0].scatter(s["macs"]["mean"], s["J"]["mean"])
        axes[0].annotate(name, (s["macs"]["mean"], s["J"]["mean"]), fontsize=8)
        axes[1].scatter(s["corrupt"]["mean"], s["change"]["mean"])
        axes[1].annotate(name, (s["corrupt"]["mean"], s["change"]["mean"]), fontsize=8)
    axes[0].set_xscale("log")
    axes[0].set_xlabel("Linear MAC / physical step")
    axes[0].set_ylabel("Pre-correction NMSE J")
    axes[1].set_xlabel("Corruption NMSE")
    axes[1].set_ylabel("True-change NMSE")
    fig.savefig(dest / "tradeoffs.png", dpi=160)
    plt.close(fig)
    for file in (
        "confirmation-receipt.json",
        "reproduction.json",
        "source.json",
        "manifest.json",
        "fixture-projection.json",
    ):
        shutil.copyfile(output / file, dest / file)
    budget.check(force=True)
    print(json.dumps({"outcome": result["outcome"], "audit_rows": len(audit)}), flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--phase",
        choices=["fixture", "development", "freeze", "confirmation", "repeat", "report"],
        required=True,
    )
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    source = identity()
    if (output / "source.json").exists():
        assert source["aggregate"] == json.loads((output / "source.json").read_text())["aggregate"]
        m = json.loads((output / "manifest.json").read_text())
    else:
        m = json.loads(MANIFEST.read_text())
        previous = ROOT / "runs/study-b-v1"
        old_bytes = size(previous) + size(ROOT / "reports/study-b")
        m["artifact_bytes"] -= old_bytes
        m["carried_artifact_bytes"] = old_bytes
        dump(output / "ledger.json", json.loads((previous / "ledger.json").read_text()))
        dump(output / "source.json", source)
        dump(output / "manifest.json", m)
        for rel in source["hashes"]:
            path = output / "source" / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, path)
    with (output / (args.phase + "-started.json")).open("x") as f:
        json.dump({"source": source["aggregate"]}, f)
    budget = Budget(output, m, "magnitude-" + args.phase)
    try:
        run_phase(args.phase, output, m, budget, normalization())
        budget.check(force=True)
        budget.finish("complete")
    except BaseException as error:
        budget.finish("failed", repr(error))
        raise


if __name__ == "__main__":
    main()
