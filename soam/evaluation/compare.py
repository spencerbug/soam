"""Compare complete runs without averaging away config identity."""

import argparse
import json
import statistics
from pathlib import Path


def mean_sd(values):
    return (
        f"{statistics.mean(values):.4f} ± {statistics.stdev(values) if len(values) > 1 else 0:.4f}"
    )


def compare(paths, output):
    lines = [
        "# Substrate results",
        "",
        (
            "Mean ± sample standard deviation across seeds; "
            "a single seed has no estimated spread. NMSE is MSE divided by target feature energy."
        ),
        "",
    ]
    for path in map(Path, paths):
        status = json.loads((path / "status.json").read_text())
        if status["status"] != "complete":
            raise ValueError(f"Incomplete run: {path}")
        rows = json.loads((path / "results.json").read_text())
        provenance = json.loads((path / "provenance.json").read_text())
        lines += [
            f"## {path.name}",
            "",
            (
                f"Source commit: `{provenance['commit']}`. "
                f"Source SHA-256: `{provenance['source_sha256']}`."
            ),
            "",
            "| Model | Seeds | Parameters | Grounded NMSE | Free NMSE | Switching NMSE | Long NMSE | Perturbation final gap ratio | Train seconds |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for model in dict.fromkeys(row["model"] for row in rows):
            subset = [row for row in rows if row["model"] == model]
            values = [
                mean_sd([r[case]["free"]["nmse"] for r in subset])
                for case in ("steady", "switching")
            ]
            lines.append(
                f"| {model} | {len(subset)} | {subset[0]['parameters']} | "
                f"{mean_sd([r['steady']['grounded']['nmse'] for r in subset])} | "
                f"{' | '.join(values)} | "
                f"{mean_sd([r['long_horizon']['nmse'] for r in subset])} | "
                f"{mean_sd([r['steady']['perturbation']['final_hidden_gap_ratio'] for r in subset])} | "
                f"{mean_sd([r['training_seconds'] for r in subset])} |"
            )
        lines += [
            "",
            (
                "Perturbation gap is relative to an unperturbed model rollout, not a proof "
                "of return to the correct world trajectory. Separate cores share sensory "
                "initialization/readout and have their total parameter count matched to additive. "
                "Gated and low-rank variants retain additional parameters. See per-seed metrics "
                "for persistence references, invalid rates, prefix errors, and data exposure."
            ),
            "",
        ]
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    compare(args.runs, args.output)


if __name__ == "__main__":
    main()
