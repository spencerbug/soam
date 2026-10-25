"""Finite engineering demonstration, not an H2 acquisition benchmark or a sweep."""

import argparse
import hashlib
import json
from pathlib import Path

import torch

from soam.config import Config
from soam.environments.dynamics import Dynamics
from soam.evaluation.metrics import hidden_stability, prediction_metrics
from soam.evaluation.provenance import capture
from soam.evaluation.runner import seed_everything, write_json
from soam.plasticity import GroundedEvidence, LocalMemory, WriteConfig, encoder_identity


def measure(snapshot, batches):
    result = {}
    for key, batch in batches.items():
        pred, hidden = snapshot.rollout(batch.observations[:, 0], batch.actions, batch.contexts)
        grounded, _ = snapshot.rollout(
            batch.observations[:, 0], batch.actions, batch.contexts, observations=batch.observations
        )
        target = batch.observations[:, 1:]
        result[key] = {
            "free": prediction_metrics(pred, target),
            "grounded": prediction_metrics(grounded, target),
            "stability": hidden_stability(hidden, 1.5),
            "per_start_context": {
                str(c): prediction_metrics(
                    pred[batch.contexts[:, 0] == c], target[batch.contexts[:, 0] == c]
                )
                for c in range(3)
            },
        }
    return result


def run(config_path, output):
    cfg = json.loads(config_path.read_text())
    repo = Path(__file__).resolve().parents[1]
    output.mkdir(parents=True, exist_ok=False)
    writer_cfg = WriteConfig(**cfg["writer"]).validate()
    seed_everything(11, 1)
    provenance = capture(repo, Config())
    provenance["config_sha256"] = hashlib.sha256(
        json.dumps(cfg, sort_keys=True).encode()
    ).hexdigest()
    provenance["contract_sha256"] = hashlib.sha256(
        (repo / "soam/plasticity/README.md").read_bytes()
    ).hexdigest()
    provenance["purpose"] = "engineering contract check; not hypothesis evidence"
    write_json(output / "config.json", cfg)
    write_json(output / "provenance.json", provenance)
    write_json(output / "status.json", {"status": "running"})
    rows = []
    try:
        for seed in cfg["seeds"]:
            seed_everything(seed, 1)
            memory = LocalMemory.from_manifest(repo, seed, writer_cfg)
            before = memory.predictor()
            env = Dynamics(Config().environment, seed, "train", cfg["adaptation_namespace"])
            batch = env.sample(3, cfg["history_length"], balanced=True)
            evidence = GroundedEvidence(
                f"seed{seed}-context0-final-transition",
                f"simulator:seed{seed}:train:namespace{cfg['adaptation_namespace']}",
                "episode0",
                0,
                "adaptation",
                "simulator",
                batch.observations[0],
                batch.actions[0],
                batch.contexts[0],
                encoder_identity(env.encoder),
            )
            batches = {}
            for h in cfg["evaluation_horizons"]:
                for label in ("steady", "irregular"):
                    env = Dynamics(
                        Config().environment,
                        seed,
                        "dev",
                        cfg["evaluation_namespace"] + h * 10 + (label == "irregular"),
                    )
                    batches[f"{label}-{h}"] = env.sample(
                        3 * cfg["sequences_per_context"],
                        h,
                        balanced=True,
                        irregular=label == "irregular",
                    )
            metrics_before = measure(before, batches)
            proposal = memory.propose(evidence)
            assert memory.identity == before.identity
            receipt = memory.commit(proposal)
            after = memory.predictor()
            metrics_after = measure(after, batches)
            folder = output / f"low_rank-seed{seed}"
            folder.mkdir()
            files = {}
            for name, snapshot in (("before", before), ("after", after)):
                path = folder / f"{name}.pt"
                torch.save(
                    {
                        "state_dict": snapshot.state_dict(),
                        "identity": snapshot.identity,
                        "base_checkpoint_sha256": receipt["source_checkpoint_sha256"],
                    },
                    path,
                )
                files[name] = {
                    "path": str(path.relative_to(output)),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "state_identity": snapshot.identity,
                }
            torch.save(
                {
                    "observations": evidence.observations,
                    "actions": evidence.actions,
                    "contexts": evidence.contexts,
                },
                folder / "evidence.pt",
            )
            rollback = memory.rollback(receipt["receipt_id"])
            reverted = memory.predictor()
            assert reverted.identity == before.identity
            assert all(
                torch.equal(v, reverted.state_dict()[k]) for k, v in before.state_dict().items()
            )
            assert measure(reverted, batches) == metrics_before
            row = {
                "seed": seed,
                "proposal": proposal.audit,
                "commit": receipt,
                "rollback": rollback,
                "checkpoint_files": files,
                "before": metrics_before,
                "after": metrics_after,
                "exact_rollback_parameters_and_predictions": True,
            }
            write_json(folder / "audit.json", row)
            rows.append(row)
            print(
                seed,
                "conditional MSE",
                receipt["mse_before"],
                "->",
                receipt["mse_after"],
                "norm",
                receipt["applied_update_norm"],
                "rank",
                receipt["proposal_rank"],
                "rollback exact",
                flush=True,
            )
        write_json(output / "results.json", rows)
    except Exception as error:
        write_json(
            output / "status.json",
            {
                "status": "failed",
                "error": f"{type(error).__name__}: {error}",
                "completed_seeds": [r["seed"] for r in rows],
            },
        )
        raise
    write_json(output / "status.json", {"status": "complete", "completed_seeds": cfg["seeds"]})
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/local-write-contract.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.config, args.output)
