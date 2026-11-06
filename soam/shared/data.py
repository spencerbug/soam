"""E1 data ownership: observed records for fitting, world states for auditing only."""

import hashlib
from dataclasses import dataclass

import numpy as np
import torch

from soam.encoders.projection import FixedProjection
from soam.platform.core import Command, Observation, derived_seed, fingerprint
from soam.platform.tasks import Episode, EvaluationTargets
from soam.shared.models import manifest

PROTOCOL = "soam-e1-shared"
VERSION = 1
ROLES = ("recall", "transition")
TRAIN_SPLITS = ("train", "fixture/train")
EVAL_SPLITS = ("development", "confirmation", "development_diagnostic", "fixture/evaluation")


def stream(split, root, index, component):
    return derived_seed(PROTOCOL, VERSION, split, root, index, component)


def initialization_seed(split, root, family, config_index):
    if config_index not in (0, 1) or family not in {r["id"] for r in manifest()["models"]}:
        raise ValueError("unknown frozen family/configuration")
    return stream(split, root, 0, f"fit-initialization/{family}/{config_index}")


@dataclass(frozen=True)
class ObservedBatch:
    """Contains sensor records, never projection, world state or generator access."""

    initial: Observation
    clean: torch.Tensor  # [time including initial, batch, feature], float32
    actions: torch.Tensor  # [transition, batch, action], float32
    role: str

    def later_observation(self, time):
        if not 1 <= time < len(self.clean):
            raise ValueError("only subsequent clean records can correct state")
        z = self.clean[time].clone()
        return Observation(
            z,
            torch.ones_like(z, dtype=torch.bool),
            torch.zeros(len(z), 2, dtype=torch.float32),
            torch.zeros(len(z), 2, dtype=torch.bool),
        )


def observed_batch(episodes, role):
    """Copy only observation channels; evaluator targets cannot enter the learner."""
    if role not in ROLES or not episodes:
        raise ValueError("nonempty single-role episode collection required")
    initial = Observation(
        *(
            torch.cat([getattr(e.observations[0], field) for e in episodes])
            for field in ("z", "valid", "cue", "cue_valid")
        )
    )
    expected = torch.tensor([1, 0] if role == "recall" else [0, 1], dtype=torch.float32)
    if not torch.equal(initial.cue, expected.expand(len(episodes), -1)):
        raise ValueError("batch role does not match supplied cue")
    # Clean initial records belong to the training archive, separate from cues.
    clean = torch.cat([e.clean_records for e in episodes], dim=1)
    actions = torch.stack([torch.cat([c.action for c in e.commands]) for e in episodes], 1)
    return ObservedBatch(initial, clean, actions, role)


@dataclass(frozen=True)
class RecordedEpisode(Episode):
    clean_records: torch.Tensor


