"""Contract and failure tests; fixture accuracy is not a scientific gate."""

import json
from dataclasses import replace
from types import MethodType

import numpy as np
import pytest
import torch

from soam.platform.core import (
    BACKENDS,
    Command,
    Intervention,
    ModelSpec,
    SuppliedDynamics,
    derived_seed,
    fingerprint,
    freeze,
    model_fingerprint,
    predict,
    storage,
)
from soam.platform.evaluation import evaluate
from soam.platform.runner import (
    Budget,
    BudgetExceeded,
    FixtureConfig,
    compare_runs,
    read_arrays,
    run_suite,
)
from soam.platform.tasks import TASKS, RotationTask, TranslationTask


@pytest.fixture
def case():
    task = RotationTask()
    episode = task.episode("fixture", 9001, 0)
    model = SuppliedDynamics(ModelSpec(12, 3), 42)
    return task, episode, model


def test_stream_keys_are_stable_separate_and_do_not_touch_global_rng():
    key = ("p", 1, "train", 11, 0, "actions")
    assert derived_seed(*key) == derived_seed(*key)
    assert (
        len(
            {
                derived_seed("p", 1, s, 11, 0, c)
                for s in ("train", "dev", "test")
                for c in ("actions", "initial")
            }
        )
        == 6
    )
    before = torch.get_rng_state().clone()
    np_before = np.random.get_state()
    SuppliedDynamics(ModelSpec(8, 1), derived_seed(*key))
    TranslationTask().episode("fixture", 9001, 0)
    assert torch.equal(before, torch.get_rng_state())
    after = np.random.get_state()
    assert np.array_equal(np_before[1], after[1]) and np_before[2:] == after[2:]
    for root in (-1, True):
        with pytest.raises(ValueError):
            derived_seed("p", 1, "train", root, 0, "x")


def test_storage_distinguishes_aliases_from_clones():
    a = torch.ones(4)
    assert storage([a, a[:2]]) == {"logical_bytes": 24, "unique_storage_bytes": 16}
    assert storage([a, a.clone()]) == {"logical_bytes": 32, "unique_storage_bytes": 32}


def test_action_indexing_and_assimilation_once(case):
    task, episode, model = case
    arrays, record = evaluate(model, task, episode)
    h0 = model.assimilate(model.initial_state(1), episode.observations[0])
    expected = model.readout(model.advance(h0, episode.commands[0]))
    assert torch.equal(arrays["anchor_state"], h0)
    assert torch.equal(arrays["free_features"][0], expected)
    assert torch.equal(arrays["grounded_features"][0], expected)
    assert record["exposure"]["grounded_assimilations"] == 4
    assert record["work"]["prediction"]["assimilation_calls"] == 0
    assert record["work"]["live_linear_macs"] == 4 * 8 * 12 + 3 * (64 + 24 + 96)
    assert record["resources"]["trained_parameters"] == 0
    assert record["resources"]["peak_coexisting_model_copies"] == 3


def test_future_observations_and_truth_cannot_change_free_predictions(case):
    task, episode, model = case
    baseline, _ = evaluate(model, task, episode)
    obs = list(episode.observations)
    obs[1] = replace(obs[1], z=obs[1].z + 2)
    changed = replace(
        episode,
        observations=tuple(obs),
        targets=replace(
            episode.targets,
            features=episode.targets.features + 99,
            world=episode.targets.world - 333,
        ),
    )
    actual, _ = evaluate(model, task, changed)
    assert torch.equal(actual["free_features"], baseline["free_features"])
    assert not torch.equal(actual["grounded_features"][1], baseline["grounded_features"][1])
    changed_first = replace(episode, observations=(replace(obs[0], z=obs[0].z + 1), *obs[1:]))
    first, _ = evaluate(model, task, changed_first)
    assert not torch.equal(first["free_features"], baseline["free_features"])


def test_snapshot_isolation_in_both_directions_and_repeated_predictions(case):
    _, episode, model = case
    state = model.assimilate(model.initial_state(1), episode.observations[0])
    snap = freeze(model, state)
    baseline = predict(snap, episode.commands).features.clone()
    model.recurrent.add_(100)
    state.add_(100)
    result = predict(snap, episode.commands)
    assert torch.equal(result.features, baseline)
    result.features.zero_()
    result.states.zero_()
    assert torch.equal(predict(snap, episode.commands).features, baseline)


