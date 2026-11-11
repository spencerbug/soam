"""Fresh paired E1 streams. Truth belongs to the training/evaluation layer only."""

import hashlib
from dataclasses import dataclass

import numpy as np
import torch

from soam.encoders.projection import FixedProjection
from soam.platform.core import derived_seed

SCHEDULES = ("every1", "every2", "every4", "every8", "irregular", "initial")
CONDITIONS = (
    "clean",
    "partial",
    "missing",
    "noise",
    "corrupt",
    "contradict",
    "change",
    "motion",
    "gap",
)
SPLITS = {"fixture", "train", "development", "confirmation", "normalization"}


def seed(split, root, index, component):
    if split not in SPLITS:
        raise ValueError("Unknown Study B split")
    return derived_seed("soam-study-b", 1, split, root, index, component)


@dataclass(frozen=True)
class Evidence:
    observed: torch.Tensor
    mask: torch.Tensor
    actions: torch.Tensor
    roles: torch.Tensor
    noise_sd: torch.Tensor


@dataclass(frozen=True)
class Episode:
    evidence: Evidence
    target: torch.Tensor
    condition: str
    schedule: str


def generate(split, root, index=0, *, batch=20, horizon=64, condition="partial", schedule="every4"):
    if condition not in CONDITIONS or schedule not in SCHEDULES:
        raise ValueError("Unknown condition/schedule")
    rng = {
        k: np.random.default_rng(seed(split, root, index, k))
        for k in ("initial", "actions", "mask", "noise", "corruption", "schedule", "dropout")
    }
    parity = 0 if split in {"train", "fixture", "normalization"} else 1
    r = rng["initial"].uniform(0.4, 0.8, batch)
    phi = (
        rng["initial"].choice(np.arange(parity, 8, 2), batch) + rng["initial"].uniform(size=batch)
    ) * (2 * np.pi / 8)
    x = r[:, None] * np.stack((np.cos(phi), np.sin(phi)), -1)
    pairs = np.array([(i, j) for i in range(4) for j in range(4) if (i + j) % 2 == parity])
    chosen = pairs[rng["actions"].integers(len(pairs), size=(horizon, batch))]
    a = rng["actions"].uniform(-1, 1, (horizon, batch, 3)).astype(np.float32)
    a[..., :2] = -1 + 0.5 * (chosen + rng["actions"].uniform(size=(horizon, batch, 2)))
    upper = (-1 + 0.5 * (chosen + 1)).astype(np.float32)
    a[..., :2] = np.minimum(a[..., :2], np.nextafter(upper, np.float32(-np.inf)))
    role = (np.arange(horizon)[:, None] // 8 + np.arange(batch)[None, :] % 2) % 2
    q = np.eye(2, dtype=np.float32)[role]
    a[role == 0] = 0
    event_start, event_end = 3 * horizon // 8, horizon // 2
    if condition == "motion":
        a[event_start : 5 * horizon // 8] *= -2
    world = [x.copy()]
    for t in range(horizon):
        angle = 0.30 * a[t, :, 0].astype(np.float64)
        c, s = np.cos(angle), np.sin(angle)
        moved = (
            0.98 * np.stack((c * x[:, 0] - s * x[:, 1], s * x[:, 0] + c * x[:, 1]), -1)
            + 0.03 * a[t, :, 1:]
        )
        x = np.where(role[t, :, None] == 1, moved, x)
        if condition == "change" and t + 1 == event_start:
            x = -x
        world.append(x.copy())
    target = (
        torch.from_numpy(np.stack(world)) @ FixedProjection(12, 1729).matrix.double().T
    ).float()
    shape = (horizon + 1, batch, 12)
    potential = np.zeros(shape, dtype=bool)
    count = 12 if condition == "clean" else 6
    order = np.argsort(rng["mask"].uniform(size=shape), axis=-1)[..., :count]
    np.put_along_axis(potential, order, True, axis=-1)
    scheduled = np.zeros((horizon + 1, batch), dtype=bool)
    scheduled[0] = True
    if schedule.startswith("every"):
        scheduled[:: int(schedule[5:])] = True
    elif schedule == "irregular":
        for b in range(batch):
            t = 0
            while t <= horizon:
                scheduled[t, b] = True
                t += int(rng["schedule"].integers(1, 9))
    if condition == "missing":
        scheduled[1:] &= rng["dropout"].uniform(size=(horizon, batch)) >= 0.25
    if condition == "gap":
        scheduled[horizon // 4 + 1 : 3 * horizon // 4 + 1] = False
    sd = 0.1 if condition == "noise" else 0.01
    z = target.numpy().copy() + rng["noise"].normal(0, sd, shape).astype(np.float32)
    if condition == "corrupt":
        z[event_start:event_end] += (
            rng["corruption"]
            .normal(0, 0.5, (event_end - event_start, batch, 12))
            .astype(np.float32)
        )
    elif condition == "contradict":
        z[event_start:event_end] -= 2 * target.numpy()[event_start:event_end]
    mask = potential & scheduled[..., None]
    z[~mask] = 0
    ev = Evidence(
        torch.from_numpy(z),
        torch.from_numpy(mask),
        torch.from_numpy(a),
        torch.from_numpy(q),
        torch.full((horizon + 1, batch, 1), sd),
    )
    return Episode(ev, target, condition, schedule)


def training_data(root, updates=1200, batch=8, horizon=16, split="train"):
    return [
        generate(
            split,
            root,
            i,
            batch=batch,
            horizon=horizon,
            condition=CONDITIONS[(i // 6) % 9],
            schedule=SCHEDULES[i % 6],
        )
        for i in range(updates)
    ]


def input_hash(data):
    h = hashlib.sha256()
    for b in data:
        for t in (*vars(b.evidence).values(), b.target):
            h.update(str((t.dtype, tuple(t.shape))).encode())
            h.update(t.contiguous().numpy().tobytes())
    return h.hexdigest()


def normalization():
    x = generate("normalization", 10909, batch=2048, horizon=1).target[0].double()
    return (x - x.mean(0)).square().mean().clamp_min(1e-6).item()
