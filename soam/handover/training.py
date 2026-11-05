"""Observed-data-only fitting primitives. SOAM-034 does not run measured fits."""

import resource
import sys
import time
from dataclasses import dataclass

import torch
from torch import nn

from soam.handover.data import generate_episode
from soam.handover.protocol import load_protocol, rng


@dataclass(frozen=True)
class ObservedBatch:
    z: torch.Tensor
    valid: torch.Tensor
    cue: torch.Tensor
    cue_present: torch.Tensor
    actions: torch.Tensor
    supplied_gains: torch.Tensor
    presented_labels: torch.Tensor


def observed_batch(episodes):
    """Explicit training adapter; phases, noiseless features and ideal focus are excluded."""
    return ObservedBatch(
        z=torch.stack([torch.stack([p.z for p in e.packets]) for e in episodes]),
        valid=torch.stack([torch.stack([p.valid for p in e.packets]) for e in episodes]),
        cue=torch.stack([torch.stack([p.cue for p in e.packets]) for e in episodes]),
        cue_present=torch.tensor([[p.cue_present for p in e.packets] for e in episodes]),
        actions=torch.stack([e.actions for e in episodes]).float(),
        supplied_gains=torch.tensor([[1.0, 1.0 if e.condition == 1 else 0.7] for e in episodes]),
        presented_labels=torch.stack([e.presented for e in episodes]),
    )


def selector_loss(model, batch):
    size, frames = batch.z.shape[:2]
    hidden, weights = torch.zeros(size, 16), torch.full((size, 3), 1 / 3)
    losses = []
    for t in range(frames):
        priming = weights @ model.coupling.T @ model.patterns.T
        inputs = torch.cat((batch.cue[:, t], priming, batch.cue_present[:, t, None].float()), -1)
        hidden = model.selector(inputs, hidden)
        logits = model.selector_readout(hidden)
        weights = torch.softmax(logits, -1)
        losses.append(nn.functional.cross_entropy(logits, batch.presented_labels[:, t]))
    return torch.stack(losses).mean()


def pose_loss(model, batch):
    size, frames = batch.z.shape[:2]
    separate = model.variant == "G2"
    hidden = torch.zeros(size * 2 if separate else size, model.pose_cell.hidden_size)

    def advance(state, z, valid, action):
        if separate:
            inputs = torch.cat(
                (
                    z * valid[..., None],
                    valid[..., None].float(),
                    action[:, None, None].expand(-1, 2, 1),
                    batch.supplied_gains[..., None],
                ),
                -1,
            ).reshape(size * 2, 15)
        else:
            inputs = torch.cat(
                (
                    (z * valid[..., None]).flatten(1),
                    valid.float(),
                    action[:, None],
                    batch.supplied_gains,
                ),
                -1,
            )
        return model.pose_cell(inputs, state)

    current_sum = torch.zeros(())
    next_sum = torch.zeros(())
    for t in range(frames):
        past_action = torch.zeros(size) if t == 0 else batch.actions[:, t - 1]
        hidden = advance(hidden, batch.z[:, t], batch.valid[:, t], past_action)
        prediction = model.pose_readout(hidden).reshape(size, 2, 12)
        current_sum = (
            current_sum + ((prediction - batch.z[:, t]).square() * batch.valid[:, t, :, None]).sum()
        )
        if t + 1 < frames:
            predicted_hidden = advance(
                hidden,
                torch.zeros_like(batch.z[:, t]),
                torch.zeros_like(batch.valid[:, t]),
                batch.actions[:, t],
            )
            prediction = model.pose_readout(predicted_hidden).reshape(size, 2, 12)
            next_sum = (
                next_sum
                + ((prediction - batch.z[:, t + 1]).square() * batch.valid[:, t + 1, :, None]).sum()
            )
    return current_sum / (12 * batch.valid.sum()).clamp_min(1) + next_sum / (
        12 * batch.valid[:, 1:].sum()
    ).clamp_min(1)


def learned_state(model, component=None):
    prefixes = (
        ("selector",)
        if component == "selector"
        else ("pose_",)
        if component == "pose"
        else ("selector", "pose_")
    )
    return {
        name: p.detach().clone()
        for name, p in model.named_parameters()
        if name.startswith(prefixes)
    }


@torch.no_grad()
def load_learned(model, state, component=None):
    expected = learned_state(model, component)
    if set(state) != set(expected):
        raise ValueError("checkpoint parameter names differ")
    parameters = dict(model.named_parameters())
    for name, value in state.items():
        if value.shape != expected[name].shape or not torch.isfinite(value).all():
            raise ValueError("invalid checkpoint tensor")
    for name, value in state.items():
        parameters[name].copy_(value)


