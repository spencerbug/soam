import json

import numpy as np
import pytest
import torch

from soam.platform.runner import Budget, BudgetExceeded
from soam.shared import continuation as c
from soam.shared import execution as e
from soam.shared.archive import InputStore
from soam.shared.data import SharedTask
from soam.shared.models import manifest
from soam.shared.runner import Config
from soam.shared.study_summary import aggregate


def test_remaining_inventory_matches_frozen_manifest():
    rows = c.continuation_inventory()
    assert sum(r["fits"] for r in rows) == 77
    assert sum(r["cells"] for r in rows) == 25300
    assert [r["root"] for r in rows[:-1]] == manifest()["streams"]["confirmation_roots"]
    assert rows[-1]["phase"] == "repeat" and rows[-1]["root"] == 11
    cells = e.cell_inventory()
    assert len(cells) == 2300
    assert sum(name.startswith("selection-") for name in cells) == 1320
    assert sum(name.startswith("T32-") for name in cells) == 120
    assert len(e.cell_inventory(2)) == 230


def test_fixture_freezes_selection_before_evaluation_and_replays_without_simulator(
    tmp_path, monkeypatch
):
    old_threads = torch.get_num_threads()
    torch.set_num_threads(1)
    budget = Budget(Config(archive_revision="a1"))
    store = InputStore(tmp_path / "objects", budget)
    configs = {name: 1 if name != "L12" else 0 for name in e.FAMILIES}
    original_episode = SharedTask.episode
    source = tmp_path / "original"

    def guarded(self, split, root, index, role, **kwargs):
        assert split.startswith("fixture/"), "fixture attempted scientific exposure"
        if split == "fixture/evaluation" and root == 9001:
            assert (source / "selection.json").exists()
            assert json.loads((source / "selection.json").read_text())["status"] == "complete"
            assert all((source / "fits" / family / "final.npz").exists() for family in e.FAMILIES)
        return original_episode(self, split, root, index, role, **kwargs)

    monkeypatch.setattr(SharedTask, "episode", guarded)
    try:
        result = e.execute_root(
            source, store, budget, budget.check, configs, 0.04, 9001, fixture=True
        )
        assert len(result["cells"]) == 230
        assert all(v["status"] == "complete" for v in result["cells"].values())
        before_objects = set(store.root.iterdir())

        def forbidden(*args, **kwargs):
            raise AssertionError("repeat regenerated source inputs")

        monkeypatch.setattr(SharedTask, "episode", forbidden)
        monkeypatch.setattr(SharedTask, "training_batch", forbidden)
        repeated = e.execute_root(
            tmp_path / "repeat",
            store,
            budget,
            budget.check,
            configs,
            0.04,
            9001,
            fixture=True,
            restore=source,
        )
        assert repeated["selection"] == result["selection"]
        assert before_objects == set(store.root.iterdir())
        checked = e.compare_repeat(source, tmp_path / "repeat", store, budget.check)
        assert checked["exact_repeat"] and checked["numerical_arrays_compared"] > 1000
        # A corrupt numerical artifact and missing cells must not pass replay.
        artifact = tmp_path / "repeat/fits/S32/final.npz"
        artifact.unlink()
        with pytest.raises(AssertionError, match="inventory mismatch"):
            e.compare_repeat(source, tmp_path / "repeat", store, budget.check)
    finally:
        torch.set_num_threads(old_threads)


def test_budget_preserves_cumulative_cost_and_stops_each_phase(monkeypatch):
    clock = [100.0]
    monkeypatch.setattr(c.time, "process_time", lambda: clock[0])
    prior = {
        "cpu_seconds": 406.0,
        "wall_seconds": 408.0,
        "artifact_bytes": 97000000,
        "peak_rss_bytes": 400000000,
        "development_cpu_seconds": 392.0,
    }
    b = c.ContinuationBudget(prior)
    assert b.measurements()["cpu_seconds"] == 406
    assert b.measurements()["artifact_bytes"] == 97000000
    b.begin("confirmation")
    clock[0] += 8001
    with pytest.raises(BudgetExceeded, match="confirmation phase"):
        b.check()
    b.end()
    b.phases["confirmation"] = 8000
    b.begin("repeat")
    clock[0] += 1201
    with pytest.raises(BudgetExceeded, match="repeat phase"):
        b.check()
    b.end()
    b.phases["repeat"] = 1200
    clock[0] += 1200
    with pytest.raises(BudgetExceeded, match="overhead"):
        b.check()


