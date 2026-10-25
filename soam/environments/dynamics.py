"""Deterministic action-conditioned regimes with independent RNG streams.

Ground-truth states belong to the environment/evaluator only, never the predictor.
"""

from dataclasses import dataclass

import numpy as np
import torch

from soam.config import EnvironmentConfig
from soam.encoders.projection import FixedProjection

SPLIT_IDS = {"train": 0, "dev": 1, "test": 2, "stability": 3}


@dataclass
class SequenceBatch:
    observations: torch.Tensor  # [batch, time+1, feature]
    actions: torch.Tensor  # [batch, time, 3]
    contexts: torch.Tensor  # [batch, time], known controls, not inferred labels
    states: torch.Tensor  # diagnostic ground truth only


class Dynamics:
    def __init__(self, config: EnvironmentConfig, seed: int, split: str):
        self.config = config
        self.rng = np.random.default_rng(np.random.SeedSequence([seed, SPLIT_IDS[split]]))
        self.encoder = FixedProjection(config.observation_dim, config.projection_seed)
        self.n_contexts = len(config.angles)

    def transition(self, states, actions, contexts):
        cfg = self.config
        centers = np.asarray(cfg.centers)[contexts]
        theta = np.asarray(cfg.angles)[contexts] + cfg.angular_action_gain * actions[..., 0]
        delta = states - centers
        rotated = np.stack(
            (
                np.cos(theta) * delta[..., 0] - np.sin(theta) * delta[..., 1],
                np.sin(theta) * delta[..., 0] + np.cos(theta) * delta[..., 1],
            ),
            -1,
        )
        return centers + cfg.damping * rotated + cfg.translation_action_gain * actions[..., 1:]

    def sample(self, batch_size, horizon, switch_every=None, balanced=False):
        if batch_size < 1 or horizon < 1 or (switch_every is not None and switch_every < 1):
            raise ValueError("batch_size, horizon and switch_every must be positive")
        rng = self.rng
        phase = rng.uniform(-np.pi, np.pi, batch_size)
        radius = rng.uniform(0.25, 0.8, batch_size)
        states = np.empty((batch_size, horizon + 1, 2), np.float32)
        states[:, 0] = radius[:, None] * np.stack((np.cos(phase), np.sin(phase)), -1)
        actions = rng.uniform(-1, 1, (batch_size, horizon, 3)).astype(np.float32)
        start = (
            np.arange(batch_size) % self.n_contexts
            if balanced
            else rng.integers(self.n_contexts, size=batch_size)
        )
        offsets = np.arange(horizon) // switch_every if switch_every else np.zeros(horizon, int)
        contexts = (start[:, None] + offsets) % self.n_contexts
        for t in range(horizon):
            states[:, t + 1] = self.transition(states[:, t], actions[:, t], contexts[:, t])
        state_tensor = torch.from_numpy(states)
        return SequenceBatch(
            self.encoder(state_tensor),
            torch.from_numpy(actions),
            torch.from_numpy(contexts),
            state_tensor,
        )
