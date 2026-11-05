"""Scientific integrity checks on fixture streams, not confirmation trials."""

import itertools
import json
from dataclasses import fields, replace
from types import MethodType

import numpy as np
import pytest
import torch

from soam.encoders.projection import FixedProjection
from soam.handover.data import ObservationPacket, generate_episode, load_episode
from soam.handover.evaluation import Interaction, effective_packet, run_episode
from soam.handover.models import HandoverModel, Work
from soam.handover.probes import run_probes
from soam.handover.protocol import initialization_seed, rng, templates, tensor_fingerprint
from soam.handover.runner import SmokeConfig, compare_runs, run_smoke, save_arrays
from soam.handover.training import (
    learned_state,
    load_learned,
    observed_batch,
    pose_loss,
    selector_loss,
)


@pytest.fixture(autouse=True)
def deterministic_cpu():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def empty_packet(action=0.0):
    return ObservationPacket(
        torch.zeros(2, 12), torch.zeros(2, dtype=torch.bool), torch.zeros(16), False, action
    )


def state_fingerprint(state):
    return tensor_fingerprint(state.tensors()), state.attended, state.initialized


def test_packet_contract_and_action_timing():
    episode = generate_episode()
    assert {f.name for f in fields(ObservationPacket)} == {
        "z",
        "valid",
        "cue",
        "cue_present",
        "executed_action_previous",
    }
    assert episode.packets[0].executed_action_previous == 0
    for t, packet in enumerate(episode.packets):
        packet.validate()
        assert not packet.z[~packet.valid].count_nonzero()
        if t:
            assert packet.executed_action_previous == float(episode.actions[t - 1])
    for onset in (0, 48, 96, 144):
        support = episode.packets[onset].cue != 0
        assert support.sum() == 8
        for t in range(onset, onset + 4):
            assert torch.equal(episode.packets[t].cue != 0, support)
    assert episode.packets[43].valid.tolist() == [True, True]
    assert episode.packets[48].valid.tolist() == [True, False]
    assert episode.packets[96].valid.tolist() == [False, True]
    bad = replace(empty_packet(), z=torch.ones(2, 12))
    with pytest.raises(ValueError, match="masked"):
        bad.validate()


def test_conditions_are_paired_and_labels_are_presented_not_ideal():
    baseline = generate_episode()
    for condition in (2, 3, 4, 5, 6):
        changed = generate_episode(condition=condition)
        assert torch.equal(baseline.actions, changed.actions)
        assert torch.equal(baseline.phases, changed.phases)
        if condition != 6:
            for a, b in zip(baseline.packets, changed.packets):
                visible = a.valid & b.valid
                assert torch.equal(a.z[visible], b.z[visible])
    no_cue = generate_episode(condition=2)
    assert no_cue.presented.unique().tolist() == [0]
    assert no_cue.requested[48] == 1
    assert not any(p.cue_present for p in no_cue.packets[4:])
    shuffled = generate_episode(condition=3)
    assert shuffled.presented[48] == 0 and shuffled.requested[48] == 1
    unsupported = generate_episode(condition=4)
    assert unsupported.presented[120] == 2 and unsupported.requested[120] == 0
    coordinate = generate_episode(condition=1)
    difference = torch.remainder(coordinate.phases[:, 1] - coordinate.phases[:, 0], 2 * np.pi)
    torch.testing.assert_close(
        difference, torch.full_like(difference, np.pi / 3), atol=1e-12, rtol=0
    )
    mismatch = HandoverModel("G2", condition=7)
    assert float(mismatch.gains[1]) == pytest.approx(0.7)


def test_seed_separation_and_no_global_rng_side_effects():
    draws = [
        rng(11, split, 0, 0, "actions").normal(size=5)
        for split in ("train", "development", "confirmation", "fixture")
    ]
    assert len({x.tobytes() for x in draws}) == 4
    assert np.array_equal(draws[-1], rng(11, "fixture", 0, 0, "actions").normal(size=5))
    before = torch.random.get_rng_state().clone()
    models = [HandoverModel(name) for name in ("G2", "GS24", "GS9")]
    assert torch.equal(torch.random.get_rng_state(), before)
    for other in models[1:]:
        for name, value in learned_state(models[0], "selector").items():
            assert torch.equal(value, learned_state(other, "selector")[name])
    assert len({initialization_seed(11, name) for name in ("selector", "G2", "GS24", "GS9")}) == 4
    with pytest.raises(ValueError, match="fixture budget"):
        generate_episode(index=2)


