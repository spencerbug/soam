"""Render frozen B2 results. No fitting, candidates, thresholds or selection changes."""

import hashlib
import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from soam.robust.data import CORRUPTION, EXTENSIONS, INTERMITTENT, SENSED
from soam.robust.runner import MANIFEST, OUT, ROOT, receipt_check
from soam.robust.statistics import interval
from soam.temporal.data import CONDITIONS
from soam.temporal.runner import Budget, dump

DEST = ROOT / "reports/study-b2"
COLORS = {
    "FILTER2": "#64748b",
    "STABLE": "#a1a1aa",
    "PC16": "#7c3aed",
    "R100": "#d97706",
    "NIS99": "#dc2626",
    "CHANNEL2": "#0891b2",
    "NISEMP": "#2563eb",
    "ADAPT1": "#059669",
}


def save(fig, name):
    fig.savefig(DEST / f"{name}.png", dpi=170, bbox_inches="tight")
    fig.savefig(DEST / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def cell_stats(receipt, m):
    roots = receipt["confirmation_roots"]
    names = receipt["inventory"]
    draws = np.random.default_rng(m["bootstrap_seed"]).integers(
        0, len(roots), (m["bootstrap_resamples"], len(roots))
    )
    source = {
        n: [
            json.loads((OUT / "confirmation" / str(r) / n / "results.json").read_text())
            for r in roots
        ]
        for n in names
    }
    fields = (
        "prior",
        "posterior",
        "recovery",
        "censored",
        "recovery_after_end",
        "censored_after_end",
        "event_exposure",
        "rejected",
        "downweighted",
        "mean_weight",
        "tail95",
        "worst",
        "nis",
        "accepted_nis",
        "coverage95",
        "feature_coverage95",
        "mahalanobis",
        "covariance_trace",
        "min_eigenvalue",
        "max_asymmetry",
        "delta_norm",
        "gain_norm",
    )
    results = {}
    for n, records in source.items():
        results[n] = {}
        for c in (*CONDITIONS, *EXTENSIONS):
            schedules = SENSED if c in CONDITIONS else INTERMITTENT
            first = records[0]["rows"][f"{c}/{schedules[0]}"]
            results[n][c] = {
                k: interval(
                    [np.mean([r["rows"][f"{c}/{s}"][k] for s in schedules]) for r in records],
                    draws=draws,
                )
                for k in fields
                if k in first
            }
    dump(DEST / "condition-statistics.json", results)
    worst = {}
    for name, records in source.items():
        cells = [
            (v["worst"], roots[i], key, v["worst_episode"])
            for i, r in enumerate(records)
            for key, v in r["rows"].items()
            if key.split("/")[0] in CORRUPTION and not key.endswith("/initial")
        ]
        value, root, cell, episode = max(cells)
        worst[name] = {"episode_mean_nmse": value, "root": root, "cell": cell, "episode": episode}
    dump(DEST / "worst-cases.json", worst)
    return source, results


def resources(receipt, source):
    root = receipt["confirmation_roots"][0]
    result = {}
    for name in receipt["inventory"]:
        record = source[name][0]
        latency = json.loads((OUT / "confirmation" / str(root) / name / "latency.json").read_text())
        ops = json.loads((OUT / "confirmation" / str(root) / name / "operations.json").read_text())
        state = record["resources"]["state_floats"]
        scalar_bytes = 4 if name in ("PC16", "FILTER2") else 8
        fit_name = "PC16" if name == "PC16" else "FILTER2"
        fit_records = [
            json.loads(
                (OUT / "confirmation" / str(r) / "fits" / f"{fit_name}-fit.json").read_text()
            )
            for r in receipt["confirmation_roots"]
        ]
        searches = []
        for phase in ("screen1", "screen2", "hybrid"):
            for p in (OUT / phase).glob(f"*/{name}/results.json"):
                searches.append(json.loads(p.read_text())["evaluation_cpu_seconds"])
        result[name] = {
            "fitted_scalars": 1340 if name == "PC16" else 64,
            "persistent_allocated_bytes": record["resources"]["persistent_bytes"],
            "persistent_used_bytes": 5360 if name == "PC16" else 65 * scalar_bytes,
            "transient_state_and_covariance_bytes": state * scalar_bytes,
            "state_scalars": state,
            "covariance_scalars": 0 if name == "PC16" else 4,
            "additional_history_scalars": max(0, state - 6) if name != "PC16" else 0,
            "mean_base_fit_cpu_seconds": float(
                np.mean([x["fit_cpu_seconds"] for x in fit_records])
            ),
            "screen_eval_cpu_seconds": sum(searches),
            "confirmation_evaluation_with_diagnostics_cpu_seconds": sum(
                r["evaluation_cpu_seconds"] for r in source[name]
            ),
            "latency": latency,
            "operations": ops,
            "config": record["config"],
            "exposure_per_root": fit_records[0]["exposure"],
            "note": "Shared FILTER2 fits counted once across correctors. Controller constants are explicit config; sizeof Python config objects excluded from numerical tensor storage. Float64 robust versus float32 original/neural. Latency is minimal serial loop every4; diagnostics excluded.",
        }
    dump(DEST / "resources.json", result)
    return result


def plots(receipt, stats, res):
    names = [n for n in receipt["inventory"] if n != "STABLE"]
    summary = stats["descriptive"]
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7), layout="constrained")
    offsets = {
        "FILTER2": (-45, 8),
        "PC16": (-30, 8),
        "R100": (-10, -20),
        "NIS99": (-16, 8),
        "CHANNEL2": (-30, 8),
        "NISEMP": (-10, -18),
        "ADAPT1": (7, 8),
    }
    for ax, metric, label in zip(
        axes, ("C", "corrupt"), ("Balanced corruption C", "Original corruption NMSE"), strict=True
    ):
        for n in names:
            x, y = summary[n]["J"]["mean"], summary[n][metric]["mean"]
            xerr = [[x - summary[n]["J"]["lo"]], [summary[n]["J"]["hi"] - x]]
            yerr = [[y - summary[n][metric]["lo"]], [summary[n][metric]["hi"] - y]]
            ax.errorbar(x, y, xerr=xerr, yerr=yerr, color=COLORS[n], alpha=0.5, linewidth=1)
            marker = "X" if n in ("PC16", "R100", "NIS99") else "o"
            ax.scatter(
                x,
                y,
                s=res[n]["latency"]["1"]["mean_us_per_step"] * 1.2,
                color=COLORS[n],
                marker=marker,
                zorder=3,
            )
            ax.annotate(n, (x, y), xytext=offsets[n], textcoords="offset points", fontsize=9)
        ax.set(xlabel="Ordinary prediction J (lower is better)", ylabel=label)
        ax.grid(alpha=0.15)
    fig.suptitle(
        "B2 confirmation: accuracy, corruption and measured cost\nMarker area ∝ single-episode CPU latency; X marks genuine-change target failure; ordinary 95% root intervals",
        fontsize=12,
    )
    save(fig, "pareto")
    root = receipt["confirmation_roots"][0]
    arrays = {n: np.load(OUT / "confirmation" / str(root) / n / "arrays.npz") for n in names}
    checkpoint = torch.load(OUT / "confirmation" / str(root) / "fits/FILTER2.pt", weights_only=True)
    H = checkpoint["P"].numpy()
    mean = checkpoint["mean"].numpy()
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), layout="constrained")
    for ax, c in zip(axes.flat, ("corrupt", "coherent", "sustained", "change"), strict=True):
        key = f"{c}__every4__"
        truth = (arrays["FILTER2"][key + "target"][:, 0] - mean) @ H
        ax.plot(truth[:, 0], truth[:, 1], color="black", label="True feature state", lw=2)
        for n in ("FILTER2", "PC16", "NISEMP", "ADAPT1"):
            pred = (arrays[n][key + "prediction"][:, 0] - mean) @ H
            ax.plot(pred[:, 0], pred[:, 1], color=COLORS[n], label=n, lw=1.3, alpha=0.85)
        ax.scatter(truth[24, 0], truth[24, 1], color="black", marker="*", s=70)
        ax.set(title=c, xlabel="Fitted feature coordinate 1", ylabel="Fitted feature coordinate 2")
        ax.grid(alpha=0.15)
    axes[0, 0].legend(fontsize=8)
    fig.suptitle(
        f"Pre-correction trajectories: root {root}, episode 0, every4\nPreselected example; fitted coordinate basis, not supplied simulator inverse",
        fontsize=12,
    )
    save(fig, "trajectories")
    fig, axes = plt.subplots(4, 2, figsize=(12, 10), layout="constrained")
    for j, c in enumerate(("corrupt", "change")):
        key = f"{c}__every4__"
        for n in ("FILTER2", "NISEMP", "ADAPT1"):
            a = arrays[n]
            color = COLORS[n]
            axes[0, j].plot(np.arange(1, 65), a[key + "prior"][:, 0], color=color, label=n)
            axes[0, j].plot(
                np.arange(65), a[key + "posterior"][:, 0], color=color, ls=":", alpha=0.7
            )
            axes[1, j].plot(
                np.arange(1, 65)[a[key + "sensed"][:, 0]],
                a[key + "nis"][:, 0][a[key + "sensed"][:, 0]],
                ".-",
                color=color,
            )
            axes[2, j].plot(
                np.arange(1, 65)[a[key + "sensed"][:, 0]],
                a[key + "weight"][:, 0][a[key + "sensed"][:, 0]],
                ".-",
                color=color,
            )
            axes[3, j].plot(np.arange(1, 65), a[key + "covtrace"][:, 0], color=color)
            axes[3, j].plot(
                np.arange(1, 65), a[key + "postcovtrace"][:, 0], color=color, ls=":", alpha=0.7
            )
        for ax in axes[:, j]:
            if c == "corrupt":
                ax.axvspan(24, 31, color="#ef4444", alpha=0.1)
            else:
                ax.axvline(24, color="#16a34a", alpha=0.4)
            ax.set(xlabel="Physical time", xlim=(0, 64))
            ax.grid(alpha=0.15)
        axes[0, j].set(
            title=c, ylabel="NMSE: prior solid / posterior dotted", yscale="symlog", ylim=(0, None)
        )
        axes[1, j].set(ylabel="Pre-gating NIS (log scale)", yscale="log")
        axes[2, j].set(ylabel="Precision weight / acceptance", ylim=(-0.03, 1.08))
        axes[3, j].set(ylabel="Covariance trace: prior / posterior", yscale="log")
    axes[0, 0].legend(fontsize=8)
    fig.suptitle(
        "Correction mechanism traces, same preselected episode\nADAPT1 uses current-observation plug-in R; its NIS is not nominal chi-square",
        fontsize=12,
    )
    save(fig, "correction-diagnostics")
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), layout="constrained")
    for ax, c in zip(axes, ("change", "coherent", "sustained"), strict=True):
        for n in ("FILTER2", "PC16", "R100", "NIS99", "NISEMP", "ADAPT1"):
            root_curves = []
            for r in receipt["confirmation_roots"]:
                a = np.load(OUT / "confirmation" / str(r) / n / "arrays.npz")
                root_curves.append(
                    np.mean(
                        [
                            a[f"{c}__{s}__prior"].mean(1)
                            for s in (SENSED if c == "change" else INTERMITTENT)
                        ],
                        axis=0,
                    )
                )
            ax.plot(
                np.arange(1, 65), np.mean(root_curves, axis=0), color=COLORS[n], label=n, lw=1.5
            )
        ax.axvline(24, color="black", alpha=0.25)
        ax.set(title=c, xlabel="Physical time", ylabel="Mean pre-correction NMSE", ylim=(0, None))
        ax.grid(alpha=0.15)
    axes[0].legend(fontsize=8)
    fig.suptitle(
        "Adaptation versus plausible sensor faults: all 10 confirmation roots", fontsize=12
    )
    save(fig, "adaptation")
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5), layout="constrained")
    for ax, n in zip(axes.flat, ("FILTER2", "NIS99", "NISEMP", "ADAPT1"), strict=True):
        for c, style in [("partial", "-"), ("noise", "--"), ("corrupt", ":")]:
            values = []
            accepted = []
            for r in receipt["confirmation_roots"]:
                a = np.load(OUT / "confirmation" / str(r) / n / "arrays.npz")
                k = f"{c}__every4__"
                active = a[k + "sensed"]
                values.extend(a[k + "nis"][active])
                accepted.extend(a[k + "nis"][active & (a[k + "weight"] > 0)])
            bins = np.logspace(-4, 5, 55)
            hist, _ = np.histogram(values, bins=bins)
            ax.plot(
                np.sqrt(bins[:-1] * bins[1:]),
                hist / len(values),
                ls=style,
                label=f"{c}: all ({len(values)})",
            )
            if c == "corrupt" and accepted:
                hist, _ = np.histogram(accepted, bins=bins)
                ax.plot(
                    np.sqrt(bins[:-1] * bins[1:]),
                    hist / len(accepted),
                    color="black",
                    alpha=0.5,
                    label="corrupt: accepted only",
                )
        ax.axvline(16.811894, color="gray", ls=":", alpha=0.5)
        ax.set(
            xscale="log", xlabel="NIS (log bins)", ylabel="Fraction of sensed events / bin", title=n
        )
        ax.legend(fontsize=7)
    fig.suptitle(
        "All pre-gating versus accepted innovation statistics\nGray reference is nominal χ²₆ 99%; data are correlated diagnostics, not independent replicates",
        fontsize=12,
    )
    save(fig, "innovations")
    fig, axes = plt.subplots(3, 1, figsize=(11, 7.5), layout="constrained")
    for ax, n in zip(axes, ("FILTER2", "CHANNEL2", "ADAPT1"), strict=True):
        a = arrays[n]
        k = "channels__every4__"
        contribution = np.linalg.norm(
            a[k + "diagnostic_gain"][:, 0] * a[k + "diagnostic_innovation"][:, 0, None, :], axis=1
        ).T
        im = ax.imshow(
            contribution,
            aspect="auto",
            origin="lower",
            extent=(1, 64, -0.5, 11.5),
            vmin=0,
            vmax=0.3,
            cmap="magma",
        )
        ax.set(title=n, ylabel="Observed channel", xlabel="Physical time")
        ax.axvspan(24, 31, facecolor="none", edgecolor="cyan", lw=1)
    fig.colorbar(
        im,
        ax=axes,
        label="Norm of channel term Kᵢ rᵢ (not independent causal contributions)",
        shrink=0.8,
    )
    fig.suptitle(
        "Partial-channel corruption: individual correction contributions\nPreselected root15307, episode0, every4; missing channels contribute zero",
        fontsize=12,
    )
    save(fig, "channel-contributions")


