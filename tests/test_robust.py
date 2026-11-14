import dataclasses

import pytest
import torch

from soam.robust.data import generate, seed, training_data
from soam.robust.engine import trace
from soam.robust.models import Config, Robust, phase1
from soam.temporal.engine import fit_linear, rollout
from soam.temporal.models import make


@pytest.fixture
def fitted():
    torch.set_num_threads(1)
    m = make("FILTER2", 0)
    fit_linear(m, training_data(15001, updates=12, batch=4, horizon=16, split="fixture"), 0.0001)
    return m


def test_seed_and_evidence_pair_contract():
    assert len({seed(s, 15001) for s in ("train", "development", "confirmation")}) == 3
    a, b = [generate("fixture", 15001, condition=c, batch=3) for c in ("ambiguous", "change")]
    assert all(torch.equal(v, vars(b.evidence)[k]) for k, v in vars(a.evidence).items())
    assert not torch.equal(a.target, b.target)
    assert all(
        torch.equal(v, vars(generate("fixture", 15001, condition="ambiguous", batch=3).evidence)[k])
        for k, v in vars(a.evidence).items()
    )


def test_stable_historical_equivalence_and_no_writes(fitted):
    b = generate("fixture", 15001, batch=5)
    old, new = rollout(fitted, b.evidence), rollout(Robust(fitted, Config()), b.evidence)
    assert torch.allclose(old["prior"].double(), new["prior"], atol=2e-6, rtol=2e-5)
    trace(Robust(fitted, Config()), b.evidence)


@pytest.mark.parametrize("config", phase1())
def test_psd_rejection_missing_and_future_causality(fitted, config):
    model = Robust(fitted, config)
    b = generate("fixture", 15001, batch=3, condition="corrupt")
    t = trace(model, b.evidence)
    cov = t["poststate"][..., 2:6].reshape(65, 3, 2, 2)
    assert torch.linalg.eigvalsh(cov).min() > 0
    assert torch.allclose(cov, cov.transpose(-1, -2), atol=1e-15, rtol=0)
    changed = b.evidence.observed.clone()
    changed[24:] += 100
    ev = dataclasses.replace(b.evidence, observed=changed)
    assert torch.equal(t["prior"][:24], trace(model, ev)["prior"][:24])
    h = model.initialize(b.evidence.observed[0], b.evidence.mask[0])
    p, _ = model.predict(h, b.evidence.actions[0], b.evidence.roles[0])
    y, _ = model.correct(
        p,
        h,
        b.evidence.actions[0],
        b.evidence.roles[0],
        torch.full((3, 12), float("nan")),
        torch.zeros(3, 12, dtype=torch.bool),
        b.evidence.noise_sd[0],
    )
    assert torch.equal(y, p)
    if config.mode.startswith("nis"):
        y, _ = model.correct(
            p,
            h,
            b.evidence.actions[0],
            b.evidence.roles[0],
            torch.full((3, 12), 100.0),
            torch.ones(3, 12, dtype=torch.bool),
            b.evidence.noise_sd[0],
        )
        assert torch.equal(y, p)


def test_solve_gain_and_nis_match_dense_measurement_equations(fitted):
    model = Robust(fitted, Config())
    model.diagnostics = True
    b = generate("fixture", 15001, batch=3)
    h = model.initialize(b.evidence.observed[0], b.evidence.mask[0])
    p, _ = model.predict(h, b.evidence.actions[0], b.evidence.roles[0])
    y, _ = model.correct(
        p,
        h,
        b.evidence.actions[0],
        b.evidence.roles[0],
        b.evidence.observed[4],
        b.evidence.mask[4],
        b.evidence.noise_sd[4],
    )
    for j in range(3):
        mask = b.evidence.mask[4, j]
        H = model.P[mask]
        C = p[j, 2:6].reshape(2, 2)
        S = H @ C @ H.T + 0.0001 * torch.eye(int(mask.sum()), dtype=torch.double)
        K = torch.linalg.solve(S, H @ C).T
        r = b.evidence.observed[4, j, mask].double() - model.readout(p)[j, mask]
        assert torch.allclose(y[j, :2], p[j, :2] + K @ r, atol=1e-10, rtol=1e-10)
        assert torch.allclose(
            model.last["nis"][j], r @ torch.linalg.solve(S, r), atol=1e-9, rtol=1e-9
        )


def test_downweight_changes_covariance_and_free_prediction_is_identical(fitted):
    b = generate("fixture", 15001, batch=3, condition="corrupt")
    paths = [
        trace(Robust(fitted, c), b.evidence)
        for c in (Config(), Config("R100", r=100), Config("HUBER99", "huber"))
    ]
    assert (
        paths[1]["poststate"][24, :, 2:6].reshape(3, 2, 2).diagonal(dim1=-2, dim2=-1).sum()
        > paths[0]["poststate"][24, :, 2:6].reshape(3, 2, 2).diagonal(dim1=-2, dim2=-1).sum()
    )
    b = generate("fixture", 15001, batch=3, schedule="initial")
    x = trace(Robust(fitted, Config()), b.evidence)["prior"]
    for c in phase1():
        if c.q == 1:
            assert torch.equal(x, trace(Robust(fitted, c), b.evidence)["prior"])


def test_benchmark_masks_and_dynamics_control():
    for c in ("isolated", "channels", "coherent", "sustained", "heavy", "biased", "dynamics"):
        b = generate("fixture", 15001, batch=3, condition=c)
        assert (b.evidence.observed[~b.evidence.mask] == 0).all()
    base = generate("fixture", 15001, batch=3)
    dyn = generate("fixture", 15001, batch=3, condition="dynamics")
    assert torch.equal(base.target[:24], dyn.target[:24])
    assert not torch.equal(base.target[24:], dyn.target[24:])
    assert torch.equal(base.evidence.actions, dyn.evidence.actions)


