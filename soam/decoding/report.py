"""Independent reductions and fixed-root inference for the D-R2 diagnostic."""

import hashlib

import matplotlib
import numpy as np
import torch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from soam.temporal.runner import dump

from .engine import ARMS
from .runner import OUT, REPORT, ROOT, read


def independent_reduce(a, denominator):
    """Compute reported scientific metrics independently from archived raw arrays."""
    out = {}
    for name in ARMS:
        error = np.sum(np.square(a[f"{name}_pred"] - a["truth"]), axis=-1) / (8 * denominator)
        out[f"{name}_accuracy"] = float(np.mean(error[..., 0] <= 0.1))
        out[f"{name}_canonical_nmse"] = float(np.mean(error[..., 0]))
        out[f"{name}_free1_nmse"] = float(np.mean(error[..., 1]))
        out[f"{name}_free8_nmse"] = float(np.mean(error[..., 1:]))
    exact = a["codes"][:, :7, :, 512:].astype(float).reshape(4, 7, 8, 8, 32).sum(-1) * (1.5 / 32)
    errors = []
    for seq in range(4):
        for obj in range(7):
            for query in range(8):
                errors.extend(
                    np.sum((exact[seq, obj] - a["truth"][seq, obj, query, 0]) ** 2, axis=-1)
                    / (8 * denominator)
                )
    out["exact_accuracy"] = float(np.mean(np.asarray(errors) <= 0.1))
    out["exact_nmse"] = float(np.mean(errors))
    out["gap"] = out["exact_accuracy"] - out["PH-FULL_accuracy"]
    np.testing.assert_allclose(exact, a["exact_values"], atol=0, rtol=0)
    np.testing.assert_allclose(
        np.reshape(errors, (4, 7, 8, 8)), a["exact_error"], atol=1e-14, rtol=1e-12
    )
    same, other = [], []
    for seq in range(4):
        for obj in range(7):
            for q in range(8):
                free = np.r_[np.repeat(~a["mask"][seq, obj, q], 32), np.ones(256, dtype=bool)]
                delta = a["codes"][seq][..., free] - a["states"][seq, obj, q, free]
                distance = np.sum(delta * delta, axis=-1) / (4 * np.sum(free))
                same.append(float(np.min(distance[obj])))
                other.append(float(np.min(distance[np.arange(8) != obj])))
    np.testing.assert_allclose(
        np.reshape(same, (4, 7, 8)), a["same_code_discrepancy"], atol=0, rtol=0
    )
    np.testing.assert_allclose(
        np.reshape(other, (4, 7, 8)), a["other_code_discrepancy"], atol=0, rtol=0
    )
    out["same_code_discrepancy"] = float(np.mean(same))
    out["other_code_discrepancy"] = float(np.mean(other))
    relation = a["states"][..., 512:].reshape(4, 7, 8, 8, 32)
    out["nonmonotone"] = float(
        np.mean(np.any(relation[..., 1:] > relation[..., :-1], axis=(-1, -2)))
    )
    out["cycles"] = float(np.mean(a["cycles"]))
    out["nonconvergence"] = float(np.mean(a["converged"] == 0))
    out["wrong_object_closer"] = float(np.mean(np.asarray(other) < np.asarray(same)))
    return out


def interval(values, draws, alpha):
    values = np.asarray(values, dtype=float)
    lo, hi = np.quantile(values[draws].mean(1), [alpha / 2, 1 - alpha / 2])
    return {
        "mean": float(values.mean()),
        "lo": float(lo),
        "hi": float(hi),
        "width": float(hi - lo),
        "roots": len(values),
        "degenerate": bool(np.ptp(values) == 0),
    }


def classify(primary, adequacy, m):
    adequate = adequacy["lo"] >= m["exact_code_accuracy_min"]
    precise = primary["width"] <= m["gap_width_max"]
    if adequate and precise and primary["lo"] > m["practical_gap"]:
        return "completion_path_limitation_supported"
    if adequate and precise and primary["hi"] < m["practical_gap"]:
        return "practically_small_gap"
    if adequacy["hi"] < m["exact_code_accuracy_min"]:
        return "exact_decoding_inadequate"
    return "inconclusive"


