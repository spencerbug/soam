"""Evidence-only candidate states, fixed PC gains and inherited B2 correctors."""

import math

import torch
from torch import nn

from soam.robust.models import Config, Robust
from soam.temporal.models import Linear, Neural


def weights(logit):
    p = logit.sigmoid()
    return torch.stack((1 - p, p), -1)


def advance_support(logit):
    w = 0.98 * weights(logit) + 0.01
    return torch.log(w[:, 1]) - torch.log(w[:, 0])


def mixing(logit):
    w = weights(logit)
    trans = w.new_tensor([[0.99, 0.01], [0.01, 0.99]])
    joint = w[:, :, None] * trans
    return joint / joint.sum(1, keepdim=True)


def mix_gaussian(state, mix):
    """B,I,D states and B,I,J conditional weights -> B,J,D moment matches."""
    mu, cov = state[..., :2], state[..., 2:6].reshape(*state.shape[:2], 2, 2)
    mean = torch.einsum("bij,bik->bjk", mix, mu)
    delta = mu[:, :, None] - mean[:, None]
    total = cov[:, :, None] + delta[..., :, None] * delta[..., None, :]
    covariance = torch.einsum("bij,bijxy->bjxy", mix, total)
    extras = torch.einsum("bij,bik->bjk", mix, state[..., 6:])
    return torch.cat((mean, covariance.flatten(-2), extras), -1)


class Recurrent(nn.Module):
    def __init__(self, width=16, multiple=False, seed=0):
        super().__init__()
        self.width, self.multiple = width, multiple
        # Historical constructor recognizes 16/32 only; explicitly resize for PC40.
        self.core = Neural("PC16" if width == 16 else "PC32", seed)
        if width not in {16, 32}:
            with torch.random.fork_rng(devices=[]):
                torch.manual_seed(seed)
                self.core.n = width
                for name, layer in {
                    "initial": nn.Linear(24, width),
                    "W": nn.Linear(width, width),
                    "A": nn.Linear(3, width, bias=False),
                    "Q": nn.Linear(2, width, bias=False),
                    "D": nn.Linear(width, 12),
                    "E": nn.Linear(24, width, bias=False),
                }.items():
                    setattr(self.core, name, layer)
        if not multiple:
            with torch.random.fork_rng(devices=[]):
                torch.manual_seed(seed + 1)
                self.offset = nn.Linear(width, 12, bias=False)
                nn.init.zeros_(self.offset.weight)
        self.register_buffer("variance", torch.full((12,), 0.0025))
        self.temperature = 1.0
        self.name = "TWO16" if multiple else f"PC{width}"

    def initialize(self, z, mask):
        h = self.core.initialize(z, mask)
        return h[:, None].repeat(1, 2 if self.multiple else 1, 1)

    def predict(self, state, action, logit):
        if self.multiple:
            state = torch.einsum("bij,bik->bjk", mixing(logit), state)
            a = action[:, None].repeat(1, 2, 1)
            a[:, 0, 0] *= -1
        else:
            a = action[:, None]
        flat = state.flatten(0, 1)
        q = flat.new_zeros((len(flat), 2))
        q[:, 1] = 1
        return self.core.predict(flat, a.flatten(0, 1), q)[0].reshape_as(state)

    def decode(self, state):
        out = self.core.readout(state)
        if self.multiple:
            return out
        delta = self.offset(state[:, 0])
        return out + torch.stack((-delta, delta), 1)

    def score(self, prior, z, mask):
        residual = (z[:, None] - self.decode(prior)) * mask[:, None]
        terms = residual.square() / self.variance
        nis = terms.sum(-1)
        logdet = (mask * self.variance.log()).sum(-1)[:, None]
        d = mask.sum(-1)[:, None]
        score = -0.5 * (nis + logdet + d * math.log(2 * math.pi))
        return score, nis / d.clamp_min(1), nis

    def correct(self, prior, z, mask, logit):
        predictions = self.decode(prior)
        if not self.multiple:
            predictions = (predictions * weights(logit)[..., None]).sum(1, keepdim=True)
        residual = (z[:, None] - predictions) * mask[:, None]
        masks = mask[:, None].expand(*residual.shape)
        update = prior + 0.5 * torch.tanh(self.core.E(torch.cat((residual, masks.float()), -1)))
        return torch.where(mask.any(-1)[:, None, None], update, prior)

    def retain(self, posterior, logit):
        return posterior

    def resources(self):
        n, k = self.width, 2 if self.multiple else 1
        return {
            "fitted_scalars": sum(p.numel() for p in self.parameters()) + 13,
            "gradient_fitted_scalars": sum(p.numel() for p in self.parameters()),
            "calibration_fitted_scalars": 13,
            "development_selected_scalars": 1,
            "persistent_bytes": sum(
                x.numel() * x.element_size() for x in self.state_dict().values()
            ),
            "retained_scalars": n * k + 1,
            "retained_bytes": 4 * (n * k + 1),
            "prior_workspace_scalars": n * k,
            "posterior_workspace_scalars": n * k,
            "candidate_prediction_scalars": 24,
            "confidence_workspace_scalars": 9,
            "initial_macs": 24 * n,
            "predict_macs": k * (n * n + 5 * n),
            "decode_macs": 48 * n,
            "correction_macs": k * 24 * n,
            "evidence_note": "24 diagonal residual squares/scales; one log-odds update",
            "supplied_constants": "two candidate signs, hazard, clip, temperature; fixed gains",
            "supplied_rule_scalars": 8,
            "calibration_scalar_bytes_outside_tensors": 16,
            "operation_counts_per_step": "k predictions and k corrections (including empty-mask work), two candidate score evaluations, one support update; two decode calls in timed loop",
            "allocation_limit": "Tensor bytes plus separately declared scalar settings; Python/Torch object overhead is captured by process RSS, not this logical ledger",
        }


