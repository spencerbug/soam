"""Causal inference, equal-information offline fitting and evaluator-only metrics."""

import math
import time

import numpy as np
import torch

from soam.gating.engine import ridge
from soam.gating.models import bilinear
from soam.temporal.models import Linear

from .data import PRIMARY
from .models import advance_support, weights


def rollout(model, evidence, *, detail=False):
    ev = evidence
    state = model.initialize(ev.observed[0], ev.mask[0])
    logit = state.new_zeros(len(state))
    result = {
        k: []
        for k in (
            "candidate_prior",
            "candidate_post",
            "mixture_prior",
            "mixture_post",
            "prob",
            "prior_prob",
            "misfit",
            "nis",
        )
    }
    states = [state] if detail else []
    for t, action in enumerate(ev.actions):
        prior = model.predict(state, action, logit)
        lp = advance_support(logit)
        cp = model.decode(prior)
        result["candidate_prior"].append(cp)
        result["mixture_prior"].append((cp * weights(lp)[..., None]).sum(1))
        result["prior_prob"].append(lp.sigmoid())
        # This is the first access to current observation t+1.
        z, m = ev.observed[t + 1], ev.mask[t + 1]
        score, misfit, nis = model.score(prior, z, m)
        ratio = ((score[:, 1] - score[:, 0]) / model.temperature).clamp(-6, 6)
        logit = (lp + torch.where(m.any(-1), ratio, 0)).to(state.dtype)
        posterior = model.correct(prior, z, m, logit)
        decoded = model.decode(posterior)
        result["candidate_post"].append(decoded)
        result["mixture_post"].append((decoded * weights(logit)[..., None]).sum(1))
        result["prob"].append(logit.sigmoid())
        result["misfit"].append(misfit)
        result["nis"].append(nis)
        state = model.retain(posterior, logit)
        if detail:
            states.append(state)
    out = {k: torch.stack(v) for k, v in result.items()}
    if detail:
        out["state"] = torch.stack(states)
    return out


def chosen(values, labels):
    return values.gather(2, labels.long()[..., None, None].expand(-1, -1, 1, 12))[..., 0, :]


def objective(model, batch):
    out = rollout(model, batch.evidence)
    y = batch.labels[1:].to(out["prob"].dtype)
    prior = chosen(out["candidate_prior"], y)
    post = chosen(out["candidate_post"], y)
    return (
        (prior - batch.target[1:]).square().mean()
        + 0.5 * (post - batch.target[1:]).square().mean()
        + 0.05 * (out["prob"] - y).square().mean()
    )


@torch.no_grad()
def fit_linear(data):
    model = Linear("FILTER2")
    clean = torch.cat([b.target.reshape(-1, 12) for b in data]).double()
    mean = clean.mean(0)
    _, _, v = torch.linalg.svd(clean - mean, full_matrices=False)
    p = v[:2].T
    for j in range(2):
        if p[p[:, j].abs().argmax(), j] < 0:
            p[:, j] *= -1
    model.P.copy_(p.float())
    model.mean.copy_(mean.float())
    old = torch.cat([b.target[:-1].reshape(-1, 12) for b in data])
    new = torch.cat([b.target[1:].reshape(-1, 12) for b in data])
    actions = torch.cat([b.evidence.actions.reshape(-1, 3) for b in data]).clone()
    signs = torch.cat([(2 * b.labels[1:] - 1).flatten() for b in data])
    actions[:, 0] *= signs.float()
    x, y = (old - model.mean) @ model.P, (new - model.mean) @ model.P
    design = bilinear(x, actions)
    model.B.copy_(ridge(design, y, 0.0001))
    residual = (y - design @ model.B.T).double()
    model.process.copy_((residual.T @ residual / len(residual)).float() + 1e-6 * torch.eye(2))
    # L is an inherited unused buffer; initialization uses the fitted masked solve.
    return model


@torch.no_grad()
def calibrate_variance(model, data):
    sums, count = torch.zeros(12, dtype=torch.float64), 0
    for batch in data[:24]:
        out = rollout(model, batch.evidence)
        error = chosen(out["candidate_prior"], batch.labels[1:]) - batch.target[1:]
        sums += error.double().square().sum((0, 1))
        count += error.shape[0] * error.shape[1]
    model.variance.copy_((sums / count + 0.0001).clamp_min(0.0001).float())


def fit_neural(model, data, lr, check=lambda: None, development=None):
    start = time.process_time()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    trace, learning = [], {}
    for i, batch in enumerate(data):
        check()
        scale = (
            1 if i < 600 else 0.01 + 0.99 * 0.5 * (1 + math.cos(math.pi * min((i - 600) / 599, 1)))
        )
        opt.param_groups[0]["lr"] = lr * scale
        opt.zero_grad(set_to_none=True)
        loss = objective(model, batch)
        if not torch.isfinite(loss):
            raise FloatingPointError("nonfinite training loss")
        loss.backward()
        grad = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
        opt.step()
        trace.append([i + 1, loss.item(), float(grad), lr * scale])
        if development is not None and i + 1 in {1050, 1200}:
            with torch.no_grad():
                learning[str(i + 1)] = float(
                    np.mean(
                        [metrics(rollout(model, b.evidence), b, 1.0)["brier"] for b in development]
                    )
                )
    calibrate_variance(model, data)
    return {"trace": trace, "learning": learning, "fit_cpu_seconds": time.process_time() - start}


