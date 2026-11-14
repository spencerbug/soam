"""Inference traces and evaluator reductions for the bounded B2 benchmark."""

import time

import numpy as np
import torch

from soam.robust.data import CORRUPTION, EXTENSIONS, INTERMITTENT, SENSED, generate
from soam.robust.models import Config, Robust
from soam.temporal.data import CONDITIONS, SCHEDULES, input_hash


def batches(split, root, batch):
    result = {
        f"{c}/{s}": generate(split, root, batch=batch, condition=c, schedule=s)
        for c in CONDITIONS
        for s in SCHEDULES
    }
    result.update(
        {
            f"{c}/{s}": generate(split, root, batch=batch, condition=c, schedule=s)
            for c in EXTENSIONS
            for s in INTERMITTENT
        }
    )
    return result


@torch.no_grad()
def trace(model, ev):
    """No scoring labels/target/condition in this interface."""
    before = {k: t.clone() for k, t in model.state_dict().items()}
    h = model.initialize(ev.observed[0], ev.mask[0])
    priors, posterior = [], [model.readout(h)]
    states, poststates = [], [h.clone()]
    diagnostics = []
    helper = Robust(model, Config()) if model.name == "FILTER2" else None
    if isinstance(model, Robust):
        model.diagnostics = True
    if helper:
        helper.diagnostics = True
    for t in range(len(ev.actions)):
        prev = h
        prior, _ = model.predict(h, ev.actions[t], ev.roles[t])
        priors.append(model.readout(prior).clone())
        states.append(prior.clone())
        # Current observation accessed only after prediction is frozen above.
        h, gamma = model.correct(
            prior,
            prev,
            ev.actions[t],
            ev.roles[t],
            ev.observed[t + 1],
            ev.mask[t + 1],
            ev.noise_sd[t + 1],
        )
        if helper:
            helper.correct(
                prior.double(),
                prev.double(),
                ev.actions[t],
                ev.roles[t],
                ev.observed[t + 1],
                ev.mask[t + 1],
                ev.noise_sd[t + 1],
            )
        posterior.append(model.readout(h).clone())
        poststates.append(h.clone())
        diag_model = helper or (model if isinstance(model, Robust) else None)
        diagnostics.append(
            {k: v.clone() for k, v in diag_model.last.items()}
            if diag_model
            else {"event_weight": gamma[:, 0].clone()}
        )
    assert all(torch.equal(v, before[k]) for k, v in model.state_dict().items()), (
        "persistent inference write"
    )
    if isinstance(model, Robust):
        model.diagnostics = False
    return {
        "prior": torch.stack(priors),
        "posterior": torch.stack(posterior),
        "state": torch.stack(states),
        "poststate": torch.stack(poststates),
        **{k: torch.stack([d[k] for d in diagnostics]) for k in diagnostics[0]},
    }


def event_windows(batch):
    """Evaluator event onset/end; no event metadata is passed to inference."""
    count = len(batch.target[0])
    start = np.full(
        count, 49 if batch.condition == "gap" else 1 if batch.condition == "heavy" else 24
    )
    end = start.copy()
    active = np.ones(count, dtype=bool)
    if batch.condition in {
        "isolated",
        "coherent",
        "corrupt",
        "contradict",
        "channels",
        "sustained",
        "biased",
    }:
        stop = 40 if batch.condition == "sustained" else 48 if batch.condition == "biased" else 32
        if batch.condition in {"isolated", "coherent"}:
            stop = 65
        observed = batch.evidence.mask.any(-1).numpy()
        for j in range(count):
            times = np.flatnonzero(observed[24:stop, j]) + 24
            if len(times):
                start[j] = times[0]
                end[j] = times[0] + 1 if batch.condition in {"isolated", "coherent"} else stop
            else:
                active[j] = False
    if batch.condition == "heavy":
        end[:] = 64
    return start, end, active


def event_recovery(errors, starts, ends=None):
    """Pre-onset baseline fixed even when measuring recovery after fault end."""
    ends = starts if ends is None else ends
    result = np.empty(errors.shape[1])
    censored = np.ones(errors.shape[1], dtype=bool)
    for j, (start, begin) in enumerate(zip(starts, ends, strict=True)):
        threshold = max(0.01, 2 * errors[max(0, start - 8) : start, j].mean())
        result[j] = len(errors) - begin
        for t in range(begin, len(errors) - 2):
            if (errors[t : t + 3, j] <= threshold).all():
                result[j] = t - begin
                censored[j] = False
                break
    return result, censored


def mean_or_zero(x):
    return float(np.mean(x)) if np.size(x) else 0.0


