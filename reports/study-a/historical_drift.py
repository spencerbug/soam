"""Descriptive reanalysis of exposed E1 archives; no new fitting or holdout claims."""

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

from soam.encoders.projection import FixedProjection
from soam.gating.runner import Budget, dump
from soam.shared.archive import InputStore

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "runs/study-a-v2"
HIST = ROOT / "runs/e1-confirmation-v1-a1"
m = json.loads((OUT / "manifest.json").read_text())
budget = Budget(OUT, m)
torch.set_num_threads(1)
p = FixedProjection(12, 1729).matrix.numpy().astype(np.float64)
inverse = np.linalg.pinv(p)
with np.load(HIST / "normalization.npz", allow_pickle=False) as norm:
    variance = float(norm["variance"])
roots = [11, 23, 47, 71, 101, 131, 173, 211, 257, 307]
models = ["G28", "G32", "L12"]
rows = []
store = InputStore(HIST / "input-objects")
checked = 0
for root in roots:
    budget.check(reserve=False)
    per = {name: [] for name in models}
    for episode in range(20):
        reference = json.loads(
            (
                HIST
                / "confirmation"
                / str(root)
                / "evaluation-data"
                / f"transition-{episode}"
                / "input-ref.json"
            ).read_text()
        )
        obj = store.verify(reference["object"], reference["manifest_sha256"])
        with np.load(obj / "targets.npz", allow_pickle=False) as target:
            truth = target["world"][1:].reshape(32, 2).astype(np.float64)
            features = target["features"][1:].reshape(32, 12).astype(np.float64)
        for name in models:
            folder = HIST / "confirmation" / str(root) / "cells" / f"{name}-transition-{episode}"
            with np.load(folder / "arrays.npz", allow_pickle=False) as arrays:
                pred = arrays["free_features"].reshape(32, 12).astype(np.float64)
            record = json.loads((folder / "record.json").read_text())
            error = ((pred - features) ** 2).mean(1) / variance
            assert abs(error.mean() - record["metrics"]["free32_nmse"]) < 1e-12
            checked += 1
            xy = pred @ inverse.T
            r = np.linalg.norm(truth, axis=1)
            rp = np.linalg.norm(xy, axis=1)
            cosine = np.clip((xy * truth).sum(1) / np.maximum(r * rp, 1e-15), -1, 1)
            radial = (rp - r) ** 2 / (12 * variance)
            angular = 2 * rp * r * (1 - cosine) / (12 * variance)
            orthogonal = ((pred - xy @ p.T) ** 2).mean(1) / variance
            assert np.max(np.abs(radial + angular + orthogonal - error)) < 1e-6
            phase = np.abs(
                np.arctan2(
                    np.sin(np.arctan2(xy[:, 1], xy[:, 0]) - np.arctan2(truth[:, 1], truth[:, 0])),
                    np.cos(np.arctan2(xy[:, 1], xy[:, 0]) - np.arctan2(truth[:, 1], truth[:, 0])),
                )
            )
            per[name].append(
                {
                    "nmse": error,
                    "radial_nmse": radial,
                    "angular_nmse": angular,
                    "outside_plane_nmse": orthogonal,
                    "phase_radians": phase,
                    "radius_bias": rp - r,
                }
            )
    for name in models:
        curves = {key: np.mean([v[key] for v in per[name]], axis=0) for key in per[name][0]}
        metrics = {
            f"{key}_{period}": float(value[section].mean())
            for key, value in curves.items()
            for period, section in [
                ("early8", slice(0, 8)),
                ("late8", slice(24, 32)),
                ("all32", slice(0, 32)),
            ]
        }
        rows.append(
            {
                "root": root,
                "model": name,
                "metrics": metrics,
                "curves": {k: v.tolist() for k, v in curves.items()},
            }
        )
rng = np.random.default_rng(8675312)
draws = rng.integers(10, size=(20000, 10))
summary = {}
for name in models:
    selected = [r for r in rows if r["model"] == name]
    summary[name] = {}
    for key in selected[0]["metrics"]:
        vals = np.array([r["metrics"][key] for r in selected])
        lo, hi = np.quantile(vals[draws].mean(1), [0.025, 0.975])
        summary[name][key] = {"mean": float(vals.mean()), "lo": float(lo), "hi": float(hi)}
result = {
    "scope": "descriptive exposed E1 archive reanalysis; not Study A confirmation",
    "roots": roots,
    "cells_checked_against_original_metrics": checked,
    "projection_use": "evaluator-only least-squares inverse of fixed sensory projection",
    "decomposition": "squared radial + angle-weighted distance + outside sensory-plane feature residual; floating Gram discrepancy below 1e-6 NMSE",
    "summary": summary,
    "root_rows": rows,
    "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
dump(ROOT / "reports/study-a/historical-drift.json", result)
fig, axes = plt.subplots(1, 4, figsize=(15, 4))
for name in models:
    for ax, key, title in zip(
        axes,
        ["nmse", "radial_nmse", "angular_nmse", "outside_plane_nmse"],
        [
            "Total error",
            "Radial contribution",
            "Angular contribution",
            "Outside-plane contribution",
        ],
    ):
        vals = np.mean([r["curves"][key] for r in rows if r["model"] == name], axis=0)
        ax.plot(np.arange(1, 33), vals, label=name)
        ax.set_title(title)
        ax.set_xlabel("free rollout step")
        ax.set_ylabel("NMSE")
        ax.grid(alpha=0.2)
axes[0].legend()
fig.tight_layout()
fig.savefig(ROOT / "reports/study-a/historical-drift.png", dpi=160)
fig.savefig(ROOT / "reports/study-a/historical-drift.svg")
plt.close(fig)
budget.finish("historical-archive-drift-analysis", "complete")
print(json.dumps(summary, indent=2))
