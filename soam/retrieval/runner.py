"""Finite D-R1 phases with source receipts, explicit allocation and cumulative ceilings."""

import argparse
import hashlib
import json
import platform
import resource
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import torch

from soam.acquisition.models import Core
from soam.temporal.runner import digest, dump, size, tensor_hash

from .data import training
from .engine import CONDITIONS, array_hash, core_error, evaluate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "runs/study-d-r1-v1"
REPORT = ROOT / "reports/study-d-r1"
MANIFEST = ROOT / "docs/protocols/study_d_r1_v1.json"
ALLOCATION = ROOT / "docs/requests/study_d_r1_allocation_2026_11_18.json"
GROUPS = ("NOWRITE", "KV", "REG", "FAST", "REG-LIFT", "PH-FULL")


def read(path):
    return json.loads(path.read_text())


def now():
    return datetime.now(UTC).isoformat()


def source(dest=None):
    paths = sorted(
        [
            *ROOT.glob("soam/**/*.py"),
            *ROOT.glob("tests/*.py"),
            ROOT / "pyproject.toml",
            ROOT / "uv.lock",
            MANIFEST,
            ALLOCATION,
            ROOT / "docs/STUDY_D_R1_PROTOCOL.md",
        ]
    )
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    if not set(hashes) <= tracked:
        raise RuntimeError("Commit all scientific source before numerical work")
    if subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", *hashes], cwd=ROOT, check=False
    ).returncode:
        raise RuntimeError("Scientific source is not committed")
    value = {
        "hashes": hashes,
        "aggregate": digest(hashes),
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "dirty": subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True
        ).splitlines(),
        "python": sys.version,
        "torch": torch.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "device": "cpu",
        "dtype": "float64",
        "threads": torch.get_num_threads(),
        "interop_threads": torch.get_num_interop_threads(),
        "deterministic": torch.are_deterministic_algorithms_enabled(),
    }
    if dest:
        dump(dest / "source.json", value)
        for rel in hashes:
            target = dest / "source" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)
    return value


class ScreenStop(RuntimeError):
    """A prespecified scientific/resource stop, distinct from invalid software execution."""

    def __init__(self, kind, message):
        self.kind = kind
        super().__init__(message)


class Budget:
    def __init__(self, phase, limits):
        self.phase, self.m = phase, limits
        self.cpu, self.wall = time.process_time(), time.monotonic()
        self.rows = read(OUT / "ledger.json") if (OUT / "ledger.json").exists() else []
        self.last = 0.0
        self.check(force=True)

    def check(self, force=False):
        elapsed = time.process_time() - self.cpu
        if not force and elapsed - self.last < 0.25:
            return
        self.last = elapsed
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (
            1 if sys.platform == "darwin" else 1024
        )
        total_cpu = sum(x["cpu_seconds"] for x in self.rows) + elapsed
        total_wall = sum(x["wall_seconds"] for x in self.rows) + time.monotonic() - self.wall
        fraction = 1.0 if self.phase == "report" else 0.9
        if (
            total_cpu > self.m["cpu_seconds"] * fraction
            or total_wall > self.m["wall_seconds"] * fraction
        ):
            raise ScreenStop("resource_limit", "Numerical CPU/wall ceiling reached")
        if rss > self.m["rss_bytes"]:
            raise ScreenStop("resource_limit", "RSS ceiling reached")
        if size(OUT) + size(REPORT) > self.m["artifact_bytes"]:
            raise ScreenStop("resource_limit", "Artifact ceiling reached")

    def finish(self, status, error):
        row = {
            "phase": self.phase,
            "status": status,
            "error": error,
            "ended_utc": now(),
            "cpu_seconds": time.process_time() - self.cpu,
            "wall_seconds": time.monotonic() - self.wall,
            "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            * (1 if sys.platform == "darwin" else 1024),
            "artifact_bytes": size(OUT) + size(REPORT),
        }
        self.rows.append(row)
        dump(OUT / "ledger.json", self.rows)
        print(json.dumps(row), flush=True)


