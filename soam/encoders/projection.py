"""Frozen sensory features; inverse projection is diagnostic only."""

import numpy as np
import torch
from torch import nn


class FixedProjection(nn.Module):
    def __init__(self, observation_dim: int, seed: int):
        super().__init__()
        if observation_dim < 2:
            raise ValueError("observation_dim must be >= 2")
        q, _ = np.linalg.qr(np.random.default_rng(seed).normal(size=(observation_dim, 2)))
        self.register_buffer("matrix", torch.tensor(q, dtype=torch.float32))

    def forward(self, observation):
        return observation @ self.matrix.T

    def diagnostic_inverse(self, features):
        return features @ self.matrix