def phase_brier(error, condition):
    boundary = 28 if condition == "delayed" else 12
    return 0.5 * (error[: boundary - 1].mean() + error[boundary - 1 :].mean())


def recovery(prob, labels, start=20):
    correct = np.where(labels > 0.5, prob, 1 - prob)
    result = np.full(prob.shape[1], len(prob) - start + 1, dtype=float)
    for j in range(prob.shape[1]):
        for t in range(start - 1, len(prob) - 2):
            if np.all(correct[t : t + 3, j] >= 0.8):
                result[j] = t - (start - 1)
                break
    return result


def arrays(out, batch, variance):
    result = {k: v.detach().cpu().numpy() for k, v in out.items()}
    target = batch.target[1:].double().numpy()
    result["labels"] = batch.labels[1:].numpy()
    result["target"] = target
    result["mask"] = batch.evidence.mask[1:].numpy()
    result["actions"] = batch.evidence.actions.numpy()
    result["pairs"] = batch.pairs.numpy()
    result["prior_error"] = ((result["mixture_prior"] - target) ** 2).mean(-1) / variance
    result["post_error"] = ((result["mixture_post"] - target) ** 2).mean(-1) / variance
    result["brier_error"] = (result["prob"] - result["labels"]) ** 2
    return result


def metrics(out, batch, variance):
    return reduce_arrays(arrays(out, batch, variance), batch.condition)


def reduce_arrays(a, condition):
    p, y, e = a["prob"].astype(float), a["labels"], a["brier_error"]
    valid = y <= 1
    confidence = np.maximum(p, 1 - p)
    ninfo = (
        len(p)
        if condition in {"ambiguous", "uninformative"}
        else (27 if condition == "delayed" else 11)
    )
    amb = e[:ninfo]
    clipped = np.clip(p, 1e-8, 1 - 1e-8)
    nll = -(y * np.log(clipped) + (1 - y) * np.log(1 - clipped))
    correct_p = np.where(y > 0.5, p, 1 - p)
    rec = recovery(p, y)
    known = condition != "unknown"
    index = np.minimum(y, 1).astype(int)
    candidate = np.take_along_axis(a["candidate_prior"], index[..., None, None], axis=2)[:, :, 0]
    # Candidate error shares the exact normalization encoded in prior_error.
    sq = ((a["mixture_prior"] - a["target"]) ** 2).mean(-1)
    good = sq > 1e-16
    normalizer = float(np.median(sq[good] / a["prior_error"][good])) if np.any(good) else 1.0
    bins = []
    for lo in np.arange(0, 1, 0.1):
        use = (p >= lo) & (p < lo + 0.1) & valid
        bins.append(
            {
                "lower": float(lo),
                "count": int(use.sum()),
                "mean_probability": float(p[use].mean()) if use.any() else None,
                "frequency": float(y[use].mean()) if use.any() else None,
            }
        )
    return {
        "brier": float(phase_brier(e, condition)) if known else None,
        "prior_brier": float(phase_brier((a["prior_prob"] - y) ** 2, condition)) if known else None,
        "ambiguous_brier": float(amb.mean()),
        "ambiguity_confidence": float((confidence[:ninfo] > 0.95).mean()),
        "late_brier": float(e[-8:].mean()) if known else None,
        "prior_nmse": float(a["prior_error"].mean()),
        "posterior_nmse": float(a["post_error"].mean()),
        "candidate_nmse": float(((candidate - a["target"]) ** 2).mean() / normalizer)
        if known
        else None,
        "nll": float(nll[valid].mean()),
        "wrong_confident": float(((correct_p < 0.05) & valid).sum() / valid.sum()),
        "recovery": float(rec.mean()),
        "recovery_censored": float((rec == len(p) - 20 + 1).mean()),
        "episode_p95_nmse": float(np.quantile(a["prior_error"].mean(0), 0.95)),
        "worst_episode_nmse": float(a["prior_error"].mean(0).max()),
        "minimum_misfit": float(a["misfit"].min(-1)[a["mask"].any(-1)].mean()),
        "reliability_bins": bins,
    }


def headline(rows):
    informative = ("later", "diagnostic", "misleading", "delayed")
    return {
        "brier": float(np.mean([rows[c]["brier"] for c in PRIMARY])),
        "prior_nmse": float(np.mean([rows[c]["prior_nmse"] for c in PRIMARY])),
        "ambiguous_brier": float(np.mean([rows[c]["ambiguous_brier"] for c in PRIMARY])),
        "ambiguity_confidence": float(np.mean([rows[c]["ambiguity_confidence"] for c in PRIMARY])),
        "late_brier": float(np.mean([rows[c]["late_brier"] for c in informative])),
        "recovery": rows["misleading"]["recovery"],
    }