@pytest.mark.parametrize(
    "exception,status",
    [
        (FloatingPointError("fixture nonfinite"), "numerical_failure"),
        (ValueError("fixture bug"), "unexecuted"),
    ],
)
def test_failures_keep_inventory_and_never_retry(tmp_path, monkeypatch, exception, status):
    calls = []

    def failed(family, *args, **kwargs):
        calls.append(family)
        raise exception

    monkeypatch.setattr(e, "fit", failed)
    # No need to generate any observations when all fits are unavailable.
    monkeypatch.setattr(
        SharedTask, "episode", lambda *a, **k: (_ for _ in ()).throw(ValueError("no models"))
    )
    budget = Budget(Config(archive_revision="a1"))
    store = InputStore(tmp_path / "objects", budget)

    def execute():
        return e.execute_root(
            tmp_path / "root",
            store,
            budget,
            budget.check,
            dict.fromkeys(e.FAMILIES, 0),
            0.04,
            9001,
            fixture=True,
        )

    if status == "numerical_failure":
        execute()
    else:
        with pytest.raises(ValueError, match="fixture bug"):
            execute()
    inventory = json.loads((tmp_path / "root/inventory.json").read_text())
    assert len(inventory["cells"]) == 230
    assert len(calls) == (7 if status == "numerical_failure" else 1)
    assert inventory["fits"]["S32"]["status"] == status
    cell_status = "unavailable" if status == "numerical_failure" else "unexecuted"
    assert all(r["status"] == cell_status for r in inventory["cells"].values())


def test_missing_readiness_cannot_create_scientific_output(tmp_path):
    with pytest.raises(ValueError, match="readiness"):
        c.run(tmp_path / "no-science")
    assert not (tmp_path / "no-science").exists()


def test_exact_output_checks_include_grounded_predictions():
    a = {"free_features": torch.ones(2), "grounded_features": torch.ones(2)}
    b = {"free_features": torch.ones(2), "grounded_features": torch.zeros(2)}
    with pytest.raises(AssertionError, match="grounded"):
        e.same_outputs(a, b)


def test_aggregation_pairs_roots_and_preserves_all_comparisons():
    roots = {}
    for root in manifest()["streams"]["confirmation_roots"]:
        means = {}
        for family in e.FAMILIES:
            means[f"{family}-transition"] = {"free8_nmse": 0.05 if family == "S32" else 0.1}
            means[f"{family}-recall_final"] = {"recall_nmse": 0.01}
        means["S32-recall_pre"] = {"recall_nmse": 0.01}
        for mode, recall, transition in [("targeted", 0.02, 0.07), ("readout", 0.012, 0.052)]:
            means[f"{mode}-recall"] = {"recall_nmse": recall}
            means[f"{mode}-transition"] = {"free8_nmse": transition}
        for name in ("action_shift", "zero_A"):
            means[name] = {"free8_nmse": 0.07}
        roots[root] = {
            "complete": True,
            "condition_means": means,
            "recovery": {
                "halving_fraction": 1.0,
                "halving_advantage": 0.5,
                "perturbed_recall_nmse": 0.01,
                "false_recovery_fraction": 0.0,
                "feature_variance_ratio": 1.0,
            },
        }
    result = aggregate(roots)
    assert result["outcome"] == "useful_sharing_supported"
    assert np.array(result["utility_root_contrasts"]).shape == (10, 7)
    assert np.array(result["causal_root_contrasts"]).shape == (10, 6)
    assert result["utility"]["resampling_unit"] == "paired_confirmation_root"
    assert result["recovery"]["outcome"] == "finite_horizon_recovery_supported"
    with pytest.raises(ValueError, match="ordered confirmation"):
        aggregate({**roots, 9001: roots[11]})
    roots[11]["complete"] = False
    assert aggregate(roots)["outcome"] == "incomplete_or_inconclusive_or_candidate_instability"


def test_full_size_inventory_survives_storage_stop(tmp_path, monkeypatch):
    budget = Budget(Config(archive_revision="a1"))

    def exhausted(*args, **kwargs):
        budget.sizes["partial-attempt"] = (
            budget.config.max_artifact_bytes - sum(budget.sizes.values()) - 65536
        )
        raise BudgetExceeded("fixture artifact stop")

    monkeypatch.setattr(e, "fit", exhausted)
    with pytest.raises(BudgetExceeded):
        e.execute_root(
            tmp_path / "root",
            InputStore(tmp_path / "objects", budget),
            budget,
            budget.check,
            dict.fromkeys(e.FAMILIES, 0),
            0.04,
            11,
        )
    inv = json.loads((tmp_path / "root/inventory.json").read_text())
    assert len(inv["cells"]) == 2300
    assert all(row["status"] == "unexecuted" for row in inv["cells"].values())
    assert sum(budget.sizes.values()) <= budget.config.max_artifact_bytes


