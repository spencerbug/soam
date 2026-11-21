---
schema_version: 2
id: "SOAM-096"
title: "Execute the bounded E0 navigation pilot"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-094", "SOAM-095"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-21"
updated: "2026-11-21"
github_issue: null
decision: null
---

# SOAM-096: Execute the bounded E0 navigation pilot

## Recommended thinking

**high** — Verify causal interfaces, deterministic fitting, bounded execution and evaluator-only geometry without changing the frozen design.

## Problem / hypothesis

Can a learned recurrent population preserve and navigate orientation while recovering locally from perturbations? The [owner selection](../docs/requests/e0_2026_11_21.md) activates one narrow test under H1/H6. Earlier studies do not answer this question. Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Run only the frozen development selection, ten-root confirmation and prescribed exact repeat after the harness preflight passes. Preserve every failure and stop at the declared ceiling.

Use [E0 v1](../docs/STUDY_E0_PROTOCOL.md) and its [manifest](../docs/protocols/study_e0_v1.json). Classification: **essential next**.

## Acceptance criteria

- [x] Reconcile all 58 prescribed scientific fits or document a stopped/invalid partial inventory.
- [x] Archive configuration/source/seeds, raw metrics, checkpoints, resources, uncertainty and exact repeat checks in reports/STUDY_E0.md.

## Metrics / evidence

Free-64 sensory NMSE; grounded prediction; zero-action pose retention; transverse contraction with pose-preservation guard; tangent retention; correction on returning evidence. NAV32, SYM32, GRU32 and fitted PCA2 controls. Two development roots, ten confirmation roots and one four-model repeat. Frozen ceiling: 3,600 CPU / 7,200 execution-wall seconds, 2 GiB RSS and 1 GiB numerical artifacts. Protocol owns thresholds; reports own measured findings.

## Dependencies

- [SOAM-094](SOAM-094-e0-protocol.md) — required done; decision prerequisite must be proceed.
- [SOAM-095](SOAM-095-e0-harness.md) — required done; decision prerequisite must be proceed.

## Branch conditions

The November 21 owner selection activates only E0 v1. SOAM-093 proceed accepts inconclusive evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. Coupling, translation, attention, hierarchy, load/encoder sweeps and online acquisition require fresh routing.

## Completion record

Started after SOAM-094 done/proceed and SOAM-095 done with a passing four-model preflight. Numerical source `7168e2e`, source fingerprint `4dd66fc4194336388dc8a96a742d157eab7eceac521112760f385744d5b21622`. The finite runner will execute development before frozen confirmation; no confirmation tuning.

Completed all 58 scientific fits (14 development, 40 confirmation, four repeats)
and four fixtures with no failures or exclusions. [Study report](../reports/STUDY_E0.md),
[receipt](../reports/study-e0/receipt.json), [root metrics](../reports/study-e0/root_metrics.csv)
and [archive hashes](../reports/study-e0/archive_sha256.json) preserve the measured evidence.
NAV32 passes six criteria; stationary error 13.861 degrees [12.119,16.278] has width
4.159 > 4 degrees, so its joint result remains inconclusive. GRU32 is negative on
free-64 accuracy; PCA2 is negative only for transverse attraction; SYM32 is inconclusive.
All 108 repeat arrays and 29 tensors match exactly. Independent reduction verified
280 root metrics, 28 adjusted intervals, 148 source hashes and 124 checkpoint/array hashes.

Commands: `uv run python -m soam.navigation.runner fixture|development|confirmation
--output runs/study-e0-v1` (three separate sequential invocations), followed by the
archived `reports/study-e0/analysis.py` reducer. Numerical use 150.927601 CPU /
151.144840 execution-wall seconds; two audit/figure passes add 2.035203 / 2.041270 seconds.
Peak numerical RSS 336,904,192 bytes; raw archive 155,163,746 bytes. Limits pass.
Full configuration/software/source and per-fit training-data hashes are in the receipt/ledger.
Development source commit `7b07dd4`; selected settings were committed before confirmation
at `95e7fd0`; numerical source fingerprint remains `4dd66fc4194336388dc8a96a742d157eab7eceac521112760f385744d5b21622`.
The local raw archive is ignored by Git; tracked summaries and hashes do not imply
remote publication. Plot visually checked; no parameter or threshold changed after fitting.

Final verification: `uv run pytest` — 339 passed in 17.84s; Ruff passes for the harness, tests and reducer. Ticket validation checks 98 tickets/two templates; 536 local Markdown links resolve. The formatting-only second analysis pass repeats raw reduction without fitting and preserves cumulative audit cost and the first source in its receipt history.
