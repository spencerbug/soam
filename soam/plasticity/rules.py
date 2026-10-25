"""One-step local correction; no BPTT or access to simulator ground truth."""

import math
from dataclasses import asdict, dataclass
from typing import Protocol

import torch


@dataclass(frozen=True)
class WriteConfig:
    learning_rate: float = 0.1
    damping: float = 0.001
    key_epsilon: float = 1e-8
    max_update_norm: float = 0.01
    max_total_norm: float = 0.1
    max_rank: int = 1

    def validate(self):
        values = asdict(self)
        if any(
            isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v <= 0
            for v in values.values()
        ):
            raise ValueError("writer settings must be finite positive numbers")
        if type(self.max_rank) is not int or not 1 <= self.max_rank <= 37:
            raise ValueError("max_rank must be an integer in [1,37]")
        if self.max_update_norm > self.max_total_norm:
            raise ValueError("per-write cap cannot exceed total path-norm budget")
        return self


@dataclass(frozen=True)
class LocalSignals:
    cue: torch.Tensor
    preactivation: torch.Tensor
    prediction: torch.Tensor
    target: torch.Tensor
    readout: torch.Tensor
    alpha: float


class CorrectionRule(Protocol):
    name: str

    def __call__(self, signals: LocalSignals, config: WriteConfig) -> torch.Tensor: ...


class DampedJacobianDelta:
    name = "damped_jacobian_delta"

    @torch.no_grad()
    def __call__(self, signals, config):
        # Float64 solve avoids amplifying float32 error in the small regularized system.
        h = signals.cue.double()
        gain = signals.alpha * (1 - signals.preactivation.double().tanh().square())
        jacobian = signals.readout.double() * gain.unsqueeze(0)
        error = (signals.target - signals.prediction).double()
        system = jacobian @ jacobian.T + config.damping * torch.eye(
            jacobian.shape[0], dtype=torch.float64
        )
        pre_correction = jacobian.T @ torch.linalg.solve(system, error)
        delta = (
            config.learning_rate
            * torch.outer(pre_correction, h)
            / (h.square().sum() + config.key_epsilon)
        )
        return delta.to(signals.cue.dtype)
