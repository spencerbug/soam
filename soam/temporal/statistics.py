"""Paired independent-root inference; never resample timesteps."""

import numpy as np


def interval(values, *, alpha=0.05, resamples=20000, seed=12203):
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or len(values) < 2 or not np.isfinite(values).all():
        raise ValueError("Finite independent-root values required")
    rng = np.random.default_rng(seed)
    means = values[rng.integers(len(values), size=(resamples, len(values)))].mean(1)
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return {
        "mean": float(values.mean()),
        "lo": float(lo),
        "hi": float(hi),
        "width": float(hi - lo),
        "n": len(values),
    }


def primary_decision(headlines, unresolved=()):
    comparisons = {}
    gains, guards = [], []
    ga = headlines["GA32"]
    for control in ("PC32", "MIX32"):
        ref = headlines[control]
        g = (np.array([v["J"] for v in ref]) - np.array([v["J"] for v in ga])) / np.maximum(
            [v["J"] for v in ref], 1e-6
        )
        ci = interval(g, alpha=0.05 / 10)
        comparisons[control + "/gain"] = ci
        gains.append(ci)
        for key in ("clean", "corrupt", "change", "free32"):
            d = np.array([v[key] for v in ga]) - np.array([v[key] for v in ref])
            ci = interval(d, alpha=0.05 / 10)
            comparisons[control + "/" + key] = ci
            guards.append(ci)
    competent = np.mean([v["J"] for v in ga]) <= 0.15
    supported = all(v["mean"] >= 0.1 and v["lo"] > 0 and v["width"] <= 0.4 for v in gains) and all(
        v["hi"] <= 0.01 for v in guards
    )
    precise_negative = any(v["hi"] < 0.1 and v["width"] <= 0.4 for v in gains)
    harmful = any(v["lo"] > 0.01 for v in guards)
    if unresolved or not competent or any(v["width"] > 0.4 for v in gains):
        outcome = "inconclusive"
    elif supported:
        outcome = "supported"
    elif harmful:
        outcome = "tradeoff"
    elif precise_negative:
        outcome = "negative practical advantage"
    else:
        outcome = "inconclusive"
    return {
        "outcome": outcome,
        "comparisons": comparisons,
        "competent": bool(competent),
        "optimization_unresolved": list(unresolved),
    }
