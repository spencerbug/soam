"""Scientific invariants for E0; oracle geometry is confined to tests."""

import copy
import json
from dataclasses import replace

import numpy as np
import pytest
import torch
from torch import nn

from soam.encoders.projection import FixedProjection
from soam.navigation.data import generate, seed, sensor
from soam.navigation.engine import evaluate, fit, geometry, rollout
from soam.navigation.models import NAMES, make
from soam.navigation.runner import MANIFEST, inventory
from soam.navigation.statistics import classify


@pytest.fixture
def config():
    cfg = json.loads(MANIFEST.read_text())
    cfg.update(
        updates=2,
        batch=4,
        train_horizon=4,
        evaluation_batch=4,
        free_horizon=6,
        grid=32,
        atlas_burnin=2,
        stationary_steps=8,
        perturbation_steps=4,
    )
    return cfg


def test_streams_and_fixed_sensor():
    a, truth = generate("train", 17, batch=4, horizon=5)
    b, _ = generate("train", 17, batch=4, horizon=5)
    torch.testing.assert_close(a.target, b.target, rtol=0, atol=0)
    torch.testing.assert_close(a.target, sensor(truth), rtol=0, atol=0)
    torch.testing.assert_close(
        truth[1:] - truth[:-1], a.evidence.actions[..., 0].double(), atol=1e-8, rtol=1e-6
    )
    assert (
        len({seed(s, 17, 0, "x") for s in ("train", "development", "confirmation", "fixture")}) == 4
    )
    c, _ = generate("confirmation", 17, batch=4, horizon=5)
    assert not torch.equal(a.target, c.target)
    torch.testing.assert_close(a.target.square().sum(-1), torch.ones(6, 4), atol=1e-6, rtol=1e-6)


def test_missing_stream_and_no_target_access():
    b, _ = generate("confirmation", 44, batch=4, horizon=8, condition="free")
    assert not b.evidence.mask[1:].any()
    assert not b.evidence.observed[1:].any()
    assert vars(b.evidence).keys() == {"observed", "mask", "actions"}
    model = make("NAV32", 1)
    before = rollout(model, b.evidence)
    poisoned = replace(b, target=torch.full_like(b.target, float("nan")))
    after = rollout(model, poisoned.evidence)
    for key in before:
        torch.testing.assert_close(before[key], after[key], rtol=0, atol=0)
    changed = replace(b.evidence, observed=b.evidence.observed.clone())
    changed.observed[5:] += 100
    # Unobserved future values cannot change any state, even after their timestamp.
    for key in before:
        torch.testing.assert_close(before[key], rollout(model, changed)[key], rtol=0, atol=0)


@pytest.mark.parametrize("name", NAMES)
def test_absent_correction_and_no_write(name, config):
    model = make(name, 31)
    fit(model, 31, config, 0.001, fixture=True)
    b, _ = generate("fixture", 31, batch=4, horizon=6, condition="free")
    h = model.initialize(b.evidence.observed[0], b.evidence.mask[0])
    before = copy.deepcopy(model.state_dict())
    new = model.correct(h, torch.randn(4, 12), torch.zeros(4, 12, dtype=torch.bool))
    assert torch.equal(h, new)
    result, arrays = evaluate(model, "fixture", 31, config)
    for k, tensor in model.state_dict().items():
        assert torch.equal(tensor, before[k])
    assert result["metrics"]["free_nmse"] == arrays["free/prior_nmse"].mean()
    assert result["metrics"]["return_nmse"] == arrays["return/posterior_nmse"][-1].mean()


def test_action_structure_control():
    nav, symmetric = make("NAV32", 9), make("SYM32", 9)
    h, a = torch.randn(5, 32), torch.zeros(5, 1)
    assert torch.equal(nav.predict(h, a), symmetric.predict(h, a))
    s, k = nav.matrices()
    assert torch.equal(s, s.T)
    assert torch.equal(k, -k.T)
    _, k2 = symmetric.matrices()
    assert torch.equal(k2, k2.T)
    assert not torch.equal(nav.predict(h, a + 0.1), symmetric.predict(h, a + 0.1))


