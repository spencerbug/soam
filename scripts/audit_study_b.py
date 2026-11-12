"""Post-execution evidence audit. No fitting, model selection or new experiments."""

import hashlib
import json
import resource
import sys
import time
from pathlib import Path

import numpy as np
import torch

from soam.temporal.data import CONDITIONS, SCHEDULES, generate, input_hash, training_data
from soam.temporal.models import make
from soam.temporal.runner import digest, dump, size, source_identity
from soam.temporal.statistics import interval


@torch.no_grad()
def filter_calibration(output, receipt, roots):
    """Post hoc requested uncertainty diagnostic, never used for selection or the gate."""
    results = {}
    for root in roots:
        model = make("FILTER2", 0)
        path = (
            output
            / "confirmation"
            / str(root)
            / "FILTER2"
            / str(receipt["selection"]["FILTER2"]["setting"])
            / "checkpoint.pt"
        )
        model.load_state_dict(torch.load(path, weights_only=True))
        rows = {}
        for metadata in (False, True):
            for condition in CONDITIONS:
                for schedule in SCHEDULES:
                    b = generate("confirmation", root, condition=condition, schedule=schedule)
                    ev = b.evidence
                    h = model.initialize(ev.observed[0], ev.mask[0])
                    maha, nll = [], []
                    for t in range(len(ev.actions)):
                        previous = h
                        prior, _ = model.predict(h, ev.actions[t], ev.roles[t])
                        # The current observation/target has not entered prediction.
                        target_coordinates = (b.target[t + 1] - model.mean) @ model.P
                        error = (prior[:, :2] - target_coordinates).double()
                        covariance = prior[:, 2:].reshape(-1, 2, 2).double()
                        md = (
                            error[:, None] @ torch.linalg.solve(covariance, error[..., None])
                        ).flatten()
                        maha.append(md)
                        nll.append(
                            0.5
                            * (
                                md
                                + torch.linalg.slogdet(covariance).logabsdet
                                + 2 * np.log(2 * np.pi)
                            )
                        )
                        h, _ = model.correct(
                            prior,
                            previous,
                            ev.actions[t],
                            ev.roles[t],
                            ev.observed[t + 1],
                            ev.mask[t + 1],
                            ev.noise_sd[t + 1],
                            metadata=metadata,
                        )
                    md = torch.stack(maha)
                    rows[f"{'metadata' if metadata else 'fixed_noise'}/{condition}/{schedule}"] = {
                        "mean_mahalanobis_squared": md.mean().item(),
                        "coverage90": (md <= 4.605170186).double().mean().item(),
                        "coverage95": (md <= 5.991464547).double().mean().item(),
                        "gaussian_nll": torch.stack(nll).mean().item(),
                    }
        results[str(root)] = rows
    intervals = {
        key: {
            metric: interval([results[str(r)][key][metric] for r in roots])
            for metric in next(iter(results.values()))[key]
        }
        for key in next(iter(results.values()))
    }
    return {
        "classification": "Post hoc descriptive calibration requested for the modeled covariance; not used for tuning, primary inference or architecture selection. Nominal 2D Gaussian ellipse coverage is tested in the learned sensory basis, not simulator coordinates.",
        "roots": results,
        "intervals": intervals,
    }


