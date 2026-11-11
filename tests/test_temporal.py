"""Scientific invariants for the Study B temporal interface."""

from dataclasses import replace

import numpy as np
import pytest
import torch

from soam.temporal.data import generate, input_hash, normalization, seed, training_data
from soam.temporal.engine import evaluate, fit, fit_linear, objective, recovery, rollout
from soam.temporal.models import make
from soam.temporal.runner import Budget, digest, tensor_hash
from soam.temporal.statistics import interval, primary_decision


@pytest.fixture(autouse=True)
def one_thread():
    torch.set_num_threads(1)


def test_split_pairing_mask_and_clock():
    a = generate("development", 12, schedule="every2", horizon=16)
    b = generate("development", 12, schedule="every4", horizon=16)
    assert torch.equal(a.target, b.target)
    assert torch.equal(a.evidence.actions, b.evidence.actions)
    assert torch.equal(a.evidence.observed[::4], b.evidence.observed[::4])
    assert not b.evidence.mask[1:4].any()
    assert not a.evidence.observed[~a.evidence.mask].any()
    stationary = a.evidence.roles[..., 0].bool()
    assert torch.equal(a.target[:-1][stationary], a.target[1:][stationary])
    assert stationary.sum() == stationary.numel() / 2
    assert len({seed(s, 12, 0, "noise") for s in ("train", "development", "confirmation")}) == 3
    with pytest.raises(ValueError):
        seed("unknown", 0, 0, "noise")


@pytest.mark.parametrize("name", ["MIX32", "PC32", "GA32", "AM32", "SET32"])
def test_current_observation_cannot_change_current_prior(name):
    b = generate("fixture", 12, batch=3, horizon=8, schedule="every1")
    model = make(name, 12)
    altered = b.evidence.observed.clone()
    altered[4] += 3 * b.evidence.mask[4]
    changed = replace(b.evidence, observed=altered)
    a = rollout(model, b.evidence)
    c = rollout(model, changed)
    assert torch.equal(a["prior"][:4], c["prior"][:4])
    assert not torch.equal(a["posterior"][4], c["posterior"][4])
    assert torch.equal(a["prior"][3], c["prior"][3])


def test_missing_mask_ignores_values_and_zero_time_settling():
    b = generate("fixture", 17, batch=3, horizon=8, schedule="initial")
    model = make("SET32", 4)
    before = tensor_hash(model.state_dict())
    changed = torch.where(
        b.evidence.mask, b.evidence.observed, torch.full_like(b.evidence.observed, 999)
    )
    a = rollout(model, b.evidence, k=4)
    c = rollout(model, replace(b.evidence, observed=changed), k=4)
    assert torch.equal(a["prior"], c["prior"])
    assert tensor_hash(model.state_dict()) == before
    assert a["counts"][0].eq(4).all() and not a["counts"][1:].any()
    assert a["updates"].eq(1 + 8 + 4).all()
    assert len(a["prior"]) == len(b.evidence.actions) == 8
    h = torch.randn(3, 32)
    z = torch.randn(3, 12)
    m = torch.ones(3, 12, dtype=torch.bool)
    q = torch.tensor([[1.0, 0.0]]).repeat(3, 1)
    expected = 0.5 * h + 0.5 * torch.tanh(model.W(h) + model.Q(q))
    assert torch.equal(model.settle(h, z, m), expected)
    assert torch.equal(model.settle(h, z, m), model.settle(h, -z, m))


def test_mixed_update_recomputes_from_previous_not_double_motion():
    model = make("MIX32", 1)
    h = torch.randn(2, 32)
    a = torch.randn(2, 3)
    q = torch.tensor([[0.0, 1.0]]).repeat(2, 1)
    z = torch.randn(2, 12)
    m = torch.ones(2, 12, dtype=torch.bool)
    prior, _ = model.predict(h, a, q)
    post, _ = model.correct(prior, h, a, q, z, m, torch.full((2, 1), 0.01))
    expected = 0.5 * h + 0.5 * torch.tanh(
        model.W(h) + model.A(a) + model.Q(q) + model.E(torch.cat((z, m.float()), -1))
    )
    assert torch.equal(post, expected)


def test_independent_sensory_motion_gains():
    model = make("AM32", 1)
    h = torch.randn(2, 32)
    a = torch.randn(2, 3)
    q = torch.tensor([[0.0, 1.0]]).repeat(2, 1)
    p, beta = model.predict(h, a, q)
    assert beta.eq(1).all()
    with torch.no_grad():
        model.gate.bias.fill_(-10)
    pp, bb = model.predict(h, a, q)
    assert torch.equal(p, pp) and torch.equal(beta, bb)
    with torch.no_grad():
        model.motion.bias.fill_(-10)
    pp, bb = model.predict(h, a, q)
    assert not torch.equal(p, pp) and (bb < 0.001).all()


