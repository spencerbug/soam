"""Finite D-R2 phases with immutable source receipts and cumulative limits."""

import argparse
import hashlib
import json
import platform
import resource
import shutil
import signal
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import torch

from soam.temporal.runner import digest, dump, size

from .engine import run_root

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "runs/study-d-r2-v1"
REPORT = ROOT / "reports/study-d-r2"
MANIFEST = ROOT / "docs/protocols/study_d_r2_v1.json"


def read(path):
    return json.loads(path.read_text())


def now():
    return datetime.now(UTC).isoformat()


def source():
    paths = sorted(
        [
            *ROOT.glob("soam/**/*.py"),
            *ROOT.glob("tests/*.py"),
            ROOT / "pyproject.toml",
            ROOT / "uv.lock",
            MANIFEST,
            ROOT / "docs/STUDY_D_R2_PROTOCOL.md",
            ROOT / "docs/requests/retrieval_diagnostic_2026_11_19.md",
            ROOT / "reports/study-d-r1/development-selection.json",
        ]
    )
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    if (
        not set(hashes) <= tracked
        or subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", *hashes], cwd=ROOT, check=False
        ).returncode
    ):
        raise RuntimeError("Commit all scientific source before numerical execution")
    return {
        "hashes": hashes,
        "aggregate": digest(hashes),
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "python": sys.version,
        "numpy": np.__version__,
        "torch": torch.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "device": "cpu",
        "dtype": "float64",
        "threads": torch.get_num_threads(),
        "interop_threads": torch.get_num_interop_threads(),
        "deterministic": torch.are_deterministic_algorithms_enabled(),
    }


class ResourceStop(RuntimeError):
    """A finite allocation stop, not a scientific negative."""


class Budget:
    def __init__(self, phase, limits):
        self.phase, self.limits = phase, limits
        self.cpu, self.wall = time.process_time(), time.monotonic()
        self.rows = read(OUT / "ledger.json") if (OUT / "ledger.json").exists() else []
        self.last = -1.0

    def usage(self):
        return {
            "cpu_seconds": sum(r["cpu_seconds"] for r in self.rows)
            + time.process_time()
            - self.cpu,
            "wall_seconds": sum(r["wall_seconds"] for r in self.rows)
            + time.monotonic()
            - self.wall,
            "rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            * (1 if sys.platform == "darwin" else 1024),
            "artifact_bytes": size(OUT)
            + size(REPORT)
            + (
                (ROOT / "reports/STUDY_D_R2.md").stat().st_size
                if (ROOT / "reports/STUDY_D_R2.md").exists()
                else 0
            ),
        }

    def check(self, force=False):
        if not force and time.process_time() - self.last < 0.2:
            return
        self.last = time.process_time()
        fraction = 1 if self.phase == "report" else self.limits["stop_new_trials_fraction"]
        for key, value in self.usage().items():
            bound = self.limits[key] * (fraction if key.endswith("seconds") else 1)
            if value > bound:
                raise ResourceStop(f"Cumulative {key} ceiling reached: {value} > {bound}")

    def finish(self, status, error):
        row = {
            "phase": self.phase,
            "status": status,
            "error": error,
            "ended_utc": now(),
            "cpu_seconds": time.process_time() - self.cpu,
            "wall_seconds": time.monotonic() - self.wall,
            "peak_rss_bytes": self.usage()["rss_bytes"],
            "artifact_bytes": size(OUT) + size(REPORT),
        }
        self.rows.append(row)
        dump(OUT / "ledger.json", self.rows)
        if self.phase == "report":
            dump(
                REPORT / "resource-final.json",
                {
                    "phases": self.rows,
                    "cpu_seconds": sum(r["cpu_seconds"] for r in self.rows),
                    "wall_seconds": sum(r["wall_seconds"] for r in self.rows),
                    "peak_rss_bytes": max(r["peak_rss_bytes"] for r in self.rows),
                    "artifact_bytes_before_final_receipt": self.usage()["artifact_bytes"],
                    "limits": self.limits,
                },
            )
        print(json.dumps(row), flush=True)


