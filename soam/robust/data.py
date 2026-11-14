"""Evaluator-owned paired B2 streams; no truth in the Evidence interface."""

import numpy as np
import torch

from soam.encoders.projection import FixedProjection
from soam.platform.core import derived_seed
from soam.temporal.data import Episode, Evidence
from soam.temporal.data import generate as original
from soam.temporal.data import training_data as old_training

EXTENSIONS = (
    "isolated",
    "channels",
    "coherent",
    "sustained",
    "dynamics",
    "heavy",
    "biased",
    "ambiguous",
)
SENSED = ("every1", "every2", "every4", "every8", "irregular")
INTERMITTENT = SENSED[1:]
CORRUPTION = ("corrupt", "isolated", "channels", "coherent", "sustained", "heavy", "biased")


def seed(split, root, index=0, component="base"):
    return derived_seed("soam-study-b2", 1, split, root, index, component)


def training_data(root, **kwargs):
    split = kwargs.get("split", "train")
    return old_training(seed(split, root), **kwargs)


def generate(split, root, index=0, *, batch=20, horizon=64, condition="partial", schedule="every4"):
    mapped = seed(split, root)
    base = original(
        split,
        mapped,
        index,
        batch=batch,
        horizon=horizon,
        condition="partial" if condition in EXTENSIONS else condition,
        schedule=schedule,
    )
    if condition not in EXTENSIONS:
        return base
    ev = base.evidence
    z, target = ev.observed.clone(), base.target.clone()
    rng = np.random.default_rng(seed(split, root, index, "b2-corruption"))
    start, end = 3 * horizon // 8, horizon // 2
    present = ev.mask.any(-1).numpy()
    first = np.full(batch, horizon + 1)
    for j in range(batch):
        indices = np.flatnonzero(present[start:, j])
        if len(indices):
            first[j] = start + indices[0]
    changed = original(
        split, mapped, index, batch=batch, horizon=horizon, condition="change", schedule=schedule
    )
    if condition in {"coherent", "sustained", "ambiguous"}:
        if condition == "ambiguous":
            # Exactly the genuine-change evidence, but unchanged hidden world.
            return Episode(changed.evidence, base.target, condition, schedule)
        for j in range(batch):
            times = [first[j]] if condition == "coherent" else range(start, 5 * horizon // 8)
            for t in times:
                if t <= horizon:
                    z[t, j] = changed.evidence.observed[t, j]
    elif condition == "isolated":
        noise = torch.tensor(rng.normal(0, 0.5, (batch, 12)), dtype=z.dtype)
        for j, t in enumerate(first):
            if t <= horizon:
                z[t, j] += noise[j]
    elif condition == "channels":
        for t in range(start, end):
            for j in range(batch):
                valid = ev.mask[t, j].nonzero().flatten().numpy()
                if len(valid):
                    idx = rng.choice(valid, min(2, len(valid)), replace=False)
                    z[t, j, idx] += torch.tensor(rng.normal(0, 0.5, len(idx)), dtype=z.dtype)
    elif condition == "heavy":
        z[1:] = target[1:] + torch.tensor(rng.standard_t(3, z[1:].shape) * 0.05, dtype=z.dtype)
    elif condition == "biased":
        bias = rng.normal(0, 0.1, (batch, 12))
        error = rng.normal(0, 0.1, (3 * horizon // 4 - start, batch, 1)) + bias
        z[start : 3 * horizon // 4] += torch.tensor(error, dtype=z.dtype)
    elif condition == "dynamics":
        # Simulator geometry is evaluator-only. Fitted filters never see this inverse.
        projection = FixedProjection(12, 1729).matrix.double()
        x = (target[start - 1].double() @ projection).numpy()
        for t in range(start - 1, horizon):
            a = ev.actions[t].double().numpy()
            angle = 0.60 * a[:, 0]
            c, s = np.cos(angle), np.sin(angle)
            moved = (
                0.995 * np.stack((c * x[:, 0] - s * x[:, 1], s * x[:, 0] + c * x[:, 1]), -1)
                + 0.06 * a[:, 1:]
            )
            x = np.where(ev.roles[t, :, 1:].numpy().astype(bool), moved, x)
            target[t + 1] = (torch.tensor(x) @ projection.T).float()
        z += target - base.target
    z = torch.where(ev.mask, z, 0)
    return Episode(
        Evidence(z, ev.mask, ev.actions, ev.roles, ev.noise_sd), target, condition, schedule
    )


def normalization():
    x = generate("normalization", 15007, batch=2048, horizon=1).target[0].double()
    return (x - x.mean(0)).square().mean().clamp_min(1e-6).item()
