"""Summarize the fixed SOAM-001 grid without selecting seeds or changing thresholds."""

import argparse
import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def summarize(source, output):
    output.mkdir(parents=True, exist_ok=True)
    rows = json.loads((source / "results.json").read_text())
    cfg = json.loads((source / "config.json").read_text())
    provenance = json.loads((source / "provenance.json").read_text())
    expected = {(m, s) for m in cfg["models"] for s in cfg["seeds"]}
    assert {(r["model"], r["seed"]) for r in rows} == expected
    assert len(rows) == len(expected)
    for name in ("results.json", "config.json", "provenance.json", "trials.json", "status.json"):
        shutil.copyfile(source / name, output / name)
    readiness = [{"model": r["model"], "seed": r["seed"], **r["controls_readiness"]} for r in rows]
    (output / "readiness.json").write_text(json.dumps(readiness, indent=2) + "\n")
    lines = [
        "# Substrate controls: measured summary",
        "",
        f"Source commit: `{provenance['commit']}`. Source SHA-256: `{provenance['source_sha256']}`.",
        f"Completed {len(rows)}/{len(expected)} planned trials; seeds {cfg['seeds']}.",
        "Mean ± sample SD across seeds. NMSE is error divided by target feature energy.",
        "",
        "| Model | Width | Params | Difference | Grounded 48 | Steady 48 | Irregular 48 | Held-action 48 | Irregular 384 | Screen |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    def stats(values):
        return f"{np.mean(values):.4f} ± {np.std(values, ddof=1):.4f}"

    fig, axes = plt.subplots(2, 3, figsize=(16, 9), layout="constrained")
    resource = [
        "",
        "| Model | Weight bytes | Optimizer bytes | Stored eval tensor bytes | MACs/step | Train seconds |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for model in cfg["models"]:
        group = [r for r in rows if r["model"] == model]

        def values(h, condition, metric="nmse", sub="free", group=group):
            return [r["controls"]["test"][str(h)][condition][sub][metric] for r in group]

        r = group[0]
        columns = [
            model,
            str(r["hidden_dim"]),
            str(r["parameters"]),
            f"{100 * (r['parameters'] / 2892 - 1):+.2f}%",
            stats(values(48, "steady", sub="grounded")),
            stats(values(48, "steady")),
            stats(values(48, "irregular")),
            stats(values(48, "irregular_hold")),
            stats(values(384, "irregular")),
            f"{sum(x['controls_readiness']['passed'] for x in group)}/{len(group)}",
        ]
        lines.append("| " + " | ".join(columns) + " |")
        resource.append(
            f"| {model} | {r['parameter_bytes']} | {r['optimizer_tensor_bytes']} | "
            f"{r['stored_evaluation_tensor_bytes']} | "
            f"{r['linear_macs_per_recurrent_step_including_readout']} | "
            f"{np.mean([x['training_seconds'] for x in group]):.2f} |"
        )
        horizons = cfg["control_horizons"]
        axes[0, 0].plot(
            horizons, [np.mean(values(h, "irregular")) for h in horizons], "-o", label=model
        )
        axes[0, 1].plot(
            horizons, [np.mean(values(h, "irregular_hold")) for h in horizons], "-o", label=model
        )
        case = [x["controls"]["test"]["48"]["irregular"] for x in group]
        axes[0, 2].plot(
            range(8), np.mean([[v["nmse"] for v in x["switch_lags"]] for x in case], 0), label=model
        )
        axes[1, 0].plot(
            np.mean([x["perturbation"]["hidden_gap_ratio_by_step"] for x in case], 0), label=model
        )
        axes[1, 1].plot(
            np.mean([x["perturbation"]["feature_gap_nmse_by_step"] for x in case], 0), label=model
        )
        axes[1, 2].plot(
            horizons,
            [
                np.mean(
                    [
                        x["controls"]["test"][str(h)]["irregular"][
                            "predicted_to_true_motion_energy"
                        ]
                        for x in group
                    ]
                )
                for h in horizons
            ],
            "-o",
            label=model,
        )
        shutil.copyfile(
            source / f"{model}-seed11" / "diagnostics.png", output / f"{model}-seed11.png"
        )
    titles = [
        "Irregular switching: free error",
        "Irregular switching + held actions: free error",
        "48-step trial: error since most recent switch",
        "48-step trial: hidden perturbation gap",
        "48-step trial: paired feature perturbation gap",
        "Irregular switching: motion energy ratio",
    ]
    labels = [
        ("Rollout horizon", "NMSE"),
        ("Rollout horizon", "NMSE"),
        ("Transitions since switch", "NMSE"),
        ("Transitions after perturbation", "Hidden gap / injected RMS"),
        ("Transitions after perturbation", "Feature gap NMSE"),
        ("Rollout horizon", "Predicted / true"),
    ]
    for ax, title, (x, y) in zip(axes.flat, titles, labels):
        ax.set(title=title, xlabel=x, ylabel=y)
        ax.grid(alpha=0.2)
    axes[0, 0].legend(fontsize=8)
    fig.suptitle("SOAM-001: all three seeds; descriptive means, no significance claim")
    fig.savefig(output / "controls-summary.png", dpi=140)
    plt.close(fig)
    lines += resource
    lines += [
        "",
        "Linear MACs exclude backward/assimilation/nonlinearity/dispatch and switch handoffs.",
        "Per-condition switch counts and extra independent initializer MACs are in results.json.",
        "Tensor storage counts are not peak process memory.",
        "",
        "## Failed screen checks",
        "",
    ]
    for r in readiness:
        if not r["passed"]:
            lines.append(
                f"- {r['model']} seed {r['seed']}: "
                + ", ".join(k for k, v in r["checks"].items() if not v)
            )
    lines += ["", "![Extended controls](controls-summary.png)", ""]
    (output / "summary.md").write_text("\n".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    summarize(args.source, args.output)
