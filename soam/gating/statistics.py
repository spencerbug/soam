"""Prespecified paired-root inference; diagnostics remain descriptive."""

import numpy as np


def summarize(records, manifest, receipt):
    roots = manifest["confirmation_roots"]
    ids = list(manifest["variants"])
    by = {(r["root"], r["model"]): r for r in records}
    if set(by) != {(r, m) for r in roots for m in ids}:
        raise ValueError("incomplete confirmation inventory")
    rng = np.random.default_rng(manifest["bootstrap"]["seed"])
    draws = rng.integers(len(roots), size=(manifest["bootstrap"]["resamples"], len(roots)))
    tail = 0.05 / (2 * manifest["bootstrap"]["family_size"])

    def interval(values, adjusted=False):
        values = np.asarray(values, dtype=float)
        samples = values[draws].mean(1)
        q = tail if adjusted else 0.025
        lo, hi = np.quantile(samples, [q, 1 - q], method="linear")
        return {
            "mean": float(values.mean()),
            "lo": float(lo),
            "hi": float(hi),
            "width": float(hi - lo),
            "roots": values.tolist(),
        }

    metrics = ("J", "recall", "free8", "free32", "grounded32")
    models = {
        m: {k: interval([by[r, m]["metrics"][k] for r in roots]) for k in metrics} for m in ids
    }
    diagnostics = {
        m: {
            k: interval([by[r, m]["diagnostics"][k] for r in roots])
            for k in by[roots[0], m]["diagnostics"]
        }
        for m in ids
    }
    contrasts = {}
    c = manifest["criteria"]
    for other in ("FU38", "R52", "R55"):
        full = np.array([by[r, "G32"]["metrics"]["J"] for r in roots])
        control = np.array([by[r, other]["metrics"]["J"] for r in roots])
        contrasts[f"gain_{other}"] = {
            "adjusted": interval((control - full) / np.maximum(control, 1e-6), True),
            "ordinary": interval((control - full) / np.maximum(control, 1e-6)),
        }
        for metric in ("recall", "free8", "free32", "grounded32"):
            values = [
                by[r, "G32"]["metrics"][metric] - by[r, other]["metrics"][metric] for r in roots
            ]
            contrasts[f"{metric}_minus_{other}"] = {
                "adjusted": interval(values, True),
                "ordinary": interval(values),
            }
    secondary = {}
    for a, b in [
        ("G32", "FU32"),
        ("G32", "FR32"),
        ("G32", "FB32"),
        ("GS32", "S32"),
        ("FR32", "R32"),
        ("L2", "L12"),
    ]:
        secondary[f"{a}_minus_{b}"] = {
            k: interval([by[r, a]["metrics"][k] - by[r, b]["metrics"][k] for r in roots])
            for k in metrics
        }
    resources = {m: by[roots[0], m]["costs"] for m in ids}
    for m in ids:
        resources[m] = {
            **resources[m],
            "mean_fit_cpu": float(np.mean([by[r, m]["fit_cpu"] for r in roots])),
        }
    ratios = {
        k: resources["G32"][k] / resources["FU38"][k]
        for k in ("parameters", "advance_readout_linear_macs", "mean_fit_cpu")
    }
    precise = all(
        contrasts[f"gain_{m}"]["adjusted"]["width"] <= c["gain_width"]
        for m in ("FU38", "R52", "R55")
    )
    gains = all(
        (v := contrasts[f"gain_{m}"]["adjusted"])["mean"] >= c["gain"] and v["lo"] > 0
        for m in ("FU38", "R52", "R55")
    )
    guardkeys = ("recall", "free8", "free32", "grounded32")
    guards = all(
        contrasts[f"{k}_minus_{m}"]["adjusted"]["hi"] <= c[k + "_margin"]
        for k in guardkeys
        for m in ("FU38", "R52", "R55")
    )
    absolute = (
        models["G32"]["recall"]["mean"] <= c["absolute_recall"]
        and models["G32"]["free8"]["mean"] <= c["absolute_free8"]
    )
    resource_ok = (
        ratios["parameters"] <= c["parameter_ratio"]
        and ratios["advance_readout_linear_macs"] <= c["mac_ratio"]
        and ratios["mean_fit_cpu"] <= c["fit_cpu_ratio"]
    )
    competence = receipt["competence_pass"] and not receipt["optimization_unresolved"]
    negative = any(
        (v := contrasts[f"gain_{m}"]["adjusted"])["hi"] < c["gain"]
        and v["width"] <= c["gain_width"]
        for m in ("FU38", "R52", "R55")
    )
    mixed = any(
        any(contrasts[f"{k}_minus_{m}"]["adjusted"]["hi"] < 0 for k in guardkeys)
        and any(contrasts[f"{k}_minus_{m}"]["adjusted"]["lo"] > c[k + "_margin"] for k in guardkeys)
        for m in ("FU38", "R52", "R55")
    )
    if not competence or not resource_ok:
        outcome = "inconclusive"
    elif gains and guards and precise and absolute:
        outcome = "supported"
    elif mixed:
        outcome = "mixed"
    elif negative:
        outcome = "negative"
    else:
        outcome = "inconclusive"
    return {
        "models": models,
        "diagnostics": diagnostics,
        "contrasts": contrasts,
        "secondary": secondary,
        "resources": resources,
        "resource_ratios": ratios,
        "outcome": outcome,
        "checks": {
            "competence_and_optimization": competence,
            "resources": resource_ok,
            "gain_precision": precise,
            "gains": gains,
            "guards": guards,
            "absolute_competence": absolute,
            "negative_practical_gain": negative,
            "mixed_endpoint_evidence": mixed,
        },
        "roots": roots,
    }
