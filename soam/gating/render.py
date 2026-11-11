"""Standalone report tables and scientific figures for the frozen Study A inventory."""

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch


def render(output, stats, records, m, receipt):
    dest = output / "report"
    ids = list(m["variants"])
    colors = plt.cm.tab20(np.linspace(0, 1, len(ids)))

    def save(fig, name):
        fig.tight_layout()
        fig.savefig(dest / f"{name}.png", dpi=160)
        fig.savefig(dest / f"{name}.svg")
        plt.close(fig)

    def cell(v):
        return f"{v['mean']:.5f} [{v['lo']:.5f}, {v['hi']:.5f}]"

    lines = [
        "# Study A numerical tables",
        "",
        "Ordinary 95% paired-root percentile intervals; independent roots are the units. Adjusted decision contrasts follow below.",
        "",
        "| Model | Parameters | Active hidden | MACs per advance/readout | J | Recall-10 | Free-8 | Free-32 | Grounded-32 |",
        "| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for name in ids:
        c = stats["resources"][name]
        lines.append(
            f"| {name} | {c['parameters']} | {c['active_hidden']} | {c['advance_readout_linear_macs']} | "
            + " | ".join(
                cell(stats["models"][name][k])
                for k in ("J", "recall", "free8", "free32", "grounded32")
            )
            + " |"
        )
    lines += [
        "",
        "## Decision contrasts",
        "",
        "Positive gain favors G32. Positive endpoint differences indicate worse G32 error. Intervals adjusted across the 15 prespecified contrasts.",
        "",
        "| Contrast | Mean [adjusted interval] | Ordinary 95% interval |",
        "| --- | --- | --- |",
    ]
    for name, v in stats["contrasts"].items():
        lines.append(f"| {name} | {cell(v['adjusted'])} | {cell(v['ordinary'])} |")
    lines += [
        "",
        "## Diagnostics",
        "",
        "Descriptive root intervals; no extra confirmatory tests are claimed.",
        "",
        "| Model | Free-128 | Recall linear R² | Transition linear R² | Transition nonlinear R² | Recall useful recovery | Movement useful recovery |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for name in ids:
        lines.append(
            f"| {name} | "
            + " | ".join(
                cell(stats["diagnostics"][name][k])
                for k in (
                    "free128",
                    "recall_linear_r2",
                    "transition_linear_r2",
                    "transition_nonlinear_r2",
                    "recall_useful_recovery_fraction",
                    "transition_useful_recovery_fraction",
                )
            )
            + " |"
        )
    (dest / "tables.md").write_text("\n".join(lines) + "\n")
    lines = [
        "# Root-level Study A results",
        "",
        "| Root | Model | Config | Recall-10 | Free-8 | Free-32 | Grounded-32 | J | Free-128 diagnostic | Fit CPU seconds |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    compact = []
    for r in records:
        lines.append(
            f"| {r['root']} | {r['model']} | {r['config']} | "
            + " | ".join(
                f"{r['metrics'][k]:.8f}" for k in ("recall", "free8", "free32", "grounded32", "J")
            )
            + f" | {r['diagnostics']['free128']:.8f} | {r['fit_cpu']:.4f} |"
        )
        compact.append({k: v for k, v in r.items() if k not in ("trace", "learning")})
    (dest / "root-results.md").write_text("\n".join(lines) + "\n")
    (dest / "root-results.json").write_text(json.dumps(compact, indent=2) + "\n")
    fig, axes = plt.subplots(1, 4, figsize=(15, 5), sharey=True)
    for ax, key in zip(axes, ("recall", "free8", "free32", "grounded32")):
        vals = [stats["models"][n][key] for n in ids]
        mean = np.array([v["mean"] for v in vals])
        lo = np.array([v["lo"] for v in vals])
        hi = np.array([v["hi"] for v in vals])
        ax.errorbar(mean, np.arange(len(ids)), xerr=[mean - lo, hi - mean], fmt="o", capsize=2)
        ax.set_title(key)
        ax.set_xlabel("NMSE, 95% root CI")
        ax.grid(alpha=0.2)
    axes[0].set_yticks(np.arange(len(ids)), ids)
    axes[0].invert_yaxis()
    save(fig, "endpoint-comparisons")
    dev = json.loads((output / "development/results.json").read_text())
    fig, axes = plt.subplots(3, 4, figsize=(14, 9))
    for name, ax in zip(ids, axes.flat):
        for r in dev:
            if r["model"] != name:
                continue
            points = sorted(int(x) for x in r["learning"])
            ax.plot(
                points,
                [r["learning"][str(x)]["J"] for x in points],
                marker=".",
                alpha=0.7,
                label=f"{r['root']}, c{r['config']}",
            )
        ax.set_title(name)
        ax.set_yscale("log")
        ax.set_xlabel("training updates")
        ax.set_ylabel("development J")
        ax.grid(alpha=0.2)
    axes.flat[0].legend(fontsize=6)
    save(fig, "development-curves")
    root = m["repeat_root"]
    loaded = {}
    for name in ids:
        folder = output / "confirmation" / f"{root}-{name}-c{receipt['selected'][name]}"
        loaded[name] = torch.load(folder / "diagnostics.pt", weights_only=False)
    fig, axes = plt.subplots(4, 2, figsize=(13, 10))
    for row, name in enumerate(("G32", "FU38", "FR32", "GS32")):
        for col, role in enumerate(("recall", "transition")):
            gate = loaded[name][role]["path"]["alpha"][:, 0].T
            im = axes[row, col].imshow(gate, aspect="auto", vmin=0, vmax=1, origin="lower")
            axes[row, col].set_title(f"{name}: {role}, episode 0")
            axes[row, col].set_ylabel("hidden unit")
            axes[row, col].set_xlabel("step")
            fig.colorbar(im, ax=axes[row, col], label="update rate 1 − retention")
    save(fig, "gate-trajectories")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for name in ("G32", "FU38", "FR32", "R52", "S32", "GS32", "L12", "L2"):
        for ax, role in zip(axes, ("recall", "transition")):
            ratio = loaded[name][role]["perturb_gap_ratio"].mean(1)
            ax.plot(ratio, label=name)
            ax.set_title(role)
            ax.set_xlabel("steps after perturbation")
            ax.set_ylabel("hidden RMS gap / injected RMS")
            ax.set_yscale("log")
            ax.grid(alpha=0.2)
    axes[0].legend(ncol=2, fontsize=8)
    save(fig, "perturbation-recovery")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    for name in ("G32", "FU38", "FR32", "R52", "S32", "GS32", "L12", "L2"):
        for ax, key, title in zip(
            axes,
            ("nmse_curve", "radial_error_curve", "phase_error_curve"),
            ("Free rollout error", "Radial error", "Wrapped phase error"),
        ):
            ax.plot(np.arange(1, 129), loaded[name]["transition"][key], label=name)
            ax.set_title(title)
            ax.set_xlabel("horizon")
            ax.grid(alpha=0.2)
    axes[0].set_ylabel("NMSE")
    axes[1].set_ylabel("coordinate units")
    axes[2].set_ylabel("radians")
    axes[0].legend(fontsize=8, ncol=2)
    save(fig, "long-horizon")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for name, color in zip(ids, colors):
        d = stats["diagnostics"][name]
        axes[0].scatter(
            d["transition_linear_r2"]["mean"],
            d["transition_nonlinear_r2"]["mean"],
            label=name,
            color=color,
        )
        axes[1].scatter(
            d["transition_effective_rank"]["mean"],
            d["transition_distance_correlation"]["mean"],
            label=name,
            color=color,
        )
    axes[0].plot([-1, 1], [-1, 1], ":", color="gray")
    axes[0].set_xlabel("linear probe R²")
    axes[0].set_ylabel("nonlinear probe R²")
    axes[1].set_xlabel("hidden effective rank")
    axes[1].set_ylabel("hidden/position distance correlation")
    axes[1].legend(fontsize=7, ncol=2)
    save(fig, "state-geometry")
    from soam.encoders.projection import FixedProjection

    projection = FixedProjection(12, 1729).matrix.double()
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    for name, ax in zip(("G32", "FU38", "FR32", "R52", "S32", "GS32", "L12", "L2"), axes.flat):
        d = loaded[name]["transition"]
        truth = d["world"][:, 0]
        decoded = d["path"]["output"][:, 0].double() @ projection
        ax.plot(truth[:, 0], truth[:, 1], label="truth", color="black")
        ax.plot(decoded[:, 0], decoded[:, 1], label="predicted")
        ax.set_title(name)
        ax.set_aspect("equal")
        ax.grid(alpha=0.2)
    axes.flat[0].legend(fontsize=8)
    save(fig, "decoded-trajectories")
