"""Hand-constructed scientific invariants, not a development parameter search."""

import numpy as np
import pytest
import torch

from soam.acquisition.data import Cue, Record, tensor
from soam.acquisition.models import Core
from soam.retrieval.data import objects, queries
from soam.retrieval.models import RetrievalMemory, conjugate_gradient, decode, encode, sweep


@pytest.fixture
def core():
    torch.set_num_threads(1)
    return Core(torch.eye(8, dtype=torch.float64), torch.zeros(8, 8, dtype=torch.float64))


def examples():
    # Fixed orthogonal appearance signs; no simulator truth enters the writer API.
    return [
        Record(
            tensor([1.5 * (-1) ** (j // (2**i)) for j in range(16)]),
            tensor([[0.5, -0.5, 0.25][i] * (-1) ** j for j in range(8)]),
            0.0,
        )
        for i in range(3)
    ]


def test_encoder_midpoints_and_decoder():
    x = tensor([-1.5, -0.4, 0.0, 0.5, 1.5])
    assert (decode(encode(x, 1.5), 1.5) - x).abs().max() <= 1.5 / 32
    assert torch.equal(encode(tensor([10.0]), 4), torch.ones(32, dtype=torch.float64))
    assert decode(tensor([1.0, -1.0] * 16), 1.5).item() == 0


def test_projector_and_three_association_fixture(core):
    m = RetrievalMemory("PH-FULL", core)
    encoded = []
    for rec in examples():
        m.acquire(rec, grounded=True)
        encoded.append(torch.cat((encode(rec.key, 4), encode(rec.features, 1.5))))
        p = m.buffers["projector"]
        assert torch.allclose(p, p.T, atol=1e-8, rtol=0)
        assert torch.allclose(p @ p, p, atol=1e-8, rtol=0)
        for x in encoded:
            assert torch.allclose(p @ x, x, atol=1e-8, rtol=0)
    x = torch.stack(encoded, 1)
    assert torch.allclose(p, x @ torch.linalg.pinv(x), atol=1e-8, rtol=0)
    old = p.clone()
    m.acquire(examples()[0], grounded=True)
    assert torch.equal(old, m.buffers["projector"])
    assert int(m.buffers["rank"]) == 3
    for rec in examples():
        cue = Cue(rec.key[None], torch.ones(1, 16, dtype=torch.bool))
        recalled, _, _ = m.recall(cue)
        assert (recalled[0] - rec.features).square().mean() <= 0.1
        assert (m.trace["energy"].diff(dim=0) <= 1e-8).all()


@pytest.mark.parametrize("name", ["NOWRITE", "KV", "REG", "FAST", "REG-LIFT", "PH-FULL", "PH-1"])
def test_reset_nowrite_hidden_poison_and_order(core, name):
    m = RetrievalMemory(name, core, 0.1 if name in {"REG", "REG-LIFT"} else 1.0)
    rec = examples()[0]
    m.acquire(rec, grounded=True)
    saved, original = m.snapshot(), m.fingerprint()
    mask = torch.ones(2, 16, dtype=torch.bool)
    mask[0, :8] = False
    mask[1, 8:] = False
    x = rec.key[None].repeat(2, 1)
    cue = Cue(torch.where(mask, x, float("nan")), mask)
    actions = torch.zeros(2, 8, dtype=torch.float64)
    first = m.rollout(cue, actions)[0]
    m.state.fill_(123)
    m.action_state.fill_(99)
    m.reset()
    assert not m.state.any() and not m.action_state.any() and not m.trace
    second = m.rollout(Cue(cue.features.flip(0), mask.flip(0)), actions.flip(0))[0]
    assert torch.equal(first, second.flip(0))
    assert m.fingerprint() == original
    m.restore(saved)
    assert m.fingerprint() == original
    assert m.resources()["persistent_bytes"] <= 8388608
    with pytest.raises(ValueError):
        m.acquire(rec)
    with pytest.raises(ValueError):
        m.acquire(Record(rec.key, rec.features * float("nan"), 0), grounded=True)
    assert m.fingerprint() == original


def test_one_cycle_control_and_perturbation(core):
    full = RetrievalMemory("PH-FULL", core)
    short = RetrievalMemory("PH-1", core)
    for rec in examples():
        full.acquire(rec, grounded=True)
    short.restore(full.snapshot())
    cue = Cue(examples()[0].key[None], torch.ones(1, 16, dtype=torch.bool))
    full.recall(cue)
    first = full.trace["values"][0].clone()
    assert torch.equal(short.recall(cue)[0], first)
    before = full.fingerprint()
    full.recall(cue, perturb_uniform=torch.arange(768)[None].to(torch.float64))
    assert full.fingerprint() == before
    assert full.trace["perturb_count"].item() == 13
    assert torch.equal(full.state[:, :512], encode(cue.features, 4.0))


def test_sweep_matches_naive_coordinate_law():
    w = tensor([[0, 0.4, -0.2], [0.4, 0, 0.3], [-0.2, 0.3, 0]])
    state = tensor([[1, 0, 0], [-1, 0, 0]])
    clamp = torch.tensor([[True, False, False], [True, False, False]])
    expected = state.clone()
    for i in range(3):
        for j in range(2):
            h = w[i] @ expected[j]
            if not clamp[j, i] and abs(h) > 1e-12:
                expected[j, i] = h.sign()
    result, changes, deltas = sweep(state, w, clamp, torch.ones(2, dtype=torch.bool))
    assert torch.equal(result, expected)
    assert (deltas <= 0).all() and (changes > 0).all()


def test_linear_solver_direct_equivalence():
    x = tensor([[1, 2, 3], [3, 1, 2], [2, 3, 1], [1, 1, 1]])
    a, b = x.T @ x + 0.01 * torch.eye(3, dtype=torch.float64), tensor([0.3, 0.1, 0.4])
    solution = conjugate_gradient(a, b)
    assert torch.allclose(solution, torch.linalg.solve(a, b), atol=1e-8, rtol=1e-7)
    assert torch.linalg.vector_norm(a @ solution - b) / torch.linalg.vector_norm(b) <= 1e-8


def test_fresh_streams_and_pairing_and_ambiguous_truth():
    from soam.acquisition.data import objects as historical_objects

    obj = objects(1, "fixture", 0, 1)[0]
    assert not np.array_equal(obj[0], historical_objects(1, "fixture", 0, 1)[0][0])
    assert not np.array_equal(obj[0], objects(1, "confirmation", 0, 1)[0][0])
    cues, actions, truth = queries(obj, 1, "fixture", 0)
    visible = cues["partial"].mask
    assert torch.equal(cues["partial"].features[visible], cues["full"].features[visible])
    other, acts, other_truth = queries((obj[0], -obj[1]), 1, "fixture", 0)
    assert torch.equal(cues["full"].features, other["full"].features)
    assert torch.equal(actions, acts) and not np.array_equal(truth, other_truth)


def test_full_evaluator_scoring_with_hand_constructed_failure(core, monkeypatch):
    from soam.retrieval import engine
    from soam.retrieval.report import independent_metrics

    key = tensor([1.0] * 16)
    record = Record(key, torch.zeros(8, dtype=torch.float64), 0.0)
    mask = torch.ones(8, 16, dtype=torch.bool)
    partial = mask.clone()
    partial[:, 8:] = False
    cues = {
        "full": Cue(key[None].repeat(8, 1), mask),
        "partial": Cue(key[None].repeat(8, 1) * partial, partial),
    }
    monkeypatch.setattr(engine, "objects", lambda root, split, family, count: [None] * count)
    monkeypatch.setattr(engine, "records", lambda *args: [record] * 8)
    monkeypatch.setattr(
        engine,
        "queries",
        lambda *args: (cues, torch.zeros(8, 8, dtype=torch.float64), np.ones((8, 9, 8))),
    )
    monkeypatch.setattr(engine, "core_error", lambda *args: 0.0)
    result, arrays, _, _ = engine.evaluate("KV", core, 1.0, 1, "hand-fixture", 1.0)
    metrics = result["KV"]["metrics"]["partial"]
    assert metrics["old_accuracy"] == 0
    assert metrics["accepted_wrong"] == 1
    assert metrics["known_queries"] == 224
    assert result["KV"]["distinct_grounded_snapshots"] == 448
    a = arrays["KV"]
    assert (a["d2_error"][:, :, ~a["d2_valid"]] == 0).all()
    independently = independent_metrics(a, 1.0, {"full": 1e30, "partial": 1e30})
    for condition, values in independently.items():
        for k, v in values.items():
            assert v == result["KV"]["metrics"][condition][k]


def test_manifest_inventory_and_approval_receipt():
    import hashlib

    from soam.retrieval.runner import ALLOCATION, MANIFEST, inventory, read

    m, approval = read(MANIFEST), read(ALLOCATION)
    assert len(inventory(m)) == 12
    assert len(m["confirmation_roots"]) == 10
    assert approval["manifest_sha256"] == hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
    assert approval["limits"] == m["limits"]
