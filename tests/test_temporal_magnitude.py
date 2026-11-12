"""Missing magnitude channels and fresh-stream/reproducibility invariants."""

import torch

from soam.temporal.data import generate, training_data
from soam.temporal.engine import fit, rollout
from soam.temporal.magnitude import candidate, decision, mapped_root
from soam.temporal.runner import tensor_hash


def test_explicit_magnitudes_are_sign_invariant_and_not_labels():
    model = candidate("GN32", 13103)
    h = torch.randn(3, 32)
    a = torch.randn(3, 3)
    m = torch.ones(3, 12, dtype=torch.bool)
    sd = torch.full((3, 1), 0.01)
    pred = model.readout(h)
    r = torch.randn(3, 12)
    x, _ = model.gate_features(h, a, pred + r, m, sd)
    y, _ = model.gate_features(h, -a, pred - r, m, sd)
    assert torch.allclose(x[:, -2:], y[:, -2:])
    assert torch.allclose(x[:, -2], (r.square().mean(-1) + 1e-12).sqrt())
    assert torch.allclose(x[:, -1], a.norm(dim=-1))
    with torch.no_grad():
        model.gate.weight[0, -2] = -2
    small = torch.sigmoid(model.gate(model.gate_features(h, a, pred + 0.1 * r, m, sd)[0]))
    large = torch.sigmoid(model.gate(x))
    assert (small > large).all()


def test_metadata_and_motion_inputs_remain_independent():
    model = candidate("AMN32", 13103)
    h = torch.randn(3, 32)
    a = torch.randn(3, 3)
    q = torch.tensor([[0.0, 1.0]]).repeat(3, 1)
    p, b = model.predict(h, a, q)
    assert b.eq(1).all()
    with torch.no_grad():
        model.gate.weight[0, -1] = 3
    pp, bb = model.predict(h, a, q)
    assert torch.equal(p, pp) and torch.equal(b, bb)
    with torch.no_grad():
        model.motion.weight[0, -1] = 2
    _, bb = model.predict(h, a, q)
    assert (bb > 1).all()
    meta = candidate("GMN32", 13103)
    m = torch.ones(3, 12, dtype=torch.bool)
    z = torch.randn(3, 12)
    f, _ = meta.gate_features(h, a, z, m, torch.full((3, 1), 0.1))
    assert f[:, -1].eq(0.1).all()


def test_fresh_data_and_matched_core_initialization():
    root = mapped_root(14207)
    assert root != 14207 and root == mapped_root(14207) and root != mapped_root(14221)
    a = generate("confirmation", root, batch=2, horizon=8)
    b = generate("confirmation", 12007, batch=2, horizon=8)
    assert not torch.equal(a.target, b.target)
    old, new = candidate("GA32", 13103), candidate("GN32", 13103)
    assert torch.equal(old.W.weight, new.W.weight) and torch.equal(old.E.weight, new.E.weight)
    assert new.resources()["fitted_scalars"] - old.resources()["fitted_scalars"] == 2


def test_no_write_causal_rollout_and_exact_fitting():
    torch.set_num_threads(1)
    data = training_data(mapped_root(13003), updates=3, batch=2, horizon=8, split="fixture")
    a, b = candidate("GN32", 13003), candidate("GN32", 13003)
    fa = fit(a, data, 0.003, lambda: None)
    fb = fit(b, data, 0.003, lambda: None)
    assert tensor_hash(a.state_dict()) == tensor_hash(b.state_dict()) and fa["trace"] == fb["trace"]
    before = tensor_hash(a.state_dict())
    rollout(a, data[0].evidence)
    assert tensor_hash(a.state_dict()) == before


def test_supplement_decision_does_not_relabel_v1_controls():
    base = [
        {"J": 0.1, "clean": 0.01, "corrupt": 0.02, "change": 0.03, "free32": 0.02}
        for _ in range(10)
    ]
    good = [{**row, "J": 0.08} for row in base]
    d = decision({"GN32": good, "PC32": base, "GA32": base})
    assert d["outcome"] == "supported" and "GA32/gain" in d["comparisons"]
    assert "MIX32/gain" not in d["comparisons"]
