"""Causal evidence-only rollout, offline fitting and evaluator-owned reduction."""

import math
import time

import numpy as np
import torch
from torch.nn import functional as F

from soam.gating.engine import ridge
from soam.gating.models import bilinear
from soam.temporal.data import CONDITIONS, SCHEDULES, generate
from soam.temporal.models import LINEAR, SETTLERS


def rollout(model, evidence, *, k=None, mode="fixed", variance=1.0, metadata=False):
    """No target or environment input. Every prior is recorded before current evidence access."""
    k = (4 if model.name in SETTLERS else 0) if k is None else k
    if k and model.name not in SETTLERS:
        raise ValueError("candidate does not support extra iterations")
    ev = evidence
    h = model.initialize(ev.observed[0], ev.mask[0])
    b = len(h)
    updates = torch.ones(b)
    macs = torch.full((b,), float(model.resources()["initial_macs"]))
    costs = model.resources()
    stages, counts, halt_logits, halt_active = [], [], [], []

    def settling(h, t):
        active = ev.mask[t].any(-1)
        if mode == "periodic" and t % 2:
            active = torch.zeros_like(active)
        stage = [model.readout(h)]
        count = torch.zeros(b)
        logits, used = [], []
        for j in range(k):
            if mode == "learned":
                proposed = torch.zeros(b, dtype=torch.bool)
                idx = active.nonzero().flatten()
                if len(idx):
                    proposed[idx] = torch.sigmoid(model.halt(h[idx])).flatten() >= 0.5
                    macs[idx] += costs["halting_macs"]
                active = active & proposed
            idx = active.nonzero().flatten()
            logit = h.new_zeros((b, 1))
            previous_output = stage[-1]
            if len(idx):
                if hasattr(model, "halt") and torch.is_grad_enabled():
                    # Offline supervision of continuation. No target enters this operation.
                    logit = logit.index_copy(0, idx, model.halt(h[idx]))
                changed = model.settle(h[idx], ev.observed[t, idx], ev.mask[t, idx])
                h = h.index_copy(0, idx, changed)
                count[idx] += 1
                updates[idx] += 1
                macs[idx] += costs["settle_macs"]
            current_output = model.readout(h)
            stage.append(current_output)
            logits.append(logit)
            used.append(active.clone())
            if mode == "event":
                difference = (current_output - previous_output).square().mean(-1) / variance
                active = active & (difference > 0.01)
        stages.append(torch.stack(stage))
        counts.append(count)
        if k:
            halt_logits.append(torch.stack(logits))
            halt_active.append(torch.stack(used))
        return h

    h = settling(h, 0)
    posterior = [model.readout(h)]
    priors, gammas, betas = [], [], []
    for t in range(len(ev.actions)):
        previous = h
        prior, beta = model.predict(previous, ev.actions[t], ev.roles[t])
        priors.append(model.readout(prior))  # strictly before observation t+1
        betas.append(beta)
        updates += 1
        macs += costs["predict_macs"]
        h = prior
        idx = ev.mask[t + 1].any(-1).nonzero().flatten()
        gamma = h.new_zeros((b, 1))
        if len(idx):
            corrected, g = model.correct(
                prior[idx],
                previous[idx],
                ev.actions[t, idx],
                ev.roles[t, idx],
                ev.observed[t + 1, idx],
                ev.mask[t + 1, idx],
                ev.noise_sd[t + 1, idx],
                metadata=metadata,
            )
            h = h.index_copy(0, idx, corrected)
            gamma = gamma.index_copy(0, idx, g)
            updates[idx] += 1
            macs[idx] += costs["correct_macs"]
        gammas.append(gamma)
        h = settling(h, t + 1)
        posterior.append(model.readout(h))
    return {
        "prior": torch.stack(priors),
        "posterior": torch.stack(posterior),
        "stages": torch.stack(stages),
        "counts": torch.stack(counts),
        "gamma": torch.stack(gammas),
        "beta": torch.stack(betas),
        "updates": updates,
        "macs": macs,
        "halt_logits": torch.stack(halt_logits) if k else h.new_empty(0),
        "halt_active": torch.stack(halt_active) if k else torch.empty(0, dtype=torch.bool),
    }


