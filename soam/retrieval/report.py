"""Independent array audit, paired-root inference and bounded D-R1 reporting."""

import hashlib
import json
import time

import matplotlib
import numpy as np
import torch

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from soam.temporal.runner import dump, size, tensor_hash

from .runner import CONDITIONS, GROUPS, OUT, REPORT, ROOT, read


def independent_metrics(a, denominator, thresholds):
    """Reconstruct errors from predictions, independently of engine.reduce."""
    output = {}
    for ci, condition in enumerate(CONDITIONS):
        err1 = ((a["d1_pred"][ci] - a["d1_truth"][None]) ** 2).sum(-1) / (8 * denominator)
        err2 = ((a["d2_pred"][ci] - a["d2_truth"][:, None]) ** 2).sum(-1) / (8 * denominator)
        assert np.allclose(err1, a["d1_error"][ci], atol=1e-12, rtol=1e-12)
        assert np.allclose(
            err2[:, a["d2_valid"]], a["d2_error"][ci][:, a["d2_valid"]], atol=1e-12, rtol=1e-12
        )
        initial = [err2[s, o, o, :, 1:].mean() for s in range(4) for o in range(7)]
        final = [err2[s, 7, o, :, 1:].mean() for s in range(4) for o in range(7)]
        correct = np.concatenate([err2[s, 7, o, :, 0] <= 0.1 for s in range(4) for o in range(7)])
        scores = np.concatenate([a["d2_scores"][ci, s, 7, o] for s in range(4) for o in range(7)])
        accepted = (scores <= thresholds[condition]) & (scores < np.finfo(float).max)
        unknown = a["unknown_scores"][ci]
        unknown_accept = (unknown <= thresholds[condition]) & (unknown < np.finfo(float).max)
        count = int(accepted.sum())
        output[condition] = {
            "J": float(np.mean([err1[b, :, :, 1:].mean() for b in range(1, 5)])),
            "one_shot": float(err1[1, :, :, 1:].mean()),
            "accuracy8": float((err1[4, :, :, 0] <= 0.1).mean()),
            "error8": float(err1[4, :, :, 1:].mean()),
            "old_error": float(np.mean(final)),
            "old_accuracy": float(correct.mean()),
            "retention": float(np.mean(np.array(final) - initial)),
            "known_coverage": float(accepted.mean()),
            "accepted_wrong": float((accepted & ~correct).mean()),
            "unknown_acceptance": float(unknown_accept.mean()),
            "accepted_accuracy": float((accepted & correct).sum() / count) if count else None,
            "conditional_wrong": float((accepted & ~correct).sum() / count) if count else None,
            "known_queries": len(correct),
            "accepted_queries": count,
            "unknown_queries": int(unknown.size),
        }
    return output


def intervals(values, draws, adjusted=True):
    v = np.asarray(values, dtype=float)
    means = v[draws].mean(1)
    alpha = 0.05 / 12 if adjusted else 0.05
    lo, hi = np.quantile(means, [alpha / 2, 1 - alpha / 2])
    return {
        "mean": float(v.mean()),
        "lo": float(lo),
        "hi": float(hi),
        "width": float(hi - lo),
        "roots": len(v),
        "degenerate": bool(np.ptp(v) == 0),
    }


