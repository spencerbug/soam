"""Scientific contracts for Study A, including independent recurrence checks."""

import pytest
import torch

from soam.gating.data import generate, normalization, seed, training_data
from soam.gating.engine import evaluate, fit, rollout
from soam.gating.models import Core, fold_fixed_reset
from soam.platform.core import Command
from soam.shared.models import Candidate


@pytest.fixture(autouse=True)
def deterministic():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def tensors(n=32):
    g = torch.Generator().manual_seed(77)
    return (
        torch.randn(7, n, generator=g) * 0.2,
        torch.randn(7, 3, generator=g),
        torch.tensor([[0.0, 1.0]]).expand(7, -1),
    )


def test_full_gru_matches_historical_pytorch():
    old = Candidate("G32", 42)
    new = Core("gru", 32, 42)
    h, a, q = tensors()
    torch.testing.assert_close(
        new.step(h, a, q), old.gru(torch.cat((a, q), 1), h), rtol=1e-6, atol=1e-7
    )
    torch.testing.assert_close(new.E, old.E, rtol=0, atol=0)
    torch.testing.assert_close(new.D, old.D, rtol=0, atol=0)
    assert new.costs()["parameters"] == 4940


@pytest.mark.parametrize(
    "kind,zfixed,rfixed",
    [
        ("gru", False, False),
        ("fixed_update", True, False),
        ("fixed_reset", False, True),
        ("fixed_both", True, True),
    ],
)
def test_gates_match_independent_equations(kind, zfixed, rfixed):
    m = Core(kind, 32, 42)
    h, a, q = tensors()
    x = torch.cat((a, q), 1)

    def g(k, fixed):
        return (
            getattr(m, k + "_constant").sigmoid()
            if fixed
            else (
                x @ getattr(m, k + "_W").T
                + getattr(m, k + "_bi")
                + h @ getattr(m, k + "_U").T
                + getattr(m, k + "_bh")
            ).sigmoid()
        )

    z, r = g("z", zfixed), g("r", rfixed)
    c = (x @ m.c_W.T + m.c_bi + r * (h @ m.c_U.T + m.c_bh)).tanh()
    out, diag = m.step(h, a, q, diagnostics=True)
    torch.testing.assert_close(out, z * h + (1 - z) * c)
    torch.testing.assert_close(diag["alpha"], (1 - z).expand_as(h))
    out.sum().backward()
    if zfixed:
        assert m.z_constant.grad is not None and m.z_constant.grad.abs().sum() > 0
        assert not hasattr(m, "z_W")
    if rfixed:
        assert m.r_constant.grad is not None and m.r_constant.grad.abs().sum() > 0
        assert not hasattr(m, "r_W")


def test_frozen_override_is_not_a_learned_or_dynamic_gate():
    m = Core("gru", 32, 42)
    h, a, q = tensors()
    out, d = m.step(h, a, q, overrides={"alpha": 0.0}, diagnostics=True)
    torch.testing.assert_close(out, h, atol=1e-7, rtol=1e-6)
    assert d["alpha"].count_nonzero() == 0
    _, d = m.step(h, a, q, overrides={"reset": 1.0}, diagnostics=True)
    assert (d["reset"] == 1).all()


def test_fixed_reset_folds_into_gated_leaky_core():
    m = Core("fixed_reset", 32, 42)
    with torch.no_grad():
        m.r_constant.copy_(torch.linspace(-3, 3, 32))
    folded = fold_fixed_reset(m)
    h, a, q = tensors()
    torch.testing.assert_close(m.step(h, a, q), folded.step(h, a, q), rtol=1e-5, atol=1e-7)
    assert folded.costs()["parameters"] < m.costs()["parameters"]


