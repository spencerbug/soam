"""Fixed E1 confirmation-root inventory and archived-input repeat orchestration.

Equations, fitting, streams, probes and thresholds remain in the frozen modules.
This module only orders calls, archives their results and accounts for failures.
"""

import json
from pathlib import Path

import torch

from soam.platform.core import fingerprint
from soam.platform.runner import read_arrays
from soam.shared.data import SharedTask, observed_batch, stream
from soam.shared.evaluation import Probe, evaluate, random_masks, select_units
from soam.shared.fitting import FitPlan, fit
from soam.shared.models import Candidate, TiedStateCandidate, manifest
from soam.shared.study import atomic_arrays

FAMILIES = tuple(row["id"] for row in manifest()["models"])
ROLES = ("recall", "transition")


def cell_inventory(count=20):
    """One root: 420 base + 1,320 selection + 560 other diagnostic cells."""
    names = [
        f"{family}-{condition}-{i}"
        for family in FAMILIES
        for condition in ("recall_pre", "recall_final", "transition")
        for i in range(count)
    ]
    names += [
        f"selection-{role}-{unit}-{i}"
        for role in ROLES
        for unit in ("intact", *range(32))
        for i in range(count)
    ]
    for role in ROLES:
        modes = ["targeted", "readout", *(f"random-{j}" for j in range(4))]
        modes += [f"D16-bank-{j}" for j in (0, 1)]
        modes += ["T32-intact", "T32-bank-0", "T32-bank-1"]
        names += [f"{mode}-{role}-{i}" for mode in modes for i in range(count)]
    names += [
        f"{mode}-{i}"
        for mode in ("action_shift", "zero_A", "zero_cue", "perturb", "zero_S", "zero_S_perturb")
        for i in range(count)
    ]
    return {name: {"status": "pending"} for name in names}


def numerical_failure(error):
    return isinstance(error, FloatingPointError) or (
        isinstance(error, RuntimeError) and "non-finite" in str(error) and "norm" in str(error)
    )


def same_outputs(a, b):
    """Compare both free and grounded predictions; bank widths can differ."""
    for key in ("free_features", "grounded_features"):
        if (key in a or key in b) and (
            key not in a or key not in b or not torch.equal(a[key], b[key])
        ):
            raise AssertionError("exact intact/opposite-bank output check failed: " + key)


class SelectionReplay:
    def __init__(self, path, store, fixture):
        self.path, self.store, self.fixture = path, store, fixture

    def episode(self, split, root, index, role, *, component):
        expected = "fixture/evaluation" if self.fixture else "development_diagnostic"
        if split != expected or root != 401 or component != f"lesion-selection/{role}":
            raise ValueError("unexpected selection replay stream")
        return self.store.restore(self.path / "selection-data" / f"{role}-{index}")[0]