def execute_root(phase, root, manifest, budget):
    dest = OUT / phase / f"root-{root}"
    if dest.exists():
        status = read(dest / "fit-status.json")
        if status["status"] == "complete":
            return read(dest / "result.json")
        raise RuntimeError("An incomplete/failed root cannot be retried or replaced")
    budget.check(force=True)
    if len(list(OUT.glob("*/root-*/fit-status.json"))) >= manifest["limits"]["max_fit_attempts"]:
        raise ResourceStop("Fit-attempt ceiling")
    dest.mkdir(parents=True)
    dump(dest / "fit-status.json", {"status": "running", "root": root, "started_utc": now()})
    try:
        result = run_root(root, manifest, dest, budget.check)
        dump(dest / "result.json", result)
        budget.check(force=True)
        dump(dest / "fit-status.json", {"status": "complete", "root": root})
        print(json.dumps({"phase": phase, "root": root, "status": "complete"}), flush=True)
        return result
    except BaseException as exc:
        dump(dest / "fit-status.json", {"status": "failed", "root": root, "error": repr(exc)})
        raise


def fixture(manifest, budget):
    start_cpu, start_wall = time.process_time(), time.monotonic()
    execute_root("fixture", manifest["fixture_root"], manifest, budget)
    root_cpu, root_wall = time.process_time() - start_cpu, time.monotonic() - start_wall
    limits = manifest["limits"]
    projected = {
        "cpu_seconds": 2 * 12 * root_cpu + limits["report_seconds_reserve"],
        "wall_seconds": 2 * 12 * root_wall + limits["report_seconds_reserve"],
        "rss_bytes": 2 * budget.usage()["rss_bytes"],
        "artifact_bytes": 2 * 12 * size(OUT / "fixture")
        + size(OUT / "source")
        + limits["report_bytes_reserve"],
    }
    receipt = {
        "projected": projected,
        "limits": limits,
        "pass": all(v <= limits[k] for k, v in projected.items()),
    }
    dump(OUT / "feasibility.json", receipt)
    if not receipt["pass"]:
        raise ResourceStop("Fixture-based projection does not fit; confirmation prohibited")


def validate_schedule(phase, statuses):
    required = {
        "fixture": [],
        "confirmation": ["fixture"],
        "repeat": ["fixture", "confirmation"],
        "report": ["fixture", "confirmation", "repeat"],
    }[phase]
    if phase in statuses:
        raise RuntimeError("Phase already attempted; no silent rerun")
    if any(statuses.get(p, {}).get("status") != "complete" for p in required):
        raise RuntimeError("Required preceding phase is not complete")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("fixture", "confirmation", "repeat", "report"))
    phase = parser.parse_args().phase
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    manifest = read(MANIFEST)
    statuses = read(OUT / "phase-status.json") if (OUT / "phase-status.json").exists() else {}
    validate_schedule(phase, statuses)
    receipt = source()
    if phase == "fixture":
        OUT.mkdir(parents=True, exist_ok=False)
    elif read(OUT / "source.json")["aggregate"] != receipt["aggregate"]:
        raise RuntimeError("Frozen scientific source changed")
    budget = Budget(phase, manifest["limits"])
    status, error = "running", None
    statuses[phase] = {"status": status, "started_utc": now()}
    dump(OUT / "phase-status.json", statuses)

    def timed_out(signum, frame):
        raise ResourceStop("Execution-wall watchdog expired")

    old_handler = signal.signal(signal.SIGALRM, timed_out)
    remaining = manifest["limits"]["wall_seconds"] - budget.usage()["wall_seconds"]
    signal.setitimer(signal.ITIMER_REAL, max(0.01, remaining))
    try:
        budget.check(force=True)
        if phase == "fixture":
            dump(OUT / "source.json", receipt)
            dump(OUT / "manifest.json", manifest)
            for rel in receipt["hashes"]:
                target = OUT / "source" / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, target)
            fixture(manifest, budget)
        elif phase in {"confirmation", "repeat"}:
            if not read(OUT / "feasibility.json")["pass"]:
                raise ResourceStop("Fixture feasibility did not pass")
            roots = (
                manifest["confirmation_roots"]
                if phase == "confirmation"
                else [manifest["repeat_root"]]
            )
            for root in roots:
                execute_root(phase, root, manifest, budget)
        else:
            from .report import report

            report(manifest, budget)
        budget.check(force=True)
        status = "complete"
    except BaseException as exc:
        status = "resource_stop" if isinstance(exc, ResourceStop) else "invalid_execution"
        error = repr(exc)
        raise
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)
        statuses[phase].update(status=status, error=error, ended_utc=now())
        dump(OUT / "phase-status.json", statuses)
        budget.finish(status, error)


if __name__ == "__main__":
    main()
