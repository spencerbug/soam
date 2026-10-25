"""Configuration-driven substrate experiment with immutable output directories."""

import argparse
import json
import random
import time
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import torch

from soam.config import Config
from soam.environments.dynamics import Dynamics
from soam.evaluation.metrics import evaluate, hidden_stability, prediction_metrics
from soam.evaluation.plots import plot_run
from soam.evaluation.provenance import capture
from soam.recurrent.models import build_model, parameter_bytes, parameter_count, training_loss


def write_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n")


def seed_everything(seed, threads):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(threads)
    torch.use_deterministic_algorithms(True)


def linear_macs_per_step(model):
    """Linear-layer multiply-accumulates; excludes activation/gating/dispatch costs."""
    h, d = model.hidden_dim, model.observation_dim
    count = h * h + 3 * h + h * d
    if model.variant == "gru":
        count = 3 * h * (h + 3 + model.contexts) + h * d
    if model.variant == "low_rank":
        count += 2 * h * model.rank
    return count


def train_one(cfg, variant, seed, output):
    seed_everything(seed, cfg.threads)
    model = build_model(cfg, variant)
    training = Dynamics(cfg.environment, seed, "train", cfg.stream_namespace)
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.learning_rate)
    history = []
    start = time.perf_counter()
    for step in range(1, cfg.steps + 1):
        # Identical data order/exposure for all models. Half the batches contain switches.
        batch = training.sample(
            cfg.batch_size,
            cfg.train_horizon,
            switch_every=cfg.switch_every if step % 2 == 0 else None,
        )
        model.train()
        optimizer.zero_grad(set_to_none=True)
        loss = training_loss(model, batch, cfg.grounded_loss_weight)
        if not torch.isfinite(loss):
            raise FloatingPointError(f"nonfinite training loss for {variant} seed {seed}")
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
        log = step == 1 or step % cfg.log_every == 0 or step == cfg.steps
        before = [p.detach().clone() for p in model.parameters()] if log else None
        optimizer.step()
        if log:
            update_norm = (
                sum((p.detach() - old).square().sum() for p, old in zip(model.parameters(), before))
                .sqrt()
                .item()
            )
            row = {
                "step": step,
                "loss": loss.item(),
                "gradient_norm": grad_norm.item(),
                "update_norm": update_norm,
            }
            history.append(row)
            print(
                f"{variant} seed={seed} step={step}/{cfg.steps} loss={loss.item():.6f}", flush=True
            )
    train_seconds = time.perf_counter() - start
    output.mkdir()
    write_json(output / "training.json", history)
    torch.save(
        {
            "state_dict": model.state_dict(),
            "config": cfg.to_dict(),
            "variant": variant,
            "seed": seed,
            "hidden_dim": model.hidden_dim,
        },
        output / "checkpoint.pt",
    )
    metrics = {
        "model": variant,
        "seed": seed,
        "hidden_dim": model.hidden_dim,
        "parameters": parameter_count(model),
        "parameter_bytes": parameter_bytes(model),
        "optimizer_tensor_bytes": sum(
            t.numel() * t.element_size()
            for state in optimizer.state.values()
            for t in state.values()
            if isinstance(t, torch.Tensor)
        ),
        "training_seconds": train_seconds,
        "train_sequences": cfg.steps * cfg.batch_size,
        "train_transitions": cfg.steps * cfg.batch_size * cfg.train_horizon,
        "linear_macs_per_recurrent_step_including_readout": linear_macs_per_step(model),
        "compute_note": "Linear MAC estimate excludes nonlinearities, assimilation, backward pass, "
        "and Python dispatch; 1 MAC conventionally equals 2 FLOPs. Two rollouts "
        "are differentiated per training batch. Timings include those costs.",
    }
    n = cfg.eval_sequences_per_context * len(cfg.environment.angles)
    dev = Dynamics(cfg.environment, seed, "dev", cfg.stream_namespace)
    dev_batch = dev.sample(n, cfg.eval_horizon, balanced=True)
    model.eval()
    with torch.no_grad():
        pred, _ = model.rollout(dev_batch.observations[:, 0], dev_batch.actions, dev_batch.contexts)
    metrics["development"] = prediction_metrics(pred, dev_batch.observations[:, 1:])
    evaluation = Dynamics(cfg.environment, seed, "test", cfg.stream_namespace)
    steady = evaluation.sample(n, cfg.eval_horizon, balanced=True)
    switching = evaluation.sample(n, cfg.eval_horizon, switch_every=cfg.switch_every, balanced=True)
    metrics["steady"], steady_artifact = evaluate(
        model, steady, cfg, evaluation.encoder, seed + 991
    )
    metrics["switching"], switch_artifact = evaluate(
        model, switching, cfg, evaluation.encoder, seed + 991
    )
    stability = Dynamics(cfg.environment, seed, "stability", cfg.stream_namespace).sample(
        n, cfg.stability_horizon, switch_every=cfg.switch_every, balanced=True
    )
    with torch.no_grad():
        long_pred, long_hidden = model.rollout(
            stability.observations[:, 0], stability.actions, stability.contexts
        )
    metrics["long_horizon"] = {
        **prediction_metrics(long_pred, stability.observations[:, 1:]),
        **hidden_stability(long_hidden, cfg.hidden_bound),
    }
    metrics["stored_evaluation_tensor_bytes"] = sum(
        t.numel() * t.element_size()
        for artifact in (steady_artifact, switch_artifact)
        for t in artifact.values()
    )
    control_artifacts = {}
    if cfg.controls_evaluation:
        from soam.evaluation.controls import evaluate_controls, readiness

        metrics["controls"], control_artifacts = evaluate_controls(model, cfg, seed)
        metrics["controls_readiness"] = readiness(metrics["controls"])
        metrics["switch_semantics"] = (
            "predicted-feature handoff with hidden reinitialization; no real sensory reset"
            if variant == "independent"
            else "carry hidden activity without reset"
        )
        metrics["stored_evaluation_tensor_bytes"] += sum(
            t.numel() * t.element_size() for t in control_artifacts.values()
        )
    write_json(output / "metrics.json", metrics)
    plot_run(
        output / "diagnostics.png",
        history,
        steady_artifact,
        switch_artifact,
        metrics,
        evaluation.encoder,
    )
    np.savez_compressed(
        output / "trajectories.npz",
        **{key: tensor.numpy() for key, tensor in control_artifacts.items()},
        **{
            f"{label}_{key}": tensor.numpy()
            for label, artifact in (("steady", steady_artifact), ("switching", switch_artifact))
            for key, tensor in artifact.items()
        },
    )
    return metrics


