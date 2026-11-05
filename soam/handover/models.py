"""Explicit key/ring dynamics and conventional GRU controls with caller-owned state."""

import math
import time
from dataclasses import dataclass, fields

import torch
from torch import nn

from soam.encoders.projection import FixedProjection
from soam.handover.data import ObservationPacket
from soam.handover.protocol import initialization_seed, load_protocol, templates, tensor_fingerprint


@dataclass
class ModelState:
    key: torch.Tensor
    pose: torch.Tensor
    weights: torch.Tensor
    consecutive: torch.Tensor
    evidence_age: torch.Tensor
    localized: torch.Tensor
    attended: int = -1
    initialized: bool = False

    def clone(self):
        return ModelState(
            **{
                f.name: getattr(self, f.name).clone()
                if isinstance(getattr(self, f.name), torch.Tensor)
                else getattr(self, f.name)
                for f in fields(self)
            }
        )

    def tensors(self):
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if isinstance(getattr(self, f.name), torch.Tensor)
        }


@dataclass
class Work:
    key_substeps: int = 0
    selector_calls: int = 0
    pose_calls: int = 0
    ring_propagations: int = 0
    sensory_corrections: int = 0
    readout_calls: int = 0
    linear_macs: int = 0
    replay_packets: int = 0
    state_resets: int = 0
    state_copies: int = 0
    snapshot_clones: int = 0
    transition_state_clones: int = 0
    history_packet_copies: int = 0
    key_seconds: float = 0.0
    pose_seconds: float = 0.0
    readout_seconds: float = 0.0

    def add(self, other):
        for f in fields(self):
            setattr(self, f.name, getattr(self, f.name) + getattr(other, f.name))
        return self

    def to_dict(self):
        return {
            f.name: getattr(self, f.name) for f in fields(self) if not f.name.endswith("_seconds")
        }

    def timings(self):
        return {f.name: getattr(self, f.name) for f in fields(self) if f.name.endswith("_seconds")}


