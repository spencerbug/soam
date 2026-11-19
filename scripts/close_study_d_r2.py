"""Reporting-only D-R2 source/archive closeout; no model fits or inference."""

import hashlib
import json
import resource
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs/study-d-r2-v1"
REPORT = ROOT / "reports/study-d-r2"


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    started_cpu, started_wall = time.process_time(), time.monotonic()
    if (REPORT / "closeout.json").exists() or (REPORT / "archive.json").exists():
        raise RuntimeError("Closeout already exists; do not overwrite provenance")
    source = read(OUT / "source.json")
    for rel, expected in source["hashes"].items():
        if sha(ROOT / rel) != expected or sha(OUT / "source" / rel) != expected:
            raise RuntimeError(f"Frozen source mismatch: {rel}")
    statuses = read(OUT / "phase-status.json")
    if set(statuses) != {"fixture", "confirmation", "repeat", "report"} or any(
        value["status"] != "complete" for value in statuses.values()
    ):
        raise RuntimeError("Incomplete phase inventory")
    verification = read(REPORT / "verification.json")
    if (
        verification["status"] != "pass"
        or verification["fit_attempts"] != 12
        or verification["failed_attempts"]
    ):
        raise RuntimeError("Invalid verification receipt")
    paths = sorted(
        [
            *[p for p in OUT.rglob("*") if p.is_file()],
            *[p for p in REPORT.rglob("*") if p.is_file()],
            ROOT / "reports/STUDY_D_R2.md",
            ROOT / "reports/STUDY_D_R2_DECISION.md",
            Path(__file__).resolve(),
        ]
    )
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    archive = {
        "hashes": hashes,
        "files": len(hashes),
        "exclusions": ["reports/study-d-r2/archive.json", "reports/study-d-r2/closeout.json"],
        "reason": "These final receipts are self-referential and created after the hashed payload.",
    }
    (REPORT / "archive.json").write_text(json.dumps(archive, indent=2, sort_keys=True) + "\n")
    prior = read(REPORT / "resource-final.json")
    totals = {
        "cpu_seconds": prior["cpu_seconds"] + time.process_time() - started_cpu,
        "wall_seconds": prior["wall_seconds"] + time.monotonic() - started_wall,
        "rss_bytes": max(
            prior["peak_rss_bytes"],
            resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            * (1 if sys.platform == "darwin" else 1024),
        ),
        "artifact_bytes": sum(p.stat().st_size for p in paths)
        + (REPORT / "archive.json").stat().st_size,
    }
    if any(value > prior["limits"][key] for key, value in totals.items()):
        raise RuntimeError("Closeout exceeds frozen allocation")
    receipt = {
        "status": "complete",
        "scientific_source": source["aggregate"],
        "source_commit": source["commit"],
        "frozen_files_verified": len(source["hashes"]),
        "archive_sha256": sha(REPORT / "archive.json"),
        "archived_files": len(hashes),
        "closeout_script_sha256": sha(Path(__file__).resolve()),
        "closeout_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "cumulative_use_before_closeout_receipt": totals,
        "limits": prior["limits"],
        "new_fits_or_inference": 0,
    }
    (REPORT / "closeout.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
