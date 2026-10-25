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
        if variant not in {"additive", "gated", "low_rank", "separate", "gru"}:
            raise ValueError(variant)
        self.variant, self.hidden_dim, self.contexts = variant, hidden_dim, contexts
        self.observation_dim = observation_dim
        self.rank, self.alpha, self.assimilation_gain = rank, alpha, assimilation_gain
        self.sensory = nn.Linear(observation_dim, hidden_dim)
        self.readout = nn.Linear(hidden_dim, observation_dim)
        if variant == "gru":
            self.cell = nn.GRUCell(3 + contexts, hidden_dim)
        elif variant == "separate":
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

    def initialize(self, observation, context=None):
        return torch.tanh(self.sensory(observation))

    def assimilate(self, predicted_hidden, observation, context):
        # Context enters transition, not this initial sensory correction baseline.
        return (
            1 - self.assimilation_gain
        ) * predicted_hidden + self.assimilation_gain * self.initialize(observation)

    def decode(self, hidden, context=None):
        return self.readout(hidden)

    def step(self, hidden, action, context):
        if self.variant == "gru":
            inputs = torch.cat((action, F.one_hot(context, self.contexts).to(action.dtype)), -1)
            return self.cell(inputs, hidden)
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


class IndependentPredictor(nn.Module):
    """Disjoint per-context sensory, transition, and readout parameters.

    Switches bridge through predicted features, not unrelated hidden coordinates.
    Only grounded rollouts can assimilate an observed current feature.
    """

    def __init__(self, observation_dim, hidden_dim, contexts, alpha, assimilation_gain, **kwargs):
        super().__init__()
        self.variant, self.hidden_dim, self.contexts = "independent", hidden_dim, contexts
        self.observation_dim = observation_dim
        self.alpha, self.assimilation_gain = alpha, assimilation_gain
        self.sensories = nn.ModuleList(
            nn.Linear(observation_dim, hidden_dim) for _ in range(contexts)
        )
        self.readouts = nn.ModuleList(
            nn.Linear(hidden_dim, observation_dim) for _ in range(contexts)
        )
        self.cores = nn.ModuleList(nn.Linear(hidden_dim + 3, hidden_dim) for _ in range(contexts))

    @staticmethod
    def dispatch(layers, value, context):
        result = value.new_zeros((value.shape[0], layers[0].out_features))
        for i, layer in enumerate(layers):
            select = context == i
            result[select] = layer(value[select])
        return result

    def initialize(self, observation, context):
        return torch.tanh(self.dispatch(self.sensories, observation, context))

    def decode(self, hidden, context):
        return self.dispatch(self.readouts, hidden, context)

    def assimilate(self, hidden, observation, context):
        return (1 - self.assimilation_gain) * hidden + self.assimilation_gain * self.initialize(
            observation, context
        )

    def step(self, hidden, action, context):
        pre = self.dispatch(self.cores, torch.cat((hidden, action), -1), context)
        return (1 - self.alpha) * hidden + self.alpha * torch.tanh(pre)

    def rollout(self, observation, actions, contexts, *, observations=None, perturb=None):
        hidden = self.initialize(observation, contexts[:, 0])
        predicted, states = [], [hidden]
        for t in range(actions.shape[1]):
            if t > 0:
                switch = contexts[:, t] != contexts[:, t - 1]
                # Bridge only switched rows, using the previous prediction even in training.
                if switch.any():
                    bridge = self.initialize(predicted[-1][switch], contexts[switch, t])
                    hidden = hidden.clone()
                    hidden[switch] = bridge
                if observations is not None:
                    hidden = self.assimilate(hidden, observations[:, t], contexts[:, t])
            # Perturb after handoff, in the new active predictor's coordinates.
            if perturb is not None and t == perturb[0]:
                hidden = hidden + perturb[1]
            hidden = self.step(hidden, actions[:, t], contexts[:, t])
            predicted.append(self.decode(hidden, contexts[:, t]))
            states.append(hidden)
        return torch.stack(predicted, 1), torch.stack(states, 1)


def analytic_parameter_count(h, d, n, variant, rank):
    shared = h * h + (2 * d + n + 5) * h + d
    if variant == "additive":
        return shared
    if variant == "gated":
        return shared + n * h
    if variant == "low_rank":
        return shared + 2 * h * rank + n * rank
    if variant == "separate":
        return n * h * (h + 4) + 2 * d * h + h + d
    if variant == "gru":
        return 3 * h * h + (3 * (3 + n) + 7 + 2 * d) * h + d
    if variant == "independent":
        return n * (h * h + (2 * d + 5) * h + d)
    raise ValueError(variant)


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
    target = analytic_parameter_count(
        width, env.observation_dim, len(env.angles), "additive", config.rank
    )
    if config.match_budgets or variant == "separate":
        width = min(
            range(2, config.hidden_dim + 1),
            key=lambda h: abs(
                analytic_parameter_count(
                    h, env.observation_dim, len(env.angles), variant, config.rank
                )
                - target
            ),
        )
    cls = IndependentPredictor if variant == "independent" else RecurrentPredictor
    if variant != "independent":
        args["variant"] = variant
    model = cls(hidden_dim=width, **args)
    if (
        config.match_budgets
        and abs(parameter_count(model) - target) / target > config.parameter_tolerance
    ):
        raise ValueError(f"{variant} cannot meet parameter tolerance at selected width {width}")
    return model


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
            model.decode(
                model.initialize(batch.observations[:, 0], batch.contexts[:, 0]),
                batch.contexts[:, 0],
            ),
            batch.observations[:, 0],
        )
    )
