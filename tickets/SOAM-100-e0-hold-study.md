---
schema_version: 2
id: "SOAM-100"
title: "Execute the frozen longer stationary-training study"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-098", "SOAM-099"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-21"
updated: "2026-11-21"
github_issue: null
decision: null
---

# SOAM-100: Execute the frozen longer stationary-training study

## Recommended thinking

**high** — Preserve exact pairing, causal interfaces, historical contracts and reproducible bounded execution.

## Problem / hypothesis

[E0](../reports/STUDY_E0.md) showed favorable action/recovery proxies but unfavorable long stationary drift. The [owner](../docs/requests/e0_hold_2026_11_21.md) selected a longer zero-action training test. Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Execute only the frozen 140 confirmation fits and seven exact repeats. Preserve all failures, provenance, raw results, costs and uncertainty in reports/STUDY_E0_HOLD.md.

Use [E0-HOLD v1](../docs/STUDY_E0_HOLD_PROTOCOL.md) and its [manifest](../docs/protocols/study_e0_hold_v1.json). Classification: **essential next**.

## Acceptance criteria

- [x] Complete the bounded deliverable with checkable commands, artifacts and source/config/seed provenance.
- [x] Preserve negative/inconclusive outcomes, verify applicable invariants/checks and leave later forks unselected.

## Metrics / evidence

Primary NAV32 paired stationary-error reduction of at least 5 degrees and final error at most 5 degrees; action/recovery/correction absolute guards and paired degradation margins. Twenty paired roots; NAV32/SYM32/GRU32 at SHORT24 and LONG128, plus PCA2. 147 scientific and seven fixture fits maximum. 7,200 CPU / 14,400 execution-wall seconds, 2 GiB RSS/artifacts. Numerical rules belong to the protocol.

## Dependencies

- [SOAM-098](SOAM-098-e0-hold-protocol.md) — required done; decision dependencies require proceed.
- [SOAM-099](SOAM-099-e0-hold-harness.md) — required done; decision dependencies require proceed.

## Branch conditions

The new owner request explicitly selects this one follow-up. SOAM-097 proceed accepts earlier inconclusive evidence, not a positive geometry gate. No hierarchy/coupling/encoder/acquisition branch is activated. Earlier stop/revise/negative decisions remain intact.

## Completion record

Started after SOAM-098 done/proceed and SOAM-099 done with a passing seven-cell preflight. Source `6733775`; the frozen 147-fit scientific inventory and exact repeats are beginning. No hyperparameter selection or confirmation tuning is permitted.

Completed all 147 scientific fits (140 confirmation, seven exact repeats) and seven
fixtures with no failed fits/excluded roots. [Report](../reports/STUDY_E0_HOLD.md),
[full tables](../reports/study-e0-hold/tables.md), [receipt](../reports/study-e0-hold/receipt.json)
and [raw root metrics](../reports/study-e0-hold/root_metrics.csv) preserve the evidence.
Formal NAV32 outcome: **negative declared joint fix**. Stationary improvement
6.63463 degrees [5.01706,8.80467] passes; LONG error 5.69773 [5.25935,6.18261]
precisely exceeds 5 degrees. Recovery-ratio degradation .033117 [.007312,.062184]
crosses the .05 margin, so its noninferiority check is unresolved. Eleven criteria pass.

All 189 arrays and 54 tensors repeat exactly. Sixty main and three repeated neural
initializations pair exactly; all cells share each root's prefix data. Independent
reduction verifies 980 root metrics, 13 adjusted intervals, 153 source hashes,
148 unchanged historical E0 source hashes and 308 checkpoint/array hashes.
There are 621 fingerprinted raw archive files, local under `runs/study-e0-hold-v1`.

Commands: with `UV_CACHE_DIR=/private/tmp/soam-uv-cache`, run
`uv run --offline --no-sync python -m soam.hold.runner fixture --output runs/study-e0-hold-v1`,
then the same command with `confirmation`; finally the archived independent reducer
`reports/study-e0-hold/analysis.py` and its table helper. Model source `6733775`;
confirmation commit `cff19dd`; source fingerprint
`6501d4de87f6fd9c7b352c6142eb98ccc4353a813bd46fa5052eafec05a8c307`.
Numerical use 826.872116 CPU / 827.135330 execution-wall seconds; audit/tables/figures
add 2.023757 / 2.026321 seconds. Peak RSS 354,746,368 bytes; raw artifacts 544,009,667
bytes. All resource ceilings pass. No tuning, retry or budget extension occurred.

The unchanged final model source passed 348 tests in 28.60s before fitting; the
independent reducer/table helper execute successfully and pass Ruff. Figure visually
checked. Source/config/software/numerical settings, original/mapped seeds, training
hashes and data/compute exposures are recorded in the receipt and per-fit records.

Final closeout checks: Ruff passes for the harness/tests/independent analysis scripts; the validator accepts 102 tickets and two templates; all checked local Markdown links resolve. Archived analysis hashes match the executed sources. Source tests remain 348/348 passing, with no subsequent numerical-source changes. No raw payloads were added to Git.