def inventory(m):
    return [
        (name, float(setting))
        for name in GROUPS
        for setting in (
            m["reg_ridges"]
            if name == "REG"
            else m["fast_rates"]
            if name == "FAST"
            else m["reg_lift_ridges"]
            if name == "REG-LIFT"
            else [1.0]
        )
    ]


def fit(dest, root, ridge, budget):
    budget.check(force=True)
    if len(list(OUT.glob("**/fit-status.json"))) >= budget.m["max_fit_attempts"]:
        raise RuntimeError("Fit-attempt ceiling")
    dest.mkdir(parents=True, exist_ok=False)
    dump(dest / "fit-status.json", {"status": "running", "started_utc": now()})
    start = time.process_time()
    try:
        data = training(root)
        core = Core.fit(data, ridge)
        denominator = max(float(data[0].square().mean()), 1e-8)
        checkpoint = {"a": core.a, "b": core.b}
        torch.save(checkpoint, dest / "core.pt")
        inputs = {str(i): v.numpy() for i, v in enumerate(data)}
        np.savez_compressed(dest / "training.npz", **inputs)
        row = {
            "root": root,
            "ridge": ridge,
            "normalization": denominator,
            "input_hash": array_hash(inputs),
            "core_hash": tensor_hash(checkpoint),
            "core_probe": core_error(core, root, denominator),
            "cpu_seconds": time.process_time() - start,
            "transition_records": 2048,
            "feature_snapshots": 4096,
        }
        dump(dest / "fit.json", row)
        if row["core_probe"] > 0.02:
            raise RuntimeError("Core competence invalid")
        dump(dest / "fit-status.json", {"status": "complete"})
        budget.check(force=True)
        return core, denominator, row
    except BaseException as exc:
        dump(dest / "fit-status.json", {"status": "failed", "error": repr(exc)})
        raise


def load_fit(dest):
    checkpoint = torch.load(dest / "core.pt", weights_only=True)
    return Core(checkpoint["a"], checkpoint["b"]), read(dest / "fit.json")["normalization"]


def trial(dest, name, core, setting, root, split, denominator, budget):
    budget.check(force=True)
    dest.mkdir(parents=True, exist_ok=False)
    dump(dest / "status.json", {"status": "running", "started_utc": now()})
    cpu, wall = time.process_time(), time.monotonic()
    try:
        results, arrays, inputs, memory = evaluate(
            name, core, setting, root, split, denominator, budget.check
        )
        np.savez_compressed(dest / "inputs.npz", **inputs)
        torch.save(memory, dest / "last-memory.pt")
        for arm in arrays:
            np.savez_compressed(dest / f"{arm}.npz", **arrays[arm])
        row = {
            "group": name,
            "setting": setting,
            "root": root,
            "split": split,
            "cpu_seconds": time.process_time() - cpu,
            "wall_seconds": time.monotonic() - wall,
            "results": results,
        }
        dump(dest / "result.json", row)
        dump(dest / "status.json", {"status": "complete", "ended_utc": now()})
        budget.check(force=True)
        print(
            json.dumps({"trial": str(dest.relative_to(OUT)), "cpu_seconds": row["cpu_seconds"]}),
            flush=True,
        )
        return row
    except BaseException as exc:
        dump(dest / "status.json", {"status": "failed", "error": repr(exc), "ended_utc": now()})
        raise


