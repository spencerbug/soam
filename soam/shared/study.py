"""E1 v1+A1 development phase: fixed inventory, no retries or confirmation access."""

import argparse
import hashlib
import json
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import torch

from soam.shared.archive import InputStore, digest, verify_contract
from soam.shared.data import SharedTask
from soam.shared.evaluation import evaluate
from soam.shared.fitting import FitPlan, fit
from soam.shared.inference import choose_configs
from soam.shared.models import ROOT, Candidate, manifest
from soam.shared.runner import Budget, BudgetExceeded, Config, provenance


@dataclass(frozen=True)
class Limits:
    max_cpu_seconds: int = 14400
    max_wall_seconds: int = 28800
    max_rss_bytes: int = 2 * 1024**3
    max_artifact_bytes: int = 8 * 1024**3


def development_inventory():
    protocol = manifest()
    return [
        {
            "id": f"development-{m['id']}-c{config}-s{root}",
            "family": m["id"],
            "config": config,
            "root": root,
            "status": "pending",
            "base_cells": 60,
        }
        for m in protocol["models"]
        for config in (0, 1)
        for root in protocol["streams"]["development_roots"]
    ]


def check_calibration(path):
    path = Path(path)
    record = json.loads((path / "provenance.json").read_text())
    ledger = json.loads((path / "cost-ledger.json").read_text())
    status = json.loads((path / "status.json").read_text())
    if (
        status["status"] != "complete"
        or ledger.get("archive_revision") != "a1"
        or not ledger["feasible"]
        or not all(ledger["checks"].values())
    ):
        raise ValueError("passing completed A1 calibration required")
    if "soam/shared/study.py" not in record["source_files"]:
        raise ValueError("study entry point is absent from calibrated source")
    for name, expected in record["source_files"].items():
        if digest(ROOT / name) != expected:
            raise ValueError("source differs from calibration: " + name)
        committed = subprocess.run(
            ["git", "show", "HEAD:" + name], cwd=ROOT, capture_output=True, check=True
        ).stdout
        if hashlib.sha256(committed).hexdigest() != expected:
            raise ValueError("study source must be committed: " + name)
    verify_contract()
    return record, ledger, status


def atomic_arrays(budget, path, arrays):
    if path.exists():
        raise FileExistsError(path)
    temporary = path.with_name(path.name + ".tmp")
    budget.arrays(temporary, arrays)
    temporary.replace(path)
    budget.sizes[str(path)] = budget.sizes.pop(str(temporary))


