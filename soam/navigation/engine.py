"""Offline fitting and causal evaluation for the frozen E0 pilot."""

import hashlib
import time

import numpy as np
import torch

from soam.encoders.projection import FixedProjection
from soam.navigation.data import generate, seed, sensor
from soam.navigation.models import learning_rate


def rollout(model, evidence, check=lambda: None):
    """No targets or simulator state accepted; every action advances exactly once."""
    h = model.initialize(evidence.observed[0], evidence.mask[0])
    posterior, prior = [model.readout(h)], []
    for t, a in enumerate(evidence.actions):
        check()
        h = model.predict(h, a)
        prior.append(model.readout(h))
        h = model.correct(h, evidence.observed[t + 1], evidence.mask[t + 1])
        posterior.append(model.readout(h))
    return {"prior": torch.stack(prior), "posterior": torch.stack(posterior)}


def training_batches(root, config, *, fixture=False, hasher=None):
    for i in range(config["updates"]):
        batch = generate(
            "fixture" if fixture else "train",
            root,
            i,
            batch=config["batch"],
            horizon=config["train_horizon"],
            condition="train",
        )[0]
        if hasher is not None:
            for tensor in (
                batch.target,
                batch.evidence.observed,
                batch.evidence.mask,
                batch.evidence.actions,
            ):
                hasher.update(tensor.numpy().tobytes())
        yield batch


@torch.no_grad()
def fit_pca(model, root, config, check, *, fixture=False, hasher=None):
    # Streaming sufficient statistics avoid keeping the entire training corpus in memory.
    total = 0
    sx, sxx = torch.zeros(12, dtype=torch.float64), torch.zeros(12, 12, dtype=torch.float64)
    for b in training_batches(root, config, fixture=fixture, hasher=hasher):
        check()
        x = b.target.reshape(-1, 12).double()
        sx += x.sum(0)
        sxx += x.T @ x
        total += len(x)
    mean = sx / total
    _, vectors = torch.linalg.eigh(sxx / total - torch.outer(mean, mean))
    p = vectors[:, -2:]
    for j in range(2):
        if p[p[:, j].abs().argmax(), j] < 0:
            p[:, j] *= -1
    xx = torch.zeros(6, 6, dtype=torch.float64)
    xy = torch.zeros(6, 2, dtype=torch.float64)
    yy = torch.zeros(2, 2, dtype=torch.float64)
    count = 0
    for b in training_batches(root, config, fixture=fixture):
        check()
        old = (b.target[:-1].reshape(-1, 12).double() - mean) @ p
        new = (b.target[1:].reshape(-1, 12).double() - mean) @ p
        a = b.evidence.actions.reshape(-1, 1).double()
        x = torch.cat([old * a**power for power in (1, 2, 3)], -1)
        y = new - old
        xx += x.T @ x
        xy += x.T @ y
        yy += y.T @ y
        count += len(x)
    beta = torch.linalg.solve(xx / count + config["ridge"] * torch.eye(6), xy / count)
    residual = (yy - xy.T @ beta - beta.T @ xy + beta.T @ xx @ beta) / count
    values, vectors = torch.linalg.eigh(0.5 * (residual + residual.T))
    process = (vectors * values.clamp_min(0)) @ vectors.T + 1e-6 * torch.eye(2)
    for name, value in {"mean": mean, "P": p, "B": beta.T, "process": process}.items():
        getattr(model, name).copy_(value.float())
    return []


