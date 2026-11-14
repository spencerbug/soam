"""Post-freeze diagnostics on registered streams; no selection/fitting/changes."""

import hashlib
import json
from pathlib import Path

import numpy as np
import torch

from soam.robust.data import CORRUPTION, INTERMITTENT, generate
from soam.robust.engine import trace
from soam.robust.models import Config, Robust
from soam.robust.runner import MANIFEST, OUT, load_models, receipt_check
from soam.robust.statistics import interval
from soam.temporal.runner import Budget, dump


@torch.no_grad()
def main():
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    m = json.loads(MANIFEST.read_text())
    receipt = receipt_check()
    dest = OUT / "diagnostics"
    dest.mkdir(exist_ok=False)
    budget = Budget(OUT, m, "diagnostics")
    try:
        roots = receipt["confirmation_roots"]
        var = receipt["normalization"]
        names = receipt["inventory"]
        draws = np.random.default_rng(m["bootstrap_seed"]).integers(
            0, len(roots), (m["bootstrap_resamples"], len(roots))
        )
        influence = {}
        ambiguity = {}
        conditioning = {}
        for root in roots:
            base = load_models(OUT / "confirmation" / str(root) / "fits")
            clean = generate("confirmation", root, batch=20, schedule="every4")
            for name in names:
                budget.check()
                model = (
                    base[name]
                    if name in base
                    else Robust(base["FILTER2"], Config(**receipt["configs"][name]))
                )
                rows = {}
                for condition in CORRUPTION:
                    b = generate(
                        "confirmation", root, batch=20, condition=condition, schedule="every4"
                    )
                    actual = trace(model, b.evidence)
                    # Counterfactual correction at the SAME prior/history. Evaluator-only clean
                    # observation is never fed back into the actual trajectory.
                    values = []
                    for t in range(64):
                        label = (
                            (b.evidence.observed[t + 1] - clean.evidence.observed[t + 1]).abs()
                            > 1e-7
                        ).any(-1) & b.evidence.mask[t + 1].any(-1)
                        if not label.any():
                            continue
                        p = actual["state"][t].clone()
                        prev = actual["poststate"][t].clone()
                        corrected, _ = model.correct(
                            p,
                            prev,
                            b.evidence.actions[t],
                            b.evidence.roles[t],
                            clean.evidence.observed[t + 1],
                            b.evidence.mask[t + 1],
                            b.evidence.noise_sd[t + 1],
                        )
                        reference = model.readout(corrected).double()
                        truth = b.target[t + 1].double()
                        real = actual["posterior"][t + 1].double()
                        prior = actual["prior"][t].double()
                        pe = (real - truth).square().mean(-1) / var
                        ce = (reference - truth).square().mean(-1) / var
                        before = (prior - truth).square().mean(-1) / var
                        effect = (real - reference).square().mean(-1) / var
                        for j in label.nonzero().flatten():
                            values.append(
                                [
                                    float(pe[j]),
                                    float(ce[j]),
                                    float(effect[j]),
                                    float(pe[j] < before[j]),
                                    float(pe[j] - ce[j]),
                                ]
                            )
                    x = np.array(values)
                    rows[condition] = {
                        "fault_events": len(x),
                        **{
                            k: float(x[:, i].mean())
                            for i, k in enumerate(
                                (
                                    "posterior_error",
                                    "counterfactual_clean_error",
                                    "corrupted_influence_nmse",
                                    "helpful_fraction",
                                    "excess_posterior_error",
                                )
                            )
                        },
                    }
                influence.setdefault(name, {})[str(root)] = rows
            # Exact evidence identity for all registered T10 schedules; distinct target lower bound.
            checks = []
            lower = []
            for schedule in INTERMITTENT:
                a = generate(
                    "confirmation", root, batch=20, condition="ambiguous", schedule=schedule
                )
                b = generate("confirmation", root, batch=20, condition="change", schedule=schedule)
                checks.append(
                    all(torch.equal(v, vars(b.evidence)[k]) for k, v in vars(a.evidence).items())
                )
                lower.append(
                    float((a.target[1:].double() - b.target[1:].double()).square().mean() / var / 4)
                )
            ambiguity[str(root)] = {
                "evidence_identical": all(checks),
                "equal_prior_pair_minimum_nmse": float(np.mean(lower)),
            }
            # Numerical conditioning of the actually used state precision (baseline prior covariances).
            path = trace(base["FILTER2"], clean.evidence)
            cov = path["state"][..., 2:6].double().reshape(64, 20, 2, 2)
            conditioning[str(root)] = {
                "prior_covariance_condition_max": float(torch.linalg.cond(cov).max()),
                "prior_covariance_eigen_min": float(torch.linalg.eigvalsh(cov).min()),
            }
        influence_ci = {
            n: {
                c: {
                    k: interval([influence[n][str(r)][c][k] for r in roots], draws=draws)
                    for k in influence[n][str(roots[0])][c]
                }
                for c in CORRUPTION
            }
            for n in names
        }
        dump(
            dest / "influence.json",
            {
                "roots": influence,
                "intervals": influence_ci,
                "method": "Same actual prior/history, actual versus clean counterfactual current cue; counterfactual never propagated. Evaluator labels only.",
            },
        )
        checks = {}
        for name in names:
            a = np.load(OUT / "confirmation" / str(roots[0]) / name / "arrays.npz")
            checks[name] = bool(
                np.array_equal(a["change__every4__prediction"], a["ambiguous__every4__prediction"])
            )
        assert all(checks.values()) and all(v["evidence_identical"] for v in ambiguity.values())
        dump(
            dest / "identifiability.json",
            {
                "roots": ambiguity,
                "paired_lower_bound": interval(
                    [ambiguity[str(r)]["equal_prior_pair_minimum_nmse"] for r in roots], draws=draws
                ),
                "all_saved_example_predictions_identical": checks,
                "scope": "Identical evidence, different truths. Excluded from gate; equal-prior midpoint lower bound.",
            },
        )
        dump(dest / "conditioning.json", conditioning)
        # Independent dense measurement-space comparison across a noisy/sparse fixture trajectory.
        fitted = load_models(OUT / "confirmation" / str(roots[0]) / "fits")["FILTER2"]
        from soam.temporal.engine import rollout

        fixture = generate("fixture", 15001, batch=4, condition="noise", schedule="irregular")
        old = rollout(fitted, fixture.evidence)["prior"].double()
        new = rollout(Robust(fitted, Config()), fixture.evidence)["prior"]
        dump(
            dest / "numerical-control.json",
            {
                "max_absolute_prediction_difference": float((old - new).abs().max()),
                "allclose_2e_6": bool(torch.allclose(old, new, atol=2e-6, rtol=2e-5)),
            },
        )
        dump(
            dest / "provenance.json",
            {
                "receipt": receipt["sha256"],
                "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "new_fits": 0,
                "selection_changed": False,
            },
        )
        budget.finish("complete")
    except BaseException as e:
        budget.finish("failed", repr(e))
        raise


if __name__ == "__main__":
    main()
