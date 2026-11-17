"""Archived-array verification, paired-root uncertainty, runtime and scientific plots."""

import json
import time

import matplotlib
import numpy as np
import torch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from soam.encoders.projection import FixedProjection
from soam.robust.statistics import interval
from soam.temporal.runner import dump, size

from .data import PRIMARY, SECONDARY, generate
from .models import advance_support
from .runner import OUT, REPORT, filters, load_base, load_neural, receipt_check, sha


@torch.no_grad()
def inference_only(model, evidence):
    state = model.initialize(evidence.observed[0], evidence.mask[0])
    logit = state.new_zeros(len(state))
    for t, action in enumerate(evidence.actions):
        prior = model.predict(state, action, logit)
        lp = advance_support(logit)
        z, mask = evidence.observed[t + 1], evidence.mask[t + 1]
        score = model.score(prior, z, mask)[0]
        ratio = ((score[:, 1] - score[:, 0]) / model.temperature).clamp(-6, 6)
        logit = (lp + torch.where(mask.any(-1), ratio, 0)).to(state.dtype)
        state = model.retain(model.correct(prior, z, mask, logit), logit)
    return state, logit


@torch.no_grad()
def timings(model, root, budget):
    result = {}
    for batch in (1, 32):
        ev = generate("development", root, pairs=16, condition="later").evidence
        if batch == 1:
            ev = type(ev)(ev.observed[:, :1], ev.mask[:, :1], ev.actions[:, :1])
        for _ in range(3):
            inference_only(model, ev)
        values = []
        for _ in range(20):
            budget.check()
            start = time.perf_counter_ns()
            inference_only(model, ev)
            values.append((time.perf_counter_ns() - start) / 1000 / 48 / batch)
        result[str(batch)] = {
            "mean_us_per_episode_step": float(np.mean(values)),
            "p95_us_per_episode_step": float(np.quantile(values, 0.95)),
            "max_us_per_episode_step": max(values),
            "repetitions": values,
        }
    return result


def independent_reduction(root, name, expected):
    brier, nmse, amb, maximum = [], [], [], 0.0
    checks = 0
    for condition in PRIMARY:
        with np.load(OUT / "confirmation" / str(root) / name / (condition + ".npz")) as a:
            errors = np.square(a["prob"].astype(float) - a["labels"])
            cut = 27 if condition == "delayed" else 11
            score = (
                sum(errors[:cut].mean(axis=1)) / cut + sum(errors[cut:].mean(axis=1)) / (48 - cut)
            ) / 2
            first = 48 if condition in {"ambiguous", "uninformative"} else cut
            brier.append(float(score))
            nmse.append(float(np.mean(a["prior_error"], axis=0).mean()))
            amb.append(float(np.mean(errors[:first], axis=0).mean()))
            maximum = max(maximum, abs(score - expected["rows"][condition]["brier"]))
            checks += 1
    for metric, values in (("brier", brier), ("prior_nmse", nmse), ("ambiguous_brier", amb)):
        maximum = max(maximum, abs(sum(values) / 6 - expected["headline"][metric]))
        checks += 1
    if maximum > 1e-7:
        raise RuntimeError("independent reduction disagrees")
    return checks, maximum


