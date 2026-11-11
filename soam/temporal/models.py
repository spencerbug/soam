"""Inference models accept only evidence. No environment, targets or writes."""

import torch
from torch import nn

from soam.gating.models import bilinear

SETTLERS = {"SET32", "REP32", "MIXC32"}
LINEAR = {"L2", "FILTER2", "RESET2"}


class Neural(nn.Module):
    def __init__(self, name, seed):
        super().__init__()
        self.name, self.n = name, (16 if name.endswith("16") else 32)
        n = self.n
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed)
            self.initial = nn.Linear(24, n)
            self.W = nn.Linear(n, n)
            self.A = nn.Linear(3, n, bias=False)
            self.Q = nn.Linear(2, n, bias=False)
            self.D = nn.Linear(n, 12)
            self.E = nn.Linear(24, n, bias=False)
            gate_dims = {
                "GM32": 12,
                "GR32": 24,
                "GS32": 24 + n,
                "GA32": 27 + n,
                "GMETA32": 28 + n,
                "AM32": 27 + n,
            }
            if name in gate_dims:
                self.gate = nn.Linear(gate_dims[name], 1)
                nn.init.zeros_(self.gate.weight)
                nn.init.zeros_(self.gate.bias)
            if name == "AM32":
                self.motion = nn.Linear(n + 5, 1)
                nn.init.zeros_(self.motion.weight)
                nn.init.zeros_(self.motion.bias)
            if name == "SET32":
                self.halt = nn.Linear(n, 1)

    def initialize(self, z, m):
        return torch.tanh(self.initial(torch.cat((z * m, m.float()), -1)))

    def readout(self, h):
        return self.D(h)

    def predict(self, h, a, q):
        beta = (
            2 * torch.sigmoid(self.motion(torch.cat((h, a, q), -1)))
            if self.name == "AM32"
            else torch.ones_like(h[:, :1])
        )
        return 0.5 * h + 0.5 * torch.tanh(self.W(h) + beta * self.A(a) + self.Q(q)), beta

    def correct(self, prior, previous, a, q, z, m, sd, *, metadata=False):
        present = m.any(-1, keepdim=True)
        residual = (z - self.readout(prior)) * m if not self.name.startswith("MIX") else None
        gamma = torch.full_like(prior[:, :1], 0.5)
        if hasattr(self, "gate"):
            xs = [m.float()]
            if self.name != "GM32":
                xs.append(residual)
            if self.name in {"GS32", "GA32", "GMETA32", "AM32"}:
                xs.append(prior)
            if self.name in {"GA32", "GMETA32", "AM32"}:
                xs.append(a)
            if self.name == "GMETA32":
                xs.append(sd)
            gamma = torch.sigmoid(self.gate(torch.cat(xs, -1)))
        if self.name.startswith("MIX"):
            update = 0.5 * previous + 0.5 * torch.tanh(
                self.W(previous) + self.A(a) + self.Q(q) + self.E(torch.cat((z * m, m.float()), -1))
            )
        else:
            update = prior + gamma * torch.tanh(self.E(torch.cat((residual, m.float()), -1)))
        return torch.where(present, update, prior), gamma * present

    def settle(self, h, z, m):
        q = torch.zeros_like(h[:, :2])
        q[:, 0] = 1
        drive = self.W(h) + self.Q(q)
        if self.name == "REP32":
            drive = drive + self.E(torch.cat((z * m, m.float()), -1))
        return 0.5 * h + 0.5 * torch.tanh(drive)

    def resources(self):
        n = self.n
        gate = self.gate.in_features if hasattr(self, "gate") else 0
        motion = n + 5 if hasattr(self, "motion") else 0
        return {
            "fitted_scalars": sum(p.numel() for p in self.parameters()),
            "persistent_bytes": sum(p.numel() * p.element_size() for p in self.parameters()),
            "state_floats": n,
            "prior_workspace_floats": n,
            "initial_macs": 24 * n,
            "predict_macs": n * n + 5 * n + 12 * n + motion,
            "correct_macs": (n * n + 5 * n if self.name.startswith("MIX") else 12 * n)
            + 24 * n
            + gate,
            "settle_macs": n * n + 2 * n + (24 * n if self.name == "REP32" else 0),
            "halting_macs": n if self.name == "SET32" else 0,
            "readout_macs": 12 * n,
            "nonlinear_note": "tanh per recurrent/correction unit; sigmoid per gain/head; MAC estimate excludes elementwise ops",
        }