@torch.no_grad()
def evaluate(model, data, variance, check=lambda: None, detail=False):
    rows, arrays = {}, {}
    start_cpu = time.process_time()
    for key, b in data.items():
        check()
        path = trace(model, b.evidence)
        prior = (
            (path["prior"].double() - b.target[1:].double()).square().mean(-1) / variance
        ).numpy()
        post = (
            (path["posterior"].double() - b.target.double()).square().mean(-1) / variance
        ).numpy()
        assert np.isfinite(prior).all() and np.isfinite(post).all(), "nonfinite inference"
        sensed = b.evidence.mask[1:].any(-1).numpy()
        weights = path["event_weight"].numpy()
        starts, ends, exposed = event_windows(b)
        lag, censored = event_recovery(post, starts)
        lag_end, censored_end = event_recovery(post, starts, ends)
        episode = prior.mean(0)
        prefix = key.replace("/", "__") + "__"
        arrays[prefix + "prior"] = prior
        arrays[prefix + "posterior"] = post
        arrays[prefix + "recovery"] = lag
        arrays[prefix + "recovery_after_end"] = lag_end
        arrays[prefix + "event_exposed"] = exposed
        row = {
            "prior": float(prior.mean()),
            "posterior": float(post.mean()),
            "free8": float(prior[:8].mean()),
            "free32": float(prior[:32].mean()),
            "tail95": float(np.quantile(episode, 0.95)),
            "worst": float(episode.max()),
            "worst_episode": int(episode.argmax()),
            "recovery": mean_or_zero(lag[exposed]),
            "censored": mean_or_zero(censored[exposed]),
            "recovery_after_end": mean_or_zero(lag_end[exposed]),
            "censored_after_end": mean_or_zero(censored_end[exposed]),
            "event_exposure": float(exposed.mean()),
            "events": int(sensed.sum()),
            "rejected": mean_or_zero(weights[sensed] == 0),
            "downweighted": mean_or_zero(weights[sensed] < 0.5),
            "mean_weight": mean_or_zero(weights[sensed]),
            "input_hash": input_hash([b]),
            "nonfinite": 0,
            "divergent_episodes_nmse_gt100": int((prior.max(0) > 100).sum()),
        }
        if "nis" in path:
            nis = path["nis"].numpy()
            accepted = sensed & (weights > 0)
            row.update(
                nis=mean_or_zero(nis[sensed]),
                accepted_nis=mean_or_zero(nis[accepted]),
                innovation_rms=mean_or_zero(
                    path["innovation"].square().sum(-1).sqrt().numpy()[sensed]
                ),
                delta_norm=mean_or_zero(path["delta"].norm(dim=-1).numpy()[sensed]),
                gain_norm=mean_or_zero(path["gain"].norm(dim=(-1, -2)).numpy()[sensed]),
            )
            # Evaluator-only calibration in learned coordinates; never fed to model.
            truth = (b.target[1:].double() - model.mean.double()) @ model.P.double()
            error = path["state"][..., :2].double() - truth
            covariance = path["state"][..., 2:6].double().reshape(*error.shape[:-1], 2, 2)
            post_cov = path["poststate"][1:, ..., 2:6].double().reshape_as(covariance)
            maha = (
                (error[..., None, :] @ torch.linalg.solve(covariance, error[..., None]))
                .flatten(-3)
                .numpy()
                .reshape(prior.shape)
            )
            predicted_feature_var = torch.einsum(
                "mi,tbij,mj->tbm", model.P.double(), covariance, model.P.double()
            )
            feature_error = path["prior"].double() - b.target[1:].double()
            coverage = (
                (feature_error.square() <= 3.841458820694124 * predicted_feature_var)
                .double()
                .mean(-1)
                .numpy()
            )
            row.update(
                coverage95=float((maha <= 5.991464547).mean()),
                feature_coverage95=float(coverage.mean()),
                mahalanobis=float(maha.mean()),
                min_eigenvalue=float(torch.linalg.eigvalsh(post_cov).min()),
                max_asymmetry=float((post_cov - post_cov.transpose(-1, -2)).abs().max()),
                covariance_trace=float(covariance.diagonal(dim1=-2, dim2=-1).sum(-1).mean()),
            )
            arrays.update(
                {
                    prefix + "nis": nis,
                    prefix + "weight": weights,
                    prefix + "sensed": sensed,
                    prefix + "maha": maha,
                    prefix + "covtrace": covariance.diagonal(dim1=-2, dim2=-1).sum(-1).numpy(),
                    prefix + "postcovtrace": post_cov.diagonal(dim1=-2, dim2=-1).sum(-1).numpy(),
                }
            )
            if detail and b.schedule == "every4":
                for field in ("innovation", "weight", "delta", "gain", "Sdiag"):
                    arrays[prefix + "diagnostic_" + field] = path[field][:, :4].numpy()
        if detail and b.schedule == "every4":
            arrays[prefix + "prior_state"] = path["state"][:, :4].numpy()
            arrays[prefix + "post_state"] = path["poststate"][:, :4].numpy()
            arrays[prefix + "prediction"] = path["prior"][:, :4].numpy()
            arrays[prefix + "post_features"] = path["posterior"][:, :4].numpy()
            arrays[prefix + "target"] = b.target[:, :4].numpy()
            arrays[prefix + "observed"] = b.evidence.observed[:, :4].numpy()
            arrays[prefix + "mask"] = b.evidence.mask[:, :4].numpy()
        rows[key] = row
    return rows, arrays, time.process_time() - start_cpu