def statistics(results, runtime, selection, m):
    roots, names = m["confirmation_roots"], selection["inventory"]
    draws = np.random.default_rng(m["bootstrap_seed"]).integers(0, len(roots), (20000, len(roots)))

    def values(name, metric):
        return np.array([results[str(r)][name]["headline"][metric] for r in roots])

    descriptive = {
        name: {
            metric: interval(values(name, metric), draws=draws)
            for metric in results[str(roots[0])][name]["headline"]
        }
        for name in names
    }
    comparisons = {}
    for candidate, reference in (
        ("TWO16", "PC16"),
        ("TWO16", selection["r2"]),
        ("ADAPT1-M", "ADAPT1-C"),
        ("TWO16", "ADAPT1-M"),
    ):
        contrasts = {
            "benefit": interval(
                values(reference, "brier") - values(candidate, "brier"), draws=draws, family=16
            )
        }
        for metric in ("prior_nmse", "ambiguous_brier", "recovery"):
            contrasts[metric] = interval(
                values(candidate, metric) - values(reference, metric), draws=draws, family=16
            )
        latency = {}
        for metric in ("mean_us_per_episode_step", "p95_us_per_episode_step"):
            ratios = [
                runtime[str(r)][candidate]["timing"]["1"][metric]
                / runtime[str(r)][reference]["timing"]["1"][metric]
                for r in roots
            ]
            latency[metric] = interval(ratios, draws=draws)
        c, ref = descriptive[candidate], descriptive[reference]
        checks = {
            "effect": contrasts["benefit"]["mean"] >= 0.01,
            "positive": contrasts["benefit"]["lo"] > 0,
            "precision": contrasts["benefit"]["width"] <= 0.04,
            "prediction_guard": contrasts["prior_nmse"]["hi"] <= 0.02,
            "ambiguity_guard": contrasts["ambiguous_brier"]["hi"] <= 0.01,
            "recovery_guard": contrasts["recovery"]["hi"] <= 4,
            "absolute_ambiguity": c["ambiguous_brier"]["mean"] <= 0.26,
            "absolute_resolution": c["late_brier"]["mean"] <= 0.15,
            "absolute_prediction": c["prior_nmse"]["mean"] <= 0.25,
            "false_confidence": c["ambiguity_confidence"]["hi"] <= 0.05,
            "reference_competence": ref["late_brier"]["mean"] <= 0.18
            and ref["prior_nmse"]["mean"] <= 0.30,
        }
        checks["optimization"] = all(
            selection["convergence"].get(n, {}).get("relative_late_improvement", 0) <= 0.2
            for n in (candidate, reference)
        )
        if reference == "ADAPT1-M":
            checks["latency"] = latency["p95_us_per_episode_step"]["mean"] <= 1.25
            checks["capacity"] = True  # no equal state-count claim across families
        else:
            checks["latency"] = all(v["mean"] <= 3 for v in latency.values())
            r = runtime[str(roots[0])]
            compare = selection["r2"] if candidate == "TWO16" else reference
            cap = 1.25 if candidate == "TWO16" else 2.5
            checks["capacity"] = (
                r[candidate]["resources"]["retained_scalars"]
                <= cap * r[compare]["resources"]["retained_scalars"]
            )
        if (
            not checks["reference_competence"]
            or not checks["optimization"]
            or not checks["precision"]
        ):
            outcome = "inconclusive competence or precision"
        elif all(checks.values()):
            outcome = "supported bounded benefit"
        elif contrasts["benefit"]["hi"] < 0.01:
            outcome = "precise exclusion of declared practical benefit"
        else:
            outcome = "inconclusive or guard/resource tradeoff"
        comparisons[candidate + " vs " + reference] = {
            "contrasts": contrasts,
            "latency_ratios": latency,
            "checks": checks,
            "outcome": outcome,
        }
    condition_stats = {}
    for name in names:
        condition_stats[name] = {}
        for condition in PRIMARY + SECONDARY:
            first = results[str(roots[0])][name]["rows"][condition]
            condition_stats[name][condition] = {
                metric: interval(
                    [results[str(r)][name]["rows"][condition][metric] for r in roots], draws=draws
                )
                for metric, value in first.items()
                if isinstance(value, (float, int))
            }
    return {
        "descriptive": descriptive,
        "comparisons": comparisons,
        "conditions": condition_stats,
        "family_size": 16,
        "bootstrap_draws": 20000,
        "bootstrap_seed": m["bootstrap_seed"],
        "independent_units": "ten independently fitted roots; pair members/episodes/times averaged within roots",
    }


