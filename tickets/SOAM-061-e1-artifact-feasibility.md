---
schema_version: 2
id: "SOAM-061"
title: "Resolve E1 artifact feasibility before scientific fitting"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-00", "WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-049", "SOAM-050"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-05"
updated: "2026-11-06"
github_issue: null
decision: "proceed"
---

# SOAM-061: Resolve E1 artifact feasibility before scientific fitting

## Recommended thinking

**high** — Separate a conservative storage-layout failure from scientific infeasibility,
preserve v1 evidence, and verify a complete reproducible inventory before authorizing fitting.

## Problem / hypothesis

SOAM-050's v1 calibration projected 12,680,048,016 artifact bytes with the required
2× margin, exceeding 8 GiB. Compute, phase, per-fit and RSS projections passed.
This is a failed engineering feasibility check, not a negative scientific result.
The [report](../reports/SHARED_POPULATION_HARNESS.md) and
[original cost ledger](../reports/shared-population-harness/preflight-cost-ledger.json)
retain its exact source, timing samples, formulas and result.
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- **Essential next:** decide a bounded correction under the v1 failure rule; do not
  change the old ledger, protocol or SOAM-049's historical proceed decision.
- Review artifact accounting and layout first. The conservative projection stores
  repeated paired inputs per fit, including repeated recall observations, and uses
  a maximum-width transition payload for every cell. Consider content-addressed
  shared input archives with exact references/replay and narrower per-condition
  accounting; do not assume compression of unfitted zeros predicts learned data.
- Freeze the chosen archive/replay/ledger contract in a fresh protocol/manifest
  version or explicit corrective versioned addendum before a replacement calibration.
  Preserve all 119 fit instances, 27,820 cells, seeds, baselines, scientific thresholds
  and budgets unless a separately justified protocol amendment explicitly changes them.
- Implement and test the selected reversible storage correction within this bounded
  decision task if needed to make the decision concrete; rerun the full-inventory
  shape-equivalent calibration. No scientific fitting or pilot results in this task.
- Decide proceed/revise/stop. Proceed requires all original ceilings with the 2×
  margin, archive integrity and replay verification. A second failure remains a failure.

## Acceptance criteria

- [x] Preserve and cite the failed v1 ledger; explain overestimation versus actual storage costs.
- [x] Specify versioned archive ownership, deduplication references, collision/integrity checks,
  replay restoration and failed-run accounting before applying a correction.
- [x] Test the revised archive format and project every fit/cell, checkpoints, inputs,
  outputs, metadata, repeats and failures using measured sizes and explicit upper bounds.
- [x] Record source/config/software, ten timings after one warm-up, all ceiling checks,
  and the decision even if it remains negative. No silent trial reduction or cap increase.
- [x] Update SOAM-051 readiness and protocol links only after proceed and a passing ledger.

## Metrics / evidence

Existing evidence: [SOAM-050 report](../reports/SHARED_POPULATION_HARNESS.md),
[cost ledger](../reports/shared-population-harness/preflight-cost-ledger.json).
Required ceilings: 90 CPU seconds per fit; phase CPU 4,000/8,000/1,200 seconds;
14,400 CPU / 28,800 wall seconds total; 2 GiB RSS; 8 GiB artifacts.
Calibration remains inside 120 CPU / 240 wall seconds and 256 MiB artifacts.

## Dependencies

- [SOAM-049](SOAM-049-shared-population-protocol.md) — historical v1 protocol proceed; preserve it.
- [SOAM-050](SOAM-050-shared-population-candidates.md) — delivered harness and failed storage projection.

## Completion record

Completed 2026-11-06 with `decision: "proceed"` for E1 scientific v1 plus
[archive addendum A1](../docs/E1_ARCHIVE_A1.md). The [decision report](../reports/E1_ARCHIVE_A1.md)
and [new cost ledger](../reports/e1-archive-a1/preflight-cost-ledger.json) preserve
all original scientific conditions and the old failed ledger. New storage projection:
5,661,352,816 bytes with 2× margin; every original ceiling passes.

Baseline 171 tests passed in 16.03s; final `UV_CACHE_DIR=/tmp/soam-uv-cache uv run pytest`:
173 passed in 16.71s. Ruff checks pass. A1 fixture: 181 cells per execution,
1,344 exactly repeated output/checkpoint arrays, nine verified shared input objects.
The first fixture's old-path replay error is retained and explained in the report.
Replacement calibration used ten timings after one warm-up, zero optimizer updates,
and complete 119-fit/27,820-cell projections. Both successful runs share source
fingerprint `6a857bb877d222cb1c7da7c3a4bde9753687e3883b06806d1ba3d697835becd3`.
SOAM-051 is ready under v1+A1; no scientific pilot or new research fork ran.
