"""Study A recurrences. No simulator or target access in any model operation."""

import copy

import torch
from torch import nn
from torch.nn import functional as F

from soam.shared.models import Bank, Candidate


class Core(nn.Module):
    def __init__(self, kind, width, seed):
        super().__init__()
        self.kind, self.n = kind, width
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed)
            if kind in ("ridge", "pca_ridge"):
                self.L = nn.Parameter(torch.zeros(width, 25))
                self.B = nn.Parameter(torch.zeros(width, 4 * width + 4))
                if width == 2:
                    self.P = nn.Parameter(torch.zeros(12, 2))
                    self.mean = nn.Parameter(torch.zeros(12))
                return
            if kind in ("s32", "gated_s32"):
                self.bank = Bank(width, torch.Generator().manual_seed(seed))
                if kind == "gated_s32":
                    self.gate = nn.Linear(width + 5, width)
                    nn.init.zeros_(self.gate.weight)
                    nn.init.zeros_(self.gate.bias)
                return
            # Same E/D and GRU initializations as the historical G32 convention.
            old = Candidate("G32", seed) if width == 32 else None
            g = torch.Generator().manual_seed(seed)
            self.E = nn.Parameter(
                torch.empty(width, 24).uniform_(-(24**-0.5), 24**-0.5, generator=g)
            )
            self.e = nn.Parameter(torch.zeros(width))
            self.D = nn.Parameter(
                torch.empty(12, width).uniform_(-(width**-0.5), width**-0.5, generator=g)
            )
            self.d = nn.Parameter(torch.zeros(12))
            if kind in ("gru", "fixed_update", "fixed_reset", "fixed_both"):
                cell = old.gru if old is not None else nn.GRUCell(5, width)
                for k, index in [("r", 0), ("z", 1), ("c", 2)]:
                    constant = (k == "z" and kind in ("fixed_update", "fixed_both")) or (
                        k == "r" and kind in ("fixed_reset", "fixed_both")
                    )
                    if constant:
                        self.register_parameter(k + "_constant", nn.Parameter(torch.zeros(width)))
                    else:
                        for key, value in [
                            ("W", cell.weight_ih),
                            ("U", cell.weight_hh),
                            ("bi", cell.bias_ih),
                            ("bh", cell.bias_hh),
                        ]:
                            self.register_parameter(
                                k + "_" + key,
                                nn.Parameter(
                                    value[index * width : (index + 1) * width].detach().clone()
                                ),
                            )
            elif kind in ("rnn", "gated_leaky"):
                self.core = nn.Linear(width + 5, width)
                if kind == "gated_leaky":
                    self.gate = nn.Linear(width + 5, width)
            else:
                raise ValueError(f"unknown kind {kind}")

    def encode(self, z, valid):
        u = torch.cat((z, valid.float()), -1)
        if self.kind in ("ridge", "pca_ridge"):
            return F.linear(torch.cat((u, torch.ones_like(u[:, :1])), -1), self.L)
        if self.kind in ("s32", "gated_s32"):
            return torch.tanh(F.linear(u, self.bank.E, self.bank.e))
        return torch.tanh(F.linear(u, self.E, self.e))

    def assimilate(self, h, z, valid):
        correction = self.encode(z, valid)
        return correction if h is None else 0.5 * h + 0.5 * correction

    def readout(self, h):
        if self.kind == "ridge":
            return h
        if self.kind == "pca_ridge":
            return h @ self.P.T + self.mean
        if self.kind in ("s32", "gated_s32"):
            return F.linear(h, self.bank.D, self.bank.d)
        return F.linear(h, self.D, self.d)

    def step(self, h, a, q, *, overrides=None, diagnostics=False):
        x = torch.cat((a, q), -1)
        overrides = {} if overrides is None else overrides
        if self.kind in ("ridge", "pca_ridge"):
            c = F.linear(bilinear(h, a), self.B)
            out = torch.where(q[:, :1].bool(), h, c)
            alpha = q[:, 1:2].expand_as(h)
            reset = torch.ones_like(h)
        elif self.kind in ("s32", "gated_s32"):
            b = self.bank
            s, skew = b.matrices()
            coefficients = torch.cat((torch.ones_like(a[:, :1]), a), 1)
            pre = F.linear(h, s, b.b) + q[:, 1:2] * torch.einsum(
                "bk,kij,bj->bi", coefficients, skew, h
            )
            c = torch.tanh(pre + F.linear(a, b.U) + q[:, 1:2] * b.v)
            alpha = (
                torch.sigmoid(self.gate(torch.cat((h, x), -1)))
                if self.kind == "gated_s32"
                else torch.full_like(h, 0.5)
            )
            alpha = torch.as_tensor(overrides.get("alpha", alpha), dtype=h.dtype).expand_as(h)
            reset = torch.ones_like(h)
            out = (1 - alpha) * h + alpha * c
        elif self.kind in ("rnn", "gated_leaky"):
            inputs = torch.cat((h, x), -1)
            c = torch.tanh(self.core(inputs))
            alpha = (
                torch.sigmoid(self.gate(inputs))
                if self.kind == "gated_leaky"
                else torch.full_like(h, 0.5)
            )
            alpha = torch.as_tensor(overrides.get("alpha", alpha), dtype=h.dtype).expand_as(h)
            reset = torch.ones_like(h)
            out = (1 - alpha) * h + alpha * c
        else:

            def gate(k):
                if hasattr(self, k + "_constant"):
                    return torch.sigmoid(getattr(self, k + "_constant")).expand_as(h)
                return torch.sigmoid(
                    F.linear(x, getattr(self, k + "_W"), getattr(self, k + "_bi"))
                    + F.linear(h, getattr(self, k + "_U"), getattr(self, k + "_bh"))
                )

            reset = torch.as_tensor(overrides.get("reset", gate("r")), dtype=h.dtype).expand_as(h)
            alpha = torch.as_tensor(overrides.get("alpha", 1 - gate("z")), dtype=h.dtype).expand_as(
                h
            )
            c = torch.tanh(
                F.linear(x, self.c_W, self.c_bi) + reset * F.linear(h, self.c_U, self.c_bh)
            )
            out = c + (1 - alpha) * (h - c)
        if diagnostics:
            return out, {"alpha": alpha, "retention": 1 - alpha, "reset": reset, "candidate": c}
        return out

    def costs(self):
        n, k = self.n, self.kind
        if k in ("ridge", "pca_ridge"):
            mac = n * (4 * n + 4) + (12 * n if n == 2 else 0)
            initialization = n * 25
        elif k in ("s32", "gated_s32"):
            mac = 5 * n * n + 15 * n + ((n * n + 5 * n) if k == "gated_s32" else 0)
            initialization = 24 * n
        elif k in ("rnn", "gated_leaky"):
            mac = n * n + 17 * n + ((n * n + 5 * n) if k == "gated_leaky" else 0)
            initialization = 24 * n
        else:
            blocks = 3 - int(hasattr(self, "r_constant")) - int(hasattr(self, "z_constant"))
            mac = blocks * (n * n + 5 * n) + 12 * n
            initialization = 24 * n
        parameters = sum(p.numel() for p in self.parameters())
        return {
            "parameters": parameters,
            "parameter_bytes": 4 * parameters,
            "active_hidden": n,
            "state_floats_with_role": n + 2,
            "advance_readout_linear_macs": mac,
            "initialization_linear_macs": initialization,
            "mac_excludes": "nonlinearities, elementwise arithmetic, matrix expansion and backward; S32 counts four skew matvecs",
        }


def bilinear(h, a):
    return torch.cat(
        (h, *(a[..., j : j + 1] * h for j in range(3)), a, torch.ones_like(a[..., :1])), -1
    )


def fold_fixed_reset(source):
    """Exactly the same function in real arithmetic, with redundant bias/reset removed."""
    if source.kind != "fixed_reset":
        raise ValueError("FR required")
    target = Core("gated_leaky", source.n, 0)
    with torch.no_grad():
        for key in ("E", "e", "D", "d"):
            getattr(target, key).copy_(getattr(source, key))
        r = torch.sigmoid(source.r_constant)
        target.core.weight.copy_(torch.cat((r[:, None] * source.c_U, source.c_W), 1))
        target.core.bias.copy_(source.c_bi + r * source.c_bh)
        target.gate.weight.copy_(-torch.cat((source.z_U, source.z_W), 1))
        target.gate.bias.copy_(-source.z_bi - source.z_bh)
    return target


def snapshot(model):
    return copy.deepcopy(model.state_dict())
