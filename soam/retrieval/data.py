"""Fresh D-R1 streams; evaluator-only objects and paired full/partial cues."""

import hashlib

import numpy as np
import torch

from soam.acquisition.data import DTYPE, Cue, Record


def rng(*parts):
    key = "/".join(map(str, ("soam-study-d-r1-v1", *parts))).encode()
    return np.random.default_rng(int.from_bytes(hashlib.sha256(key).digest()[:8], "little"))


def tensor(x):
    return torch.as_tensor(np.array(x, copy=True), dtype=DTYPE)


def projection():
    return np.linalg.qr(np.random.default_rng(1729).normal(size=(8, 2)))[0]


def rotate(v, q):
    c, s = np.cos(q), np.sin(q)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])


def objects(root, split, family, count):
    r = rng(root, split, "family", family)
    prototype = r.normal(size=16)
    out = []
    for _ in range(count):
        k = prototype + 0.5 * r.normal(size=16)
        k *= 4 / np.linalg.norm(k)
        out.append((k, r.uniform(-1, 1, size=2)))
    return out


def records(obj, root, split, identity, count=8):
    k, v = obj
    r = rng(root, split, "acquisition", identity)
    out = []
    for _ in range(count):
        q = float(r.uniform(-0.4, 0.4))
        y = projection() @ rotate(v, q) + r.normal(0, 0.02, size=8)
        out.append(Record(tensor(k), tensor(y), q))
    return out


def queries(obj, root, split, identity, count=8):
    k, v = obj
    r = rng(root, split, "queries", identity)
    masks = np.zeros((count, 16), dtype=bool)
    for mask in masks:
        mask[r.choice(16, size=8, replace=False)] = True
    noisy = k + r.normal(0, 0.02, size=(count, 16))
    keys = np.where(masks, noisy, 0)
    actions = r.uniform(-0.6, 0.6, size=(count, 8))
    truth = np.stack(
        [np.stack([projection() @ rotate(v, q) for q in np.r_[0, np.cumsum(a)]]) for a in actions]
    )
    cues = {
        "full": Cue(tensor(noisy), torch.ones(count, 16, dtype=torch.bool)),
        "partial": Cue(tensor(keys), torch.as_tensor(masks)),
    }
    return cues, tensor(actions), truth


def training(root):
    r = rng(root, "train", "transitions")
    xs, ys, angles = [], [], []
    for family in range(8):
        for _, v in objects(root, "train", family, 8):
            for _ in range(32):
                q, a = r.uniform(-np.pi, np.pi, size=2)
                xs.append(projection() @ rotate(v, q))
                ys.append(projection() @ rotate(v, q + a))
                angles.append(a)
    return tensor(xs), tensor(angles), tensor(ys)


def core_probes(root):
    r = rng(root, "old-core", "probes")
    v = r.uniform(-1, 1, size=(64, 2))
    actions = r.uniform(-0.6, 0.6, size=(64, 8))
    truth = np.stack(
        [
            np.stack([projection() @ rotate(z, q) for q in np.r_[0, np.cumsum(a)]])
            for z, a in zip(v, actions, strict=True)
        ]
    )
    return tensor(truth[:, 0]), tensor(actions), truth