class Linear(nn.Module):
    def __init__(self, name, seed=0):
        super().__init__()
        self.name, self.n = name, 2
        for key, value in {
            "P": torch.zeros(12, 2),
            "mean": torch.zeros(12),
            "B": torch.zeros(2, 12),
            "L": torch.zeros(2, 25),
            "process": torch.eye(2) * 1e-5,
            "penalty": torch.tensor(1e-4),
        }.items():
            self.register_buffer(key, value)

    def decode_mean(self, z, m):
        if self.name == "L2":
            x = torch.cat((z * m, m.float(), torch.ones_like(z[:, :1])), -1)
            return x @ self.L.T
        dp = self.P[None] * m[..., None]
        precision = self.P.T @ dp + self.penalty * torch.eye(2)
        rhs = ((z - self.mean) * m) @ self.P
        return torch.linalg.solve(precision, rhs[..., None])[..., 0]

    def initialize(self, z, m):
        h = self.decode_mean(z, m)
        if self.name == "FILTER2":
            dp = self.P[None] * m[..., None]
            cov = torch.linalg.inv(self.P.T @ dp / 0.0001 + torch.eye(2))
            return torch.cat((h, cov.flatten(1)), -1)
        return h

    def readout(self, h):
        return h[:, :2] @ self.P.T + self.mean

    def predict(self, h, a, q):
        y = bilinear(h[:, :2], a) @ self.B.T
        y = torch.where(q[:, :1].bool(), h[:, :2], y)
        if self.name == "FILTER2":
            jac = self.B[:, :2][None] + sum(
                a[:, j, None, None] * self.B[:, 2 + 2 * j : 4 + 2 * j] for j in range(3)
            )
            jac = torch.where(q[:, :1, None].bool(), torch.eye(2), jac)
            cov = jac @ h[:, 2:].reshape(-1, 2, 2) @ jac.transpose(-1, -2) + self.process
            y = torch.cat((y, cov.flatten(1)), -1)
        return y, torch.ones_like(y[:, :1])

    def correct(self, prior, previous, a, q, z, m, sd, *, metadata=False):
        present = m.any(-1, keepdim=True)
        if self.name == "FILTER2":
            cov = prior[:, 2:].reshape(-1, 2, 2)
            pinv = torch.linalg.inv(cov + torch.eye(2) * 1e-10)
            variance = sd.square().clamp_min(1e-6) if metadata else torch.full_like(sd, 0.0001)
            precision = pinv + (self.P.T @ (self.P[None] * m[..., None])) / variance[..., None]
            new_cov = torch.linalg.inv(precision)
            rhs = (pinv @ prior[:, :2, None])[..., 0] + ((z - self.mean) * m) @ self.P / variance
            y = (new_cov @ rhs[..., None])[..., 0]
            update = torch.cat((y, new_cov.flatten(1)), -1)
        else:
            y = self.decode_mean(z, m)
            update = 0.5 * prior + 0.5 * y if self.name == "L2" else y
        return torch.where(present, update, prior), present.float() * (
            0.5 if self.name == "L2" else 1.0
        )

    def resources(self):
        tensors = dict(self.named_buffers())
        # L is used only by historical L2, process only by FILTER2; allocated bytes also explicit.
        used = ["P", "mean", "B"] + (["L"] if self.name == "L2" else ["penalty"])
        if self.name == "FILTER2":
            used += ["process"]
        return {
            "fitted_scalars": sum(tensors[k].numel() for k in used),
            "persistent_bytes": sum(t.numel() * t.element_size() for t in tensors.values()),
            "state_floats": 6 if self.name == "FILTER2" else 2,
            "prior_workspace_floats": 6 if self.name == "FILTER2" else 2,
            "initial_macs": 50 if self.name == "L2" else 72,
            "predict_macs": 48 + (32 if self.name == "FILTER2" else 0),
            "correct_macs": 50 if self.name == "L2" else 90,
            "settle_macs": 0,
            "halting_macs": 0,
            "readout_macs": 24,
            "nonlinear_note": "bilinear products plus 2x2 solves/inverses; solves excluded from linear MAC proxy; use measured CPU",
        }


def make(name, seed):
    return Linear(name, seed) if name in LINEAR else Neural(name, seed)
