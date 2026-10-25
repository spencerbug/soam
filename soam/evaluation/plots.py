"""Standalone diagnostic figures, with a noninteractive backend."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def plot_run(path, history, steady, switching, metrics, projection):
    fig, axes = plt.subplots(2, 3, figsize=(15, 8.5))
    # Fixed margins avoid data-dependent equal-aspect layout clipping text.
    fig.subplots_adjust(left=0.07, right=0.98, bottom=0.09, top=0.90, wspace=0.30, hspace=0.40)
    steps = [row["step"] for row in history]
    axes[0, 0].plot(steps, [row["loss"] for row in history], color="#2463a6")
    axes[0, 0].set(title="Training objective", xlabel="Optimizer step", ylabel="Loss", yscale="log")
    for label, case in (("Steady", metrics["steady"]), ("Switching", metrics["switching"])):
        axes[0, 1].plot(
            np.arange(1, len(case["free"]["prefix_nmse"]) + 1),
            case["free"]["prefix_nmse"],
            label=label,
        )
    axes[0, 1].set(
        title="Free rollout error", xlabel="Prediction horizon", ylabel="Energy-normalized MSE"
    )
    axes[0, 1].legend()
    for i in range(min(3, len(steady["truth"]))):
        truth = steady["truth"][i].numpy()
        pred = projection.diagnostic_inverse(steady["predicted"][i]).numpy()
        (line,) = axes[0, 2].plot(truth[:, 0], truth[:, 1], label=f"Context {i} truth")
        axes[0, 2].plot(pred[:, 0], pred[:, 1], "--", color=line.get_color())
    axes[0, 2].set(
        title="Steady trajectories (dashed: prediction)", xlabel="x", ylabel="y", aspect="equal"
    )
    axes[0, 2].legend(fontsize=7)
    truth = switching["truth"][0].numpy()
    pred = projection.diagnostic_inverse(switching["predicted"][0]).numpy()
    axes[1, 0].plot(truth[:, 0], label="Observed x")
    axes[1, 0].plot(np.arange(1, len(pred) + 1), pred[:, 0], "--", label="Predicted x")
    contexts = switching["contexts"][0].numpy()
    for t in np.flatnonzero(contexts[1:] != contexts[:-1]) + 1:
        axes[1, 0].axvline(t, color="gray", alpha=0.35)
    axes[1, 0].set(
        title=(
            "Switches; predicted-feature handoff"
            if metrics["model"] == "independent"
            else "Context switches; activity is carried"
        ),
        xlabel="Time",
        ylabel="Diagnostic x",
    )
    axes[1, 0].legend(fontsize=8)
    for label, case in (("Steady", metrics["steady"]), ("Switching", metrics["switching"])):
        axes[1, 1].plot(case["perturbation"]["hidden_gap_ratio_by_step"], label=label)
    axes[1, 1].axhline(0.5, color="gray", linestyle=":")
    axes[1, 1].set(
        title="Perturbation response",
        xlabel="Steps after perturbation",
        ylabel="Hidden gap / injected RMS",
    )
    axes[1, 1].legend()
    axes[1, 2].plot(steps, [row["update_norm"] for row in history], color="#9750a5")
    axes[1, 2].set(
        title="Ordinary optimizer updates", xlabel="Optimizer step", ylabel="Parameter delta norm"
    )
    for ax in axes.flat:
        ax.grid(alpha=0.15)
    fig.suptitle(path.parent.name + " · recurrent baseline diagnostics", fontsize=14)
    fig.savefig(path, dpi=140, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
