"""Auditable root tables and static scientific figures; no fitting or selection."""

import json
import shutil

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from soam.temporal.data import CONDITIONS, SCHEDULES
from soam.temporal.models import SETTLERS
from soam.temporal.statistics import interval, primary_decision


def render(output, manifest, budget):
    from soam.temporal.runner import ROOT, dump

    receipt = json.loads((output / "confirmation-receipt.json").read_text())
    folder = output / "report"
    folder.mkdir(exist_ok=False)
    fits, evals, diagnostics, heads = {}, {}, {}, {}
    audit = []
    for name in manifest["candidates"]:
        fits[name], evals[name], diagnostics[name] = [], [], []
        for root in manifest["confirmation_roots"]:
            budget.check()
            d = (
                output
                / "confirmation"
                / str(root)
                / name
                / str(receipt["selection"][name]["setting"])
            )
            fits[name].append(json.loads((d / "fit.json").read_text()))
            e = json.loads((d / "evaluation.json").read_text())
            evals[name].append(e)
            diagnostics[name].append(json.loads((d / "diagnostics.json").read_text()))
            with np.load(d / "errors.npz") as arrays:
                j = np.mean(
                    [
                        arrays[f"{c}__{s}__prior"].astype(float).mean()
                        for c in ("partial", "missing", "noise")
                        for s in ("every2", "every4", "every8", "irregular")
                    ]
                )
            audit.append(
                {
                    "name": name,
                    "root": root,
                    "reduced_J": float(j),
                    "reported_J": e["headline"]["J"],
                    "matches": bool(abs(j - e["headline"]["J"]) < 1e-7),
                }
            )
        heads[name] = [e["headline"] for e in evals[name]]
    if not all(r["matches"] for r in audit):
        raise RuntimeError("Independent error reduction differs")
    statistics = {
        name: {key: interval([v[key] for v in rows]) for key in rows[0]}
        for name, rows in heads.items()
    }
    decision = primary_decision(heads, receipt["optimization_unresolved"])
    dump(folder / "root-results.json", heads)
    dump(folder / "statistics.json", statistics)
    dump(folder / "primary-decision.json", decision)
    dump(folder / "audit.json", audit)
    condition_stats = {
        name: {
            key: {
                metric: interval([e["rows"][key][metric] for e in evals[name]])
                for metric in (
                    "prior",
                    "posterior",
                    "free8",
                    "free32",
                    "recovery_steps",
                    "recovery_censored_fraction",
                    "updates_per_step",
                    "macs_per_step",
                    "settles_per_event",
                )
            }
            for key in evals[name][0]["rows"]
        }
        for name in heads
    }
    dump(folder / "condition-statistics.json", condition_stats)
    secondary = {}
    for a, b in [
        ("PC16", "MIX16"),
        ("PC32", "MIX32"),
        ("AM32", "GA32"),
        ("GMETA32", "GA32"),
        ("FILTER2", "L2"),
        ("RESET2", "L2"),
    ]:
        secondary[f"{a}-{b}"] = {
            key: interval([x[key] - y[key] for x, y in zip(heads[a], heads[b], strict=True)])
            for key in ("J", "corrupt", "change", "free32")
        }
    settling = {}
    for name in SETTLERS:
        settling[name] = {
            mode: {
                key: interval([d[mode]["headline"][key] for d in diagnostics[name]])
                for key in diagnostics[name][0][mode]["headline"]
            }
            for mode in diagnostics[name][0]
        }
    for k in (0, 1, 2, 4):
        for ref in ("REP32", "MIXC32"):
            secondary[f"SET32-{ref}/k{k}"] = interval(
                [
                    x[f"fixed{k}"]["headline"]["J"] - y[f"fixed{k}"]["headline"]["J"]
                    for x, y in zip(diagnostics["SET32"], diagnostics[ref], strict=True)
                ]
            )
    dump(folder / "secondary-comparisons.json", secondary)
    dump(folder / "settling-statistics.json", settling)
    resources = {
        name: {
            **fits[name][0]["resources"],
            "mean_fit_cpu": float(np.mean([f["fit_cpu_seconds"] for f in fits[name]])),
            "mean_evaluation_cpu": float(
                np.mean([e["inference_cpu_seconds"] for e in evals[name]])
            ),
            "training_episodes": 1200 * 8,
            "training_feature_targets": 1200 * 8 * 17,
            "gradient_updates": 0 if name in {"L2", "RESET2", "FILTER2"} else 1200,
            "setting": receipt["selection"][name],
        }
        for name in heads
    }
    dump(folder / "resources.json", resources)
    table = [
        "# Study B confirmation root summary",
        "",
        "Ordinary 95% paired-root bootstrap intervals; primary adjusted contrasts are separate.",
        "",
        "| Model | Prior J [95% CI] | Free32 | Corrupt | True change | MAC/step | State | Scalars | Fit CPU s |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name, stats in statistics.items():
        j = stats["J"]
        r = resources[name]
        table.append(
            f"| {name} | {j['mean']:.5f} [{j['lo']:.5f}, {j['hi']:.5f}] | {stats['free32']['mean']:.5f} | {stats['corrupt']['mean']:.5f} | {stats['change']['mean']:.5f} | {stats['macs']['mean']:.0f} | {r['state_floats']} | {r['fitted_scalars']} | {r['mean_fit_cpu']:.2f} |"
        )
    (folder / "tables.md").write_text("\n".join(table) + "\n")
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), layout="constrained")
    for name, stats in statistics.items():
        j = stats["J"]["mean"]
        r = resources[name]
        axes[0].scatter(stats["macs"]["mean"], j)
        axes[0].annotate(
            name, (stats["macs"]["mean"], j), xytext=(3, 2), textcoords="offset points", fontsize=7
        )
        axes[1].scatter(r["mean_fit_cpu"], j)
        axes[1].annotate(
            name, (r["mean_fit_cpu"], j), xytext=(3, 2), textcoords="offset points", fontsize=7
        )
    for ax in axes:
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.set_ylabel("Pre-correction NMSE J (lower is better)")
        ax.grid(alpha=0.2)
    axes[0].set_xlabel("Linear MAC estimate / physical step (solves excluded)")
    axes[1].set_xlabel("Mean fitting CPU seconds / root")
    fig.savefig(folder / "resource-frontier.png", dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), layout="constrained")
    colors = {
        name: plt.cm.tab10(i)
        for i, name in enumerate(("MIX32", "PC32", "GA32", "AM32", "FILTER2", "RESET2"))
    }
    for ax, c in zip(axes, ("partial", "corrupt", "change"), strict=True):
        for name, color in colors.items():
            values = np.array([e["rows"][c + "/every4"]["prior_curve"] for e in evals[name]])
            ax.plot(np.arange(1, 65), values.mean(0), label=name, color=color)
        ax.set_title(c)
        ax.set_xlabel("Physical step")
        ax.set_ylabel("Pre-correction NMSE")
        ax.set_yscale("log")
        ax.grid(alpha=0.2)
    axes[-1].legend(fontsize=7)
    fig.savefig(folder / "stress-responses.png", dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
    for name in sorted(SETTLERS):
        xs = [0, 1, 2, 4]
        ys = [settling[name][f"fixed{k}"]["J"]["mean"] for k in xs]
        axes[0].plot(xs, ys, "o-", label=name)
        for mode, stats in settling[name].items():
            axes[1].scatter(stats["macs"]["mean"], stats["J"]["mean"])
            axes[1].annotate(
                name + ":" + mode, (stats["macs"]["mean"], stats["J"]["mean"]), fontsize=6
            )
    axes[0].set_xlabel("Extra zero-time iterations / sensed event")
    axes[0].set_ylabel("Pre-correction NMSE J")
    axes[0].legend()
    axes[1].set_xlabel("Linear MAC / physical step")
    axes[1].set_ylabel("Pre-correction NMSE J")
    fig.savefig(folder / "settling-frontier.png", dpi=160)
    plt.close(fig)
    # Every required condition and sensing schedule, in a compact model/error heatmap.
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), layout="constrained")
    for ax, groups, kind in [(axes[0], CONDITIONS, "condition"), (axes[1], SCHEDULES, "schedule")]:
        values = []
        for name in heads:
            values.append(
                [
                    np.mean(
                        [
                            e["rows"][c + "/" + s]["prior"]
                            for e in evals[name]
                            for c in CONDITIONS
                            for s in SCHEDULES
                            if (c if kind == "condition" else s) == g
                        ]
                    )
                    for g in groups
                ]
            )
        im = ax.imshow(np.log10(np.maximum(values, 1e-6)), aspect="auto", cmap="viridis_r")
        ax.set_xticks(range(len(groups)), groups, rotation=45, ha="right")
        ax.set_yticks(range(len(heads)), list(heads))
        fig.colorbar(im, ax=ax, label="log10 pre-correction NMSE")
    fig.savefig(folder / "conditions.png", dpi=160)
    plt.close(fig)
    for file in (
        "confirmation-receipt.json",
        "reproduction.json",
        "source.json",
        "manifest.json",
        "fixture-projection.json",
    ):
        shutil.copyfile(output / file, folder / file)
    dest = ROOT / "reports/study-b"
    dest.mkdir(exist_ok=True)
    for p in folder.iterdir():
        shutil.copyfile(p, dest / p.name)
    return {"decision": decision["outcome"], "audit_rows": len(audit), "models": len(heads)}
