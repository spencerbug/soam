"""SOAM-052 read-only audit of sealed E1 evidence; no fitting or new evaluation."""
import time

START_CPU, START_WALL = time.process_time(), time.perf_counter()
import hashlib
import json
import resource
import subprocess
from pathlib import Path

import numpy as np
import torch

from soam.platform.runner import read_arrays
from soam.shared.archive import InputStore
from soam.shared.continuation import audit_development, current_calibration, tree_identity
from soam.shared.data import stream
from soam.shared.execution import FAMILIES, cell_inventory, compare_repeat, same_outputs
from soam.shared.fitting import FitPlan, exposure_counts
from soam.shared.models import ROOT, manifest
from soam.shared.runner import Config
from soam.shared.study_summary import aggregate

torch.set_num_threads(1)
torch.use_deterministic_algorithms(True)
OUT = ROOT / "reports/shared-population-gate"
assert not (OUT / "audit.json").exists(), "Keep prior gate audits; do not overwrite"
COMPACT = ROOT / "reports/shared-population-study/confirmation"
RAW = ROOT / "runs/e1-confirmation-v1-a1"
read = lambda path: json.loads(path.read_text())
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
protocol = manifest()
previous = read(COMPACT / "final-ledger.json")


def check():
    elapsed = time.process_time() - START_CPU
    assert previous["overhead_cpu_seconds"] + elapsed < 1200
    assert previous["cpu_seconds"] + elapsed < 14400
    assert previous["wall_seconds"] + time.perf_counter() - START_WALL < 28800
    assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < 2 * 1024**3


checked_files = {}
for phase in ("development", "continuation", "confirmation"):
    folder = ROOT / "reports/shared-population-study" / phase
    for name, expected in read(folder / "sha256.json").items():
        actual = sha(folder / name)
        assert actual == expected, (phase, name)
        checked_files[str((folder / name).relative_to(ROOT))] = actual
calibration, _, _ = current_calibration(ROOT / "runs/e1-continuation-calibration-v1")
development = audit_development()
audit = read(COMPACT / "audit.json")
assert tree_identity(RAW) == audit["raw_archive"]
for name in ("config.json", "provenance.json", "inventory.json", "result.json", "reproduction.json", "status.json"):
    assert sha(RAW / name) == sha(COMPACT / name), name
record = read(RAW / "provenance.json")
assert record["source_files"] == calibration["source_files"]
assert record["source_sha256"] == calibration["source_sha256"]
for name, digest in record["source_files"].items():
    at_run = subprocess.run(["git", "show", record["commit"] + ":" + name], cwd=ROOT, capture_output=True, check=True).stdout
    assert hashlib.sha256(at_run).hexdigest() == digest == sha(ROOT / name), name
config = read(RAW / "config.json")
canonical_hash = lambda value: hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
assert canonical_hash(config) == audit["resolved_study_config_sha256"]
assert canonical_hash(Config(archive_revision="a1").to_dict()) == record["config_sha256"] == audit["capture_wrapper_config_sha256"]
assert not config["fixture"]
assert config["selected_configs"] == development["screen"]["selected_configs"]
assert config["budget"] == protocol["budget"] and config["inventory"] == protocol["inventory"]
assert read(ROOT / "runs/e1-confirmation-readiness-v1/execution-claim.json")["source"] == record["source_sha256"]
check()

