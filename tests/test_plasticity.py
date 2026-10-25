import hashlib
import json
from dataclasses import replace

import pytest
import torch

from soam.config import Config
from soam.encoders.projection import FixedProjection
from soam.environments.dynamics import Dynamics
from soam.plasticity import (
    DampedJacobianDelta,
    GroundedEvidence,
    LocalMemory,
    LocalSignals,
    WriteConfig,
    encoder_identity,
)
from soam.recurrent.models import build_model


@pytest.fixture
def model():
    torch.set_num_threads(1)
    torch.manual_seed(11)
    return build_model(Config(match_budgets=True), "low_rank")


@pytest.fixture
def evidence():
    batch = Dynamics(Config().environment, 11, "train", 2002).sample(3, 4, balanced=True)
    return GroundedEvidence(
        "example-0",
        "simulator:namespace2002:seed11:train",
        "episode-0",
        0,
        "adaptation",
        "simulator",
        batch.observations[0],
        batch.actions[0],
        batch.contexts[0],
        encoder_identity(FixedProjection(12, 1729)),
    )


def equal_states(a, b):
    assert a.keys() == b.keys()
    assert all(torch.equal(a[k], b[k]) for k in a)


def test_proposal_commit_and_exact_rollback_only_designated_weight(model, evidence):
    original = {k: v.clone() for k, v in model.state_dict().items()}
    memory = LocalMemory(model)
    before_id = memory.identity
    old_snapshot = memory.predictor()
    proposal = memory.propose(evidence)
    assert memory.identity == before_id
    equal_states(original, memory.predictor().state_dict())
    assert proposal.audit["evidence"]["encoder_sha256"] == evidence.encoder_sha256
    assert proposal.audit["proposal_rank"] == 1
    receipt = memory.commit(proposal)
    after = memory.predictor().state_dict()
    changed = [k for k in original if not torch.equal(original[k], after[k])]
    assert changed == ["recurrent.weight"]
    assert memory.identity == receipt["after_identity"] != before_id
    assert 0 < memory.spent_norm <= memory.config.max_update_norm
    equal_states(original, model.state_dict())  # caller's source model was never mutated
    equal_states(original, old_snapshot.state_dict())
    event = memory.rollback(receipt["receipt_id"])
    assert event["after_identity"] == before_id == memory.identity
    assert memory.spent_norm == 0
    equal_states(original, memory.predictor().state_dict())
    with pytest.raises(ValueError):
        memory.commit(proposal)  # stale even though parameters again match
    with pytest.raises(ValueError):
        memory.rollback(receipt["receipt_id"])


def test_snapshot_has_no_write_capability_or_aliases(model, evidence):
    memory = LocalMemory(model)
    snapshot = memory.predictor()
    assert not hasattr(snapshot, "propose") and not hasattr(snapshot, "commit")
    assert all(not p.requires_grad for p in snapshot._model.parameters())
    before = memory.identity
    args = (
        evidence.observations[:1],
        evidence.actions.unsqueeze(0),
        evidence.contexts.unsqueeze(0),
    )
    predicted, _ = snapshot.rollout(*args)
    snapshot.state_dict()["recurrent.weight"].fill_(float("nan"))
    again, _ = snapshot.rollout(*args)
    assert torch.equal(predicted, again) and before == memory.identity
    # Grounded assimilation is also read-only; an inference wrapper never calls a writer.
    snapshot.rollout(*args, observations=evidence.observations.unsqueeze(0))
    assert memory.identity == before


@pytest.mark.parametrize(
    "field,value",
    [
        ("origin", "imagined"),
        ("split", "test"),
        ("split", "evaluation"),
        ("source_id", ""),
        ("encoder_sha256", "wrong-projection"),
        ("start_step", -1),
    ],
)
def test_untrusted_evidence_rejected_before_mutation(model, evidence, field, value):
    memory = LocalMemory(model)
    before = memory.identity
    with pytest.raises(ValueError):
        memory.propose(replace(evidence, **{field: value}))
    assert memory.identity == before


def test_evidence_shapes_finiteness_and_context_validation(model, evidence):
    for bad in (
        replace(evidence, observations=evidence.observations[:-1]),
        replace(evidence, actions=evidence.actions.double()),
        replace(evidence, contexts=evidence.contexts + 4),
        replace(evidence, observations=evidence.observations * float("nan")),
    ):
        memory = LocalMemory(model)
        before = memory.identity
        with pytest.raises(ValueError):
            memory.propose(bad)
        assert memory.identity == before


def test_proposal_tampering_discard_and_stale_receipts(model, evidence):
    memory = LocalMemory(model)
    p = memory.propose(evidence)
    with pytest.raises(RuntimeError):
        memory.propose(evidence)
    tampered = replace(p, delta=p.delta + 1)
    with pytest.raises(ValueError):
        memory.commit(tampered)
    altered_audit = {**p.audit, "after_identity": "invented"}
    with pytest.raises(ValueError):
        memory.commit(replace(p, audit=altered_audit))
    memory.discard(p)
    with pytest.raises(ValueError):
        memory.commit(p)
    receipt1 = memory.commit(memory.propose(evidence))
    receipt2 = memory.commit(memory.propose(evidence))
    with pytest.raises(ValueError):
        memory.rollback(receipt1["receipt_id"])
    memory.rollback(receipt2["receipt_id"])
    assert memory.identity == receipt1["after_identity"]


