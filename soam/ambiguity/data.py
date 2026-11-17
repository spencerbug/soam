"""Evaluator-owned worlds; inference receives only the immutable Evidence fields."""

import hashlib
from dataclasses import dataclass

import numpy as np
import torch

from soam.encoders.projection import FixedProjection
from soam.platform.core import derived_seed

PRIMARY = ("later", "ambiguous", "uninformative", "diagnostic", "misleading", "delayed")
SECONDARY = ("sensor", "change", "coherent", "unknown")
TRAIN = PRIMARY + ("sensor", "change")


def seed(split, root, index=0, component="base"):
    if split not in {"train", "development", "confirmation", "fixture", "normalization"}:
        raise ValueError("unknown split")
    return derived_seed("soam-study-c", 1, split, root, index, component)


@dataclass(frozen=True)
class Evidence:
    observed: torch.Tensor
    mask: torch.Tensor
    actions: torch.Tensor


@dataclass(frozen=True)
class Episode:
    evidence: Evidence
    target: torch.Tensor
    labels: torch.Tensor
    world: torch.Tensor
    pairs: torch.Tensor
    condition: str


def generate(split, root, index=0, *, pairs=16, horizon=48, condition="later"):
    if condition not in PRIMARY + SECONDARY:
        raise ValueError("unknown condition")
    rng = {
        k: np.random.default_rng(seed(split, root, index, k))
        for k in ("initial", "action", "mask", "noise", "corrupt", "order")
    }
    x0 = np.stack(
        (
            rng["initial"].uniform(-0.5, 0.5, pairs),
            rng["initial"].uniform(0.4, 0.8, pairs) * rng["initial"].choice([-1, 1], pairs),
        ),
        -1,
    )
    x0 = np.repeat(x0, 2, axis=0)
    signs = np.tile([-1.0, 1.0], pairs)
    a = rng["action"].uniform(-1, 1, (horizon, pairs, 3))
    a[..., 0] = 0
    if condition not in {"ambiguous", "uninformative"}:
        a[11:, :, 0] = 1
    if condition == "diagnostic":
        a[15:, :, 0] = 0
    if condition == "uninformative":
        a[..., 1:] *= 2
    a = np.repeat(a, 2, axis=1)

    def path(changed=False, unknown=False):
        x, values, labels = x0.copy(), [x0.copy()], [signs.copy()]
        for t in range(horizon):
            k = -signs if changed and t + 1 >= 24 else signs
            k = np.full_like(k, 2) if unknown and t + 1 >= 24 else k
            nxt = 0.98 * x + 0.03 * a[t, :, 1:]
            nxt[:, 0] += 0.08 * k * a[t, :, 0] * x[:, 1]
            x = nxt
            values.append(x.copy())
            labels.append(k.copy())
        return np.stack(values), np.stack(labels)

    world, labels = path(changed=condition == "change", unknown=condition == "unknown")
    projection = FixedProjection(12, 1729).matrix.double().numpy()
    target = (world @ projection.T).astype(np.float32)
    sensed = target.copy()
    if condition == "coherent":
        sensed = (path(changed=True)[0] @ projection.T).astype(np.float32)
    if condition == "misleading":
        sensed[12:20] = (
            sensed[12:20].reshape(-1, pairs, 2, 12)[:, :, ::-1].reshape(-1, 2 * pairs, 12)
        )
    noise = rng["noise"].normal(0, 0.01, (horizon + 1, pairs, 12)).astype(np.float32)
    observed = sensed + np.repeat(noise, 2, axis=1)
    mask = np.zeros((horizon + 1, pairs, 12), dtype=bool)
    order = rng["mask"].random(mask.shape).argsort(-1)[..., :6]
    np.put_along_axis(mask, order, True, axis=-1)
    period = 2 if condition in {"uninformative", "diagnostic"} else 4
    mask[np.arange(horizon + 1) % period != 0] = False
    mask[0] = True
    if condition == "delayed":
        mask[12:28] = False
    mask = np.repeat(mask, 2, axis=1)
    if condition == "sensor":
        observed[24:32] += np.repeat(
            rng["corrupt"].normal(0, 0.3, observed[24:32, ::2].shape).astype(np.float32), 2, axis=1
        )
    observed = np.where(mask, observed, 0)
    perm = rng["order"].permutation(2 * pairs)
    inverse = np.argsort(perm).reshape(pairs, 2)
    return Episode(
        Evidence(
            torch.tensor(observed[:, perm]),
            torch.tensor(mask[:, perm]),
            torch.tensor(a[:, perm], dtype=torch.float32),
        ),
        torch.tensor(target[:, perm]),
        torch.tensor((labels[:, perm] + 1) / 2),
        torch.tensor(world[:, perm]),
        torch.tensor(inverse),
        condition,
    )


def training_data(root, updates=1200, *, split="train", horizon=48):
    return [
        generate(split, root, i, pairs=4, horizon=horizon, condition=TRAIN[i % len(TRAIN)])
        for i in range(updates)
    ]


def input_hash(batch):
    h = hashlib.sha256()
    for x in (
        batch.evidence.observed,
        batch.evidence.mask,
        batch.evidence.actions,
        batch.target,
        batch.labels,
    ):
        h.update(str(x.dtype).encode())
        h.update(x.contiguous().numpy().tobytes())
    return h.hexdigest()


def normalization():
    z = generate("normalization", 26017, pairs=1024, horizon=1).target[0].double()
    return (z - z.mean(0)).square().mean().clamp_min(1e-6).item()
