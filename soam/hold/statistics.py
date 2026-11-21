"""One confirmatory NAV32 family, with mandatory descriptive control results."""

import numpy as np

from soam.temporal.statistics import interval


def rules(config):
    return {
        **{"absolute/" + k: v for k, v in config["endpoints"].items()},
        "gain/stationary_deg": config["gain"],
        **{"degradation/" + k: v for k, v in config["degradation"].items()},
    }


def classify(intervals, config):
    status = {}
    for key, rule in rules(config).items():
        ci = intervals[key]
        if ci is None:
            status[key] = "unavailable"
        elif ci["width"] > rule["width"]:
            status[key] = "imprecise"
        else:
            low, high = rule["min"], rule["max"]
            passed = (low is None or ci["lo"] >= low) and (high is None or ci["hi"] <= high)
            failed = (low is not None and ci["hi"] < low) or (high is not None and ci["lo"] > high)
            status[key] = "pass" if passed else "negative" if failed else "unresolved"
    if all(v == "pass" for v in status.values()):
        outcome = "supported bounded fix"
    elif any(v == "negative" and k.startswith("degradation/") for k, v in status.items()):
        outcome = "tradeoff"
    elif "negative" in status.values():
        outcome = "negative declared joint fix"
    else:
        outcome = "inconclusive"
    return {"outcome": outcome, "criteria": status}


def summarize(records, config):
    raw, descriptive, contrasts = {}, {}, {}
    kwargs = {"seed": config["bootstrap_seed"], "resamples": config["bootstrap_resamples"]}
    for name in config["models"]:
        arms = ["REFERENCE"] if name == "PCA2" else config["arms"]
        for arm in arms:
            key = name + "/" + arm
            rows = [
                records[f"confirmation/{r}/{key}"]["evaluation"]["metrics"]
                for r in config["confirmation_roots"]
            ]
            raw[key] = {metric: [r[metric] for r in rows] for metric in config["endpoints"]}
            descriptive[key] = {
                metric: interval(values, **kwargs) if all(v is not None for v in values) else None
                for metric, values in raw[key].items()
            }
        if name != "PCA2":
            contrasts[name] = {}
            for metric in config["endpoints"]:
                short, long = raw[name + "/SHORT24"][metric], raw[name + "/LONG128"][metric]
                values = None if None in short or None in long else np.array(long) - short
                contrasts[name][metric] = interval(values, **kwargs) if values is not None else None
    values = {"absolute/" + k: v for k, v in raw["NAV32/LONG128"].items()}
    short, long = raw["NAV32/SHORT24"], raw["NAV32/LONG128"]
    values["gain/stationary_deg"] = np.array(short["stationary_deg"]) - long["stationary_deg"]
    for key in config["degradation"]:
        values["degradation/" + key] = (
            None if None in short[key] or None in long[key] else np.array(long[key]) - short[key]
        )
    adjusted = {
        k: interval(v, alpha=0.05 / config["family_size"], **kwargs)
        if v is not None and all(x is not None for x in v)
        else None
        for k, v in values.items()
    }
    return {
        **classify(adjusted, config),
        "adjusted_NAV32": adjusted,
        "descriptive_95": descriptive,
        "descriptive_long_minus_short": contrasts,
        "raw_root_values": raw,
    }
