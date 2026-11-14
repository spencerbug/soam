"""Correction-only variants. Parameters are inherited unchanged from fitted FILTER2."""

from dataclasses import dataclass

import torch

from soam.temporal.models import Linear

# Exact tabulated upper .99 chi-square quantiles, dimensions 1..12.
CHI99 = (
    0.0,
    6.634897,
    9.210340,
    11.344867,
    13.276704,
    15.086272,
    16.811894,
    18.475307,
    20.090235,
    21.665994,
    23.209251,
    24.724970,
    26.216967,
)


@dataclass(frozen=True)
class Config:
    name: str = "STABLE"
    mode: str = "plain"
    r: float = 1.0
    q: float = 1.0
    gain: float = 1.0
    threshold: float = 1.0
    alpha: float = 1.0
    persistence: int = 2
    empirical6: float = CHI99[6]
    empirical12: float = CHI99[12]


def phase1():
    return [
        Config(),
        Config("R10", r=10),
        Config("R100", r=100),
        Config("Q01", q=0.1),
        Config("Q10", q=10),
        Config("GAIN25", gain=0.25),
        Config("GAIN50", gain=0.5),
        Config("NIS99", "nis"),
        Config("NISEMP", "nis_emp"),
        Config("RAW05", "raw", threshold=0.05),
        Config("RAW10", "raw", threshold=0.1),
        Config("HUBER99", "huber"),
        Config("CHANNEL2", "channel", threshold=2),
        Config("CHANNEL4", "channel", threshold=4),
    ]