def execute_root(
    path, store, budget, check, configs, variance, root, *, fixture=False, restore=None
):
    """All fits, then development-only lesion freeze, then confirmation observations.

    The repeat uses the same function, restoring every training/evaluation/selection
    input through A1. No resume, retry, alternate config or simulator regeneration.
    """
    path = Path(path)
    count = 2 if fixture else 20
    split = "fixture/evaluation" if fixture else "confirmation"
    plan = FitPlan(True, 1, 1, 2) if fixture else FitPlan()
    cells = cell_inventory(count)
    fits = {family: {"status": "pending", "config": configs[family]} for family in FAMILIES}
    models, pre_models = {}, {}
    task = SharedTask() if restore is None else None
    selection = {"status": "unavailable", "reason": "S32 unavailable"}

    def save(emergency=False):
        budget.json(path / "inventory.json", {"fits": fits, "cells": cells}, emergency=emergency)

    def archive_cell(name, episode, arrays, record):
        if cells[name]["status"] != "pending":
            raise ValueError("duplicate scoring cell: " + name)
        target = path / "cells" / name
        store.write(target / "inputs", (episode,))
        budget.arrays(target / "arrays.npz", arrays)
        budget.json(target / "record.json", record)
        cells[name] = {
            "status": "complete",
            "metrics": record["metrics"],
            "arrays_sha256": fingerprint(arrays),
        }
        check()

    def cell(name, model, episode, probe=None):
        check()
        try:
            arrays, record = evaluate(model, episode, variance, probe)
            archive_cell(name, episode, arrays, record)
            return arrays
        except (FloatingPointError, RuntimeError) as error:
            if not numerical_failure(error):
                raise
            cells[name] = {"status": "numerical_failure", "error": str(error)}
            budget.json(path / "cells" / name / "failure.json", cells[name])
            return None

    # Keep enough room to describe every unexecuted cell even at the storage cap.
    # This is a reservation inside the existing ceiling, not additional capacity.
    reserve_key = str(path / "failure-metadata-reserve")
    budget.sizes[reserve_key] = 2 * 1024**2
    try:
        save()
        # No held-out observations exist in this root until every fit and selection
        # has finished. Fitting uses train keys, including for confirmation roots.
        for family in FAMILIES:
            check()
            target = path / "fits" / family
            checkpoints = {}
            fits[family]["status"] = "running"
            save()

            def archive_batch(update, role, episodes, target=target):
                store.write(target / "data" / f"{update}-{role}", episodes)

            def checkpoint(stage, state, optimizer, target=target, checkpoints=checkpoints):
                atomic_arrays(budget, target / f"{stage}.npz", state)
                checkpoints[stage] = state
                if optimizer is not None:
                    arrays = {
                        f"{i}-{key}": value
                        for i, values in optimizer["state"].items()
                        for key, value in values.items()
                        if isinstance(value, torch.Tensor)
                    }
                    atomic_arrays(budget, target / f"{stage}-optimizer.npz", arrays)
                    budget.json(target / f"{stage}-optimizer.json", optimizer["param_groups"])

            def replay_batch(request_root, update, role, *, fixture, batch_size, family=family):
                if request_root != root or fixture != plan.fixture or batch_size != plan.batch_size:
                    raise ValueError("unexpected repeat fit request")
                episodes = store.restore(restore / "fits" / family / "data" / f"{update}-{role}")
                return observed_batch(episodes, role), episodes

            try:
                model, record = fit(
                    family,
                    root,
                    configs[family],
                    plan=plan,
                    archive_batch=archive_batch,
                    checkpoint=checkpoint,
                    budget_check=check,
                    batch_provider=replay_batch if restore is not None else None,
                )
                budget.json(target / "fit.json", record)
                models[family] = model
                pre_models[family] = Candidate(family, record["initialization_seed"])
                pre_models[family].load_state_dict(checkpoints["recall"])
                fits[family].update(status="complete", cpu_seconds=record["cpu_seconds"])
            except (FloatingPointError, RuntimeError) as error:
                if not numerical_failure(error):
                    raise
                fits[family].update(status="numerical_failure", error=str(error))
                budget.json(target / "failure.json", fits[family])
            save()

        if "S32" in models:

            def archive_selection(role, units, index, episode, arrays, record):
                name = f"selection-{role}-{units[0] if units else 'intact'}-{index}"
                store.write(path / "selection-data" / f"{role}-{index}", (episode,))
                archive_cell(name, episode, arrays, record)

            try:
                selected, details = select_units(
                    models["S32"],
                    task if restore is None else SelectionReplay(restore, store, fixture),
                    variance,
                    fixture=fixture,
                    archive_cell=archive_selection,
                    budget_check=check,
                )
                masks, random_seed = random_masks(root, fixture=fixture)
                selection = {
                    "status": "complete",
                    "targeted": list(selected),
                    "random": [list(mask) for mask in masks],
                    "random_seed": random_seed,
                    **details,
                }
            except (FloatingPointError, RuntimeError) as error:
                if not numerical_failure(error):
                    raise
                selection = {"status": "numerical_failure", "error": str(error)}
        # Durable freeze precedes the first confirmation input request, including
        # the intact base cells. Repeat verifies the original selection exactly.
        budget.json(path / "selection.json", selection)
        if restore is not None and selection != json.loads(
            (restore / "selection.json").read_text()
        ):
            raise AssertionError("repeat lesion selection mismatch")
        save()
        episodes = {}
        for role in ROLES if models else ():
            for i in range(count):
                check()
                episode = (
                    task.episode(split, root, i, role)
                    if restore is None
                    else store.restore(restore / "evaluation-data" / f"{role}-{i}")[0]
                )
                store.write(path / "evaluation-data" / f"{role}-{i}", (episode,))
                episodes[role, i] = episode
        intact = {}
        for family, model in models.items():
            for condition, role, candidate in (
                ("recall_pre", "recall", pre_models[family]),
                ("recall_final", "recall", model),
                ("transition", "transition", model),
            ):
                for i in range(count):
                    result = cell(f"{family}-{condition}-{i}", candidate, episodes[role, i])
                    if condition != "recall_pre" and result is not None:
                        intact[family, role, i] = result

        # D16 is independent of successful S32 fitting/selection.
        if "D16" in models:
            for role in ROLES:
                for i in range(count):
                    for bank in (0, 1):
                        result = cell(
                            f"D16-bank-{bank}-{role}-{i}",
                            models["D16"],
                            episodes[role, i],
                            Probe("full_clamp", tuple(range(bank * 16, bank * 16 + 4))),
                        )
                        baseline = intact.get(("D16", role, i))
                        if (
                            bank != (role == "transition")
                            and result is not None
                            and baseline is not None
                        ):
                            same_outputs(baseline, result)
        if selection["status"] == "complete":
            selected = tuple(selection["targeted"])
            tied = TiedStateCandidate(models["S32"])
            for role in ROLES:
                for i in range(count):
                    episode = episodes[role, i]
                    cell(
                        f"targeted-{role}-{i}",
                        models["S32"],
                        episode,
                        Probe("full_clamp", selected),
                    )
                    cell(
                        f"readout-{role}-{i}",
                        models["S32"],
                        episode,
                        Probe("readout_clamp", selected),
                    )
                    for j, units in enumerate(selection["random"]):
                        cell(
                            f"random-{j}-{role}-{i}",
                            models["S32"],
                            episode,
                            Probe("full_clamp", tuple(units)),
                        )
                    result = cell(f"T32-intact-{role}-{i}", tied, episode)
                    baseline = intact.get(("S32", role, i))
                    if result is not None and baseline is not None:
                        same_outputs(baseline, result)
                    for bank in (0, 1):
                        masked = cell(
                            f"T32-bank-{bank}-{role}-{i}",
                            tied,
                            episode,
                            Probe("full_clamp", tuple(unit + bank * 32 for unit in selected)),
                        )
                        if (
                            bank != (role == "transition")
                            and result is not None
                            and masked is not None
                        ):
                            same_outputs(result, masked)
        if "S32" in models:
            for i in range(count):
                for kind in ("action_shift", "zero_A"):
                    cell(f"{kind}-{i}", models["S32"], episodes["transition", i], Probe(kind))
                perturb_seed = stream(split, root, i, "perturbations")
                for kind in ("zero_cue", "perturb", "zero_S", "zero_S_perturb"):
                    cell(
                        f"{kind}-{i}",
                        models["S32"],
                        episodes["recall", i],
                        Probe(kind, seed=perturb_seed),
                    )
        for value in cells.values():
            if value["status"] == "pending":
                value.update(
                    status="unavailable", reason="numerical_failure_of_required_fit_or_selection"
                )
        save()
        result = {"fits": fits, "cells": cells, "selection": selection}
        budget.json(path / "result.json", result)
        return result
    except BaseException as error:
        budget.sizes.pop(reserve_key, None)
        for value in (*fits.values(), *cells.values()):
            if value["status"] in ("pending", "running"):
                value.update(status="unexecuted", reason=type(error).__name__)
        save(emergency=True)
        raise
    finally:
        budget.sizes.pop(reserve_key, None)


