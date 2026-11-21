"""Fixed sensor and split-isolated circle streams; truth never enters inference."""

from dataclasses import dataclass

import numpy as np
import torch

from soam.encoders.projection import FixedProjection
from soam.platform.core import derived_seed

SPLITS = {"train", "development", "confirmation", "fixture"}


def seed(split, root, index, component):
    if split not in SPLITS:
        raise ValueError("unknown E0 split")
    return derived_seed("soam-e0", 1, split, root, index, component)


def sensor(theta):
    xy = torch.stack((theta.cos(), theta.sin()), -1)
    return (xy.double() @ FixedProjection(12, 1729).matrix.double().T).float()


@dataclass(frozen=True)
class Evidence:
    observed: torch.Tensor
    mask: torch.Tensor
    actions: torch.Tensor


@dataclass(frozen=True)
class Batch:
    evidence: Evidence
    target: torch.Tensor


def generate(split, root, index=0, *, batch=32, horizon=24, condition="train"):
    if condition not in {
        "train",
        "free",
        "grounded",
        "return",
        "interpolate",
        "extrapolate",
        "positive",
        "negative",
    }:
        raise ValueError("unknown E0 condition")
    rng = {
        k: np.random.default_rng(seed(split, root, index, condition + "/" + k))
        for k in ("phase", "action", "mask", "noise")
    }
    speeds = (
        [-0.12, -0.06, 0, 0.06, 0.12] if condition == "train" else [-0.18, -0.09, 0, 0.09, 0.18]
    )
    if condition == "interpolate":
        speeds = [-0.09, 0, 0.09]
    elif condition == "extrapolate":
        speeds = [-0.18, 0.18]
    elif condition in {"positive", "negative"}:
        speeds = [0.09 if condition == "positive" else -0.09]
    blocks = rng["action"].choice(speeds, ((horizon + 3) // 4, batch))
    actions = np.repeat(blocks, 4, axis=0)[:horizon]
    if condition == "train":
        actions[:, rng["action"].random(batch) < 0.25] = 0
    theta = np.concatenate((rng["phase"].uniform(-np.pi, np.pi, (1, batch)), actions)).cumsum(0)
    target = sensor(torch.from_numpy(theta))
    ranking = np.argsort(rng["mask"].random((horizon + 1, batch, 12)), axis=-1)
    mask = np.zeros_like(ranking, dtype=bool)
    np.put_along_axis(mask, ranking[..., :6], True, axis=-1)
    full = rng["mask"].random((horizon + 1, batch)) < 0.5
    mask[full] = True
    present = np.zeros((horizon + 1, batch), dtype=bool)
    present[0] = True
    if condition == "train":
        intermittent = rng["mask"].random(batch) < 0.5
        present[4::4] = intermittent
    elif condition == "grounded":
        present[:] = True
    elif condition == "return":
        present[33:] = True
    mask &= present[..., None]
    noise = torch.from_numpy(rng["noise"].normal(0, 0.01, target.shape)).float()
    mask = torch.from_numpy(mask)
    observed = torch.where(mask, target + noise, torch.zeros_like(target))
    evidence = Evidence(observed, mask, torch.from_numpy(actions[..., None]).float())
    return Batch(evidence, target), torch.from_numpy(theta)