def plots(stats, runtime, selection, root):
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    names = ["PC16", selection["r2"], "TWO16", "ADAPT1-C", "ADAPT1-M"]
    colors = ["#7c6b9a", "#d79427", "#058482", "#9c6665", "#2564a0"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    for ax, condition in zip(
        axes.flat, ("later", "ambiguous", "misleading", "delayed"), strict=True
    ):
        for name, color in zip(names, colors, strict=True):
            with np.load(OUT / "confirmation" / str(root) / name / (condition + ".npz")) as a:
                index = a["pairs"][0, 1]
                ax.plot(np.arange(1, 49), a["prob"][:, index], label=name, color=color)
        ax.axhline(0.5, color="gray", ls=":", lw=1)
        ax.axvline(12, color="gray", ls="--", lw=1)
        if condition == "delayed":
            ax.axvspan(12, 28, alpha=0.1, color="gray")
        ax.set(
            title=condition,
            xlabel="Physical step",
            ylabel="Support for + candidate",
            ylim=(-0.02, 1.02),
        )
    axes[0, 0].legend(ncol=2, fontsize=8)
    fig.suptitle("Study C: preselected first paired + world, first confirmation root")
    for ext in ("png", "svg"):
        fig.savefig(REPORT / ("belief-trajectories." + ext), dpi=160)
    plt.close(fig)

    p = FixedProjection(12, 1729).matrix.numpy()
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), constrained_layout=True)
    for ax, name in zip(axes, (selection["r2"], "TWO16", "ADAPT1-M"), strict=True):
        with np.load(OUT / "confirmation" / str(root) / name / "delayed.npz") as a:
            j = a["pairs"][0, 1]
            candidate = a["candidate_prior"][:, j] @ p
            ax.plot(np.arange(1, 49), candidate[:, 0, 0], label="- candidate", color="#b47723")
            ax.plot(np.arange(1, 49), candidate[:, 1, 0], label="+ candidate", color="#227f89")
            ax.plot(np.arange(1, 49), (a["target"][:, j] @ p)[:, 0], "k--", label="Actual state")
        ax.axvspan(12, 28, alpha=0.1, color="gray")
        ax.set(title=name, xlabel="Physical step", ylabel="Decoded x1 (evaluator only)")
    axes[0].legend(fontsize=8)
    fig.suptitle("Candidate-conditioned prior trajectories through an occlusion")
    for ext in ("png", "svg"):
        fig.savefig(REPORT / ("candidate-trajectories." + ext), dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    for name in selection["inventory"]:
        x = np.mean([r[name]["timing"]["1"]["p95_us_per_episode_step"] for r in runtime.values()])
        v = stats["descriptive"][name]["brier"]
        ax.errorbar(x, v["mean"], yerr=[[v["mean"] - v["lo"]], [v["hi"] - v["mean"]]], fmt="o")
        ax.annotate(name, (x, v["mean"]), xytext=(4, 5), textcoords="offset points", fontsize=8)
    ax.set(
        xlabel="Mean root p95 serial inference μs / step",
        ylabel="Brier score (95% root interval)",
        title="Probability quality and measured inference cost",
        xscale="log",
    )
    for ext in ("png", "svg"):
        fig.savefig(REPORT / ("accuracy-cost." + ext), dpi=160)
    plt.close(fig)


def report(dest, m, budget, variance):
    receipt = receipt_check()
    selection, roots = receipt["selection"], m["confirmation_roots"]
    results = {
        str(r): json.loads((OUT / "confirmation" / str(r) / "results.json").read_text())
        for r in roots
    }
    verification = {
        "independent_values": 0,
        "maximum_absolute_error": 0.0,
        "identical_evidence": {},
        "frozen_source_verified": len(receipt["source"]["hashes"]),
    }
    runtime = {}
    for root in roots:
        models = []
        for name in selection["inventory"][:3]:
            model = load_neural(OUT / "confirmation" / str(root) / "fits" / name, name, root)
            model.temperature = selection["temperatures"][name]
            models.append(model)
        models += filters(load_base(OUT / "confirmation" / str(root) / "fits/BASE"), selection)
        runtime[str(root)] = {}
        for model in models:
            n, error = independent_reduction(root, model.name, results[str(root)][model.name])
            verification["independent_values"] += n
            verification["maximum_absolute_error"] = max(
                error, verification["maximum_absolute_error"]
            )
            with (
                np.load(OUT / "confirmation" / str(root) / model.name / "change.npz") as a,
                np.load(OUT / "confirmation" / str(root) / model.name / "coherent.npz") as b,
            ):
                same = all(
                    np.array_equal(a[k], b[k])
                    for k in ("prob", "candidate_prior", "mixture_prior", "state")
                )
                verification["identical_evidence"][f"{root}/{model.name}"] = same
                if not same:
                    raise RuntimeError("identical-evidence predictions differ")
            runtime[str(root)][model.name] = {
                "resources": model.resources(),
                "timing": timings(model, root, budget),
            }
        print(json.dumps({"verified_and_profiled_root": root}), flush=True)
    stats = statistics(results, runtime, selection, m)
    adequacy = {}
    for name in selection["inventory"]:
        adequacy[name] = {}
        threshold = selection["adequacy_thresholds"][name]
        for condition in PRIMARY + SECONDARY:
            rates = []
            for root in roots:
                with np.load(OUT / "confirmation" / str(root) / name / (condition + ".npz")) as a:
                    use = a["mask"].any(-1)
                    if condition in SECONDARY:
                        use[:23] = False
                    rates.append(float((a["misfit"].min(-1)[use] > threshold).mean()))
            draws = np.random.default_rng(m["bootstrap_seed"]).integers(0, 10, (20000, 10))
            adequacy[name][condition] = interval(rates, draws=draws)
    dump(REPORT / "root-results.json", results)
    dump(REPORT / "statistics.json", stats)
    dump(REPORT / "runtime.json", runtime)
    dump(REPORT / "verification.json", verification)
    dump(REPORT / "adequacy.json", adequacy)
    plots(stats, runtime, selection, roots[0])
    lines = [
        "# Study C confirmation tables",
        "",
        "Ten independent fitted roots; ordinary 95% root intervals.",
        "",
        "| Model | Brier [95% CI] | Prior NMSE | Late Brier | Ambiguous Brier | Recovery steps | Retained scalars | Mean root p95 μs |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name in selection["inventory"]:
        d = stats["descriptive"][name]
        b = d["brier"]
        latency = np.mean(
            [runtime[str(r)][name]["timing"]["1"]["p95_us_per_episode_step"] for r in roots]
        )
        count = runtime[str(roots[0])][name]["resources"]["retained_scalars"]
        lines.append(
            f"| {name} | {b['mean']:.5f} [{b['lo']:.5f}, {b['hi']:.5f}] | {d['prior_nmse']['mean']:.5f} | {d['late_brier']['mean']:.5f} | {d['ambiguous_brier']['mean']:.5f} | {d['recovery']['mean']:.2f} | {count} | {latency:.2f} |"
        )
    lines += ["", "## Frozen comparisons", ""]
    for comparison, row in stats["comparisons"].items():
        b = row["contrasts"]["benefit"]
        lines.append(
            f"- {comparison}: {row['outcome']}; Brier improvement {b['mean']:.5f} [{b['lo']:.5f}, {b['hi']:.5f}], family-adjusted."
        )
    (REPORT / "tables.md").write_text("\n".join(lines) + "\n")
    index = {
        str(p.relative_to(OUT.parent.parent)): sha(p)
        for p in OUT.rglob("*")
        if p.is_file() and "report" not in p.relative_to(OUT).parts and p.name != "ledger.json"
    }
    dump(REPORT / "artifact-sha256.json", index)
    dump(
        REPORT / "resource-before-report-close.json",
        {
            "prior_phases": budget.ledger,
            "report_cpu_so_far": time.process_time() - budget.cpu,
            "raw_bytes": size(OUT),
            "compact_bytes": size(REPORT),
            "fits": len(list(OUT.glob("**/fit-status.json"))),
            "frozen_source": receipt["source"]["aggregate"],
        },
    )
    print(
        json.dumps({"comparisons": {k: v["outcome"] for k, v in stats["comparisons"].items()}}),
        flush=True,
    )
