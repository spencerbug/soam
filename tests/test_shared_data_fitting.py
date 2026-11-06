import copy

import numpy as np
import pytest
import torch

from soam.platform.core import fingerprint, model_fingerprint
from soam.shared.data import SharedTask, initialization_seed, observed_batch
from soam.shared.fitting import FitPlan, RidgeMoments, exposure_counts, fit, losses
from soam.shared.models import Candidate


def test_projection_split_partition_and_executed_commands():
    task = SharedTask()
    torch.testing.assert_close(task.projection.T @ task.projection, torch.eye(2))
    seeds = []
    for split, parity in (("fixture/train", 0), ("fixture/evaluation", 1)):
        for i in range(12):
            episode = task.episode(split, 9001, i, "transition")
            world = episode.targets.world.numpy()
            phase = np.arctan2(world[0, 1], world[0, 0]) % (2 * np.pi)
            assert int(phase / (np.pi / 4)) % 2 == parity
            assert 0.4 <= np.linalg.norm(world[0]) <= 0.8
            actions = torch.cat([c.action for c in episode.commands]).numpy()
            bins = np.minimum(((actions[:, :2] + 1) * 2).astype(int), 3)
            assert ((bins.sum(1) % 2) == parity).all()
            for t, a in enumerate(actions.astype(np.float64)):
                theta = 0.3 * a[0]
                rotation = np.array(
                    [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
                )
                np.testing.assert_array_equal(
                    world[t + 1], 0.98 * (rotation @ world[t]) + 0.03 * a[1:]
                )
            assert episode.targets.world.dtype == torch.float64
            assert episode.clean_records.dtype == torch.float32
            assert episode.observations[0].valid.sum() == 6
            assert episode.observations[0].z[~episode.observations[0].valid].count_nonzero() == 0
            assert not any(o.cue_valid.any() for o in episode.observations[1:])
            assert len(actions) == (8 if parity == 0 else 32)
            seeds.extend(row["seed"] for row in episode.stream_seeds.values())
    assert len(seeds) == len(set(seeds))


def test_data_pairing_record_ownership_and_training_packet_indices():
    task = SharedTask()
    a = task.episode("fixture/train", 9001, 0, "recall")
    b = task.episode("fixture/train", 9001, 0, "recall")
    assert fingerprint(a.observed_arrays()) == fingerprint(b.observed_arrays())
    assert a.stream_seeds == b.stream_seeds
    assert a.clean_records.data_ptr() != a.targets.features.data_ptr()
    expected = a.clean_records.clone()
    a.targets.features.fill_(1000)
    batch = observed_batch([a], "recall")
    assert torch.equal(batch.clean, expected)
    assert set(vars(batch)) == {"initial", "clean", "actions", "role"}
    with pytest.raises(ValueError, match="begins"):
        task.training_batch(9001, 99, "transition", fixture=True, batch_size=2)
    _, episodes = task.training_batch(9001, 100, "transition", fixture=True, batch_size=2)
    assert [e.stream_seeds["phase"]["key"][4] for e in episodes] == [1600, 1601]
    with pytest.raises(ValueError, match="frozen at 16"):
        task.training_batch(9001, 100, "transition", batch_size=2)
    assert initialization_seed("train", 401, "S32", 0) != initialization_seed(
        "train", 401, "S32", 1
    )


def test_normalization_is_separate_and_uses_float64_centered_variance():
    task = SharedTask()
    result = task.normalization()
    assert result["samples"].shape == (2048, 12)
    values = result["samples"].double()
    expected = (values - values.mean(0)).square().mean().clamp_min(1e-6)
    assert torch.equal(result["variance"], expected)
    assert result["sha256"] == fingerprint({"samples": result["samples"]})
    ordinary = task.episode("train", 1801, 0, "recall").clean_records[0, 0]
    assert not torch.equal(result["samples"][0], ordinary)


def test_losses_exclude_targets_from_free_rollout_and_do_not_detach(monkeypatch):
    task = SharedTask()
    recall, _ = task.training_batch(9001, 0, "recall", fixture=True, batch_size=2)
    transition, _ = task.training_batch(9001, 100, "transition", fixture=True, batch_size=2)
    model = Candidate("S32", 6)
    records = []
    original = model.readout

    def readout(state):
        value = original(state)
        records.append(value)
        return value

    monkeypatch.setattr(model, "readout", readout)
    before = model_fingerprint(model)
    terms = losses(model, recall, transition)
    original_free = torch.stack(records[10::2]).detach().clone()
    last_free = records[-2]
    records.clear()
    poisoned = copy.deepcopy(transition)
    poisoned.clean[1:] = 100
    losses(model, recall, poisoned)
    assert torch.equal(original_free, torch.stack(records[10::2]))
    assert model_fingerprint(model) == before
    # Final-step loss reaches the initial sensory projection through all updates.
    gradient = torch.autograd.grad(last_free.square().mean(), model.bank.E)[0]
    assert gradient.abs().sum() > 0
    assert set(terms) == {"recall", "free", "grounded"}


def test_ridge_including_bias_matches_direct_normalized_equations():
    x = torch.tensor([[1.0, 2.0, 1.0], [3.0, 4.0, 1.0], [5.0, 6.0, 1.0]])
    y = torch.arange(36, dtype=torch.float32).reshape(3, 12) / 10
    moments = RidgeMoments(3)
    moments.add(x[:1], y[:1])
    moments.add(x[1:], y[1:])
    expected = torch.linalg.solve(
        x.double().T @ x.double() / 3 + 0.01 * torch.eye(3, dtype=torch.float64),
        x.double().T @ y.double() / 3,
    ).T.float()
    assert torch.equal(moments.solve(0.01), expected)


@pytest.mark.parametrize("family", ["S32", "D25", "D16", "G28", "G32", "SYM32", "L12"])
def test_tiny_fit_checkpoint_exposures_and_exact_repeat(family):
    plan = FitPlan(True, 1, 1, 2)

    def once():
        archive, checkpoints = [], {}

        def batch(update, role, episodes):
            archive.append((update, role, [fingerprint(e.observed_arrays()) for e in episodes]))

        def checkpoint(name, state, optimizer):
            checkpoints[name] = (state, optimizer)

        model, result = fit(
            family,
            9001,
            0,
            plan=plan,
            archive_batch=batch,
            checkpoint=checkpoint,
            budget_check=lambda: None,
        )
        return model, result, archive, checkpoints

    old_threads = torch.get_num_threads()
    try:
        torch.set_num_threads(1)
        a, ra, archive_a, checkpoints = once()
        b, rb, archive_b, _ = once()
    finally:
        torch.set_num_threads(old_threads)
    assert ra["trace"] == rb["trace"]
    assert model_fingerprint(a) == model_fingerprint(b)
    assert archive_a == archive_b
    assert [(u, r) for u, r, _ in archive_a] == [
        (0, "recall"),
        (100, "recall"),
        (100, "transition"),
    ]
    assert set(checkpoints) == {"recall", "final"}
    assert fingerprint(checkpoints["recall"][0]) != fingerprint(checkpoints["final"][0])
    assert ra["exposure"]["distinct_recall_records"] == 4
    assert ra["exposure"]["executed_transitions"] == 16
    if family == "L12":
        assert checkpoints["recall"][0]["B"].count_nonzero() == 0
        assert checkpoints["final"][0]["B"].count_nonzero() > 0


def test_frozen_schedule_budget_failure_and_no_retry():
    expected = exposure_counts(FitPlan())
    assert expected["distinct_recall_records"] == 6400
    assert expected["transition_episodes"] == 4800
    assert expected["executed_transitions"] == 38400
    with pytest.raises(ValueError, match="frozen"):
        FitPlan(False, 1, 1, 2).validate()
    calls = []

    def exhausted():
        calls.append(1)
        raise TimeoutError("budget exhausted")

    with pytest.raises(TimeoutError):
        fit(
            "S32",
            9001,
            0,
            plan=FitPlan(True, 1, 1, 2),
            archive_batch=lambda *a: pytest.fail("archived after stop"),
            checkpoint=lambda *a: pytest.fail("checkpoint after stop"),
            budget_check=exhausted,
        )
    assert len(calls) == 1