def test_failed_prediction_isolated_and_persistent_write_detected(case):
    _, episode, model = case

    def bad(self, state, command, *, clamp_units=None):
        self.recurrent.add_(1)
        state.add_(1)
        command.action.add_(1)
        raise ValueError("injected")

    model.advance = MethodType(bad, model)
    state = model.initial_state(1)
    before = model_fingerprint(model)
    snap = freeze(model, state)
    snap_before = model_fingerprint(snap._model)
    actions = fingerprint({str(i): c.action for i, c in enumerate(episode.commands)})
    with pytest.raises(RuntimeError, match="persistent write"):
        predict(snap, episode.commands)
    assert before == model_fingerprint(model) and snap_before == model_fingerprint(snap._model)
    assert state.count_nonzero() == 0
    assert actions == fingerprint({str(i): c.action for i, c in enumerate(episode.commands)})


def test_input_and_readout_mutation_rejected(case):
    _, episode, model = case

    def bad_readout(self, state):
        state.add_(1)
        return state @ self.decoder.T

    model.readout = MethodType(bad_readout, model)
    with pytest.raises(RuntimeError, match="readout mutated"):
        predict(freeze(model, model.initial_state(1)), episode.commands)


def test_assimilation_mutation_rejected(case):
    task, episode, model = case

    def bad(self, state, observation):
        observation.z.add_(1)
        return state.clone()

    model.assimilate = MethodType(bad, model)
    before = fingerprint(episode.observed_arrays())
    with pytest.raises(RuntimeError, match="assimilation mutated"):
        evaluate(model, task, episode)
    assert fingerprint(episode.observed_arrays()) == before


def test_masks_dimensions_and_capabilities_fail_explicitly(case):
    _, episode, model = case
    obs = replace(episode.observations[0], valid=torch.zeros(1, 12, dtype=torch.bool))
    with pytest.raises(ValueError, match="masked"):
        model.assimilate(model.initial_state(1), obs)
    with pytest.raises(ValueError, match="shape"):
        model.advance(model.initial_state(1), Command(torch.ones(1, 4)))
    snap = freeze(model, model.initial_state(1))
    for intervention in (
        Intervention("energy_descent"),
        Intervention("state_clamp", (8,)),
        Intervention("state_perturb", amplitude=float("nan")),
    ):
        with pytest.raises(ValueError):
            predict(snap, episode.commands, intervention)


def test_clamp_and_perturbation_apply_only_to_private_state(case):
    _, episode, model = case
    state = torch.ones(1, 8)
    snap = freeze(model, state)
    trace = predict(snap, episode.commands, Intervention("state_clamp", (1, 3)))
    assert trace.states[:, :, [1, 3]].count_nonzero() == 0
    assert torch.equal(state, torch.ones_like(state))
    item = Intervention("state_perturb", amplitude=0.1, seed=13)
    assert torch.equal(
        predict(snap, episode.commands, item).features,
        predict(snap, episode.commands, item).features,
    )
    assert not torch.equal(
        predict(snap, episode.commands, item).features, predict(snap, episode.commands).features
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"learning": "offline"},
        {"learning": "online"},
        {"split": "confirmation"},
        {"seed": True},
        {"threads": True},
        {"max_cpu_seconds": 61},
        {"tasks": ["rotation", "absent"]},
    ],
)
def test_fixture_configuration_cannot_activate_scientific_work(changes):
    with pytest.raises(ValueError):
        replace(FixtureConfig(), **changes).validate()


def test_full_matrix_repeat_accounting_and_no_overwrite(tmp_path):
    output = tmp_path / "suite"
    result = run_suite(FixtureConfig(), output)
    assert result["status"] == "complete" and result["cells_per_pass"] == 8
    assert result["expected_invalid_cases_per_pass"] == 1 and result["fitted_models"] == 0
    assert result["artifact_bytes"] == sum(
        p.stat().st_size for p in output.rglob("*") if p.is_file()
    )
    assert not result["empirical_gate_passed"]
    reproduction = compare_runs(output / "original", output / "repeat")
    assert reproduction["exact_numeric_match"] and reproduction["array_files"] == 33
    record = json.loads((output / "original/rotation-leaky-0/record.json").read_text())
    assert record["resources"]["persistent"]["logical_bytes"] == (64 + 96 + 24 + 96 + 8) * 4
    assert record["resources"]["live_state"]["unique_storage_bytes"] == 32
    failure = json.loads((output / "original/expected-failure/failure.json").read_text())
    assert failure["status"] == "invalid" and failure["live_state_unchanged"]
    with pytest.raises(FileExistsError):
        run_suite(FixtureConfig(), output)
    arrays = read_arrays(output / "repeat/rotation-leaky-0/trajectories.npz")
    arrays["free_features"].add_(1)
    np.savez(
        output / "repeat/rotation-leaky-0/trajectories.npz",
        **{k: v.numpy() for k, v in arrays.items()},
    )
    with pytest.raises(AssertionError, match="array differs"):
        compare_runs(output / "original", output / "repeat")


