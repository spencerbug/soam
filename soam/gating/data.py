"""Paired fresh E1-family streams; world coordinates remain evaluator-owned."""

from dataclasses import dataclass

import numpy as np
import torch

from soam.encoders.projection import FixedProjection
from soam.platform.core import derived_seed

PROTOCOL = "soam-study-a"
VERSION = 1
SPLITS = {
    "train",
    "development",
    "confirmation",
    "fixture",
    "probe_train",
    "diagnostic",
    "normalization",
}


def seed(split, root, index, component):
    if split not in SPLITS:
        raise ValueError("unknown Study A split")
    return derived_seed(PROTOCOL, VERSION, split, root, index, component)


@dataclass(frozen=True)
class Batch:
    z: torch.Tensor
    valid: torch.Tensor
    clean: torch.Tensor
    actions: torch.Tensor
    roles: torch.Tensor  # [time,batch,2]

    def inputs(self):
        # Free inference receives no clean targets or evaluator state.
        return self.z, self.valid, self.actions, self.roles


def generate(split, root, index, role, *, batch=16, horizon=None):
    if role not in ("recall", "transition", "switch"):
        raise ValueError("unknown role")
    horizon = (10 if role == "recall" else 32) if horizon is None else horizon
    parity = 0 if split in ("train", "fixture", "normalization") else 1
    rng = {
        k: np.random.Generator(np.random.PCG64(seed(split, root, index, f"{role}/{k}")))
        for k in ("radius", "phase", "action", "mask", "noise")
    }
    radius = rng["radius"].uniform(0.4, 0.8, batch)
    sector = rng["phase"].choice(np.arange(parity, 8, 2), batch)
    phase = (sector + rng["phase"].uniform(size=batch)) * (2 * np.pi / 8)
    x = radius[:, None] * np.stack((np.cos(phase), np.sin(phase)), -1)
    actions = np.zeros((horizon, batch, 3), dtype=np.float32)
    roles = np.zeros((horizon, batch, 2), dtype=np.float32)
    roles[..., 0 if role == "recall" else 1] = 1
    if role == "switch":
        roles[:] = 0
        for t in range(horizon):
            roles[t, :, (t // 8) % 2] = 1
    if role != "recall":
        pairs = np.array([(i, j) for i in range(4) for j in range(4) if (i + j) % 2 == parity])
        choices = pairs[rng["action"].integers(len(pairs), size=(horizon, batch))]
        actions[..., :2] = -1 + 0.5 * (choices + rng["action"].uniform(size=(horizon, batch, 2)))
        upper = (-1 + 0.5 * (choices + 1)).astype(np.float32)
        actions[..., :2] = np.minimum(actions[..., :2], np.nextafter(upper, np.float32(-np.inf)))
        actions[..., 2] = rng["action"].uniform(-1, 1, (horizon, batch))
        actions[roles[..., 0].astype(bool)] = 0
    world = [x.copy()]
    for t, a in enumerate(actions.astype(np.float64)):
        c, s = np.cos(0.30 * a[:, 0]), np.sin(0.30 * a[:, 0])
        moved = (
            0.98 * np.stack((c * x[:, 0] - s * x[:, 1], s * x[:, 0] + c * x[:, 1]), -1)
            + 0.03 * a[:, 1:]
        )
        x = np.where(roles[t, :, 1:2].astype(bool), moved, x)
        world.append(x.copy())
    world = torch.from_numpy(np.stack(world))
    projection = FixedProjection(12, 1729).matrix.double()
    clean = (world @ projection.T).float()
    valid = np.zeros((batch, 12), dtype=bool)
    selected = np.argsort(rng["mask"].uniform(size=(batch, 12)), axis=1)[:, :6]
    valid[np.arange(batch)[:, None], selected] = True
    valid = torch.from_numpy(valid)
    z = clean[0].clone()
    z += torch.from_numpy(rng["noise"].normal(0, 0.01, z.shape)).float()
    z[~valid] = 0
    return Batch(z, valid, clean, torch.from_numpy(actions), torch.from_numpy(roles)), world


def training_data(root, *, fixture=False, recall_updates=100, joint_updates=700, batch=16):
    split = "fixture" if fixture else "train"
    recall, transition = [], []
    for i in range(recall_updates + joint_updates):
        recall.append(generate(split, root, i, "recall", batch=batch, horizon=10)[0])
        if i >= recall_updates:
            transition.append(generate(split, root, i, "transition", batch=batch, horizon=8)[0])
    return {"recall": recall, "transition": transition}


def normalization(root=8801, count=2048):
    b, _ = generate("normalization", root, 0, "recall", batch=count, horizon=1)
    values = b.clean[0].double()
    mean = values.mean(0)
    return {
        "variance": (values - mean).square().mean().clamp_min(1e-6).item(),
        "mean": mean,
        "samples": b.clean[0],
    }
