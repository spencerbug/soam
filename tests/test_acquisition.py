import numpy as np
import pytest
import torch

from soam.acquisition.data import (
    Cue,
    Record,
    objects,
    projection,
    queries,
    records,
    tensor,
    training,
)
from soam.acquisition.engine import array_hash, core_error
from soam.acquisition.models import Core, Memory


def analytic_core():
    p = tensor(projection())
    return Core(p @ p.T, p @ tensor([[0.0, -1.0], [1.0, 0.0]]) @ p.T)


@pytest.mark.parametrize("name", ["NOWRITE", "KV", "REG", "FAST"])
def test_reset_and_no_write_and_restore(name):
    core = analytic_core()
    memory = Memory(name, core, 0.01 if name == "REG" else 1.0)
    obj = objects(1, "fixture", 1, 1)[0]
    blank = memory.snapshot()
    before = memory.fingerprint()
    for rec in records(obj, 1, "fixture", 1):
        memory.acquire(rec, grounded=True)
    acquired = memory.fingerprint()
    assert (acquired != before) == (name != "NOWRITE")
    cue, actions, _ = queries(obj, 1, "fixture", 1)
    first = memory.rollout(cue, actions)[0]
    memory.state.fill_(12345)
    memory.reset()
    assert not memory.state.any()
    second = memory.rollout(cue, actions)[0]
    assert torch.equal(first, second)
    assert memory.fingerprint() == acquired
    assert memory.resources()["writable_bytes"] <= 8192
    memory.restore(blank)
    assert memory.fingerprint() == before
    assert not memory.rollout(cue, actions)[0].any()


@pytest.mark.parametrize("name", ["KV", "REG", "FAST"])
def test_one_snapshot_identifiable(name):
    memory = Memory(name, analytic_core(), 1e-8 if name == "REG" else 1.0)
    k, v = objects(2, "analytic", 0, 1)[0]
    y = tensor(projection() @ v)
    memory.acquire(Record(tensor(k), y, 0.0), grounded=True)
    mask = torch.arange(16)[None] < 8
    cue = Cue(tensor(k)[None] * mask, mask)
    result, _, _ = memory.recall(cue)
    assert torch.allclose(result[0], y, atol=1e-8)
    if name == "FAST":
        q = cue.features * (16 / cue.features.square().sum())
        assert torch.equal(result, (q @ memory.buffers["w"].T)[:, 16:])


@pytest.mark.parametrize("name", ["NOWRITE", "KV", "REG", "FAST"])
def test_reject_invalid_or_ungrounded_without_writing(name):
    memory = Memory(name, analytic_core())
    rec = records(objects(3, "fixture", 0, 1)[0], 3, "fixture", 0)[0]
    before = memory.fingerprint()
    with pytest.raises(ValueError):
        memory.acquire(rec)
    with pytest.raises(ValueError):
        memory.acquire(Record(rec.key, rec.features * float("nan"), 0.0), grounded=True)
    assert before == memory.fingerprint()


def test_split_independence_and_repeat():
    a, b = training(11), training(12)
    assert all(torch.equal(x, y) for x, y in zip(a, training(11), strict=True))
    assert not torch.equal(a[0], b[0])
    train = objects(11, "train", 0, 1)[0]
    test = objects(11, "confirmation", 0, 1)[0]
    assert not np.array_equal(train[0], test[0])
    assert not np.array_equal(train[1], test[1])


def test_fitted_feature_core_and_no_simulator_input():
    data = training(13)
    core = Core.fit(data, 1e-6)
    assert core_error(core, 13, float(data[0].square().mean())) < 1e-12
    assert set(Record.__dataclass_fields__) == {"key", "features", "angle"}
    assert set(Cue.__dataclass_fields__) == {"features", "mask"}


def test_missing_values_and_query_order_do_not_leak():
    obj = objects(17, "fixture", 0, 1)[0]
    memory = Memory("FAST", analytic_core())
    memory.acquire(records(obj, 17, "fixture", 0)[0], grounded=True)
    cue, actions, _ = queries(obj, 17, "fixture", 0)
    first = memory.rollout(cue, actions)[0]
    poisoned = cue.features.clone()
    poisoned[~cue.mask] = float("nan")
    second = memory.rollout(Cue(poisoned.flip(0), cue.mask.flip(0)), actions.flip(0))[0]
    assert torch.equal(first, second.flip(0))


def test_ambiguous_same_cue_cannot_reveal_evaluator_truth():
    core = analytic_core()
    memory = Memory("KV", core)
    k, v = objects(19, "fixture", 0, 1)[0]
    memory.acquire(Record(tensor(k), tensor(projection() @ v), 0.0), grounded=True)
    cue, actions, truth = queries((k, v), 19, "fixture", 0)
    other, _, different_truth = queries((k, -v), 19, "fixture", 0)
    assert torch.equal(cue.features, other.features)
    assert not np.array_equal(truth, different_truth)
    assert torch.equal(memory.rollout(cue, actions)[0], memory.rollout(other, actions)[0])


def test_key_value_fixed_capacity_is_not_grown():
    memory = Memory("KV", analytic_core())
    for i in range(32):
        obj = objects(23, "fixture", i, 1)[0]
        memory.acquire(records(obj, 23, "fixture", i)[0], grounded=True)
    before = memory.fingerprint()
    obj = objects(23, "fixture", 32, 1)[0]
    with pytest.raises(ValueError, match="capacity"):
        memory.acquire(records(obj, 23, "fixture", 32)[0], grounded=True)
    assert memory.fingerprint() == before


def test_array_hash_includes_shape_and_contents():
    assert array_hash({"x": np.ones((2, 2))}) != array_hash({"x": np.ones(4)})


def test_fast_write_equals_normalized_online_gradient():
    memory = Memory("FAST", analytic_core(), 0.5)
    obj = objects(29, "fixture", 0, 1)[0]
    rec = records(obj, 29, "fixture", 0)[0]
    w = memory.buffers["w"].clone().requires_grad_()
    target = torch.cat((rec.key, memory.core.advance(rec.features, -rec.angle)))
    loss = 0.5 * (w @ rec.key - target).square().sum()
    loss.backward()
    expected = w.detach() - 0.5 * w.grad / rec.key.square().sum()
    memory.acquire(rec, grounded=True)
    assert torch.allclose(memory.buffers["w"], expected, atol=1e-15)
