"""Identical prefix data and optimizer counts; extend only stationary episodes."""

import hashlib
import time

import numpy as np
import torch

from soam.navigation.engine import fit as original_fit
from soam.navigation.engine import rollout, training_batches
from soam.navigation.models import learning_rate
from soam.platform.core import derived_seed


def mapped_root(root):
    return derived_seed("soam-e0-hold", 1, "root-map", root, 0, "streams")


def eligible(batch):
    stationary = (batch.evidence.actions == 0).all(dim=(0, 2))
    values = batch.target[:, stationary]
    if not torch.equal(values, values[-1:].expand_as(values)):
        raise AssertionError("Stationary prefix targets must be constant")
    return stationary


def objective(model, batch, horizon, check=lambda: None):
    evidence, target = batch.evidence, batch.target
    prefix = len(evidence.actions)
    if horizon < prefix:
        raise ValueError("hold horizon cannot shorten the original prefix")
    stationary = eligible(batch)
    h = model.initialize(evidence.observed[0], evidence.mask[0])
    posterior = 12 * (model.readout(h) - target[0]).square().mean(-1)
    prior = torch.zeros_like(posterior)
    for t, action in enumerate(evidence.actions):
        h = model.predict(h, action)
        prior = prior + 12 * (model.readout(h) - target[t + 1]).square().mean(-1)
        h = model.correct(h, evidence.observed[t + 1], evidence.mask[t + 1])
        posterior = posterior + 12 * (model.readout(h) - target[t + 1]).square().mean(-1)
    short_loss = prior / prefix + 0.5 * posterior / (prefix + 1)
    if horizon == prefix or not stationary.any():
        return short_loss.mean()
    h = h[stationary]
    fixed_target = target[-1, stationary]
    zeros = torch.zeros(len(h), 1, dtype=h.dtype, device=h.device)
    tail = torch.zeros(len(h), dtype=h.dtype, device=h.device)
    for _ in range(horizon - prefix):
        check()
        h = model.predict(h, zeros)
        # No cue/correction and no new target or simulator access in this tail.
        tail = tail + 12 * (model.readout(h) - fixed_target).square().mean(-1)
    long_loss = (prior[stationary] + tail) / horizon
    long_loss = long_loss + 0.5 * (posterior[stationary] + tail) / (horizon + 1)
    return (short_loss[~stationary].sum() + long_loss.sum()) / len(stationary)


def state_hash(model):
    digest = hashlib.sha256()
    for key, value in sorted(model.state_dict().items()):
        digest.update(key.encode())
        digest.update(value.detach().numpy().tobytes())
    return digest.hexdigest()


def fit(model, root, config, arm, check=lambda: None, *, fixture=False):
    if arm not in {"SHORT24", "LONG128", "REFERENCE"}:
        raise ValueError("unknown E0-HOLD arm")
    count = config["updates"] * config["batch"]
    exposure = {
        "distinct_prefix_sequences": count,
        "distinct_prefix_sensory_snapshots": count * (config["train_horizon"] + 1),
        "extra_observations": 0,
        "prefix_transition_examples": count * config["train_horizon"],
        "extra_stationary_transition_examples": 0,
        "eligible_stationary_episodes": 0,
        "training_data_passes": 2 if model.name == "PCA2" else 1,
        "optimizer_updates": 0 if model.name == "PCA2" else config["updates"],
    }
    if model.name == "PCA2":
        if arm != "REFERENCE":
            raise ValueError("PCA2 is a single reference, not a training-horizon treatment")
        result = original_fit(model, root, config, None, check, fixture=fixture)
        return {**result, "exposure": exposure}
    if arm == "REFERENCE":
        raise ValueError("neural families require a horizon arm")
    start_cpu, start_wall = time.process_time(), time.monotonic()
    hasher = hashlib.sha256()
    model.train()
    opt = torch.optim.Adam(model.parameters(), lr=config["rate"])
    trace, step_times = [], []
    for i, batch in enumerate(training_batches(root, config, fixture=fixture, hasher=hasher)):
        check()
        step_start = time.process_time()
        lr = learning_rate(config["rate"], i, config["updates"])
        for group in opt.param_groups:
            group["lr"] = lr
        opt.zero_grad(set_to_none=True)
        stationary_count = int(eligible(batch).sum())
        exposure["eligible_stationary_episodes"] += stationary_count
        if arm == "SHORT24":
            # Exactly the historical fitting objective and reduction order.
            path = rollout(model, batch.evidence)
            loss = 12 * (
                (path["prior"] - batch.target[1:]).square().mean()
                + 0.5 * (path["posterior"] - batch.target).square().mean()
            )
        else:
            loss = objective(model, batch, config["long_horizon"], check)
            exposure["extra_stationary_transition_examples"] += stationary_count * (
                config["long_horizon"] - config["train_horizon"]
            )
        if not torch.isfinite(loss):
            raise FloatingPointError("nonfinite E0-HOLD loss")
        loss.backward()
        grad = torch.nn.utils.clip_grad_norm_(model.parameters(), 1, error_if_nonfinite=True)
        opt.step()
        trace.append([i + 1, loss.item(), grad.item(), lr])
        step_times.append(time.process_time() - step_start)
    model.eval()
    if any(not t.isfinite().all() for t in model.state_dict().values()):
        raise FloatingPointError("nonfinite E0-HOLD checkpoint")
    return {
        "trace": trace,
        "cpu_seconds": time.process_time() - start_cpu,
        "wall_seconds": time.monotonic() - start_wall,
        "steady_update_cpu_seconds": float(np.mean(step_times[2:] or step_times)),
        "training_data_sha256": hasher.hexdigest(),
        "exposure": exposure,
    }
