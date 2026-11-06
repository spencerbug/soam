import json

import pytest
import torch

from soam.platform.core import fingerprint
from soam.platform.runner import Budget, BudgetExceeded
from soam.shared.data import SharedTask
from soam.shared.runner import Config, archive_episodes, restore_episodes, run


def test_archived_records_restore_without_simulator_or_aliasing(tmp_path, monkeypatch):
    task = SharedTask()
    _, episodes = task.training_batch(9001, 100, "transition", fixture=True, batch_size=2)
    budget = Budget(Config())
    archive_episodes(tmp_path, episodes, budget)
    monkeypatch.setattr(SharedTask, "episode", lambda *args: pytest.fail("replay used simulator"))
    restored = restore_episodes(tmp_path)
    for a, b in zip(episodes, restored):
        assert fingerprint(a.observed_arrays()) == fingerprint(b.observed_arrays())
        assert torch.equal(a.clean_records, b.clean_records)
        assert torch.equal(a.targets.world, b.targets.world)
        assert a.stream_seeds == b.stream_seeds
        assert b.targets.features.data_ptr() != b.clean_records.data_ptr()


def test_runner_records_failure_stops_and_restores_settings(tmp_path, monkeypatch):
    calls = []

    def fail(*args, **kwargs):
        calls.append(1)
        raise BudgetExceeded("deliberate fixture stop")

    monkeypatch.setattr("soam.shared.runner.fixture", fail)
    before = (torch.get_num_threads(), torch.are_deterministic_algorithms_enabled())
    output = tmp_path / "failed"
    with pytest.raises(BudgetExceeded):
        run(output)
    status = json.loads((output / "status.json").read_text())
    assert status["status"] == "budget_exhausted"
    assert status["subsequent_work_stopped"]
    assert len(calls) == 1
    assert before == (torch.get_num_threads(), torch.are_deterministic_algorithms_enabled())
    with pytest.raises(FileExistsError):
        run(output)
    with pytest.raises(ValueError, match="engineering-only"):
        run(tmp_path / "study", Config(mode="confirmation"))
