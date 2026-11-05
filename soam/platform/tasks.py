"""Two tiny task adapters. Physical state and targets stay outside dynamics."""

from dataclasses import dataclass

import numpy as np
import torch

from soam.encoders.projection import FixedProjection
from soam.platform.core import Command, Observation, derived_seed, tensor_check

PROTOCOL = "soam-platform-fixture"
VERSION = 1


def seed_for(root, index, component, split="fixture"):
    return derived_seed(PROTOCOL, VERSION, split, root, index, component)


@dataclass(frozen=True)
class EvaluationTargets:
    features: torch.Tensor
    world: torch.Tensor


@dataclass(frozen=True)
class Episode:
    observations: tuple[Observation, ...]
    commands: tuple[Command, ...]
    targets: EvaluationTargets
    stream_seeds: dict

    def observed_arrays(self):
        return {
            "z": torch.stack([o.z for o in self.observations]),
            "valid": torch.stack([o.valid for o in self.observations]),
            "cue": torch.stack([o.cue for o in self.observations]),
            "cue_valid": torch.stack([o.cue_valid for o in self.observations]),
            "actions": torch.stack([c.action for c in self.commands]),
        }


class FixtureTask:
    def __init__(self, name, features, actions):
        self.name, self.features, self.actions = name, features, actions
        self.encoder = FixedProjection(features, 1729)

    def transition(self, x, action):
        raise NotImplementedError

    def episode(self, split, seed, index):
        if split != "fixture" or seed != 9001 or index not in (0, 1):
            raise ValueError("fixture-only task: seed 9001, indices 0/1")
        seeds = {
            c: seed_for(seed, index, self.name + "/" + c, split) for c in ("initial", "actions")
        }
        x = np.random.Generator(np.random.PCG64(seeds["initial"])).uniform(-0.5, 0.5, 2)
        commands = (
            np.random.Generator(np.random.PCG64(seeds["actions"]))
            .uniform(-0.1, 0.1, (3, self.actions))
            .astype(np.float32)
        )
        world = [x.copy()]
        for command in commands:
            x = self.transition(x, command.astype(np.float64))
            world.append(x.copy())
        world = torch.tensor(np.array(world), dtype=torch.float32)
        z = self.encoder(world).unsqueeze(1)
        observations = tuple(
            Observation(
                v.clone(),
                torch.ones_like(v, dtype=torch.bool),
                torch.empty(1, 0),
                torch.empty(1, 0, dtype=torch.bool),
            )
            for v in z
        )
        return Episode(
            observations,
            tuple(Command(torch.tensor(a).unsqueeze(0)) for a in commands),
            EvaluationTargets(z.clone(), world),
            seeds,
        )

    def score(self, predictions, targets):
        tensor_check(predictions, targets.features.shape)
        tensor_check(targets.features, predictions.shape)
        errors = (predictions.double() - targets.features.double()).square().mean((1, 2))
        return [
            {
                "metric": "feature_mse",
                "units": "squared_feature",
                "horizon": t + 1,
                "value": value,
                "sample_count": predictions.shape[1],
                "status": "valid",
            }
            for t, value in enumerate(errors.tolist())
        ]


class RotationTask(FixtureTask):
    def __init__(self):
        super().__init__("rotation", 12, 3)

    def transition(self, x, action):
        c, s = np.cos(action[0]), np.sin(action[0])
        return np.array([[c, -s], [s, c]]) @ x + action[1:]


class TranslationTask(FixtureTask):
    def __init__(self):
        super().__init__("translation", 8, 1)

    def transition(self, x, action):
        return x + np.array([action[0], 0])


TASKS = {"rotation": RotationTask, "translation": TranslationTask}
