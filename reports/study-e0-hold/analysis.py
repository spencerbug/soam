"""Independent E0-HOLD reduction audit and figure creation; no model fitting."""

import csv
import hashlib
import json
import resource
import runpy
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import matplotlib
import numpy as np
import torch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

started_cpu, started_wall = time.process_time(), time.monotonic()
torch.set_num_threads(1)
repo = Path.cwd()
raw = repo / "runs/study-e0-hold-v1"
out = repo / "reports/study-e0-hold"
out.mkdir(exist_ok=True)
previous = json.loads((out / "receipt.json").read_text()) if (out / "receipt.json").exists() else {}
ledger = json.loads((raw / "ledger.json").read_text())
summary = json.loads((raw / "summary.json").read_text())
config = json.loads((repo / "docs/protocols/study_e0_hold_v1.json").read_text())
assert len(ledger["records"]) == 154
assert sum(r["phase"] != "fixture" for r in ledger["records"].values()) == 147
assert all(r["status"] == "complete" for r in ledger["records"].values())
projection, _ = np.linalg.qr(np.random.default_rng(1729).normal(size=(12, 2)))
projection = projection.astype(np.float32).astype(np.float64)


def phase(features):
    xy = features.astype(np.float64) @ projection
    return np.arctan2(xy[..., 1], xy[..., 0])


def wrap(x):
    return np.arctan2(np.sin(x), np.cos(x))


def readout(h, checkpoint, name):
    state = {k: v.numpy() for k, v in checkpoint.items()}
    return (
        h[..., :2] @ state["P"].T + state["mean"]
        if name == "PCA2"
        else h @ state["D.weight"].T + state["D.bias"]
    )


rows, curves = [], {}
audit = {
    "root_metrics": 0,
    "adjusted_intervals": 0,
    "source_hashes": 0,
    "historical_source_hashes": 0,
    "payload_hashes": 0,
    "unavailable_geometry": [],
}
for name in config["models"]:
    for arm in ["REFERENCE"] if name == "PCA2" else config["arms"]:
        key = name + "/" + arm
        curves[key] = {k: [] for k in ("free", "stationary", "normal", "normal_pose", "return")}
        for root in config["confirmation_roots"]:
            record = ledger["records"][f"confirmation/{root}/{key}"]
            directory = raw / "trials/confirmation" / str(root) / key
            checkpoint = torch.load(directory / "checkpoint.pt", weights_only=True)
            with np.load(directory / "arrays.npz") as a:
                fresh = {
                    "free_nmse": a["free/prior_nmse"].mean(),
                    "grounded_nmse": a["grounded/prior_nmse"].mean(),
                    "return_nmse": a["return/posterior_nmse"][-1].mean(),
                }
                stationary = (
                    np.abs(wrap(phase(a["stationary_features"]) - a["theta"])) * 180 / np.pi
                )
                np.testing.assert_allclose(stationary, a["stationary_deg"], atol=1e-10, rtol=1e-10)
                fresh["stationary_deg"] = stationary[-1].mean()
                base, perturbed = a["geometry_base_states"], a["geometry_perturbed_states"]
                n = 2 if name == "PCA2" else 32
                tangent = np.roll(base[..., :n], -1, 1) - np.roll(base[..., :n], 1, 1)
                tangent /= np.maximum(np.linalg.norm(tangent, axis=-1, keepdims=True), 1e-12)
                delta = perturbed[..., :n] - base[..., :n]
                normal = delta - np.sum(delta * tangent, axis=-1, keepdims=True) * tangent
                ratio = np.linalg.norm(normal, axis=-1) / max(
                    0.1 * float(a["family_radius"]), 1e-12
                )
                np.testing.assert_allclose(ratio, a["normal_ratio"], atol=2e-6, rtol=1e-5)
                p0, p1 = (
                    phase(readout(base, checkpoint, name)),
                    phase(readout(perturbed, checkpoint, name)),
                )
                pose = np.abs(wrap(p1 - p0)) * 180 / np.pi
                np.testing.assert_allclose(pose, a["normal_pose_deg"], atol=0.0005, rtol=0.001)
                gap = wrap(np.roll(p0, -config["tangent_bins"], 1) - p0)
                np.testing.assert_allclose(gap, a["tangent_phase_gap"], atol=1e-5, rtol=0.001)
                tangent_ratio = gap / np.where(np.abs(gap[0]) >= 1e-8, gap[0], 1e-8)
                fresh.update(
                    normal_ratio=float(ratio[-1].mean()),
                    normal_pose_deg=float(pose[-1].mean()),
                    tangent_ratio=float(tangent_ratio[-1].mean()),
                )
                for metric, value in fresh.items():
                    stored = record["evaluation"]["metrics"][metric]
                    if stored is None:
                        audit["unavailable_geometry"].append([name, arm, root, metric])
                    else:
                        np.testing.assert_allclose(
                            value, stored, atol=0.001, rtol=0.001, err_msg=f"{root}/{key}/{metric}"
                        )
                        audit["root_metrics"] += 1
                for label, data in {
                    "free": a["free/prior_nmse"],
                    "stationary": stationary,
                    "normal": a["normal_ratio"],
                    "normal_pose": a["normal_pose_deg"],
                    "return": a["return/posterior_nmse"],
                }.items():
                    curves[key][label].append(data.mean(1))
            rows.append(
                {
                    "model": name,
                    "arm": arm,
                    "root": root,
                    **record["evaluation"]["metrics"],
                    "fit_cpu_seconds": record["fitting"]["cpu_seconds"],
                    "inference_cpu_seconds": record["evaluation"]["inference_cpu_seconds"],
                    **record["fitting"]["exposure"],
                    **record["loss_diagnostics"],
                }
            )

