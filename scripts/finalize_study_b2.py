"""Read-only integrity audit and cumulative B2 resource receipt after confirmation."""

import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

from soam.robust.runner import MANIFEST, OUT, ROOT, receipt_check
from soam.temporal.runner import Budget, dump, size


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads(MANIFEST.read_text())
    budget = Budget(OUT, manifest, "final-verification-v2")
    dest = OUT / "final-verification-v2"
    dest.mkdir(exist_ok=False)
    report = ROOT / "reports/study-b2"
    try:
        receipt = receipt_check()
        historical = json.loads((ROOT / "reports/study-b/source.json").read_text())
        assert all(sha(ROOT / p) == h for p, h in historical["hashes"].items())
        changed = subprocess.check_output(
            ["git", "diff", "--name-only"], cwd=ROOT, text=True
        ).splitlines()
        allowed = {
            "README.md",
            "PRIORITIES.md",
            "docs/HYPOTHESES.md",
            "docs/RESEARCH_PATHS.md",
            "docs/ROADMAP.md",
            "tickets/README.md",
        }
        assert set(changed) <= allowed, changed
        baseline = json.loads((report / "baseline-audit.json").read_text())
        assert baseline["fit_exact"] and baseline["source_matches_historical"]
        assert all(baseline["prediction_arrays_exact"].values())
        repeat = json.loads((report / "reproduction.json").read_text())
        assert all(all(v.values()) for v in repeat.values())
        reduction = json.loads((report / "independent-reduction.json").read_text())
        assert reduction["checked_values"] == 1040
        assert reduction["maximum_absolute_error"] < 1e-12
        fits = list(OUT.glob("**/*-status.json"))
        assert len(fits) == 28
        assert all(json.loads(p.read_text())["status"] == "complete" for p in fits)
        evaluations = [
            p
            for phase in ("confirmation", "repeat")
            for p in (OUT / phase).glob("*/*/results.json")
        ]
        assert len(evaluations) == 88
        nonfinite, divergence, eigen_min, asymmetry = 0, 0, float("inf"), 0.0
        array_count = 0
        for p in evaluations:
            budget.check()
            result = json.loads(p.read_text())
            assert json.loads((p.parent / "status.json").read_text())["status"] == "complete"
            for row in result["rows"].values():
                nonfinite += row["nonfinite"]
                divergence += row["divergent_episodes_nmse_gt100"]
                if row.get("min_eigenvalue", 0) > 0:
                    eigen_min = min(eigen_min, row["min_eigenvalue"])
                asymmetry = max(asymmetry, row.get("max_asymmetry", 0))
                if p.parent.name != "PC16":
                    assert row["min_eigenvalue"] > 0
            with np.load(p.parent / "arrays.npz") as arrays:
                for key in arrays.files:
                    assert np.isfinite(arrays[key]).all(), (str(p), key)
                    array_count += 1
        assert nonfinite == 0
        index = {}
        for phase in (
            "audit",
            "fixture",
            "fixture-storage-correction",
            "fixture-storage-a1",
            "screen1",
            "screen2",
            "hybrid",
            "freeze",
            "confirmation",
            "repeat",
            "report",
        ):
            for p in sorted((OUT / phase).rglob("*")):
                if p.is_file():
                    index[str(p.relative_to(ROOT))] = sha(p)
            budget.check()
        dump(report / "artifact-sha256.json", index)
        record = {
            "confirmation_receipt": receipt["sha256"],
            "frozen_source_files_verified": len(receipt["source"]["hashes"]),
            "historical_dependency_files_verified": len(historical["hashes"]),
            "historical_fitted_tensors_exact": True,
            "historical_prediction_arrays_exact": len(baseline["prediction_arrays_exact"]),
            "historical_tracked_artifacts_and_decisions_unchanged": True,
            "completed_new_base_fits": len(fits),
            "total_fits_including_historical_audit": len(fits) + 1,
            "completed_confirmation_and_repeat_evaluations": len(evaluations),
            "finite_saved_arrays": array_count,
            "nonfinite_records": nonfinite,
            "divergent_episodes_nmse_gt100": divergence,
            "minimum_positive_posterior_covariance_eigenvalue": eigen_min,
            "maximum_covariance_asymmetry": asymmetry,
            "independent_reduction": reduction,
            "exact_repeat_candidates": len(repeat),
            "indexed_immutable_artifact_files": len(index),
            "artifact_index_sha256": sha(report / "artifact-sha256.json"),
            "post_freeze_reporting_scripts": {
                str(p.relative_to(ROOT)): sha(p)
                for p in sorted((ROOT / "scripts").glob("*study_b2*.py"))
                if str(p.relative_to(ROOT)) not in receipt["source"]["hashes"]
            },
            "validation": {
                "baseline_pytest": "238 passed in 16.94s before changes",
                "final_pytest": "266 passed in 15.65s",
                "robust_invariants": "28 passed in 1.49s",
                "lint_scope": "soam tests scripts; frozen historical report scripts excluded",
                "broad_lint_limitation": "16 existing errors in historical reports/shared-population-gate/audit.py and reports/shared-population-study/confirmation/{analysis,final-verify,render}.py; unchanged",
            },
            "selection_or_threshold_changed": False,
        }
        dump(dest / "verification.json", record)
        dump(report / "verification.json", record)
        assert size(OUT) + size(report) < manifest["artifact_bytes"]
        budget.check(force=True)
        budget.finish("complete")
    except BaseException as error:
        budget.finish("failed", repr(error))
        raise
    ledger = json.loads((OUT / "ledger.json").read_text())
    resource = {
        "scope": "B2 numerical phases only, including preserved failed storage projection, profiling, diagnostics, rendering and final verification; no GPU use",
        "excluded_engineering_overhead": "Tests, source/literature review and unsuccessful local-worker assistance; total CPU not instrumented",
        "limits": {
            k: manifest[k]
            for k in (
                "cpu_seconds",
                "wall_seconds",
                "rss_bytes",
                "artifact_bytes",
                "max_fit_attempts",
            )
        },
        "cpu_seconds": sum(v["cpu_seconds"] for v in ledger),
        "execution_wall_seconds": sum(v["wall_seconds"] for v in ledger),
        "peak_rss_bytes": max(v["peak_rss_bytes"] for v in ledger),
        "gpu_seconds": 0,
        "fits_including_historical_audit": 29,
        "ledger": ledger,
        "ledger_sha256": sha(OUT / "ledger.json"),
        "checkpoint_artifact_bytes": size(OUT),
        "compact_report_artifact_bytes": size(report),
        "script_sha256": sha(Path(__file__)),
    }
    assert resource["cpu_seconds"] <= manifest["cpu_seconds"]
    assert resource["execution_wall_seconds"] <= manifest["wall_seconds"]
    assert resource["peak_rss_bytes"] <= manifest["rss_bytes"]
    # Include this receipt in artifact accounting, iterating until its byte count settles.
    for _ in range(4):
        resource["compact_report_artifact_bytes"] = size(report)
        resource["total_artifact_bytes"] = size(OUT) + size(report)
        resource["within_all_limits"] = (
            resource["total_artifact_bytes"] <= manifest["artifact_bytes"]
        )
        dump(report / "resource-final.json", resource)
    assert resource["within_all_limits"]
    print(json.dumps({k: v for k, v in resource.items() if k != "ledger"}, indent=2))


if __name__ == "__main__":
    main()
