"""Numerical fixtures only: no fitting or evidence for the E1 hypothesis."""

import pytest
import torch

from soam.platform.core import Command, Observation, freeze, model_fingerprint, predict
from soam.shared.models import Candidate, TiedStateCandidate, manifest

COUNTS = {
    "S32": (3868, 34),
    "D25": (3849, 52),
    "D16": (2040, 34),
    "G28": (3988, 30),
    "G32": (4940, 34),
    "SYM32": (1884, 34),
    "L12": (924, 14),
}


def observation(role, batch=2, initial=True):
    z = torch.linspace(-0.4, 0.4, 12, dtype=torch.float32).repeat(batch, 1)
    valid = torch.ones_like(z, dtype=torch.bool)
    valid[:, 6:] = False
    z[~valid] = 0
    cue = torch.zeros(batch, 2, dtype=torch.float32)
    if initial:
        cue[:, role] = 1
    return Observation(z, valid, cue, torch.full_like(cue, initial, dtype=torch.bool))


def command(role, batch=2):
    a = torch.tensor([[0.2, -0.3, 0.4]], dtype=torch.float32).repeat(batch, 1)
    return Command(a if role else a * 0)


@pytest.mark.parametrize("name", COUNTS)
def test_manifest_counts_precision_reproducibility_and_no_global_rng_changes(name):
    before = torch.random.get_rng_state().clone()
    # Construction must not depend on the caller's default numerical precision.
    old_dtype = torch.get_default_dtype()
    try:
        torch.set_default_dtype(torch.float64)
        model = Candidate(name, 17)
    finally:
        torch.set_default_dtype(old_dtype)
    assert torch.equal(before, torch.random.get_rng_state())
    assert all(p.dtype == torch.float32 for p in model.parameters())
    count, width = COUNTS[name]
    assert sum(p.numel() for p in model.parameters()) == count
    assert model.initial_state(2).shape == (2, width)
    assert model_fingerprint(model) == model_fingerprint(Candidate(name, 17))
    assert len(manifest()["models"]) == 7


@pytest.mark.parametrize("name", COUNTS)
@pytest.mark.parametrize("role", [0, 1])
def test_snapshot_prediction_preserves_parameters_state_and_commands(name, role):
    model = Candidate(name, 19)
    initial = model.initial_state(2)
    state = model.assimilate(initial, observation(role))
    state_before = state.clone()
    cmd = command(role)
    action_before = cmd.action.clone()
    before = model_fingerprint(model)
    trace = predict(freeze(model, state), [cmd] * 3)
    assert trace.features.shape == (3, 2, 12)
    assert torch.equal(state, state_before)
    assert torch.equal(cmd.action, action_before)
    assert initial.count_nonzero() == 0
    assert model_fingerprint(model) == before
    expected = state
    for _ in range(3):
        expected = model.advance(expected, cmd)
    assert torch.equal(trace.features[-1], model.readout(expected))
    # Generic fixture work estimates are deliberately not treated as E1 accounting.


def test_packed_symmetry_and_independent_dense_action_formula():
    model = Candidate("S32", 5)
    bank = model.bank
    with torch.no_grad():
        bank.b.fill_(0.03)
        bank.v.fill_(0.07)
    s, skew = bank.matrices()
    assert torch.equal(s, s.T)
    assert torch.equal(skew, -skew.transpose(1, 2))
    assert skew.diagonal(dim1=1, dim2=2).count_nonzero() == 0
    assert torch.equal(s.diag(), torch.full((32,), 0.5))
    for role in (0, 1):
        state = model.assimilate(model.initial_state(2), observation(role))
        cmd = command(role)
        rows = []
        for h, a in zip(state[:, :-2], cmd.action):
            w = s.clone()
            if role:
                w = w + skew[0] + a[0] * skew[1] + a[1] * skew[2] + a[2] * skew[3]
            rows.append(0.5 * h + 0.5 * torch.tanh(w @ h + bank.U @ a + bank.b + role * bank.v))
        actual = model.advance(state, cmd)
        torch.testing.assert_close(actual[:, :-2], torch.stack(rows), atol=1e-7, rtol=1e-6)
        assert torch.equal(actual[:, -2:], state[:, -2:])
    model.readout(actual).square().sum().backward()
    assert bank.S.grad.abs().sum() > 0
    assert (bank.A.grad.abs().sum(1) > 0).all()


