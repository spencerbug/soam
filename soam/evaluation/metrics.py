"""Paired grounded/open-loop diagnostics; never used to train the predictor."""

import time

import torch


def prediction_metrics(predicted, target):
    if not torch.isfinite(predicted).all():
        raise FloatingPointError("nonfinite predicted observations")
    squared = (predicted - target).square()
    # Energy normalization, not variance-normalization or a claimed R-squared.
    energy = target.square().mean().clamp_min(1e-12)
    return {
        "mse": squared.mean().item(),
        "nmse": (squared.mean() / energy).item(),
        "final_nmse": (squared[:, -1].mean() / energy).item(),
        "prefix_nmse": (squared.mean((0, 2)) / energy).tolist(),
        "target_energy": energy.item(),
    }


def hidden_stability(hidden, bound):
    valid = torch.isfinite(hidden).all(-1)
    over_bound = hidden.abs().amax(-1) > bound
    return {
        "invalid_trajectory_fraction": (~valid.all(-1)).float().mean().item(),
        "bound_violation_fraction": over_bound.any(-1).float().mean().item(),
        "max_abs_hidden": hidden.abs().max().item(),
    }


@torch.no_grad()
def evaluate(model, batch, cfg, projection, perturb_seed):
    model.eval()
    obs, actions, contexts = batch.observations, batch.actions, batch.contexts
    start = time.perf_counter()
    pred, hidden = model.rollout(obs[:, 0], actions, contexts)
    elapsed = time.perf_counter() - start
    grounded, _ = model.rollout(obs[:, 0], actions, contexts, observations=obs)
    target = obs[:, 1:]
    metrics = {
        "free": prediction_metrics(pred, target),
        "grounded": prediction_metrics(grounded, target),
        "persistence_free": prediction_metrics(obs[:, :1].expand_as(target), target),
        "persistence_grounded": prediction_metrics(obs[:, :-1], target),
        "stability": hidden_stability(hidden, cfg.hidden_bound),
        "rollout_seconds": elapsed,
        "seconds_per_transition": elapsed / actions.shape[0] / actions.shape[1],
    }
    metrics["per_start_context"] = {
        str(i): prediction_metrics(pred[contexts[:, 0] == i], target[contexts[:, 0] == i])
        for i in range(model.contexts)
        if (contexts[:, 0] == i).any()
    }
    wrong_context, _ = model.rollout(obs[:, 0], actions, (contexts + 1) % model.contexts)
    scrambled_action, _ = model.rollout(obs[:, 0], actions.flip(1), contexts)
    metrics["wrong_context_nmse"] = prediction_metrics(wrong_context, target)["nmse"]
    metrics["reversed_actions_nmse"] = prediction_metrics(scrambled_action, target)["nmse"]
    switch_mask = contexts[:, 1:] != contexts[:, :-1]
    energy = target.square().mean().clamp_min(1e-12)
    errors = (pred - target).square().mean(-1) / energy
    by_offset = []
    for lag in range(cfg.switch_every):
        mask = torch.zeros_like(contexts, dtype=torch.bool)
        length = contexts.shape[1] - 1 - lag
        if length > 0:
            mask[:, 1 + lag :] = switch_mask[:, :length]
        by_offset.append(errors[mask].mean().item() if mask.any() else None)
    metrics["nmse_by_steps_after_switch"] = by_offset
    generator = torch.Generator().manual_seed(perturb_seed)
    noise = torch.randn(hidden[:, 0].shape, generator=generator) * cfg.perturb_std
    perturbed, perturbed_hidden = model.rollout(
        obs[:, 0], actions, contexts, perturb=(cfg.perturb_step, noise)
    )
    step = cfg.perturb_step
    hidden_delta = (
        (perturbed_hidden[:, step + 1 :] - hidden[:, step + 1 :]).square().mean(-1).sqrt()
    )
    reference_delta = noise.square().mean(-1).sqrt().clamp_min(1e-12)
    ratio = hidden_delta / reference_delta[:, None]
    feature_gap = (perturbed[:, step:] - pred[:, step:]).square().mean((0, 2)) / energy
    metrics["perturbation"] = {
        **prediction_metrics(perturbed[:, step:], target[:, step:]),
        "noise_rms": noise.square().mean().sqrt().item(),
        "hidden_gap_ratio_by_step": ratio.mean(0).tolist(),
        "final_hidden_gap_ratio": ratio[:, -1].mean().item(),
        "sustained_half_gap_fraction": (ratio[:, -min(4, ratio.shape[1]) :] <= 0.5)
        .all(-1)
        .float()
        .mean()
        .item(),
        "feature_gap_nmse_by_step": feature_gap.tolist(),
        "excess_mse_after_perturbation": (
            (perturbed[:, step:] - target[:, step:]).square().mean()
            - (pred[:, step:] - target[:, step:]).square().mean()
        ).item(),
        **hidden_stability(perturbed_hidden, cfg.hidden_bound),
    }
    decoded = projection.diagnostic_inverse(pred)
    # Temporal motion diagnostic helps distinguish stability from collapse.
    true_speed = (batch.states[:, 2:] - batch.states[:, 1:-1]).square().sum(-1).mean()
    pred_speed = (decoded[:, 1:] - decoded[:, :-1]).square().sum(-1).mean()
    metrics["predicted_to_true_motion_energy"] = (pred_speed / true_speed.clamp_min(1e-12)).item()
    return metrics, {
        "predicted": pred,
        "perturbed": perturbed,
        "hidden": hidden,
        "truth": batch.states,
        "contexts": contexts,
    }
