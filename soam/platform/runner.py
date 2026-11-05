"""Execute and exactly repeat the bounded SOAM-048 engineering fixture matrix."""

import argparse
import hashlib
import io
import json
import resource
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import torch

from soam.evaluation.provenance import capture
from soam.platform.core import (
    BACKENDS,
    Command,
    ModelSpec,
    Observation,
    SuppliedDynamics,
    fingerprint,
    freeze,
    model_fingerprint,
    predict,
)
from soam.platform.evaluation import evaluate
from soam.platform.tasks import TASKS, Episode, EvaluationTargets, seed_for

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/RECURRENT_PLATFORM_CONTRACT.md"
CONTRACT_HASH = "4a30165d4399198cc42ca5d2cc82a295718109d511fb77e86bf5ede6116e9f61"


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rss_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform == "darwin" else value * 1024)


@dataclass(frozen=True)
class FixtureConfig:
    tasks: tuple = ("rotation", "translation")
    backends: tuple = ("leaky", "linear")
    seed: int = 9001
    split: str = "fixture"
    learning: str = "supplied"
    threads: int = 1
    max_cpu_seconds: int = 60
    max_wall_seconds: int = 120
    max_rss_bytes: int = 1024**3
    max_artifact_bytes: int = 256 * 1024**2

    def validate(self):
        if self.split != "fixture" or self.learning != "supplied":
            raise ValueError("fixture-only runner rejects fitting, online writes and study splits")
        if (
            type(self.seed) is not int
            or self.seed != 9001
            or type(self.threads) is not int
            or self.threads != 1
        ):
            raise ValueError("fixture seed 9001 and one thread required")
        for names, registry in ((self.tasks, TASKS), (self.backends, BACKENDS)):
            if not isinstance(names, (tuple, list)) or len(names) != 2 or len(set(names)) != 2:
                raise ValueError("exactly two distinct registered fixtures required")
            if any(name not in registry for name in names):
                raise ValueError("unknown registered fixture")
        for name, ceiling in (
            ("max_cpu_seconds", 60),
            ("max_wall_seconds", 120),
            ("max_rss_bytes", 1024**3),
            ("max_artifact_bytes", 256 * 1024**2),
        ):
            value = getattr(self, name)
            if type(value) is not int or not 0 < value <= ceiling:
                raise ValueError("invalid fixture budget: " + name)
        if self.max_artifact_bytes < 65536:
            raise ValueError("artifact budget must reserve 64 KiB for failure status")
        return self

    def to_dict(self):
        return asdict(self)


class BudgetExceeded(RuntimeError):
    pass