def fixture(dest, m, budget):
    core, den, fitted = fit(dest / "fit", m["fixture_root"], m["core_ridges"][0], budget)
    rows = []
    for index, (name, setting) in enumerate(inventory(m)):
        path = dest / f"{index:02d}-{name}"
        row = trial(path, name, core, setting, m["fixture_root"], "fixture", den, budget)
        rows.append({**row, "bytes": size(path)})

    # Exact finite family counts: two full tuning inventories, plus 13 selected
    # inventories (2 calibration + 10 confirmation + 1 repeat). Use worst setting cost.
    def projected(key):
        return 2 * sum(r[key] for r in rows) + 13 * sum(
            max(r[key] for r in rows if r["group"] == name) for name in GROUPS
        )

    remaining_cpu = 2 * (projected("cpu_seconds") + 15 * fitted["cpu_seconds"] + 120)
    remaining_wall = 2 * (projected("wall_seconds") + 15 * fitted["cpu_seconds"] + 120)
    remaining_bytes = 2 * (projected("bytes") + 15 * size(dest / "fit") + 32 * 1024**2)
    spent_cpu = time.process_time() - budget.cpu
    spent_wall = time.monotonic() - budget.wall
    projection = {
        "remaining_cpu_seconds_2x": remaining_cpu,
        "remaining_wall_seconds_2x": remaining_wall,
        "remaining_artifact_bytes_2x": remaining_bytes,
        "spent_fixture_cpu_seconds": spent_cpu,
        "planned_fits": 16,
        "fixture_writer_configurations": len(rows),
        "pass": remaining_cpu + spent_cpu < 0.9 * m["limits"]["cpu_seconds"]
        and remaining_wall + spent_wall < 0.9 * m["limits"]["wall_seconds"]
        and remaining_bytes + size(OUT) + size(REPORT) < 0.9 * m["limits"]["artifact_bytes"],
    }
    dump(dest / "projection.json", projection)
    if not projection["pass"]:
        raise ScreenStop(
            "infeasible", "Fixture feasibility screen failed; no development authorized"
        )


def development(dest, m, budget):
    fitted = []
    for root in m["development_roots"]:
        for index, ridge in enumerate(m["core_ridges"]):
            _, _, row = fit(dest / str(root) / f"core{index}", root, ridge, budget)
            fitted.append(row)
    scores = [
        np.mean([x["core_probe"] for x in fitted if x["ridge"] == ridge])
        for ridge in m["core_ridges"]
    ]
    core_index = next(i for i, s in enumerate(scores) if s <= min(scores) + 1e-12)
    rows = []
    for root in m["development_roots"]:
        core, den = load_fit(dest / str(root) / f"core{core_index}")
        for i, (name, setting) in enumerate(inventory(m)):
            rows.append(
                trial(
                    dest / str(root) / f"{i:02d}-{name}",
                    name,
                    core,
                    setting,
                    root,
                    "development-selection",
                    den,
                    budget,
                )
            )
    selected = {}
    for name in GROUPS:
        candidates = []
        for arm, setting in inventory(m):
            if arm != name:
                continue
            metrics = [
                r["results"][name]["metrics"]
                for r in rows
                if r["group"] == name and r["setting"] == setting
            ]
            score = np.mean(
                [v[c][key] for v in metrics for c in CONDITIONS for key in ("J", "old_error")]
            )
            candidates.append((setting, float(score)))
        selected[name] = next(
            setting
            for setting, score in candidates
            if score <= min(x[1] for x in candidates) + 1e-12
        )
    competent = all(
        r["results"]["PH-FULL"]["metrics"]["full"]["accuracy8"] >= 0.9
        and r["results"]["PH-FULL"]["metrics"]["partial"]["accuracy8"] >= 0.8
        for r in rows
        if r["group"] == "PH-FULL"
    )
    result = {
        "core_index": core_index,
        "core_ridge": m["core_ridges"][core_index],
        "settings": selected,
        "competence_pass": competent,
        "core_selection_scores": scores,
    }
    dump(dest / "selection.json", result)
    if not competent:
        raise ScreenStop(
            "competence_failure", "Bounded development competence failure; confirmation prohibited"
        )


def calibration(dest, m, budget):
    selection = read(OUT / "development/selection.json")
    rows = []
    for root in m["development_roots"]:
        core, den = load_fit(OUT / "development" / str(root) / f"core{selection['core_index']}")
        for name in GROUPS:
            trial(
                dest / str(root) / name,
                name,
                core,
                selection["settings"][name],
                root,
                "development-calibration",
                den,
                budget,
            )
            rows.append((root, name))
    thresholds = {}
    for name in m["arms"]:
        group = "PH-FULL" if name == "PH-1" else name
        thresholds[name] = {}
        for ci, condition in enumerate(CONDITIONS):
            scores = []
            for root in m["development_roots"]:
                with np.load(dest / str(root) / group / f"{name}.npz") as a:
                    scores.extend(a["d2_scores"][ci, :, -1].flatten())
            thresholds[name][condition] = float(np.quantile(scores, 0.95, method="higher"))
    dump(dest / "thresholds.json", thresholds)