class SharedTask:
    """Simulator and clean-record archive. Never passed to a model or loss."""

    def __init__(self):
        self.protocol = manifest()
        self.projection = FixedProjection(12, 1729).matrix.detach().clone()
        expected = "c0ad772cb34d7a2ee8971c9108772f70478b79a818970759c9526ad64e05805c"
        if hashlib.sha256(self.projection.numpy().tobytes()).hexdigest() != expected:
            raise ValueError("fixed sensory projection changed")

    def episode(self, split, root, index, role, *, component=None):
        if split not in TRAIN_SPLITS + EVAL_SPLITS or role not in ROLES:
            raise ValueError("unknown split/role")
        parity = 0 if split in TRAIN_SPLITS else 1
        horizon = 10 if role == "recall" else (8 if parity == 0 else 32)
        prefix = component or role
        names = ("radius", "phase", "action", "mask", "noise")
        seeds = {name: stream(split, root, index, f"{prefix}/{name}") for name in names}
        rng = {name: np.random.Generator(np.random.PCG64(seed)) for name, seed in seeds.items()}
        radius = rng["radius"].uniform(0.4, 0.8)
        sector = rng["phase"].choice(np.arange(parity, 8, 2))
        phase = (sector + rng["phase"].uniform()) * (2 * np.pi / 8)
        x = radius * np.array([np.cos(phase), np.sin(phase)], dtype=np.float64)
        actions = np.zeros((horizon, 3), dtype=np.float32)
        if role == "transition":
            pairs = np.array([(i, j) for i in range(4) for j in range(4) if (i + j) % 2 == parity])
            for t in range(horizon):
                pair = pairs[rng["action"].integers(len(pairs))]
                actions[t, :2] = -1 + 0.5 * (pair + rng["action"].uniform(size=2))
                actions[t, 2] = rng["action"].uniform(-1, 1)
                # Float32 rounding must not place a command in a neighboring cell.
                for j in range(2):
                    upper = np.float32(-1 + 0.5 * (pair[j] + 1))
                    if pair[j] < 3 and actions[t, j] >= upper:
                        actions[t, j] = np.nextafter(upper, np.float32(-np.inf))
        world = [x.copy()]
        for a in actions.astype(np.float64):
            if role == "transition":
                c, s = np.cos(0.30 * a[0]), np.sin(0.30 * a[0])
                x = 0.98 * (np.array([[c, -s], [s, c]]) @ x) + 0.03 * a[1:]
            world.append(x.copy())
        world = torch.from_numpy(np.array(world))
        z = (world @ self.projection.double().T).float().unsqueeze(1)
        valid = torch.zeros(1, 12, dtype=torch.bool)
        valid[0, rng["mask"].choice(12, 6, replace=False)] = True
        cue_z = z[0].clone()
        noise = torch.from_numpy(rng["noise"].normal(0, 0.01, 6)).float()
        cue_z[valid] += noise
        cue_z[~valid] = 0
        cue = torch.tensor([[1, 0] if role == "recall" else [0, 1]], dtype=torch.float32)
        first = Observation(cue_z, valid, cue, torch.ones(1, 2, dtype=torch.bool))
        observations = (first,) + tuple(
            Observation(
                v.clone(),
                torch.ones_like(v, dtype=torch.bool),
                torch.zeros(1, 2, dtype=torch.float32),
                torch.zeros(1, 2, dtype=torch.bool),
            )
            for v in z[1:]
        )
        record = {
            name: {
                "key": [PROTOCOL, VERSION, split, root, index, f"{prefix}/{name}"],
                "seed": seeds[name],
            }
            for name in names
        }
        return RecordedEpisode(
            observations,
            tuple(Command(torch.from_numpy(a).unsqueeze(0).clone()) for a in actions),
            EvaluationTargets(z.clone(), world),
            record,
            z.clone(),
        )

    def training_batch(self, root, update, role, *, fixture=False, batch_size=16):
        if type(update) is not int or not 0 <= update < 400:
            raise ValueError("training update outside frozen inventory")
        if role == "transition" and update < 100:
            raise ValueError("transition exposure begins at update 100")
        if batch_size != 16 and not (fixture and type(batch_size) is int and 1 <= batch_size <= 16):
            raise ValueError("study batch size is frozen at 16")
        split = "fixture/train" if fixture else "train"
        episodes = tuple(
            self.episode(split, root, update * 16 + i, role) for i in range(batch_size)
        )
        return observed_batch(episodes, role), episodes

    def normalization(self):
        samples = torch.cat(
            [
                self.episode("train", 1801, i, "recall", component="normalization").clean_records[0]
                for i in range(2048)
            ]
        )
        mean = samples.double().mean(0)
        variance = (samples.double() - mean).square().mean().clamp_min(1e-6)
        return {
            "samples": samples,
            "mean": mean,
            "variance": variance,
            "sha256": fingerprint({"samples": samples}),
            "stream_key_template": [
                PROTOCOL,
                VERSION,
                "train",
                1801,
                "index=0..2047",
                "normalization/{radius,phase,action,mask,noise}",
            ],
        }
