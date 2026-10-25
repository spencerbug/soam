"""Conventional bounded recurrent baselines, not a demonstrated SOAM mechanism."""

import torch
from torch import nn
from torch.nn import functional as F


class RecurrentPredictor(nn.Module):
    def __init__(
        self,
        observation_dim,
        hidden_dim,
        contexts,
        variant="additive",
        rank=4,
        alpha=0.7,
        assimilation_gain=0.5,
    ):
        super().__init__()
        if variant not in {"additive", "gated", "low_rank", "separate"}:
            raise ValueError(variant)
        self.variant, self.hidden_dim, self.contexts = variant, hidden_dim, contexts
        self.rank, self.alpha, self.assimilation_gain = rank, alpha, assimilation_gain
        self.sensory = nn.Linear(observation_dim, hidden_dim)
        self.readout = nn.Linear(hidden_dim, observation_dim)
        if variant == "separate":
            # Independent transition weights; shared sensory interface aligns active coordinates.
            self.cores = nn.ModuleList(
                nn.Linear(hidden_dim + 3, hidden_dim) for _ in range(contexts)
            )
        else:
            self.recurrent = nn.Linear(hidden_dim, hidden_dim)
            self.action = nn.Linear(3, hidden_dim, bias=False)
            self.context = nn.Embedding(contexts, hidden_dim)
            if variant == "gated":
                self.gate = nn.Embedding(contexts, hidden_dim)
                nn.init.zeros_(self.gate.weight)
            if variant == "low_rank":
                self.down = nn.Linear(hidden_dim, rank, bias=False)
                self.up = nn.Linear(rank, hidden_dim, bias=False)
                self.modulation = nn.Embedding(contexts, rank)

    def initialize(self, observation):
        return torch.tanh(self.sensory(observation))

    def assimilate(self, predicted_hidden, observation, context):
        # Context enters transition, not this initial sensory correction baseline.
        return (
            1 - self.assimilation_gain
        ) * predicted_hidden + self.assimilation_gain * self.initialize(observation)

    def decode(self, hidden):
        return self.readout(hidden)

    def step(self, hidden, action, context):
        if self.variant == "separate":
            inputs = torch.cat((hidden, action), dim=-1)
            # Dispatch only active examples to their context-specific core.
            pre = torch.zeros_like(hidden)
            for i, core in enumerate(self.cores):
                select = context == i
                pre[select] = core(inputs[select])
        else:
            recurrent_input = hidden
            if self.variant == "gated":
                recurrent_input = hidden * (2 * torch.sigmoid(self.gate(context)))
            pre = self.recurrent(recurrent_input) + self.action(action) + self.context(context)
            if self.variant == "low_rank":
                pre = pre + self.up(self.down(hidden) * self.modulation(context))
        return (1 - self.alpha) * hidden + self.alpha * torch.tanh(pre)

    def rollout(self, observation, actions, contexts, *, observations=None, perturb=None):
        """Open loop by default; observations opt into grounded correction.

        Perturb is (state index, additive noise); perturbing index k happens before
        transition k. No implicit state, reset at switches, or parameter updates.
        """
        hidden = self.initialize(observation)
        predicted, states = [], [hidden]
        for t in range(actions.shape[1]):
            if observations is not None and t > 0:
                hidden = self.assimilate(hidden, observations[:, t], contexts[:, t])
            if perturb is not None and t == perturb[0]:
                hidden = hidden + perturb[1]
            hidden = self.step(hidden, actions[:, t], contexts[:, t])
            predicted.append(self.decode(hidden))
            states.append(hidden)
        return torch.stack(predicted, dim=1), torch.stack(states, dim=1)


def parameter_count(model):
    return sum(p.numel() for p in model.parameters())


def parameter_bytes(model):
    return sum(p.numel() * p.element_size() for p in model.parameters())


def build_model(config, variant):
    env = config.environment
    args = {
        "observation_dim": env.observation_dim,
        "contexts": len(env.angles),
        "rank": config.rank,
        "alpha": config.alpha,
        "assimilation_gain": config.assimilation_gain,
    }
    width = config.hidden_dim
    if variant == "separate":
        # Analytic counts avoid consuming RNG while selecting the matched width.
        obs, n = env.observation_dim, len(env.angles)
        target = width * width + (2 * obs + n + 5) * width + obs
        candidates = range(2, width + 1)
        width = min(candidates, key=lambda h: abs(n * h * (h + 4) + 2 * obs * h + h + obs - target))
    return RecurrentPredictor(hidden_dim=width, variant=variant, **args)


def training_loss(model, batch, grounded_weight):
    free, _ = model.rollout(batch.observations[:, 0], batch.actions, batch.contexts)
    grounded, _ = model.rollout(
        batch.observations[:, 0], batch.actions, batch.contexts, observations=batch.observations
    )
    target = batch.observations[:, 1:]
    return (
        F.mse_loss(free, target)
        + grounded_weight * F.mse_loss(grounded, target)
        + 0.1
        * F.mse_loss(
            model.decode(model.initialize(batch.observations[:, 0])), batch.observations[:, 0]
        )
    )
