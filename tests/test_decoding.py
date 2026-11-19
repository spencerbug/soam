"""D-R2 information boundaries and independently checkable diagnostic failures."""

import copy

import numpy as np
import pytest
import torch

from soam.acquisition.data import Cue, Record
from soam.acquisition.models import Core
from soam.decoding.engine import acquired_code, diagnostic, metrics, predict, stream_root
from soam.decoding.report import classify, independent_reduce
from soam.decoding.runner import validate_schedule
from soam.retrieval.data import objects, queries, tensor
from soam.retrieval.models import RetrievalMemory, decode, encode


@pytest.fixture
def core():
    torch.set_num_threads(1)
    return Core(torch.eye(8, dtype=torch.float64), torch.zeros(8, 8, dtype=torch.float64))


def example():
    return Record(tensor([1.5, -1.5] * 8), tensor([0.5, -0.5] * 4), 0.0)


def test_actual_code_uses_observation_and_reference_angle(core):
    rec = example()
    np.testing.assert_array_equal(acquired_code(core, rec)[:512], encode(rec.key, 4))
    decoded = decode(acquired_code(core, rec)[512:], 1.5)
    assert torch.max(torch.abs(decoded - rec.features)) <= 1.5 / 32
    noisy = Record(rec.key, rec.features + 0.2, 0)
    assert not torch.equal(acquired_code(core, noisy), acquired_code(core, rec))
    assert not torch.equal(
        acquired_code(core, Record(rec.key, rec.features, 0.8)), acquired_code(core, rec)
    )


@pytest.mark.parametrize("name", ["PH-FULL", "KV", "REG-LIFT"])
def test_privileged_scoring_and_target_poison_cannot_change_inference(core, name):
    rec = example()
    memory = RetrievalMemory(name, core, 0.01 if name == "REG-LIFT" else 1)
    memory.acquire(rec, grounded=True)
    fingerprint = memory.fingerprint()
    mask = torch.tensor([[True] * 8 + [False] * 8])
    cue = Cue(torch.where(mask, rec.key[None], float("nan")), mask)
    actions = torch.zeros(1, 8, dtype=torch.float64)
    first, _, _, _ = predict(memory, cue, actions)
    states = np.ones((1, 1, 768))
    codes = np.tile(acquired_code(core, rec).numpy(), (2, 8, 1))
    before_codes = codes.copy()
    normal = diagnostic(states, codes, mask.numpy()[None], np.zeros((1, 1, 8)), 1)
    poisoned = diagnostic(states, codes, mask.numpy()[None], np.full((1, 1, 8), 100), 1)
    assert not np.array_equal(normal["exact_error"], poisoned["exact_error"])
    np.testing.assert_array_equal(codes, before_codes)
    memory.state.fill_(999)
    memory.reset()
    second, _, _, _ = predict(memory, cue, actions)
    np.testing.assert_array_equal(first, second)
    assert memory.fingerprint() == fingerprint


def fixture_arrays():
    codes = np.tile(np.array([1] * 16 + [-1] * 16, dtype=np.int8), (4, 8, 8, 24))
    states = np.ones((4, 7, 8, 768))
    mask = np.tile(np.array([True] * 8 + [False] * 8), (4, 7, 8, 1))
    truth = np.zeros((4, 7, 8, 9, 8))
    a = {
        "codes": codes,
        "states": states,
        "mask": mask,
        "truth": truth,
        "PH-FULL_pred": np.full_like(truth, 1.5),
        "KV_pred": truth.copy(),
        "REG-LIFT_pred": truth.copy(),
        "cycles": np.ones((4, 7, 8), dtype=int),
        "converged": np.ones((4, 7, 8), dtype=bool),
    }
    rows = [diagnostic(states[s], codes[s], mask[s], truth[s, ..., 0, :], 1) for s in range(4)]
    a.update({k: np.stack([r[k] for r in rows]) for k in rows[0]})
    return a


def test_correct_stored_decode_with_failed_completion_and_independent_reduction():
    a = fixture_arrays()
    actual = metrics(a, 1)
    independent = independent_reduce(a, 1)
    assert actual == independent
    assert actual["PH-FULL_accuracy"] == 0
    assert actual["exact_accuracy"] == 1
    assert actual["gap"] == 1
    assert actual["same_code_discrepancy"] == 0.5


def test_all_acquired_snapshots_scored_without_best_target_selection():
    a = fixture_arrays()
    # Half the acquired relationship codes now decode incorrectly; no best-of-eight.
    a["codes"][:, :, :4, 512:] = 1
    rows = [
        diagnostic(a["states"][s], a["codes"][s], a["mask"][s], a["truth"][s, ..., 0, :], 1)
        for s in range(4)
    ]
    a.update({k: np.stack([r[k] for r in rows]) for k in rows[0]})
    assert metrics(a, 1)["exact_accuracy"] == 0.5


def test_discrepancy_excludes_clamped_bits_and_handles_zero_activity():
    codes = np.ones((2, 8, 768))
    states = np.ones((1, 1, 768))
    mask = np.ones((1, 1, 16), dtype=bool)
    states[..., :512] = -1
    r = diagnostic(states, codes, mask, np.zeros((1, 1, 8)), 1)
    assert r["same_code_discrepancy"].item() == 0
    states[..., 512:] = 0
    r = diagnostic(states, codes, mask, np.zeros((1, 1, 8)), 1)
    assert r["same_code_discrepancy"].item() == 0.25


def test_fresh_namespaced_streams_and_truth_independence():
    key = stream_root(53003)
    obj = objects(key, "evaluation", 0, 1)[0]
    assert not np.array_equal(obj[0], objects(53003, "evaluation", 0, 1)[0][0])
    assert not np.array_equal(obj[0], objects(key, "train", 0, 1)[0][0])
    cue, actions, truth = queries(obj, key, "evaluation", 0)
    changed, changed_actions, changed_truth = queries((obj[0], -obj[1]), key, "evaluation", 0)
    assert torch.equal(cue["partial"].features, changed["partial"].features)
    assert torch.equal(actions, changed_actions)
    assert not np.array_equal(truth, changed_truth)


def test_decision_requires_adequacy_gap_and_precision():
    m = {"exact_code_accuracy_min": 0.95, "gap_width_max": 0.1, "practical_gap": 0.05}
    adequate = {"lo": 0.96, "hi": 1}
    gap = {"lo": 0.06, "hi": 0.14, "width": 0.08}
    assert classify(gap, adequate, m) == "completion_path_limitation_supported"
    assert classify({**gap, "width": 0.2}, adequate, m) == "inconclusive"
    assert classify(gap, {"lo": 0.8, "hi": 0.94}, m) == "exact_decoding_inadequate"
    assert (
        classify({"lo": -0.01, "hi": 0.04, "width": 0.05}, adequate, m) == "practically_small_gap"
    )
    assert classify(gap, {"lo": 0.94, "hi": 1}, m) == "inconclusive"


def test_schedule_blocks_failed_predecessors_and_reruns():
    state = {"fixture": {"status": "complete"}}
    before = copy.deepcopy(state)
    validate_schedule("confirmation", state)
    assert state == before
    with pytest.raises(RuntimeError):
        validate_schedule("fixture", state)
    with pytest.raises(RuntimeError):
        validate_schedule("repeat", state)
    with pytest.raises(RuntimeError):
        validate_schedule("confirmation", {"fixture": {"status": "resource_stop"}})