for root in config["confirmation_roots"]:
    records = [
        r for r in ledger["records"].values() if r["phase"] == "confirmation" and r["root"] == root
    ]
    assert len({r["fitting"]["training_data_sha256"] for r in records}) == 1
    for name in config["models"][:-1]:
        pair = {r["arm"]: r for r in records if r["model"] == name}
        assert pair["SHORT24"]["initial_state_sha256"] == pair["LONG128"]["initial_state_sha256"]
        short, long = (pair[a]["fitting"]["exposure"] for a in config["arms"])
        assert short["extra_observations"] == long["extra_observations"] == 0
        assert short["eligible_stationary_episodes"] == long["eligible_stationary_episodes"]
        assert short["extra_stationary_transition_examples"] == 0
        assert (
            long["extra_stationary_transition_examples"]
            == long["eligible_stationary_episodes"] * 104
        )

nav = {
    arm: {
        metric: np.array([r[metric] for r in rows if r["model"] == "NAV32" and r["arm"] == arm])
        for metric in config["endpoints"]
    }
    for arm in config["arms"]
}


def difference(left, right):
    if any(v is None for v in left) or any(v is None for v in right):
        return None
    return left - right


values = {"absolute/" + k: v for k, v in nav["LONG128"].items()}
values["gain/stationary_deg"] = difference(
    nav["SHORT24"]["stationary_deg"], nav["LONG128"]["stationary_deg"]
)
values.update(
    {
        "degradation/" + k: difference(nav["LONG128"][k], nav["SHORT24"][k])
        for k in config["degradation"]
    }
)
for key, value in values.items():
    ci = summary["adjusted_NAV32"][key]
    if value is None or any(v is None for v in value):
        assert ci is None
        continue
    rng = np.random.default_rng(config["bootstrap_seed"])
    means = value[rng.integers(len(value), size=(config["bootstrap_resamples"], len(value)))].mean(
        1
    )
    lo, hi = np.quantile(means, [0.05 / 13 / 2, 1 - 0.05 / 13 / 2])
    np.testing.assert_allclose(
        [ci["mean"], ci["lo"], ci["hi"], ci["width"]],
        [value.mean(), lo, hi, hi - lo],
        atol=1e-12,
        rtol=0,
    )
    audit["adjusted_intervals"] += 1

with (out / "root_metrics.csv").open("w") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.3), constrained_layout=True)
for ax, key, title, label in [
    (axes[0, 0], "stationary", "Zero action, no new cues", "Absolute pose error (degrees)"),
    (axes[0, 1], "free", "Free action navigation", "Feature NMSE"),
    (axes[1, 0], "normal", "Local perturbation recovery", "Transverse separation ratio"),
    (
        axes[1, 1],
        "normal_pose",
        "Pose preservation during recovery",
        "Perturbation-induced error (degrees)",
    ),
]:
    for arm, color in (("SHORT24", "#2775b6"), ("LONG128", "#d17b20")):
        ys = np.mean(curves["NAV32/" + arm][key], axis=0)
        x = np.arange(len(ys)) + (1 if key == "free" else 0)
        ax.plot(x, ys, label=arm, color=color, lw=2)
    ax.set(title=title, ylabel=label, xlabel="Steps")
    ax.grid(alpha=0.18)
    if key in {"stationary", "normal", "normal_pose"}:
        ax.axhline(
            {"stationary": 5, "normal": 0.5, "normal_pose": 3}[key], color="gray", ls=":", lw=1
        )