def test_s32_symmetry_and_initial_gated_equality():
    old = Candidate("S32", 42)
    m = Core("s32", 32, 42)
    g = Core("gated_s32", 32, 42)
    h, a, q = tensors()
    torch.testing.assert_close(
        m.step(h, a, q), old.advance(torch.cat((h, q), 1), Command(a))[:, :32], rtol=1e-6, atol=1e-7
    )
    torch.testing.assert_close(m.step(h, a, q), g.step(h, a, q), rtol=0, atol=0)
    s, sk = m.bank.matrices()
    assert torch.equal(s, s.T)
    assert torch.equal(sk, -sk.transpose(1, 2))
    g.step(h, a, q).sum().backward()
    assert g.gate.weight.grad.abs().sum() > 0


def test_rnn_equation_and_budget_matching():
    m = Core("rnn", 32, 42)
    h, a, q = tensors()
    torch.testing.assert_close(
        m.step(h, a, q), 0.5 * h + 0.5 * m.core(torch.cat((h, a, q), 1)).tanh()
    )
    full = Core("gru", 32, 42).costs()
    for kind, n in [("fixed_update", 38), ("rnn", 52)]:
        c = Core(kind, n, 42).costs()
        assert abs(c["parameters"] / full["parameters"] - 1) < 0.02
    c = Core("rnn", 55, 42).costs()
    assert abs(c["advance_readout_linear_macs"] / full["advance_readout_linear_macs"] - 1) < 0.01


def test_fresh_streams_mask_dynamics_and_split_separation():
    a, world = generate("train", 8401, 0, "transition", batch=20, horizon=32)
    b, _ = generate("train", 8401, 0, "transition", batch=20, horizon=32)
    assert torch.equal(a.clean, b.clean)
    assert (a.valid.sum(1) == 6).all() and a.z[~a.valid].count_nonzero() == 0
    assert not hasattr(a, "world")
    angle = 0.30 * a.actions[0, :, 0].double()
    x = world[0]
    expected = (
        0.98
        * torch.stack(
            (
                angle.cos() * x[:, 0] - angle.sin() * x[:, 1],
                angle.sin() * x[:, 0] + angle.cos() * x[:, 1],
            ),
            1,
        )
        + 0.03 * a.actions[0, :, 1:].double()
    )
    torch.testing.assert_close(world[1], expected, rtol=0, atol=1e-15)
    keys = {
        seed(s, 8401, 0, "transition/radius")
        for s in ("train", "development", "confirmation", "fixture", "probe_train", "diagnostic")
    }
    assert len(keys) == 6
    for split, parity in [("train", 0), ("confirmation", 1)]:
        b, _ = generate(split, 8401, 0, "transition", batch=100)
        bins = torch.floor((b.actions[..., :2] + 1) * 2).int()
        assert ((bins.sum(-1) % 2) == parity).all()


def test_free_inference_no_target_leakage_or_parameter_writes():
    r, _ = generate("fixture", 3, 0, "recall", batch=2)
    b, _ = generate("fixture", 3, 0, "transition", batch=2)
    m = Core("gru", 32, 1)
    before = {k: v.clone() for k, v in m.state_dict().items()}
    p = rollout(m, *b.inputs())["output"]
    b.clean.fill_(999.0)
    assert torch.equal(p, rollout(m, *b.inputs())["output"])
    for k, v in m.state_dict().items():
        assert torch.equal(v, before[k])
    assert len(r.inputs()) == 4


@pytest.mark.parametrize(
    "kind,width",
    [
        ("gru", 32),
        ("fixed_update", 32),
        ("fixed_reset", 32),
        ("fixed_both", 32),
        ("s32", 32),
        ("gated_s32", 32),
        ("rnn", 32),
        ("ridge", 12),
        ("pca_ridge", 2),
    ],
)
def test_tiny_fit_reproducible_and_no_write_evaluation(kind, width):
    data = training_data(8301, fixture=True, recall_updates=2, joint_updates=2, batch=2)
    a, b = Core(kind, width, 4), Core(kind, width, 4)
    fa = fit(a, data, {"lr": 0.003, "ridge": 0.0001}, lambda: None)
    fb = fit(b, data, {"lr": 0.003, "ridge": 0.0001}, lambda: None)
    for k, v in a.state_dict().items():
        assert torch.equal(v, b.state_dict()[k])
    assert fa["trace"] == fb["trace"]
    recall, _ = generate("fixture", 4, 0, "recall", batch=2)
    trans, _ = generate("fixture", 4, 0, "transition", batch=2)
    result, _ = evaluate(a, recall, trans, normalization(count=32)["variance"])
    assert all(
        torch.isfinite(torch.tensor(result[k])) for k in ("recall", "free8", "free32", "grounded32")
    )