def test_registry_extension_needs_no_runner_control_flow(tmp_path, monkeypatch):
    monkeypatch.setitem(TASKS, "alternate_translation", TranslationTask)
    monkeypatch.setitem(
        BACKENDS,
        "linear_alias",
        lambda spec, seed: SuppliedDynamics(replace(spec, kind="linear"), seed),
    )
    config = replace(
        FixtureConfig(),
        tasks=("rotation", "alternate_translation"),
        backends=("leaky", "linear_alias"),
    )
    assert run_suite(config, tmp_path / "extension")["cells_per_pass"] == 8


def test_budget_reserves_before_writing_and_records_failure(tmp_path):
    config = replace(FixtureConfig(), max_artifact_bytes=65536)
    budget = Budget(config)
    with pytest.raises(BudgetExceeded):
        budget.write(tmp_path / "must-not-exist", b"x")
    assert not (tmp_path / "must-not-exist").exists()
    with pytest.raises(BudgetExceeded):
        run_suite(config, tmp_path / "exhausted")
    status = json.loads((tmp_path / "exhausted/status.json").read_text())
    assert status["status"] == "budget_exhausted"
    assert (
        sum(p.stat().st_size for p in (tmp_path / "exhausted").rglob("*") if p.is_file()) <= 65536
    )


def test_cpu_and_wall_caps_checked(monkeypatch):
    budget = Budget(FixtureConfig())
    monkeypatch.setattr(
        budget, "measurements", lambda: {"cpu_seconds": 61, "wall_seconds": 0, "peak_rss_bytes": 0}
    )
    with pytest.raises(BudgetExceeded, match="cpu"):
        budget.check()
    monkeypatch.setattr(
        budget, "measurements", lambda: {"cpu_seconds": 0, "wall_seconds": 121, "peak_rss_bytes": 0}
    )
    with pytest.raises(BudgetExceeded, match="wall"):
        budget.check()


def test_failed_cell_has_identity_and_archived_inputs(tmp_path, monkeypatch):
    def bad_factory(spec, seed):
        model = SuppliedDynamics(spec, seed)
        model.recurrent.fill_(float("nan"))
        return model

    monkeypatch.setitem(BACKENDS, "leaky", bad_factory)
    with pytest.raises(FloatingPointError):
        run_suite(FixtureConfig(), tmp_path / "failed")
    cell = tmp_path / "failed/original/rotation-leaky-0"
    record = json.loads((cell / "failure.json").read_text())
    assert record["seed"] == 9001 and record["episode"] == 0
    assert record["backend"] == "leaky" and record["stream_seeds"]
    assert (cell / "checkpoint.npz").exists() and (cell / "observations.npz").exists()
    assert json.loads((tmp_path / "failed/status.json").read_text())["status"] == "invalid"


def test_runtime_settings_restored_after_failure(tmp_path):
    old_dtype = torch.get_default_dtype()
    try:
        torch.set_default_dtype(torch.float64)
        with pytest.raises(BudgetExceeded):
            run_suite(replace(FixtureConfig(), max_artifact_bytes=65536), tmp_path / "budget")
        assert torch.get_default_dtype() == torch.float64
    finally:
        torch.set_default_dtype(old_dtype)


def test_perturbation_has_declared_rms_without_role_or_model_changes():
    model = SuppliedDynamics(ModelSpec(8, 1, kind="linear"), 12)
    model.recurrent.copy_(torch.eye(8))
    model.action.zero_()
    snap = freeze(model, model.initial_state(2))
    trace = predict(
        snap, (Command(torch.zeros(2, 1)),), Intervention("state_perturb", amplitude=0.1, seed=71)
    )
    assert torch.allclose(trace.states[0].square().mean(1).sqrt(), torch.full((2,), 0.1))
    assert snap._state.count_nonzero() == 0