@pytest.mark.parametrize("name", COUNTS)
def test_role_cues_and_lesions_cannot_change_authority(name):
    model = Candidate(name, 1)
    state = model.initial_state(2)
    with pytest.raises(ValueError, match="initial role"):
        model.assimilate(state, observation(0, initial=False))
    state = model.assimilate(state, observation(0))
    corrected = model.assimilate(state, observation(0, initial=False))
    assert torch.equal(corrected[:, -2:], state[:, -2:])
    with pytest.raises(ValueError, match="contradictory"):
        model.assimilate(state, observation(1))
    with pytest.raises(ValueError, match="zero recall"):
        model.advance(state, command(1))
    mask = torch.zeros(model.spec.width, dtype=torch.bool)
    mask[-1] = True
    with pytest.raises(ValueError, match="role flags"):
        model.advance(state, command(0), clamp_units=mask)
    obs = observation(0)
    obs.cue_valid[:, 1] = False
    with pytest.raises(ValueError, match="partial role"):
        model.assimilate(state, obs)


@pytest.mark.parametrize("name", ["D16", "D25"])
def test_disjoint_banks_have_no_parameter_aliases_or_inactive_execution(name, monkeypatch):
    model = Candidate(name, 2)
    recall = {p.data_ptr() for p in model.recall.parameters()}
    transition = {p.data_ptr() for p in model.transition.parameters()}
    assert recall.isdisjoint(transition)

    def forbidden(*args):
        pytest.fail("inactive bank executed")

    for operation in ("correction", "advance", "readout"):
        monkeypatch.setattr(model.transition, operation, forbidden)
    state = model.assimilate(model.initial_state(2), observation(0))
    state = model.advance(state, command(0))
    model.readout(state)
    assert state[:, model.n : -2].count_nonzero() == 0
    state[:, model.n] = 1
    with pytest.raises(ValueError, match="inactive"):
        model.check_state(state)


@pytest.mark.parametrize("role", [0, 1])
def test_tied_state_exact_equivalence_and_selective_bank_clamp(role):
    source = Candidate("S32", 3)
    tied = TiedStateCandidate(source)
    assert tied.bank is source.bank
    assert sum(p.numel() for p in tied.parameters()) == 3868
    assert tied.initial_state(2).shape == (2, 66)
    state = source.assimilate(source.initial_state(2), observation(role))
    other = tied.assimilate(tied.initial_state(2), observation(role))
    mask = torch.zeros(66, dtype=torch.bool)
    mask[(1 - role) * 32 : (1 - role) * 32 + 4] = True
    source_mask = torch.zeros(34, dtype=torch.bool)
    source_mask[:4] = True
    active_mask = torch.zeros(66, dtype=torch.bool)
    active_mask[role * 32 : role * 32 + 4] = True
    for _ in range(8):
        state = source.advance(state, command(role))
        other = tied.advance(other, command(role), clamp_units=mask)
        assert torch.equal(source.readout(state), tied.readout(other))
    clamped_source = source.advance(state, command(role), clamp_units=source_mask)
    clamped_tied = tied.advance(other, command(role), clamp_units=active_mask)
    assert torch.equal(source.readout(clamped_source), tied.readout(clamped_tied))
    assert clamped_tied[:, role * 32 : role * 32 + 4].count_nonzero() == 0


def test_bilinear_feature_order_and_recall_hold():
    model = Candidate("L12", 0)
    with torch.no_grad():
        model.L[:, :12] = torch.eye(12)
        model.B[:, :12] = torch.eye(12)
        for j in range(3):
            model.B[:, 12 * (j + 1) : 12 * (j + 2)] = (j + 2) * torch.eye(12)
        model.B[:, -1] = 0.1
    state = model.assimilate(model.initial_state(2), observation(1))
    a = command(1)
    actual = model.advance(state, a)
    scale = 1 + 2 * a.action[:, :1] + 3 * a.action[:, 1:2] + 4 * a.action[:, 2:3]
    torch.testing.assert_close(actual[:, :-2], state[:, :-2] * scale + 0.1)
    recall = model.assimilate(model.initial_state(2), observation(0))
    assert torch.equal(model.advance(recall, command(0)), recall)