@pytest.mark.parametrize(
    "variant,count,width",
    [("A2", 0, 40), ("A1", 0, 28), ("G2", 3699, 40), ("GS24", 7059, 40), ("GS9", 3819, 25)],
)
def test_candidate_counts_no_write_and_snapshot_isolation(variant, count, width, monkeypatch):
    model = HandoverModel(variant)
    monkeypatch.setattr(
        FixedProjection, "diagnostic_inverse", lambda *a: pytest.fail("learner inverse")
    )
    assert model.resources()["trainable_parameters"] == count
    assert model.resources()["recurrent_floats"] == width
    before_weights = model.persistent_fingerprint()
    episode = generate_episode()
    state = model.initial_state()
    original = state_fingerprint(state)
    next_state, estimates, _ = model.step(state, episode.packets[0])
    assert state_fingerprint(state) == original
    before = state_fingerprint(next_state)
    prediction = model.predict(next_state, episode.actions[:8])
    torch.testing.assert_close(
        prediction, model.predict(next_state, episode.actions[:8]), atol=0, rtol=0
    )
    assert state_fingerprint(next_state) == before
    assert model.persistent_fingerprint() == before_weights
    assert estimates.shape == (2, 12) and prediction.shape == (8, 2, 12)
    # Different truth and future observations cannot alter prediction from the snapshot.
    episode.phases.fill_(1000)
    episode.true_features.fill_(-999)
    episode.packets[1].z.fill_(123)
    torch.testing.assert_close(
        prediction, model.predict(next_state, episode.actions[:8]), atol=0, rtol=0
    )


@pytest.mark.parametrize("variant", ["A2", "G2"])
def test_independent_banks_do_not_alias_or_share_correction(variant):
    model = HandoverModel(variant)
    state = model.initial_state()
    state.initialized = True
    packet = generate_episode().packets[20]
    altered = replace(packet, z=packet.z.clone())
    altered.z[1] += 0.3
    first, _, _ = model.step(state, packet)
    second, _, _ = model.step(state, altered)
    torch.testing.assert_close(first.pose[0], second.pose[0], rtol=0, atol=0)
    assert not torch.equal(first.pose[1], second.pose[1])
    before = first.pose[1].clone()
    first.pose[0].fill_(777)
    assert torch.equal(first.pose[1], before)
    assert torch.equal(state.pose, model.initial_state().pose)


def test_key_energy_gradient_and_ring_recovery_without_sensory_truth():
    model = HandoverModel("A2")
    p = templates().double()
    torch.testing.assert_close(p.T @ p, torch.eye(3, dtype=torch.float64), atol=0, rtol=0)
    q = torch.linspace(-0.2, 0.5, 16, requires_grad=True)
    energy = model.key_energy(q)
    (derivative,) = torch.autograd.grad(energy, q)
    updated = model.key_substep(q, coupled=False)
    torch.testing.assert_close(updated, q - 0.1 * derivative, atol=1e-7, rtol=1e-6)
    key = model.patterns[:, 0] * 0.5
    energies = []
    for _ in range(80):
        energies.append(float(model.key_energy(key)))
        key = model.key_substep(key, coupled=False)
    assert max(b - a for a, b in itertools.pairwise(energies)) < 2e-6
    pose = 0.5 * model.encoder(torch.tensor([1.0, 0.0]))
    for _ in range(16):
        pose = model.ring(pose, 0.08, model.gains[0])
    expected = model.encoder(
        torch.tensor([np.cos(16 * 0.08), np.sin(16 * 0.08)], dtype=torch.float32)
    )
    torch.testing.assert_close(pose, expected, atol=1e-5, rtol=1e-5)


def test_initial_observation_is_not_propagated_or_assimilated_twice():
    model = HandoverModel("A2")
    packet = generate_episode().packets[0]
    state, _, _ = model.step(model.initial_state(), packet)
    torch.testing.assert_close(
        state.pose[0], 0.75 * model.pose_prior + 0.25 * packet.z[0], atol=0, rtol=0
    )
    torch.testing.assert_close(state.pose[1], model.pose_prior, atol=0, rtol=0)
    propagated, _, _ = model.step(state, empty_packet(0.1))
    for bank in range(2):
        torch.testing.assert_close(
            propagated.pose[bank],
            model.ring(state.pose[bank], 0.1, model.gains[bank]),
            atol=0,
            rtol=0,
        )


