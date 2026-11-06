"""Frozen E1 inference and decision rules; no adaptive trials or seed extension."""

import numpy as np

from soam.shared.data import stream
from soam.shared.models import manifest


def paired_intervals(values, *, family_size):
    """Rows are the ten independent roots, never episodes or timesteps."""
    values = np.asarray(values, dtype=np.float64)
    if values.ndim != 2 or values.shape[0] != 10 or not np.isfinite(values).all():
        raise ValueError("finite contrasts for exactly ten paired roots required")
    if family_size not in (1, 6, 7) or values.shape[1] != family_size:
        raise ValueError("frozen inference family dimensions required")
    seed = stream("inference", 8675309, 0, "inference-resampling")
    rng = np.random.Generator(np.random.PCG64(seed))
    indices = rng.integers(0, 10, size=(10000, 10))
    samples = values[indices].mean(1)
    tail = 0.05 / (2 * family_size)
    adjusted = np.quantile(samples, [tail, 1 - tail], axis=0, method="linear")
    ordinary = np.quantile(samples, [0.025, 0.975], axis=0, method="linear")
    return {
        "mean": values.mean(0).tolist(),
        "lower": adjusted[0].tolist(),
        "upper": adjusted[1].tolist(),
        "width": (adjusted[1] - adjusted[0]).tolist(),
        "ordinary_lower": ordinary[0].tolist(),
        "ordinary_upper": ordinary[1].tolist(),
        "root_count": 10,
        "replicates": 10000,
        "seed": seed,
        "resampling_unit": "paired_confirmation_root",
    }


def choose_configs(development):
    """Two config means per family, each over exactly three development roots.

    Input shape [config, root, (transition free8, recall endpoint)]. Never accepts
    confirmation records. Recall affects the competence screen, not selection.
    """
    protocol = manifest()
    selected, scores = {}, {}
    for row in protocol["models"]:
        name = row["id"]
        values = np.asarray(development[name], dtype=np.float64)
        if values.shape != (2, 3, 2) or not np.isfinite(values).all():
            raise ValueError("complete finite development-only inventory required")
        means = values.mean(1)
        index = 1 if means[1, 0] < means[0, 0] - 1e-12 else 0
        selected[name] = index
        scores[name] = means[index].tolist()
    refs = protocol["comparisons"]["required_references"]
    best = refs[0]
    for name in refs[1:]:
        if scores[name][0] < scores[best][0] - 1e-12:
            best = name
    best_gru = "G32" if scores["G32"][0] < scores["G28"][0] - 1e-12 else "G28"
    floor = any(scores[name][0] <= 1e-6 for name in refs)
    competent = scores[best_gru][0] <= 0.15 and scores[best_gru][1] <= 0.03
    return {
        "selected_configs": selected,
        "selected_means": scores,
        "primary_reference": best,
        "best_selected_gru": best_gru,
        "floor_limited": floor,
        "gru_competent": competent,
        "confirmation_allowed": competent and not floor,
    }


def classify(
    *,
    utility,
    causal,
    candidate_recall,
    candidate_transition,
    invalid=False,
    incomplete=False,
    floor_limited=False,
    candidate_finite=True,
    references_finite=True,
):
    """Apply the frozen precedence to already aggregated root contrasts.

    Utility order: five relative gains, S32 final-minus-pre recall, then
    S32-minus-D25 recall. Causal order: targeted recall/transition increases,
    full-minus-readout recall/transition, action-shift and zero-A relative increases.
    Upstream completeness validation must set invalid for missing required rows.
    """
    if invalid:
        return {"outcome": "invalid_execution_or_comparison"}
    if incomplete or floor_limited or not references_finite or not candidate_finite:
        return {
            "outcome": "incomplete_or_inconclusive_or_candidate_instability",
            "candidate_instability": not candidate_finite,
            "floor_limited": floor_limited,
            "incomplete": incomplete,
            "reference_instability": not references_finite,
        }
    try:
        u = paired_intervals(utility, family_size=7)
        c = paired_intervals(causal, family_size=6)
        recall = np.asarray(candidate_recall, dtype=np.float64)
        transition = np.asarray(candidate_transition, dtype=np.float64)
        if (
            recall.shape != (10,)
            or transition.shape != (10,)
            or not np.isfinite([recall, transition]).all()
        ):
            raise ValueError("invalid candidate root inventory")
    except ValueError as error:
        return {"outcome": "invalid_execution_or_comparison", "error": str(error)}
    um, ul, uu, uw = (np.asarray(u[k]) for k in ("mean", "lower", "upper", "width"))
    cm, cl, cu, cw = (np.asarray(c[k]) for k in ("mean", "lower", "upper", "width"))
    minima = np.array([0.005, 0.005, 0.002, 0.002, 0.1, 0.1])
    caps = np.array([0.02, 0.02, 0.02, 0.02, 0.2, 0.2])
    causal_pass = (cm >= minima) & (cl > 0) & (cw <= caps)
    causal_precise_failure = (cu < minima) & (cw <= caps)
    guardrail_pass = (uu[5:] <= 0.005).all()
    guardrail_failure = (ul[5:] > 0.005).any() or recall.mean() > 0.02
    utility_pass = ((um[:5] >= 0.1) & (ul[:5] > 0) & (uw[:5] <= 0.2)).all()
    no_benefit = ((uu[:5] < 0.1) & (uw[:5] <= 0.2)).any()
    if guardrail_failure:
        outcome = "recall_interference_or_failure"
    elif not guardrail_pass:
        outcome = "inconclusive_or_mechanism_unresolved"
    elif recall.mean() <= 0.02 and (transition.mean() > 0.1 or causal_precise_failure[4:].any()):
        outcome = "directional_failure"
    elif utility_pass and guardrail_pass and transition.mean() <= 0.1 and causal_pass.all():
        outcome = "useful_sharing_supported"
    elif no_benefit:
        outcome = "precise_no_practical_benefit"
    else:
        outcome = "inconclusive_or_mechanism_unresolved"
    return {
        "outcome": outcome,
        "utility": u,
        "causal": c,
        "guardrail_pass": bool(guardrail_pass),
        "utility_pass": bool(utility_pass),
        "causal_pass": causal_pass.tolist(),
        "causal_precise_failure": causal_precise_failure.tolist(),
        "absolute_recall_mean": recall.mean().item(),
        "absolute_transition_mean": transition.mean().item(),
    }