def run(cfg, output, repo=None):
    cfg.validate()
    output = Path(output)
    # Refuse to mix/overwrite experiments or silently resume partial results.
    output.mkdir(parents=True, exist_ok=False)
    repo = Path(repo) if repo else Path(__file__).resolve().parents[2]
    write_json(output / "config.json", cfg.to_dict())
    write_json(output / "provenance.json", capture(repo, cfg))
    status = {"status": "running", "started_at": datetime.now(UTC).isoformat()}
    write_json(output / "status.json", status)
    rows, trials = [], []
    started = time.monotonic()
    try:
        for variant in cfg.models:
            for seed in cfg.seeds:
                if cfg.controls_evaluation and time.monotonic() - started > 1200:
                    raise TimeoutError("20-minute controls execution limit exceeded")
                trial = {
                    "model": variant,
                    "seed": seed,
                    "status": "running",
                    "started_at": datetime.now(UTC).isoformat(),
                }
                trials.append(trial)
                write_json(output / "trials.json", trials)
                try:
                    rows.append(train_one(cfg, variant, seed, output / f"{variant}-seed{seed}"))
                except Exception as error:
                    trial.update(status="failed", error=f"{type(error).__name__}: {error}")
                    raise
                else:
                    trial["status"] = "complete"
                finally:
                    trial["finished_at"] = datetime.now(UTC).isoformat()
                    write_json(output / "trials.json", trials)
        write_json(output / "results.json", rows)
        status["status"] = "complete"
    except Exception as error:
        status.update(status="failed", error=f"{type(error).__name__}: {error}")
        raise
    finally:
        status["finished_at"] = datetime.now(UTC).isoformat()
        write_json(output / "status.json", status)
    from soam.evaluation.compare import compare

    compare([output], output / "comparison.md")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--seeds", type=int, nargs="+", help="Explicit override saved in resolved config"
    )
    args = parser.parse_args()
    cfg = Config.load(args.config)
    if args.seeds:
        cfg = replace(cfg, seeds=tuple(args.seeds)).validate()
    run(cfg, args.output)


if __name__ == "__main__":
    main()
