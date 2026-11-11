"""Readable mechanism contrasts and reset heatmaps from already-frozen results."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from soam.gating.runner import Budget, dump

ROOT = Path(__file__).resolve().parents[2]
out = ROOT / "runs/study-a-v2"
dest = ROOT / "reports/study-a"
m = json.loads((out / "manifest.json").read_text())
budget = Budget(out, m)
s = json.loads((out / "report/statistics.json").read_text())
receipt = json.loads((out / "freeze/receipt.json").read_text())
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), gridspec_kw={"width_ratios": [1, 1.3]})
for i, (name, label) in enumerate(
    [
        ("FU38", "Learned constant update (FU38)"),
        ("R52", "Parameter-matched tanh (R52)"),
        ("R55", "MAC-matched tanh (R55)"),
    ]
):
    v = s["contrasts"]["gain_" + name]["adjusted"]
    mean = 100 * v["mean"]
    axes[0].errorbar(
        mean,
        i,
        xerr=[[mean - 100 * v["lo"]], [100 * v["hi"] - mean]],
        fmt="o",
        capsize=4,
        color="#147d92",
    )
    axes[0].annotate(
        f"{mean:.2f}%",
        (mean, i),
        xytext=(0, 12),
        textcoords="offset points",
        ha="center",
        fontsize=9,
    )
axes[0].set_yticks(range(3), ["FU38 (primary)", "R52", "R55"])
axes[0].axvline(10, color="#be6b25", ls="--", label="10% practical margin")
axes[0].axvline(0, color="gray", lw=0.7)
axes[0].set_ylim(2.5, -0.5)
axes[0].set_xlabel("G32 improvement in joint error J (%)")
axes[0].set_title("Adjusted paired-root intervals")
axes[0].legend(loc="lower right", fontsize=8)
axes[0].grid(axis="x", alpha=0.2)
names = ["G32", "FU32", "FU38", "FR32", "FB32", "S32", "GS32", "R32", "R52", "R55"]
for i, n in enumerate(names):
    v = s["models"][n]["free32"]
    mse = s["models"][n]["J"]
    axes[1].scatter(mse["mean"], v["mean"], s=55)
    axes[1].annotate(
        n,
        (mse["mean"], v["mean"]),
        xytext=(4, 5 if i % 2 == 0 else -12),
        textcoords="offset points",
        fontsize=8,
    )
axes[1].set_xlabel("Joint reconstruction / free-8 error J")
axes[1].set_ylabel("Free-32 NMSE")
axes[1].set_title("Short- and long-horizon tradeoff (means)")
axes[1].grid(alpha=0.2)
fig.tight_layout()
fig.savefig(dest / "mechanism-comparison.png", dpi=180)
fig.savefig(dest / "mechanism-comparison.svg")
plt.close(fig)
fig, axes = plt.subplots(3, 2, figsize=(11, 7))
root = m["repeat_root"]
for row, name in enumerate(["G32", "FU38", "FR32"]):
    d = torch.load(
        out / "confirmation" / f"{root}-{name}-c{receipt['selected'][name]}" / "diagnostics.pt",
        weights_only=False,
    )
    for col, role in enumerate(["recall", "transition"]):
        im = axes[row, col].imshow(
            d[role]["path"]["reset"][:, 0].T, aspect="auto", vmin=0, vmax=1, origin="lower"
        )
        axes[row, col].set_title(f"{name}, {role}")
        axes[row, col].set_xlabel("step")
        axes[row, col].set_ylabel("unit")
        fig.colorbar(im, ax=axes[row, col], label="reset gate")
fig.suptitle("Preselected root 9301, episode 0", y=1.01)
fig.tight_layout()
fig.savefig(dest / "reset-trajectories.png", dpi=160, bbox_inches="tight")
fig.savefig(dest / "reset-trajectories.svg", bbox_inches="tight")
plt.close(fig)
summary = {}
for name in ["G32", "FU38", "FR32", "GS32"]:
    units = []
    for root in m["confirmation_roots"]:
        d = torch.load(
            out / "confirmation" / f"{root}-{name}-c{receipt['selected'][name]}" / "diagnostics.pt",
            weights_only=False,
        )
        units.append(d["recall"]["path"]["alpha"].mean((0, 1)).numpy())
    a = np.concatenate(units)
    half = np.log(0.5) / np.log(1 - a)
    summary[name] = {
        "unit_mean_update_rate_quantiles_10_50_90": np.quantile(a, [0.1, 0.5, 0.9]).tolist(),
        "gate_only_retention_half_life_quantiles": np.quantile(half, [0.1, 0.5, 0.9]).tolist(),
        "warning": "Gate-only half-life ignores the candidate-state feedback Jacobian; it is not an observed dynamical memory time constant.",
    }
dump(dest / "gate-timescale-description.json", summary)
budget.finish("supplemental-figures-and-gate-description", "complete")
