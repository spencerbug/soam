"""Audit completed Study C archives without fitting or changing scientific results."""

import argparse
import json
import shutil
import subprocess

from soam.ambiguity.runner import MANIFEST, OUT, REPORT, ROOT, receipt_check, sha
from soam.temporal.runner import Budget, dump, size


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify_hashes(hashes):
    for relative, expected in hashes.items():
        require(sha(ROOT / relative) == expected, f"Hash mismatch: {relative}")
    return len(hashes)


def main():
    receipt = receipt_check()
    m = json.loads(MANIFEST.read_text())
    dest = OUT / "final-audit"
    dest.mkdir(exist_ok=False)
    budget = Budget(OUT, m["limits"], "final-audit")
    try:
        require(
            sha(REPORT / "confirmation-receipt.json") == sha(OUT / "freeze/receipt.json"),
            "Compact confirmation receipt differs",
        )
        fits = list(OUT.glob("**/fit-status.json"))
        require(len(fits) == 67, "Unexpected fitted execution count")
        require(
            all(json.loads(p.read_text())["status"] == "complete" for p in fits),
            "Incomplete or failed fit",
        )
        inventory = receipt["selection"]["inventory"]
        conditions = m["primary_conditions"] + m["secondary_conditions"]
        cells = 0
        for root in m["confirmation_roots"]:
            results = json.loads((OUT / "confirmation" / str(root) / "results.json").read_text())
            require(set(results) == set(inventory), "Missing mandatory candidate")
            for name in inventory:
                for condition in conditions:
                    path = OUT / "confirmation" / str(root) / name / f"{condition}.npz"
                    require(path.is_file(), f"Missing archive: {path}")
                    cells += 1

        repeat = json.loads((REPORT / "reproduction.json").read_text())
        require(
            all(all(v for k, v in row.items() if k != "arrays") for row in repeat.values()),
            "Prescribed repeat failed",
        )
        repeat_arrays = sum(row.get("arrays", 0) for row in repeat.values())
        require(repeat_arrays == 1530, "Unexpected repeat array count")
        verification = json.loads((REPORT / "verification.json").read_text())
        require(verification["independent_values"] == 810, "Incomplete independent reduction")
        require(verification["maximum_absolute_error"] < 1e-12, "Reduction mismatch")
        require(all(verification["identical_evidence"].values()), "Causal invariance failed")

        b2 = json.loads((ROOT / "reports/study-b2/confirmation-receipt.json").read_text())
        historical = {
            "study_b2_source": verify_hashes(b2["source"]["hashes"]),
            "study_b_source": verify_hashes(
                json.loads((ROOT / "reports/study-b/source.json").read_text())["hashes"]
            ),
        }
        protected = [
            "reports/STUDY_A.md",
            "reports/STUDY_A_DECISION.md",
            "reports/STUDY_B.md",
            "reports/STUDY_B_DECISION.md",
            "reports/STUDY_B2.md",
            "reports/STUDY_B2_DECISION.md",
            "reports/SHARED_POPULATION_GATE.md",
            "tickets/SOAM-052-shared-population-gate.md",
        ]
        subprocess.run(
            ["git", "diff", "--exit-code", receipt["source"]["commit"], "--", *protected],
            cwd=ROOT,
            check=True,
        )
        old_index = json.loads((REPORT / "artifact-sha256.json").read_text())
        verified_archives = verify_hashes(old_index)
        shutil.copyfile(REPORT / "artifact-sha256.json", dest / "original-artifact-sha256.json")
        index = {
            str(p.relative_to(ROOT)): sha(p)
            for p in sorted(OUT.rglob("*"))
            if p.is_file() and dest not in p.parents and p != OUT / "ledger.json"
        }
        dump(REPORT / "artifact-sha256.json", index)
        script_paths = sorted(ROOT.glob("scripts/*study_c*.py"))
        provenance = {
            "scope": "Post-confirmation archive verification only; no new scientific runs",
            "reporting_script_hashes": {str(p.relative_to(ROOT)): sha(p) for p in script_paths},
        }
        dump(dest / "provenance.json", provenance)
        audit = {
            "status": "pass",
            "source_fingerprint": receipt["source"]["aggregate"],
            "frozen_source_files": len(receipt["source"]["hashes"]),
            "historical_source_files": historical,
            "historical_reports_unchanged": protected,
            "fits_complete": len(fits),
            "confirmation_roots": m["confirmation_roots"],
            "mandatory_candidates": inventory,
            "confirmation_cells_present": cells,
            "prescribed_repeat_arrays_exact": repeat_arrays,
            "independent_reduction": verification,
            "prior_raw_artifact_hashes_verified": verified_archives,
            "refreshed_raw_artifact_index_entries": len(index),
            "artifact_index_sha256": sha(REPORT / "artifact-sha256.json"),
            "index_exclusions": ["mutable ledger.json", "this final-audit directory"],
            **provenance,
        }
        dump(REPORT / "final-verification.json", audit)
        dump(dest / "verification.json", audit)
        budget.check(force=True)
        budget.finish("complete")
    except Exception as error:
        budget.finish("failed", repr(error))
        raise

    export_resources()


def export_resources():
    receipt_check()
    m = json.loads(MANIFEST.read_text())
    dest = OUT / "resource-export"
    dest.mkdir(exist_ok=False)
    budget = Budget(OUT, m["limits"], "resource-export")
    dump(
        dest / "provenance.json",
        {
            "script_sha256": sha(ROOT / "scripts/finalize_study_c.py"),
            "scope": "Resource summary only; no scientific fits or primary-result changes",
            "repair": "First export raised KeyError rss_bytes after a successful integrity audit; peak_rss_bytes now maps explicitly to the rss_bytes limit. Original script preserved in final-audit/script-at-audit.py.",
        },
    )
    budget.check(force=True)
    budget.finish("complete")
    ledger = json.loads((OUT / "ledger.json").read_text())
    resources = {
        "phases": ledger,
        "cpu_seconds": sum(row["cpu_seconds"] for row in ledger),
        "wall_seconds": sum(row["wall_seconds"] for row in ledger),
        "peak_rss_bytes": max(row["peak_rss_bytes"] for row in ledger),
        "gpu_seconds": 0,
        "fits": len(list(OUT.glob("**/fit-status.json"))),
        "limits": m["limits"],
        "accounting": "Instrumented phases only; imports, tests and editorial work excluded",
        "artifact_accounting": "Raw archives, compact reports and three Study C Markdown reports at audit close",
    }
    target = REPORT / "resource-final.json"
    for _ in range(8):
        resources["artifact_bytes"] = (
            size(OUT)
            + size(REPORT)
            + sum(p.stat().st_size for p in (ROOT / "reports").glob("STUDY_C*.md"))
        )
        resources["within_limits"] = all(
            resources["peak_rss_bytes" if key == "rss_bytes" else key] <= limit
            for key, limit in m["limits"].items()
        )
        previous = target.read_text() if target.exists() else None
        dump(target, resources)
        if target.read_text() == previous:
            break
    require(resources["within_limits"], "Final resource ceiling exceeded")
    print(json.dumps({key: value for key, value in resources.items() if key != "phases"}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resources-only", action="store_true")
    if parser.parse_args().resources_only:
        export_resources()
    else:
        main()