def fit_component(model, component, seed, checkpoint_callback=None):
    """Run one fixed-budget fit when SOAM-035 is executed; preserve partial state on failure.

    Callback receives losses/exposure and completion status at checkpoints. Only training
    streams are generated here. Selector is fitted once per seed and copied to all G layouts.
    """
    if component not in ("selector", "pose") or model.analytic:
        raise ValueError("select a GRU component")
    if seed != model.seed:
        raise ValueError("model and fitting seed differ")
    protocol = load_protocol()
    if seed not in protocol["rng"]["seeds"]:
        raise ValueError("fitting seed is not preregistered")
    m = protocol["training"]
    names = learned_state(model, component)
    parameters = [p for name, p in model.named_parameters() if name in names]
    optimizer = torch.optim.Adam(parameters, lr=m["learning_rate"], weight_decay=m["weight_decay"])
    order = rng(seed, "train", 0, 0, "training_order")
    loss_function = selector_loss if component == "selector" else pose_loss
    history, seen, status = [], set(), "running"
    attempted_steps, generated_presentations = 0, 0

    def progress():
        return {
            "seed": seed,
            "split": "train",
            "component": component,
            "completed_steps": len(history),
            "attempted_steps": attempted_steps,
            "generated_episode_presentations": generated_presentations,
            "unique_derived_episode_ids": sorted(seen),
            "losses": list(history),
        }

    def check_budget():
        if time.monotonic() - started >= m["max_seconds_per_fit"]:
            raise TimeoutError("fixed fit budget exhausted")
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak_bytes = peak if sys.platform == "darwin" else peak * 1024
        if peak_bytes > protocol["evaluation"]["max_process_rss_gib"] * 1024**3:
            raise MemoryError("fixed fit RSS budget exhausted")

    started = time.monotonic()
    try:
        for step in range(m["steps_per_fit"]):
            check_budget()
            attempted_steps += 1
            indices = order.integers(m["episodes_generated_per_seed"], size=m["batch_episodes"])
            episodes = []
            for i in indices:
                episodes.append(generate_episode(seed, "train", int(i % 8), int(i // 8)))
                seen.add(int(i))
                generated_presentations += 1
            batch = observed_batch(episodes)
            optimizer.zero_grad(set_to_none=True)
            loss = loss_function(model, batch)
            if not torch.isfinite(loss):
                raise FloatingPointError("nonfinite training loss")
            loss.backward()
            nn.utils.clip_grad_norm_(parameters, m["gradient_norm_cap"], error_if_nonfinite=True)
            optimizer.step()
            history.append({"step": step + 1, "loss": float(loss.detach())})
            if checkpoint_callback and (step + 1) % 50 == 0:
                checkpoint_callback(learned_state(model, component), progress(), "running")
        check_budget()
        status = "complete"
    except Exception:
        status = "failed"
        raise
    finally:
        if checkpoint_callback:
            checkpoint_callback(learned_state(model, component), progress(), status)
    presentations = len(history) * m["batch_episodes"]
    if component == "selector":
        forward_macs = presentations * 192 * (9 + 48 + 3 * 16 * (33 + 16) + 16 * 3)
    else:
        hidden, inputs, outputs = (
            model.pose_cell.hidden_size,
            model.pose_cell.input_size,
            model.pose_readout.out_features,
        )
        instances = 2 if model.variant == "G2" else 1
        forward_macs = (
            presentations
            * instances
            * (192 + 191)
            * (3 * hidden * (inputs + hidden) + hidden * outputs)
        )
    return {
        "component": component,
        "exposure": progress(),
        "steps": len(history),
        "losses": history,
        "unique_derived_episodes": len(seen),
        "unique_base_streams": len({i // 8 for i in seen}),
        "episode_presentations": len(history) * m["batch_episodes"],
        "transitions_presented": len(history) * m["batch_episodes"] * 191,
        "forward_linear_macs": forward_macs,
        "estimated_backward_linear_macs": 2 * forward_macs,
        "compute_note": "Backward is a rough 2x-forward linear-MAC estimate; nonlinearities, "
        "optimizer/vector operations and dispatch excluded. Use measured runtime as well.",
        "seconds": time.monotonic() - started,
        "optimizer_tensor_bytes": sum(
            v.numel() * v.element_size()
            for state in optimizer.state.values()
            for v in state.values()
            if isinstance(v, torch.Tensor)
        ),
    }
