"""E0 models receive evidence/actions only and never mutate persistent state in inference."""

import math

import torch
from torch import nn

NAMES = ("NAV32", "SYM32", "GRU32", "PCA2")


class Neural(nn.Module):
    def __init__(self, name, seed):
        super().__init__()
        if name not in NAMES[:3]:
            raise ValueError("unknown neural model")
        self.name, self.n = name, 32
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed)
            self.E = nn.Linear(24, 32)
            self.D = nn.Linear(32, 12)
            self.C = nn.Linear(24, 32, bias=False)
            if name == "GRU32":
                self.core = nn.GRUCell(1, 32)
            else:
                self.W = nn.Parameter(torch.eye(32) + 0.01 * torch.randn(32, 32))
                self.V = nn.Parameter(0.01 * torch.randn(32, 32))
                self.bias = nn.Parameter(torch.zeros(32))

    def initialize(self, z, mask):
        return torch.tanh(self.E(torch.cat((z * mask, mask.float()), -1)))

    def readout(self, h):
        return self.D(h)

    def matrices(self):
        s = 0.5 * (self.W + self.W.T)
        k = 0.5 * (self.V - self.V.T if self.name == "NAV32" else self.V + self.V.T)
        return s, k

    def predict(self, h, action):
        if self.name == "GRU32":
            return self.core(action / 0.12, h)
        s, k = self.matrices()
        return 0.5 * h + 0.5 * torch.tanh(h @ s.T + self.bias + action / 0.12 * (h @ k.T))

    def correct(self, prior, z, mask):
        residual = (z - self.readout(prior)) * mask
        delta = 0.5 * torch.tanh(self.C(torch.cat((residual, mask.float()), -1)))
        return torch.where(mask.any(-1, keepdim=True), prior + delta, prior)

    def resources(self):
        return {
            "parameters": sum(p.numel() for p in self.parameters()),
            "persistent_bytes": sum(p.numel() * p.element_size() for p in self.parameters()),
            "state_floats": 32,
            "prior_workspace_floats": 32,
            "initial_macs": 24 * 32,
            "predict_macs": 3 * (32 * 32 + 32) if self.name == "GRU32" else 2 * 32 * 32,
            "readout_macs": 32 * 12,
            "correct_macs": 32 * 12 + 24 * 32,
            "note": "MACs exclude biases, elementwise/nonlinear work and matrix symmetrization; timing measured",
            "effective_core_matrix_dof": None
            if self.name == "GRU32"
            else (32 * 32 if self.name == "NAV32" else 32 * 33),
        }


class PCAFilter(nn.Module):
    def __init__(self):
        super().__init__()
        self.name, self.n = "PCA2", 2
        for name, tensor in {
            "mean": torch.zeros(12),
            "P": torch.zeros(12, 2),
            "B": torch.zeros(2, 6),
            "process": torch.eye(2) * 1e-6,
        }.items():
            self.register_buffer(name, tensor)

    def initialize(self, z, mask):
        precision = self.P.T @ (self.P[None] * mask[..., None]) / 0.0001
        cov = torch.linalg.inv(precision + torch.eye(2) * 1e-6)
        rhs = ((z - self.mean) * mask) @ self.P / 0.0001
        h = (cov @ rhs[..., None])[..., 0]
        return torch.cat((h, cov.flatten(1)), -1)

    def readout(self, h):
        return h[:, :2] @ self.P.T + self.mean

    def predict(self, h, action):
        jac = torch.eye(2) + sum(
            action[..., None] ** (j + 1) * self.B[:, 2 * j : 2 * j + 2] for j in range(3)
        )
        y = (jac @ h[:, :2, None])[..., 0]
        cov = jac @ h[:, 2:].reshape(-1, 2, 2) @ jac.transpose(-1, -2) + self.process
        return torch.cat((y, cov.flatten(1)), -1)

    def correct(self, prior, z, mask):
        cov = prior[:, 2:].reshape(-1, 2, 2)
        precision = torch.linalg.inv(cov)
        update_precision = precision + self.P.T @ (self.P[None] * mask[..., None]) / 0.0001
        new_cov = torch.linalg.inv(update_precision)
        rhs = (precision @ prior[:, :2, None])[..., 0]
        rhs = rhs + ((z - self.mean) * mask) @ self.P / 0.0001
        y = (new_cov @ rhs[..., None])[..., 0]
        update = torch.cat((y, new_cov.flatten(1)), -1)
        return torch.where(mask.any(-1, keepdim=True), update, prior)

    def resources(self):
        return {
            "parameters": sum(t.numel() for t in self.buffers()),
            "persistent_bytes": sum(t.numel() * t.element_size() for t in self.buffers()),
            "state_floats": 6,
            "prior_workspace_floats": 6,
            "initial_macs": 72,
            "predict_macs": 36,
            "readout_macs": 24,
            "correct_macs": 100,
            "note": "Four covariance entries counted; only two mean coordinates receive geometry perturbations. MAC proxy excludes 2x2 inverses and elementwise work.",
        }


def make(name, seed):
    if name not in NAMES:
        raise ValueError("unknown E0 model")
    return PCAFilter() if name == "PCA2" else Neural(name, seed)


def learning_rate(initial, update, total):
    return initial * (0.01 + 0.99 * 0.5 * (1 + math.cos(math.pi * update / max(total - 1, 1))))
