"""Final provenance/reduction audit and transparent post hoc recovery repair."""

import hashlib
import json
import resource
import sys
import time
from pathlib import Path

import numpy as np
import torch

from soam.temporal.data import CONDITIONS, SCHEDULES, generate, input_hash, training_data
from soam.temporal.magnitude import identity, mapped_root
from soam.temporal.runner import dump, size
from soam.temporal.statistics import interval


def repaired_recovery(errors, resume, disruption):
    baseline = errors[max(0, disruption - 8) : disruption].mean(0)
    threshold = np.maximum(0.01, 2 * baseline)
    times = np.full(errors.shape[1], errors.shape[0] - resume, dtype=float)
    censored = np.ones(errors.shape[1], dtype=bool)
    for t in range(resume, len(errors) - 2):
        ok = (errors[t : t + 3] <= threshold).all(0) & censored
        times[ok] = t - resume
        censored[ok] = False
    return float(times.mean()), float(censored.mean())


def main():
    start = time.process_time()
    wall = time.monotonic()
    torch.set_num_threads(1)
    root = Path(__file__).resolve().parents[1]
    output = root / "runs/study-b-magnitude-v1"
    dest = root / "reports/study-b-magnitude"
    m = json.loads((output / "manifest.json").read_text())
    receipt = json.loads((output / "confirmation-receipt.json").read_text())
    assert receipt["source"] == identity()["aggregate"]
    old_source = json.loads((root / "runs/study-b-v1/source.json").read_text())
    assert all(
        hashlib.sha256((root / p).read_bytes()).hexdigest() == h
        for p, h in old_source["hashes"].items()
    )
    provenance = {}
    audit = []
    for r in m["confirmation_roots"]:
        data = training_data(mapped_root(r))
        hashed = input_hash(data)
        exposure = {
            "episodes": len(data) * 8,
            "supervisory_observations": len(data) * 8 * 17,
            "sensory_events": sum(int(b.evidence.mask.any(-1).sum()) for b in data),
            "feature_values": sum(int(b.evidence.mask.sum()) for b in data),
        }
        del data
        hashes = {
            c + "/" + s: input_hash(
                [generate("confirmation", mapped_root(r), condition=c, schedule=s)]
            )
            for c in CONDITIONS
            for s in SCHEDULES
        }
        provenance[str(r)] = {
            "effective_root": mapped_root(r),
            "train": hashed,
            "evaluation": hashes,
            "exposure": exposure,
        }
        for name in m["candidates"]:
            d = output / "confirmation" / str(r) / name / str(receipt["selection"][name]["setting"])
            assert json.loads((d / "fit.json").read_text())["input_hash"] == hashed
            h = json.loads((d / "evaluation.json").read_text())["headline"]
            with np.load(d / "errors.npz") as arrays:
                values = {
                    c: np.mean(
                        [
                            arrays[f"{c}__{s}__prior"].astype(float).mean()
                            for s in SCHEDULES
                            if s != "initial"
                        ]
                    )
                    for c in CONDITIONS
                }
                values["J"] = np.mean(
                    [
                        arrays[f"{c}__{s}__prior"].astype(float).mean()
                        for c in ("partial", "missing", "noise")
                        for s in ("every2", "every4", "every8", "irregular")
                    ]
                )
                for horizon in (8, 32):
                    values[f"free{horizon}"] = (
                        arrays["partial__initial__prior"][:horizon].astype(float).mean()
                    )
            for key, value in values.items():
                assert abs(value - h[key]) < 1e-7
                audit.append(
                    {
                        "root": r,
                        "name": name,
                        "metric": key,
                        "recomputed": float(value),
                        "stored": h[key],
                    }
                )
    dump(dest / "data-provenance.json", provenance)
    dump(dest / "independent-reduction.json", audit)
    recovery = {}
    for label, path in [("v1", root / "runs/study-b-v1"), ("magnitude", output)]:
        manifest = json.loads((path / "manifest.json").read_text())
        rec = json.loads((path / "confirmation-receipt.json").read_text())
        models = {}
        for name in manifest["candidates"]:
            cells = {}
            for condition in ("corrupt", "contradict", "change", "gap"):
                for schedule in SCHEDULES:
                    rows = []
                    for r in manifest["confirmation_roots"]:
                        p = (
                            path
                            / "confirmation"
                            / str(r)
                            / name
                            / str(rec["selection"][name]["setting"])
                            / "errors.npz"
                        )
                        with np.load(p) as arrays:
                            errors = arrays[f"{condition}__{schedule}__posterior"].astype(float)
                        disruption = 17 if condition == "gap" else 24
                        resume = 49 if condition == "gap" else 24 if condition == "change" else 32
                        rows.append(repaired_recovery(errors, resume, disruption))
                    cells[condition + "/" + schedule] = {
                        "capped_steps": interval([r[0] for r in rows]),
                        "censored_fraction": interval([r[1] for r in rows]),
                    }
            models[name] = cells
        recovery[label] = models
    dump(
        root / "reports/study-b/recovery-pre-disruption.json",
        {
            "classification": "Post hoc descriptive reporting repair. Original recovery.json and raw evaluation records are preserved. Their baseline immediately before recovery could include corruption/gap error. This analysis uses the eight physical steps before disruption (24 for corruption/contradiction/change, 17 for gaps), and starts the recovery clock at clean-data resumption (32/49) or genuine change (24). No primary endpoint or decision changes.",
            "versions": recovery,
        },
    )
    repeat = json.loads((output / "reproduction.json").read_text())
    assert all(all(v.values()) for v in repeat.values())
    summary = {
        "supplement_recomputed_values": len(audit),
        "training_and_evaluation_hashes_saved": True,
        "original_source_dependencies_unchanged": True,
        "all_primary_and_guard_values_match": True,
        "repeat_checks": sum(len(v) for v in repeat.values()),
        "repeat_exact": True,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    dump(dest / "extended-audit.json", summary)
    # The supplement ledger already includes the complete v1 allocation, exactly once.
    ledger = json.loads((output / "ledger.json").read_text())
    ledger.append(
        {
            "phase": "final-audit",
            "status": "complete",
            "cpu_seconds": time.process_time() - start,
            "wall_seconds": time.monotonic() - wall,
            "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            * (1 if sys.platform == "darwin" else 1024),
            "error": None,
        }
    )
    plot = root / "reports/study-b/plot-verification.json"
    if plot.exists():
        p = json.loads(plot.read_text())
        ledger.append(
            {
                "phase": "final-presentation",
                "status": "complete",
                "cpu_seconds": p["cpu_seconds"],
                "wall_seconds": p["wall_seconds"],
                "error": None,
            }
        )
    dump(output / "ledger.json", ledger)
    total_bytes = sum(
        size(root / p)
        for p in (
            "runs/study-b-v1",
            "runs/study-b-magnitude-v1",
            "reports/study-b",
            "reports/study-b-magnitude",
        )
    )
    measured_counts = {}
    failures = 0
    for label, path in [("v1", root / "runs/study-b-v1"), ("supplement", output)]:
        statuses = [json.loads(p.read_text())["status"] for p in path.glob("*/*/*/*/status.json")]
        measured_counts[label] = len(statuses)
        failures += statuses.count("failed")
        assert all(s in {"complete", "fit complete"} for s in statuses)
    assert measured_counts == {"v1": 256, "supplement": 112}
    result = {
        "cpu_seconds": sum(v["cpu_seconds"] for v in ledger),
        "execution_wall_seconds": sum(v["wall_seconds"] for v in ledger),
        "peak_rss_bytes": max(v.get("peak_rss_bytes", 0) for v in ledger),
        "artifact_bytes": total_bytes,
        "fits": sum(measured_counts.values()),
        "v1_fits": measured_counts["v1"],
        "supplement_fits": measured_counts["supplement"],
        "failed_fits": failures,
        "cpu_cap": 7200,
        "wall_cap": 14400,
        "rss_cap": 2147483648,
        "artifact_cap": 2147483648,
        "ledger": ledger,
        "notes": "Counts v1 once via the carried ledger. Tests/local language-model work are engineering outside scientific compute. Process import/source-copy setup precedes phase timing. Reported bytes include raw and compact result duplicates.",
    }
    assert (
        result["cpu_seconds"] < 7200
        and result["execution_wall_seconds"] < 14400
        and result["peak_rss_bytes"] < 2147483648
        and total_bytes < 2147483648
    )
    dump(root / "reports/study-b/resource-final.json", result)
    print(json.dumps({**summary, **{k: v for k, v in result.items() if k != "ledger"}}), flush=True)


if __name__ == "__main__":
    main()