class Robust(Linear):
    def __init__(self, fitted, config):
        super().__init__("FILTER2")
        self.load_state_dict(fitted.state_dict())
        self.double()
        self.config = config
        self.name = config.name
        self.diagnostics = False
        self.last = None

    def initialize(self, z, m):
        z = z.double()
        h = self.decode_mean(z, m)
        information = self.P.T @ (self.P[None] * m[..., None]) / 0.0001 + torch.eye(
            2, dtype=z.dtype
        )
        cov = torch.linalg.solve(information, torch.eye(2, dtype=z.dtype).expand_as(information))
        extra = []
        if self.config.mode in {"adaptive", "hybrid"}:
            extra.append(torch.full_like(h[:, :1], 0.0001))
        if self.config.mode in {"temporal", "hybrid"}:
            extra.append(torch.zeros((len(h), 4), dtype=h.dtype))
        return torch.cat((h, cov.flatten(1), *extra), -1)

    def predict(self, h, a, q):
        # Keep exact fitted transition, including affine/action-only terms.
        from soam.gating.models import bilinear

        a = a.double()
        x = bilinear(h[:, :2], a) @ self.B.T
        x = torch.where(q[:, :1].bool(), h[:, :2], x)
        jac = self.B[:, :2][None] + sum(
            a[:, j, None, None] * self.B[:, 2 + 2 * j : 4 + 2 * j] for j in range(3)
        )
        jac = torch.where(q[:, :1, None].bool(), torch.eye(2, dtype=h.dtype), jac)
        cov = (
            jac @ h[:, 2:6].reshape(-1, 2, 2) @ jac.transpose(-1, -2) + self.config.q * self.process
        )
        history = h[:, 6:].clone()
        if self.config.mode in {"temporal", "hybrid"}:
            offset = 1 if self.config.mode == "hybrid" else 0
            history[:, offset : offset + 2] = (jac @ history[:, offset : offset + 2, None])[..., 0]
            history[:, offset + 3] += 1
            history[:, offset + 2] = torch.where(
                history[:, offset + 3] > 16, 0.0, history[:, offset + 2]
            )
        return torch.cat((x, cov.flatten(1), history), -1), torch.ones_like(x[:, :1])

    def readout(self, h):
        return h[:, :2] @ self.P.T + self.mean

    def _gain(self, cov, m, variance):
        eye = torch.eye(2, dtype=cov.dtype).expand_as(cov)
        precision = torch.linalg.solve(cov, eye)
        weighted_h = self.P[None] * (m / variance)[..., None]
        information = precision + self.P.T @ weighted_h
        # One solve for posterior precision inverse and gain, no explicit inverse.
        answer = torch.linalg.solve(information, torch.cat((eye, weighted_h.transpose(-1, -2)), -1))
        return answer[:, :, 2:], answer[:, :, :2]

    def correct(self, prior, previous, a, q, z, m, sd, *, metadata=False):
        cfg = self.config
        cov = prior[:, 2:6].reshape(-1, 2, 2)
        innovation = torch.where(m, z.double() - self.readout(prior), 0.0)
        variance = torch.full_like(innovation, 0.0001 * cfg.r)
        d = m.sum(-1)
        history = prior[:, 6:].clone()
        orth = None
        displacement = None
        if cfg.mode in {"adaptive", "temporal", "hybrid"}:
            gram = self.P.T @ (self.P[None] * m[..., None])
            displacement = torch.linalg.solve(
                gram + 1e-12 * torch.eye(2, dtype=prior.dtype), (innovation @ self.P)[..., None]
            )[..., 0]
            orth = ((innovation - displacement @ self.P.T) * m).square().sum(-1) / (
                d - 2
            ).clamp_min(1)
            full_rank = torch.linalg.eigvalsh(gram)[:, 0] > 1e-8
            identifiable = (d > 2) & full_rank
            if cfg.mode in {"adaptive", "hybrid"}:
                estimate = orth.clamp(0.0001, 0.25)
                new_r = cfg.alpha * estimate + (1 - cfg.alpha) * history[:, 0]
                new_r = torch.where(identifiable, new_r, history[:, 0])
                variance = new_r[:, None].expand_as(innovation)
                history[:, 0] = torch.where(d > 0, new_r, history[:, 0])
        gain, covariance = self._gain(cov, m, variance)
        scaled = innovation / variance
        b = scaled @ self.P
        nis = (
            (innovation * scaled).sum(-1) - (b[:, None] @ covariance @ b[..., None]).flatten()
        ).clamp_min(0)
        d = m.sum(-1)
        threshold = torch.tensor(CHI99, dtype=prior.dtype)[d]
        if cfg.mode == "nis_emp":
            threshold = torch.where(d == 12, cfg.empirical12, cfg.empirical6)
        weight = torch.ones_like(innovation)
        reject = torch.zeros_like(d, dtype=torch.bool)
        if cfg.mode.startswith("nis") or cfg.mode in {"temporal", "hybrid"}:
            reject = nis > threshold
        elif cfg.mode == "huber":
            weight *= torch.minimum(
                torch.ones_like(nis), torch.sqrt(threshold / nis.clamp_min(1e-30))
            )[:, None]
        elif cfg.mode == "raw":
            rms = torch.sqrt(innovation.square().sum(-1) / d.clamp_min(1))
            weight *= (cfg.threshold / rms.clamp_min(1e-30)).clamp_max(1)[:, None]
        elif cfg.mode == "channel":
            diag = torch.einsum("mi,bij,mj->bm", self.P, cov, self.P) + variance
            weight = (cfg.threshold * diag.sqrt() / innovation.abs().clamp_min(1e-30)).clamp_max(1)
        if cfg.mode in {"huber", "raw", "channel"}:
            variance = variance / weight.clamp_min(1e-8)
            gain, _ = self._gain(cov, m, variance)
        if cfg.mode in {"temporal", "hybrid"}:
            offset = 1 if cfg.mode == "hybrid" else 0
            previous_displacement = history[:, offset : offset + 2]
            close = (displacement - previous_displacement).norm(dim=-1) <= 0.15 * displacement.norm(
                dim=-1
            ).clamp_min(1)
            plausible = identifiable & (orth <= 0.0025) & reject
            count = torch.where(plausible, torch.where(close, history[:, offset + 2] + 1, 1.0), 0.0)
            release = count >= cfg.persistence
            reject = reject & ~release
            history[:, offset : offset + 2] = torch.where(plausible[:, None], displacement, 0.0)
            history[:, offset + 2] = torch.where(release, 0.0, count)
            history[:, offset + 3] = torch.where(d > 0, 0.0, history[:, offset + 3])
        gain = gain * cfg.gain
        reject |= d == 0
        gain = torch.where(reject[:, None, None], 0.0, gain)
        delta = (gain @ innovation[..., None])[..., 0]
        x = prior[:, :2] + delta
        residual = torch.eye(2, dtype=prior.dtype) - gain @ self.P
        updated_cov = residual @ cov @ residual.transpose(-1, -2) + (
            gain * variance[:, None]
        ) @ gain.transpose(-1, -2)
        updated_cov = 0.5 * (updated_cov + updated_cov.transpose(-1, -2))
        core = torch.cat((x, updated_cov.flatten(1)), -1)
        core = torch.where(reject[:, None], prior[:, :6], core)
        history = torch.where((d > 0)[:, None], history, prior[:, 6:])
        posterior = torch.cat((core, history), -1)
        if cfg.mode in {"adaptive", "hybrid"}:
            weight = (0.0001 / variance).clamp_max(1)
        event_weight = (weight * m).sum(-1) / d.clamp_min(1) * cfg.gain
        event_weight = torch.where(reject, 0.0, event_weight)
        if self.diagnostics:
            self.last = {
                "innovation": innovation,
                "nis": nis,
                "weight": weight * m * (~reject[:, None]),
                "event_weight": event_weight,
                "reject": reject,
                "delta": delta,
                "gain": gain,
                "Sdiag": torch.einsum("mi,bij,mj->bm", self.P, cov, self.P) + 0.0001 * cfg.r,
            }
        return posterior, event_weight[:, None]

    def resources(self):
        out = super().resources()
        out.update(
            fitted_scalars=64,
            persistent_bytes=sum(t.numel() * t.element_size() for t in self.buffers()),
            state_floats=6
            + (1 if self.config.mode in {"adaptive", "hybrid"} else 0)
            + (4 if self.config.mode in {"temporal", "hybrid"} else 0),
            prior_workspace_floats=6,
            correct_macs=90,
            predict_macs=80,
            nonlinear_note="Joseph covariance and diagnostic NIS; 2x2 solves; robust modes add a second gain solve; MAC proxy inherited only, not equal-compute claim",
        )
        return out
