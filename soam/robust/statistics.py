"""Frozen paired-root comparisons; episodes/time are not independent replicates."""

import numpy as np


def interval(values, *, draws, family=1):
    values = np.asarray(values, dtype=float)
    means = values[draws].mean(1)
    alpha = 0.05 / family
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return {
        "mean": float(values.mean()),
        "lo": float(lo),
        "hi": float(hi),
        "width": float(hi - lo),
        "n": len(values),
        "family": family,
    }


def summarize(results, receipt, manifest):
    roots = receipt["confirmation_roots"]
    names = receipt["inventory"]
    draws = np.random.default_rng(manifest["bootstrap_seed"]).integers(
        0, len(roots), (manifest["bootstrap_resamples"], len(roots))
    )
    headlines = {n: [results[str(r)][n]["headline"] for r in roots] for n in names}
    descriptive = {
        n: {metric: interval([x[metric] for x in values], draws=draws) for metric in values[0]}
        for n, values in headlines.items()
    }
    guards = ("J", "change", "clean", "gap", "free32")
    family = 6 * len(receipt["challengers"])
    comparisons = {}
    base = headlines["FILTER2"]
    for name in receipt["challengers"]:
        values = headlines[name]
        gain = [(b["C"] - v["C"]) / max(b["C"], 1e-6) for b, v in zip(base, values, strict=True)]
        contrast = {"gain": interval(gain, draws=draws, family=family)}
        for g in guards:
            contrast[g] = interval(
                [v[g] - b[g] for b, v in zip(base, values, strict=True)], draws=draws, family=family
            )
        means = descriptive[name]
        checks = {
            "gain_mean": contrast["gain"]["mean"] >= manifest["benefit"],
            "gain_positive": contrast["gain"]["lo"] > 0,
            "precision": contrast["gain"]["width"] <= manifest["precision_width"],
            "J_absolute": means["J"]["mean"] <= manifest["J_max"],
            "corrupt_absolute": means["corrupt"]["mean"] <= manifest["corrupt_max"],
            "change_absolute": means["change"]["mean"] <= manifest["change_max"],
            **{g + "_guard": contrast[g]["hi"] <= manifest["guard_margin"] for g in guards},
        }
        outcome = (
            "supported bounded benefit"
            if all(checks.values())
            else "tradeoff"
            if any(contrast[g]["lo"] > manifest["guard_margin"] for g in guards)
            else "precise negative practical gain"
            if contrast["gain"]["hi"] < manifest["benefit"] and checks["precision"]
            else "inconclusive"
        )
        comparisons[name] = {"contrasts": contrast, "checks": checks, "outcome": outcome}
    secondary = {
        n: {
            g: interval(
                [v[g] - b[g] for v, b in zip(headlines[n], headlines["PC16"], strict=True)],
                draws=draws,
            )
            for g in ("J", "C", "corrupt", "change")
        }
        for n in names
        if n != "PC16"
    }
    return {
        "descriptive": descriptive,
        "primary": comparisons,
        "secondary_vs_PC16": secondary,
        "bootstrap_seed": manifest["bootstrap_seed"],
        "resamples": manifest["bootstrap_resamples"],
        "independent_units": "10 independently fitted paired roots",
    }