def compare_repeat(original, repeat, store, check):
    """Compare every numeric archive, fit trace/seed/exposure and scoring record.

    Timing and container bytes are excluded; missing or extra files are errors.
    Input references must be identical and resolve to the same verified objects.
    """
    left = {str(p.relative_to(original)) for p in original.rglob("*") if p.is_file()}
    right = {str(p.relative_to(repeat)) for p in repeat.rglob("*") if p.is_file()}
    if left != right:
        raise AssertionError("repeat artifact inventory mismatch")
    arrays, refs, records = 0, 0, 0
    for name in sorted(left):
        check()
        a, b = original / name, repeat / name
        if name.endswith(".npz"):
            av, bv = read_arrays(a), read_arrays(b)
            if fingerprint(av) != fingerprint(bv):
                raise AssertionError("repeat array mismatch: " + name)
            arrays += len(av)
        elif name.endswith(".json"):
            av, bv = json.loads(a.read_text()), json.loads(b.read_text())
            if name.endswith("fit.json"):
                av.pop("cpu_seconds")
                bv.pop("cpu_seconds")
            if name in ("inventory.json", "result.json"):
                for value in (*av["fits"].values(), *bv["fits"].values()):
                    value.pop("cpu_seconds", None)
            if name == "summary.json":
                for value in (*av["fit_status"].values(), *bv["fit_status"].values()):
                    value.pop("cpu_seconds", None)
            if av != bv:
                raise AssertionError("repeat record mismatch: " + name)
            if name.endswith("input-ref.json"):
                store.restore(a.parent)
                store.restore(b.parent)
                refs += 1
            records += 1
    return {
        "exact_repeat": True,
        "numerical_arrays_compared": arrays,
        "input_references_compared": refs,
        "records_compared": records,
        "independent_confirmation_roots_added": 0,
    }
