"""Independent E0 reduction audit and descriptive figures; performs no fitting."""

import csv
import hashlib
import json
import resource
import sys
import time
from pathlib import Path

import matplotlib
import numpy as np
import torch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

started_cpu, started_wall = time.process_time(), time.monotonic()
torch.set_num_threads(1)
repo = Path.cwd()
raw = repo / "runs/study-e0-v1"
out = repo / "reports/study-e0"
out.mkdir(exist_ok=True)
previous_receipt = (
    json.loads((out / "receipt.json").read_text()) if (out / "receipt.json").exists() else {}
)
ledger = json.loads((raw / "ledger.json").read_text())
summary = json.loads((raw / "summary.json").read_text())
config = json.loads((repo / "docs/protocols/study_e0_v1.json").read_text())
assert len([r for r in ledger["records"].values() if r["phase"] != "fixture"]) == 58
assert all(r["status"] == "complete" for r in ledger["records"].values())
# Reconstruct the frozen projection directly, independently of model/evaluation code.
projection, _ = np.linalg.qr(np.random.default_rng(1729).normal(size=(12, 2)))
projection = projection.astype(np.float32).astype(np.float64)


def phase(z):
    xy = z.astype(np.float64) @ projection
    return np.arctan2(xy[..., 1], xy[..., 0])


def wrap(x):
    return np.arctan2(np.sin(x), np.cos(x))


def readout(h, checkpoint, name):
    state = {k: v.numpy() for k, v in checkpoint.items()}
    if name == "PCA2":
        return h[..., :2] @ state["P"].T + state["mean"]
    return h @ state["D.weight"].T + state["D.bias"]


rows, curves, audit = (
    [],
    {},
    {
        "root_metrics": 0,
        "bootstrap_intervals": 0,
        "source_hashes": 0,
        "payload_hashes": 0,
        "unavailable_geometry": [],
    },
)
for name in config["models"]:
    curves[name] = {k: [] for k in ("free", "stationary", "normal", "return")}
    for root in config["confirmation_roots"]:
        record = ledger["records"][f"confirmation/{root}/{name}"]
        directory = raw / "trials/confirmation" / str(root) / name
        checkpoint = torch.load(directory / "checkpoint.pt", weights_only=True)
        with np.load(directory / "arrays.npz") as a:
            fresh = {
                "free_nmse": a["free/prior_nmse"].mean(),
                "grounded_nmse": a["grounded/prior_nmse"].mean(),
                "return_nmse": a["return/posterior_nmse"][-1].mean(),
            }
            stationary = np.abs(wrap(phase(a["stationary_features"]) - a["theta"])) * 180 / np.pi
            np.testing.assert_allclose(stationary, a["stationary_deg"], atol=1e-10, rtol=1e-10)
            fresh["stationary_deg"] = stationary[-1].mean()
            base, perturbed = a["geometry_base_states"], a["geometry_perturbed_states"]
            n = 2 if name == "PCA2" else 32
            tangent = np.roll(base[..., :n], -1, 1) - np.roll(base[..., :n], 1, 1)
            tangent /= np.maximum(np.linalg.norm(tangent, axis=-1, keepdims=True), 1e-12)
            delta = perturbed[..., :n] - base[..., :n]
            normal = delta - np.sum(delta * tangent, axis=-1, keepdims=True) * tangent
            eps = config["perturbation_fraction"] * float(a["family_radius"])
            normal_ratio = np.linalg.norm(normal, axis=-1) / max(eps, 1e-12)
            np.testing.assert_allclose(normal_ratio, a["normal_ratio"], atol=2e-6, rtol=1e-5)
            base_phase, perturbed_phase = (
                phase(readout(base, checkpoint, name)),
                phase(readout(perturbed, checkpoint, name)),
            )
            pose_error = np.abs(wrap(perturbed_phase - base_phase)) * 180 / np.pi
            np.testing.assert_allclose(pose_error, a["normal_pose_deg"], atol=0.0005, rtol=0.001)
            gap = wrap(np.roll(base_phase, -config["tangent_bins"], 1) - base_phase)
            np.testing.assert_allclose(gap, a["tangent_phase_gap"], atol=1e-5, rtol=0.001)
            ratio = gap / np.where(np.abs(gap[0]) >= 1e-8, gap[0], 1e-8)
            fresh.update(
                normal_ratio=float(normal_ratio[-1].mean()),
                normal_pose_deg=float(pose_error[-1].mean()),
                tangent_ratio=float(ratio[-1].mean()),
            )
            for key, value in fresh.items():
                stored = record["evaluation"]["metrics"][key]
                if stored is None:
                    audit["unavailable_geometry"].append([name, root, key])
                else:
                    np.testing.assert_allclose(
                        value, stored, atol=0.001, rtol=0.001, err_msg=f"{name}/{root}/{key}"
                    )
                    audit["root_metrics"] += 1
            curves[name]["free"].append(a["free/prior_nmse"].mean(1))
            curves[name]["stationary"].append(stationary.mean(1))
            curves[name]["normal"].append(a["normal_ratio"].mean(1))
            curves[name]["return"].append(a["return/posterior_nmse"].mean(1))
        rows.append(
            {
                "model": name,
                "root": root,
                **record["evaluation"]["metrics"],
                "fit_cpu_seconds": record["fitting"]["cpu_seconds"],
                "inference_cpu_seconds": record["evaluation"]["inference_cpu_seconds"],
                "last100_loss": record["loss_diagnostics"]["last100"],
                "previous100_loss": record["loss_diagnostics"]["previous100"],
            }
        )
    for metric in config["endpoints"]:
        values = [r[metric] for r in rows if r["model"] == name]
        ci = summary["models"][name]["adjusted"][metric]
        if any(v is None for v in values):
            assert ci is None
            continue
        values = np.array(values)
        rng = np.random.default_rng(config["bootstrap_seed"])
        means = values[
            rng.integers(len(values), size=(config["bootstrap_resamples"], len(values)))
        ].mean(1)
        lo, hi = np.quantile(means, [0.05 / 28 / 2, 1 - 0.05 / 28 / 2])
        np.testing.assert_allclose(
            [ci["mean"], ci["lo"], ci["hi"], ci["width"]],
            [values.mean(), lo, hi, hi - lo],
            rtol=0,
            atol=1e-12,
        )
        audit["bootstrap_intervals"] += 1