def statistics(rows, m):
    draws = np.random.default_rng(m["inference"]["bootstrap_seed"]).integers(0, 10, (200000, 10))

    def vals(name, key):
        return np.array([r["metrics"]["partial"][key] for r in rows[name]])

    def ci(v):
        return intervals(v, draws)

    ph, one = vals("PH-FULL", "old_accuracy"), vals("PH-1", "old_accuracy")
    out = {
        "primary": ci(ph - one),
        "acquisition_gain": ci(
            (vals("NOWRITE", "J") - vals("PH-FULL", "J")) / np.maximum(vals("NOWRITE", "J"), 1e-6)
        ),
    }
    limits = {
        "accuracy8": ("lo", 0.8, "min"),
        "error8": ("hi", 0.15, "max"),
        "old_accuracy": ("lo", 0.8, "min"),
        "retention": ("hi", 0.02, "max"),
        "known_coverage": ("lo", 0.9, "min"),
        "accepted_wrong": ("hi", 0.05, "max"),
        "unknown_acceptance": ("hi", 0.1, "max"),
    }
    out["guards"] = {}
    for key, (bound, limit, mode) in limits.items():
        entry = ci(vals("PH-FULL", key))
        entry["pass"] = entry[bound] >= limit if mode == "min" else entry[bound] <= limit
        entry["established_failure"] = entry["hi"] < limit if mode == "min" else entry["lo"] > limit
        out["guards"][key] = entry
    gain = out["acquisition_gain"]
    floor = bool((vals("NOWRITE", "J") < 1e-6).any())
    out["acquisition_floor_limited"] = floor
    reliable = (
        not floor
        and gain["mean"] >= 0.2
        and gain["lo"] > 0
        and gain["width"] <= 0.4
        and all(x["pass"] for x in out["guards"].values())
    )
    out["reliable_retrieval"] = bool(reliable)

    def classify(x):
        if x["hi"] < 0.05 and x["width"] <= 0.1:
            return "adequately precise negative practical benefit"
        if x["mean"] >= 0.05 and x["lo"] > 0 and x["width"] <= 0.1:
            return (
                "supported" if reliable else "positive contrast; reliability conjunction not passed"
            )
        return "inconclusive"

    out["settling_outcome"] = classify(out["primary"])
    out["secondary"] = {}
    for ref in ("REG", "KV", "REG-LIFT"):
        x = ci(ph - vals(ref, "old_accuracy"))
        out["secondary"][ref] = {**x, "outcome": classify(x)}
    out["descriptive"] = {
        n: {
            c: {key: intervals([r["metrics"][c][key] for r in rr], draws, False) for key in limits}
            for c in CONDITIONS
        }
        for n, rr in rows.items()
    }
    return out


