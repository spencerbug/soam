from dataclasses import replace
from itertools import pairwise

import pytest
import torch

from soam.config import Config
from soam.environments.dynamics import Dynamics
from soam.evaluation.controls import switch_lag_metrics
from soam.evaluation.runner import run
from soam.recurrent.models import (
    analytic_parameter_count,
    build_model,
    parameter_count,
    training_loss,
)

VARIANTS = ("additive", "gated", "low_rank", "separate", "gru", "independent")


@pytest.mark.parametrize("variant", VARIANTS)
def test_control_parameter_budgets_and_no_write_inference(variant):
    torch.set_num_threads(1)
    cfg = Config(match_budgets=True)
    model = build_model(cfg, variant)
    assert parameter_count(model) == analytic_parameter_count(
        model.hidden_dim, 12, 3, variant, cfg.rank
    )
    assert abs(parameter_count(model) - 2892) / 2892 <= 0.05
    batch = Dynamics(cfg.environment, 11, "test", 1).sample(6, 16, irregular=True, balanced=True)
    snapshot = {k: v.clone() for k, v in model.state_dict().items()}
    with torch.no_grad():
        pred, hidden = model.rollout(batch.observations[:, 0], batch.actions, batch.contexts)
        batch.states.fill_(float("nan"))
        batch.observations[:, 1:].fill_(float("nan"))
        repeated, _ = model.rollout(batch.observations[:, 0], batch.actions, batch.contexts)
    assert torch.equal(pred, repeated)
    assert hidden.abs().max() <= 1
    assert all(torch.equal(v, snapshot[k]) for k, v in model.state_dict().items())


def test_independent_switch_handoff_and_parameter_disjointness():
    cfg = Config(match_budgets=True)
    model = build_model(cfg, "independent")
    batch = Dynamics(cfg.environment, 11, "train", 1).sample(6, 12, switch_every=4, balanced=True)
    pred, _ = model.rollout(batch.observations[:, 0], batch.actions, batch.contexts)
    hidden = model.initialize(batch.observations[:, 0], batch.contexts[:, 0])
    manual = []
    for t in range(12):
        if t in (4, 8):
            hidden = model.initialize(manual[-1], batch.contexts[:, t])
        hidden = model.step(hidden, batch.actions[:, t], batch.contexts[:, t])
        manual.append(model.decode(hidden, batch.contexts[:, t]))
    torch.testing.assert_close(pred, torch.stack(manual, 1), rtol=0, atol=0)
    parameter_sets = [
        {
            p.data_ptr()
            for layers in (model.sensories, model.cores, model.readouts)
            for p in layers[i].parameters()
        }
        for i in range(3)
    ]
    assert all(not parameter_sets[i] & parameter_sets[j] for i in range(3) for j in range(i))
    before, _ = model.rollout(
        batch.observations[:, 0], batch.actions, torch.zeros_like(batch.contexts)
    )
    with torch.no_grad():
        for p in model.cores[1].parameters():
            p.add_(100)
    after, _ = model.rollout(
        batch.observations[:, 0], batch.actions, torch.zeros_like(batch.contexts)
    )
    assert torch.equal(before, after)


@pytest.mark.parametrize("variant", ("gru", "independent"))
def test_new_model_gradients_across_switches(variant):
    cfg = Config(match_budgets=True)
    model = build_model(cfg, variant)
    batch = Dynamics(cfg.environment, 11, "train", 1).sample(6, 12, switch_every=4, balanced=True)
    training_loss(model, batch, 0.3).backward()
    for name, p in model.named_parameters():
        assert p.grad is not None and torch.isfinite(p.grad).all(), name
        assert p.grad.abs().sum() > 0, name


def test_reserved_streams_irregular_schedules_and_held_actions():
    cfg = Config()
    args = {"batch_size": 12, "horizon": 80, "irregular": True, "balanced": True, "action_hold": 4}
    first = Dynamics(cfg.environment, 11, "test", 10483).sample(**args)
    repeat = Dynamics(cfg.environment, 11, "test", 10483).sample(**args)
    dev = Dynamics(cfg.environment, 11, "dev", 10483).sample(**args)
    old = Dynamics(cfg.environment, 11, "test").sample(**args)
    assert torch.equal(first.observations, repeat.observations)
    assert not torch.equal(first.actions, dev.actions)
    assert not torch.equal(first.actions, old.actions)
    for row in first.contexts:
        ends = [0] + (torch.where(row[1:] != row[:-1])[0] + 1).tolist()
        assert {b - a for a, b in pairwise(ends)} <= {3, 4, 5, 6, 7, 9, 10, 11, 12, 13}
    for offset in range(1, 4):
        assert torch.equal(first.actions[:, ::4], first.actions[:, offset::4])


def test_switch_lag_censors_previous_context_and_initial_segment():
    contexts = torch.tensor([[0, 0, 1, 1, 2, 2, 2]])
    target = torch.ones(1, 7, 1)
    predicted = target + torch.arange(7).reshape(1, 7, 1)
    lags = switch_lag_metrics(predicted, target, contexts, 4)
    assert [m["count"] for m in lags] == [2, 2, 1, 0]
    assert lags[0]["nmse"] == 10  # errors at transitions 2 and 4 only
    assert lags[2]["nmse"] == 36  # previous switch's lag 2 is censored


def test_controls_smoke_reproducible_and_artifact_complete(tmp_path):
    cfg = replace(
        Config.load("configs/substrate-controls.json"),
        seeds=(11,),
        models=("gru", "independent"),
        steps=2,
        batch_size=6,
        train_horizon=12,
        eval_horizon=12,
        stability_horizon=24,
        eval_sequences_per_context=1,
        control_horizons=(12,),
    )
    first = run(cfg, tmp_path / "first")
    repeat = run(cfg, tmp_path / "repeat")
    from scripts.check_reproduction import verify

    assert verify(tmp_path / "first", tmp_path / "repeat")["exact_numerical_match"]
    for row in first + repeat:
        assert not row["controls_readiness"]["applicable"]
        assert set(row["controls"]) == {"dev", "test"}
        assert set(row["controls"]["test"]["12"]) == {
            "steady",
            "regular",
            "irregular",
            "irregular_hold",
        }
        assert row["controls"]["test"]["12"]["irregular"]["switch_count"] > 0