with (out / "root_metrics.csv").open("w") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.2), constrained_layout=True)
colors = {"NAV32": "#2775b6", "SYM32": "#8a5da8", "GRU32": "#d17b20", "PCA2": "#218660"}
labels = {
    "free": ("Free action rollout", "Feature NMSE (log scale)"),
    "stationary": ("Zero action, no new cues", "Absolute pose error (degrees)"),
    "normal": ("Transverse perturbation", "Paired transverse separation ratio"),
    "return": ("Evidence returns after step 32", "Posterior NMSE (log scale)"),
}
for ax, (key, (title, ylabel)) in zip(axes.flat, labels.items()):
    for name in config["models"]:
        y = np.mean(curves[name][key], axis=0)
        x = np.arange(len(y)) + (1 if key == "free" else 0)
        ax.plot(x, y, label=name, color=colors[name], lw=2)
    ax.set(
        title=title,
        xlabel="Physical steps" if key != "normal" else "Autonomous zero-action steps",
        ylabel=ylabel,
    )
    ax.grid(alpha=0.18)
    if key in {"free", "return"}:
        ax.set_yscale("log")
    if key == "normal":
        ax.axhline(0.5, color="gray", ls=":", lw=1)
    if key == "stationary":
        ax.axhline(5, color="gray", ls=":", lw=1)
    if key == "return":
        ax.axvline(32, color="gray", ls=":", lw=1)
axes[0, 0].legend(ncol=2, fontsize=9)
fig.suptitle("E0 v1 · ten independently trained roots · mean diagnostic trajectories", fontsize=13)
fig.savefig(out / "trajectories.png", dpi=180)
fig.savefig(out / "trajectories.svg")
plt.close(fig)

source = ledger["commands"][-1]["provenance"]
for relative, expected in source["source_files"].items():
    for path in (repo / relative, raw / "source" / relative):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, relative
    audit["source_hashes"] += 1
for record in ledger["records"].values():
    for relative, expected in record["sha256"].items():
        assert hashlib.sha256((raw / relative).read_bytes()).hexdigest() == expected, relative
        audit["payload_hashes"] += 1
payload = {
    str(p.relative_to(raw)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(raw.rglob("*"))
    if p.is_file()
}
(out / "archive_sha256.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
(out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
current_cpu = time.process_time() - started_cpu
current_wall = time.monotonic() - started_wall
history = previous_receipt.get("postprocessing_history", [])
if not history and previous_receipt:
    history = [
        {
            "source_sha256": previous_receipt["postprocessing_source_sha256"],
            "cpu_seconds": previous_receipt["postprocessing_cpu_seconds"],
            "wall_seconds": previous_receipt["postprocessing_wall_seconds"],
            "source_archive": "analysis-first-pass.txt",
        }
    ]
history.append(
    {
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "cpu_seconds": current_cpu,
        "wall_seconds": current_wall,
        "source_archive": "analysis.py",
    }
)
receipt = {
    "audit": audit,
    "repeat": ledger["repeat_check"],
    "source": source,
    "postprocessing_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "numerical_cpu_seconds": ledger["cpu_seconds"],
    "numerical_wall_seconds": ledger["wall_seconds"],
    "postprocessing_cpu_seconds": current_cpu
    + previous_receipt.get("postprocessing_cpu_seconds", 0),
    "postprocessing_wall_seconds": current_wall
    + previous_receipt.get("postprocessing_wall_seconds", 0),
    "postprocessing_history": history,
    "raw_artifact_bytes": sum(p.stat().st_size for p in raw.rglob("*") if p.is_file()),
    "numerical_peak_rss_bytes": ledger["peak_rss_bytes"],
    "postprocessing_peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    * (1 if sys.platform == "darwin" else 1024),
    "archive_note": "Full local raw archive under runs/study-e0-v1; not included in Git. Payload hashes and summaries tracked.",
    "planned_scientific_fits": 58,
    "completed_scientific_fits": 58,
    "fixture_fits": 4,
    "failed_fits": 0,
    "excluded_roots": 0,
}
(out / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
print(json.dumps({k: v for k, v in receipt.items() if k not in {"source"}}, indent=2))
for name, result in summary["models"].items():
    print(name, result["outcome"], result["criteria"])
    for key, ci in result["adjusted"].items():
        print(" ", key, ci)