class OracleGeometry(nn.Module):
    """Analytic controls verify the evaluator, not candidates in the experiment."""

    def __init__(self, radial_gain):
        super().__init__()
        self.n, self.radial_gain = 2, radial_gain

    def initialize(self, z, mask):
        return z @ FixedProjection(12, 1729).matrix

    def readout(self, h):
        return h @ FixedProjection(12, 1729).matrix.T

    def predict(self, h, action):
        radius = h.norm(dim=-1, keepdim=True)
        return h / radius * (1 + self.radial_gain * (radius - 1))


def test_geometry_distinguishes_identity_from_recovery(config):
    stationary, _, issues = geometry(OracleGeometry(1), "fixture", 3, config)
    recovery, _, other_issues = geometry(OracleGeometry(0.3), "fixture", 3, config)
    assert not issues and not other_issues
    assert stationary["normal_ratio"] == pytest.approx(1, abs=1e-5)
    assert recovery["normal_ratio"] == pytest.approx(0.3 ** config["perturbation_steps"], abs=1e-5)
    for metric in (stationary, recovery):
        assert metric["stationary_deg"] < 1e-4
        assert metric["normal_pose_deg"] < 1e-4
        assert metric["tangent_ratio"] == pytest.approx(1, abs=1e-6)


def test_fit_reproducible_and_only_fixture_stream(monkeypatch, config):
    from soam.navigation import engine

    original, splits = engine.generate, []

    def observed(split, *args, **kwargs):
        splits.append(split)
        return original(split, *args, **kwargs)

    monkeypatch.setattr(engine, "generate", observed)
    a, b = make("GRU32", 2), make("GRU32", 2)
    one, two = [fit(m, 5, config, 0.001, fixture=True) for m in (a, b)]
    np.testing.assert_array_equal(one["trace"], two["trace"])
    assert set(splits) == {"fixture"}
    for key in a.state_dict():
        assert torch.equal(a.state_dict()[key], b.state_dict()[key])


def test_frozen_inventory_and_precision_rules():
    config = json.loads(MANIFEST.read_text())
    trials = inventory(config)
    assert len(trials) == 58 == len({t["id"] for t in trials})
    assert sum(t["phase"] == "development" for t in trials) == 14
    assert sum(t["phase"] == "confirmation" for t in trials) == 40
    assert sum(t["phase"] == "repeat" for t in trials) == 4
    rules = {"x": {"min": None, "max": 0.05, "width": 0.04}}
    assert classify({"x": {"lo": 0.06, "hi": 0.08, "width": 0.02}}, rules)["outcome"].startswith(
        "negative"
    )
    assert (
        classify({"x": {"lo": 0.06, "hi": 0.8, "width": 0.74}}, rules)["outcome"] == "inconclusive"
    )
    assert classify({"x": {"lo": 0.01, "hi": 0.04, "width": 0.03}}, rules)["outcome"].startswith(
        "supported"
    )
    assert classify({"x": None}, rules)["outcome"] == "inconclusive"


def test_prediction_advances_once_and_correction_never_advances():
    b, _ = generate("fixture", 55, batch=4, horizon=9, condition="grounded")

    class Counter:
        steps = 0
        corrections = 0

        def initialize(self, z, mask):
            return torch.zeros_like(z)

        def readout(self, h):
            return h

        def predict(self, h, a):
            self.steps += 1
            return h + a

        def correct(self, h, z, mask):
            self.corrections += 1
            return h

    model = Counter()
    path = rollout(model, b.evidence)
    assert model.steps == model.corrections == 9
    torch.testing.assert_close(path["prior"], b.evidence.actions.cumsum(0).expand(-1, -1, 12))
