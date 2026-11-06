"""Frozen E1 v1 equations. Construction does not train or select a candidate."""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import torch
from torch import nn

from soam.platform.core import tensor_check

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_HASH = "beda95e9aba660c4b912339dfe26f331363e8de7cbc715af132e95fd1821d83e"
PROTOCOL_HASH = "98846328f3ad6803a7e85d910fc2be2f8075c5d44e75d19351ad311d9eae12bf"


def manifest():
    path = ROOT / "docs/protocols/shared_population_v1.json"
    for source, expected in (
        (path, MANIFEST_HASH),
        (ROOT / "docs/SHARED_POPULATION_PROTOCOL.md", PROTOCOL_HASH),
    ):
        if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise ValueError("E1 protocol changed; review a new version before execution")
    return json.loads(path.read_text())


@dataclass(frozen=True)
class Spec:
    kind: str
    width: int
    features: int = 12
    actions: int = 3


def param(shape, generator, bound=None):
    x = torch.zeros(shape, dtype=torch.float32)
    if bound is not None:
        x.uniform_(-bound, bound, generator=generator)
    return nn.Parameter(x)


class Bank(nn.Module):
    def __init__(self, n, generator, kind="shared"):
        super().__init__()
        self.n, self.kind = n, kind
        self.E = param((n, 24), generator, 1 / 24**0.5)
        self.e = param((n,), generator)
        self.D = param((12, n), generator, 1 / n**0.5)
        self.d = param((12,), generator)
        self.b = param((n,), generator)
        i, j = torch.triu_indices(n, n)
        s = torch.randn(len(i), generator=generator, dtype=torch.float32) * (0.1 / n**0.5)
        s[i == j] = 0.5
        self.S = nn.Parameter(s)
        if kind in ("shared", "transition"):
            self.A = nn.Parameter(
                torch.randn(4, n * (n - 1) // 2, generator=generator, dtype=torch.float32)
                * (0.01 / n**0.5)
            )
        if kind != "recall":
            self.U = param((n, 3), generator, 1 / 3**0.5)
        if kind in ("shared", "symmetric"):
            self.v = param((n,), generator)

    def matrices(self):
        i, j = torch.triu_indices(self.n, self.n)
        upper = self.S.new_zeros(self.n, self.n)
        upper[i, j] = self.S
        symmetric = upper + upper.T - torch.diag(upper.diag())
        if not hasattr(self, "A"):
            return symmetric, None
        i, j = torch.triu_indices(self.n, self.n, 1)
        upper = self.A.new_zeros(4, self.n, self.n)
        upper[:, i, j] = self.A
        return symmetric, upper - upper.transpose(1, 2)

    def correction(self, u):
        pre = u @ self.E.T + self.e
        tensor_check(pre, (len(u), self.n))
        return torch.tanh(pre)

    def advance(self, h, a, q):
        s, skew = self.matrices()
        pre = h @ s.T + self.b
        if skew is not None:
            coefficients = torch.cat((torch.ones_like(a[:, :1]), a), 1)
            direction = torch.einsum("bk,kij,bj->bi", coefficients, skew, h)
            pre = pre + q[:, 1:2] * direction
        if hasattr(self, "U"):
            pre = pre + a @ self.U.T
        if hasattr(self, "v"):
            pre = pre + q[:, 1:2] * self.v
        tensor_check(pre, h.shape)
        return 0.5 * h + 0.5 * torch.tanh(pre)

    def readout(self, h):
        return h @ self.D.T + self.d


class Candidate(nn.Module):
    def __init__(self, name, seed):
        super().__init__()
        row = next((r for r in manifest()["models"] if r["id"] == name), None)
        if row is None:
            raise ValueError("unknown E1 candidate")
        self.spec = Spec(name, row["state_floats_including_role"])
        self.n = row["width_per_bank"]
        self.separated = name.startswith("D")
        g = torch.Generator().manual_seed(seed)
        if name.startswith("D"):
            self.recall = Bank(self.n, g, "recall")
            self.transition = Bank(self.n, g, "transition")
        elif name.startswith("G"):
            self.E = param((self.n, 24), g, 1 / 24**0.5)
            self.e = param((self.n,), g)
            self.D = param((12, self.n), g, 1 / self.n**0.5)
            self.d = param((12,), g)
            with torch.random.fork_rng(devices=[]):
                torch.manual_seed(seed)
                self.gru = nn.GRUCell(5, self.n, dtype=torch.float32)
        elif name == "L12":
            self.L = param((12, 25), g)
            self.B = param((12, 52), g)
        else:
            self.bank = Bank(self.n, g, "symmetric" if name == "SYM32" else "shared")
        if sum(p.numel() for p in self.parameters()) != row["expected_trainable_scalars"]:
            raise AssertionError("candidate parameter count differs from frozen manifest")

    def initial_state(self, batch_size):
        if type(batch_size) is not int or batch_size < 1:
            raise ValueError("positive batch size required")
        return torch.zeros(batch_size, self.spec.width, dtype=torch.float32)

    def check_state(self, state):
        if not isinstance(state, torch.Tensor) or state.ndim != 2 or not len(state):
            raise ValueError("nonempty batched state required")
        tensor_check(state, (state.shape[0], self.spec.width))
        q = state[:, -2:]
        if not (((q == 0) | (q == 1)).all() and (q.sum(1) <= 1).all()):
            raise ValueError("invalid supplied role flags")
        if self.separated:
            for role in range(2):
                inactive = state[q[:, role] == 0, role * self.n : (role + 1) * self.n]
                if inactive.count_nonzero():
                    raise ValueError("inactive role bank must be zero")

    def _banks(self):
        return self.recall, self.transition

    def _selected(self, q, operation, output_width):
        """Run only selected rows; never evaluate an inactive neural bank."""
        outputs = []
        for role, bank in enumerate(self._banks()):
            selected = q[:, role] == 1
            output = q.new_zeros(len(q), output_width)
            if selected.any():
                output[selected] = operation(bank, selected, role)
            outputs.append(output)
        return outputs

    def assimilate(self, state, observation):
        self.check_state(state)
        observation.validate(len(state), 12, 2)
        q = state[:, -2:]
        first = q.sum(1, keepdim=True) == 0
        present = observation.cue_valid.all(1, keepdim=True)
        if (observation.cue_valid.any(1, keepdim=True) != present).any():
            raise ValueError("partial role cue is unsupported")
        if (first & ~present).any():
            raise ValueError("initial role cue required")
        incoming = observation.cue
        if present.any() and not (
            ((incoming[present[:, 0]] == 0) | (incoming[present[:, 0]] == 1)).all()
            and (incoming[present[:, 0]].sum(1) == 1).all()
        ):
            raise ValueError("role cue must be one-hot")
        if ((~first & present) & (incoming != q).any(1, keepdim=True)).any():
            raise ValueError("contradictory role cue")
        q = torch.where(first, incoming, q)
        u = torch.cat((observation.z, observation.valid.float()), 1)
        name = self.spec.kind
        if self.separated:
            correction = torch.cat(
                self._selected(q, lambda bank, rows, role: bank.correction(u[rows]), self.n), 1
            )
        elif name.startswith("G"):
            pre = u @ self.E.T + self.e
            tensor_check(pre, (len(u), self.n))
            correction = torch.tanh(pre)
        elif name == "L12":
            correction = torch.cat((u, torch.ones_like(u[:, :1])), 1) @ self.L.T
        else:
            correction = self.bank.correction(u)
        h = torch.where(first, correction, 0.5 * state[:, :-2] + 0.5 * correction)
        result = torch.cat((h, q), 1)
        self.check_state(result)
        return result

    def advance(self, state, command, *, clamp_units=None):
        self.check_state(state)
        h, q, a = state[:, :-2], state[:, -2:], command.action
        tensor_check(a, (len(state), 3))
        if (q.sum(1) != 1).any() or (a[q[:, 0] == 1] != 0).any():
            raise ValueError("initialized role and zero recall command required")
        name = self.spec.kind
        if self.separated:
            out = torch.cat(
                self._selected(
                    q,
                    lambda bank, rows, role: bank.advance(
                        h[rows, role * self.n : (role + 1) * self.n], a[rows], q[rows]
                    ),
                    self.n,
                ),
                1,
            )
        elif name.startswith("G"):
            # Expose and check preactivations: bounded gates cannot hide overflow.
            x = torch.cat((a, q), 1)
            gi = torch.nn.functional.linear(x, self.gru.weight_ih, self.gru.bias_ih)
            gh = torch.nn.functional.linear(h, self.gru.weight_hh, self.gru.bias_hh)
            tensor_check(gi, (len(h), 3 * self.n))
            tensor_check(gh, (len(h), 3 * self.n))
            ir, iz, inn = gi.chunk(3, 1)
            hr, hz, hn = gh.chunk(3, 1)
            reset_pre, update_pre = ir + hr, iz + hz
            tensor_check(reset_pre, h.shape)
            tensor_check(update_pre, h.shape)
            reset, update = torch.sigmoid(reset_pre), torch.sigmoid(update_pre)
            candidate_pre = inn + reset * hn
            tensor_check(candidate_pre, h.shape)
            candidate = torch.tanh(candidate_pre)
            out = candidate + update * (h - candidate)
        elif name == "L12":
            inputs = torch.cat(
                (h, *(a[:, j : j + 1] * h for j in range(3)), a, torch.ones_like(a[:, :1])), 1
            )
            out = torch.where(q[:, :1].bool(), h, inputs @ self.B.T)
        else:
            out = self.bank.advance(h, a, q)
        if clamp_units is not None:
            tensor_check(clamp_units, (self.spec.width,), torch.bool)
            if clamp_units[-2:].any():
                raise ValueError("role flags are not lesionable neurons")
            out = out.masked_fill(clamp_units[:-2].unsqueeze(0), 0)
        result = torch.cat((out, q), 1)
        self.check_state(result)
        return result

    def readout(self, state):
        self.check_state(state)
        h, q = state[:, :-2], state[:, -2:]
        name = self.spec.kind
        if self.separated:
            out = sum(
                self._selected(
                    q,
                    lambda bank, rows, role: bank.readout(
                        h[rows, role * self.n : (role + 1) * self.n]
                    ),
                    12,
                )
            )
        elif name.startswith("G"):
            out = h @ self.D.T + self.d
        elif name == "L12":
            out = h.clone()
        else:
            out = self.bank.readout(h)
        tensor_check(out, (len(state), 12))
        return out


class TiedStateCandidate(Candidate):
    """No-fit T32 view: one actual S32 parameter store, two independent states.

    The source parameters are deliberately aliased, not copied. Construct this
    diagnostic from a frozen final checkpoint; inference never updates weights.
    """

    def __init__(self, source):
        nn.Module.__init__(self)
        if source.spec.kind != "S32":
            raise ValueError("T32 requires S32 parameters")
        self.spec = Spec("T32", 66)
        self.n = 32
        self.separated = True
        self.bank = source.bank

    def _banks(self):
        return self.bank, self.bank