def test_three_frame_policy_and_unsupported_key_have_separate_authority():
    model = HandoverModel("A2")
    state = model.initial_state()
    state.localized[:] = True
    state.evidence_age[:] = 0
    estimates = model.pose_prior.expand(2, 12) * 10
    state.weights = torch.tensor([0.0, 1.0, 0.0])
    state.consecutive[1] = 2
    model.select(state, estimates)
    assert state.attended == -1
    state.consecutive[1] = 3
    model.select(state, estimates)
    assert state.attended == 1
    state.weights = torch.tensor([0.0, 0.0, 1.0])
    state.consecutive[:] = torch.tensor([0, 0, 4])
    model.select(state, estimates)
    assert state.attended == 1
    assert model.diagnostics(state, torch.ones(2, dtype=torch.bool))["key_winner"] == 2


@pytest.mark.parametrize("variant", ["A2", "G2"])
def test_equal_history_reconstruction_matches_full_prefix(variant):
    model = HandoverModel(variant)
    episode = generate_episode()
    online = Interaction(model)
    replay = Interaction(model, "equal_history_replay")
    for t, packet in enumerate(episode.packets[:60]):
        state, _, _ = online.step(packet)
        replay.history.append(packet.clone())
        if t in (2, 20, 50, 59):
            for bank in range(2):
                reconstructed, work = replay.reconstruct(bank)
                torch.testing.assert_close(reconstructed, state.pose[bank], atol=1e-6, rtol=1e-6)
                assert work.replay_packets == t + 1


@pytest.mark.parametrize(
    "mode,event",
    [
        ("cold", "cold_reset"),
        ("equal_history_replay", "replay"),
        ("source_transport", "source_transport"),
    ],
)
def test_repeated_handover_controls_log_operations_and_keep_source(mode, event):
    model = HandoverModel("A2")
    episode = generate_episode()
    interaction = Interaction(model, mode)
    kinds, commits = [], []
    for packet in episode.packets:
        old = interaction.state.clone()
        state, _, diagnostics = interaction.step(packet)
        for item in diagnostics["events"]:
            kinds.append(item["kind"])
            if item["kind"] == "commit":
                commits.append(item["bank"])
                if old.attended >= 0:
                    expected, _ = model.pose_transition(
                        old.pose[old.attended], packet, True, old.attended
                    )
                    torch.testing.assert_close(state.pose[old.attended], expected, atol=0, rtol=0)
    assert commits == [0, 1, 0, 1]
    assert kinds.count(event) == 3


def test_gru_history_control_dispatch_with_declared_test_selector():
    model = HandoverModel("G2")

    # Test double isolates controller dispatch; it is never used in runner/scientific evidence.
    def key_transition(self, key, weights, cue, present):
        if present:
            target = int((self.patterns.T @ cue).argmax())
            weights = torch.nn.functional.one_hot(torch.tensor(target), 3).float()
        return key.clone(), weights.clone(), weights.clone(), Work()

    model.key_transition = MethodType(key_transition, model)
    with torch.no_grad():
        model.pose_readout.weight.zero_()
        model.pose_readout.bias.copy_(model.encoder.matrix[:, 0])
    episode = generate_episode()
    original = model.persistent_fingerprint()
    for mode in ("cold", "equal_history_replay"):
        interaction = Interaction(model, mode)
        commits = []
        for packet in episode.packets:
            _, _, diagnostics = interaction.step(packet)
            commits.extend(e["bank"] for e in diagnostics["events"] if e["kind"] == "commit")
        assert commits == [0, 1, 0, 1]
    assert model.persistent_fingerprint() == original


def test_sensory_ablation_and_oracle_preserve_available_information():
    episode = generate_episode()
    packet = episode.packets[20]
    ablated = effective_packet(packet, 20, "no_sensing_after_15")
    assert not ablated.valid.any() and not ablated.z.any()
    assert packet.valid.all()  # Source packet remains intact.
    oracle = generate_episode(oracle=True)
    torch.testing.assert_close(oracle.packets[48].cue, templates()[:, 1], atol=0, rtol=0)
    assert torch.equal(oracle.phases, episode.phases)
    assert torch.equal(oracle.packets[48].z, episode.packets[48].z)


