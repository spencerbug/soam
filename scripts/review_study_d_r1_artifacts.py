"""Final reporting-only plot QA and post hoc algebraic audit of saved checkpoints."""

import hashlib
from pathlib import Path

import matplotlib
import numpy as np
import torch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from soam.retrieval.runner import MANIFEST, OUT, REPORT, ROOT, Budget, read
from soam.temporal.runner import dump, size


def main():
    dest = OUT / "artifact-review"
    dest.mkdir(parents=True, exist_ok=False)
    m = read(MANIFEST)
    budget = Budget("report-artifact-review", m["limits"])
    status, error = "running", None
    torch.set_num_threads(1)
    rows = []
    try:
        diag = read(REPORT / "diagnostics.json")["roots"]
        times = np.mean([r["cycle_batch_ms"] for r in diag], 0)
        accuracy = np.mean([r["cycle_accuracy"] for r in diag], 0)
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        ix = [0, 1, 3, 31]
        ax.plot(times[ix], accuracy[ix], "-o", color="#295b93")
        for index, label, offset in [
            (0, "1", (5, 7)),
            (1, "2", (5, 7)),
            (3, "4", (-15, -18)),
            (31, "8–32", (-40, 10)),
        ]:
            ax.annotate(
                label,
                (times[index], accuracy[index]),
                xytext=offset,
                textcoords="offset points",
                fontsize=9,
            )
        ax.margins(x=0.12, y=0.2)
        ax.set(
            xlabel="Mean elapsed ms per batch of eight queries",
            ylabel="Earlier-object partial-cue raw accuracy",
            title="PH768: useful recall versus settling cost",
        )
        ax.grid(alpha=0.2)
        fig.tight_layout()
        fig.savefig(REPORT / "settling-cost.png", dpi=170)
        plt.close(fig)
        fig, ax = plt.subplots(figsize=(9, 4.5))
        for name in m["arms"]:
            group = "PH-FULL" if name == "PH-1" else name
            curves = []
            for root in m["confirmation_roots"]:
                with np.load(OUT / "confirmation" / str(root) / group / f"{name}.npz") as a:
                    curves.append((a["d2_error"][1, :, 7, :, :, 0] <= 0.1).mean((0, 2))[::-1])
            ax.plot(range(8), np.mean(curves, 0), marker="o", label=name)
        ax.set(
            xlabel="Later objects acquired since this object",
            ylabel="Final raw partial-cue accuracy",
            ylim=(-0.03, 1.03),
        )
        ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1))
        fig.tight_layout()
        fig.savefig(REPORT / "retention.png", dpi=170)
        plt.close(fig)
        # All available final confirmation PH checkpoints: each is the fourth sequence,
        # chosen by the runner's fixed archive layout, not by recall performance.
        for root in m["confirmation_roots"]:
            path = OUT / "confirmation" / str(root)
            memory = torch.load(path / "PH-FULL/last-memory.pt", weights_only=True)
            core = torch.load(path / "fit/core.pt", weights_only=True)
            p = memory["projector"]
            residuals = []
            with np.load(path / "PH-FULL/inputs.npz") as inputs:
                for obj in range(8):
                    for snapshot in range(8):
                        r = inputs[f"{('d2', 3, obj)}/record{snapshot}"]
                        key = torch.as_tensor(r[:16])
                        y = torch.as_tensor(r[16:24])
                        q = float(r[24])
                        value = (y @ core["a"].T) * np.cos(-q) + (y @ core["b"].T) * np.sin(-q)

                        def code(x, b):
                            threshold = (torch.arange(32, dtype=torch.float64) + 0.5) * (
                                2 * b / 32
                            ) - b
                            return (
                                torch.where(x[:, None] >= threshold, 1.0, -1.0)
                                .to(torch.float64)
                                .flatten()
                            )

                        encoded = torch.cat((code(key, 4.0), code(value, 1.5)))
                        residuals.append(float((p @ encoded - encoded).abs().max()))
            rows.append(
                {
                    "root": root,
                    "sequence": 3,
                    "observed_codes": 64,
                    "max_observed_code_span_residual": max(residuals),
                    "max_projector_idempotence_residual": float((p @ p - p).abs().max()),
                    "max_symmetry_residual": float((p - p.T).abs().max()),
                    "rank": int(memory["rank"]),
                }
            )
            budget.check()
        script = Path(__file__).resolve()
        dump(
            REPORT / "checkpoint-audit.json",
            {
                "classification": "post hoc algebraic diagnostic; not a new confirmatory endpoint",
                "scope": "all ten available final confirmation checkpoints, fourth sequence only",
                "rows": rows,
                "source_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
                "new_observations": 0,
                "new_fits": 0,
                "new_writes": 0,
                "new_retrieval_trials": 0,
            },
        )
        status = "complete"
    except BaseException as exc:
        status, error = "failed", repr(exc)
        raise
    finally:
        dump(dest / "phase-status.json", {"status": status, "error": error})
        budget.finish(status, error)
        dump(
            REPORT / "resource-final.json",
            {
                "ledger": budget.rows,
                "cpu_seconds": sum(r["cpu_seconds"] for r in budget.rows),
                "wall_seconds": sum(r["wall_seconds"] for r in budget.rows),
                "peak_rss_bytes": max(r["peak_rss_bytes"] for r in budget.rows),
                "artifact_bytes_before_receipt": size(OUT)
                + size(REPORT)
                + sum(p.stat().st_size for p in (ROOT / "reports").glob("STUDY_D_R1*.md")),
            },
        )
        dump(
            REPORT / "phase-status.json",
            {
                p.name: read(p / "phase-status.json")
                for p in OUT.iterdir()
                if p.is_dir() and (p / "phase-status.json").exists()
            },
        )


if __name__ == "__main__":
    main()