class Conventional(nn.Module):
    def __init__(self, fitted, kind="ADAPT1", multiple=False, thresholds=(16.811894, 26.216967)):
        super().__init__()
        self.kind, self.multiple = kind, multiple
        if kind == "FILTER2":
            self.core = Linear("FILTER2")
            self.core.load_state_dict(fitted.state_dict())
        else:
            mode = "adaptive" if kind == "ADAPT1" else "nis_emp"
            self.core = Robust(
                fitted, Config(kind, mode, empirical6=thresholds[0], empirical12=thresholds[1])
            )
        self.name = kind + ("-M" if multiple else "-C")
        self.temperature = 1.0

    @property
    def dtype(self):
        return self.core.P.dtype

    def initialize(self, z, mask):
        state = self.core.initialize(z.to(self.dtype), mask)
        return state[:, None].repeat(1, 2 if self.multiple else 1, 1)

    def predict(self, state, action, logit):
        if self.multiple:
            state = mix_gaussian(state, mixing(logit).to(state.dtype))
        else:
            state = state.expand(-1, 2, -1)
        a = action.to(self.dtype)[:, None].repeat(1, 2, 1)
        a[:, 0, 0] *= -1
        flat = state.flatten(0, 1)
        q = flat.new_zeros((len(flat), 2))
        q[:, 1] = 1
        return self.core.predict(flat, a.flatten(0, 1), q)[0].reshape_as(state)

    def decode(self, state):
        return state[..., :2] @ self.core.P.T + self.core.mean

    def score(self, prior, z, mask):
        # Woodbury and determinant lemma: score BEFORE current-observation R adaptation.
        c = prior[..., 2:6].reshape(-1, 2, 2).double()
        h = self.core.P.double()
        m = mask[:, None].expand(-1, 2, -1).flatten(0, 1)
        r = ((z.double()[:, None] - self.decode(prior).double()) * mask[:, None]).flatten(0, 1)
        variance = (
            prior[..., 6].flatten().double()
            if self.kind == "ADAPT1"
            else torch.full((len(c),), 0.0001, dtype=torch.float64)
        )
        inv = torch.linalg.solve(c, torch.eye(2, dtype=c.dtype).expand_as(c))
        info = inv + h.T @ (h[None] * (m / variance[:, None])[..., None])
        b = (r / variance[:, None]) @ h
        nis = (
            r.square().sum(-1) / variance
            - (b * torch.linalg.solve(info, b[..., None])[..., 0]).sum(-1)
        ).clamp_min(0)
        d = m.sum(-1)
        logdet = d * variance.log() + torch.linalg.slogdet(c)[1] + torch.linalg.slogdet(info)[1]
        score = -0.5 * (nis + logdet + d * math.log(2 * math.pi))
        return score.reshape(-1, 2), (nis / d.clamp_min(1)).reshape(-1, 2), nis.reshape(-1, 2)

    def correct(self, prior, z, mask, logit):
        b = len(prior)
        flat = prior.flatten(0, 1)
        z = z.to(self.dtype)[:, None].expand(-1, 2, -1).reshape(-1, 12)
        m = mask[:, None].expand(-1, 2, -1).reshape(-1, 12)
        a, q = flat.new_zeros((2 * b, 3)), flat.new_zeros((2 * b, 2))
        sd = flat.new_full((2 * b, 1), 0.01)
        return self.core.correct(flat, flat, a, q, z, m, sd)[0].reshape_as(prior)

    def retain(self, posterior, logit):
        if self.multiple:
            return posterior
        return mix_gaussian(posterior, weights(logit).to(posterior.dtype)[..., None])

    def resources(self):
        k, d = (2 if self.multiple else 1), (7 if self.kind == "ADAPT1" else 6)
        return {
            "fitted_scalars": 65 + (1 if self.kind == "NISEMP" else 0),
            "calibration_fitted_scalars": 1 + (1 if self.kind == "NISEMP" else 0),
            "development_selected_scalars": 1,
            "persistent_bytes": sum(
                x.numel() * x.element_size() for x in self.state_dict().values()
            ),
            "retained_scalars": k * d + 1,
            "retained_bytes": (k * d + 1) * (4 if self.kind == "FILTER2" else 8),
            "prior_workspace_scalars": 2 * d,
            "posterior_workspace_scalars": 2 * d,
            "candidate_prediction_scalars": 24,
            "confidence_workspace_scalars": 9,
            "initial_macs": 72,
            "predict_macs": 160,
            "decode_macs": 96,
            "correction_macs": 180,
            "evidence_note": "two covariance-conditioned 2x2 solve/logdet scores; mixing/collapse work extra",
            "supplied_constants": "two signs, hazard, clip, temperature, nominal R/ridge; ADAPT bounds or NIS thresholds",
            "supplied_rule_scalars": 10 if self.kind == "ADAPT1" else 8,
            "calibration_scalar_bytes_outside_tensors": 24 if self.kind == "NISEMP" else 16,
            "operation_counts_per_step": "two predictions, two corrections including missing-mask work, two covariance-conditioned evidence scores and one support update; additional moment mixing/collapse",
            "allocation_limit": "Tensor bytes plus separately declared scalar settings; Python/Torch object overhead is captured by process RSS, not this logical ledger",
            "mac_limit": "inherited partial linear proxy excludes solves, mixing, robust R and elementwise work",
        }
