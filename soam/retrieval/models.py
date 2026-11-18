"""Observation-only D-R1 writers; fixed encodings and read-only settling."""

import math
import time

import torch

from soam.acquisition.data import DTYPE, Cue, Record
from soam.acquisition.models import Memory

BITS = 32
N = 768


def encode(x, bound):
    thresholds = (torch.arange(BITS, dtype=DTYPE) + 0.5) * (2 * bound / BITS) - bound
    return torch.where(x[..., None] >= thresholds, 1.0, -1.0).to(DTYPE).flatten(-2)


def decode(x, bound):
    return x.reshape(*x.shape[:-1], -1, BITS).mean(-1) * bound


def validate_record(record, grounded):
    if not grounded or not isinstance(record, Record):
        raise ValueError("Grounded observation record required")
    if (
        record.key.shape != (16,)
        or record.features.shape != (8,)
        or not torch.isfinite(record.key).all()
        or not torch.isfinite(record.features).all()
        or not math.isfinite(record.angle)
        or record.key.square().sum() < 1e-12
    ):
        raise ValueError("Invalid grounded observation")


def validate_cue(cue):
    if not isinstance(cue, Cue) or cue.features.ndim != 2:
        raise ValueError("Masked cue batch required")
    x, mask = cue.features, cue.mask
    if (
        x.shape != mask.shape
        or x.shape[1] != 16
        or mask.dtype != torch.bool
        or not mask.any(1).all()
        or not torch.isfinite(x[mask]).all()
    ):
        raise ValueError("Invalid cue")
    return torch.where(mask, x, 0.0), mask


@torch.jit.script
def sweep(state: torch.Tensor, w: torch.Tensor, clamp: torch.Tensor, active: torch.Tensor):
    """Ascending asynchronous updates; cached fields are updated after each coordinate."""
    fields = state @ w.T
    changes = torch.zeros(state.shape[0], dtype=torch.int64)
    deltas = torch.zeros_like(state)
    for i in range(state.shape[1]):
        h = fields[:, i].clone()
        old = state[:, i].clone()
        proposed = torch.where(h > 1e-12, torch.ones_like(h), old)
        proposed = torch.where(h < -1e-12, -torch.ones_like(h), proposed)
        proposed = torch.where(clamp[:, i] | ~active, old, proposed)
        delta = proposed - old
        state[:, i] = proposed
        fields = fields + delta[:, None] * w[i][None, :]
        changes += (delta != 0).to(torch.int64)
        deltas[:, i] = -delta * h
    return state, changes, deltas