def report(dest, m, budget):
    REPORT.mkdir(parents=True, exist_ok=True)
    phases = {
        p.name: read(p / "phase-status.json")
        for p in OUT.iterdir()
        if p.is_dir() and p.name != "report" and (p / "phase-status.json").exists()
    }
    complete = all(
        phases.get(p, {}).get("status") == "complete" for p in ("confirmation", "repeat")
    )
    provenance = read(OUT / "fixture/source.json")
    dump(REPORT / "source.json", provenance)
    dump(REPORT / "phase-status.json", phases)
    for phase, file in [
        ("fixture", "projection.json"),
        ("development", "selection.json"),
        ("freeze", "receipt.json"),
    ]:
        path = OUT / phase / file
        if path.exists():
            dump(REPORT / (phase + "-" + file), read(path))
    headline = "D-R1 stopped before confirmation"
    lines = [
        "# Study D-R1 — recurrent associative retrieval",
        "",
        "The frozen [protocol](../docs/STUDY_D_R1_PROTOCOL.md) tests PH768 projection memory,",
        "with same-weights PH-1, NOWRITE, KV, REG, FAST and REG-LIFT controls.",
        "",
    ]
    decision = ["# Study D-R1 decision", ""]
    if not complete:
        failures = {k: v for k, v in phases.items() if v["status"] != "complete"}
        lines += [
            "**No confirmation claim is available.**",
            "",
            "Execution stopped at a frozen preconfirmation boundary. The phase receipts",
            "distinguish scientific competence, resource feasibility and invalid execution.",
            "",
            "```json",
            json.dumps(failures, indent=2),
            "```",
            "",
        ]
        if (OUT / "fixture/projection.json").exists():
            lines += [
                "Resource projection:",
                "",
                "```json",
                json.dumps(read(OUT / "fixture/projection.json"), indent=2),
                "```",
                "",
            ]
        development = list((OUT / "development").glob("*/**/result.json"))
        if development:
            lines += [
                "Development-only PH768 isolated acquisition:",
                "",
                "| Root | Full accuracy at eight | Partial accuracy at eight |",
                "| --- | ---: | ---: |",
            ]
            for path in development:
                row = read(path)
                if row["group"] == "PH-FULL":
                    metrics = row["results"]["PH-FULL"]["metrics"]
                    lines.append(
                        f"| {row['root']} | {metrics['full']['accuracy8']:.5f} | {metrics['partial']['accuracy8']:.5f} |"
                    )
        decision += [
            "**Revise: the v1 execution stopped before confirmation.**",
            "",
            "No useful-settling or reliable-component hypothesis is confirmed or falsified",
            "by a resource/software stop. A development competence failure applies only",
            "to this fixed candidate under its supplied encoding and budget.",
            "",
            "Recommend one fresh corrective feasibility/protocol review addressing the",
            "recorded stopping cause before any additional numerical execution. Do not",
            "extend this allocation, replace roots or activate another research branch.",
        ]
        dump(REPORT / "outcome.json", {"complete_confirmation": False, "failures": failures})
    else:
        receipt = read(OUT / "freeze/receipt.json")
        rows = {name: [] for name in m["arms"]}
        verified = {"repeat_arrays": 0, "independent_metrics": 0, "source_files": 0}
        for root in m["confirmation_roots"]:
            fit = read(OUT / "confirmation" / str(root) / "fit/fit.json")
            for name in m["arms"]:
                group = "PH-FULL" if name == "PH-1" else name
                path = OUT / "confirmation" / str(root) / group
                result = read(path / "result.json")["results"][name]
                with np.load(path / f"{name}.npz") as a:
                    recalculated = independent_metrics(
                        a, fit["normalization"], receipt["thresholds"][name]
                    )
                    raw = independent_metrics(
                        a, fit["normalization"], {c: 1e30 for c in CONDITIONS}
                    )
                    for c in CONDITIONS:
                        for k, v in raw[c].items():
                            old = result["metrics"][c][k]
                            if v is None:
                                assert old is None
                            else:
                                assert np.isclose(v, old, atol=1e-12, rtol=1e-12), (
                                    name,
                                    root,
                                    c,
                                    k,
                                )
                            verified["independent_metrics"] += 1
                rows[name].append({**result, "root": root, "metrics": recalculated})
            budget.check()
        for group in GROUPS:
            original = OUT / "confirmation" / str(m["repeat_root"]) / group
            repeat = OUT / "repeat" / str(m["repeat_root"]) / group
            for path in original.glob("*.npz"):
                with np.load(path) as x, np.load(repeat / path.name) as y:
                    assert set(x.files) == set(y.files)
                    for key in x.files:
                        if key == "trace_elapsed":
                            continue
                        assert np.array_equal(x[key], y[key]), (group, path.name, key)
                        verified["repeat_arrays"] += 1
            assert tensor_hash(
                torch.load(original / "last-memory.pt", weights_only=True)
            ) == tensor_hash(torch.load(repeat / "last-memory.pt", weights_only=True))
        x = OUT / "confirmation" / str(m["repeat_root"]) / "fit/core.pt"
        y = OUT / "repeat" / str(m["repeat_root"]) / "fit/core.pt"
        assert tensor_hash(torch.load(x, weights_only=True)) == tensor_hash(
            torch.load(y, weights_only=True)
        )
        for rel, expected in receipt["source"]["hashes"].items():
            assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == expected
            verified["source_files"] += 1
        stats = statistics(rows, m)
        dump(REPORT / "root-results.json", rows)
        dump(REPORT / "statistics.json", stats)
        dump(REPORT / "verification.json", verified)
        headline = stats["settling_outcome"]
        lines += [
            f"**Additional nonlinear settling: {headline}.**",
            "",
            f"Reliable PH768 retrieval conjunction: **{stats['reliable_retrieval']}**.",
            "",
            "Ten independent roots; paired root-bootstrap intervals use the frozen",
            "12-quantity Bonferroni family. Nested queries are not independent roots.",
            "",
            "| Contrast | Mean | Adjusted interval | Outcome |",
            "| --- | ---: | --- | --- |",
        ]
        for name, x in [
            ("PH-FULL minus PH-1", stats["primary"]),
            *[(f"PH-FULL minus {r}", v) for r, v in stats["secondary"].items()],
        ]:
            lines.append(
                f"| {name} | {x['mean']:.5f} | [{x['lo']:.5f}, {x['hi']:.5f}] | {x.get('outcome', headline)} |"
            )
        lines += [
            "",
            "| PH768 guard | Mean | Adjusted interval | Pass |",
            "| --- | ---: | --- | --- |",
        ]
        for name, x in stats["guards"].items():
            lines.append(
                f"| {name} | {x['mean']:.5f} | [{x['lo']:.5f}, {x['hi']:.5f}] | {x['pass']} |"
            )
        lines += [
            "",
            "| Arm | Partial old accuracy | Full old accuracy | Persistent bytes | Serial recall us |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
        for name, rr in rows.items():
            lines.append(
                f"| {name} | {np.mean([r['metrics']['partial']['old_accuracy'] for r in rr]):.5f} | "
                f"{np.mean([r['metrics']['full']['old_accuracy'] for r in rr]):.5f} | "
                f"{rr[0]['resources']['persistent_bytes']} | {np.mean([r['serial_recall_us_mean'] for r in rr]):.2f} |"
            )
        lines += [
            "",
            "PH-1 shares the acquired checkpoint; its trace records first-cycle cost.",
            "The current serial-latency table uses the full retrieval profiling path for",
            "that shared arm; it is not an independent measured PH-1 speed comparison.",
            "",
            "![Acquisition](study-d-r1/acquisition.png)",
            "![Retention](study-d-r1/retention.png)",
            "![Settling](study-d-r1/settling.png)",
            "",
            "Full calibrated root metrics, acceptance denominators and descriptive uncertainty",
            "are in [root results](study-d-r1/root-results.json) and [statistics](study-d-r1/statistics.json).",
            "Zero-width boundary intervals describe this finite sample, not zero population risk.",
            "",
            (
                f"Verification: {verified['repeat_arrays']} numerical arrays repeat exactly; "
                f"{verified['independent_metrics']} endpoints independently reconstructed."
            ),
        ]
        plots(m, rows)
        failures = []
        for name in m["arms"]:
            group = "PH-FULL" if name == "PH-1" else name
            worst = (-1, None)
            for root in m["confirmation_roots"]:
                with np.load(OUT / "confirmation" / str(root) / group / f"{name}.npz") as a:
                    err = a["d2_error"][1, :, 7, :7, :, 0]
                    i = np.unravel_index(err.argmax(), err.shape)
                    if err[i] > worst[0]:
                        worst = (
                            float(err[i]),
                            {
                                "arm": name,
                                "root": root,
                                "sequence": int(i[0]),
                                "object": int(i[1]),
                                "query": int(i[2]),
                                "canonical_nmse": float(err[i]),
                            },
                        )
            failures.append(worst[1])
        dump(REPORT / "failures.json", failures)
        decision += [
            f"**Accept the bounded v1 evidence: {headline}.**",
            "",
            f"Candidate reliable-retrieval conjunction: {stats['reliable_retrieval']}.",
            "",
            "Keep persistent storage, correct retrieval, causal benefit from additional",
            "settling and complete-system resource comparisons separate. The protocol",
            "does not require a KV win for a component result. No shared-neuron, learned",
            "organization, biological or general capacity claim follows.",
            "",
            "Recommend one targeted diagnostic protocol for the dominant failing guard",
            "or unresolved settling contrast, using fresh streams; do not execute it.",
            "If no guard fails, the next review should select one scaffold-removal test.",
        ]
    historical = read(ROOT / "reports/study-d/source.json")
    hashes = historical.get("hashes", historical.get("source", {}).get("hashes", {}))
    assert hashes, "Historical D source receipt missing hashes"
    for rel, expected in hashes.items():
        assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == expected, rel
    lines += [
        "",
        f"Source commit: `{provenance['commit']}`; fingerprint `{provenance['aggregate']}`.",
        f"All {len(hashes)} historical D source hashes remain unchanged.",
        "Fresh allocation: 7200 CPU / 14400 execution wall seconds, 2 GiB RSS/artifacts.",
        "Numerical fixtures, failures, development, calibration, confirmation, repeat and",
        "reporting are charged cumulatively; process import/startup and engineering are separate.",
        "Final resource and phase receipts are exported after reporting completes.",
        "",
        "The memory uses supplied threshold encoding, fixed clamped cues, an offline-fitted",
        "action basis and hand-assigned roles. Projection stability and decreasing energy",
        "alone do not establish correct completion or useful attractors. All historical",
        "gates remain unchanged. No later experiment or publication was executed.",
    ]
    (ROOT / "reports/STUDY_D_R1.md").write_text("\n".join(lines) + "\n")
    (ROOT / "reports/STUDY_D_R1_DECISION.md").write_text("\n".join(decision) + "\n")
    dump(
        REPORT / "archive-index.json",
        {
            str(p.relative_to(OUT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in OUT.rglob("*")
            if p.is_file() and p.name not in {"phase-status.json", "ledger.json"}
        },
    )
    dump(
        dest / "report-result.json",
        {
            "headline": headline,
            "confirmation_complete": complete,
            "historical_source_hashes_verified": len(hashes),
            "artifact_bytes_before_final_export": size(OUT) + size(REPORT),
            "report_cpu_seconds_so_far": time.process_time() - budget.cpu,
        },
    )


def plots(m, rows):
    fig, ax = plt.subplots(figsize=(8, 4))
    for name in m["arms"]:
        curves = []
        group = "PH-FULL" if name == "PH-1" else name
        for root in m["confirmation_roots"]:
            with np.load(OUT / "confirmation" / str(root) / group / f"{name}.npz") as a:
                curves.append((a["d1_error"][1, :, :, :, 0] <= 0.1).mean((1, 2)))
        ax.plot([0, 1, 2, 4, 8], np.mean(curves, 0), marker="o", label=name)
    ax.set(
        xlabel="Distinct grounded snapshots", ylabel="Raw partial-cue accuracy", ylim=(-0.03, 1.03)
    )
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(REPORT / "acquisition.png", dpi=160)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4))
    for name in m["arms"]:
        curves = []
        group = "PH-FULL" if name == "PH-1" else name
        for root in m["confirmation_roots"]:
            with np.load(OUT / "confirmation" / str(root) / group / f"{name}.npz") as a:
                curves.append((a["d2_error"][1, :, 7, :, :, 0] <= 0.1).mean((0, 2))[::-1])
        ax.plot(range(8), np.mean(curves, 0), marker="o", label=name)
    ax.set(
        xlabel="Later objects acquired since this object",
        ylabel="Final raw partial-cue accuracy",
        ylim=(-0.03, 1.03),
    )
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(REPORT / "retention.png", dpi=160)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4))
    curves = []
    for root in m["confirmation_roots"]:
        with np.load(OUT / "confirmation" / str(root) / "PH-FULL/PH-FULL.npz") as a:
            ids = a["trace_ids"]
            mask = (ids[:, 0] == 1) & (ids[:, 1] == 1) & (ids[:, 3] == 7) & (ids[:, 4] < 7)
            den = next(r["normalization"] for r in rows["PH-FULL"] if r["root"] == root)
            err = ((a["trace_values"][mask] - a["trace_truth"][mask, None]) ** 2).mean(-1) / den
            curves.append((err <= 0.1).mean((0, 2)))
    ax.plot(range(1, 33), np.mean(curves, 0), marker=".")
    ax.set(
        xlabel="Complete settling cycles (stopped paths padded)",
        ylabel="Final earlier-object partial-cue accuracy",
        ylim=(-0.03, 1.03),
    )
    fig.tight_layout()
    fig.savefig(REPORT / "settling.png", dpi=160)
    plt.close(fig)
