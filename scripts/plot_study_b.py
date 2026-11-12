"""Readable final plots from saved statistics only; no models or new trials."""

import hashlib
import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main():
    start = time.process_time()
    wall = time.monotonic()
    root = Path(__file__).resolve().parents[1]
    dest = root / "reports/study-b"
    stats = json.loads((dest / "statistics.json").read_text())
    res = json.loads((dest / "resources.json").read_text())
    colors = {n: plt.cm.tab20(i) for i, n in enumerate(stats)}
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), layout="constrained")
    for name, s in stats.items():
        j = s["J"]
        err = np.array([[j["mean"] - j["lo"]], [j["hi"] - j["mean"]]])
        for ax, x in [(axes[0], s["macs"]["mean"]), (axes[1], res[name]["mean_fit_cpu"])]:
            ax.errorbar(
                x,
                j["mean"],
                yerr=err,
                fmt="o",
                color=colors[name],
                capsize=2,
                markersize=5,
                label=name,
                alpha=0.85,
            )
    for ax in axes:
        ax.set_xscale("log")
        ax.set_ylabel("Pre-correction NMSE J")
        ax.grid(alpha=0.15)
    axes[0].set_xlabel("Linear MAC / physical step (solves excluded)")
    axes[1].set_xlabel("Mean fit CPU seconds / root")
    axes[1].legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8, frameon=False)
    fig.suptitle("Study B v1: accuracy and resources — ordinary 95% root intervals")
    fig.savefig(dest / "resource-frontier.png", dpi=180)
    plt.close(fig)
    settle = json.loads((dest / "settling-statistics.json").read_text())
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), layout="constrained")
    for name in ("MIXC32", "REP32", "SET32"):
        x = np.array([0, 1, 2, 4])
        ys = [settle[name][f"fixed{k}"]["J"] for k in x]
        y = [s["mean"] for s in ys]
        axes[0].plot(x, y, "o-", label=name)
        axes[0].fill_between(x, [s["lo"] for s in ys], [s["hi"] for s in ys], alpha=0.12)
    axes[0].set_xlabel("Zero-time updates per sensed event")
    axes[0].set_ylabel("Pre-correction NMSE J")
    axes[0].legend(frameon=False)
    markers = ["o", "s", "^", "D", "v", "X", "P"]
    for i, mode in enumerate(
        ["fixed0", "fixed1", "fixed2", "fixed4", "event", "learned", "periodic"]
    ):
        s = settle["SET32"][mode]
        j = s["J"]
        axes[1].errorbar(
            s["macs"]["mean"],
            j["mean"],
            yerr=[[j["mean"] - j["lo"]], [j["hi"] - j["mean"]]],
            fmt=markers[i],
            capsize=2,
            label=mode,
            markersize=6,
        )
    axes[1].set_xlabel("SET32 linear MAC / physical step")
    axes[1].set_ylabel("Pre-correction NMSE J")
    axes[1].legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=8)
    for ax in axes:
        ax.grid(alpha=0.15)
    fig.suptitle("Fixed update budgets and SET32 scheduling — descriptive 95% root intervals")
    fig.savefig(dest / "settling-frontier.png", dpi=180)
    plt.close(fig)
    other = root / "reports/study-b-magnitude"
    if (other / "statistics.json").exists():
        ss = json.loads((other / "statistics.json").read_text())
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), layout="constrained")
        for i, (name, s) in enumerate(ss.items()):
            color = plt.cm.tab10(i)
            j = s["J"]
            axes[0].errorbar(
                s["macs"]["mean"],
                j["mean"],
                yerr=[[j["mean"] - j["lo"]], [j["hi"] - j["mean"]]],
                fmt="o",
                capsize=2,
                color=color,
                label=name,
            )
            axes[1].scatter(s["corrupt"]["mean"], s["change"]["mean"], color=color, label=name)
        axes[0].set_xscale("log")
        axes[0].set_xlabel("Linear MAC / physical step")
        axes[0].set_ylabel("Pre-correction NMSE J")
        axes[1].set_xlabel("Corrupted-snapshot NMSE")
        axes[1].set_ylabel("Genuine-change NMSE")
        axes[1].legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False)
        for ax in axes:
            ax.grid(alpha=0.15)
        fig.suptitle("Magnitude supplement: fresh roots, no pooling with v1")
        fig.savefig(other / "tradeoffs.png", dpi=180)
        plt.close(fig)
    report = {
        "cpu_seconds": time.process_time() - start,
        "wall_seconds": time.monotonic() - wall,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "note": "Replaces overlapping labels in presentation plots only; all plotted statistics unchanged.",
    }
    (dest / "plot-verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