class Budget:
    """Combined original/repeat allocation, with cooperative operation boundaries."""

    def __init__(self, config):
        self.config = config
        self.cpu_start, self.wall_start = time.process_time(), time.perf_counter()
        self.sizes = {}

    def measurements(self):
        return {
            "cpu_seconds": time.process_time() - self.cpu_start,
            "wall_seconds": time.perf_counter() - self.wall_start,
            "peak_rss_bytes": rss_bytes(),
            "artifact_bytes": sum(self.sizes.values()),
        }

    def check(self):
        for metric, limit in (
            ("cpu_seconds", "max_cpu_seconds"),
            ("wall_seconds", "max_wall_seconds"),
            ("peak_rss_bytes", "max_rss_bytes"),
        ):
            if self.measurements()[metric] > getattr(self.config, limit):
                raise BudgetExceeded(metric + " budget exhausted")

    def write(self, path, payload, emergency=False):
        if not emergency:
            self.check()
        path = Path(path)
        size = sum(self.sizes.values()) - self.sizes.get(str(path), 0) + len(payload)
        reserve = 0 if emergency else 65536
        if size > self.config.max_artifact_bytes - reserve:
            raise BudgetExceeded("artifact byte budget exhausted before write")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        self.sizes[str(path)] = len(payload)
        if not emergency:
            self.check()

    def json(self, path, value, emergency=False):
        self.write(
            path,
            (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode(),
            emergency,
        )

    def arrays(self, path, values):
        # Check uncompressed payload before allocating serialization workspace.
        logical = sum(v.numel() * v.element_size() for v in values.values())
        if logical + sum(self.sizes.values()) + 65536 > self.config.max_artifact_bytes:
            raise BudgetExceeded("array serialization reservation exceeds artifact budget")
        out = io.BytesIO()
        np.savez_compressed(out, **{k: v.detach().cpu().numpy() for k, v in values.items()})
        self.write(path, out.getvalue())


def read_arrays(path):
    with np.load(path, allow_pickle=False) as source:
        return {name: torch.from_numpy(source[name].copy()) for name in source.files}


def restore_episode(path):
    a, t = read_arrays(path / "observations.npz"), read_arrays(path / "targets.npz")
    observations = tuple(
        Observation(*(a[key][i].clone() for key in ("z", "valid", "cue", "cue_valid")))
        for i in range(len(a["z"]))
    )
    record = json.loads((path / "record.json").read_text())
    return Episode(
        observations,
        tuple(Command(x.clone()) for x in a["actions"]),
        EvaluationTargets(t["features"], t["world"]),
        record["stream_seeds"],
    )


def provenance(config):
    result = capture(ROOT, config)
    result["source_files"][str(CONTRACT.relative_to(ROOT))] = file_hash(CONTRACT)
    result["source_sha256"] = hashlib.sha256(
        json.dumps(result["source_files"], sort_keys=True).encode()
    ).hexdigest()
    result.update(
        contract_sha256=file_hash(CONTRACT),
        fixture_only=True,
        training_exposure=0,
        development_exposure=0,
        confirmation_exposure=0,
        torch_threads=torch.get_num_threads(),
        deterministic_algorithms=torch.are_deterministic_algorithms_enabled(),
        default_dtype=str(torch.get_default_dtype()),
        metric_dtype="float64",
    )
    return result


def run_cell(task, model, episode, path, budget, metadata):
    try:
        return _run_cell(task, model, episode, path, budget, metadata)
    except BaseException as exc:
        budget.json(
            path / "failure.json",
            {
                **metadata,
                "stream_seeds": episode.stream_seeds,
                "status": "budget_exhausted" if isinstance(exc, BudgetExceeded) else "invalid",
                "exception": type(exc).__name__,
                "reason": str(exc),
                "scientific_result": False,
            },
            emergency=True,
        )
        raise


def _run_cell(task, model, episode, path, budget, metadata):
    budget.check()
    start_cpu, start_wall = time.process_time(), time.perf_counter()
    budget.arrays(path / "observations.npz", episode.observed_arrays())
    budget.arrays(
        path / "targets.npz", {"features": episode.targets.features, "world": episode.targets.world}
    )
    budget.arrays(path / "checkpoint.npz", model.state_dict())
    arrays, record = evaluate(model, task, episode)
    record.update(metadata, stream_seeds=episode.stream_seeds)
    budget.arrays(path / "trajectories.npz", arrays)
    budget.json(path / "record.json", record)
    budget.json(
        path / "timing.json",
        {
            "cpu_seconds": time.process_time() - start_cpu,
            "wall_seconds": time.perf_counter() - start_wall,
        },
    )
    return record


class NonfiniteFixture(SuppliedDynamics):
    def advance(self, state, command, *, clamp_units=None):
        return torch.full_like(state, float("nan"))


def expected_failure(path, budget):
    model = NonfiniteFixture(ModelSpec(8, 1), seed_for(9001, 0, "failure/model"))
    state = model.initial_state(1)
    command = Command(torch.zeros(1, 1))
    before, state_before = model_fingerprint(model), fingerprint({"state": state})
    injected = model.advance(state, command)
    snapshot = freeze(model, state)
    try:
        predict(snapshot, (command,))
    except FloatingPointError as exc:
        result = {
            "status": "invalid",
            "expected": True,
            "exception": type(exc).__name__,
            "reason": str(exc),
            "model_unchanged": before == model_fingerprint(model),
            "live_state_unchanged": state_before == fingerprint({"state": state}),
            "advance_calls": 2,
            "readout_attempts": 1,
            "scientific_result": False,
        }
    else:
        raise AssertionError("nonfinite output was not rejected")
    if not result["model_unchanged"] or not result["live_state_unchanged"]:
        raise AssertionError("failed prediction modified its source")
    budget.arrays(path / "injected.npz", {"nonfinite_output": injected})
    budget.json(path / "failure.json", result)
    return result


def compare_runs(original, repeat):
    original, repeat = Path(original), Path(repeat)
    count = 0
    for name in ("config.json", "manifest.json", "deterministic.json"):
        if json.loads((original / name).read_text()) != json.loads((repeat / name).read_text()):
            raise AssertionError("reproduction record differs: " + name)
    a, b = [json.loads((p / "provenance.json").read_text()) for p in (original, repeat)]
    for key in (
        "source_sha256",
        "contract_sha256",
        "python",
        "torch",
        "numpy",
        "platform",
        "machine",
        "torch_threads",
        "deterministic_algorithms",
        "default_dtype",
    ):
        if a[key] != b[key]:
            raise AssertionError("reproduction environment/source differs: " + key)
    paths = sorted(p.relative_to(original) for p in original.rglob("*.npz"))
    if paths != sorted(p.relative_to(repeat) for p in repeat.rglob("*.npz")):
        raise AssertionError("reproduction array inventory differs")
    for path in paths:
        left, right = read_arrays(original / path), read_arrays(repeat / path)
        if left.keys() != right.keys():
            raise AssertionError("reproduction array keys differ")
        for key in left:
            # NaN equality applies only to the explicitly injected failure artifact.
            same = np.array_equal(
                left[key].numpy(), right[key].numpy(), equal_nan=path.name == "injected.npz"
            )
            if not same:
                raise AssertionError(f"reproduction array differs: {path}:{key}")
            count += 1
    return {
        "exact_numeric_match": True,
        "array_files": len(paths),
        "arrays": count,
        "excluded": ["timing", "RSS", "PID", "timestamps", "NPZ container bytes"],
        "independent_statistical_sample": False,
    }


def run_pass(config, output, budget, repeat_from=None):
    output.mkdir()
    budget.json(output / "config.json", config.to_dict())
    manifest = {
        "version": 1,
        "purpose": "engineering fixtures only",
        "contract": CONTRACT_HASH,
        "seed": 9001,
        "episode_indices": [0, 1],
        "transitions": 3,
        "width": 8,
        "tasks": list(config.tasks),
        "backends": list(config.backends),
        "projection_seed": 1729,
        "fitted_models": 0,
        "expected_invalid_cases": 1,
    }
    budget.json(output / "manifest.json", manifest)
    prov = provenance(config)
    budget.json(output / "provenance.json", prov)
    rows = []
    for task_name in config.tasks:
        task = TASKS[task_name]()
        for backend in config.backends:
            for index in range(2):
                identity = f"{task_name}-{backend}-{index}"
                seed = seed_for(config.seed, index, f"initialization/{task_name}/{backend}")
                model = BACKENDS[backend](
                    ModelSpec(task.features, task.actions, kind=backend), seed
                )
                if repeat_from:
                    episode = restore_episode(repeat_from / identity)
                    # Verify seeded supplied buffers as well as loading immutable archived ones.
                    weights = read_arrays(repeat_from / identity / "checkpoint.npz")
                    if fingerprint(weights) != fingerprint(model.state_dict()):
                        raise AssertionError("supplied initialization changed")
                    model.load_state_dict(weights, strict=True)
                else:
                    episode = task.episode(config.split, config.seed, index)
                rows.append(
                    run_cell(
                        task,
                        model,
                        episode,
                        output / identity,
                        budget,
                        {
                            "id": identity,
                            "task": task_name,
                            "backend": backend,
                            "seed": config.seed,
                            "episode": index,
                            "initialization_seed": seed,
                            "split": "fixture",
                            "model_spec": asdict(model.spec),
                        },
                    )
                )
    failure = expected_failure(output / "expected-failure", budget)
    budget.json(output / "deterministic.json", {"cells": rows, "expected_failure": failure})
    if provenance(config)["source_sha256"] != prov["source_sha256"]:
        raise RuntimeError("source changed during run")
    budget.check()
    return rows


def run_suite(config, output):
    config.validate()
    if file_hash(CONTRACT) != CONTRACT_HASH:
        raise ValueError("platform contract changed; version/review before running")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    budget = Budget(config)
    status = {
        "status": "running",
        "phase": "original",
        "fixture_only": True,
        "empirical_gate_passed": False,
        "fitted_models": 0,
    }
    old_threads = torch.get_num_threads()
    old_determinism = torch.are_deterministic_algorithms_enabled()
    old_warn = torch.is_deterministic_algorithms_warn_only_enabled()
    old_dtype = torch.get_default_dtype()
    try:
        torch.set_num_threads(1)
        torch.use_deterministic_algorithms(True)
        torch.set_default_dtype(torch.float32)
        budget.json(output / "status.json", status, emergency=True)
        rows = run_pass(config, output / "original", budget)
        status["phase"] = "repeat"
        budget.json(output / "status.json", status, emergency=True)
        run_pass(config, output / "repeat", budget, output / "original")
        reproduction = compare_runs(output / "original", output / "repeat")
        budget.json(output / "reproduction.json", reproduction)
        index = {
            str(p.relative_to(output)): file_hash(p)
            for p in sorted(output.rglob("*"))
            if p.is_file() and p.name != "status.json"
        }
        budget.json(output / "artifact-index.json", index)
        status.update(
            status="complete",
            phase=None,
            cells_per_pass=len(rows),
            expected_invalid_cases_per_pass=1,
            exact_repeat=True,
            unique_task_episodes=4,
            model_episode_executions=16,
        )
        budget.check()
    except BaseException as exc:
        status.update(
            status=(
                "budget_exhausted"
                if isinstance(exc, BudgetExceeded)
                else "interrupted"
                if isinstance(exc, KeyboardInterrupt)
                else "invalid"
            ),
            exception=type(exc).__name__,
            reason=str(exc),
        )
        raise
    finally:
        try:
            status.update(budget.measurements())
            # Resolve the final status file's self-inclusive byte count.
            status_path = output / "status.json"
            other_bytes = sum(budget.sizes.values()) - budget.sizes.get(str(status_path), 0)
            for _ in range(4):
                payload = (
                    json.dumps(status, indent=2, sort_keys=True, allow_nan=False) + "\n"
                ).encode()
                if status["artifact_bytes"] == other_bytes + len(payload):
                    break
                status["artifact_bytes"] = other_bytes + len(payload)
            budget.json(status_path, status, emergency=True)
        finally:
            torch.set_num_threads(old_threads)
            torch.set_default_dtype(old_dtype)
            torch.use_deterministic_algorithms(old_determinism, warn_only=old_warn)
    return status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/platform-fixture.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = FixtureConfig(**json.loads(args.config.read_text()))
    print(json.dumps(run_suite(config, args.output), indent=2))


if __name__ == "__main__":
    main()