def audit_codes(dest, a):
    core = torch.load(dest / "core.pt", weights_only=True)
    x, y, q = a["observations"][..., :16], a["observations"][..., 16:24], a["observations"][..., 24]
    value = (y @ core["a"].numpy().T) * np.cos(-q)[..., None]
    value += (y @ core["b"].numpy().T) * np.sin(-q)[..., None]

    def encoded(v, bound):
        thresholds = -bound + (np.arange(32) + 0.5) * 2 * bound / 32
        return np.where(v[..., None] >= thresholds, 1, -1).reshape(*v.shape[:-1], -1)

    expected = np.concatenate([encoded(x, 4), encoded(value, 1.5)], axis=-1)
    np.testing.assert_array_equal(expected, a["codes"])
    residuals = []
    for seq in range(4):
        p = torch.load(dest / f"sequence-{seq}-PH-FULL.pt", weights_only=True)["projector"].numpy()
        codes = expected[seq].reshape(-1, 768)
        residual = float(np.max(np.abs(codes @ p.T - codes)))
        if residual > 1e-8:
            raise RuntimeError("Independent acquired-code preservation check failed")
        residuals.append(residual)
    return max(residuals)


def report(manifest, budget):
    REPORT.mkdir(parents=True, exist_ok=False)
    rows, independently_checked, max_residual = [], 0, 0.0
    for root in manifest["confirmation_roots"]:
        dest = OUT / "confirmation" / f"root-{root}"
        row = read(dest / "result.json")
        with np.load(dest / "arrays.npz") as a:
            independent = independent_reduce(a, row["normalization"])
            max_residual = max(max_residual, audit_codes(dest, a))
        for key, value in independent.items():
            np.testing.assert_allclose(value, row["metrics"][key], atol=1e-12, rtol=1e-12)
            independently_checked += 1
        rows.append(row)
        budget.check()
    repeated_arrays, repeated_tensors = 0, 0
    original = OUT / "confirmation" / f"root-{manifest['repeat_root']}"
    repeat = OUT / "repeat" / original.name
    for path in sorted(original.glob("*.npz")):
        with np.load(path) as a, np.load(repeat / path.name) as b:
            if set(a.files) != set(b.files):
                raise RuntimeError("Repeated array inventory differs")
            for key in a.files:
                np.testing.assert_array_equal(a[key], b[key])
                repeated_arrays += 1
    for path in sorted(original.glob("*.pt")):
        a, b = (
            torch.load(path, weights_only=True),
            torch.load(repeat / path.name, weights_only=True),
        )
        if set(a) != set(b):
            raise RuntimeError("Repeated checkpoint inventory differs")
        for key in a:
            if not torch.equal(a[key], b[key]):
                raise RuntimeError(f"Repeated tensor differs: {path.name}/{key}")
            repeated_tensors += 1
    historical = read(ROOT / "reports/study-d-r1/source.json")["hashes"]
    for path, expected in historical.items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Historical source changed: {path}")
    m = manifest["inference"]
    draws = np.random.default_rng(m["bootstrap_seed"]).integers(
        0, len(rows), (m["bootstrap_draws"], len(rows))
    )
    descriptions = {
        key: interval([r["metrics"][key] for r in rows], draws, m["alpha"])
        for key in rows[0]["metrics"]
    }
    primary = interval([r["metrics"]["gap"] for r in rows], draws, m["alpha"] / m["family_size"])
    adequacy = interval(
        [r["metrics"]["exact_accuracy"] for r in rows], draws, m["alpha"] / m["family_size"]
    )
    statistics = {
        "primary": primary,
        "exact_code_adequacy": adequacy,
        "classification": classify(primary, adequacy, m),
        "descriptive": descriptions,
        "interval_unit": "independent_root",
        "confirmation_roots": manifest["confirmation_roots"],
    }
    verification = {
        "status": "pass",
        "independent_metrics": independently_checked,
        "repeated_arrays": repeated_arrays,
        "repeated_tensors": repeated_tensors,
        "historical_source_hashes": len(historical),
        "audited_projectors": 40,
        "max_stored_code_residual": max_residual,
        "fit_attempts": len(list(OUT.glob("*/root-*/fit-status.json"))),
        "failed_attempts": sum(
            read(p)["status"] != "complete" for p in OUT.glob("*/root-*/fit-status.json")
        ),
    }
    dump(REPORT / "root-results.json", rows)
    dump(REPORT / "statistics.json", statistics)
    dump(REPORT / "verification.json", verification)
    dump(REPORT / "source.json", read(OUT / "source.json"))
    dump(REPORT / "feasibility.json", read(OUT / "feasibility.json"))
    dump(
        REPORT / "resources.json",
        {
            "roots": [
                {
                    "root": r["root"],
                    "resources": r["resources"],
                    "timing": r["timing"],
                    "exposure": r["exposure"],
                    "fit_cpu_seconds": r["fit_cpu_seconds"],
                    "evaluator_array_bytes": r["evaluator_array_bytes"],
                }
                for r in rows
            ]
        },
    )
    table = "| Output path | Raw accuracy | Canonical NMSE | Free-eight NMSE |\n| --- | ---: | ---: | ---: |\n"
    for name in ARMS:
        table += f"| {name} | {descriptions[name + '_accuracy']['mean']:.5f} | {descriptions[name + '_canonical_nmse']['mean']:.5f} | {descriptions[name + '_free8_nmse']['mean']:.5f} |\n"
    table += f"| Exact acquired-code decode (privileged) | {adequacy['mean']:.5f} | {descriptions['exact_nmse']['mean']:.5f} | Not a learner rollout |\n"
    (REPORT / "tables.md").write_text(table)
    names = ["PH-FULL_accuracy", "REG-LIFT_accuracy", "KV_accuracy", "exact_accuracy"]
    means = np.array([descriptions[n]["mean"] for n in names])
    errors = np.array(
        [
            [descriptions[n]["mean"] - descriptions[n]["lo"] for n in names],
            [descriptions[n]["hi"] - descriptions[n]["mean"] for n in names],
        ]
    )
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.errorbar(means, np.arange(4), xerr=errors, fmt="o", color="#276b8e", capsize=4)
    ax.set(
        yticks=np.arange(4),
        yticklabels=[
            "PH768 cue recall",
            "REG-LIFT cue recall",
            "KV cue recall",
            "Exact-code decode*",
        ],
        xlabel="Raw canonical accuracy (ordinary 95% root intervals)",
        xlim=(0, 1.04),
        title="D-R2: usable code versus cue-driven recall",
    )
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.2)
    fig.text(
        0.22,
        0.02,
        "*Evaluator-only diagnostic; correct association identity is supplied.",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(REPORT / "decoding.png", dpi=160)
    plt.close(fig)
    source = read(OUT / "source.json")
    text = f"""# Study D-R2: retrieval versus exact acquired-code decoding

November 19, 2026. Frozen [protocol](../docs/STUDY_D_R2_PROTOCOL.md), SOAM-090–093.

**Frozen classification: {statistics["classification"]}.**
Exact-code minus ordinary PH768 accuracy: {primary["mean"]:.5f}, adjusted interval
[{primary["lo"]:.5f}, {primary["hi"]:.5f}], width {primary["width"]:.5f}.
Exact-code accuracy: {adequacy["mean"]:.5f} [{adequacy["lo"]:.5f}, {adequacy["hi"]:.5f}].
The practical gap is .05, precision width cap .10, exact-code adequacy floor .95.
Intervals use the frozen two-quantity Bonferroni family and ten independent roots.

{table}

![Recall and privileged decoding](study-d-r2/decoding.png)

All acquired snapshots of the correct object receive equal weight. The privileged
branch receives evaluator association identity; it is neither deployed recall nor
a target-selected best code. Ordinary predictions finish before diagnostic scoring.
No architecture, clamp, capacity, encoding or hyperparameter sweep was performed.
Inherited D-R1 development settings were fixed in advance; all data streams are fresh.
Ten roots contain 2,240 earlier-object query cues and 2,240 earlier-object acquired
snapshots. Each snapshot/cue is nested within its root; neither increases the number
of independent replicates. All-success intervals describe this finite sample only.

Every final sequence projector was audited: {verification["audited_projectors"]} projectors,
maximum stored-code residual {max_residual:.3g}. Mean free-coordinate discrepancy to
the correct object's acquired codes is {descriptions["same_code_discrepancy"]["mean"]:.5f};
to other objects' codes {descriptions["other_code_discrepancy"]["mean"]:.5f}.
Nonmonotone relationship-code fraction: {descriptions["nonmonotone"]["mean"]:.5f};
mean PH cycles {descriptions["cycles"]["mean"]:.3f}, nonconvergence
{descriptions["nonconvergence"]["mean"]:.5f}. These are descriptive, with root intervals
in [statistics](study-d-r2/statistics.json). A bit mismatch need not imply a wrong
decoded relationship; convergence and span preservation do not prove useful recall.

Grounded one-step core NMSE averaged {np.mean([r["grounded_one_step_nmse"] for r in rows]):.4g};
free-eight core probe NMSE averaged {np.mean([r["core_free8_nmse"] for r in rows]):.4g}.
The common fitted action core remains an easy scaffold. Ordinary free rollouts begin
with retrieved features and never receive correct future observations.

Reproduction: {repeated_arrays} repeated arrays and {repeated_tensors} checkpoint tensors
match exactly. Independent reduction checks {independently_checked} reported root metrics,
all reconstructed acquired codes and stored spans. {len(historical)} historical D-R1
source hashes remain unchanged. All {verification["fit_attempts"]} planned fits complete;
failed attempts: {verification["failed_attempts"]}. No exclusion, replacement or tuning.

Source commit `{source["commit"]}`; fingerprint `{source["aggregate"]}`.
CPU float64, deterministic Torch, one intra-op/inter-op thread. Version/hardware,
all seeds and source hashes: [source](study-d-r2/source.json). Per-root configuration,
normalization and observations: [root results](study-d-r2/root-results.json).
Each arm shares 2,048 training transitions and 256 acquisition snapshots per root;
the prescribed repeated root is excluded from inference. Total fit attempts include
the fixture and repeat. Raw inputs, core/checkpoints, ordinary predictions and
diagnostic arrays remain in `runs/study-d-r2-v1/`.

Persistent storage, active/workspace state, batch recall/write timings and evaluator
storage are disclosed in [resources](study-d-r2/resources.json). PH uses a 768-square
float64 projector plus a transient effective weight matrix; each cycle executes
approximately 5*768^2 multiply-add pairs with the inherited invariant diagnostics.
REG-LIFT solves 256 visible-coordinate equations per query; KV scans eight keys.
These are implementation estimates, not optimized lower bounds or matched resources.
Exact-code tensors are evaluator-only and are counted separately from model memory.
The fresh ceiling is 900 CPU / 1,800 execution-wall seconds, 2 GiB RSS and 1 GiB
artifacts. [Feasibility](study-d-r2/feasibility.json) preceded confirmation; the final
ledger is `runs/study-d-r2-v1/ledger.json`.

This diagnostic can locate a gap between usable acquired codes and cue-driven
outputs, but cannot uniquely identify cue ambiguity, clamp interference, geometry,
mixed states or attraction basins as its cause. KV/REG-LIFT are descriptive references;
no new superiority, unknown-rejection, retention or sharing gate is tested. D-R1 and
all earlier negative results remain unchanged. The separate decision owns the next
recommendation; no follow-up is automatically activated.
"""
    (ROOT / "reports/STUDY_D_R2.md").write_text(text)
    budget.check(force=True)
