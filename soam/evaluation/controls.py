"""Reserved SOAM-001 stress evaluations and preregistered engineering screen."""

from dataclasses import replace

import torch

from soam.environments.dynamics import Dynamics
from soam.evaluation.metrics import evaluate, prediction_metrics

CONDITIONS = ("steady", "regular", "irregular", "irregular_hold")


def switch_lag_metrics(predicted, target, contexts, max_lag=8):
    """Attribute each transition only to its most recent switch, excluding initial context."""
    ages = torch.full_like(contexts, -1)
    for t in range(1, contexts.shape[1]):
        switched = contexts[:, t] != contexts[:, t - 1]
        ages[:, t] = torch.where(
            switched, 0, torch.where(ages[:, t - 1] >= 0, ages[:, t - 1] + 1, -1)
        )
    errors = (predicted - target).square().mean(-1)
    energy = target.square().mean().clamp_min(1e-12)
    return [
        {
            "lag": lag,
            "count": int((ages == lag).sum()),
            "nmse": (errors[ages == lag].mean() / energy).item() if (ages == lag).any() else None,
        }
        for lag in range(max_lag)
    ]


@torch.no_grad()
def evaluate_controls(model, cfg, seed):
    records, artifacts = {}, {}
    n = cfg.eval_sequences_per_context * model.contexts
    for split in ("dev", "test"):
        records[split] = {}
        for horizon in cfg.control_horizons:
            records[split][str(horizon)] = {}
            for index, condition in enumerate(CONDITIONS):
                namespace = cfg.stream_namespace * 10000 + 10 * horizon + index
                env = Dynamics(cfg.environment, seed, split, namespace=namespace)
                batch = env.sample(
                    n,
                    horizon,
                    balanced=True,
                    switch_every=cfg.switch_every if condition == "regular" else None,
                    irregular=condition.startswith("irregular"),
                    action_hold=4 if condition == "irregular_hold" else 1,
                )
                metrics, artifact = evaluate(
                    model,
                    batch,
                    replace(cfg, eval_horizon=horizon),
                    env.encoder,
                    seed + namespace + 991,
                )
                pred, target = artifact["predicted"], batch.observations[:, 1:]
                energy = target.square().mean().clamp_min(1e-12)
                step_errors = (pred - target).square().mean((0, 2)) / energy
                metrics["free"]["cumulative_nmse"] = (
                    step_errors.cumsum(0) / torch.arange(1, horizon + 1)
                ).tolist()
                metrics["per_active_context"] = {
                    str(c): prediction_metrics(
                        pred[batch.contexts == c].unsqueeze(0),
                        target[batch.contexts == c].unsqueeze(0),
                    )
                    for c in range(model.contexts)
                    if (batch.contexts == c).any()
                }
                # Active-context final/prefix fields have no temporal interpretation; keep scalars.
                metrics["per_active_context"] = {
                    c: {k: v for k, v in values.items() if k in {"mse", "nmse", "target_energy"}}
                    for c, values in metrics["per_active_context"].items()
                }
                del metrics["nmse_by_steps_after_switch"]  # Regular-schedule legacy diagnostic.
                metrics["switch_lags"] = switch_lag_metrics(pred, target, batch.contexts)
                metrics["motion_collapse"] = metrics["predicted_to_true_motion_energy"] < 0.25
                metrics["stream_namespace"] = namespace
                metrics["switch_count"] = int(
                    (batch.contexts[:, 1:] != batch.contexts[:, :-1]).sum()
                )
                metrics["extra_handoff_macs"] = (
                    metrics["switch_count"] * model.hidden_dim * model.observation_dim
                    if model.variant == "independent"
                    else 0
                )
                metrics["stored_trajectory_tensor_bytes"] = sum(
                    t.numel() * t.element_size() for t in artifact.values()
                )
                records[split][str(horizon)][condition] = metrics
                # Preserve all test trajectories for reproducibility and diagnostics.
                if split == "test":
                    for key, tensor in artifact.items():
                        artifacts[f"control_{horizon}_{condition}_{key}"] = tensor
    return records, artifacts


def readiness(controls):
    test = controls["test"]
    if "48" not in test:
        return {"applicable": False, "reason": "48-step protocol horizon absent (smoke only)"}
    steady, irregular = test["48"]["steady"], test["48"]["irregular"]
    checks = {
        "steady_accuracy": steady["free"]["nmse"] <= 0.15,
        "irregular_accuracy": irregular["free"]["nmse"] <= 0.25,
        "steady_contexts": all(v["nmse"] <= 0.25 for v in steady["per_start_context"].values()),
        "beats_persistence": steady["free"]["nmse"] <= 0.25 * steady["persistence_free"]["nmse"],
        "motion": all(
            0.25 <= m["predicted_to_true_motion_energy"] <= 4 for m in (steady, irregular)
        ),
        "perturbation": all(
            m["perturbation"]["final_hidden_gap_ratio"] <= 1 for m in (steady, irregular)
        ),
        "stability": all(
            m["stability"]["invalid_trajectory_fraction"] == 0
            and m["stability"]["bound_violation_fraction"] == 0
            for horizon in test.values()
            for m in horizon.values()
        ),
    }
    return {"applicable": True, "passed": all(checks.values()), "checks": checks}