@pytest.mark.parametrize("variant", ["G2", "GS24", "GS9"])
def test_training_gradients_use_observed_features_and_keep_components_separate(variant):
    model = HandoverModel(variant)
    episode = generate_episode()
    # A short prefix of the existing fixture exercises BPTT, not a measured training fit.
    episode = replace(
        episode,
        packets=episode.packets[:5],
        actions=episode.actions[:4],
        presented=episode.presented[:5],
    )
    batch = observed_batch([episode])
    loss = pose_loss(model, batch)
    loss.backward()
    for name, p in model.named_parameters():
        if name.startswith("pose_"):
            assert p.grad is not None and torch.isfinite(p.grad).all()
        else:
            assert p.grad is None
    original = loss.detach().clone()
    episode.phases.fill_(999)
    episode.requested.fill_(2)
    episode.true_features.fill_(-100)
    torch.testing.assert_close(
        pose_loss(model, observed_batch([episode])), original, atol=0, rtol=0
    )
    model.zero_grad(set_to_none=True)
    selector_loss(model, batch).backward()
    for name, p in model.named_parameters():
        if name.startswith("selector"):
            assert p.grad is not None and torch.isfinite(p.grad).all()
        else:
            assert p.grad is None


def test_checkpoint_loading_preserves_condition_specific_fixed_gains():
    original = HandoverModel("GS9")
    other = HandoverModel("GS9", condition=1)
    load_learned(other, learned_state(original))
    assert other.gains.tolist() == [1.0, 1.0]
    bad = learned_state(original)
    bad["pose_readout.bias"] = torch.zeros(1)
    before = other.persistent_fingerprint()
    with pytest.raises(ValueError, match="invalid checkpoint"):
        load_learned(other, bad)
    assert other.persistent_fingerprint() == before


def test_probe_matrix_and_expected_restoring_ablation_effects():
    rows, arrays = run_probes()
    assert len(rows) == 30
    assert {r["variant"] for r in rows} == {"A2", "G2", "key_passive_leak", "ring_lambda_zero"}
    for row in rows:
        if row["kind"] == "ring" and row["variant"] == "A2":
            assert row["radial_error"] < 0.01 and row["orthogonal_error"] < 0.01
            assert row["phase_error_from_own_trajectory"] < 0.01
    passive = [r for r in rows if r["variant"] == "ring_lambda_zero" and r["perturbation"] == 0]
    assert all(r["radial_error"] > 0.49 for r in passive)
    assert all(torch.isfinite(x).all() for x in arrays.values())


def test_packet_archive_roundtrip_is_exact(tmp_path):
    episode = generate_episode()
    path = tmp_path / "packets.npz"
    save_arrays(path, episode.arrays())
    restored = load_episode(path)
    assert restored.fingerprint() == episode.fingerprint()
    assert [p.executed_action_previous for p in restored.packets] == [
        p.executed_action_previous for p in episode.packets
    ]


def test_failed_events_are_scored_and_not_deleted():
    model = HandoverModel("G2")
    result = run_episode(model, generate_episode())
    assert len(result["metrics"]["events"]) == 3
    assert all(np.isfinite(e["continuity_nmse"]) for e in result["metrics"]["events"])
    assert result["metrics"]["abstention_frames"] == 192
    assert all(e["censored_delay"] == 16 for e in result["metrics"]["events"])


def test_runner_rejects_nonfixture_and_refuses_overwrite(tmp_path):
    for change in ({"split": "confirmation"}, {"seed": 23}, {"episodes_per_condition": 3}):
        with pytest.raises(ValueError):
            SmokeConfig(**change).validate()
    with pytest.raises(FileExistsError):
        run_smoke(SmokeConfig(), tmp_path)


def test_failure_status_preserves_partial_output(tmp_path, monkeypatch):
    from soam.handover import runner

    def failure(*args, **kwargs):
        raise RuntimeError("injected integrity failure")

    monkeypatch.setattr(runner, "run_episode", failure)
    output = tmp_path / "failed"
    with pytest.raises(RuntimeError, match="injected"):
        run_smoke(SmokeConfig(), output)
    status = json.loads((output / "status.json").read_text())
    assert status["status"] == "failed" and status["completed_episode_cells"] == 0
    assert (output / "provenance.json").is_file()


def test_reproduction_checker_detects_numeric_change(tmp_path):
    first, second = tmp_path / "first", tmp_path / "second"
    for path in (first, second):
        path.mkdir()
        for name in ("config", "manifest", "deterministic", "probes"):
            (path / f"{name}.json").write_text("{}")
        (path / "provenance.json").write_text(json.dumps({"source_sha256": "same"}))
        np.savez(path / "data.npz", x=np.array([1.0, 2.0]))
    assert compare_runs(first, second)["exact_numeric_match"]
    np.savez(second / "data.npz", x=np.array([1.0, 3.0]))
    with pytest.raises(AssertionError, match="numeric reproduction"):
        compare_runs(first, second)


