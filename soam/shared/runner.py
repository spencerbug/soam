"""SOAM-050 engineering artifacts; deliberately no scientific-study entry point."""

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import torch

from soam.evaluation.provenance import capture
from soam.platform.core import Command, Observation, fingerprint
from soam.platform.runner import Budget, BudgetExceeded, read_arrays
from soam.platform.tasks import EvaluationTargets
from soam.shared.data import RecordedEpisode, SharedTask, observed_batch, stream
from soam.shared.evaluation import Probe, evaluate, random_masks, select_units
from soam.shared.fitting import FitPlan, fit
from soam.shared.models import (
    MANIFEST_HASH,
    PROTOCOL_HASH,
    ROOT,
    Candidate,
    TiedStateCandidate,
    manifest,
)


@dataclass(frozen=True)
class Config:
    archive_revision: str = "v1"
    mode: str = "fixture"
    seed: int = 9001
    threads: int = 1
    max_cpu_seconds: int = 120
    max_wall_seconds: int = 240
    max_rss_bytes: int = 2 * 1024**3
    max_artifact_bytes: int = 256 * 1024**2

    def validate(self):
        if self.archive_revision not in ("v1", "a1"):
            raise ValueError("unknown archive revision")
        if self.mode not in ("fixture", "preflight") or self.seed != 9001 or self.threads != 1:
            raise ValueError("engineering-only mode, seed 9001 and one thread required")
        for name, limit in (
            ("max_cpu_seconds", 120),
            ("max_wall_seconds", 240),
            ("max_rss_bytes", 2 * 1024**3),
            ("max_artifact_bytes", 256 * 1024**2),
        ):
            value = getattr(self, name)
            if type(value) is not int or not 0 < value <= limit:
                raise ValueError("invalid engineering budget")
        if self.max_artifact_bytes < 65536:
            raise ValueError("reserve failure metadata space")
        return self

    def to_dict(self):
        return asdict(self)


def provenance(config):
    result = capture(ROOT, config)
    if config.archive_revision == "a1":
        from soam.shared.archive import verify_contract

        result["source_files"]["docs/E1_ARCHIVE_A1.md"] = verify_contract()
    for path in (
        "docs/SHARED_POPULATION_PROTOCOL.md",
        "docs/protocols/shared_population_v1.json",
        "docs/RECURRENT_PLATFORM_CONTRACT.md",
    ):
        result["source_files"][path] = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    result["source_sha256"] = hashlib.sha256(
        json.dumps(result["source_files"], sort_keys=True).encode()
    ).hexdigest()
    result.update(
        protocol_sha256=PROTOCOL_HASH,
        manifest_sha256=MANIFEST_HASH,
        engineering_only=True,
        study_fits=0,
        confirmation_exposure=0,
        metric_dtype="float64",
        simulator_dtype="float64",
        deterministic_algorithms=torch.are_deterministic_algorithms_enabled(),
        torch_threads=torch.get_num_threads(),
    )
    return result


def archive_episodes(path, episodes, budget, store=None):
    """Keep model observations, training sensor records and evaluator truth separate."""
    if store is not None:
        return store.write(path, episodes)
    observations = {
        name: torch.cat([e.observed_arrays()[name] for e in episodes], dim=1)
        for name in episodes[0].observed_arrays()
    }
    budget.arrays(path / "observations.npz", observations)
    budget.arrays(
        path / "clean-records.npz", {"features": torch.cat([e.clean_records for e in episodes], 1)}
    )
    budget.arrays(
        path / "targets.npz",
        {
            "features": torch.cat([e.targets.features for e in episodes], 1),
            "world": torch.stack([e.targets.world for e in episodes], 1),
        },
    )
    budget.json(path / "streams.json", [e.stream_seeds for e in episodes])


def restore_episodes(path, store=None):
    if store is not None:
        return store.restore(path)
    observed = read_arrays(path / "observations.npz")
    clean = read_arrays(path / "clean-records.npz")["features"]
    targets = read_arrays(path / "targets.npz")
    streams = json.loads((path / "streams.json").read_text())
    episodes = []
    for i, keys in enumerate(streams):
        observations = tuple(
            Observation(
                *(observed[k][t, i : i + 1].clone() for k in ("z", "valid", "cue", "cue_valid"))
            )
            for t in range(len(observed["z"]))
        )
        commands = tuple(Command(a[i : i + 1].clone()) for a in observed["actions"])
        episodes.append(
            RecordedEpisode(
                observations,
                commands,
                EvaluationTargets(
                    targets["features"][:, i : i + 1].clone(), targets["world"][:, i].clone()
                ),
                keys,
                clean[:, i : i + 1].clone(),
            )
        )
    return tuple(episodes)