class FixedRule:
    name = "test-only-controlled-update"

    def __init__(self, delta):
        self.delta = delta

    def __call__(self, signals, config):
        return self.delta.clone()


def test_independent_norm_rank_and_cumulative_budget_guards(model, evidence):
    cfg = WriteConfig(max_update_norm=0.005, max_total_norm=0.007)
    memory = LocalMemory(model, cfg)
    initial = memory.predictor().state_dict()["recurrent.weight"]
    rule = FixedRule(torch.ones(37, 37) * 100)
    for _ in range(4):
        p = memory.propose(evidence, rule)
        assert p.audit["applied_update_norm"] <= 0.005
        memory.commit(p)
        assert memory.spent_norm <= 0.007
    assert (
        float((memory.predictor().state_dict()["recurrent.weight"] - initial).double().norm())
        <= 0.007
    )
    for bad in (torch.eye(37), torch.ones(37, 37) * float("nan")):
        before = memory.identity
        with pytest.raises(ValueError):
            memory.propose(evidence, FixedRule(bad))
        assert memory.identity == before


def test_no_future_target_enters_cue_or_ground_truth_interface(model, evidence):
    captured = []

    class Capture:
        name = "capture"

        def __call__(self, s, cfg):
            captured.append(s)
            return torch.zeros(37, 37)

    for target_offset in (0, 10):
        obs = evidence.observations.clone()
        obs[-1] += target_offset
        LocalMemory(model).propose(replace(evidence, observations=obs), Capture())
    assert torch.equal(captured[0].cue, captured[1].cue)
    assert torch.equal(captured[0].prediction, captured[1].prediction)
    assert not torch.equal(captured[0].target, captured[1].target)
    assert "states" not in GroundedEvidence.__dataclass_fields__


def test_damped_local_lift_matches_analytic_linearized_solution():
    cue = torch.zeros(37)
    cue[0] = 1
    target = torch.zeros(12)
    target[0] = 0.1
    signals = LocalSignals(cue, torch.zeros(37), torch.zeros(12), target, torch.eye(12, 37), 0.7)
    cfg = WriteConfig()
    delta = DampedJacobianDelta()(signals, cfg)
    expected = cfg.learning_rate * 0.7 * 0.1 / (0.7**2 + cfg.damping) / (1 + cfg.key_epsilon)
    assert delta[0, 0].item() == pytest.approx(expected, rel=1e-6)
    assert torch.count_nonzero(delta) == 1
    zero = replace(signals, cue=torch.zeros(37))
    assert torch.count_nonzero(DampedJacobianDelta()(zero, cfg)) == 0


def test_freeze_settings_and_external_mutations_fail_closed(model, evidence):
    memory = LocalMemory(model)
    with pytest.raises(AttributeError):
        memory.config = WriteConfig(learning_rate=0.2)
    memory._model.alpha = 0.9
    with pytest.raises(RuntimeError):
        memory.propose(evidence)
    memory = LocalMemory(model)
    with torch.no_grad():
        memory._model.recurrent.weight.add_(0.1)
    with pytest.raises(RuntimeError):
        memory.predictor()


def test_pending_candidate_isolated_from_caller_evidence_and_rule_signals(model, evidence):
    memory = LocalMemory(model)
    p = memory.propose(evidence)
    expected = p.audit["after_identity"]
    evidence.observations.fill_(999)
    evidence.actions.fill_(999)
    memory.commit(p)
    assert memory.identity == expected


def test_manifest_loader_verifies_hash_and_preserves_rng(tmp_path, model):
    path = tmp_path / "checkpoint.pt"
    torch.save(
        {
            "variant": "low_rank",
            "seed": 11,
            "config": Config(match_budgets=True).to_dict(),
            "state_dict": model.state_dict(),
        },
        path,
    )
    folder = tmp_path / "reports/gate-1"
    folder.mkdir(parents=True)
    manifest = {
        "decision": "proceed",
        "primary_model": "low_rank",
        "models": {
            "low_rank": [
                {
                    "seed": 11,
                    "path": "checkpoint.pt",
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            ]
        },
    }
    (folder / "checkpoints.json").write_text(json.dumps(manifest))
    rng = torch.random.get_rng_state().clone()
    memory = LocalMemory.from_manifest(tmp_path)
    assert torch.equal(rng, torch.random.get_rng_state())
    equal_states(memory.predictor().state_dict(), model.state_dict())
    path.write_bytes(path.read_bytes() + b"changed")
    with pytest.raises(ValueError, match="hash mismatch"):
        LocalMemory.from_manifest(tmp_path)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"damping": 0},
        {"max_rank": 1.5},
        {"learning_rate": float("nan")},
        {"max_update_norm": 0.2},
        {"max_total_norm": float("inf")},
    ],
)
def test_invalid_write_config(kwargs):
    with pytest.raises(ValueError):
        WriteConfig(**kwargs).validate()
