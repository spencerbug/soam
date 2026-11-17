from dataclasses import fields, replace

import numpy as np
import pytest
import torch

from soam.ambiguity.data import Evidence, generate, input_hash, training_data
from soam.ambiguity.engine import fit_linear, rollout
from soam.ambiguity.models import Conventional, Recurrent, advance_support, mix_gaussian
from soam.encoders.projection import FixedProjection


@pytest.fixture(scope="module")
def fitted_c():
    return fit_linear(training_data(26001, updates=8, split="fixture"))


def test_full_permitted_history_equivalence_and_revealing_probe():
    assert {f.name for f in fields(Evidence)} == {"observed", "mask", "actions"}
    for condition, stop in [
        ("ambiguous", 49),
        ("uninformative", 49),
        ("later", 12),
        ("diagnostic", 12),
        ("delayed", 28),
    ]:
        b = generate("fixture", 26001, condition=condition)
        i, j = b.pairs.T
        assert torch.equal(b.evidence.observed[:stop, i], b.evidence.observed[:stop, j])
        assert torch.equal(b.evidence.mask[:, i], b.evidence.mask[:, j])
        assert torch.equal(b.evidence.actions[:, i], b.evidence.actions[:, j])
        assert torch.equal(b.labels[0, i], torch.zeros(len(i), dtype=b.labels.dtype))
        if stop < 49:
            assert not torch.equal(b.evidence.observed[stop, i], b.evidence.observed[stop, j])
    delayed = generate("fixture", 26001, condition="delayed")
    assert not torch.equal(
        delayed.target[20, delayed.pairs[:, 0]], delayed.target[20, delayed.pairs[:, 1]]
    )
    assert not delayed.evidence.mask[12:28].any()


def test_represented_change_and_coherent_corruption_are_identical_evidence():
    a = generate("fixture", 26001, condition="change")
    b = generate("fixture", 26001, condition="coherent")
    for f in fields(Evidence):
        assert torch.equal(getattr(a.evidence, f.name), getattr(b.evidence, f.name))
    assert not torch.equal(a.target, b.target)
    assert not torch.equal(a.labels, b.labels)


def test_all_visible_masks_identify_the_supplied_two_dimensional_family():
    b = generate("fixture", 26001)
    p = FixedProjection(12, 1729).matrix
    for mask in b.evidence.mask.reshape(-1, 12):
        if mask.any():
            assert torch.linalg.matrix_rank(p[mask]) == 2


def test_splits_repeat_and_never_share_data():
    hashes = [
        input_hash(generate(s, 26001)) for s in ("train", "development", "confirmation", "fixture")
    ]
    assert len(set(hashes)) == 4
    assert hashes[0] == input_hash(generate("train", 26001))


@pytest.mark.parametrize(
    "name",
    [
        "PC16",
        "PC32",
        "PC40",
        "TWO16",
        "ADAPT1-C",
        "ADAPT1-M",
        "FILTER2-C",
        "FILTER2-M",
        "NISEMP-C",
        "NISEMP-M",
    ],
)
def test_causality_no_write_batch_independence_and_psd(fitted_c, name):
    torch.set_num_threads(1)
    if name.startswith("PC"):
        model = Recurrent(int(name[2:]), seed=31)
    elif name == "TWO16":
        model = Recurrent(16, True, 31)
    else:
        model = Conventional(fitted_c, name.split("-")[0], name.endswith("M"))
    b = generate("fixture", 26001, pairs=2, condition="delayed")
    before = {k: v.clone() for k, v in model.state_dict().items()}
    poisoned = b.evidence.observed.clone()
    poisoned[28:] = 1e3
    with torch.no_grad():
        out = rollout(model, b.evidence, detail=True)
        changed = rollout(model, replace(b.evidence, observed=poisoned), detail=True)
        one = rollout(
            model,
            Evidence(b.evidence.observed[:, :1], b.evidence.mask[:, :1], b.evidence.actions[:, :1]),
        )
    assert torch.equal(out["candidate_prior"][:28], changed["candidate_prior"][:28])
    assert torch.equal(out["prob"][:27], changed["prob"][:27])
    assert torch.allclose(one["prob"], out["prob"][:, :1], atol=2e-5, rtol=2e-5)
    assert all(torch.equal(v, before[k]) for k, v in model.state_dict().items())
    assert all(torch.isfinite(v).all() for v in out.values())
    assert ((out["prob"] >= 0) & (out["prob"] <= 1)).all()
    if isinstance(model, Conventional):
        cov = out["state"][..., 2:6].reshape(-1, 2, 2)
        assert torch.linalg.eigvalsh(cov).min() > 0
        assert torch.allclose(cov, cov.transpose(-1, -2), atol=1e-6)