def test_diagnostics_do_not_modify_core_and_probe_is_diagnostic_only():
    from soam.gating.diagnostics import diagnose

    m = Core("gru", 32, 42)
    before = {k: v.clone() for k, v in m.state_dict().items()}
    spec = {"diagnostic_episodes": 3, "diagnostic_horizon": 128, "probe_episodes": 4}
    values, arrays = diagnose(m, 5, normalization(count=32)["variance"], spec, lambda: None)
    assert "transition_linear_r2" in values and "recall_useful_recovery_fraction" in values
    assert arrays["transition"]["path"]["hidden"].shape == (129, 3, 32)
    for key, v in m.state_dict().items():
        assert torch.equal(v, before[key])
    q = arrays["switch"]["roles"]
    assert (q[:8, :, 0] == 1).all() and (q[8:16, :, 1] == 1).all()


def test_numerical_digest_and_budget_stop(tmp_path):
    import json

    from soam.gating.runner import Budget, digest

    a = {"x": torch.tensor([1.0]), "y": 2}
    assert digest(a) == digest({"y": 2, "x": a["x"].clone()})
    assert digest(a) != digest({"x": torch.tensor([2.0]), "y": 2})
    m = {
        "limits": {
            "cpu_seconds": 1000,
            "wall_seconds": 1000,
            "rss_bytes": 10**12,
            "artifact_bytes": 10**9,
            "fit_attempts": 1,
            "reserve_cpu_seconds": 0,
        }
    }
    b = Budget(tmp_path, m)
    b.attempt()
    with pytest.raises(TimeoutError):
        b.attempt()
    b.finish("test", "complete")
    assert json.loads((tmp_path / "ledger.json").read_text())["fit_attempts"] == 1


def test_statistics_use_roots_and_frozen_guardrails():
    import copy
    import json
    from pathlib import Path

    from soam.gating.statistics import summarize

    spec = json.loads(Path("docs/protocols/study_a_v1.json").read_text())
    records = []
    for root in spec["confirmation_roots"]:
        for name, (kind, width) in spec["variants"].items():
            error = 0.01 if name == "G32" else 0.02
            records.append(
                {
                    "root": root,
                    "model": name,
                    "metrics": dict.fromkeys(
                        ("J", "recall", "free8", "free32", "grounded32"), error
                    ),
                    "diagnostics": {},
                    "fit_cpu": 1.0,
                    "costs": Core(kind, width, 1).costs(),
                }
            )
    receipt = {"competence_pass": True, "optimization_unresolved": False}
    result = summarize(records, spec, receipt)
    assert result["outcome"] == "supported"
    assert result["contrasts"]["gain_FU38"]["adjusted"]["roots"] == [0.5] * 10
    negative = copy.deepcopy(records)
    for r in negative:
        r["metrics"] = dict.fromkeys(r["metrics"], 0.01)
    assert summarize(negative, spec, receipt)["outcome"] == "negative"
    mixed = copy.deepcopy(records)
    for r in mixed:
        if r["model"] == "G32":
            r["metrics"]["free32"] = 0.08
    assert summarize(mixed, spec, receipt)["outcome"] == "mixed"
    assert (
        summarize(records, spec, {**receipt, "optimization_unresolved": True})["outcome"]
        == "inconclusive"
    )
    with pytest.raises(ValueError):
        summarize(records[:-1], spec, receipt)