class ReplaySelectionTask:
    def __init__(self, path, store=None):
        self.path, self.store = path, store

    def episode(self, split, root, index, role, *, component):
        if split != "fixture/evaluation" or root != 401 or component != f"lesion-selection/{role}":
            raise ValueError("unexpected replay selection stream")
        return restore_episodes(self.path / "selection-data" / f"{role}-{index}", self.store)[0]


def fixture(path, budget, config, restore=None, store=None):
    task = SharedTask()
    normalization = (
        task.normalization()
        if restore is None
        else {
            **read_arrays(restore / "normalization.npz"),
            **json.loads((restore / "normalization.json").read_text()),
        }
    )
    variance = float(normalization["variance"])
    budget.arrays(
        path / "normalization.npz",
        {k: v for k, v in normalization.items() if isinstance(v, torch.Tensor)},
    )
    budget.json(
        path / "normalization.json",
        {k: v for k, v in normalization.items() if not isinstance(v, torch.Tensor)},
    )
    budget.arrays(path / "projection.npz", {"matrix": task.projection})
    models, fits, cells = {}, {}, []
    episodes = {
        role: task.episode("fixture/evaluation", config.seed, 0, role)
        if restore is None
        else restore_episodes(restore / "evaluation-data" / role, store)[0]
        for role in ("recall", "transition")
    }
    for role, episode in episodes.items():
        archive_episodes(path / "evaluation-data" / role, (episode,), budget, store)

    def cell(name, model, role, probe=None, episode=None):
        budget.check()
        arrays, record = evaluate(
            model, episodes[role] if episode is None else episode, variance, probe
        )
        budget.arrays(path / "cells" / name / "arrays.npz", arrays)
        budget.json(path / "cells" / name / "record.json", record)
        cells.append({"id": name, "arrays_sha256": fingerprint(arrays), "record": record})
        budget.check()
        return arrays

    for row in manifest()["models"]:
        family = row["id"]
        checkpoints = {}

        def replay_batch(root, update, role, *, fixture, batch_size, family=family):
            if root != config.seed or not fixture or batch_size != 2:
                raise ValueError("unexpected replay fit dimensions")
            batch = restore_episodes(restore / "fits" / family / "data" / f"{update}-{role}", store)
            return observed_batch(batch, role), batch

        def archive_batch(update, role, batch, family=family):
            archive_episodes(
                path / "fits" / family / "data" / f"{update}-{role}", batch, budget, store
            )

        def checkpoint(stage, state, optimizer, family=family, checkpoints=checkpoints):
            checkpoints[stage] = state
            budget.arrays(path / "fits" / family / f"{stage}.npz", state)
            if optimizer is not None:
                arrays = {
                    f"{index}-{key}": value
                    for index, values in optimizer["state"].items()
                    for key, value in values.items()
                    if isinstance(value, torch.Tensor)
                }
                budget.arrays(path / "fits" / family / f"{stage}-optimizer.npz", arrays)
                budget.json(
                    path / "fits" / family / f"{stage}-optimizer.json", optimizer["param_groups"]
                )

        model, record = fit(
            family,
            config.seed,
            0,
            plan=FitPlan(True, 1, 1, 2),
            archive_batch=archive_batch,
            checkpoint=checkpoint,
            budget_check=budget.check,
            batch_provider=replay_batch if restore is not None else None,
        )
        budget.json(path / "fits" / family / "record.json", record)
        fits[family] = {k: v for k, v in record.items() if k != "cpu_seconds"}
        models[family] = model
        pre = Candidate(family, record["initialization_seed"])
        pre.load_state_dict(checkpoints["recall"])
        cell(f"{family}-pre-recall", pre, "recall")
        for role in episodes:
            cell(f"{family}-final-{role}", model, role)

    def selection_archive(role, units, index, episode, arrays, record):
        name = f"selection-{role}-{units[0] if units else 'intact'}-{index}"
        budget.arrays(path / "cells" / name / "arrays.npz", arrays)
        budget.json(path / "cells" / name / "record.json", record)
        # Selection uses distinct component keys and must be reproducible itself.
        archive_episodes(path / "selection-data" / f"{role}-{index}", (episode,), budget, store)
        cells.append({"id": name, "arrays_sha256": fingerprint(arrays), "record": record})

    selected, selection = select_units(
        models["S32"],
        task if restore is None else ReplaySelectionTask(restore, store),
        variance,
        fixture=True,
        archive_cell=selection_archive,
        budget_check=budget.check,
    )
    masks, random_seed = random_masks(config.seed, fixture=True)
    budget.json(
        path / "selection.json",
        {"targeted": selected, "random": masks, "random_seed": random_seed, **selection},
    )
    for role in episodes:
        cell(f"targeted-{role}", models["S32"], role, Probe("full_clamp", selected))
        cell(f"readout-{role}", models["S32"], role, Probe("readout_clamp", selected))
        for i, units in enumerate(masks):
            cell(f"random-{i}-{role}", models["S32"], role, Probe("full_clamp", units))
        for bank in (0, 1):
            cell(
                f"D16-bank-{bank}-{role}",
                models["D16"],
                role,
                Probe("full_clamp", tuple(range(bank * 16, bank * 16 + 4))),
            )
        tied = TiedStateCandidate(models["S32"])
        tied_arrays = cell(f"T32-intact-{role}", tied, role)
        source_arrays = read_arrays(path / "cells" / f"S32-final-{role}" / "arrays.npz")
        if not torch.equal(source_arrays["free_features"], tied_arrays["free_features"]):
            raise AssertionError("T32 intact equivalence failed")
        for bank in (0, 1):
            masked = cell(
                f"T32-bank-{bank}-{role}",
                tied,
                role,
                Probe("full_clamp", tuple(i + bank * 32 for i in selected)),
            )
            if bank != (role == "transition") and not torch.equal(
                tied_arrays["free_features"], masked["free_features"]
            ):
                raise AssertionError("T32 opposite-bank isolation failed")
    for kind in ("action_shift", "zero_A"):
        cell(kind, models["S32"], "transition", Probe(kind))
    perturb_seed = stream("fixture/evaluation", config.seed, 0, "perturbations")
    for kind in ("zero_cue", "perturb", "zero_S", "zero_S_perturb"):
        cell(kind, models["S32"], "recall", Probe(kind, seed=perturb_seed))
    broken = Candidate("S32", config.seed)
    with torch.no_grad():
        broken.bank.E.fill_(float("nan"))
    try:
        evaluate(broken, episodes["recall"], variance)
    except FloatingPointError as error:
        budget.json(
            path / "expected-failure.json",
            {
                "fixture_only": True,
                "expected": True,
                "status": "numerical_failure",
                "condition": "nonfinite sensory weights",
                "family": "S32",
                "seed": config.seed,
                "exception": type(error).__name__,
                "message": str(error),
                "successful_score": None,
            },
        )
    else:
        raise AssertionError("nonfinite candidate incorrectly accepted")
    return {
        "fixture_only": True,
        "fits": fits,
        "cells": cells,
        "selected": list(selected),
        "normalization_sha256": normalization["sha256"],
        "study_fit_count": 0,
    }


