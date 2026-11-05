"""Explicit state, isolated prediction and observable resource accounting."""

import copy
import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Protocol

import numpy as np
import torch
from torch import Tensor, nn


def derived_seed(protocol, version, split, root, episode, component):
    if any(type(x) is not int or x < 0 for x in (version, root, episode)):
        raise ValueError("nonnegative integer stream indices required")
    if any(not isinstance(x, str) or not x for x in (protocol, split, component)):
        raise ValueError("explicit stream names required")
    key = [protocol, version, split, root, episode, component]
    raw = json.dumps(key, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    return int.from_bytes(hashlib.sha256(raw.encode()).digest()[:8], "big")


def fingerprint(tensors):
    digest = hashlib.sha256()
    for name, value in sorted(tensors.items()):
        a = value.detach().cpu().contiguous()
        digest.update(json.dumps([name, str(a.dtype), list(a.shape)]).encode())
        digest.update(a.numpy().tobytes())
    return digest.hexdigest()


def storage(tensors):
    logical = 0
    unique = {}
    for tensor in tensors:
        logical += tensor.numel() * tensor.element_size()
        store = tensor.untyped_storage()
        unique[(str(tensor.device), store.data_ptr())] = store.nbytes()
    return {"logical_bytes": logical, "unique_storage_bytes": sum(unique.values())}


def tensor_check(value, shape, dtype=torch.float32):
    if not isinstance(value, Tensor) or value.device.type != "cpu":
        raise ValueError("CPU tensor required")
    if tuple(value.shape) != tuple(shape) or value.dtype != dtype:
        raise ValueError("invalid tensor shape/dtype")
    if not torch.isfinite(value).all():
        raise FloatingPointError("nonfinite tensor")


@dataclass(frozen=True)
class Observation:
    z: Tensor
    valid: Tensor
    cue: Tensor
    cue_valid: Tensor

    def validate(self, batch, features, cues):
        tensor_check(self.z, (batch, features))
        tensor_check(self.valid, (batch, features), torch.bool)
        tensor_check(self.cue, (batch, cues))
        tensor_check(self.cue_valid, (batch, cues), torch.bool)
        if self.z[~self.valid].count_nonzero() or self.cue[~self.cue_valid].count_nonzero():
            raise ValueError("masked coordinates must be zero")
        return self

    def clone(self):
        return Observation(
            *(x.detach().clone() for x in (self.z, self.valid, self.cue, self.cue_valid))
        )


@dataclass(frozen=True)
class Command:
    action: Tensor

    def clone(self):
        return Command(self.action.detach().clone())


class Dynamics(Protocol):
    def initial_state(self, batch_size: int) -> Tensor: ...
    def assimilate(self, state: Tensor, observation: Observation) -> Tensor: ...
    def advance(self, state: Tensor, command: Command, *, clamp_units=None) -> Tensor: ...
    def readout(self, state: Tensor) -> Tensor: ...


@dataclass(frozen=True)
class ModelSpec:
    features: int
    actions: int
    width: int = 8
    kind: str = "leaky"

    def validate(self):
        if any(type(v) is not int or v < 1 for v in (self.features, self.actions, self.width)):
            raise ValueError("positive model dimensions required")
        if self.kind not in ("leaky", "linear"):
            raise ValueError("unsupported fixture backend")
        return self


class SuppliedDynamics(nn.Module):
    """A tiny numeric backend with no task, target, geometry or learned parameter."""

    def __init__(self, spec, seed):
        super().__init__()
        self.spec = spec.validate()
        rng = np.random.Generator(np.random.PCG64(seed))
        n, d, a = spec.width, spec.features, spec.actions
        for name, shape, scale in (
            ("recurrent", (n, n), 0.2 / np.sqrt(n)),
            ("sensory", (n, d), 1 / np.sqrt(d)),
            ("action", (n, a), 0.1 / np.sqrt(a)),
            ("decoder", (d, n), 1 / np.sqrt(n)),
        ):
            self.register_buffer(
                name, torch.tensor(rng.normal(0, scale, shape), dtype=torch.float32)
            )
        self.register_buffer("bias", torch.zeros(n, dtype=torch.float32))

    def initial_state(self, batch_size):
        if type(batch_size) is not int or batch_size < 1:
            raise ValueError("positive batch size required")
        return torch.zeros(batch_size, self.spec.width, dtype=torch.float32)

    def check_state(self, state):
        tensor_check(state, (state.shape[0], self.spec.width))

    def assimilate(self, state, observation):
        self.check_state(state)
        observation.validate(state.shape[0], self.spec.features, 0)
        projected = observation.z @ self.sensory.T
        return 0.5 * state + 0.5 * torch.tanh(projected)

    def advance(self, state, command, *, clamp_units=None):
        self.check_state(state)
        tensor_check(command.action, (state.shape[0], self.spec.actions))
        pre = state @ self.recurrent.T + command.action @ self.action.T + self.bias
        tensor_check(pre, state.shape)
        out = 0.5 * state + 0.5 * torch.tanh(pre) if self.spec.kind == "leaky" else pre
        if clamp_units is not None:
            tensor_check(clamp_units, (self.spec.width,), torch.bool)
            out = out.masked_fill(clamp_units.unsqueeze(0), 0)
        tensor_check(out, state.shape)
        return out

    def readout(self, state):
        self.check_state(state)
        out = state @ self.decoder.T
        tensor_check(out, (state.shape[0], self.spec.features))
        return out


BACKENDS = {name: (lambda spec, seed: SuppliedDynamics(spec, seed)) for name in ("leaky", "linear")}


def model_fingerprint(model):
    return hashlib.sha256(
        (json.dumps(asdict(model.spec), sort_keys=True) + fingerprint(model.state_dict())).encode()
    ).hexdigest()


@dataclass(frozen=True)
class PredictionSnapshot:
    _model: SuppliedDynamics
    _state: Tensor


@dataclass(frozen=True)
class Intervention:
    kind: str
    units: tuple[int, ...] = ()
    amplitude: float = 0.0
    seed: int = 0

    def validate(self, width):
        if self.kind not in ("state_clamp", "state_perturb"):
            raise ValueError("unsupported intervention capability")
        if type(self.seed) is not int or self.seed < 0:
            raise ValueError("invalid intervention seed")
        if self.kind == "state_clamp":
            if not self.units or len(set(self.units)) != len(self.units) or self.amplitude != 0:
                raise ValueError("invalid clamp fields")
            if any(type(i) is not int or i < 0 or i >= width for i in self.units):
                raise ValueError("invalid clamp unit")
        elif self.units or not np.isfinite(self.amplitude) or self.amplitude <= 0:
            raise ValueError("invalid perturbation fields")
        return self


@dataclass(frozen=True)
class PredictionTrace:
    features: Tensor
    states: Tensor
    work: dict


def freeze(model, state):
    model.check_state(state)
    cloned = copy.deepcopy(model).eval().requires_grad_(False)
    return PredictionSnapshot(cloned, state.detach().clone())


def predict(snapshot, commands, intervention=None):
    """All modifications are private, including when a backend raises or misbehaves."""
    if not commands:
        raise ValueError("nonempty finite command schedule required")
    model = copy.deepcopy(snapshot._model)
    before = model_fingerprint(model)
    state = snapshot._state.detach().clone()
    if intervention:
        intervention.validate(model.spec.width)
    clamp = None
    if intervention and intervention.kind == "state_clamp":
        clamp = torch.zeros(model.spec.width, dtype=torch.bool)
        clamp[list(intervention.units)] = True
        state = state.masked_fill(clamp.unsqueeze(0), 0)
    elif intervention:
        rng = np.random.Generator(np.random.PCG64(intervention.seed))
        delta = torch.tensor(rng.normal(size=tuple(state.shape)), dtype=torch.float32)
        delta = delta / delta.square().mean(1, keepdim=True).sqrt()
        state = state + intervention.amplitude * delta
    features, states = [], []
    try:
        with torch.no_grad():
            for command in commands:
                old = fingerprint({"state": state, "action": command.action})
                # Do not lend the caller's command storage to a backend.
                state_in, command_in = state.clone(), command.clone()
                inputs = fingerprint({"state": state_in, "action": command_in.action})
                state = model.advance(state_in, command_in, clamp_units=clamp)
                if fingerprint({"state": state_in, "action": command_in.action}) != inputs:
                    raise RuntimeError("backend mutated prediction inputs")
                if fingerprint({"state": state_in, "action": command.action}) != old:
                    raise RuntimeError("prediction input corruption")
                state_before_readout = fingerprint({"state": state})
                output = model.readout(state)
                if fingerprint({"state": state}) != state_before_readout:
                    raise RuntimeError("readout mutated prediction state")
                tensor_check(output, (state.shape[0], model.spec.features))
                states.append(state.detach().clone())
                features.append(output.detach().clone())
    finally:
        if model_fingerprint(model) != before:
            raise RuntimeError("persistent write during prediction")
    n, d, a, h, b = (
        model.spec.width,
        model.spec.features,
        model.spec.actions,
        len(commands),
        state.shape[0],
    )
    return PredictionTrace(
        torch.stack(features),
        torch.stack(states),
        {
            "advance_calls": h,
            "readout_calls": h,
            "assimilation_calls": 0,
            "linear_macs": b * h * (n * n + n * a + d * n),
            "tanh_elements": b * h * n if model.spec.kind == "leaky" else 0,
            "state_input_copies": h,
            "command_copies": h,
            "prediction_initial_state_copies": 1,
            "prediction_model_copies": 1,
            "trajectory_state_copies": h,
            "trajectory_feature_copies": h,
        },
    )
