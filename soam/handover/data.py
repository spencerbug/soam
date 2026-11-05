"""Paired observation streams. Evaluator truth never enters learner packets."""

from dataclasses import dataclass

import numpy as np
import torch

from soam.encoders.projection import FixedProjection
from soam.handover.protocol import load_protocol, rng, templates, tensor_fingerprint


@dataclass(frozen=True)
class ObservationPacket:
    z: torch.Tensor
    valid: torch.Tensor
    cue: torch.Tensor
    cue_present: bool
    executed_action_previous: float

    def validate(self):
        for name, shape in (("z", (2, 12)), ("valid", (2,)), ("cue", (16,))):
            value = getattr(self, name)
            dtype = torch.bool if name == "valid" else torch.float32
            if value.shape != shape or value.dtype != dtype or value.device.type != "cpu":
                raise ValueError(f"invalid {name} shape/dtype/device")
            if not torch.isfinite(value).all():
                raise ValueError(f"nonfinite {name}")
        if type(self.cue_present) is not bool or not np.isfinite(self.executed_action_previous):
            raise ValueError("invalid scalar packet fields")
        if self.z[~self.valid].count_nonzero() or (
            not self.cue_present and self.cue.count_nonzero()
        ):
            raise ValueError("masked values must be zero")
        return self

    def clone(self):
        return ObservationPacket(
            self.z.clone(),
            self.valid.clone(),
            self.cue.clone(),
            self.cue_present,
            self.executed_action_previous,
        )


@dataclass(frozen=True)
class Episode:
    packets: tuple[ObservationPacket, ...]
    actions: torch.Tensor
    true_features: torch.Tensor
    phases: torch.Tensor
    requested: torch.Tensor
    presented: torch.Tensor
    seed: int
    split: str
    condition: int
    index: int

    def arrays(self):
        return {
            "z": torch.stack([p.z for p in self.packets]),
            "valid": torch.stack([p.valid for p in self.packets]),
            "cue": torch.stack([p.cue for p in self.packets]),
            "cue_present": torch.tensor([p.cue_present for p in self.packets]),
            "actions": self.actions,
            "true_features": self.true_features,
            "phases": self.phases,
            "requested": self.requested,
            "presented_training_labels": self.presented,
        }

    def fingerprint(self):
        return tensor_fingerprint(self.arrays())


def generate_episode(seed=11, split="fixture", condition=0, index=0, oracle=False):
    m = load_protocol()
    e = m["environment"]
    if condition not in range(8):
        raise ValueError("unknown condition")
    if split == "fixture" and (seed != 11 or index not in range(2)):
        raise ValueError("fixture budget: seed 11, episode indices 0 or 1")
    n = e["observations"]
    # All conditions consume exactly the same complete base innovations.
    stream = lambda component: rng(seed, split, 0, index, component)
    initial = stream("initial_phase").uniform(-np.pi, np.pi)
    actions = np.repeat(
        stream("actions").uniform(*e["action_range"], size=(n - 2) // e["action_hold"] + 1),
        e["action_hold"],
    )[: n - 1]
    process = stream("process_noise").normal(size=(n - 1, 2)) * e["process_noise_sd"]
    observation_noise = stream("observation_noise").normal(size=(n, 2, 2))
    mask_rng = stream("cue_masks")
    masks = np.zeros((n, 16))
    for t in range(n):
        masks[t, mask_rng.choice(16, m["cue"]["coordinates_retained"], replace=False)] = 1
    cue_noise = stream("cue_noise").normal(size=(n, 16))
    gains = np.array(e["gains"])
    if condition == 1:
        gains[1] = 1
        process[:, 1] = process[:, 0]
    elif condition == 7:
        gains[1] = 0.9
    phases = np.empty((n, 2))
    phases[0] = [initial, initial + np.pi / 3]
    for t in range(n - 1):
        phases[t + 1] = phases[t] + gains * actions[t] + process[t]
    phases = (phases + np.pi) % (2 * np.pi) - np.pi
    planar = np.stack((np.cos(phases), np.sin(phases)), -1)
    encoder = FixedProjection(e["projection_dim"], e["projection_seed"])
    truth = encoder(torch.tensor(planar, dtype=torch.float32))
    noise_sd = 0.1 if condition == 6 else e["observation_noise_sd"]
    observations = encoder(torch.tensor(planar + noise_sd * observation_noise, dtype=torch.float32))
    valid = torch.zeros(n, 2, dtype=torch.bool)
    for first, last, names in e["visibility"]:
        for name in names:
            valid[first : last + 1, "AB".index(name)] = True
    if condition == 5:
        for first, last in m["conditions"][5]["mask_both_intervals"]:
            valid[first : last + 1] = False
    observations[~valid] = 0
    requested = torch.zeros(n, dtype=torch.long)
    presented = torch.zeros(n, dtype=torch.long)
    cues = torch.zeros(n, 16)
    presence = torch.zeros(n, dtype=torch.bool)
    p = templates()
    pulses = []
    for onset, name in e["requests"]:
        target = "ABC".index(name)
        requested[onset:] = target
        if condition == 2 and onset:
            continue
        if condition == 3 and onset:
            target = 1 - target
        pulses.append((onset, target))
    if condition == 4:
        pulses.append((120, 2))
    for onset, target in sorted(pulses):
        presented[onset:] = target
        for t in range(onset, onset + e["cue_frames"]):
            presence[t] = True
            if oracle:
                cues[t] = p[:, target]
            else:
                mask = torch.tensor(masks[onset], dtype=torch.float32)
                noise = torch.tensor(cue_noise[t], dtype=torch.float32)
                cues[t] = mask * (p[:, target] / np.sqrt(0.5) + m["cue"]["noise_sd"] * noise)
    packets = tuple(
        ObservationPacket(
            observations[t].clone(),
            valid[t].clone(),
            cues[t].clone(),
            bool(presence[t]),
            0.0 if t == 0 else float(actions[t - 1]),
        ).validate()
        for t in range(n)
    )
    return Episode(
        packets,
        torch.tensor(actions, dtype=torch.float64),
        truth,
        torch.tensor(phases, dtype=torch.float64),
        requested,
        presented,
        seed,
        split,
        condition,
        index,
    )


def load_episode(path, seed=11, split="fixture", condition=0, index=0):
    """Restore actual archived packets, without regenerating their innovations."""
    with np.load(path, allow_pickle=False) as archive:
        arrays = {name: torch.from_numpy(archive[name].copy()) for name in archive.files}
    actions = arrays["actions"]
    if actions.shape != (191,) or arrays["z"].shape != (192, 2, 12):
        raise ValueError("invalid archived episode")
    packets = tuple(
        ObservationPacket(
            arrays["z"][t].clone(),
            arrays["valid"][t].clone(),
            arrays["cue"][t].clone(),
            bool(arrays["cue_present"][t]),
            0.0 if t == 0 else float(actions[t - 1]),
        ).validate()
        for t in range(192)
    )
    return Episode(
        packets,
        actions,
        arrays["true_features"],
        arrays["phases"],
        arrays["requested"],
        arrays["presented_training_labels"],
        seed,
        split,
        condition,
        index,
    )
