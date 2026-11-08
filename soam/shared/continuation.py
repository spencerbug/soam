"""E1 v1+A1 continuation: prepare readiness, verify fixtures, or explicitly execute.

The default is read-only readiness preparation. Scientific execution is a separate
mode and consumes a single-use receipt. No command resumes or retries failed work.
"""

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

import torch

from soam.platform.core import fingerprint
from soam.platform.runner import read_arrays
from soam.shared.archive import InputStore, digest
from soam.shared.data import SharedTask
from soam.shared.execution import FAMILIES, compare_repeat, execute_root
from soam.shared.models import ROOT, manifest
from soam.shared.runner import Budget, BudgetExceeded, Config, provenance
from soam.shared.study import Limits, check_calibration
from soam.shared.study_summary import aggregate, root_summary

DEVELOPMENT = ROOT / "runs/e1-development-v1-a1"
DEVELOPMENT_ARCHIVE = "3780bbb310ee7bc7d9b9ebf70afe58d0b39e0565a7234c704ea361f288d7c4fd"
DEVELOPMENT_SOURCE = "e0585121bcd98d1bf1b49e6d21858a20279cd97f17849a91e4d1291c25f652bb"
HISTORICAL_FIXTURES = (
    "shared-harness-v1",
    "shared-harness-v1-final",
    "shared-a1-fixture",
    "shared-a1-fixture-fixed",
)


def read(path):
    return json.loads(Path(path).read_text())


def load_normalization(path):
    values = {**read_arrays(path / "normalization.npz"), **read(path / "normalization.json")}
    if fingerprint({"samples": values["samples"]}) != values["sha256"]:
        raise ValueError("normalization sample digest mismatch")
    mean = values["samples"].double().mean(0)
    variance = (values["samples"].double() - mean).square().mean().clamp_min(1e-6)
    if not torch.equal(mean, values["mean"]) or not torch.equal(variance, values["variance"]):
        raise ValueError("normalization statistics mismatch")
    return values


def tree_identity(path):
    files, size = {}, 0
    for file in sorted(path.rglob("*")):
        if file.is_symlink():
            raise ValueError("symlink in sealed archive")
        if file.is_file():
            files[str(file.relative_to(path))] = digest(file)
            size += file.stat().st_size
    return {
        "sha256": hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest(),
        "files": len(files),
        "bytes": size,
    }


def check_dependencies():
    for ticket, decision in (("050", None), ("061", "proceed")):
        path = next((ROOT / "tickets").glob(f"SOAM-{ticket}-*.md"))
        fields = dict(
            line.split(": ", 1) for line in path.read_text().split("---")[1].strip().splitlines()
        )
        if fields["status"] != '"done"' or json.loads(fields["decision"]) != decision:
            raise ValueError("unsatisfied prerequisite: SOAM-" + ticket)


