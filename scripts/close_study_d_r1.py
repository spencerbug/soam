"""Verify immutable D-R1 artifacts and charge final archive packaging; no trials."""

import hashlib
from pathlib import Path

from soam.retrieval.runner import MANIFEST, OUT, REPORT, ROOT, Budget, read
from soam.temporal.runner import dump, size


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    dest = OUT / "closeout"
    dest.mkdir(parents=True, exist_ok=False)
    budget = Budget("report-closeout", read(MANIFEST)["limits"])
    status, error, counts = "running", None, {}
    try:
        for label, path in [
            ("frozen_source", REPORT / "source.json"),
            ("historical_d_source", ROOT / "reports/study-d/source.json"),
        ]:
            hashes = read(path)["hashes"]
            for name, expected in hashes.items():
                if digest(ROOT / name) != expected:
                    raise RuntimeError(f"Source mismatch: {name}")
            counts[label] = len(hashes)
        original = read(REPORT / "archive-index.json")
        for name, expected in original.items():
            if digest(OUT / name) != expected:
                raise RuntimeError(f"Original archive mismatch: {name}")
            budget.check()
        counts["original_archive_files"] = len(original)
        phases = read(REPORT / "phase-status.json")
        if any(row["status"] != "complete" or row["error"] for row in phases.values()):
            raise RuntimeError("Incomplete or failed numerical/reporting phase")
        raw = {
            str(p.relative_to(OUT)): digest(p)
            for p in sorted(OUT.rglob("*"))
            if p.is_file() and p.name != "ledger.json" and dest not in p.parents
        }
        compact_paths = list(REPORT.glob("*")) + list((ROOT / "reports").glob("STUDY_D_R1*.md"))
        compact = {
            str(p.relative_to(ROOT)): digest(p)
            for p in sorted(compact_paths)
            if p.is_file() and p.name not in {"archive-final.json", "closeout.json"}
        }
        dump(
            REPORT / "archive-final.json",
            {
                "raw_root": str(OUT.relative_to(ROOT)),
                "raw_hashes": raw,
                "repository_hashes": compact,
                "exclusions": [
                    "mutable raw ledger.json; final totals are in closeout.json",
                    "closeout receipts and archive-final.json to avoid self-reference",
                ],
            },
        )
        counts["final_raw_files"] = len(raw)
        counts["final_report_files"] = len(compact)
        budget.check(force=True)
        status = "complete"
    except BaseException as exc:
        status, error = "failed", repr(exc)
        raise
    finally:
        dump(dest / "phase-status.json", {"status": status, "error": error})
        budget.finish(status, error)
        dump(
            REPORT / "closeout.json",
            {
                "status": status,
                "error": error,
                "verified": counts,
                "new_trials": 0,
                "script_sha256": digest(Path(__file__)),
                "ledger": budget.rows,
                "cpu_seconds": sum(r["cpu_seconds"] for r in budget.rows),
                "wall_seconds": sum(r["wall_seconds"] for r in budget.rows),
                "peak_rss_bytes": max(r["peak_rss_bytes"] for r in budget.rows),
                "artifact_bytes_before_receipt": size(OUT)
                + size(REPORT)
                + sum(p.stat().st_size for p in (ROOT / "reports").glob("STUDY_D_R1*.md")),
            },
        )


if __name__ == "__main__":
    main()
