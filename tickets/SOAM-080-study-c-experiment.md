---
schema_version: 2
id: "SOAM-080"
title: "Measure explicit candidate states on fresh ambiguity streams"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-078", "SOAM-079"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-14"
updated: "2026-11-14"
github_issue: null
decision: null
---

# SOAM-080: Measure explicit candidate states on fresh ambiguity streams

## Recommended thinking

**high** — Separate observability, retained state capacity, estimator competence and resource costs in the bounded C-H1 comparison.

## Problem / hypothesis

Does retaining two candidate states improve calibrated delayed inference beyond competent single-state controls? C-H1 operationalizes H1/H6; C-H2 scheduling and C-H3 learned allocation are separate, conditional questions.

## Scope

Follow the [owner request](../docs/requests/study_c_2026_11_14.md) and [C v1 protocol](../docs/STUDY_C_PROTOCOL.md). Only the first two-explanation experiment is selected. Preserve historical E1/A/B/B2 decisions.

## Acceptance criteria

- [x] Deliver this phase with reproducible evidence or an explicit negative, inconclusive or invalid outcome.
- [x] Enforce evidence parity, full-history ambiguity, pre-correction scoring and no-write inference.
- [x] Account for all mandatory neural/conventional controls, capacity, uncertainty and resources.
- [x] Record actual checks, provenance and the effect on subsequent eligibility.

## Metrics / evidence

Primary binary Brier score, paired independent-root intervals, ambiguity/accuracy/recovery guards, state and parameter counts, mean/p95 latency. The protocol owns the frozen contract and numerical manifest.

## Dependencies

- [SOAM-078](SOAM-078-study-c-protocol.md) — completed prerequisite; decisions require proceed.
- [SOAM-079](SOAM-079-study-c-harness.md) — completed prerequisite; decisions require proceed.

## Branch conditions

The November 14 owner request and SOAM-078 select C-H1 only. SOAM-077's baseline recommendation is satisfied; SOAM-078 must accept the contract before implementation. SOAM-079 must verify invariants and feasibility before development/confirmation. SOAM-037 remains backlog under the failed SOAM-052 sharing gate. SOAM-053 is conceptual context only. Completing C-H1 does not select scheduling, acquisition, attention, object memory or another branch.

## Completion record

Completed with a supported neural-family benefit and precise negative practical
comparisons, not a universal multi-state requirement. [Report](../reports/STUDY_C.md),
[statistics](../reports/study-c/statistics.json), and
[final audit](../reports/study-c/final-verification.json) retain all nine models,
ten confirmation roots, six primary and four secondary conditions. All 67 fitted
executions completed; no fit failed and no root was replaced or excluded.
TWO16 improves Brier over PC32 by .01819 [.01505, .02204], family-adjusted;
ADAPT1-M's .00157 gain over ADAPT1-C is precisely below the .01 practical margin.
The coherent-fault/genuine-change cause pair remains overconfident.

Actual commands: `uv run python -m soam.ambiguity.runner` with phases `fixture`,
`development`, `calibrate`, `freeze`, `confirmation`, `repeat`, `report`;
`uv run python scripts/analyze_study_c_ambiguity.py`;
`uv run python scripts/render_study_c_figures.py`;
`uv run python scripts/finalize_study_c.py` and its `--resources-only` repair.
The audit passed; the first resource-summary export had a reporting-only key-name
error, repaired with separate provenance. No fitting, endpoint or threshold changed.
All commands used `UV_CACHE_DIR=/private/tmp/soam-uv-cache`; plot commands used a
writable `MPLCONFIGDIR`. The full core suite passed 285 tests before confirmation.
The prescribed repeat matches four fitted inputs/checkpoints/traces and 1,530 arrays;
independent reduction verifies 810 values within 1.6653e-16.

Base commit `a552034b3badeee2d242c40103cb4e1243f4be30`; frozen source fingerprint
`18caccec2e5e72657d48559bff6782416b7ad373ccfc486e8932dc14aa0870b2`.
[Receipt](../reports/study-c/confirmation-receipt.json) owns source/configuration,
selected settings and fresh roots; [resources](../reports/study-c/resource-final.json)
record 1350.41 instrumented CPU seconds, 1361.15 phase wall seconds,
941,932,544 peak RSS bytes and 674,572,475 artifact bytes at audit close, below all
ceilings. Raw archives remain in `runs/study-c-v1/`.

SOAM-081 may now review the measured result; no later study activates automatically.
The local Qwen worker was unavailable (`Transport closed`); primary review proceeded
directly. Historical E1/A/B/B2 sources and gate reports were verified unchanged.

Final repository checks: `uv run ruff check soam tests scripts` passed;
`uv run python scripts/check_tickets.py` validated 82 tickets and two templates;
`git diff --check` passed. All 95 frozen source hashes and 2,092 indexed raw artifact
hashes were rechecked after documentation updates.