class HandoverModel(nn.Module):
    def __init__(self, variant, seed=11, condition=0, intervention="none"):
        super().__init__()
        self.protocol = load_protocol()
        if variant not in self.protocol["variants"] or condition not in range(8):
            raise ValueError("unknown variant/condition")
        if intervention not in {cell["intervention"] for cell in self.protocol["episode_cells"]}:
            raise ValueError("unknown intervention")
        self.variant, self.seed = variant, seed
        self.analytic = variant.startswith("A")
        self.register_buffer("patterns", templates())
        coupling = (torch.ones(3, 3) - torch.eye(3)) * 0.5
        if intervention == "no_priming":
            coupling.zero_()
        elif intervention == "shuffled_priming":
            coupling = coupling[self.protocol["attractor"]["shuffled_priming_output_rows"]]
        self.register_buffer("coupling", coupling)
        self.register_buffer("gains", torch.tensor([1.0, 1.0 if condition == 1 else 0.7]))
        self.encoder = FixedProjection(12, self.protocol["environment"]["projection_seed"])
        q = self.encoder.matrix
        if self.analytic:
            self.register_buffer("plane", q @ q.T)
            self.register_buffer("quarter_turn", q @ torch.tensor([[0.0, -1.0], [1.0, 0.0]]) @ q.T)
            self.register_buffer(
                "pose_prior", self.protocol["attractor"]["pose_prior_radius"] * q[:, 0]
            )
        else:
            with torch.random.fork_rng(devices=[]):
                torch.manual_seed(initialization_seed(seed, "selector"))
                self.selector = nn.GRUCell(33, 16)
                self.selector_readout = nn.Linear(16, 3)
                torch.manual_seed(initialization_seed(seed, variant))
                width = {"G2": 12, "GS24": 24, "GS9": 9}[variant]
                self.pose_cell = nn.GRUCell(15 if variant == "G2" else 29, width)
                self.pose_readout = nn.Linear(width, 12 if variant == "G2" else 24)
        actual = sum(p.numel() for p in self.parameters())
        if actual != self.protocol["models"][variant]["trainable_parameters"]:
            raise ValueError("parameter count differs from manifest")

    def initial_state(self):
        if self.analytic:
            pose = self.pose_prior.repeat(1 if self.variant == "A1" else 2, 1)
        else:
            pose = torch.zeros(2 if self.variant == "G2" else 1, self.pose_cell.hidden_size)
        return ModelState(
            torch.zeros(16),
            pose,
            torch.full((3,), 1 / 3),
            torch.zeros(3, dtype=torch.long),
            torch.full((2,), 2**30),
            torch.zeros(2, dtype=torch.bool),
        )

    def persistent_fingerprint(self):
        return tensor_fingerprint(self.state_dict())

    def key_energy(self, key):
        q, p = key.double(), self.patterns.double()
        beta = self.protocol["attractor"]["beta"]
        return q.square().sum() / 2 - torch.logsumexp(beta * (p.T @ q), 0) / beta

    def key_substep(self, key, cue=None, coupled=True, restoring=True):
        a = self.protocol["attractor"]
        projection = self.patterns.T @ key if restoring or coupled else None
        delta = -key
        if restoring:
            delta = delta + self.patterns @ torch.softmax(a["beta"] * projection, 0)
        if cue is not None:
            delta = delta + a["cue_gain"] * cue
        if coupled:
            delta = delta + a["coupling_gain"] * (self.patterns @ (self.coupling @ projection))
        return key + a["euler_alpha"] * delta

    def key_transition(self, key, weights, cue, present):
        started = time.perf_counter()
        work = Work()
        if self.analytic:
            for _ in range(self.protocol["attractor"]["substeps_per_observation"]):
                key = self.key_substep(key, cue)
                work.key_substeps += 1
                # Reuse P^T q in restoring and coupling terms: 48+48+9+48 MACs.
                work.linear_macs += 153
            logits = self.protocol["attractor"]["beta"] * (self.patterns.T @ key)
            work.linear_macs += 48
        else:
            signal = self.patterns @ (self.coupling @ weights)
            inputs = torch.cat((cue, signal, cue.new_tensor([float(present)])))
            key = self.selector(inputs, key)
            logits = self.selector_readout(key)
            work.selector_calls = 1
            work.readout_calls = 1
            work.linear_macs = 9 + 48 + 3 * 16 * (33 + 16) + 16 * 3
        weights = torch.softmax(logits, 0)
        work.key_seconds = time.perf_counter() - started
        return key, weights, logits, work

    def ring(self, pose, action, gain, radial=None):
        a = self.protocol["attractor"]
        radial = a["lambda_radial"] if radial is None else radial
        v = self.plane @ pose
        u = pose - v
        rho2 = v.square().sum()
        denominator = torch.sqrt(rho2 + (1 - rho2) * math.exp(-2 * radial))
        angle = gain * action
        return (
            torch.cos(angle) * v + torch.sin(angle) * (self.quarter_turn @ pose)
        ) / denominator + math.exp(-a["lambda_orthogonal"]) * u

    def pose_transition(self, pose, packet, initialized, bank=None):
        """One bank (A/G2) or one shared GS state; no policy or history access."""
        started = time.perf_counter()
        work = Work(pose_calls=1)
        if self.analytic:
            if initialized:
                pose = self.ring(pose, packet.executed_action_previous, self.gains[bank])
                work.ring_propagations = 1
                work.linear_macs = 288
            if packet.valid[bank]:
                gain = self.protocol["attractor"]["sensory_gain"]
                pose = (1 - gain) * pose + gain * packet.z[bank]
                work.sensory_corrections = 1
        else:
            if self.variant == "G2":
                inputs = torch.cat(
                    (
                        packet.z[bank] * packet.valid[bank],
                        pose.new_tensor(
                            [
                                float(packet.valid[bank]),
                                packet.executed_action_previous,
                                float(self.gains[bank]),
                            ]
                        ),
                    )
                )
                observed = int(packet.valid[bank])
            else:
                inputs = torch.cat(
                    (
                        (packet.z * packet.valid[:, None]).flatten(),
                        packet.valid.float(),
                        pose.new_tensor([packet.executed_action_previous]),
                        self.gains,
                    )
                )
                observed = int(packet.valid.sum())
            pose = self.pose_cell(inputs, pose)
            work.sensory_corrections = observed
            work.linear_macs = (
                3
                * self.pose_cell.hidden_size
                * (self.pose_cell.input_size + self.pose_cell.hidden_size)
            )
        work.pose_seconds = time.perf_counter() - started
        return pose, work

    def estimates(self, state):
        started = time.perf_counter()
        if self.analytic:
            estimates = state.pose.expand(2, 12) if self.variant == "A1" else state.pose
            return estimates, Work(readout_seconds=time.perf_counter() - started)
        estimates = self.pose_readout(state.pose).reshape(2, 12)
        calls = 2 if self.variant == "G2" else 1
        return estimates, Work(
            readout_calls=calls,
            linear_macs=(calls * self.pose_cell.hidden_size * self.pose_readout.out_features),
            readout_seconds=time.perf_counter() - started,
        )

    def advance(self, state, packet, active=None):
        packet.validate()
        new = state.clone()
        new.key, new.weights, _, work = self.key_transition(
            state.key, state.weights, packet.cue, packet.cue_present
        )
        work.transition_state_clones += 1
        threshold = self.protocol["roles"]["selection_weight_threshold"]
        new.consecutive = torch.where(new.weights >= threshold, state.consecutive + 1, 0)
        new.evidence_age = torch.where(packet.valid, 0, state.evidence_age + 1)
        new.localized = state.localized | packet.valid
        updated = torch.zeros(2, dtype=torch.bool)
        if self.variant == "A1":
            bank = int(new.weights[:2].argmax())
            new.pose[0], extra = self.pose_transition(
                state.pose[0], packet, state.initialized, bank
            )
            work.add(extra)
            updated[bank] = True
        elif self.variant in ("A2", "G2"):
            for bank in range(2):
                if active is None or active[bank]:
                    new.pose[bank], extra = self.pose_transition(
                        state.pose[bank], packet, state.initialized, bank
                    )
                    work.add(extra)
                    updated[bank] = True
        else:
            if active is not None:
                raise ValueError("history modes require independent state banks")
            new.pose[0], extra = self.pose_transition(state.pose[0], packet, state.initialized)
            work.add(extra)
            updated[:] = True
        new.initialized = True
        estimates, extra = self.estimates(new)
        work.add(extra)
        self.check_state(new)
        return new, estimates, work, updated

    def eligible(self, state, estimates, ignore_norm=False):
        roles = self.protocol["roles"]
        candidates = (
            (state.consecutive[:2] >= roles["selection_consecutive_frames"])
            & state.localized
            & (state.evidence_age <= roles["max_evidence_age"])
        )
        if not ignore_norm:
            norms = estimates.norm(dim=-1)
            lower, upper = roles["decoded_norm_range"]
            candidates &= (norms >= lower) & (norms <= upper)
        ids = candidates.nonzero().flatten()
        return int(ids[state.weights[ids].argmax()]) if len(ids) else -1

    def select(self, state, estimates):
        candidate = self.eligible(state, estimates)
        if candidate >= 0:
            state.attended = candidate

    def diagnostics(self, state, updated):
        priming = self.coupling @ state.weights
        roles = []
        for bank in range(3):
            if bank == state.attended:
                role = "attended"
            elif priming[bank] >= self.protocol["roles"]["priming_threshold"]:
                role = (
                    "tracking"
                    if self.variant != "A1" and bank < 2 and state.localized[bank] and updated[bank]
                    else "primed"
                )
            else:
                role = "inactive"
            roles.append(role)
        return {
            "priming": priming,
            "roles": roles,
            "attended": state.attended,
            "key_winner": int(state.weights.argmax()),
            "updated_banks": updated,
            "source_capacity": self.variant != "A1",
        }

    @staticmethod
    def check_state(state):
        if any(not torch.isfinite(t).all() for t in state.tensors().values()):
            raise FloatingPointError("nonfinite recurrent state")
        if state.key.norm() > 10 or torch.any(state.pose.norm(dim=-1) > 10):
            raise FloatingPointError("recurrent state norm exceeds protocol limit")

    @torch.no_grad()
    def step(self, state, packet):
        new, estimates, work, updated = self.advance(state, packet)
        self.select(new, estimates)
        diagnostics = self.diagnostics(new, updated)
        work.linear_macs += 9
        diagnostics["work"] = work.to_dict()
        return new, estimates.clone(), diagnostics

    @torch.no_grad()
    def predict(self, snapshot, actions, return_work=False):
        if not snapshot.initialized:
            raise ValueError("prediction requires a post-observation state")
        state, predictions, work = snapshot.clone(), [], Work(snapshot_clones=1)
        for action in actions:
            packet = ObservationPacket(
                torch.zeros(2, 12),
                torch.zeros(2, dtype=torch.bool),
                torch.zeros(16),
                False,
                float(action),
            )
            state, estimates, extra, _ = self.advance(state, packet)
            work.add(extra)
            predictions.append(estimates.clone())
        result = torch.stack(predictions) if predictions else torch.empty(0, 2, 12)
        return (result, work) if return_work else result

    def resources(self):
        initial = self.initial_state()
        return {
            "trainable_parameters": sum(p.numel() for p in self.parameters()),
            "parameter_bytes": sum(p.numel() * p.element_size() for p in self.parameters()),
            "fixed_buffer_floats": sum(b.numel() for b in self.buffers()),
            "fixed_buffer_bytes": sum(b.numel() * b.element_size() for b in self.buffers()),
            "recurrent_floats": initial.key.numel() + initial.pose.numel(),
            "state_tensor_bytes": sum(
                t.numel() * t.element_size() for t in initial.tensors().values()
            ),
            "pose_banks": len(initial.pose),
            "independent_pose_instances": 2 if self.variant in ("A2", "G2") else 1,
            "weight_copies": 1,
            "live_interaction_states": 1,
            "prediction_snapshots": 1,
            "temporary_transition_clones": "counted in work; peak allocation represented by RSS",
            "compute_note": "Leading linear MACs only; nonlinear/vector arithmetic, Python, "
            "and diagnostics excluded. Actual wall/CPU time and RSS are recorded separately.",
        }