def objective(model, batch):
    path = rollout(model, batch.evidence)
    prediction = (path["prior"] - batch.target[1:]).square().mean()
    stage_error = (path["stages"] - batch.target[:, None]).square().mean(-1)
    reconstruction = stage_error.mean()
    halt = prediction * 0
    if model.name == "SET32":
        label = (stage_error[:, 1:] < stage_error[:, :-1]).float().detach()
        active = path["halt_active"]
        loss = F.binary_cross_entropy_with_logits(
            path["halt_logits"][..., 0], label, reduction="none"
        )
        halt = (loss * active).sum() / active.sum().clamp_min(1)
    return prediction + 0.5 * reconstruction + 0.01 * halt


@torch.no_grad()
def fit_linear(model, data, penalty):
    clean = torch.cat([b.target.reshape(-1, 12) for b in data])
    mean = clean.double().mean(0)
    _, _, v = torch.linalg.svd(clean.double() - mean, full_matrices=False)
    p = v[:2].T
    for j in range(2):
        if p[p[:, j].abs().argmax(), j] < 0:
            p[:, j] *= -1
    model.P.copy_(p.float())
    model.mean.copy_(mean.float())
    model.penalty.fill_(penalty)
    cue = torch.cat([b.evidence.observed[0] for b in data])
    mask = torch.cat([b.evidence.mask[0] for b in data])
    initial_target = torch.cat([b.target[0] for b in data])
    u = torch.cat((cue, mask.float(), torch.ones_like(cue[:, :1])), -1)
    model.L.copy_(ridge(u, (initial_target - model.mean) @ model.P, penalty))
    old = torch.cat([b.target[:-1].reshape(-1, 12) for b in data])
    new = torch.cat([b.target[1:].reshape(-1, 12) for b in data])
    a = torch.cat([b.evidence.actions.reshape(-1, 3) for b in data])
    moving = torch.cat([b.evidence.roles[..., 1].flatten().bool() for b in data])
    old, new = (old - model.mean) @ model.P, (new - model.mean) @ model.P
    model.B.copy_(ridge(bilinear(old[moving], a[moving]), new[moving], penalty))
    residual = new[moving] - bilinear(old[moving], a[moving]) @ model.B.T
    process = residual.double().T @ residual.double() / len(residual)
    model.process.copy_(process.float() + 1e-6 * torch.eye(2))


def primary_batches(split, root, batch=20, horizon=64):
    return [
        generate(split, root, batch=batch, horizon=horizon, condition=c, schedule=s)
        for c in ("partial", "missing", "noise")
        for s in ("every2", "every4", "every8", "irregular")
    ]


@torch.no_grad()
def primary_score(model, batches, variance, k=None):
    return float(
        np.mean(
            [
                (rollout(model, b.evidence, k=k)["prior"].double() - b.target[1:].double())
                .square()
                .mean()
                .item()
                / variance
                for b in batches
            ]
        )
    )


def fit(
    model,
    data,
    setting,
    check,
    *,
    development=None,
    variance=1.0,
    checkpoints=(300, 600, 900, 1050, 1200),
):
    start = time.process_time()
    trace, learning = [], {}
    if model.name in LINEAR:
        fit_linear(model, data, setting)
        check()
        if development:
            learning[str(len(data))] = primary_score(model, development, variance)
    else:
        opt = torch.optim.Adam(model.parameters(), lr=setting)
        for i, b in enumerate(data):
            check()
            ratio = (
                1.0
                if i < 600
                else 0.01 + 0.99 * 0.5 * (1 + math.cos(math.pi * min((i - 600) / 599, 1)))
            )
            for group in opt.param_groups:
                group["lr"] = setting * ratio
            opt.zero_grad(set_to_none=True)
            loss = objective(model, b)
            if not torch.isfinite(loss):
                raise FloatingPointError("nonfinite training")
            loss.backward()
            grad = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
            opt.step()
            trace.append([i + 1, loss.item(), grad.item(), setting * ratio])
            if development and i + 1 in checkpoints:
                learning[str(i + 1)] = primary_score(model, development, variance)
    if any(not t.isfinite().all() for t in model.state_dict().values()):
        raise FloatingPointError("nonfinite fitted tensor")
    return {"trace": trace, "learning": learning, "fit_cpu_seconds": time.process_time() - start}


def recovery(errors, start):
    """Per-episode recovery, censored at end+1; errors indexed by physical posterior time."""
    base = errors[max(0, start - 8) : start].mean(0)
    threshold = np.maximum(0.01, 2 * base)
    result = np.full(errors.shape[1], errors.shape[0] - start, dtype=float)
    censored = np.ones(errors.shape[1], dtype=bool)
    for t in range(start, len(errors) - 2):
        ok = (errors[t : t + 3] <= threshold).all(0) & censored
        result[ok] = t - start
        censored[ok] = False
    return result, censored