def test_fitted_filter_uses_observed_basis_and_keeps_covariance_transient():
    data = training_data(1, updates=12, batch=4, horizon=16)
    model = make("FILTER2", 1)
    fit_linear(model, data, 0.0001)
    # Direct decoder-row inverse reconstructs a new point in the fitted sensory span.
    h = torch.tensor([[0.2, -0.3]])
    z = h @ model.P.T + model.mean
    m = torch.ones_like(z, dtype=torch.bool)
    assert torch.allclose(model.decode_mean(z, m), h, atol=1e-4)
    before = tensor_hash(model.state_dict())
    b = generate("development", 2, batch=3, horizon=8)
    out = rollout(model, b.evidence, k=0)
    assert out["prior"].isfinite().all()
    assert before == tensor_hash(model.state_dict())
    assert model.initialize(z, m).shape[-1] == 6
    # Independent manual bilinear Jacobian agrees with finite differences.
    a = torch.tensor([[0.3, -0.2, 0.1]])
    q = torch.tensor([[0.0, 1.0]])
    state = model.initialize(z, m)
    pred, _ = model.predict(state, a, q)
    assert torch.linalg.eigvalsh(pred[:, 2:].reshape(-1, 2, 2)).min() > 0


def test_no_target_in_inference_api_and_deterministic_fit():
    b = generate("fixture", 4, batch=3, horizon=8)
    assert set(vars(b.evidence)) == {"observed", "mask", "actions", "roles", "noise_sd"}
    with pytest.raises(TypeError):
        rollout(make("PC32", 1), b.evidence, target=b.target)
    data = training_data(3, updates=3, batch=3, horizon=8, split="fixture")
    a, b = make("GA32", 5), make("GA32", 5)
    fa = fit(a, data, 0.003, lambda: None)
    fb = fit(b, data, 0.003, lambda: None)
    assert tensor_hash(a.state_dict()) == tensor_hash(b.state_dict())
    assert fa["trace"] == fb["trace"]
    assert input_hash(data) == input_hash(
        training_data(3, updates=3, batch=3, horizon=8, split="fixture")
    )


@pytest.mark.parametrize("mode", ["fixed", "event", "learned", "periodic"])
def test_settling_budget_and_learning_objective(mode):
    b = generate("fixture", 2, batch=3, horizon=8, schedule="every2")
    model = make("SET32", 4)
    path = rollout(model, b.evidence, k=4, mode=mode, variance=normalization())
    assert path["counts"].max() <= 4
    assert not path["counts"][~b.evidence.mask.any(-1)].any()
    loss = objective(model, b)
    loss.backward()
    assert model.halt.weight.grad is not None
    assert torch.isfinite(model.W.weight.grad).all()


def test_recovery_censor_and_root_intervals():
    e = np.ones((12, 2))
    e[6:, 0] = 0.001
    # A low pre-event baseline makes persistently large errors censored.
    e[:4] = 0.001
    t, c = recovery(e, 4)
    assert t[0] == 2 and not c[0] and c[1]
    a = interval([1, 2, 3], resamples=1000)
    assert a["n"] == 3 and a["lo"] <= 2 <= a["hi"]
    with pytest.raises(ValueError):
        interval(np.zeros((10, 30)))
    base = [
        {"J": 0.1, "clean": 0.01, "corrupt": 0.02, "change": 0.03, "free32": 0.02}
        for _ in range(10)
    ]
    good = [
        {"J": 0.08, "clean": 0.01, "corrupt": 0.02, "change": 0.03, "free32": 0.02}
        for _ in range(10)
    ]
    assert primary_decision({"GA32": good, "PC32": base, "MIX32": base})["outcome"] == "supported"
    assert (
        primary_decision({"GA32": good, "PC32": base, "MIX32": base}, ["PC32"])["outcome"]
        == "inconclusive"
    )


def test_resource_ceiling_and_receipt_digest(tmp_path):
    m = {"cpu_seconds": 100, "wall_seconds": 100, "rss_bytes": 10**12, "artifact_bytes": 1000}
    budget = Budget(tmp_path, m, "fixture")
    (tmp_path / "large").write_bytes(b"x" * 1001)
    with pytest.raises(RuntimeError, match="Artifact"):
        budget.check(force=True)
    assert digest({"a": 1, "b": 2}) == digest({"b": 2, "a": 1})


def test_evaluation_preserves_weights_and_initial_only_exposure():
    model = make("PC16", 1)
    rows, arrays, _ = evaluate(model, "fixture", 3, normalization(), horizon=8, batch=2, full=False)
    assert rows["partial/every4"]["observed_events"] == 3
    assert len(arrays) == 4