def run(output, config=None):
    config = (Config() if config is None else config).validate()
    manifest()  # Fail closed before creating an output directory on protocol mismatch.
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    old_threads, old_deterministic = (
        torch.get_num_threads(),
        torch.are_deterministic_algorithms_enabled(),
    )
    budget = Budget(config)
    try:
        torch.set_num_threads(1)
        torch.use_deterministic_algorithms(True)
        budget.json(output / "config.json", config.to_dict())
        budget.json(output / "provenance.json", provenance(config))
        budget.json(output / "status.json", {"status": "running", "mode": config.mode})
        from soam.shared.archive import InputStore

        store = (
            InputStore(output / "input-objects", budget)
            if config.archive_revision == "a1"
            else None
        )
        if config.mode == "fixture":
            original = fixture(output / "original", budget, config, store=store)
            repeat = fixture(
                output / "repeat", budget, config, restore=output / "original", store=store
            )
            if original != repeat:
                raise AssertionError("engineering fixture numerical repeat mismatch")
            # Replay archive values, not zip-container bytes or wall-clock measurements.
            compared = 0
            for a in sorted((output / "original").rglob("*.npz")):
                b = output / "repeat" / a.relative_to(output / "original")
                av, bv = read_arrays(a), read_arrays(b)
                if fingerprint(av) != fingerprint(bv):
                    raise AssertionError(f"archive repeat mismatch: {a.name}")
                compared += len(av)
            result = {
                "fixture_only": True,
                "fit_instances": 14,
                "updates_per_fit": 2,
                "batch_size": 2,
                "cells_per_execution": len(original["cells"]),
                "numerical_arrays_compared": compared,
                "exact_repeat": True,
                "study_fits": 0,
                "confirmation_exposure": 0,
                "expected_numerical_failures": 2,
            }
        else:
            from soam.shared.preflight import calibrate

            result = calibrate(output, budget, archive_revision=config.archive_revision)
        budget.json(output / "result.json", result)
        budget.json(
            output / "status.json",
            {"status": "complete", "mode": config.mode, **budget.measurements()},
        )
        return result
    except BaseException as error:
        budget.json(
            output / "status.json",
            {
                "status": "budget_exhausted" if isinstance(error, BudgetExceeded) else "failed",
                "mode": config.mode,
                "exception": type(error).__name__,
                "message": str(error),
                "subsequent_work_stopped": True,
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
    parser.add_argument("--mode", choices=("fixture", "preflight"), default="fixture")
    parser.add_argument("--archive-revision", choices=("v1", "a1"), default="v1")
    args = parser.parse_args()
    result = run(args.output, Config(mode=args.mode, archive_revision=args.archive_revision))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