roots = {}
fit_count = cell_count = training_ref_count = evaluation_ref_count = 0
isolation_arrays = {k: 0 for k in ("T32_intact", "T32_opposite_bank", "D16_opposite_bank")}
fit_cpu = []
for phase, seeds in (("confirmation", protocol["streams"]["confirmation_roots"]), ("repeat", [11])):
    for seed in seeds:
        check()
        root = RAW / phase / str(seed)
        result = read(root / "result.json")
        assert set(result["cells"]) == set(cell_inventory())
        assert all(row["status"] == "complete" for row in result["cells"].values())
        assert set(result["fits"]) == set(FAMILIES)
        assert all(row["status"] == "complete" for row in result["fits"].values())
        cell_count += len(result["cells"])
        if phase == "confirmation":
            roots[seed] = read(root / "summary.json")
        base_refs = {f.parent.name: read(f) for f in (root / "fits/S32/data").glob("*/input-ref.json")}
        assert len(base_refs) == 700
        selection = read(root / "selection.json")
        assert selection["selection_split"] == "development_diagnostic"
        assert (root / "selection.json").stat().st_mtime_ns <= min(f.stat().st_mtime_ns for f in (root / "evaluation-data").glob("*/input-ref.json"))
        for family in FAMILIES:
            folder = root / "fits" / family
            fit = read(folder / "fit.json")
            assert fit["exposure"] == exposure_counts(FitPlan()) and not fit["fixture_only"]
            assert len(fit["trace"]) == 400 and fit["cpu_seconds"] < 90
            fit_cpu.append(fit["cpu_seconds"])
            if family == "L12":
                assert fit["trace"][-1]["L_records"] == 6400 and fit["trace"][-1]["B_pairs"] == 38400
            refs = {f.parent.name: read(f) for f in (folder / "data").glob("*/input-ref.json")}
            assert refs == base_refs, (phase, seed, family)
            training_ref_count += len(refs)
            fit_count += 1
            for role in ("recall_pre", "recall_final", "transition"):
                for index in range(20):
                    data_role = "transition" if role == "transition" else "recall"
                    base = read(root / "evaluation-data" / f"{data_role}-{index}" / "input-ref.json")
                    cell = root / "cells" / f"{family}-{role}-{index}"
                    assert read(cell / "inputs/input-ref.json") == base
                    exposure = read(cell / "record.json")["exposure"]
                    assert exposure["free_future_observation_reads"] == exposure["fitting_updates"] == 0
                    evaluation_ref_count += 1
        for role in ("recall", "transition"):
            for index in range(20):
                suffix = "recall_final" if role == "recall" else "transition"
                arrays = lambda name: read_arrays(root / "cells" / name / "arrays.npz")
                s = arrays(f"S32-{suffix}-{index}")
                t = arrays(f"T32-intact-{role}-{index}")
                d = arrays(f"D16-{suffix}-{index}")
                opposite = 1 if role == "recall" else 0
                for key, a, b in (("T32_intact", s, t), ("T32_opposite_bank", t, arrays(f"T32-bank-{opposite}-{role}-{index}")), ("D16_opposite_bank", d, arrays(f"D16-bank-{opposite}-{role}-{index}"))):
                    same_outputs(a, b)
                    isolation_arrays[key] += 1 + (role == "transition")
assert (fit_count, cell_count) == (77, 25300)
computed = aggregate(roots)
stored = read(RAW / "result.json")
for key, value in computed.items():
    expected = stored[key]
    if key == "root_summaries":
        expected = {int(k): v for k, v in expected.items()}
    assert value == expected, key
# Directly reconstruct contrasts and bootstrap, independently of aggregate/classify.
refs = protocol["comparisons"]["required_references"]
utility = []
recall_roots = []
for root in roots.values():
    m = root["condition_means"]
    s = m["S32-transition"]["free8_nmse"]
    recall = m["S32-recall_final"]["recall_nmse"]
    recall_roots.append(recall)
    utility.append([(m[f"{f}-transition"]["free8_nmse"] - s) / m[f"{f}-transition"]["free8_nmse"] for f in refs] + [recall - m["S32-recall_pre"]["recall_nmse"], recall - m["D25-recall_final"]["recall_nmse"]])
assert utility == stored["utility_root_contrasts"]
rng = np.random.Generator(np.random.PCG64(stream("inference", 8675309, 0, "inference-resampling")))
indices = rng.integers(0, 10, size=(10000, 10))
for key, size in (("utility", 7), ("causal", 6)):
    samples = np.asarray(stored[key + "_root_contrasts"])[indices].mean(1)
    for label, q in (("lower", .05 / (2 * size)), ("upper", 1 - .05 / (2 * size)), ("ordinary_lower", .025), ("ordinary_upper", .975)):
        assert np.array_equal(np.quantile(samples, q, axis=0, method="linear"), stored[key][label])
