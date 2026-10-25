from dataclasses import replace

import numpy as np
import pytest
import torch

from soam.config import Config, EnvironmentConfig
from soam.encoders.projection import FixedProjection
from soam.environments.dynamics import Dynamics
from soam.recurrent.models import build_model, parameter_count, training_loss


@pytest.fixture(autouse=True)
def deterministic_cpu():
    torch.set_num_threads(1)
    torch.manual_seed(7)


def test_generator_reproducibility_and_split_separation():
    env = EnvironmentConfig()
    first = Dynamics(env, 11, "train").sample(6, 8, switch_every=4, balanced=True)
    repeat = Dynamics(env, 11, "train").sample(6, 8, switch_every=4, balanced=True)
    test = Dynamics(env, 11, "test").sample(6, 8, switch_every=4, balanced=True)
    for name in ("states", "observations", "actions", "contexts"):
        assert torch.equal(getattr(first, name), getattr(repeat, name))
    assert not torch.equal(first.states, test.states)
    assert not torch.equal(first.actions, test.actions)
    assert torch.equal(first.contexts[:, 4], (first.contexts[:, 3] + 1) % 3)


def test_rotation_direction_actions_and_translation():
    cfg = replace(EnvironmentConfig(), damping=1.0)
    env = Dynamics(cfg, 11, "train")
    states = np.tile([1.0, 0.0], (3, 1))
    actions = np.zeros((3, 3))
    contexts = np.arange(3)
    result = env.transition(states, actions, contexts)
    assert result[0, 1] < 0 < result[1, 1]
    np.testing.assert_allclose(np.linalg.norm(result[:2], axis=-1), 1.0)
    actions[:, 1] = 1
    np.testing.assert_allclose(
        env.transition(states, actions, contexts) - result,
        np.tile([cfg.translation_action_gain, 0.0], (3, 1)),
        atol=1e-7,
    )
    actions[:, 0] = 1
    assert not np.allclose(env.transition(states, actions, contexts), result)


def test_fixed_encoder_preserves_information_without_trainable_weights():
    encoder = FixedProjection(12, 1)
    assert list(encoder.parameters()) == []
    observation = torch.randn(7, 2)
    torch.testing.assert_close(encoder.diagnostic_inverse(encoder(observation)), observation)
    assert encoder.matrix.shape == (12, 2)


@pytest.mark.parametrize("variant", ["additive", "gated", "low_rank", "separate"])
def test_switches_carry_state_and_inference_cannot_write_weights(variant):
    cfg = Config(hidden_dim=16)
    model = build_model(cfg, variant)
    batch = Dynamics(cfg.environment, 11, "test").sample(6, 8, switch_every=4, balanced=True)
    before = {key: value.clone() for key, value in model.state_dict().items()}
    with torch.no_grad():
        predicted, hidden = model.rollout(batch.observations[:, 0], batch.actions, batch.contexts)
        current = model.initialize(batch.observations[:, 0])
        manual = []
        for t in range(8):
            current = model.step(current, batch.actions[:, t], batch.contexts[:, t])
            manual.append(model.decode(current))
        torch.testing.assert_close(predicted, torch.stack(manual, 1), rtol=0, atol=0)
    for key, value in model.state_dict().items():
        assert torch.equal(value, before[key])
    assert hidden.abs().max() <= 1
    # Replacing diagnostic ground truth cannot affect predictions.
    batch.states.fill_(12345)
    with torch.no_grad():
        repeated, _ = model.rollout(batch.observations[:, 0], batch.actions, batch.contexts)
    torch.testing.assert_close(predicted, repeated, rtol=0, atol=0)


@pytest.mark.parametrize("variant", ["additive", "gated", "low_rank", "separate"])
def test_trainable_gradients_and_bounded_assimilation(variant):
    cfg = Config(hidden_dim=16)
    model = build_model(cfg, variant)
    batch = Dynamics(cfg.environment, 11, "train").sample(6, 8, balanced=True)
    loss = training_loss(model, batch, 0.3)
    loss.backward()
    for name, parameter in model.named_parameters():
        assert parameter.grad is not None, name
        assert torch.isfinite(parameter.grad).all(), name
        assert parameter.grad.abs().sum() > 0, name
    corrected = model.assimilate(
        torch.ones(6, model.hidden_dim), batch.observations[:, 0], batch.contexts[:, 0]
    )
    assert corrected.abs().max() <= 1


def test_separate_total_parameter_budget():
    cfg = Config()
    shared = parameter_count(build_model(cfg, "additive"))
    separate = parameter_count(build_model(cfg, "separate"))
    assert abs(shared - separate) / shared < 0.05


def test_config_roundtrip_and_rejection():
    cfg = Config.load("configs/smoke.json")
    assert Config.from_dict(cfg.to_dict()) == cfg
    with pytest.raises(TypeError):
        Config.from_dict({"misspelled_horizon": 32})
    for changed in (
        {"alpha": 2},
        {"steps": 0},
        {"perturb_step": 999},
        {"seeds": [1, 1]},
        {"models": ["unknown"]},
        {"learning_rate": float("nan")},
        {"hidden_dim": 1},
        {"seeds": [-1]},
        {"perturb_step": 1.5},
    ):
        with pytest.raises(ValueError):
            Config.from_dict(changed)
