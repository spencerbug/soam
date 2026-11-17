"""Grounded writes and read-only recurrent inference with explicit memory lifetime."""

import copy
import math

import torch

from soam.temporal.runner import tensor_hash

from .data import DTYPE, Cue, Record


class Core:
    def __init__(self, a, b):
        self.a, self.b = a.clone(), b.clone()

    @classmethod
    def fit(cls, data, ridge):
        x, angle, y = data
        design = torch.cat((x * angle.cos()[:, None], x * angle.sin()[:, None]), 1)
        coef = torch.linalg.solve(
            design.T @ design + ridge * torch.eye(16, dtype=DTYPE), design.T @ y
        )
        return cls(coef[:8].T, coef[8:].T)

    def advance(self, value, angle):
        angle = torch.as_tensor(angle, dtype=DTYPE)
        return (value @ self.a.T) * angle.cos()[..., None] + (value @ self.b.T) * angle.sin()[
            ..., None
        ]


class Memory:
    def __init__(self, name, core, setting=1.0, threshold=1e30):
        if name not in {"NOWRITE", "KV", "REG", "FAST"}:
            raise ValueError(name)
        self.name, self.core, self.setting, self.threshold = name, core, setting, threshold
        self.buffers = {"count": torch.zeros((), dtype=torch.int64)}
        if name == "KV":
            self.buffers.update(
                keys=torch.zeros(32, 16, dtype=DTYPE),
                values=torch.zeros(32, 8, dtype=DTYPE),
                counts=torch.zeros(32, dtype=DTYPE),
            )
        elif name == "REG":
            self.buffers.update(
                xx=torch.zeros(16, 16, dtype=DTYPE), yx=torch.zeros(8, 16, dtype=DTYPE)
            )
        elif name == "FAST":
            self.buffers["w"] = torch.zeros(24, 16, dtype=DTYPE)
        self.reset()

    def persistent(self):
        return {
            **self.buffers,
            "core_a": self.core.a,
            "core_b": self.core.b,
            "settings": torch.tensor([self.setting, self.threshold], dtype=DTYPE),
        }

    def fingerprint(self):
        return tensor_hash(self.persistent())

    def snapshot(self):
        return copy.deepcopy(self.buffers)

    def restore(self, snapshot):
        if snapshot.keys() != self.buffers.keys() or any(
            snapshot[k].shape != v.shape
            or snapshot[k].dtype != v.dtype
            or not torch.isfinite(snapshot[k]).all()
            for k, v in self.buffers.items()
        ):
            raise ValueError("Invalid memory snapshot")
        self.buffers = copy.deepcopy(snapshot)
        self.reset()

    def reset(self, batch=1):
        self.state = torch.zeros(batch, 24, dtype=DTYPE)

    def acquire(self, record, *, grounded=False):
        if not grounded or not isinstance(record, Record):
            raise ValueError("A grounded observation record is required")
        k, y, q = record.key, record.features, record.angle
        if (
            k.shape != (16,)
            or y.shape != (8,)
            or not torch.isfinite(k).all()
            or not torch.isfinite(y).all()
            or not math.isfinite(q)
            or k.square().sum() < 1e-12
        ):
            raise ValueError("Invalid grounded observation")
        value = self.core.advance(y, -q)
        b = self.buffers
        if self.name == "NOWRITE":
            self.state = torch.cat((k, value))[None].clone()
            return
        if self.name == "KV":
            count = int(b["count"])
            matches = (b["keys"][:count] == k).all(1).nonzero().flatten()
            if len(matches):
                index = int(matches[0])
            else:
                if count == 32:
                    raise ValueError("Fixed capacity exhausted")
                index = count
                b["keys"][index] = k
                b["count"] += 1
            n = b["counts"][index]
            b["values"][index] = (b["values"][index] * n + value) / (n + 1)
            b["counts"][index] += 1
        elif self.name == "REG":
            b["xx"] += torch.outer(k, k)
            b["yx"] += torch.outer(value, k)
            b["count"] += 1
        else:
            target = torch.cat((k, value))
            w = b["w"]
            w += self.setting * torch.outer(target - w @ k, k) / k.square().sum()
            w *= min(1.0, 16.0 / max(float(w.norm()), 1e-12))
            b["count"] += 1
        if self.resources()["writable_bytes"] > 8192:
            raise RuntimeError("Writable memory ceiling")
        self.state = torch.cat((k, value))[None].clone()

    def recall(self, cue):
        if not isinstance(cue, Cue) or cue.features.ndim != 2:
            raise ValueError("Cue batch required")
        q, mask = cue.features, cue.mask
        if (
            q.shape != mask.shape
            or q.shape[1] != 16
            or mask.dtype != torch.bool
            or not mask.any(1).all()
            or not torch.isfinite(q[mask]).all()
        ):
            raise ValueError("Invalid cue")
        q = torch.where(mask, q, 0.0)
        self.reset(len(q))
        self.state[:, :16] = q
        scores = torch.full((len(q),), 1e30, dtype=DTYPE)
        b = self.buffers
        if self.name == "NOWRITE" or int(b["count"]) == 0:
            return self.state[:, 16:].clone(), scores, torch.zeros(len(q), dtype=torch.bool)
        if self.name == "KV":
            n = int(b["count"])
            distances = ((q[:, None] - b["keys"][None, :n]).square() * mask[:, None]).sum(2)
            distances /= mask.sum(1)[:, None]
            scores, idx = distances.min(1)
            value = b["values"][idx]
        elif self.name == "REG":
            vals, recon = [], []
            for row, visible in zip(q, mask, strict=True):
                xx = b["xx"][visible][:, visible]
                weight = torch.linalg.solve(
                    xx + self.setting * torch.eye(len(xx), dtype=DTYPE), row[visible]
                )
                vals.append(b["yx"][:, visible] @ weight)
                recon.append(b["xx"][:, visible] @ weight)
            value, reconstructed = torch.stack(vals), torch.stack(recon)
            scores = ((reconstructed - q).square() * mask).sum(1) / mask.sum(1)
        else:
            query = q * (16 / q.square().sum(1).clamp_min(1e-12))[:, None]
            # One block-recurrent recall; exactly equal to direct delta-regression readout.
            recalled = query @ b["w"].T
            value = recalled[:, 16:]
            scores = ((recalled[:, :16] - q).square() * mask).sum(1) / mask.sum(1)
        self.state[:, 16:] = value
        return value.clone(), scores, scores <= self.threshold

    def rollout(self, cue, actions):
        before = self.fingerprint()
        y, scores, accepted = self.recall(cue)
        out = [y]
        for action in actions.T:
            y = self.core.advance(y, action)
            self.state[:, 16:] = y
            out.append(y.clone())
        if self.fingerprint() != before:
            raise RuntimeError("Inference mutated persistent memory")
        return torch.stack(out, 1), scores, accepted

    def resources(self):
        writable = sum(v.numel() * v.element_size() for v in self.buffers.values())
        return {
            "offline_coefficients": 128,
            "offline_core_bytes": 1024,
            "writable_bytes": writable,
            "settings_bytes": 16,
            "persistent_bytes": writable + 1040,
            "active_state_bytes_per_query": 24 * 8,
            "active_state_batch_bytes": self.state.numel() * 8,
            "snapshot_bytes": writable,
        }