def test_single_state_control_cannot_claim_concurrent_tracking():
    model = HandoverModel("A1")
    state = model.initial_state()
    state.attended = 0
    state.localized[:] = True
    state.weights = torch.tensor([1.0, 0.0, 0.0])
    diagnostic = model.diagnostics(state, torch.tensor([False, True]))
    assert diagnostic["roles"] == ["attended", "primed", "primed"]
    assert not diagnostic["source_capacity"]


def test_protocol_rejects_silent_numeric_amendment(tmp_path):
    from soam.handover.protocol import MANIFEST, load_protocol

    changed = json.loads(MANIFEST.read_text())
    changed["attractor"]["cue_gain"] = 9
    path = tmp_path / "altered.json"
    path.write_text(json.dumps(changed))
    with pytest.raises(ValueError, match="versioned amendment"):
        load_protocol(path)


def test_live_replay_commits_match_pretracking_and_costs_are_separate():
    model = HandoverModel("A2")
    live = Interaction(model)
    replay = Interaction(model, "equal_history_replay")
    checked = 0
    for packet in generate_episode().packets:
        online, _, _ = live.step(packet)
        reconstructed, _, diagnostics = replay.step(packet)
        for event in diagnostics["events"]:
            if event["kind"] == "replay":
                bank = event["bank"]
                torch.testing.assert_close(
                    online.pose[bank], reconstructed.pose[bank], atol=1e-6, rtol=1e-6
                )
                assert diagnostics["work"]["replay_packets"] == len(replay.history)
                assert diagnostics["work"]["state_resets"] == 1
                assert diagnostics["replay_seconds"] >= 0
                assert diagnostics["key_seconds"] >= 0
                checked += 1
    assert checked == 3


@pytest.mark.parametrize(
    "variant,component", [("G2", "selector"), ("G2", "pose"), ("GS24", "pose"), ("GS9", "pose")]
)
def test_fitter_dispatch_on_mocked_fixture_batch_only(variant, component, monkeypatch):
    from soam.handover import training
    from soam.handover.protocol import load_protocol

    fixture = generate_episode()
    fixture = replace(
        fixture,
        packets=fixture.packets[:5],
        actions=fixture.actions[:4],
        presented=fixture.presented[:5],
    )
    config = load_protocol()
    config["training"]["steps_per_fit"] = 2
    config["training"]["batch_episodes"] = 1
    monkeypatch.setattr(training, "load_protocol", lambda: config)
    # No train/development/confirmation episode is generated in this optimizer unit test.
    monkeypatch.setattr(training, "generate_episode", lambda *args: fixture)
    model = HandoverModel(variant)
    frozen_component = "pose" if component == "selector" else "selector"
    frozen = learned_state(model, frozen_component)
    changed = learned_state(model, component)
    callbacks = []
    result = training.fit_component(
        model, component, 11, lambda state, history, status: callbacks.append(status)
    )
    assert result["steps"] == 2 and callbacks[-1] == "complete"
    assert any(
        not torch.equal(value, learned_state(model, component)[name])
        for name, value in changed.items()
    )
    assert all(
        torch.equal(value, learned_state(model, frozen_component)[name])
        for name, value in frozen.items()
    )


def test_failed_fit_records_exposure_without_claiming_completed_updates(monkeypatch):
    from soam.handover import training

    fixture = generate_episode()
    monkeypatch.setattr(training, "generate_episode", lambda *args: fixture)
    monkeypatch.setattr(training, "selector_loss", lambda *args: torch.tensor(float("nan")))
    model = HandoverModel("G2")
    before = model.persistent_fingerprint()
    callbacks = []
    with pytest.raises(FloatingPointError, match="training loss"):
        training.fit_component(
            model,
            "selector",
            11,
            lambda state, progress, status: callbacks.append((progress, status)),
        )
    progress, status = callbacks[-1]
    assert status == "failed" and progress["completed_steps"] == 0
    assert progress["attempted_steps"] == 1 and progress["generated_episode_presentations"] == 8
    assert progress["unique_derived_episode_ids"]
    assert model.persistent_fingerprint() == before