def test_consumed_receipt_and_existing_output_fail_before_inputs(tmp_path, monkeypatch):
    receipt = tmp_path / "receipt"
    receipt.mkdir()
    (receipt / "execution-claim.json").write_text("{}")

    def forbidden():
        raise AssertionError("must fail before input audit")

    monkeypatch.setattr(c, "audit_development", forbidden)
    with pytest.raises(FileExistsError, match="consumed"):
        c.run(tmp_path / "no-science", readiness=receipt)
    assert not (tmp_path / "no-science").exists()
    with pytest.raises(FileExistsError):
        c.run(receipt, fixture=True)


def test_stale_calibration_cannot_omit_added_source(monkeypatch, tmp_path):
    monkeypatch.setattr(
        c, "check_calibration", lambda p: ({"source_files": {}, "source_sha256": "old"}, {}, {})
    )
    with pytest.raises(ValueError, match="omits current source"):
        c.current_calibration(tmp_path)


def test_archive_seal_detects_changes_and_symlinks(tmp_path):
    (tmp_path / "record.json").write_text("{}")
    first = c.tree_identity(tmp_path)
    (tmp_path / "record.json").write_text('{"changed": true}')
    assert first != c.tree_identity(tmp_path)
    (tmp_path / "link").symlink_to(tmp_path / "record.json")
    with pytest.raises(ValueError, match="symlink"):
        c.tree_identity(tmp_path)


def test_normalization_restores_tensor_variance_and_checks_samples(tmp_path):
    from soam.platform.core import fingerprint

    samples = torch.arange(24, dtype=torch.float32).reshape(2, 12)
    mean = samples.double().mean(0)
    variance = (samples.double() - mean).square().mean()
    b = Budget(Config(archive_revision="a1"))
    b.arrays(
        tmp_path / "normalization.npz", {"samples": samples, "mean": mean, "variance": variance}
    )
    b.json(tmp_path / "normalization.json", {"sha256": fingerprint({"samples": samples})})
    loaded = c.load_normalization(tmp_path)
    assert loaded["variance"].item() == 36.0
    b.arrays(
        tmp_path / "normalization.npz", {"samples": samples, "mean": mean, "variance": variance + 1}
    )
    with pytest.raises(ValueError, match="statistics mismatch"):
        c.load_normalization(tmp_path)


def test_scientific_plumbing_uses_frozen_configs_and_exact_roots_without_data(
    tmp_path, monkeypatch
):
    # Execute only orchestration with stub fits/cells. Any task generation is an error.
    receipt_path = tmp_path / "receipt"
    receipt_path.mkdir()
    configs = {family: 1 if family != "L12" else 0 for family in e.FAMILIES}
    dev = {"screen": {"selected_configs": configs, "primary_reference": "G32"}}
    record = {"source_sha256": "fixture-source"}
    receipt = {
        "ready": True,
        "confirmation_exposure": 0,
        "development": dev,
        "calibration": "unused-stub",
        "calibration_source": record["source_sha256"],
        "components": [],
        "carried": {
            "cpu_seconds": 406.0,
            "wall_seconds": 408.0,
            "artifact_bytes": 97000000,
            "peak_rss_bytes": 400000000,
            "development_cpu_seconds": 392.0,
        },
    }
    (receipt_path / "readiness.json").write_text(json.dumps(receipt))
    monkeypatch.setattr(c, "audit_development", lambda: dev)
    monkeypatch.setattr(c, "current_calibration", lambda p: (record, {}, {}))
    monkeypatch.setattr(
        c, "load_normalization", lambda p: {"variance": torch.tensor(0.04, dtype=torch.float64)}
    )
    monkeypatch.setattr(
        SharedTask,
        "episode",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("scientific data opened")),
    )
    calls = []

    def root(path, store, budget, check, chosen, variance, root, *, fixture, restore):
        assert chosen == configs and variance == 0.04 and not fixture
        calls.append((root, restore))
        return {"cells": {"stub": {"status": "complete"}}}

    monkeypatch.setattr(c, "execute_root", root)
    monkeypatch.setattr(
        c, "root_summary", lambda *a: {"complete": True, "cell_status_counts": {"complete": 2300}}
    )
    monkeypatch.setattr(c, "compare_repeat", lambda *a: {"exact_repeat": True})

    def summarize(roots):
        assert list(roots) == manifest()["streams"]["confirmation_roots"]
        return {"outcome": "synthetic_fixture_only"}

    monkeypatch.setattr(c, "aggregate", summarize)
    out = c.run(tmp_path / "output", readiness=receipt_path)
    assert out["reproduction"]["exact_repeat"]
    assert [root for root, _ in calls] == manifest()["streams"]["confirmation_roots"] + [11]
    assert all(restore is None for _, restore in calls[:-1])
    assert calls[-1][1] == tmp_path / "output/confirmation/11"
    assert (receipt_path / "execution-claim.json").exists()
    with pytest.raises(FileExistsError, match="consumed"):
        c.run(tmp_path / "second", readiness=receipt_path)