def audit_development():
    """Pin the fully audited archive; never inspect/generate confirmation inputs."""
    check_dependencies()
    identity = tree_identity(DEVELOPMENT)
    if identity["sha256"] != DEVELOPMENT_ARCHIVE:
        raise ValueError("development archive differs from reviewed audit")
    record = read(DEVELOPMENT / "provenance.json")
    if record["source_sha256"] != DEVELOPMENT_SOURCE:
        raise ValueError("wrong development source")
    for name, expected in record["source_files"].items():
        committed = subprocess.run(
            ["git", "show", record["commit"] + ":" + name],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        if hashlib.sha256(committed).hexdigest() != expected or digest(ROOT / name) != expected:
            raise ValueError("development scientific source changed: " + name)
    screen = read(DEVELOPMENT / "development-screen.json")
    status = read(DEVELOPMENT / "status.json")
    if status["status"] != "development_complete" or not screen["confirmation_allowed"]:
        raise ValueError("development competence/floor screen does not permit confirmation")
    return {
        "archive": identity,
        "source_commit": record["commit"],
        "source_sha256": record["source_sha256"],
        "screen": screen,
        "status": status,
    }


def component(path, label):
    status = read(path / "status.json")
    identity = tree_identity(path)
    return {
        "label": label,
        "path": str(path.relative_to(ROOT)),
        "archive": identity,
        "cpu_seconds": status["cpu_seconds"],
        "wall_seconds": status["wall_seconds"],
        "artifact_bytes": max(identity["bytes"], status["artifact_bytes"]) + 65536,
        "peak_rss_bytes": status["peak_rss_bytes"],
        "status": status["status"],
    }


def current_calibration(path):
    record, ledger, status = check_calibration(path)
    current = provenance(Config(archive_revision="a1"))
    if (
        record["source_files"] != current["source_files"]
        or record["source_sha256"] != current["source_sha256"]
    ):
        raise ValueError("calibration omits current source files")
    for key in ("python", "torch", "numpy", "machine", "platform", "device", "dtype"):
        if record[key] != current[key]:
            raise ValueError("calibration runtime differs: " + key)
    if record["torch_threads"] != 1 or not record["deterministic_algorithms"]:
        raise ValueError("calibration numerical settings differ")
    if ledger["inventory"] != manifest()["inventory"] or ledger["optimizer_updates"] != 0:
        raise ValueError("wrong calibration inventory or fitted calibration")
    if set(ledger["checks"]) != {
        "per_fit",
        "development",
        "confirmation",
        "repeat",
        "total_cpu",
        "total_wall",
        "artifact_bytes",
        "peak_rss_with_margin",
    }:
        raise ValueError("incomplete calibration checks")
    return record, ledger, status


class ContinuationBudget(Budget):
    """Carry prior costs once and enforce per-phase plus total/overhead ceilings."""

    def __init__(self, carried):
        super().__init__(Limits())
        self.carried = carried
        self.cpu_start -= carried["cpu_seconds"]
        self.wall_start -= carried["wall_seconds"]
        self.sizes["carried-artifacts"] = carried["artifact_bytes"]
        self.phases = {"confirmation": 0.0, "repeat": 0.0}
        self.phase = None
        self.phase_start = None

    def measurements(self):
        result = super().measurements()
        result["peak_rss_bytes"] = max(result["peak_rss_bytes"], self.carried["peak_rss_bytes"])
        return result

    def begin(self, phase):
        if self.phase is not None:
            raise ValueError("phase already running")
        self.phase, self.phase_start = phase, time.process_time()

    def end(self):
        self.phases[self.phase] += time.process_time() - self.phase_start
        self.phase = self.phase_start = None

    def phase_totals(self):
        values = dict(self.phases)
        if self.phase is not None:
            values[self.phase] += time.process_time() - self.phase_start
        return values

    def check(self):
        super().check()
        phases = self.phase_totals()
        for name, limit in (("confirmation", 8000), ("repeat", 1200)):
            if phases[name] > limit:
                raise BudgetExceeded(name + " phase CPU ceiling exceeded")
        overhead = (
            self.measurements()["cpu_seconds"]
            - self.carried["development_cpu_seconds"]
            - sum(phases.values())
        )
        if overhead > 1200:
            raise BudgetExceeded("cumulative overhead CPU ceiling exceeded")
        if self.measurements()["artifact_bytes"] > self.config.max_artifact_bytes:
            raise BudgetExceeded("cumulative artifact ceiling exceeded")


def prepare(output, calibration, fixture_paths):
    started, wall = time.process_time(), time.perf_counter()
    development = audit_development()
    record, ledger, _ = current_calibration(calibration)
    if not fixture_paths:
        raise ValueError("at least one continuation fixture is required")
    fixtures = [Path(p).resolve() for p in fixture_paths]
    if len(set(fixtures)) != len(fixtures):
        raise ValueError("duplicate charged fixture paths")
    # The last fixture must verify this exact source. Earlier failed attempts are
    # retained and charged, never disguised as scientific retries.
    last = fixtures[-1]
    result = read(last / "result.json")
    if (
        read(last / "status.json")["status"] != "complete"
        or not result["exact_repeat"]
        or result["cells_per_root"] != 230
        or result["confirmation_exposure"] != 0
        or read(last / "provenance.json")["source_sha256"] != record["source_sha256"]
    ):
        raise ValueError("current-source passing continuation fixture required")
    components = [component(ROOT / "runs" / name, name) for name in HISTORICAL_FIXTURES]
    components += [component(p, "continuation-fixture") for p in fixtures]
    components += [component(Path(calibration).resolve(), "continuation-calibration")]
    dev = development["status"]
    carried = {
        key: dev[key] + sum(c[key] for c in components)
        for key in ("cpu_seconds", "wall_seconds", "artifact_bytes")
    }
    carried["cpu_seconds"] += time.process_time() - started
    carried["wall_seconds"] += time.perf_counter() - wall
    carried["peak_rss_bytes"] = max(
        dev["peak_rss_bytes"], *(c["peak_rss_bytes"] for c in components)
    )
    carried["development_cpu_seconds"] = dev["phase_cpu_seconds"]
    # Conservative remaining feasibility: carry observed prefix in addition to the
    # complete A1 storage projection, plus the unchanged full overhead allowance.
    projected = {
        "cpu_seconds": carried["cpu_seconds"]
        + sum(
            ledger["projections"]["cpu"]["phases_with_margin"][p]
            for p in ("confirmation", "repeat", "overhead")
        ),
        "wall_seconds": carried["wall_seconds"]
        + sum(
            ledger["projections"]["wall"]["phases_with_margin"][p]
            for p in ("confirmation", "repeat", "overhead")
        ),
        "artifact_bytes": carried["artifact_bytes"]
        + ledger["projected_artifact_bytes_with_margin"],
    }
    for name, limit in (
        ("cpu_seconds", 14400),
        ("wall_seconds", 28800),
        ("artifact_bytes", 8 * 1024**3),
    ):
        if projected[name] > limit:
            raise BudgetExceeded("remaining feasibility failed: " + name)
    budget = ContinuationBudget(carried)
    budget.check()
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    receipt = {
        "version": "e1-v1-a1-continuation-1",
        "ready": True,
        "confirmation_exposure": 0,
        "development": development,
        "calibration": str(Path(calibration).resolve().relative_to(ROOT)),
        "calibration_source": record["source_sha256"],
        "components": components,
        "carried": carried,
        "remaining_projection_with_margin": projected,
        "planned_confirmation_fits": 70,
        "planned_repeat_fits": 7,
        "planned_remaining_cells": 25300,
    }
    budget.json(output / "readiness.json", receipt)
    budget.json(
        output / "status.json", {"status": "ready_confirmation_unopened", **budget.measurements()}
    )
    return receipt


def continuation_inventory(fixture=False):
    roots = [9001] if fixture else manifest()["streams"]["confirmation_roots"]
    repeat = 9001 if fixture else manifest()["streams"]["repeat_root"]
    return [
        {
            "phase": phase,
            "root": root,
            "fits": 7,
            "cells": 230 if fixture else 2300,
            "status": "pending",
        }
        for phase, seeds in (("confirmation", roots), ("repeat", [repeat]))
        for root in seeds
    ]


def run(output, *, fixture=False, readiness=None):
    started, wall = time.process_time(), time.perf_counter()
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    old = torch.get_num_threads(), torch.are_deterministic_algorithms_enabled()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    try:
        if fixture:
            budget = Budget(Config(archive_revision="a1"))
            configs = {family: 0 for family in FAMILIES}
            normalization = SharedTask().normalization()
        else:
            if readiness is None:
                raise ValueError("explicit reviewed readiness receipt required")
            receipt_path = Path(readiness)
            if (receipt_path / "execution-claim.json").exists():
                raise FileExistsError("readiness receipt already consumed; no retries")
            receipt = read(receipt_path / "readiness.json")
            if not receipt["ready"] or receipt["confirmation_exposure"] != 0:
                raise ValueError("unopened ready receipt required")
            dev = audit_development()
            record, _, _ = current_calibration(ROOT / receipt["calibration"])
            if (
                dev != receipt["development"]
                or record["source_sha256"] != receipt["calibration_source"]
            ):
                raise ValueError("readiness inputs changed")
            for item in receipt["components"]:
                if tree_identity(ROOT / item["path"]) != item["archive"]:
                    raise ValueError("charged prior artifact changed: " + item["path"])
            carried = dict(receipt["carried"])
            carried["cpu_seconds"] += time.process_time() - started
            carried["wall_seconds"] += time.perf_counter() - wall
            # Include readiness metadata without charging its inherited costs twice.
            carried["artifact_bytes"] += tree_identity(receipt_path)["bytes"] + 65536
            budget = ContinuationBudget(carried)
            configs = dev["screen"]["selected_configs"]
            normalization = load_normalization(DEVELOPMENT)
        output.mkdir(parents=True, exist_ok=False)
        if not fixture:
            # Exclusive claim prevents the same frozen continuation being started
            # twice under different output names. Never unlink it after failure.
            with (receipt_path / "execution-claim.json").open("x") as claim:
                json.dump(
                    {"output": str(output.resolve()), "source": record["source_sha256"]}, claim
                )
        rows = continuation_inventory(fixture)
        store = InputStore(output / "input-objects", budget)
        meta = provenance(Config(archive_revision="a1"))
        meta.pop("study_fits", None)
        meta.update(
            engineering_only=fixture,
            execution_phase="continuation",
            study_fits_planned=0 if fixture else 77,
            confirmation_exposure=0 if fixture else "recorded_per_root_in_inventory",
        )
        budget.json(output / "provenance.json", meta)
        budget.arrays(
            output / "normalization.npz",
            {k: v for k, v in normalization.items() if isinstance(v, torch.Tensor)},
        )
        budget.json(
            output / "config.json",
            {
                "fixture": fixture,
                "selected_configs": configs,
                "normalization": {
                    k: v for k, v in normalization.items() if not isinstance(v, torch.Tensor)
                },
                "inventory": manifest()["inventory"],
                "budget": manifest()["budget"],
            },
        )
        budget.json(output / "status.json", {"status": "running", "fixture_only": fixture})
        budget.json(output / "inventory.json", rows)
        root_summaries, original, repeat_result = {}, None, None
        try:
            for row in rows:
                if not fixture:
                    budget.begin(row["phase"])
                budget.check()
                row["status"] = "running"
                budget.json(output / "inventory.json", rows)
                target = output / row["phase"] / str(row["root"])
                restore = (
                    output / "confirmation" / str(row["root"]) if row["phase"] == "repeat" else None
                )
                if restore is not None and not all(
                    c["status"] == "complete" for c in original["cells"].values()
                ):
                    row.update(
                        status="unexecuted", reason="original_seed_incomplete_no_rescue_repeat"
                    )
                    if not fixture:
                        budget.end()
                    continue
                result = execute_root(
                    target,
                    store,
                    budget,
                    budget.check,
                    configs,
                    float(normalization["variance"]),
                    row["root"],
                    fixture=fixture,
                    restore=restore,
                )
                summary = root_summary(target, result, store, 2 if fixture else 20)
                budget.json(target / "summary.json", summary)
                if row["phase"] == "confirmation":
                    root_summaries[row["root"]] = summary
                    if row["root"] == (9001 if fixture else 11):
                        original = result
                else:
                    repeat_result = compare_repeat(restore, target, store, budget.check)
                    budget.json(output / "reproduction.json", repeat_result)
                row.update(
                    status="complete" if summary["complete"] else "numerical_failure",
                    completed_cells=summary["cell_status_counts"].get("complete", 0),
                )
                if not fixture:
                    budget.end()
                budget.json(output / "inventory.json", rows)
                budget.check()
                print(
                    json.dumps(
                        {"phase": row["phase"], "root": row["root"], "status": row["status"]}
                    ),
                    flush=True,
                )
            if fixture:
                final = {
                    "fixture_only": True,
                    "confirmation_exposure": 0,
                    "study_fits": 0,
                    "fixture_fits": 14,
                    "cells_per_root": 230,
                    **repeat_result,
                }
            else:
                final = aggregate(root_summaries)
                final["reproduction"] = repeat_result or {
                    "exact_repeat": False,
                    "reason": "original_seed_incomplete",
                }
                final["primary_reference"] = dev["screen"]["primary_reference"]
                # A mid-run source change invalidates the execution identity too.
                current_calibration(ROOT / receipt["calibration"])
            budget.json(output / "result.json", final)
            budget.json(
                output / "status.json",
                {
                    "status": "complete",
                    "fixture_only": fixture,
                    "phase_cpu_seconds": {} if fixture else budget.phase_totals(),
                    **budget.measurements(),
                },
            )
            return final
        except BaseException as error:
            for row in rows:
                if row["status"] in ("pending", "running"):
                    row.update(status="unexecuted_or_partial", reason=type(error).__name__)
            budget.json(output / "inventory.json", rows, emergency=True)
            budget.json(
                output / "status.json",
                {
                    "status": "budget_exhausted"
                    if isinstance(error, (BudgetExceeded, TimeoutError))
                    else "invalid_execution",
                    "exception": type(error).__name__,
                    "message": str(error),
                    "retries": 0,
                    "phase_cpu_seconds": {} if fixture else budget.phase_totals(),
                    **budget.measurements(),
                },
                emergency=True,
            )
            raise
    finally:
        torch.set_num_threads(old[0])
        torch.use_deterministic_algorithms(old[1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("prepare", "fixture", "execute"), default="prepare")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--calibration", type=Path)
    parser.add_argument("--fixture", type=Path, action="append", dest="fixtures")
    parser.add_argument("--readiness", type=Path)
    args = parser.parse_args()
    if args.mode == "prepare":
        if args.calibration is None:
            parser.error("--calibration required for prepare")
        result = prepare(args.output, args.calibration, args.fixtures)
        print(json.dumps({"ready": result["ready"], "confirmation_exposure": 0}))
    else:
        result = run(args.output, fixture=args.mode == "fixture", readiness=args.readiness)
        print(
            json.dumps(
                {k: v for k, v in result.items() if k not in ("root_summaries",)}, sort_keys=True
            )
        )


if __name__ == "__main__":
    main()