def test_likelihood_matches_dense_predictive_gaussian_before_adaptation(fitted_c):
    model = Conventional(fitted_c, "ADAPT1", True)
    b = generate("fixture", 26001, pairs=1)
    state = model.initialize(b.evidence.observed[0], b.evidence.mask[0])
    prior = model.predict(state, b.evidence.actions[0], torch.zeros(2))
    z, mask = b.evidence.observed[4].double(), b.evidence.mask[4]
    score, _, _ = model.score(prior, z, mask)
    for i in range(2):
        h = model.core.P[mask[i]]
        for j in range(2):
            c = prior[i, j, 2:6].reshape(2, 2)
            cov = h @ c @ h.T + prior[i, j, 6] * torch.eye(len(h), dtype=torch.float64)
            r = z[i, mask[i]] - model.decode(prior)[i, j, mask[i]]
            expected = -0.5 * (
                r @ torch.linalg.solve(cov, r)
                + torch.linalg.slogdet(cov)[1]
                + len(h) * np.log(2 * np.pi)
            )
            assert torch.allclose(score[i, j], expected, atol=1e-8)


def test_single_gaussian_retains_between_candidate_uncertainty():
    s = torch.tensor([[[-2.0, 0, 1, 0, 0, 1, 0.01], [2.0, 0, 1, 0, 0, 1, 0.03]]])
    out = mix_gaussian(s, torch.full((1, 2, 1), 0.5))
    assert torch.allclose(out[0, 0], torch.tensor([0.0, 0, 5, 0, 0, 1, 0.02]))
    assert torch.allclose(
        advance_support(torch.tensor([-100.0, 100.0])).sigmoid(), torch.tensor([0.01, 0.99])
    )


def test_pairwise_brier_floor_for_arbitrary_early_commitments():
    b = generate("fixture", 26001, condition="ambiguous")
    p = torch.rand(len(b.pairs))
    paired = 0.5 * (p.square() + (p - 1).square())
    assert torch.all(paired >= 0.25)


def test_fitted_maps_do_not_receive_simulator_coordinates():
    data = training_data(26001, updates=8, split="fixture")
    a = fit_linear(data)
    corrupted_truth = [replace(b, world=torch.full_like(b.world, float("nan"))) for b in data]
    c = fit_linear(corrupted_truth)
    assert all(torch.equal(v, c.state_dict()[k]) for k, v in a.state_dict().items())


def test_timed_loop_matches_archived_inference(fitted_c):
    from soam.ambiguity.report import inference_only

    ev = generate("fixture", 26001, pairs=2, condition="misleading").evidence
    for model in (
        Recurrent(16),
        Recurrent(16, True),
        Conventional(fitted_c, "ADAPT1", True),
        Conventional(fitted_c, "ADAPT1", False),
    ):
        with torch.no_grad():
            archived = rollout(model, ev, detail=True)
            state, logit = inference_only(model, ev)
        assert torch.equal(state, archived["state"][-1])
        assert torch.equal(logit.sigmoid(), archived["prob"][-1])
