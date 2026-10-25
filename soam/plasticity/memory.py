"""Grounded proposal/commit boundary for the Gate 1 low-rank substrate.

This is an application-level contract, not a sandbox against malicious Python.
Callers attest observation provenance; prediction snapshots have no write interface.
"""

import hashlib
import json
import time
from copy import deepcopy
from dataclasses import asdict, dataclass
from pathlib import Path
from threading import RLock

import torch

from soam.config import Config
from soam.encoders.projection import FixedProjection
from soam.recurrent.models import build_model

from .rules import DampedJacobianDelta, LocalSignals, WriteConfig

PLASTIC = "recurrent.weight"
SETTINGS = (
    "variant",
    "hidden_dim",
    "contexts",
    "observation_dim",
    "rank",
    "alpha",
    "assimilation_gain",
)


def tensor_hash(tensors, metadata=None):
    digest = hashlib.sha256(json.dumps(metadata or {}, sort_keys=True, allow_nan=False).encode())
    for name, tensor in sorted(tensors.items()):
        value = tensor.detach().cpu().contiguous()
        digest.update(json.dumps([name, str(value.dtype), list(value.shape)]).encode())
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def encoder_identity(encoder):
    return tensor_hash(encoder.state_dict())


def model_identity(model):
    return tensor_hash(model.state_dict(), {k: getattr(model, k) for k in SETTINGS})


def frozen_identity(model):
    return tensor_hash(
        {k: v for k, v in model.state_dict().items() if k != PLASTIC},
        {k: getattr(model, k) for k in SETTINGS},
    )


def vector_data(value, shape, label):
    if not isinstance(value, torch.Tensor) or value.shape != shape:
        raise ValueError(f"invalid {label} shape; expected {shape}")
    if (
        value.device.type != "cpu"
        or value.dtype != torch.float32
        or not torch.isfinite(value).all()
    ):
        raise ValueError(f"{label} must be finite CPU float32")
    return value.detach().clone()