def fit(model, root, config, rate, check=lambda: None, *, fixture=False):
    start = time.process_time()
    wall_start = time.monotonic()
    hasher = hashlib.sha256()
    model.train()
    trace, update_cpu = [], []
    if model.name == "PCA2":
        fit_pca(model, root, config, check, fixture=fixture, hasher=hasher)
    else:
        opt = torch.optim.Adam(model.parameters(), lr=rate)
        for i, b in enumerate(training_batches(root, config, fixture=fixture, hasher=hasher)):
            step_start = time.process_time()
            check()
            lr = learning_rate(rate, i, config["updates"])
            for group in opt.param_groups:
                group["lr"] = lr
            opt.zero_grad(set_to_none=True)
            path = rollout(model, b.evidence)
            loss = 12 * (
                (path["prior"] - b.target[1:]).square().mean()
                + 0.5 * (path["posterior"] - b.target).square().mean()
            )
            if not torch.isfinite(loss):
                raise FloatingPointError("nonfinite E0 loss")
            loss.backward()
            grad = torch.nn.utils.clip_grad_norm_(model.parameters(), 1, error_if_nonfinite=True)
            opt.step()
            trace.append([i + 1, loss.item(), grad.item(), lr])
            update_cpu.append(time.process_time() - step_start)
    model.eval()
    if any(not t.isfinite().all() for t in model.state_dict().values()):
        raise FloatingPointError("nonfinite E0 checkpoint")
    return {
        "trace": trace,
        "cpu_seconds": time.process_time() - start,
        "wall_seconds": time.monotonic() - wall_start,
        "training_data_sha256": hasher.hexdigest(),
        "steady_update_cpu_seconds": float(np.mean(update_cpu[2:] or update_cpu))
        if update_cpu
        else None,
    }


def wrapped(x):
    return torch.atan2(x.sin(), x.cos())


def phase(features):
    """Privileged diagnostic inverse; never called by a model or fitter."""
    xy = features.double() @ FixedProjection(12, 1729).matrix.double()
    return torch.atan2(xy[..., 1], xy[..., 0]), xy.norm(dim=-1)


def unit_tangents(family):
    difference = family.roll(-1, 0) - family.roll(1, 0)
    norms = difference.norm(dim=-1, keepdim=True)
    return difference / norms.clamp_min(1e-12), norms[:, 0]


@torch.no_grad()
def geometry(model, split, root, config, check=lambda: None):
    rng = np.random.default_rng(seed(split, root, 0, "geometry"))
    count = config["grid"]
    theta = torch.arange(count, dtype=torch.float64) * (2 * np.pi / count)
    theta += rng.uniform(-np.pi, np.pi)
    z = sensor(theta)
    h = model.initialize(z, torch.ones_like(z, dtype=torch.bool))
    zeros = torch.zeros(count, 1)
    initial_phase, initial_power = phase(model.readout(h))
    stationary = [model.readout(h)]
    atlas = None
    for i in range(config["stationary_steps"]):
        check()
        h = model.predict(h, zeros)
        stationary.append(model.readout(h))
        if i + 1 == config["atlas_burnin"]:
            atlas = h.clone()
    assert atlas is not None
    latent = atlas[:, : model.n]
    tangents, tangent_norm = unit_tangents(latent)
    radius = (latent - latent.mean(0)).norm(dim=-1).mean()
    eps = config["perturbation_fraction"] * radius
    direction = torch.from_numpy(rng.normal(size=latent.shape)).float()
    direction -= (direction * tangents).sum(-1, keepdim=True) * tangents
    direction /= direction.norm(dim=-1, keepdim=True).clamp_min(1e-12)
    perturbed, base = atlas.clone(), atlas.clone()
    perturbed[:, : model.n] += eps * direction
    normal_ratio, normal_pose, base_phase, base_norm = [], [], [], []
    base_states, perturbed_states = [], []
    for i in range(config["perturbation_steps"] + 1):
        check()
        base_states.append(base.clone())
        perturbed_states.append(perturbed.clone())
        tangent, norms = unit_tangents(base[:, : model.n])
        delta = perturbed[:, : model.n] - base[:, : model.n]
        perpendicular = delta - (delta * tangent).sum(-1, keepdim=True) * tangent
        normal_ratio.append(perpendicular.norm(dim=-1) / eps.clamp_min(1e-12))
        p0, r0 = phase(model.readout(base))
        p1, _ = phase(model.readout(perturbed))
        normal_pose.append(wrapped(p1 - p0).abs() * (180 / np.pi))
        base_phase.append(p0)
        base_norm.append(norms)
        if i < config["perturbation_steps"]:
            base, perturbed = model.predict(base, zeros), model.predict(perturbed, zeros)
    base_phase = torch.stack(base_phase)
    phase_gap = wrapped(base_phase.roll(-config["tangent_bins"], 1) - base_phase)
    tangent_ratio = phase_gap / phase_gap[0].where(
        phase_gap[0].abs() >= 1e-8, torch.full_like(phase_gap[0], 1e-8)
    )
    stationary = torch.stack(stationary)
    stationary_phase, stationary_power = phase(stationary)
    stationary_deg = wrapped(stationary_phase - theta).abs() * (180 / np.pi)
    issues = []
    if radius < 1e-6 or min(tangent_norm.min(), torch.stack(base_norm).min()) < 1e-7:
        issues.append("degenerate hidden reference family")
    if phase_gap[0].abs().min() < 1e-5:
        issues.append("degenerate initial decoded tangent separation")
    if min(initial_power.min(), stationary_power.min(), r0.min()) < 1e-6:
        issues.append("undefined decoded orientation")
    arrays = {
        "theta": theta.numpy(),
        "atlas": atlas.numpy(),
        "stationary_features": stationary.numpy(),
        "stationary_deg": stationary_deg.numpy(),
        "stationary_drift_deg": (
            wrapped(stationary_phase - initial_phase).abs() * 180 / np.pi
        ).numpy(),
        "normal_ratio": torch.stack(normal_ratio).numpy(),
        "normal_pose_deg": torch.stack(normal_pose).numpy(),
        "tangent_ratio": tangent_ratio.numpy(),
        "tangent_phase_gap": phase_gap.numpy(),
        "family_radius": np.array(radius.item()),
        "geometry_base_states": torch.stack(base_states).numpy(),
        "geometry_perturbed_states": torch.stack(perturbed_states).numpy(),
    }
    metrics = {
        "stationary_deg": float(arrays["stationary_deg"][-1].mean()),
        "normal_ratio": float(arrays["normal_ratio"][-1].mean()),
        "normal_pose_deg": float(arrays["normal_pose_deg"][-1].mean()),
        "tangent_ratio": float(arrays["tangent_ratio"][-1].mean()),
    }
    if issues:
        for key in ("normal_ratio", "normal_pose_deg", "tangent_ratio"):
            metrics[key] = None
    return metrics, arrays, issues