def freeze(dest, m, budget):
    identity = source()
    selection = read(OUT / "development/selection.json")
    if not selection["competence_pass"]:
        raise RuntimeError("Candidate not competent")
    dump(
        dest / "receipt.json",
        {
            "manifest": m,
            "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
            "source": identity,
            "selection": selection,
            "thresholds": read(OUT / "calibration/thresholds.json"),
            "allocation": read(ALLOCATION),
            "ledger": budget.rows,
            "created_utc": now(),
        },
    )


def confirmation(dest, m, budget, repeat=False):
    receipt = read(OUT / "freeze/receipt.json")
    if source()["aggregate"] != receipt["source"]["aggregate"]:
        raise RuntimeError("Frozen confirmation source changed")
    selected = receipt["selection"]
    for root in [m["repeat_root"]] if repeat else m["confirmation_roots"]:
        core, den, _ = fit(dest / str(root) / "fit", root, selected["core_ridge"], budget)
        for name in GROUPS:
            trial(
                dest / str(root) / name,
                name,
                core,
                selected["settings"][name],
                root,
                "confirmation",
                den,
                budget,
            )


def require_previous(phase):
    previous = {
        "development": "fixture",
        "calibration": "development",
        "freeze": "calibration",
        "confirmation": "freeze",
        "repeat": "confirmation",
    }
    if phase in previous:
        status = read(OUT / previous[phase] / "phase-status.json")
        if status["status"] != "complete":
            raise RuntimeError("Previous phase incomplete")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "phase",
        choices=[
            "fixture",
            "development",
            "calibration",
            "freeze",
            "confirmation",
            "repeat",
            "report",
        ],
    )
    phase = parser.parse_args().phase
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    m, approval = read(MANIFEST), read(ALLOCATION)
    if (
        approval["manifest_sha256"] != hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
        or approval["limits"] != m["limits"]
    ):
        raise RuntimeError("Allocation does not bind current manifest")
    require_previous(phase)
    dest = OUT / phase
    dest.mkdir(parents=True, exist_ok=False)
    budget = Budget(phase, m["limits"])
    status, error, outcome_type = "running", None, None
    dump(dest / "phase-status.json", {"status": status, "started_utc": now()})
    try:
        identity = source(dest)
        if (
            phase not in {"fixture", "report"}
            and identity["aggregate"] != read(OUT / "fixture/source.json")["aggregate"]
        ):
            raise RuntimeError("Numerical implementation changed since fixture")
        if phase == "report":
            from .report import report

            report(dest, m, budget)
        elif phase in {"confirmation", "repeat"}:
            confirmation(dest, m, budget, repeat=phase == "repeat")
        else:
            globals()[phase](dest, m, budget)
        budget.check(force=True)
        status = "complete"
    except BaseException as exc:
        status, error = ("stopped" if isinstance(exc, ScreenStop) else "failed"), repr(exc)
        outcome_type = exc.kind if isinstance(exc, ScreenStop) else "invalid_execution"
        raise
    finally:
        dump(
            dest / "phase-status.json",
            {"status": status, "error": error, "outcome_type": outcome_type, "ended_utc": now()},
        )
        budget.finish(status, error)
        if phase == "report" and status == "complete":
            dump(
                REPORT / "resource-final.json",
                {
                    "ledger": budget.rows,
                    "cpu_seconds": sum(r["cpu_seconds"] for r in budget.rows),
                    "wall_seconds": sum(r["wall_seconds"] for r in budget.rows),
                    "peak_rss_bytes": max(r["peak_rss_bytes"] for r in budget.rows),
                    "artifact_bytes_before_receipt": size(OUT) + size(REPORT),
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