def tables(stats, res, conditions):
    lines = [
        "# Study B2 confirmation tables",
        "",
        "Ten independently fitted roots; ordinary95% paired-root bootstrap intervals. Frozen primary-family intervals are in `statistics.json`.",
        "",
        "| Model | Ordinary J | Balanced C | Original corruption | Genuine change | Free32 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for n in ("FILTER2", "STABLE", "PC16", "R100", "NIS99", "CHANNEL2", "NISEMP", "ADAPT1"):
        vals = [stats["descriptive"][n][k] for k in ("J", "C", "corrupt", "change", "free32")]
        lines.append(
            "| "
            + n
            + " | "
            + " | ".join(f"{v['mean']:.5f} [{v['lo']:.5f}, {v['hi']:.5f}]" for v in vals)
            + " |"
        )
    lines += [
        "",
        "## Expanded benchmark",
        "",
        "| Model | Isolated | Two channels | Coherent snapshot | Sustained coherent | Dynamics | Heavy tails | Biased/correlated | Gap |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for n in res:
        vals = [
            stats["descriptive"][n][k]
            for k in (
                "isolated",
                "channels",
                "coherent",
                "sustained",
                "dynamics",
                "heavy",
                "biased",
                "gap",
            )
        ]
        lines.append("| " + n + " | " + " | ".join(f"{v['mean']:.5f}" for v in vals) + " |")
    lines += [
        "",
        "## Real resources",
        "",
        "| Model | Fitted scalars | Allocated persistent bytes | State/cov bytes | Counted linear MAC/step | CPU μs/step batch1 | CPU μs/step batch20 | Base fit CPU s |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for n, r in res.items():
        lines.append(
            f"| {n} | {r['fitted_scalars']} | {r['persistent_allocated_bytes']} | {r['transient_state_and_covariance_bytes']} | {r['operations']['profiled_linear_macs_per_step']:.3f} | {r['latency']['1']['mean_us_per_step']:.2f} | {r['latency']['20']['mean_us_per_step']:.2f} | {r['mean_base_fit_cpu_seconds']:.3f} |"
        )
    lines += [
        "",
        "MACs exclude solves/nonlinear/elementwise work. Schedule every4, same minimal inference driver, initialization included. These are a different accounting surface from historical Study B’s average over54 cells. Robust linear arithmetic is float64; original/neural float32. Detailed solve dimensions/call counts, p95/max times, hyperparameters and exposure are in `resources.json`. Each robust corrector reuses the same FILTER2 fit.",
        "",
        "## Recovery and calibration",
        "",
        "Recovery is onset-relative post-correction recovery; eight PRE-onset errors set its threshold. Censoring and fault-end recovery are in condition-statistics. NIS is pre-gating; ADAPT1 uses data-dependent R.",
        "",
        "| Model | Change recovery steps | Change censoring | Clean rejection | High-noise rejection | Partial state95 coverage | High-noise state95 coverage |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for n, c in conditions.items():
        vals = [
            c["change"]["recovery"]["mean"],
            c["change"]["censored"]["mean"],
            c["clean"]["rejected"]["mean"],
            c["noise"]["rejected"]["mean"],
        ]
        rest = [
            c["partial"].get("coverage95", {}).get("mean"),
            c["noise"].get("coverage95", {}).get("mean"),
        ]
        lines.append(
            "| "
            + n
            + " | "
            + " | ".join(f"{v:.4f}" for v in vals)
            + " | "
            + " | ".join("not modeled" if v is None else f"{v:.4f}" for v in rest)
            + " |"
        )
    (DEST / "tables.md").write_text("\n".join(lines) + "\n")


def main():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    m = json.loads(MANIFEST.read_text())
    receipt = receipt_check()
    budget = Budget(OUT, m, "report")
    DEST.mkdir(exist_ok=True)
    try:
        source, conditions = cell_stats(receipt, m)
        res = resources(receipt, source)
        stats = json.loads((OUT / "report/statistics.json").read_text())
        for src, name in [
            ("report/statistics.json", "statistics.json"),
            ("report/root-results.json", "root-results.json"),
            ("report/independent-reduction.json", "independent-reduction.json"),
            ("repeat/reproduction.json", "reproduction.json"),
            ("freeze/confirmation-receipt.json", "confirmation-receipt.json"),
            ("audit/baseline-audit.json", "baseline-audit.json"),
            ("fixture/projection.json", "fixture-original-projection.json"),
            (
                "fixture-storage-correction/projection.json",
                "fixture-failed-storage-projection.json",
            ),
            ("fixture-storage-a1/projection.json", "fixture-a1-projection.json"),
            ("screen1/summary.json", "development-phase1.json"),
            ("screen2/summary.json", "development-phase2.json"),
            ("hybrid/summary.json", "development-hybrid.json"),
            ("screen1/nis-calibration.json", "nis-calibration.json"),
        ]:
            shutil.copyfile(OUT / src, DEST / name)
        tables(stats, res, conditions)
        plots(receipt, stats, res)
        budget.check(force=True)
        dump(
            DEST / "render-provenance.json",
            {
                "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "receipt": receipt["sha256"],
                "matplotlib": matplotlib.__version__,
                "new_fits": 0,
                "new_selection": False,
            },
        )
        budget.finish("complete")
    except BaseException as e:
        budget.finish("failed", repr(e))
        raise


if __name__ == "__main__":
    main()