def headline(rows):
    def condition(c, schedules=SENSED):
        return float(np.mean([rows[f"{c}/{s}"]["prior"] for s in schedules]))

    result = {
        "J": float(
            np.mean(
                [
                    rows[f"{c}/{s}"]["prior"]
                    for c in ("partial", "missing", "noise")
                    for s in INTERMITTENT
                ]
            )
        ),
        "free32": rows["partial/initial"]["free32"],
        "free8": rows["partial/initial"]["free8"],
    }
    result.update({c: condition(c) for c in CONDITIONS})
    result.update({c: condition(c, INTERMITTENT) for c in EXTENSIONS})
    result["C"] = float(np.mean([result[c] for c in CORRUPTION]))
    return result


@torch.no_grad()
def inference_only(model, ev):
    """The actual predict/decode/correct loop, without diagnostic storage."""
    h = model.initialize(ev.observed[0], ev.mask[0])
    for t in range(len(ev.actions)):
        previous = h
        prior, _ = model.predict(h, ev.actions[t], ev.roles[t])
        prediction = model.readout(prior)
        h = prior
        idx = ev.mask[t + 1].any(-1).nonzero().flatten()
        if len(idx):
            corrected, _ = model.correct(
                prior[idx],
                previous[idx],
                ev.actions[t, idx],
                ev.roles[t, idx],
                ev.observed[t + 1, idx],
                ev.mask[t + 1, idx],
                ev.noise_sd[t + 1, idx],
            )
            h = h.index_copy(0, idx, corrected)
    return prediction, h


@torch.no_grad()
def latency(model, root=15001):
    """Same driver and observations; no traces, evaluator, or reliability diagnostics."""
    if isinstance(model, Robust):
        model.diagnostics = False
    result = {}
    for batch in (1, 20):
        b = generate("fixture", root, batch=batch)
        # Same minimal loop for original/PC16/robust; scores no ground truth.
        for _ in range(3):
            inference_only(model, b.evidence)
        times = []
        for _ in range(20):
            start = time.perf_counter_ns()
            inference_only(model, b.evidence)
            times.append((time.perf_counter_ns() - start) / 1000 / 64 / batch)
        result[str(batch)] = {
            "mean_us_per_step": float(np.mean(times)),
            "p95_us_per_step": float(np.quantile(times, 0.95)),
            "max_us_per_step": float(max(times)),
        }
    return result


@torch.no_grad()
def operation_profile(model):
    if isinstance(model, Robust):
        model.diagnostics = False
    b = generate("fixture", 15001, batch=1)
    with torch.profiler.profile(
        activities=[torch.profiler.ProfilerActivity.CPU], record_shapes=True, with_flops=True
    ) as profile:
        inference_only(model, b.evidence)
    linear = {"aten::mm", "aten::bmm", "aten::addmm", "aten::mv", "aten::addmv"}
    solves = []
    nonlinear = {}
    macs = 0
    for e in profile.key_averages(group_by_input_shape=True):
        if e.key in linear:
            macs += e.flops / 2
        if e.key in {"aten::linalg_solve", "aten::linalg_inv", "aten::linalg_eigvalsh"}:
            solves.append({"operator": e.key, "count": e.count, "input_shapes": e.input_shapes})
        if e.key in {
            "aten::tanh",
            "aten::sigmoid",
            "aten::sqrt",
            "aten::clamp",
            "aten::clamp_min",
            "aten::minimum",
        }:
            nonlinear[e.key] = nonlinear.get(e.key, 0) + e.count
    return {
        "profiled_linear_macs_per_step": macs / 64,
        "solves_and_eigen_operations": solves,
        "nonlinear_operator_calls": nonlinear,
        "schedule": "every4",
        "batch": 1,
        "horizon": 64,
        "note": "Torch profiled mm/bmm/addmm/mv/addmv FLOPs divided by2; omits elementwise ops and internal solve/eigen flops; includes initialization and prior readout; no timing claim from MACs.",
    }
