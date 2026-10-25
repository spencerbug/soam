"""Strict, JSON-serializable experiment settings."""

import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class EnvironmentConfig:
    observation_dim: int = 12
    angles: tuple[float, ...] = (-0.18, 0.18, 0.14)
    centers: tuple[tuple[float, float], ...] = ((0.0, 0.0), (0.0, 0.0), (0.2, -0.15))
    damping: float = 0.995
    angular_action_gain: float = 0.08
    translation_action_gain: float = 0.015
    projection_seed: int = 1729


@dataclass(frozen=True)
class Config:
    name: str = "substrate"
    seeds: tuple[int, ...] = (11, 23, 47)
    models: tuple[str, ...] = ("additive", "gated", "low_rank", "separate")
    hidden_dim: int = 40
    rank: int = 4
    alpha: float = 0.7
    assimilation_gain: float = 0.5
    steps: int = 600
    batch_size: int = 48
    train_horizon: int = 24
    eval_horizon: int = 48
    stability_horizon: int = 192
    eval_sequences_per_context: int = 32
    switch_every: int = 8
    learning_rate: float = 0.003
    grounded_loss_weight: float = 0.3
    perturb_step: int = 8
    perturb_std: float = 0.15
    hidden_bound: float = 1.5
    log_every: int = 50
    threads: int = 1
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)

    def validate(self):
        if not self.seeds or len(set(self.seeds)) != len(self.seeds):
            raise ValueError("seeds must be nonempty and unique")
        if any(type(seed) is not int or seed < 0 for seed in self.seeds):
            raise ValueError("seeds must be nonnegative integers")
        if not self.models or len(set(self.models)) != len(self.models):
            raise ValueError("models must be nonempty and unique")
        if set(self.models) - {"additive", "gated", "low_rank", "separate"}:
            raise ValueError("unknown recurrent model")
        for key in (
            "hidden_dim",
            "rank",
            "steps",
            "batch_size",
            "train_horizon",
            "eval_horizon",
            "stability_horizon",
            "eval_sequences_per_context",
            "switch_every",
            "log_every",
            "threads",
        ):
            if type(getattr(self, key)) is not int or getattr(self, key) < 1:
                raise ValueError(f"{key} must be a positive integer")
        if self.hidden_dim < 2:
            raise ValueError("hidden_dim must be at least 2")
        if not 0 < self.alpha <= 1 or not 0 < self.assimilation_gain <= 1:
            raise ValueError("alpha and assimilation_gain must be in (0,1]")
        if type(self.perturb_step) is not int or not 0 <= self.perturb_step < self.eval_horizon:
            raise ValueError("perturb_step must fall within the evaluation rollout")
        if self.learning_rate <= 0 or self.grounded_loss_weight < 0:
            raise ValueError("invalid optimization settings")
        if self.perturb_std <= 0 or self.hidden_bound <= 1:
            raise ValueError("invalid perturbation/stability settings")
        e = self.environment
        if len(e.angles) < 2 or len(e.centers) != len(e.angles):
            raise ValueError("provide at least two angles and one center per context")
        if (
            type(e.observation_dim) is not int
            or e.observation_dim < 2
            or any(len(c) != 2 for c in e.centers)
        ):
            raise ValueError("invalid observation dimensions or 2D centers")
        if type(e.projection_seed) is not int or e.projection_seed < 0:
            raise ValueError("projection_seed must be a nonnegative integer")
        if not 0 < e.damping <= 1:
            raise ValueError("damping must be in (0,1]")
        numbers = [
            self.alpha,
            self.assimilation_gain,
            self.learning_rate,
            self.grounded_loss_weight,
            self.perturb_std,
            self.hidden_bound,
            e.damping,
            e.angular_action_gain,
            e.translation_action_gain,
            *e.angles,
            *(coordinate for center in e.centers for coordinate in center),
        ]
        if not all(math.isfinite(x) for x in numbers):
            raise ValueError("configuration values must be finite")
        return self

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        data = dict(data)
        env = dict(data.pop("environment", {}))
        for key in ("angles", "centers"):
            if key in env:
                env[key] = tuple(tuple(x) if isinstance(x, list) else x for x in env[key])
        for key in ("seeds", "models"):
            if key in data:
                data[key] = tuple(data[key])
        return cls(environment=EnvironmentConfig(**env), **data).validate()

    @classmethod
    def load(cls, path: str | Path):
        return cls.from_dict(json.loads(Path(path).read_text()))