@dataclass(frozen=True)
class GroundedEvidence:
    """An observed history; only the final transition supplies a write target.

    source_id must identify an actual sensor/simulator stream. A string is an
    attestation by the ingestion caller, not independent proof of physical reality.
    """

    evidence_id: str
    source_id: str
    episode_id: str
    start_step: int
    split: str
    origin: str
    observations: torch.Tensor  # [T+1,12], fixed encoder features
    actions: torch.Tensor  # [T,3], executed actions
    contexts: torch.Tensor  # [T], currently supplied known-context labels
    encoder_sha256: str

    def validated_copy(self):
        for name in ("evidence_id", "source_id", "episode_id"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ValueError(f"{name} must identify the grounded source")
        if type(self.start_step) is not int or self.start_step < 0:
            raise ValueError("start_step must be a nonnegative integer")
        if self.encoder_sha256 != encoder_identity(FixedProjection(12, 1729)):
            raise ValueError("evidence encoder does not match the frozen Gate 1 projection")
        if self.split not in {"adaptation", "development"}:
            raise ValueError("evaluation/test evidence cannot authorize writes")
        if self.origin not in {"sensor", "simulator"}:
            raise ValueError("imagined evidence cannot authorize writes")
        if not isinstance(self.actions, torch.Tensor) or self.actions.ndim != 2:
            raise ValueError("actions must be [T,3]")
        length = self.actions.shape[0]
        if length < 1:
            raise ValueError("need an observed transition")
        obs = vector_data(self.observations, (length + 1, 12), "observations")
        actions = vector_data(self.actions, (length, 3), "actions")
        c = self.contexts
        if (
            not isinstance(c, torch.Tensor)
            or c.shape != (length,)
            or c.device.type != "cpu"
            or c.dtype != torch.int64
            or not ((c >= 0) & (c < 3)).all()
        ):
            raise ValueError("contexts must be CPU int64 labels in [0,3)")
        return GroundedEvidence(
            self.evidence_id,
            self.source_id,
            self.episode_id,
            self.start_step,
            self.split,
            self.origin,
            obs,
            actions,
            c.detach().clone(),
            self.encoder_sha256,
        )

    def provenance(self):
        metadata = {
            k: getattr(self, k)
            for k in (
                "evidence_id",
                "source_id",
                "episode_id",
                "start_step",
                "split",
                "origin",
                "encoder_sha256",
            )
        }
        metadata["history_transitions"] = len(self.actions)
        metadata["target_step"] = self.start_step + len(self.actions) - 1
        metadata["payload_sha256"] = tensor_hash(
            {"observations": self.observations, "actions": self.actions, "contexts": self.contexts},
            metadata,
        )
        return metadata


@dataclass(frozen=True)
class UpdateProposal:
    proposal_id: str
    delta: torch.Tensor  # inspectable copy, never an alias of persistent weights
    audit: dict


def proposal_identity(proposal):
    return tensor_hash({"delta": proposal.delta}, proposal.audit)


class PredictionSnapshot:
    """Detached inference-only copy. Refresh after a commit to see new weights."""

    def __init__(self, model):
        self._model = deepcopy(model).eval().requires_grad_(False)
        self.identity = model_identity(self._model)

    @torch.no_grad()
    def rollout(self, observation, actions, contexts, *, observations=None, perturb=None):
        return self._model.rollout(
            observation, actions, contexts, observations=observations, perturb=perturb
        )

    def state_dict(self):
        return {k: v.detach().clone() for k, v in self._model.state_dict().items()}


class LocalMemory:
    """Single pending proposal and single-level rollback; snapshots never alias memory.

    The cumulative budget is sum of applied Frobenius norms since construction,
    restored on rollback. It is conservative: opposing writes do not refund budget.
    Locks serialize operations; no filesystem I/O occurs inside commit or rollback.
    """

    def __init__(self, model, config=None, *, checkpoint_sha256=None):
        self._config = (config or WriteConfig()).validate()
        if (
            model.variant != "low_rank"
            or model.hidden_dim != 37
            or model.contexts != 3
            or model.observation_dim != 12
            or model.rank != 4
            or model.alpha != 0.7
            or model.assimilation_gain != 0.5
        ):
            raise ValueError("requires the Gate 1 low-rank architecture/settings")
        if any(
            p.device.type != "cpu" or p.dtype != torch.float32 or not torch.isfinite(p).all()
            for p in model.parameters()
        ):
            raise ValueError("requires finite CPU float32 parameters")
        self._model = deepcopy(model).eval().requires_grad_(False)
        self._frozen = frozen_identity(self._model)
        self._initial = model_identity(self._model)
        self._expected = self._initial
        self._checkpoint_sha256 = checkpoint_sha256
        self._lock = RLock()
        self._pending = self._undo = None
        self._revision = self._proposals_seen = 0
        self._spent = 0.0

    @classmethod
    def from_manifest(cls, repo, seed=11, config=None):
        repo = Path(repo)
        manifest = json.loads((repo / "reports/gate-1/checkpoints.json").read_text())
        if manifest["decision"] != "proceed" or manifest["primary_model"] != "low_rank":
            raise ValueError("Gate 1 does not permit this substrate")
        records = [r for r in manifest["models"]["low_rank"] if r["seed"] == seed]
        if len(records) != 1:
            raise ValueError("seed absent from Gate 1 manifest")
        entry = records[0]
        path = repo / entry["path"]
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != entry["sha256"]:
            raise ValueError("checkpoint file hash mismatch")
        import io

        checkpoint = torch.load(io.BytesIO(content), weights_only=True, map_location="cpu")
        if checkpoint["variant"] != "low_rank" or checkpoint["seed"] != seed:
            raise ValueError("checkpoint identity mismatch")
        cfg = Config.from_dict(checkpoint["config"])
        with torch.random.fork_rng(devices=[]):
            model = build_model(cfg, "low_rank")
        model.load_state_dict(checkpoint["state_dict"], strict=True)
        return cls(model, config, checkpoint_sha256=entry["sha256"])

    @property
    def config(self):
        return self._config

    def _check(self):
        if model_identity(self._model) != self._expected:
            raise RuntimeError("persistent state changed outside the write contract")
        if frozen_identity(self._model) != self._frozen:
            raise RuntimeError("frozen parameters or settings changed outside the contract")
        if any(p.requires_grad for p in self._model.parameters()):
            raise RuntimeError("ordinary training was re-enabled")

    def predictor(self):
        with self._lock:
            self._check()
            return PredictionSnapshot(self._model)

    @property
    def identity(self):
        with self._lock:
            self._check()
            return model_identity(self._model)

    @property
    def spent_norm(self):
        with self._lock:
            return self._spent

    @torch.no_grad()
    def propose(self, evidence, rule=None):
        with self._lock:
            self._check()
            if self._pending is not None:
                raise RuntimeError("commit or discard the pending proposal first")
            started = time.perf_counter()
            if not isinstance(evidence, GroundedEvidence):
                raise TypeError("writes require GroundedEvidence")
            evidence = evidence.validated_copy()
            rule = rule or DampedJacobianDelta()
            if not isinstance(rule.name, str) or not rule.name.strip():
                raise ValueError("correction rule needs a nonempty name")
            m = self._model
            # Ground only on observations preceding the final outcome; no hidden world state.
            hidden = m.initialize(evidence.observations[0:1])
            for t in range(len(evidence.actions) - 1):
                hidden = m.step(hidden, evidence.actions[t : t + 1], evidence.contexts[t : t + 1])
                hidden = m.assimilate(
                    hidden, evidence.observations[t + 1 : t + 2], evidence.contexts[t + 1 : t + 2]
                )
            action, context = evidence.actions[-1:], evidence.contexts[-1:]
            pre = (
                m.recurrent(hidden)
                + m.action(action)
                + m.context(context)
                + m.up(m.down(hidden) * m.modulation(context))
            )
            predicted_hidden = (1 - m.alpha) * hidden + m.alpha * pre.tanh()
            prediction = m.decode(predicted_hidden)[0]
            target = evidence.observations[-1]
            signals = LocalSignals(
                hidden[0].clone(),
                pre[0].clone(),
                prediction.clone(),
                target.clone(),
                m.readout.weight.detach().clone(),
                m.alpha,
            )
            raw = vector_data(rule(signals, self.config), (37, 37), "proposed update")
            rank = int(torch.linalg.matrix_rank(raw))
            if rank > self.config.max_rank:
                raise ValueError("proposal exceeds configured rank limit")
            raw_norm = float(raw.double().norm())
            cap = min(self.config.max_update_norm, max(0, self.config.max_total_norm - self._spent))
            # Leave a small rounding margin when clipping; verify actual float32 write below.
            delta = raw * min(1.0, cap * 0.999 / max(raw_norm, 1e-30))
            candidate = deepcopy(m)
            # Rounding near an exhausted budget can exceed even the reserved margin.
            # Bounded halving depends only on numerical constraints, never outcome quality.
            backoffs = 0
            for attempt in range(17):
                candidate.recurrent.weight.copy_(m.recurrent.weight + delta)
                applied = candidate.recurrent.weight - m.recurrent.weight
                applied_norm = float(applied.double().norm())
                if applied_norm <= cap and torch.isfinite(candidate.recurrent.weight).all():
                    break
                backoffs += 1
                delta = delta * 0.5 if attempt < 15 else torch.zeros_like(delta)
            else:
                raise ValueError("could not construct a finite bounded candidate")
            if frozen_identity(candidate) != self._frozen:
                raise RuntimeError("candidate changed a frozen parameter")
            after_prediction = candidate.decode(candidate.step(hidden, action, context))[0]
            self._proposals_seen += 1
            before, after = model_identity(m), model_identity(candidate)
            audit = {
                "rule": rule.name,
                "config": asdict(self.config),
                "evidence": evidence.provenance(),
                "proposal_number": self._proposals_seen,
                "before_revision": self._revision,
                "before_identity": before,
                "after_identity": after,
                "initial_identity": self._initial,
                "source_checkpoint_sha256": self._checkpoint_sha256,
                "plastic_parameter": PLASTIC,
                "changed_parameters": [PLASTIC] if applied_norm else [],
                "raw_update_norm": raw_norm,
                "proposed_update_norm": float(delta.double().norm()),
                "applied_update_norm": applied_norm,
                "proposal_rank": rank,
                "rounding_backoffs": backoffs,
                "rounded_to_noop": applied_norm == 0 and raw_norm > 0,
                "applied_numerical_rank": int(torch.linalg.matrix_rank(applied)),
                "path_norm_before": self._spent,
                "path_norm_after": self._spent + applied_norm,
                "update_tensor_bytes": applied.numel() * applied.element_size(),
                "model_parameter_bytes": sum(p.numel() * p.element_size() for p in m.parameters()),
                "history_transitions_read": len(evidence.actions),
                "target_transitions": 1,
                "mse_before": float((prediction - target).square().mean()),
                "mse_after": float((after_prediction - target).square().mean()),
                "clipped": raw_norm > cap * 0.999,
                "proposal_seconds": time.perf_counter() - started,
            }
            proposal = UpdateProposal("", applied.detach().clone(), audit)
            ident = proposal_identity(proposal)
            self._pending = {"id": ident, "candidate": candidate, "audit": deepcopy(audit)}
            return UpdateProposal(ident, applied.detach().clone(), deepcopy(audit))

    def _validate_proposal(self, proposal):
        if not isinstance(proposal, UpdateProposal) or self._pending is None:
            raise ValueError("no matching pending proposal")
        if (
            proposal.proposal_id != self._pending["id"]
            or proposal_identity(proposal) != self._pending["id"]
        ):
            raise ValueError("proposal was modified or belongs to another memory/revision")
        audit = self._pending["audit"]
        if audit["before_identity"] != self.identity or audit["before_revision"] != self._revision:
            raise ValueError("stale proposal")

    def commit(self, proposal):
        with self._lock:
            started = time.perf_counter()
            self._check()
            self._validate_proposal(proposal)
            candidate, audit = self._pending["candidate"], deepcopy(self._pending["audit"])
            if model_identity(candidate) != audit["after_identity"]:
                raise RuntimeError("candidate identity changed")
            receipt = {
                **audit,
                "event": "commit",
                "receipt_id": proposal.proposal_id,
                "after_revision": self._revision + 1,
                "commit_seconds": time.perf_counter() - started,
            }
            # All validation/allocation precedes the pointer swap; readers use detached snapshots.
            undo = (self._model, self._spent, receipt["receipt_id"], audit["after_identity"])
            self._model, self._spent = candidate, audit["path_norm_after"]
            self._expected = audit["after_identity"]
            self._revision += 1
            self._pending, self._undo = None, undo
            return receipt

    def discard(self, proposal):
        with self._lock:
            self._check()
            self._validate_proposal(proposal)
            self._pending = None
            return {
                "event": "discard",
                "proposal_id": proposal.proposal_id,
                "identity": self.identity,
                "revision": self._revision,
            }

    def rollback(self, receipt_id):
        with self._lock:
            self._check()
            started = time.perf_counter()
            if self._pending is not None:
                raise ValueError("discard pending proposal before rollback")
            if self._undo is None or receipt_id != self._undo[2] or self.identity != self._undo[3]:
                raise ValueError("rollback requires the latest unchanged committed state")
            model, spent, _, before = self._undo
            event = {
                "event": "rollback",
                "receipt_id": receipt_id,
                "before_identity": before,
                "after_identity": model_identity(model),
                "after_revision": self._revision + 1,
                "path_norm_after": spent,
                "rollback_seconds": time.perf_counter() - started,
            }
            self._model, self._spent, self._undo = model, spent, None
            self._expected = event["after_identity"]
            self._revision += 1
            return event