def main():
    start_cpu, start_wall = time.process_time(), time.monotonic()
    torch.set_num_threads(1)
    root = Path(__file__).resolve().parents[1]
    output = root / "runs/study-b-v1"
    dest = root / "reports/study-b"
    receipt = json.loads((output / "confirmation-receipt.json").read_text())
    assert receipt["source"] == source_identity()["aggregate"]
    manifest = json.loads((output / "manifest.json").read_text())
    provenance = {}
    reduction = []
    all_evals = {name: [] for name in manifest["candidates"]}
    diags = {name: [] for name in manifest["candidates"]}
    for r in manifest["confirmation_roots"]:
        training = training_data(r)
        train_hash = input_hash(training)
        exposure = {
            "episodes": len(training) * 8,
            "supervisory_observations": len(training) * 8 * 17,
            "sensory_events": sum(int(b.evidence.mask.any(-1).sum()) for b in training),
            "feature_values": sum(int(b.evidence.mask.sum()) for b in training),
        }
        del training
        eval_hashes = {}
        for condition in CONDITIONS:
            for schedule in SCHEDULES:
                batch = generate("confirmation", r, condition=condition, schedule=schedule)
                eval_hashes[condition + "/" + schedule] = input_hash([batch])
        provenance[str(r)] = {
            "training_hash": train_hash,
            "evaluation_hashes": eval_hashes,
            "exposure": exposure,
        }
        for name in manifest["candidates"]:
            d = output / "confirmation" / str(r) / name / str(receipt["selection"][name]["setting"])
            fit = json.loads((d / "fit.json").read_text())
            assert fit["input_hash"] == train_hash
            e = json.loads((d / "evaluation.json").read_text())
            all_evals[name].append(e)
            diags[name].append(json.loads((d / "diagnostics.json").read_text()))
            reduced = {}
            with np.load(d / "errors.npz") as arrays:
                for c in CONDITIONS:
                    reduced[c] = np.mean(
                        [
                            arrays[f"{c}__{s}__prior"].astype(np.float64).mean()
                            for s in SCHEDULES
                            if s != "initial"
                        ]
                    )
                reduced["J"] = np.mean(
                    [
                        arrays[f"{c}__{s}__prior"].astype(np.float64).mean()
                        for c in ("partial", "missing", "noise")
                        for s in ("every2", "every4", "every8", "irregular")
                    ]
                )
                for horizon in (8, 32):
                    reduced[f"free{horizon}"] = (
                        arrays["partial__initial__prior"][:horizon].astype(np.float64).mean()
                    )
            for key, value in reduced.items():
                expected = e["headline"][key]
                assert abs(value - expected) < 1e-7, (name, r, key, value, expected)
                reduction.append(
                    {
                        "model": name,
                        "root": r,
                        "metric": key,
                        "recomputed": float(value),
                        "recorded": expected,
                    }
                )
    dump(dest / "data-provenance.json", provenance)
    dump(dest / "independent-reduction.json", reduction)
    # Descriptive mechanistic summaries use the prespecified every-four/partial cells.
    mechanisms = {}
    for name in manifest["candidates"]:
        mechanism = {}
        for c in CONDITIONS:
            rows = [e["rows"][c + "/every1"] for e in all_evals[name]]
            for key in ("gamma_curve", "beta_curve"):
                mechanism[c + "/" + key] = {
                    label: interval([float(np.mean(v[key][lo:hi])) for v in rows])
                    for label, lo, hi in [("pre", 0, 23), ("event", 23, 31), ("after", 31, 48)]
                }
        mechanisms[name] = mechanism
    dump(dest / "gain-summaries.json", mechanisms)
    settle = {}
    for name in ("SET32", "REP32", "MIXC32"):
        values = [d["fixed4"]["rows"]["partial/every4"] for d in diags[name]]
        settle[name] = {
            "initial_reconstruction_by_iteration": [
                interval([v["inner_curve"][0][k] for v in values]) for k in range(5)
            ],
            "initial_cue_output_variance_by_iteration": [
                interval([v["initial_cue_output_variance_by_iteration"][k] for v in values])
                for k in range(5)
            ],
        }
    dump(dest / "cue-retention.json", settle)
    recovery = {}
    for name, es in all_evals.items():
        recovery[name] = {
            c: {
                key: interval([e["rows"][c + "/every4"][key] for e in es])
                for key in ("recovery_steps", "recovery_censored_fraction")
            }
            for c in ("corrupt", "contradict", "change", "gap")
        }
    dump(dest / "recovery.json", recovery)
    compare = {}
    for key in ("J", "noise", "corrupt", "change", "free32"):
        compare[key] = interval(
            [
                d["supplied_noise"]["headline"][key] - e["headline"][key]
                for d, e in zip(diags["FILTER2"], all_evals["FILTER2"], strict=True)
            ]
        )
    dump(dest / "filter-metadata-comparison.json", compare)
    dump(
        dest / "filter-calibration.json",
        filter_calibration(output, receipt, manifest["confirmation_roots"]),
    )
    resources = json.loads((dest / "resources.json").read_text())
    states = {
        name: {
            "persistent_bytes_allocated": r["persistent_bytes"],
            "recurrent_state_floats": r["state_floats"],
            "prior_and_previous_workspace_floats": 2 * r["state_floats"],
            "current_evidence_values": 30,
            "prediction_and_residual_values": 24,
            "gain_values": 2,
            "logical_state_and_input_workspace_slots": 3 * r["state_floats"] + 56,
            "note": "Masks occupy 12 of the evidence slots. Count excludes ephemeral affine intermediates, evaluator histories, training autograd/optimizer and solve workspace; peak RSS includes process allocations.",
        }
        for name, r in resources.items()
    }
    dump(dest / "active-state-accounting.json", states)
    summary = {
        "source": receipt["source"],
        "receipt": receipt["sha256"],
        "roots": len(provenance),
        "independently_reduced_metrics": len(reduction),
        "all_training_hashes_match": True,
        "all_headlines_match": True,
        "audit_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "data_provenance_sha256": digest(provenance),
    }
    dump(dest / "extended-audit.json", summary)
    row = {
        "phase": "post-report-audit",
        "status": "complete",
        "error": None,
        "cpu_seconds": time.process_time() - start_cpu,
        "wall_seconds": time.monotonic() - start_wall,
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        * (1 if sys.platform == "darwin" else 1024),
        "cumulative_artifact_bytes": size(output) + size(dest),
    }
    ledger = json.loads((output / "ledger.json").read_text())
    ledger.append(row)
    dump(output / "ledger.json", ledger)
    assert sum(v["cpu_seconds"] for v in ledger) < manifest["cpu_seconds"]
    assert sum(v["wall_seconds"] for v in ledger) < manifest["wall_seconds"]
    assert row["cumulative_artifact_bytes"] < manifest["artifact_bytes"]
    assert row["peak_rss_bytes"] < manifest["rss_bytes"]
    print(json.dumps({**summary, "resources": row}), flush=True)


if __name__ == "__main__":
    main()
