import copy

import pytest
import torch

from soam.platform.core import Command, model_fingerprint
from soam.shared.data import SharedTask
from soam.shared.evaluation import Probe, evaluate, perturb, random_masks
from soam.shared.models import Candidate, TiedStateCandidate


@pytest.mark.parametrize("family", ["S32", "D16", "G28", "L12"])
def test_free_predictions_ignore_future_observations_and_evaluator_truth(family):
    episode = SharedTask().episode("fixture/evaluation", 9001, 0, "transition")
    model = Candidate(family, 7)
    before = model_fingerprint(model)
    a, _ = evaluate(model, episode, 0.04)
    changed = copy.deepcopy(episode)
    for obs in changed.observations[1:]:
        obs.z.fill_(3)
    changed.targets.features.fill_(5)
    changed.targets.world.fill_(-100)
    b, _ = evaluate(model, changed, 0.04)
    assert torch.equal(a["free_features"], b["free_features"])
    assert model_fingerprint(model) == before


def test_gru_equations_match_native_cell_and_preactivation_failures_surface():
    model = Candidate("G28", 5)
    episode = SharedTask().episode("fixture/evaluation", 9001, 0, "transition")
    state = model.assimilate(model.initial_state(1), episode.observations[0])
    cmd = episode.commands[0]
    native = model.gru(torch.cat((cmd.action, state[:, -2:]), 1), state[:, :-2])
    torch.testing.assert_close(model.advance(state, cmd)[:, :-2], native, rtol=0, atol=0)
    with torch.no_grad():
        model.gru.bias_ih.fill_(torch.finfo(torch.float32).max)
        model.gru.bias_hh.fill_(torch.finfo(torch.float32).max)
    with pytest.raises(FloatingPointError):
        model.advance(state, Command(torch.zeros(1, 3)))
    model = Candidate("S32", 5)
    with torch.no_grad():
        model.bank.E.fill_(torch.finfo(torch.float32).max)
    with pytest.raises(FloatingPointError):
        model.assimilate(model.initial_state(1), episode.observations[0])


def test_full_clamp_and_readout_only_have_distinct_timing():
    model = Candidate("S32", 8)
    episode = SharedTask().episode("fixture/evaluation", 9001, 0, "transition")
    intact, _ = evaluate(model, episode, 0.04)
    masked, record = evaluate(model, episode, 0.04, Probe("full_clamp", (0, 1, 2, 3)))
    readout, _ = evaluate(model, episode, 0.04, Probe("readout_clamp", (0, 1, 2, 3)))
    assert masked["anchor_state"][:, :4].count_nonzero() == 0
    assert masked["free_states"][:, :, :4].count_nonzero() == 0
    assert masked["live_states"][:, :, :4].count_nonzero() == 0
    assert torch.equal(readout["free_states"], intact["free_states"])
    assert not torch.equal(readout["free_features"], intact["free_features"])
    assert record["exposure"]["free_future_observation_reads"] == 0
    assert record["resources"]["parameters"] == 3868


@pytest.mark.parametrize("role", ["recall", "transition"])
def test_disjoint_and_tied_interventions_leave_opposite_role_unchanged(role):
    episode = SharedTask().episode("fixture/evaluation", 9001, 0, role)
    source = Candidate("S32", 1)
    source_arrays, _ = evaluate(source, episode, 0.04)
    for model in (Candidate("D16", 2), TiedStateCandidate(source)):
        offset = model.n if role == "recall" else 0
        baseline, _ = evaluate(model, episode, 0.04)
        masked, _ = evaluate(
            model, episode, 0.04, Probe("full_clamp", tuple(range(offset, offset + 4)))
        )
        assert torch.equal(baseline["free_features"], masked["free_features"])
        if model.spec.kind == "T32":
            assert torch.equal(source_arrays["free_features"], baseline["free_features"])


def test_direction_cue_and_recovery_probes_are_isolated_and_role_safe():
    model = Candidate("S32", 3)
    task = SharedTask()
    before = model_fingerprint(model)
    transition = task.episode("fixture/evaluation", 9001, 0, "transition")
    for kind in ("action_shift", "zero_A"):
        arrays, _ = evaluate(model, transition, 0.04, Probe(kind))
        assert torch.isfinite(arrays["free_features"]).all()
    recall = task.episode("fixture/evaluation", 9001, 0, "recall")
    a, _ = evaluate(model, recall, 0.04, Probe("perturb", seed=11))
    b, _ = evaluate(model, recall, 0.04, Probe("zero_S_perturb", seed=11))
    assert torch.equal(a["injected_delta"], b["injected_delta"])
    torch.testing.assert_close(a["injected_delta"].square().mean().sqrt(), torch.tensor(0.1))
    assert torch.equal(a["anchor_state"][:, -2:], torch.tensor([[1.0, 0.0]]))
    for kind in ("zero_S", "zero_cue"):
        evaluate(model, recall, 0.04, Probe(kind))
    assert model_fingerprint(model) == before
    with pytest.raises(ValueError, match="role flags"):
        evaluate(model, recall, 0.04, Probe("full_clamp", (32,)))
    masks, seed = random_masks(9001, fixture=True)
    assert (masks, seed) == random_masks(9001, fixture=True)
    assert len(masks) == 4 and all(len(set(mask)) == 4 for mask in masks)
    state = model.assimilate(model.initial_state(1), recall.observations[0])
    perturbed, _ = perturb(state, 11)
    assert torch.equal(perturbed[:, -2:], state[:, -2:])
