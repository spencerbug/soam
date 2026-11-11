"""Finite Study A phases with cumulative budgets and immutable confirmation receipt."""

import argparse
import dataclasses
import hashlib
import json
import platform
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch

from soam.gating.data import generate, normalization, seed, training_data
from soam.gating.diagnostics import diagnose
from soam.gating.engine import evaluate, fit
from soam.gating.models import Core
from soam.gating.statistics import summarize

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/protocols/study_a_v2.json"


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")
    temporary.replace(path)


def digest(value):
    h = hashlib.sha256()

    def visit(x):
        if dataclasses.is_dataclass(x):
            visit(dataclasses.asdict(x))
        elif isinstance(x, torch.Tensor):
            h.update(str((str(x.dtype), tuple(x.shape))).encode())
            h.update(x.detach().cpu().contiguous().numpy().tobytes())
        elif isinstance(x, dict):
            for k in sorted(x, key=str):
                h.update(str(k).encode())
                visit(x[k])
        elif isinstance(x, (tuple, list)):
            for v in x:
                visit(v)
        else:
            h.update(json.dumps(x, sort_keys=True, allow_nan=False).encode())

    visit(value)
    return h.hexdigest()


def source():
    files = list((ROOT / "soam").rglob("*.py")) + [
        MANIFEST,
        ROOT / "docs/STUDY_A_PROTOCOL_V2.md",
        ROOT / "docs/protocols/shared_population_v1.json",
        ROOT / "docs/SHARED_POPULATION_PROTOCOL.md",
        ROOT / "pyproject.toml",
        ROOT / "uv.lock",
        ROOT / "tests/test_gating.py",
    ]
    hashes = {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)
    }
    return {
        "files": hashes,
        "sha256": digest(hashes),
        "commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "git_status": subprocess.check_output(
            ["git", "status", "--short"], cwd=ROOT, text=True
        ).strip(),
        "python": sys.version,
        "torch": torch.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "device": "cpu",
        "threads": 1,
        "deterministic": True,
    }


class Budget:
    def __init__(self, output, manifest):
        self.output = output
        self.limits = manifest["limits"]
        self.cpu_start = 0.0
        self.wall_start = time.monotonic()
        self.last_scan = -100.0
        self.size = 0
        self.prior = (
            json.loads((output / "ledger.json").read_text())
            if (output / "ledger.json").exists()
            else {"cpu_seconds": 0.0, "wall_seconds": 0.0, "fit_attempts": 0, "phases": []}
        )
        self.other_output = (
            ROOT / manifest["prior_execution"] if manifest.get("prior_execution") else None
        )
        if self.other_output is not None and not (output / "ledger.json").exists():
            prior_path = self.other_output / "ledger.json"
            if (
                hashlib.sha256(prior_path.read_bytes()).hexdigest()
                != manifest["prior_ledger_sha256"]
            ):
                raise ValueError("prior execution allocation changed")
            if not (self.other_output / "closed.json").exists():
                raise ValueError("prior execution must be closed")
            self.prior = json.loads(prior_path.read_text())
        self.attempts = 0

    def check(self, *, reserve=True):
        cpu = self.prior["cpu_seconds"] + time.process_time() - self.cpu_start
        wall = self.prior["wall_seconds"] + time.monotonic() - self.wall_start
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (
            1 if sys.platform == "darwin" else 1024
        )
        if time.process_time() - self.last_scan > 10:
            self.size = sum(
                p.stat().st_size
                for base in (self.output, self.other_output)
                if base is not None
                for p in base.rglob("*")
                if p.is_file()
            )
            self.last_scan = time.process_time()
        limit = self.limits["cpu_seconds"] - (self.limits["reserve_cpu_seconds"] if reserve else 0)
        if (
            cpu > limit
            or wall > self.limits["wall_seconds"]
            or rss > self.limits["rss_bytes"]
            or self.size > self.limits["artifact_bytes"]
        ):
            raise TimeoutError(
                f"budget exhausted: CPU={cpu:.2f}, wall={wall:.2f}, RSS={rss}, artifacts={self.size}"
            )

    def attempt(self):
        self.check()
        if self.prior["fit_attempts"] + self.attempts >= self.limits["fit_attempts"]:
            raise TimeoutError("fit attempt ceiling")
        self.attempts += 1

    def finish(self, phase, status):
        self.check(reserve=False)
        cpu = time.process_time() - self.cpu_start
        wall = time.monotonic() - self.wall_start
        ledger = {
            **self.prior,
            "cpu_seconds": self.prior["cpu_seconds"] + cpu,
            "wall_seconds": self.prior["wall_seconds"] + wall,
            "fit_attempts": self.prior["fit_attempts"] + self.attempts,
            "artifact_bytes": sum(
                p.stat().st_size
                for base in (self.output, self.other_output)
                if base is not None
                for p in base.rglob("*")
                if p.is_file()
            ),
            "peak_rss_bytes": max(
                self.prior.get("peak_rss_bytes", 0),
                resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                * (1 if sys.platform == "darwin" else 1024),
            ),
            "phases": self.prior["phases"]
            + [
                {
                    "phase": phase,
                    "status": status,
                    "cpu_seconds": cpu,
                    "wall_seconds": wall,
                    "fit_attempts": self.attempts,
                }
            ],
        }
        dump(self.output / "ledger.json", ledger)
        return ledger