axes[0, 0].legend()
fig.suptitle("E0-HOLD v1 · NAV32 · means over 20 fresh paired roots", fontsize=13)
fig.savefig(out / "trajectories.png", dpi=180)
fig.savefig(out / "trajectories.svg")
plt.close(fig)

source = ledger["commands"][-1]["provenance"]
for relative, expected in source["source_files"].items():
    assert hashlib.sha256((repo / relative).read_bytes()).hexdigest() == expected
    assert hashlib.sha256((raw / "source" / relative).read_bytes()).hexdigest() == expected
    audit["source_hashes"] += 1
parent = json.loads((repo / "reports/study-e0/receipt.json").read_text())["source"]["source_files"]
for relative, expected in parent.items():
    assert hashlib.sha256((repo / relative).read_bytes()).hexdigest() == expected
    audit["historical_source_hashes"] += 1
for record in ledger["records"].values():
    for relative, expected in record["sha256"].items():
        assert hashlib.sha256((raw / relative).read_bytes()).hexdigest() == expected
        audit["payload_hashes"] += 1
archive = {
    str(p.relative_to(raw)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(raw.rglob("*"))
    if p.is_file()
}
record_times = {
    ident: {
        "record_file_modified_utc": datetime.fromtimestamp(
            (raw / "trials" / ident / "record.json").stat().st_mtime, UTC
        ).isoformat(),
        "note": "Filesystem timestamp of the completed immutable record, not inferred fit-start time.",
    }
    for ident in ledger["records"]
}
(out / "trial_record_times.json").write_text(
    json.dumps(record_times, indent=2, sort_keys=True) + "\n"
)
(out / "archive_sha256.json").write_text(json.dumps(archive, indent=2, sort_keys=True) + "\n")
(out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
tables_source = Path(__file__).with_name("soam_hold_tables.py")
runpy.run_path(str(tables_source), run_name="__main__")
cpu, wall = time.process_time() - started_cpu, time.monotonic() - started_wall
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == "darwin" else 1024)
history = previous.get("postprocessing_history", [])
history.append(
    {
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "tables_source_sha256": hashlib.sha256(tables_source.read_bytes()).hexdigest(),
        "cpu_seconds": cpu,
        "wall_seconds": wall,
        "peak_rss_bytes": rss,
    }
)
receipt = {
    "audit": audit,
    "repeat": ledger["repeat_check"],
    "source": source,
    "outcome": summary["outcome"],
    "planned_scientific_fits": 147,
    "completed_scientific_fits": 147,
    "fixture_fits": 7,
    "failed_fits": 0,
    "excluded_roots": 0,
    "numerical_cpu_seconds": ledger["cpu_seconds"],
    "numerical_wall_seconds": ledger["wall_seconds"],
    "postprocessing_cpu_seconds": sum(x["cpu_seconds"] for x in history),
    "postprocessing_wall_seconds": sum(x["wall_seconds"] for x in history),
    "postprocessing_history": history,
    "peak_rss_bytes": max(ledger["peak_rss_bytes"], *(x["peak_rss_bytes"] for x in history)),
    "raw_artifact_bytes": sum(p.stat().st_size for p in raw.rglob("*") if p.is_file()),
    "archive_files": len(archive),
    "archive_note": "Full raw payloads are local under runs/study-e0-hold-v1, ignored by Git. Summaries, receipts and hashes are tracked.",
}
assert (
    receipt["numerical_cpu_seconds"] + receipt["postprocessing_cpu_seconds"]
    <= config["limits"]["cpu_seconds"]
)
assert (
    receipt["numerical_wall_seconds"] + receipt["postprocessing_wall_seconds"]
    <= config["limits"]["wall_seconds"]
)
assert receipt["peak_rss_bytes"] <= config["limits"]["rss_bytes"]
assert receipt["raw_artifact_bytes"] <= config["limits"]["artifact_bytes"]
(out / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
print(json.dumps({k: v for k, v in receipt.items() if k != "source"}, indent=2))
for key, ci in summary["adjusted_NAV32"].items():
    print(key, ci, summary["criteria"][key])