def run_development(output, calibration):
    budget = Budget(Limits())
    accepted, cost, calibration_status = check_calibration(calibration)
    protocol = manifest()
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    # Count the selected calibration in the whole-study allocation. Historical
    # preflight attempts are added explicitly below, never discarded as free work.
    prior_statuses = [calibration_status]
    for name in (
        "reports/shared-population-harness/preflight-status.json",
        "reports/e1-archive-a1/preflight-status.json",
    ):
        prior_statuses.append(json.loads((ROOT / name).read_text()))
    budget.cpu_start -= sum(s["cpu_seconds"] for s in prior_statuses)
    budget.wall_start -= sum(s["wall_seconds"] for s in prior_statuses)
    for i, status in enumerate(prior_statuses):
        budget.sizes[f"prior-calibration-{i}"] = status["artifact_bytes"] + 65536
    store = InputStore(output / "input-objects", budget)
    rows = development_inventory()
    later_reason = "pending_development_screen"
    phase_started = None
    old_threads, old_deterministic = (
        torch.get_num_threads(),
        torch.are_deterministic_algorithms_enabled(),
    )

    def check():
        budget.check()
        if phase_started is not None and time.process_time() - phase_started > 4000:
            raise BudgetExceeded("development phase CPU ceiling exceeded")

    def save_inventory(emergency=False):
        budget.json(
            output / "inventory.json",
            {
                "development": rows,
                "planned_full_fit_instances": 119,
                "planned_full_cells": 27820,
                "later_phases": {
                    "confirmation_fits": 70,
                    "repeat_fits": 7,
                    "base_cells": 4620,
                    "diagnostic_cells": 20680,
                    "status": "not_started",
                    "reason": later_reason,
                },
            },
            emergency=emergency,
        )

    try:
        torch.set_num_threads(1)
        torch.use_deterministic_algorithms(True)
        meta = provenance(Config(archive_revision="a1"))
        meta.update(
            engineering_only=False,
            execution_phase="development",
            study_fits_planned=42,
            accepted_calibration_source=accepted["source_sha256"],
        )
        budget.json(output / "provenance.json", meta)
        budget.json(output / "protocol.json", protocol)
        budget.json(output / "limits.json", asdict(Limits()))
        budget.json(output / "accepted-calibration.json", cost)
        budget.json(output / "status.json", {"status": "running", "phase": "development"})
        save_inventory()
        task = SharedTask()
        normalization = task.normalization()
        budget.arrays(
            output / "normalization.npz",
            {k: v for k, v in normalization.items() if isinstance(v, torch.Tensor)},
        )
        budget.json(
            output / "normalization.json",
            {k: v for k, v in normalization.items() if not isinstance(v, torch.Tensor)},
        )
        budget.arrays(output / "projection.npz", {"matrix": task.projection})
        variance = float(normalization["variance"])
        phase_started = time.process_time()
        for row in rows:
            check()
            started = time.process_time()
            row["status"] = "running"
            save_inventory()
            path = output / "fits" / row["id"]
            checkpoints = {}
            progress = {"last_packet": None, "archived_batches": 0}

            def archive_batch(update, role, episodes, path=path, progress=progress):
                store.write(path / "data" / f"{update}-{role}", episodes)
                progress["last_packet"] = [update, role]
                progress["archived_batches"] += 1

            def checkpoint(stage, state, optimizer, path=path, checkpoints=checkpoints):
                atomic_arrays(budget, path / f"{stage}.npz", state)
                checkpoints[stage] = state
                if optimizer is not None:
                    arrays = {
                        f"{i}-{k}": v
                        for i, values in optimizer["state"].items()
                        for k, v in values.items()
                        if isinstance(v, torch.Tensor)
                    }
                    atomic_arrays(budget, path / f"{stage}-optimizer.npz", arrays)
                    budget.json(path / f"{stage}-optimizer.json", optimizer["param_groups"])

            cells = []
            try:
                model, record = fit(
                    row["family"],
                    row["root"],
                    row["config"],
                    plan=FitPlan(),
                    archive_batch=archive_batch,
                    checkpoint=checkpoint,
                    budget_check=check,
                )
                budget.json(path / "fit.json", record)
                pre = Candidate(row["family"], record["initialization_seed"])
                pre.load_state_dict(checkpoints["recall"])
                for condition, role, candidate in (
                    ("recall_pre", "recall", pre),
                    ("recall_final", "recall", model),
                    ("transition", "transition", model),
                ):
                    for index in range(20):
                        check()
                        episode = task.episode("development", row["root"], index, role)
                        cell_path = path / "cells" / f"{condition}-{index}"
                        store.write(cell_path / "inputs", (episode,))
                        arrays, result = evaluate(candidate, episode, variance)
                        budget.arrays(cell_path / "arrays.npz", arrays)
                        budget.json(cell_path / "record.json", result)
                        cells.append(
                            {
                                "condition": condition,
                                "index": index,
                                "status": "complete",
                                "metrics": result["metrics"],
                            }
                        )
                means = {
                    condition: float(
                        np.mean(
                            [c["metrics"][metric] for c in cells if c["condition"] == condition]
                        )
                    )
                    for condition, metric in (
                        ("recall_pre", "recall_nmse"),
                        ("recall_final", "recall_nmse"),
                        ("transition", "free8_nmse"),
                    )
                }
                row.update(status="complete", means=means, completed_cells=len(cells))
            except (FloatingPointError, RuntimeError) as error:
                if not isinstance(error, FloatingPointError) and not (
                    "non-finite" in str(error) and "norm" in str(error)
                ):
                    raise
                row.update(status="numerical_failure", error=str(error), completed_cells=len(cells))
                budget.json(
                    path / "failure.json",
                    {"exception": type(error).__name__, "message": str(error), **progress},
                )
                # No replacement fit or alternate configuration: retain all 60 rows.
                finished = {(c["condition"], c["index"]) for c in cells}
                cells.extend(
                    {
                        "condition": condition,
                        "index": i,
                        "status": "unavailable",
                        "reason": "numerical_failure",
                    }
                    for condition in ("recall_pre", "recall_final", "transition")
                    for i in range(20)
                    if (condition, i) not in finished
                )
            budget.json(path / "cells.json", cells)
            row["cpu_seconds"] = time.process_time() - started
            row["archived_batches"] = progress["archived_batches"]
            save_inventory()
            check()
            print(
                json.dumps(
                    {
                        "fit": row["id"],
                        "status": row["status"],
                        "completed": sum(r["status"] == "complete" for r in rows),
                        "cpu_seconds": row["cpu_seconds"],
                    }
                ),
                flush=True,
            )
        if all(r["status"] == "complete" for r in rows):
            values = {m["id"]: np.zeros((2, 3, 2)) for m in protocol["models"]}
            roots = protocol["streams"]["development_roots"]
            for row in rows:
                values[row["family"]][row["config"], roots.index(row["root"])] = [
                    row["means"]["transition"],
                    row["means"]["recall_final"],
                ]
            screen = choose_configs(values)
            screen["outcome"] = (
                "development_passed_confirmation_pending"
                if screen["confirmation_allowed"]
                else "inconclusive_development_screen_failed"
            )
        else:
            screen = {"confirmation_allowed": False, "outcome": "inconclusive_numerical_failures"}
        budget.json(output / "development-screen.json", screen)
        later_reason = screen["outcome"]
        save_inventory()
        budget.json(
            output / "status.json",
            {
                "status": "development_complete",
                "phase_cpu_seconds": time.process_time() - phase_started,
                **screen,
                **budget.measurements(),
            },
        )
        return screen
    except BaseException as error:
        for row in rows:
            if row["status"] in ("pending", "running"):
                row.update(status="not_completed", reason=type(error).__name__)
        save_inventory(emergency=True)
        budget.json(
            output / "status.json",
            {
                "status": "budget_exhausted"
                if isinstance(error, (BudgetExceeded, TimeoutError))
                else "invalid_execution",
                "exception": type(error).__name__,
                "message": str(error),
                "retries": 0,
                **budget.measurements(),
            },
            emergency=True,
        )
        raise
    finally:
        torch.set_num_threads(old_threads)
        torch.use_deterministic_algorithms(old_deterministic)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--calibration", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run_development(args.output, args.calibration), sort_keys=True))


if __name__ == "__main__":
    main()
