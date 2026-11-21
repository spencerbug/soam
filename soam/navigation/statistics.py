"""Frozen E0 endpoint family; independent paired roots, never timestep bootstrap."""

import numpy as np

from soam.temporal.statistics import interval


def classify(intervals, endpoints):
    checks = {}
    for key, rule in endpoints.items():
        ci = intervals.get(key)
        if ci is None:
            checks[key] = "unavailable"
        elif ci["width"] > rule["width"]:
            checks[key] = "imprecise"
        else:
            low, high = rule["min"], rule["max"]
            inside = (low is None or ci["lo"] >= low) and (high is None or ci["hi"] <= high)
            outside = (low is not None and ci["hi"] < low) or (high is not None and ci["lo"] > high)
            checks[key] = "pass" if inside else "negative" if outside else "unresolved"
    outcome = (
        "supported bounded criteria"
        if all(v == "pass" for v in checks.values())
        else (
            "negative configured-model evidence"
            if "negative" in checks.values()
            else "inconclusive"
        )
    )
    return {"outcome": outcome, "criteria": checks}


def summarize(records, config):
    results = {}
    for name in config["models"]:
        rows = [records[f"confirmation/{root}/{name}"] for root in config["confirmation_roots"]]
        adjusted, descriptive = {}, {}
        for metric in config["endpoints"]:
            values = [r["evaluation"]["metrics"][metric] for r in rows]
            if any(v is None for v in values):
                adjusted[metric] = descriptive[metric] = None
                continue
            kwargs = {"resamples": config["bootstrap_resamples"], "seed": config["bootstrap_seed"]}
            adjusted[metric] = interval(values, alpha=0.05 / config["family_size"], **kwargs)
            descriptive[metric] = interval(values, **kwargs)
        results[name] = {
            **classify(adjusted, config["endpoints"]),
            "adjusted": adjusted,
            "descriptive": descriptive,
            "resources": rows[0]["resources"],
            "geometry_issues": {str(r["root"]): r["evaluation"]["geometry_issues"] for r in rows},
        }
    comparisons = {}
    nav = np.array(
        [
            records[f"confirmation/{r}/NAV32"]["evaluation"]["metrics"]["free_nmse"]
            for r in config["confirmation_roots"]
        ]
    )
    for name in config["models"][1:]:
        control = np.array(
            [
                records[f"confirmation/{r}/{name}"]["evaluation"]["metrics"]["free_nmse"]
                for r in config["confirmation_roots"]
            ]
        )
        comparisons[name] = interval(
            nav - control, resamples=config["bootstrap_resamples"], seed=config["bootstrap_seed"]
        )
    return {"models": results, "descriptive_NAV32_minus_control_J": comparisons}
