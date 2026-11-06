import json

import pytest
import torch

from soam.platform.runner import Budget, BudgetExceeded
from soam.shared.study import (
    Limits,
    atomic_arrays,
    check_calibration,
    development_inventory,
    run_development,
)


def test_development_inventory_is_fixed_and_excludes_confirmation():
    rows = development_inventory()
    assert len(rows) == 42 and len({r["id"] for r in rows}) == 42
    assert sum(r["base_cells"] for r in rows) == 2520
    assert {r["root"] for r in rows} == {401, 409, 419}
    assert {r["config"] for r in rows} == {0, 1}
    assert all(r["id"].startswith("development-") for r in rows)


def test_gate_rejects_unapproved_calibration_before_creating_outputs(tmp_path):
    p = tmp_path / "calibration"
    p.mkdir()
    for name, value in (
        ("provenance", {}),
        ("cost-ledger", {"archive_revision": "a1", "feasible": False}),
        ("status", {"status": "complete"}),
    ):
        (p / f"{name}.json").write_text(json.dumps(value))
    with pytest.raises(ValueError, match="passing completed"):
        run_development(tmp_path / "study", p)
    assert not (tmp_path / "study").exists()
    (p / "cost-ledger.json").write_text(
        json.dumps({"archive_revision": "a1", "feasible": True, "checks": {"storage": True}})
    )
    (p / "provenance.json").write_text(json.dumps({"source_files": {}}))
    with pytest.raises(ValueError, match="entry point"):
        check_calibration(p)


def test_checkpoint_publish_is_atomic_and_never_overwrites(tmp_path, monkeypatch):
    budget = Budget(Limits())
    path = tmp_path / "checkpoint.npz"
    atomic_arrays(budget, path, {"weights": torch.ones(2)})
    assert path.exists() and not path.with_name(path.name + ".tmp").exists()
    assert str(path) in budget.sizes
    with pytest.raises(FileExistsError):
        atomic_arrays(budget, path, {"weights": torch.zeros(2)})

    def fail(*args):
        raise BudgetExceeded("fixture stop")

    monkeypatch.setattr(budget, "arrays", fail)
    with pytest.raises(BudgetExceeded):
        atomic_arrays(budget, tmp_path / "failed.npz", {})
    assert not (tmp_path / "failed.npz").exists()