@torch.no_grad()
def development_score(model, root, config, check=lambda: None):
    b, _ = generate(
        "development",
        root,
        batch=config["evaluation_batch"],
        horizon=config["free_horizon"],
        condition="free",
    )
    path = rollout(model, b.evidence, check)
    return float(12 * (path["prior"].double() - b.target[1:].double()).square().mean())


@torch.no_grad()
def evaluate(model, split, root, config, check=lambda: None):
    before = {k: v.clone() for k, v in model.state_dict().items()}
    started = time.process_time()
    wall_started = time.monotonic()
    metrics, arrays, issues = geometry(model, split, root, config, check)
    for condition in (
        "free",
        "grounded",
        "return",
        "interpolate",
        "extrapolate",
        "positive",
        "negative",
    ):
        horizon = 40 if condition == "return" else config["free_horizon"]
        b, _ = generate(
            split, root, batch=config["evaluation_batch"], horizon=horizon, condition=condition
        )
        path = rollout(model, b.evidence, check)
        for key, values in path.items():
            truth = b.target[1:] if key == "prior" else b.target
            errors = 12 * (values.double() - truth.double()).square().mean(-1)
            arrays[condition + "/" + key + "_nmse"] = errors.numpy()
        metrics[condition + "_nmse"] = float(
            arrays[condition + "/posterior_nmse"][-1].mean()
            if condition == "return"
            else arrays[condition + "/prior_nmse"].mean()
        )
    for key, tensor in model.state_dict().items():
        if not torch.equal(tensor, before[key]):
            raise AssertionError("persistent write during E0 inference")
    if any(not np.isfinite(a).all() for a in arrays.values()):
        raise FloatingPointError("nonfinite E0 evaluation array")
    return {
        "metrics": metrics,
        "geometry_issues": issues,
        "inference_cpu_seconds": time.process_time() - started,
        "inference_wall_seconds": time.monotonic() - wall_started,
    }, arrays