@pytest.mark.parametrize(
    "config",
    [
        Config("ADAPT1", "adaptive"),
        Config("ADAPT05", "adaptive", alpha=0.5),
        Config("TEMP2", "temporal"),
        Config("TEMP3", "temporal", persistence=3),
        Config("HYBRID", "hybrid"),
    ],
)
def test_extension_history_no_write_psd_and_future_causality(fitted, config):
    b = generate("fixture", 15001, batch=3, condition="change")
    model = Robust(fitted, config)
    before = {k: v.clone() for k, v in model.state_dict().items()}
    p = trace(model, b.evidence)
    assert all(torch.equal(v, before[k]) for k, v in model.state_dict().items())
    cov = p["poststate"][..., 2:6].reshape(65, 3, 2, 2)
    assert torch.linalg.eigvalsh(cov).min() > 0
    z = b.evidence.observed.clone()
    z[24:] += 100
    assert torch.equal(
        p["prior"][:24], trace(model, dataclasses.replace(b.evidence, observed=z))["prior"][:24]
    )
    alternate = dataclasses.replace(b.evidence, noise_sd=b.evidence.noise_sd * 1000)
    assert torch.equal(p["prior"], trace(model, alternate)["prior"])
    h = model.initialize(b.evidence.observed[0], b.evidence.mask[0])
    prior, _ = model.predict(h, b.evidence.actions[0], b.evidence.roles[0])
    post, _ = model.correct(
        prior,
        h,
        b.evidence.actions[0],
        b.evidence.roles[0],
        torch.zeros(3, 12),
        torch.zeros(3, 12, dtype=torch.bool),
        b.evidence.noise_sd[0],
    )
    assert torch.equal(post, prior)


def test_adaptation_subspace_invariance_and_bounds(fitted):
    model = Robust(fitted, Config("ADAPT1", "adaptive"))
    b = generate("fixture", 15001, batch=1)
    h = model.initialize(b.evidence.observed[0], b.evidence.mask[0])
    m = torch.ones(1, 12, dtype=torch.bool)
    shifted = model.readout(h) + torch.tensor([[10.0, -20.0]], dtype=torch.double) @ model.P.T
    p, _ = model.correct(
        h, h, b.evidence.actions[0], b.evidence.roles[0], shifted, m, b.evidence.noise_sd[0]
    )
    assert p[0, 6] == 0.0001
    noise = shifted + torch.arange(12, dtype=torch.double) * 100
    p, _ = model.correct(
        h, h, b.evidence.actions[0], b.evidence.roles[0], noise, m, b.evidence.noise_sd[0]
    )
    assert p[0, 6] == 0.25
    for _ in range(5):
        p, _ = model.correct(
            p,
            p,
            b.evidence.actions[0],
            b.evidence.roles[0],
            model.readout(p),
            m,
            b.evidence.noise_sd[0],
        )
    assert p[0, 6] == 0.0001


def test_temporal_reject_covariance_release_and_expiry(fitted):
    model = Robust(fitted, Config("TEMP2", "temporal"))
    b = generate("fixture", 15001, batch=1)
    h = model.initialize(b.evidence.observed[0], b.evidence.mask[0])
    m = torch.ones(1, 12, dtype=torch.bool)
    z = model.readout(h) + torch.tensor([[2.0, -2.0]], dtype=torch.double) @ model.P.T
    p, _ = model.correct(
        h, h, b.evidence.actions[0], b.evidence.roles[0], z, m, b.evidence.noise_sd[0]
    )
    assert torch.equal(p[:, :6], h[:, :6])
    assert p[0, 8] == 1
    p2, _ = model.correct(
        p, p, b.evidence.actions[0], b.evidence.roles[0], z, m, b.evidence.noise_sd[0]
    )
    assert not torch.equal(p2[:, :2], p[:, :2])
    assert p2[0, 8] == 0
    for _ in range(17):
        p, _ = model.predict(p, b.evidence.actions[0], b.evidence.roles[0])
    assert p[0, 8] == 0


def test_recovery_uses_actual_event_and_uncontaminated_baseline():
    import numpy as np

    from soam.robust.engine import event_recovery, event_windows

    errors = np.full((65, 2), 0.001)
    errors[24:40] = 1
    lag, censor = event_recovery(errors, np.array([24, 24]), np.array([32, 32]))
    assert (lag == 8).all() and not censor.any()
    b = generate("fixture", 15001, batch=8, condition="isolated", schedule="irregular")
    starts, ends, exposed = event_windows(b)
    for j in range(8):
        assert b.evidence.mask[starts[j], j].any() and ends[j] == starts[j] + 1 and exposed[j]


def test_root_bootstrap_family_and_exact_paired_null():
    import numpy as np

    from soam.robust.statistics import interval

    values = np.linspace(-0.1, 0.2, 10)
    draws = np.random.default_rng(15203).integers(0, 10, (20000, 10))
    ordinary = interval(values, draws=draws)
    adjusted = interval(values, draws=draws, family=12)
    assert adjusted["lo"] <= ordinary["lo"] and adjusted["hi"] >= ordinary["hi"]
    assert adjusted["n"] == 10
    paired = interval(values - values, draws=draws, family=12)
    assert paired["lo"] == paired["hi"] == 0
