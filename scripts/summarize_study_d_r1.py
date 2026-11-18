"""Reporting-only audit of frozen D-R1 artifacts. No model execution or new data."""

import hashlib
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from soam.retrieval.runner import MANIFEST, OUT, REPORT, ROOT, Budget, read
from soam.temporal.runner import dump, size
from soam.temporal.statistics import interval


def main():
    dest = OUT / "supplement"
    dest.mkdir(parents=True, exist_ok=False)
    m = read(MANIFEST)
    budget = Budget("report-supplement", m["limits"])
    status, error = "running", None
    dump(dest / "phase-status.json", {"status": status})
    try:
        assert read(OUT / "report/phase-status.json")["status"] == "complete"
        rows = read(REPORT / "root-results.json")
        checks = {
            "input_parity_groups": 0,
            "paired_cue_masks": 0,
            "model_evaluations": 0,
            "writer_trials": 0,
            "fits": len(list(OUT.glob("**/fit-status.json"))),
        }
        for phase in ("fixture", "development", "calibration", "confirmation", "repeat"):
            grouped = {}
            for path in (OUT / phase).glob("**/result.json"):
                r = read(path)
                hashes = {x["input_hash"] for x in r["results"].values()}
                assert len(hashes) == 1
                grouped.setdefault(r["root"], set()).update(hashes)
                checks["model_evaluations"] += len(r["results"])
                checks["writer_trials"] += 1
            assert all(len(v) == 1 for v in grouped.values())
            checks["input_parity_groups"] += len(grouped)
        # Check actual saved full/partial evidence once per independent confirmation root.
        for root in m["confirmation_roots"]:
            with np.load(OUT / "confirmation" / str(root) / "KV/inputs.npz") as inp:
                for key in inp.files:
                    if not key.endswith("/partial/cue"):
                        continue
                    prefix = key[: -len("/partial/cue")]
                    mask = inp[prefix + "/partial/mask"]
                    assert np.array_equal(inp[key][mask], inp[prefix + "/full/cue"][mask])
                    assert (mask.sum(1) == 8).all()
                    checks["paired_cue_masks"] += len(mask)
            budget.check()
        assert (
            checks["fits"] == 16
            and checks["writer_trials"] == 114
            and checks["model_evaluations"] == 130
        )
        diagnostic = []
        for root in m["confirmation_roots"]:
            den = next(r["normalization"] for r in rows["PH-FULL"] if r["root"] == root)
            with np.load(OUT / "confirmation" / str(root) / "PH-FULL/PH-FULL.npz") as a:
                ids = a["trace_ids"]
                final = (ids[:, 0] == 1) & (ids[:, 3] == 7)
                ids_final = ids[final]
                partial_old = (ids_final[:, 1] == 1) & (ids_final[:, 4] < 7)
                truth = a["trace_truth"][final][partial_old]
                pred = a["trace_values"][final][partial_old]
                errors = ((pred - truth[:, None]) ** 2).mean(-1) / den
                pert = a["trace_perturb_values"][partial_old]
                pert_error = ((pert - truth) ** 2).mean(-1) / den
                row = {
                    "root": root,
                    "cycle_accuracy": (errors <= 0.1).mean((0, 2)).tolist(),
                    "cycle_batch_ms": (
                        a["trace_elapsed"][final][partial_old].mean(0) * 1000
                    ).tolist(),
                    "mean_cycles": float(a["trace_cycles"][final][partial_old].mean()),
                    "nonconvergence_fraction": float(
                        (~a["trace_converged"][final][partial_old]).mean()
                    ),
                    "perturbed_accuracy": float((pert_error <= 0.1).mean()),
                    "unperturbed_accuracy": float((errors[:, -1] <= 0.1).mean()),
                    "perturbed_canonical_nmse": float(pert_error.mean()),
                    "perturbation_excess_nmse": float((pert_error - errors[:, -1]).mean()),
                    "perturbation_accuracy_difference": float(
                        ((pert_error <= 0.1).astype(float) - (errors[:, -1] <= 0.1)).mean()
                    ),
                    "perturbed_nonconvergence_fraction": float(
                        (~a["trace_perturb_converged"][partial_old]).mean()
                    ),
                    "mean_perturbed_bits": float(a["trace_perturb_counts"][partial_old].mean()),
                    "maximum_write_rank": int(a["write_ranks"].max()),
                }
                diagnostic.append(row)
            budget.check()
        diagnostic_intervals = {
            k: interval([r[k] for r in diagnostic], seed=43013)
            for k in (
                "mean_cycles",
                "nonconvergence_fraction",
                "perturbed_accuracy",
                "unperturbed_accuracy",
                "perturbation_excess_nmse",
                "perturbation_accuracy_difference",
                "perturbed_nonconvergence_fraction",
            )
        }
        full_partial = {
            n: interval(
                [
                    r["metrics"]["full"]["old_accuracy"] - r["metrics"]["partial"]["old_accuracy"]
                    for r in rr
                ],
                seed=43013,
            )
            for n, rr in rows.items()
        }
        comparison = {}
        for n, rr in rows.items():
            comparison[n] = {
                key: interval([r["metrics"]["partial"][key] for r in rr], seed=43013)
                for key in (
                    "J",
                    "one_shot",
                    "old_error",
                    "known_coverage",
                    "accepted_wrong",
                    "unknown_acceptance",
                )
            }
            comparison[n]["resources"] = rr[0]["resources"]
            comparison[n]["write_us"] = interval([r["write_us_mean"] for r in rr], seed=43013)
            comparison[n]["serial_recall_us"] = interval(
                [r["serial_recall_us_mean"] for r in rr], seed=43013
            )
            comparison[n]["grounded_one_step_nmse"] = interval(
                [r["grounded_one_step_nmse"] for r in rr], seed=43013
            )
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        indices = np.array([0, 1, 3, 7, 15, 31])
        times = np.array([r["cycle_batch_ms"] for r in diagnostic]).mean(0)
        accuracy = np.array([r["cycle_accuracy"] for r in diagnostic]).mean(0)
        ax.plot(times[indices], accuracy[indices], "-o", color="#295b93")
        for i in indices:
            ax.annotate(
                str(i + 1),
                (times[i], accuracy[i]),
                xytext=(4, 5),
                textcoords="offset points",
                fontsize=8,
            )
        ax.set(
            xlabel="Mean elapsed ms per batch of eight queries",
            ylabel="Earlier-object partial-cue raw accuracy",
            title="PH768: useful recall versus settling cost",
        )
        ax.grid(alpha=0.2)
        fig.tight_layout()
        fig.savefig(REPORT / "settling-cost.png", dpi=170)
        plt.close(fig)
        dump(
            REPORT / "diagnostics.json",
            {
                "roots": diagnostic,
                "ordinary_95_root_intervals": diagnostic_intervals,
                "full_minus_partial_old_accuracy": full_partial,
                "comparisons": comparison,
            },
        )
        dump(REPORT / "execution-audit.json", checks)
        script = Path(__file__).resolve()
        dump(
            REPORT / "supplement-source.json",
            {
                "path": str(script.relative_to(ROOT)),
                "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
                "frozen_scientific_source": read(OUT / "freeze/receipt.json")["source"][
                    "aggregate"
                ],
                "role": "reporting only; no fits, observations or settings changed",
            },
        )
        lines = [
            "",
            "## Additional diagnostics and audit",
            "",
            "All 16 fits, 114 writer evaluations and 130 arm outputs completed. All 16",
            "phase/root input-parity groups match; saved full/partial masks are checked",
            "coordinate-for-coordinate. Calibration used the full evaluation path, including",
            "isolated-object diagnostics; only final D2 known scores set thresholds. Those",
            "extra isolated records were reset before D2 and never entered core fitting.",
            "",
            "| Arm | Known coverage | Accepted-wrong / all known | Unknown acceptance |",
            "| --- | ---: | ---: | ---: |",
        ]
        for n, rr in rows.items():
            x = comparison[n]
            lines.append(
                f"| {n} | {x['known_coverage']['mean']:.4f} | {x['accepted_wrong']['mean']:.4f} | {x['unknown_acceptance']['mean']:.4f} |"
            )
        p = diagnostic_intervals
        lines += [
            "",
            "Perturbation diagnostics use the frozen 5% activity-flip intervention after",
            "cycle one, on final earlier-object partial-cue probes. Ordinary paired-root",
            "intervals are descriptive and do not add a confirmatory hypothesis.",
            "",
            (
                f"Mean executed cycles: {p['mean_cycles']['mean']:.3f}; nonconvergence fraction "
                f"{p['nonconvergence_fraction']['mean']:.4f}."
            ),
            (
                f"Perturbed minus unperturbed accuracy: {p['perturbation_accuracy_difference']['mean']:.5f} "
                f"[{p['perturbation_accuracy_difference']['lo']:.5f}, {p['perturbation_accuracy_difference']['hi']:.5f}]."
            ),
            (
                f"Excess canonical NMSE: {p['perturbation_excess_nmse']['mean']:.5f} "
                f"[{p['perturbation_excess_nmse']['lo']:.5f}, {p['perturbation_excess_nmse']['hi']:.5f}]."
            ),
            "",
            "![Settling cost](study-d-r1/settling-cost.png)",
            "",
            "The cost curve measures batches of eight; its one-cycle point is PH-1 under",
            "the identical initialization and acquired weights. Stopped paths are padded",
            "only for plotting; no extra cycles were executed. This is distinct from serial",
            "single-query latency. Fixed threshold constants are charged as supplied storage",
            "even when generated on demand. PH also materializes a 4,718,592-byte W per recall,",
            "has 768 activity and field coordinates per query plus an eight-coordinate action",
            "state, and retains transient state histories for cycle detection. These history",
            "bytes are bounded by 33 * 768 * 8 per query, excluding Python container overhead;",
            "process RSS includes those allocations and numerical-library workspaces.",
            "",
            "See [diagnostics](study-d-r1/diagnostics.json), [execution audit](study-d-r1/execution-audit.json)",
            "and [supplement source](study-d-r1/supplement-source.json). No new trial, tuning,",
            "confirmation root or model repair was introduced by this reporting-only audit.",
        ]
        path = ROOT / "reports/STUDY_D_R1.md"
        path.write_text(path.read_text() + "\n".join(lines) + "\n")
        budget.check(force=True)
        status = "complete"
    except BaseException as exc:
        status, error = "failed", repr(exc)
        raise
    finally:
        dump(dest / "phase-status.json", {"status": status, "error": error})
        budget.finish(status, error)
        md_bytes = sum(p.stat().st_size for p in (ROOT / "reports").glob("STUDY_D_R1*.md"))
        dump(
            REPORT / "resource-final.json",
            {
                "ledger": budget.rows,
                "cpu_seconds": sum(r["cpu_seconds"] for r in budget.rows),
                "wall_seconds": sum(r["wall_seconds"] for r in budget.rows),
                "peak_rss_bytes": max(r["peak_rss_bytes"] for r in budget.rows),
                "artifact_bytes_before_receipt": size(OUT) + size(REPORT) + md_bytes,
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