def evaluation_data(split, root, manifest):
    n = manifest["evaluation_episodes"]
    return tuple(
        generate(split, root, 0, role, batch=n, horizon=10 if role == "recall" else 32)[0]
        for role in ("recall", "transition")
    )


def run_fit(
    output,
    phase,
    root,
    name,
    config_index,
    m,
    data,
    ev,
    variance,
    budget,
    *,
    fixture=False,
    gate_mean=None,
):
    fitdir = output / phase / f"{root}-{name}-c{config_index}"
    fitdir.mkdir(parents=True, exist_ok=False)
    budget.attempt()
    dump(fitdir / "status.json", {"status": "running"})
    inventory = json.loads((output / "inventory.json").read_text())
    inventory.pop(f"{phase}/{root}/{name}/selected", None)
    inventory[f"{phase}/{root}/{name}/{config_index}"] = "running"
    dump(output / "inventory.json", inventory)
    kind, width = m["variants"][name]
    init = seed("fixture" if fixture else "train", root, 0, "initialization")
    model = Core(kind, width, init)
    try:
        result = fit(
            model,
            data,
            m["configs"][config_index],
            budget.check,
            development=ev if phase == "development" else None,
            variance=variance,
            checkpoints=tuple(m["fit"]["checkpoints"]),
        )
        metrics, paths = evaluate(model, *ev, variance)
        diag, arrays = (
            ({}, {})
            if phase in ("fixture", "development")
            else diagnose(model, root, variance, m, budget.check, gate_mean=gate_mean)
        )
        model_state = model.state_dict()
        numerical = {
            "checkpoint": digest(model_state),
            "optimizer": digest(result["optimizer_state"]),
            "trace": digest(result["trace"]),
            "input": digest(data),
            "evaluation_input": digest(ev),
            "paths": digest(paths),
            "diagnostics": digest(arrays),
            "metrics": digest(metrics),
            "diagnostic_metrics": digest(diag),
        }
        torch.save(
            {"model": model_state, "optimizer": result.pop("optimizer_state")},
            fitdir / "checkpoint.pt",
        )
        torch.save(paths, fitdir / "paths.pt")
        if arrays:
            torch.save(arrays, fitdir / "diagnostics.pt")
        record = {
            "root": root,
            "model": name,
            "config": config_index,
            "initialization_seed": init,
            "metrics": metrics,
            "diagnostics": diag,
            "costs": model.costs(),
            "fit_cpu": result["cpu_seconds"],
            "setup_cpu": result["setup_cpu_seconds"],
            "exposure": result["exposure"],
            "learning": result["learning"],
            "numerical": numerical,
            "alpha_mean": paths["free"]["alpha"].mean((0, 1)).tolist(),
            "trace": result["trace"],
        }
        dump(fitdir / "result.json", record)
        dump(fitdir / "status.json", {"status": "complete"})
        inventory[f"{phase}/{root}/{name}/{config_index}"] = "complete"
        dump(output / "inventory.json", inventory)
        print(
            json.dumps(
                {
                    "phase": phase,
                    "root": root,
                    "model": name,
                    "config": config_index,
                    "J": metrics["J"],
                    "cpu": result["cpu_seconds"],
                }
            ),
            flush=True,
        )
        budget.check()
        return record
    except BaseException as error:
        dump(fitdir / "status.json", {"status": "failed", "error": repr(error)})
        inventory[f"{phase}/{root}/{name}/{config_index}"] = "failed"
        dump(output / "inventory.json", inventory)
        raise


