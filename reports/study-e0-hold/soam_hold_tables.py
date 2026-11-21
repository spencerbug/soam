"""Create readable tables from completed, audited E0-HOLD results."""

import json
from pathlib import Path

repo = Path.cwd()
out = repo / "reports/study-e0-hold"
s = json.loads((out / "summary.json").read_text())
c = json.loads((repo / "docs/protocols/study_e0_hold_v1.json").read_text())
l = json.loads((repo / "runs/study-e0-hold-v1/ledger.json").read_text())


def mean(values):
    return sum(values) / len(values)


def fmt(ci):
    if ci is None:
        return "unavailable"
    return f"{ci['mean']:.6g} [{ci['lo']:.6g}, {ci['hi']:.6g}]"


lines = [
    "# E0-HOLD v1: complete numerical tables",
    "",
    f"Formal NAV32 result: **{s['outcome']}**. All intervals use twenty independent paired roots. The primary family uses alpha=.05/13 per interval; control tables are descriptive 95% intervals.",
    "",
    "## Confirmatory NAV32 family",
    "",
    "| Quantity | Mean [adjusted interval] | Width | Requirement | Status |",
    "| --- | --- | --- | --- | --- |",
]
rules = {
    **{"absolute/" + k: v for k, v in c["endpoints"].items()},
    "gain/stationary_deg": c["gain"],
    **{"degradation/" + k: v for k, v in c["degradation"].items()},
}
for k, rule in rules.items():
    ci = s["adjusted_NAV32"][k]
    limit = (
        ("lower >= " + str(rule["min"]) if rule["min"] is not None else "")
        + (" and " if rule["min"] is not None and rule["max"] is not None else "")
        + ("upper <= " + str(rule["max"]) if rule["max"] is not None else "")
        + f"; width <= {rule['width']}"
    )
    width = f"{ci['width']:.6g}" if ci else "unavailable"
    lines.append(f"| {k} | {fmt(ci)} | {width} | {limit} | {s['criteria'][k]} |")
lines += [
    "",
    "## All model/arm endpoints (descriptive 95%)",
    "",
    "| Model/arm | " + " | ".join(c["endpoints"]) + " |",
    "| --- | " + " | ".join(["---"] * len(c["endpoints"])) + " |",
]
for name in c["models"]:
    for arm in ["REFERENCE"] if name == "PCA2" else c["arms"]:
        key = name + "/" + arm
        lines.append(
            "| "
            + key
            + " | "
            + " | ".join(fmt(s["descriptive_95"][key][m]) for m in c["endpoints"])
            + " |"
        )
lines += [
    "",
    "## Paired LONG128 minus SHORT24 (descriptive 95%)",
    "",
    "| Model | " + " | ".join(c["endpoints"]) + " |",
    "| --- | " + " | ".join(["---"] * len(c["endpoints"])) + " |",
]
for name in c["models"][:-1]:
    lines.append(
        "| "
        + name
        + " | "
        + " | ".join(fmt(s["descriptive_long_minus_short"][name][m]) for m in c["endpoints"])
        + " |"
    )
lines += [
    "",
    "## Direction/speed diagnostics (root means; no confirmatory claim)",
    "",
    "| Cell | Interpolation | Extrapolation | Positive constant action | Negative constant action |",
    "| --- | --- | --- | --- | --- |",
]
resource = [
    "",
    "## Resource and exposure means per fitted root",
    "",
    "| Cell | Scalars / bytes | Active floats | Fit CPU s | Evaluation CPU s | Extra stationary transitions | Final 100 loss | Previous 100 loss |",
    "| --- | --- | --- | --- | --- | --- | --- | --- |",
]
for name in c["models"]:
    for arm in ["REFERENCE"] if name == "PCA2" else c["arms"]:
        key = name + "/" + arm
        rs = [l["records"][f"confirmation/{r}/{key}"] for r in c["confirmation_roots"]]
        lines.append(
            "| "
            + key
            + " | "
            + " | ".join(
                f"{mean([r['evaluation']['metrics'][m + '_nmse'] for r in rs]):.6g}"
                for m in ["interpolate", "extrapolate", "positive", "negative"]
            )
            + " |"
        )
        res = rs[0]["resources"]
        last = rs[0]["loss_diagnostics"]["last100"]
        previous = rs[0]["loss_diagnostics"]["previous100"]
        last = (
            "n/a" if last is None else f"{mean([r['loss_diagnostics']['last100'] for r in rs]):.6g}"
        )
        previous = (
            "n/a"
            if previous is None
            else f"{mean([r['loss_diagnostics']['previous100'] for r in rs]):.6g}"
        )
        resource.append(
            f"| {key} | {res['parameters']} / {res['persistent_bytes']} | {res['state_floats']} | {mean([r['fitting']['cpu_seconds'] for r in rs]):.4f} | {mean([r['evaluation']['inference_cpu_seconds'] for r in rs]):.4f} | {mean([r['fitting']['exposure']['extra_stationary_transition_examples'] for r in rs]):.1f} | {last} | {previous} |"
        )
lines += resource + [
    "",
    "Each neural fit has 19,200 original prefix episodes / 480,000 distinct original sensory snapshots and 600 optimizer updates. Extra stationary targets reuse existing supplied targets; they add no observations. PCA2 uses two passes over the original data and no optimizer steps. Model parameter counts include initializers/readouts/correction. The common fixed projection is 24 float32 values (96 bytes). Evaluation CPU includes geometry diagnostics and is not a production-latency benchmark.",
    "",
]
(out / "tables.md").write_text("\n".join(lines))
print("Wrote", out / "tables.md")