class RetrievalMemory(Memory):
    def __init__(self, name, core, setting=1.0, threshold=1e30):
        if name in {"NOWRITE", "KV", "REG", "FAST"}:
            super().__init__(name, core, setting, threshold)
        else:
            if name not in {"PH-FULL", "PH-1", "REG-LIFT"}:
                raise ValueError(name)
            self.name, self.core, self.setting, self.threshold = name, core, setting, threshold
            self.buffers = {"count": torch.zeros((), dtype=torch.int64)}
            if name.startswith("PH"):
                self.buffers.update(
                    projector=torch.zeros(N, N, dtype=DTYPE),
                    rank=torch.zeros((), dtype=torch.int64),
                )
            else:
                self.buffers.update(
                    xx=torch.zeros(512, 512, dtype=DTYPE),
                    yx=torch.zeros(8, 512, dtype=DTYPE),
                )
            self.reset()

    def reset(self, batch=1):
        self.state = torch.zeros(batch, N if self.name.startswith("PH") else 24, dtype=DTYPE)
        self.trace = {}
        self.action_state = torch.zeros(batch, 8, dtype=DTYPE)

    def acquire(self, record, *, grounded=False):
        validate_record(record, grounded)
        if self.name not in {"PH-FULL", "PH-1", "REG-LIFT"}:
            return super().acquire(record, grounded=True)
        value = self.core.advance(record.features, -record.angle)
        key = encode(record.key, 4.0)
        if self.name == "REG-LIFT":
            self.buffers["xx"] += torch.outer(key, key)
            self.buffers["yx"] += torch.outer(value, key)
        else:
            x = torch.cat((key, encode(value, 1.5)))
            p = self.buffers["projector"]
            residual = x - p @ x
            residual = residual - p @ residual
            norm = residual.square().sum()
            if norm > 1e-10 * x.square().sum():
                new = p + torch.outer(residual, residual) / norm
                new = (new + new.T) * 0.5
                if not torch.isfinite(new).all() or (new @ x - x).abs().max() > 1e-8:
                    raise RuntimeError("Projector write invariant")
                self.buffers["projector"] = new
                self.buffers["rank"] += 1
        self.buffers["count"] += 1
        self.reset()
        if self.resources()["persistent_bytes"] > 8388608:
            raise RuntimeError("Persistent storage ceiling")

    def recall(self, cue, *, perturb_uniform=None):
        query, visible = validate_cue(cue)
        if self.name not in {"PH-FULL", "PH-1", "REG-LIFT"}:
            return super().recall(Cue(query, visible))
        before = self.fingerprint()
        self.reset(len(query))
        if self.name == "REG-LIFT":
            z = encode(query, 4.0)
            masks = visible.repeat_interleave(BITS, dim=1)
            values, scores = [], []
            for row, mask in zip(z, masks, strict=True):
                xx = self.buffers["xx"][mask][:, mask]
                v = torch.linalg.solve(
                    xx + self.setting * torch.eye(len(xx), dtype=DTYPE), row[mask]
                )
                values.append(self.buffers["yx"][:, mask] @ v)
                scores.append((xx @ v - row[mask]).square().mean())
            value, score = torch.stack(values), torch.stack(scores)
            self.state[:, 16:] = value
        else:
            value, score = self._settle(query, visible, perturb_uniform)
        accepted = (score <= self.threshold) & (self.buffers["count"] > 0)
        if self.fingerprint() != before:
            raise RuntimeError("Recall mutated persistent memory")
        return value.clone(), score.clone(), accepted

    def _settle(self, query, visible, perturb_uniform):
        started = time.perf_counter()
        p = self.buffers["projector"]
        w = p.clone()
        w.fill_diagonal_(0)
        clamp = torch.zeros_like(self.state, dtype=torch.bool)
        clamp[:, :512] = visible.repeat_interleave(BITS, dim=1)
        self.state[:, :512] = torch.where(clamp[:, :512], encode(query, 4.0), 0.0)
        batch = len(query)
        max_cycles = 1 if self.name == "PH-1" else 32
        active = torch.ones(batch, dtype=torch.bool)
        seen = [[row.numpy().tobytes()] for row in self.state]
        counts = torch.zeros(batch, dtype=torch.int64)
        converged = torch.zeros(batch, dtype=torch.bool)
        perturb_counts = torch.zeros(batch, dtype=torch.int64)
        values, energies, scores, change_trace, elapsed = [], [], [], [], []
        prior_energy = -0.5 * (self.state * (self.state @ w.T)).sum(1)
        for cycle in range(1, max_cycles + 1):
            self.state, changes, de = sweep(self.state, w, clamp, active)
            energy = -0.5 * (self.state * (self.state @ w.T)).sum(1)
            if ((energy - prior_energy) > 1e-10 * prior_energy.abs().clamp_min(1)).any():
                raise RuntimeError("Settling energy increased")
            if (de > 1e-10).any():
                raise RuntimeError("Coordinate energy increased")
            counts += active.to(torch.int64)
            newly_converged = active & (changes == 0)
            converged |= newly_converged
            active &= ~newly_converged
            for j, row in enumerate(self.state):
                key = row.numpy().tobytes()
                if bool(active[j]) and key in seen[j]:
                    raise RuntimeError("Nonstationary settling cycle")
                seen[j].append(key)
            values.append(decode(self.state[:, 512:], 1.5))
            energies.append(energy)
            scores.append((self.state - self.state @ p.T).square().mean(1))
            change_trace.append(changes)
            elapsed.append(time.perf_counter() - started)
            if cycle == 1 and perturb_uniform is not None:
                if perturb_uniform.shape != self.state.shape:
                    raise ValueError("Invalid perturbation schedule")
                for j in range(batch):
                    eligible = (~clamp[j] & (self.state[j] != 0)).nonzero().flatten()
                    n = math.ceil(len(eligible) * 0.05)
                    selected = eligible[torch.argsort(perturb_uniform[j, eligible])[:n]]
                    self.state[j, selected] *= -1
                    perturb_counts[j] = n
                active[:] = True
                converged[:] = False
                seen = [[row.numpy().tobytes()] for row in self.state]
            prior_energy = -0.5 * (self.state * (self.state @ w.T)).sum(1)
            if not active.any():
                break
        self.trace = {
            "values": torch.stack(values),
            "energy": torch.stack(energies),
            "scores": torch.stack(scores),
            "changes": torch.stack(change_trace),
            "cycles": counts,
            "converged": converged,
            "elapsed": torch.tensor(elapsed),
            "perturb_count": perturb_counts,
        }
        return values[-1], scores[-1]

    def rollout(self, cue, actions):
        validate_cue(cue)
        if (
            actions.ndim != 2
            or actions.shape[0] != len(cue.features)
            or not torch.isfinite(actions).all()
        ):
            raise ValueError("Invalid actions")
        before = self.fingerprint()
        y, scores, accepted = self.recall(cue)
        predicted = [y.clone()]
        for action in actions.T:
            y = self.core.advance(y, action)
            predicted.append(y.clone())
        self.action_state = y.clone()
        if before != self.fingerprint():
            raise RuntimeError("Rollout mutated persistent memory")
        return torch.stack(predicted, 1), scores, accepted

    def resources(self):
        result = super().resources()
        if self.name in {"REG-LIFT", "PH-FULL", "PH-1"}:
            # Two fixed threshold tables, derived on demand, are charged as supplied storage.
            result["encoding_bytes"] = 64 * 8
            result["persistent_bytes"] += result["encoding_bytes"]
            result["active_state_bytes_per_query"] = self.state.shape[1] * 8
            result["active_state_batch_bytes"] = self.state.numel() * 8
            result["field_bytes_per_query"] = N * 8 if self.name.startswith("PH") else 0
            result["materialized_weight_bytes"] = N * N * 8 if self.name.startswith("PH") else 0
            result["write_workspace_bytes_upper"] = 4 * result["writable_bytes"]
            result["supplied_units"] = N if self.name.startswith("PH") else 512
        result["action_state_bytes_per_query"] = 8 * 8
        return result


def conjugate_gradient(a, b, max_iterations=64):
    """Fixture-only iterative solve; no extra trial arm."""
    x = torch.zeros_like(b)
    r = b - a @ x
    direction = r.clone()
    rr = r @ r
    for _ in range(max_iterations):
        if torch.sqrt(rr) <= 1e-10 * torch.linalg.vector_norm(b).clamp_min(1e-30):
            return x
        ad = a @ direction
        alpha = rr / (direction @ ad)
        x = x + alpha * direction
        r = r - alpha * ad
        updated = r @ r
        direction = r + (updated / rr) * direction
        rr = updated
    if torch.linalg.vector_norm(a @ x - b) > 1e-8 * torch.linalg.vector_norm(b):
        raise RuntimeError("REG iterative solve did not converge")
    return x