def run_phase(output, phase, m, budget):
    norm_path = output / "normalization.pt"
    if not norm_path.exists():
        torch.save(normalization(m["normalization_root"], m["normalization_samples"]), norm_path)
    norm = torch.load(norm_path, weights_only=False)
    variance = norm["variance"]
    if phase == "fixture":
        f = m["fixture"]
        data = training_data(
            f["root"],
            fixture=True,
            recall_updates=f["recall_updates"],
            joint_updates=f["joint_updates"],
            batch=f["batch"],
        )
        ev = evaluation_data("fixture", f["root"], m)
        records = []
        for name in m["variants"]:
            records.append(
                run_fit(
                    output, phase, f["root"], name, 0, m, data, ev, variance, budget, fixture=True
                )
            )
        # Conservative extrapolation: neural fitting dominates; reserve separate data/diagnostic costs.
        scale = (m["fit"]["recall_updates"] + m["fit"]["joint_updates"]) / (
            f["recall_updates"] + f["joint_updates"]
        )
        projection = (
            sum(
                r["setup_cpu"]
                + (r["fit_cpu"] - r["setup_cpu"]) * (1 if r["model"].startswith("L") else scale)
                for r in records
            )
            * 15
            * 1.5
            + 450
        )
        dump(
            output / "fixture/calibration.json",
            {
                "fit_cpu_projection_with_margin": projection,
                "remaining_cpu_limit": m["limits"]["cpu_seconds"]
                - m["limits"]["reserve_cpu_seconds"]
                - time.process_time(),
                "reference_batch": f["batch"],
                "scientific_batch": m["fit"]["batch"],
                "batch_cost_caveat": "small matrix calls are overhead dominated; development actual cost is mandatory second preflight",
                "records": [
                    {k: v for k, v in r.items() if k not in ("trace", "learning")} for r in records
                ],
            },
        )
        return
    if phase == "development":
        if json.loads((output / "fixture/status.json").read_text())["status"] != "complete":
            raise ValueError("completed fixture required")
        calibration = json.loads((output / "fixture/calibration.json").read_text())
        if calibration["fit_cpu_projection_with_margin"] > calibration["remaining_cpu_limit"]:
            raise TimeoutError("fixture projection exceeds ceiling")
        records = []
        for root in m["development_roots"]:
            budget.check()
            data = training_data(
                root,
                recall_updates=m["fit"]["recall_updates"],
                joint_updates=m["fit"]["joint_updates"],
                batch=m["fit"]["batch"],
            )
            torch.save(data, output / phase / f"train-{root}.pt")
            ev = evaluation_data("development", root, m)
            torch.save(ev, output / phase / f"evaluation-{root}.pt")
            for name in m["variants"]:
                for cfg in range(len(m["configs"])):
                    records.append(
                        run_fit(output, phase, root, name, cfg, m, data, ev, variance, budget)
                    )
        dump(output / phase / "results.json", records)
        return
    if phase == "freeze":
        records = json.loads((output / "development/results.json").read_text())
        selected = {}
        plateaus = {}
        gate_means = {}
        scores = {}
        for name in m["variants"]:
            configs = []
            for cfg in range(len(m["configs"])):
                rows = [r for r in records if r["model"] == name and r["config"] == cfg]
                if len(rows) != len(m["development_roots"]):
                    raise ValueError("incomplete development")
                configs.append(float(np.mean([r["metrics"]["J"] for r in rows])))
            cfg = int(np.argmin(configs))
            selected[name] = cfg
            scores[name] = configs
            rows = [r for r in records if r["model"] == name and r["config"] == cfg]
            before = np.mean([r["learning"][str(m["fit"]["checkpoints"][-2])]["J"] for r in rows])
            after = np.mean([r["learning"][str(m["fit"]["checkpoints"][-1])]["J"] for r in rows])
            plateaus[name] = float((before - after) / max(before, 1e-6))
            gate_means[name] = np.mean([r["alpha_mean"] for r in rows], axis=0).tolist()
        # Frozen before confirmation data are generated; no automatic alternate ablation selection.
        estimate = (
            sum(
                np.mean(
                    [
                        r["fit_cpu"]
                        for r in records
                        if r["model"] == name and r["config"] == selected[name]
                    ]
                )
                for name in m["variants"]
            )
            * 11
            * 1.5
            + 300
        )
        remaining = (
            m["limits"]["cpu_seconds"]
            - m["limits"]["reserve_cpu_seconds"]
            - budget.prior["cpu_seconds"]
            - time.process_time()
        )
        competence = (
            1e-6 < scores["FU38"][selected["FU38"]] < m["criteria"]["development_control_j"]
        )
        unresolved = any(
            plateaus[name] > m["criteria"]["late_improvement_limit"]
            for name in ("G32", "FU38", "R52", "R55")
        )
        receipt = {
            "protocol": m["protocol"],
            "version": m["version"],
            "selected": selected,
            "development_scores": scores,
            "late_relative_improvement": plateaus,
            "gate_means": gate_means,
            "competence_pass": competence,
            "optimization_unresolved": unresolved,
            "projected_confirmation_repeat_cpu_with_margin": estimate,
            "remaining_fit_cpu": remaining,
            "resource_pass": estimate < remaining,
            "source": source(),
            "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
            "normalization_sha256": digest(norm),
            "development_results_sha256": hashlib.sha256(
                (output / "development/results.json").read_bytes()
            ).hexdigest(),
            "criteria": m["criteria"],
            "rationale": "The 10% gain and absolute 0.005/0.01 guardrails retain the prior task-scale engineering interpretation; all candidate development scores and 1400-to-1600 slopes are recorded for auditing. No criterion is selected from confirmation. Optimization unresolved remains an attribution limitation, not permission to extend training.",
            "status": "frozen",
        }
        receipt["sha256"] = digest(receipt)
        dump(output / "freeze/receipt.json", receipt)
        print(
            json.dumps(
                {k: v for k, v in receipt.items() if k not in ("source", "gate_means")}, indent=2
            ),
            flush=True,
        )
        if not receipt["resource_pass"]:
            raise TimeoutError("confirmation projection exceeds remaining ceiling")
        return
    if phase in ("confirmation", "repeat"):
        receipt = json.loads((output / "freeze/receipt.json").read_text())
        check_receipt = dict(receipt)
        expected = check_receipt.pop("sha256")
        if (
            digest(check_receipt) != expected
            or receipt["source"]["sha256"] != source()["sha256"]
            or receipt["manifest_sha256"] != hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
        ):
            raise ValueError("confirmation source/receipt changed")
        if not receipt["resource_pass"]:
            raise ValueError("failed preflight")
        records = []
        roots = m["confirmation_roots"] if phase == "confirmation" else [m["repeat_root"]]
        for root in roots:
            budget.check()
            if phase == "repeat":
                data = torch.load(output / "confirmation" / f"train-{root}.pt", weights_only=False)
                ev = torch.load(
                    output / "confirmation" / f"evaluation-{root}.pt", weights_only=False
                )
            else:
                data = training_data(
                    root,
                    recall_updates=m["fit"]["recall_updates"],
                    joint_updates=m["fit"]["joint_updates"],
                    batch=m["fit"]["batch"],
                )
                torch.save(data, output / phase / f"train-{root}.pt")
                ev = evaluation_data("confirmation", root, m)
                torch.save(ev, output / phase / f"evaluation-{root}.pt")
            for name in m["variants"]:
                rec = run_fit(
                    output,
                    phase,
                    root,
                    name,
                    receipt["selected"][name],
                    m,
                    data,
                    ev,
                    variance,
                    budget,
                    gate_mean=torch.tensor(receipt["gate_means"][name]),
                )
                records.append(rec)
                if phase == "repeat":
                    old = json.loads(
                        (
                            output
                            / "confirmation"
                            / f"{root}-{name}-c{receipt['selected'][name]}"
                            / "result.json"
                        ).read_text()
                    )
                    if rec["numerical"] != old["numerical"]:
                        raise AssertionError(f"reproduction mismatch {name}")
        dump(output / phase / "results.json", records)
        if phase == "repeat":
            dump(
                output / phase / "reproduction.json",
                {
                    "exact": True,
                    "root": m["repeat_root"],
                    "models": list(m["variants"]),
                    "fields": list(records[0]["numerical"]),
                    "timing_excluded": True,
                },
            )
        return
    if phase == "report":
        records = json.loads((output / "confirmation/results.json").read_text())
        receipt = json.loads((output / "freeze/receipt.json").read_text())
        stats = summarize(records, m, receipt)
        dump(output / "report/statistics.json", stats)
        from soam.gating.render import render

        render(output, stats, records, m, receipt)
        return
    raise ValueError("unknown phase")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase",
        choices=["fixture", "development", "freeze", "confirmation", "repeat", "report"],
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    m = json.loads(MANIFEST.read_text())
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    phase_dir = output / args.phase
    phase_dir.mkdir(exist_ok=False)
    current = source()
    if (output / "source.json").exists():
        previous = json.loads((output / "source.json").read_text())
        if previous["sha256"] != current["sha256"]:
            raise ValueError(
                "source changed: preserve attempt and use a fresh reviewed execution identity"
            )
    else:
        dump(output / "source.json", current)
        dump(output / "manifest.json", m)
        inventory = {}
        for phase, roots, configs in [
            ("fixture", [m["fixture"]["root"]], [0]),
            ("development", m["development_roots"], [0, 1]),
            ("confirmation", m["confirmation_roots"], ["selected"]),
            ("repeat", [m["repeat_root"]], ["selected"]),
        ]:
            for root in roots:
                for name in m["variants"]:
                    for cfg in configs:
                        inventory[f"{phase}/{root}/{name}/{cfg}"] = "unexecuted"
        dump(output / "inventory.json", inventory)
        for relative in current["files"]:
            dest = output / "source" / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, dest)
    budget = Budget(output, m)
    status = "failed"
    dump(
        phase_dir / "status.json",
        {"status": "running", "phase": args.phase, "source": current["sha256"]},
    )
    try:
        run_phase(output, args.phase, m, budget)
        status = "complete"
    except BaseException as error:
        dump(
            phase_dir / "status.json",
            {"status": "failed", "error": repr(error), "phase": args.phase},
        )
        raise
    finally:
        # Preserve spent resources even if a scientific or resource check failed.
        try:
            ledger = budget.finish(args.phase, status)
        except TimeoutError:
            budget.check = lambda **kwargs: None
            ledger = budget.finish(args.phase, status)
        if status == "complete":
            dump(
                phase_dir / "status.json", {"status": status, "phase": args.phase, "ledger": ledger}
            )


if __name__ == "__main__":
    main()
