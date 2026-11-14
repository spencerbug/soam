---
schema_version: 2
id: "SOAM-076"
title: "Screen and confirm bounded robust Kalman correctors"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-074", "SOAM-075"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-12"
github_issue: null
decision: null
---

# SOAM-076: Screen and confirm bounded robust Kalman correctors

## Recommended thinking

**high** — Separate statistical identifiability, numerical validity and root-level evidence in a finite correction search.

## Problem / hypothesis

FILTER2 has strong ordinary prediction and a corruption failure; B2 tests the smallest robust corrector.

## Scope

Screen and confirm bounded robust Kalman correctors. Follow [B2 v1](../docs/STUDY_B2_PROTOCOL.md). Owner explicitly selects B2 after completed B; no other branch or Study C implementation.

## Acceptance criteria

- [x] Complete this phase with measured evidence or explicit negative/inconclusive findings.
- [x] Preserve A/B source, results and decisions; enforce no-write and causal scoring.
- [x] Record exact provenance, resource use, tests and all mandatory controls.

## Metrics / evidence

[B2 manifest](../docs/protocols/study_b2_v1.json) owns endpoints, finite allocation and fresh roots. Ordinary J, balanced corruption, genuine-change guards and real inference cost.

## Dependencies

- [SOAM-074](SOAM-074-study-b2-protocol.md) — completed evidence or proceed contract.
- [SOAM-075](SOAM-075-study-b2-harness.md) — completed evidence or proceed contract.

## Branch conditions

SOAM-074 is the fresh routing decision under the owner's explicit B2 assignment; SOAM-073 proceeds only for the interface. Historical SOAM-069 revise and SOAM-052 stop remain immutable. Protocol proceed precedes implementation; tests and fixture precede development; immutable receipt precedes confirmation. SOAM-077 completes before any fresh selection of C.

## Completion record

Completed [B2 report](../reports/STUDY_B2.md): 21 screened configurations/references,8 confirmed models,10 fresh paired roots. Both primary challengers pass the unchanged 12-contrast family and guards. Temporal/hybrid development failures and coherent-corruption limits are retained.29 fitted executions including historical reproduction; no failed scientific fits. The prescribed repeat matches every candidate; 1040 independent array reductions agree to 1.11e-16. Numerical source fingerprint 28d72614c9f2d61b0e48cdd4d2ebc896cff1d37bb7324a2d5c735a29cb69e1cd; base commit bdb3bdcbb47c7a2a24301e044ebaaac6b50a18cd; all roots/configuration/exposure in [receipt](../reports/study-b2/confirmation-receipt.json). Commands: `uv run python -m soam.robust.runner` audit/fixture/screen1/screen2/hybrid/freeze/confirmation/repeat/report; separate documented archive A1 calibration and diagnostic/render/cost audits. All numerical use including the failed storage projection is in [resource ledger](../reports/study-b2/resource-final.json). Statistical source remained frozen; no confirmation tuning or extra branch. Final validation is recorded with the decision ticket.