@torch.no_grad()
def evaluate(
    model,
    split,
    root,
    variance,
    *,
    k=0,
    mode="fixed",
    metadata=False,
    batch=20,
    horizon=64,
    check=lambda: None,
    full=True,
):
    before = {key: t.clone() for key, t in model.state_dict().items()}
    rows, arrays = {}, {}
    conditions = CONDITIONS if full else ("partial",)
    schedules = SCHEDULES if full else ("every4",)
    cpu = time.process_time()
    for condition in conditions:
        for schedule in schedules:
            check()
            b = generate(
                split, root, batch=batch, horizon=horizon, condition=condition, schedule=schedule
            )
            path = rollout(model, b.evidence, k=k, mode=mode, variance=variance, metadata=metadata)
            prior = (path["prior"].double() - b.target[1:].double()).square().mean(
                -1
            ).numpy() / variance
            post = (path["posterior"].double() - b.target.double()).square().mean(
                -1
            ).numpy() / variance
            inner = (path["stages"].double() - b.target[:, None].double()).square().mean(
                -1
            ).numpy() / variance
            if not all(np.isfinite(x).all() for x in (prior, post, inner)):
                raise FloatingPointError("nonfinite inference")
            sensed = b.evidence.mask.any(-1).numpy()
            start = (
                3 * horizon // 4 + 1
                if condition == "gap"
                else horizon // 2
                if condition in {"corrupt", "contradict"}
                else 3 * horizon // 8
            )
            times, censored = recovery(post, start)
            age = np.zeros_like(sensed, dtype=int)
            for t in range(1, horizon + 1):
                age[t] = np.where(sensed[t], 0, age[t - 1] + 1)
            key = f"{condition}/{schedule}"
            rows[key] = {
                "prior": float(prior.mean()),
                "posterior": float(post[1:].mean()),
                "free8": float(prior[:8].mean()),
                "free32": float(prior[:32].mean()),
                "prior_curve": prior.mean(1).tolist(),
                "posterior_curve": post.mean(1).tolist(),
                "inner_curve": inner.mean(2).tolist(),
                "recovery_steps": float(times.mean()),
                "recovery_censored_fraction": float(censored.mean()),
                "updates_per_step": float(path["updates"].mean() / horizon),
                "macs_per_step": float(path["macs"].mean() / horizon),
                "settles_per_event": float(path["counts"].sum() / sensed.sum()),
                "observed_events": float(sensed.sum() / batch),
                "observed_features": float(b.evidence.mask.sum() / batch),
                "gamma_curve": path["gamma"].mean((1, 2)).tolist(),
                "beta_curve": path["beta"].mean((1, 2)).tolist(),
                "gap_age_error": {
                    str(j): float(prior[age[:-1] == j].mean()) for j in np.unique(age[:-1])
                },
                "initial_cue_output_variance_by_iteration": path["stages"][0]
                .double()
                .var(1, unbiased=False)
                .mean(-1)
                .tolist(),
            }
            prefix = key.replace("/", "__")
            arrays[prefix + "__prior"] = prior.astype(np.float32)
            arrays[prefix + "__posterior"] = post.astype(np.float32)
            arrays[prefix + "__inner"] = inner.astype(np.float32)
            arrays[prefix + "__counts"] = path["counts"].numpy()
    assert all(torch.equal(t, before[key]) for key, t in model.state_dict().items()), (
        "inference wrote weights"
    )
    return rows, arrays, time.process_time() - cpu


def headline(rows):
    primary = [
        v["prior"]
        for key, v in rows.items()
        if key.split("/")[0] in {"partial", "missing", "noise"}
        and key.split("/")[1] in {"every2", "every4", "every8", "irregular"}
    ]
    return {
        "J": float(np.mean(primary)),
        **{
            c: float(
                np.mean(
                    [
                        v["prior"]
                        for key, v in rows.items()
                        if key.startswith(c + "/") and not key.endswith("/initial")
                    ]
                )
            )
            for c in CONDITIONS
        },
        "free8": rows["partial/initial"]["free8"],
        "free32": rows["partial/initial"]["free32"],
        "macs": float(np.mean([v["macs_per_step"] for v in rows.values()])),
        "updates": float(np.mean([v["updates_per_step"] for v in rows.values()])),
    }
