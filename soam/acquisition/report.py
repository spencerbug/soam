"""Plots and reviewable tables from frozen paired results; no fitting."""

import json

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from soam.temporal.statistics import interval


def render(rows, stats, receipt, output, report):
    colors = {"NOWRITE": "#737373", "KV": "#0072B2", "REG": "#E69F00", "FAST": "#D55E00"}
    budgets = [0, 1, 2, 4, 8]
    fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
    for name, records in rows.items():
        cis = [interval([r["curves"][str(b)]["free8"] for r in records]) for b in budgets]
        mean = [v["mean"] for v in cis]
        ax.plot(budgets, mean, marker="o", label=name, color=colors[name])
        ax.fill_between(
            budgets, [v["lo"] for v in cis], [v["hi"] for v in cis], color=colors[name], alpha=0.15
        )
    ax.set(
        xlabel="Distinct grounded snapshots before complete reset",
        ylabel="Free-8 NMSE",
        yscale="log",
        title="Study D1: post-reset acquisition (ordinary 95% root intervals)",
    )
    ax.set_xticks(budgets)
    ax.legend(ncol=4)
    fig.savefig(report / "acquisition.png", dpi=160)
    plt.close(fig)
    fig, axs = plt.subplots(1, 4, figsize=(13, 3.6), layout="constrained")
    for ax, name in zip(axs, rows, strict=True):
        matrices = []
        for root in receipt["manifest"]["confirmation_roots"]:
            with np.load(output / "confirmation" / str(root) / name / "arrays.npz") as a:
                matrices.append(a["d2_error"][..., 1:].mean((0, 3, 4)))
        matrix = np.ma.masked_where(~np.tri(8, dtype=bool), np.mean(matrices, axis=0))
        picture = ax.imshow(matrix, vmin=0, vmax=1.5, origin="upper", cmap="magma_r")
        ax.set(
            title=name,
            xlabel="Queried object",
            xticks=range(8),
            xticklabels=range(1, 9),
            yticks=range(8),
            yticklabels=range(1, 9),
        )
    axs[0].set_ylabel("Objects acquired so far")
    fig.colorbar(picture, ax=axs, label="Mean free-8 NMSE; common scale; >1.5 saturated")
    fig.savefig(report / "retention.png", dpi=160)
    plt.close(fig)
    table = [
        "# Study D paired results",
        "",
        "All means average ten independent fitted roots.",
        "",
        "| Model | D1 J | One-shot | D2 old error | Retention change | Old accuracy | Unknown accepted |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    resources = [
        "",
        "| Model | Persistent bytes | Writable bytes | Recall mean µs | Write mean µs |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, records in rows.items():
        means = {
            k: float(np.mean([r[k] for r in records]))
            for k in (
                "J",
                "one_shot",
                "old_error",
                "retention",
                "old_accuracy",
                "false_familiarity",
                "recall_us_mean",
                "write_us_mean",
            )
        }
        table.append(
            f"| {name} | {means['J']:.6f} | {means['one_shot']:.6f} | "
            f"{means['old_error']:.6f} | {means['retention']:+.6f} | "
            f"{means['old_accuracy']:.3f} | {means['false_familiarity']:.3f} |"
        )
        r = records[0]["resources"]
        resources.append(
            f"| {name} | {r['persistent_bytes']} | {r['writable_bytes']} | "
            f"{means['recall_us_mean']:.2f} | {means['write_us_mean']:.2f} |"
        )
    table += resources
    table += [
        "",
        "Persistent bytes include shared core and scalar settings. KV preallocates 32 rows;",
        "only eight are occupied in D2. No exact resource match is claimed. FAST and REG",
        "have equal numerical persistent bytes. Recall times are serial cue-to-association",
        "calls (three warmups, twenty samples/root); writes include validation and accounting.",
        "Core action advances are identical. Profiling and scientific orchestration are charged.",
        "Python/Torch object overhead is in process RSS, not tensor bytes.",
    ]
    (report / "tables.md").write_text("\n".join(table) + "\n")
    overview = [
        "# Study D — bounded post-reset acquisition and sequential retention",
        "",
        "November 17, 2026. D0–D2 only. See the [protocol](../docs/STUDY_D_PROTOCOL.md),",
        "[paired tables](study-d/tables.md), [statistics](study-d/statistics.json),",
        "[verification](study-d/verification.json), and [source receipt](study-d/confirmation-receipt.json).",
        "",
        "## Frozen outcomes",
        "",
    ]
    for name in ("KV", "REG", "FAST"):
        s = stats[name]
        overview.append(
            f"- {name}: persistent-acquisition conjunction "
            f"{'supported' if s['acquisition_supported'] else 'not passed'}; "
            f"one-shot conjunction {'supported' if s['one_shot_supported'] else 'not passed'}."
        )
    for name, s in stats["fast_comparisons"].items():
        overview.append(
            f"- FAST versus {name}: {s['outcome']}; relative D1 gain "
            f"{s['mean']:.4f} [{s['lo']:.4f}, {s['hi']:.4f}]."
        )
    overview += [
        "",
        "These are the frozen family-adjusted conclusions; guardrails are reported separately.",
        "A failed conjunction does not mean no information was acquired. Wide intervals do not",
        "establish equivalence. Relative gains use per-root ratios, not a ratio of means.",
        "",
        "![Post-reset acquisition](study-d/acquisition.png)",
        "",
        "![Sequential retention](study-d/retention.png)",
        "",
        "## Scope and costs",
        "",
        "All candidates receive identical grounded snapshots and queries. Each offline core fit",
        "uses 2048 clean transition pairs (4096 feature snapshots). Each model/root evaluation",
        "uses 448 new acquisition snapshots, once each, and 2368 read-only queries. Repeated",
        "evaluation of old objects supplies no training evidence. There is no replay or online",
        "slow-core fitting. Calibration uses distinct development objects; confirmation is fresh.",
        "",
        "Appearance is a stable observed random feature vector. The relationship is independently",
        "random. Half the appearance coordinates are hidden at query, and no relationship is",
        "shown. The task supplies a reversible rotation family, action basis, full acquisition",
        "snapshots and a proprioceptive angle reference. It tests memory plus reuse of that",
        "fitted transformation, not learned correspondence, unknown geometry or organization.",
        "",
        "FAST is one delta-updated block of an explicitly structured recurrent state operator.",
        "Its one-step retrieval is exactly a direct linear associative map. The same-byte REG",
        "control uses mask-aware sufficient statistics; KV uses larger preallocated episodic",
        "storage. These comparisons cannot establish a special advantage of recurrence, shared",
        "neurons, attractors or general fast-weight mechanisms. Independent whole-model refitting",
        "and learned write selection were not tested. D3/D4 remain deferred.",
        "",
        "Familiarity scores are development-thresholded reconstruction distances, not calibrated",
        "probabilities. Reported accepted wrong recalls and unknown acceptance are diagnostics;",
        "they do not establish robust writing under corrupt evidence or changing objects.",
        "",
        "## Reproduction and source",
        "",
        f"Frozen source aggregate: `{receipt['source']['aggregate']}`; base commit",
        f"`{receipt['source']['commit']}`. Exact source copies, fit inputs, all predictions/errors,",
        "checkpoints, roots and status records are under `runs/study-d-v1/`. Python/Torch/NumPy,",
        "platform, dirty status and settings are in the receipt. CPU only, one Torch thread,",
        "float64, deterministic algorithms. The first full root is repeated exactly; unchanged",
        "historical Study C files are checked. No historical gate is reinterpreted.",
        "",
        "Commands: `UV_CACHE_DIR=/private/tmp/soam-uv-cache uv run python -m",
        "soam.acquisition.runner PHASE`, with fixture, development, freeze, confirmation, repeat,",
        "report in that order. Existing phase directories refuse overwrite; use an isolated",
        "checkout from the frozen snapshot for reproduction. Resource ledger includes numerical",
        "fixture, selection, calibration, confirmation, repeat, profiling and reporting. Tests,",
        "imports/process startup, source review and language-model work are separate engineering",
        "overhead; no GPU work occurred.",
        "",
    ]
    (report.parent / "STUDY_D.md").write_text("\n".join(overview))
    (report / "selected-settings.json").write_text(
        json.dumps(receipt["selection"], indent=2) + "\n"
    )