assert min(recall_roots) > .02
assert stored["guardrail_pass"] and stored["outcome"] == "recall_interference_or_failure"
repeat = compare_repeat(RAW / "confirmation/11", RAW / "repeat/11", InputStore(RAW / "input-objects"), check)
assert repeat == read(RAW / "reproduction.json")
assert abs(previous["development_cpu_seconds"] + sum(previous["phase_cpu_seconds"].values()) + previous["overhead_cpu_seconds"] - previous["cpu_seconds"]) < 1e-9
assert sum(row["cpu_seconds_upper_charge"] for row in read(COMPACT / "audit-attempts.json")) == 221
check()

review_cpu, review_wall = time.process_time() - START_CPU, time.perf_counter() - START_WALL
rolled = {
    "cpu_seconds": previous["cpu_seconds"] + review_cpu + 2,
    "wall_seconds": previous["wall_seconds"] + review_wall + 2,
    "overhead_cpu_seconds": previous["overhead_cpu_seconds"] + review_cpu + 2,
    "artifact_bytes": previous["artifact_bytes"] + 131072,
    "peak_rss_bytes_measured": max(previous["peak_rss_bytes"], resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
    "gate_metadata_cpu_wall_reserve_seconds": 2,
    "gate_report_storage_reserve_bytes": 131072,
    "note": "Conservative decision-audit continuation only; no new fit allocation. SOAM-051 ledger remains unchanged. Prior incomplete reporting-attempt RSS remains unknown. Tests/local-worker review are engineering review, outside trial ledger as previously declared.",
}
assert rolled["cpu_seconds"] < 14400 and rolled["wall_seconds"] < 28800 and rolled["overhead_cpu_seconds"] < 1200 and rolled["artifact_bytes"] < 8 * 1024**3
result = {
    "review_ticket": "SOAM-052", "date": "2026-11-08", "review_base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "new_fits": 0, "new_observations": 0, "new_conditions": 0,
    "checked_compact_hashes": checked_files, "development_archive": development["archive"], "confirmation_archive": audit["raw_archive"],
    "scientific_source_commit": record["commit"], "source_sha256": record["source_sha256"],
    "source_files_verified": len(record["source_files"]), "capture_wrapper_config_sha256": record["config_sha256"], "resolved_study_config_sha256": canonical_hash(config),
    "preserved_configs": config["selected_configs"], "primary_reference": development["screen"]["primary_reference"],
    "all_77_training_fit_inputs_paired": True, "training_references_compared": training_ref_count,
    "base_evaluation_references_compared": evaluation_ref_count, "selection_before_confirmation": True,
    "fit_count": fit_count, "cell_count": cell_count, "fit_cpu_max": max(fit_cpu), "fit_cpu_sum": sum(fit_cpu),
    "isolation_prediction_arrays_exact": isolation_arrays, "reproduction": repeat,
    "bootstrap_adjusted_and_ordinary_bounds_exact": True,
    "root_order": list(roots), "candidate_recall_min_max": [min(recall_roots), max(recall_roots)],
    "frozen_outcome": stored["outcome"], "absolute_recall_mean": stored["absolute_recall_mean"],
    "absolute_transition_mean": stored["absolute_transition_mean"], "guardrail_pass": stored["guardrail_pass"],
    "utility": stored["utility"], "causal": stored["causal"], "causal_pass": stored["causal_pass"], "causal_precise_failure": stored["causal_precise_failure"], "recovery": stored["recovery"],
    "review_cpu_seconds": review_cpu, "review_wall_seconds": review_wall, "conservative_cumulative_ledger": rolled,
    "reporting_limitations_retained": ["Capture-wrapper hash is not resolved-study config hash", "L12 generic loss fields are not gradient iterations", "Two incomplete reporting attempts charged with conservative elapsed bounds; separate peak RSS unknown; first terminal diagnosis not retained"],
    "worker": {"job": "560aa77ad2dc464f80ece38f35dde2b6", "disposition": "Rejected: false missing-telemetry/config-explanation claims and no usable source citations. Primary direct audit used."},
}
(OUT / "audit.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"outcome": stored["outcome"], "source": record["source_sha256"], "raw_archives_unchanged": True, "repeat": repeat, "ledger": rolled}, indent=2))
