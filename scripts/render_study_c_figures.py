"""Presentation-only repair: legible cost legend and common trajectory axis."""

import hashlib
import json
import shutil
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from soam.ambiguity.runner import MANIFEST, OUT, REPORT, receipt_check
from soam.encoders.projection import FixedProjection
from soam.temporal.runner import Budget, dump


def main():
    receipt = receipt_check()
    selection = receipt["selection"]
    m = json.loads(MANIFEST.read_text())
    dest = OUT / "render-repair"
    dest.mkdir(exist_ok=False)
    budget = Budget(OUT, m["limits"], "render-repair")
    try:
        for stem in ("accuracy-cost", "candidate-trajectories"):
            for ext in ("png", "svg"):
                shutil.copyfile(REPORT / f"{stem}.{ext}", dest / f"original-{stem}.{ext}")
        stats = json.loads((REPORT / "statistics.json").read_text())
        runtime = json.loads((REPORT / "runtime.json").read_text())
        fig, ax = plt.subplots(figsize=(9, 5), constrained_layout=True)
        for name in selection["inventory"]:
            x = np.mean(
                [r[name]["timing"]["1"]["p95_us_per_episode_step"] for r in runtime.values()]
            )
            v = stats["descriptive"][name]["brier"]
            ax.errorbar(
                x,
                v["mean"],
                yerr=[[v["mean"] - v["lo"]], [v["hi"] - v["mean"]]],
                fmt="o",
                capsize=3,
                label=name,
            )
        ax.set(
            xlabel="Mean root p95 serial inference μs / step",
            ylabel="Brier score (95% root interval)",
            title="Probability quality and measured inference cost",
            xscale="log",
        )
        ax.legend(loc="upper right", ncol=2, fontsize=9)
        for ext in ("png", "svg"):
            fig.savefig(REPORT / f"accuracy-cost.{ext}", dpi=160)
        plt.close(fig)
        p = FixedProjection(12, 1729).matrix.numpy()
        root = m["confirmation_roots"][0]
        fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True, constrained_layout=True)
        for ax, name in zip(axes, (selection["r2"], "TWO16", "ADAPT1-M"), strict=True):
            with np.load(OUT / "confirmation" / str(root) / name / "delayed.npz") as a:
                j = a["pairs"][0, 1]
                candidates = a["candidate_prior"][:, j] @ p
                ax.plot(np.arange(1, 49), candidates[:, 0, 0], label="- candidate", color="#b47723")
                ax.plot(np.arange(1, 49), candidates[:, 1, 0], label="+ candidate", color="#227f89")
                ax.plot(
                    np.arange(1, 49), (a["target"][:, j] @ p)[:, 0], "k--", label="Actual state"
                )
            ax.axvspan(12, 28, alpha=0.1, color="gray")
            ax.set(title=name, xlabel="Physical step")
        axes[0].set_ylabel("Decoded x1 (evaluator only)")
        axes[0].legend(fontsize=8)
        fig.suptitle("Candidate-conditioned prior trajectories through an occlusion")
        for ext in ("png", "svg"):
            fig.savefig(REPORT / f"candidate-trajectories.{ext}", dpi=160)
        plt.close(fig)
        script = Path(__file__).resolve()
        dump(
            dest / "provenance.json",
            {
                "script": str(script),
                "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
                "scope": "Layout only; primary statistics and model arrays unchanged; original plots retained in this directory",
            },
        )
        budget.check(force=True)
        budget.finish("complete")
    except Exception as error:
        budget.finish("failed", repr(error))
        raise


if __name__ == "__main__":
    main()
