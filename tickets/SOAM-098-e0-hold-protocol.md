---
schema_version: 2
id: "SOAM-098"
title: "Freeze the longer zero-action E0 follow-up"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-097"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-21"
updated: "2026-11-21"
github_issue: null
decision: "proceed"
---

# SOAM-098: Freeze the longer zero-action E0 follow-up

## Recommended thinking

**xhigh** — Separate horizon effects, compute mismatch, precision and noninferiority from an unrestricted architecture claim.

## Problem / hypothesis

[E0](../reports/STUDY_E0.md) showed favorable action/recovery proxies but unfavorable long stationary drift. The [owner](../docs/requests/e0_hold_2026_11_21.md) selected a longer zero-action training test. Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Freeze one horizon intervention, pairing, per-episode loss weighting, primary gain/fix criteria, degradation margins, uncertainty and finite resources before implementation.

Use [E0-HOLD v1](../docs/STUDY_E0_HOLD_PROTOCOL.md) and its [manifest](../docs/protocols/study_e0_hold_v1.json). Classification: **essential next**.

## Acceptance criteria

- [x] Review and freeze the single-factor intervention, information/compute comparison and inferential decision rules.
- [x] Verify branch conditions and historical outcome preservation before implementation.

## Metrics / evidence

Primary NAV32 paired stationary-error reduction of at least 5 degrees and final error at most 5 degrees; action/recovery/correction absolute guards and paired degradation margins. Twenty paired roots; NAV32/SYM32/GRU32 at SHORT24 and LONG128, plus PCA2. 147 scientific and seven fixture fits maximum. 7,200 CPU / 14,400 execution-wall seconds, 2 GiB RSS/artifacts. Numerical rules belong to the protocol.

## Dependencies

- [SOAM-097](SOAM-097-e0-decision.md) — required done; decision dependencies require proceed.

## Branch conditions

The new owner request explicitly selects this one follow-up. SOAM-097 proceed accepts earlier inconclusive evidence, not a positive geometry gate. No hierarchy/coupling/encoder/acquisition branch is activated. Earlier stop/revise/negative decisions remain intact.

## Completion record

**Proceed with E0-HOLD v1 only.** The fresh owner request activates SOAM-097’s conditional longer-stationary-training recommendation. Manual review accepts identical initial weights/prefix evidence, equal per-episode weighting, explicit additional recurrence cost and no new observations. Twenty paired roots, 147 scientific fits, 13 NAV32 intervals and resource ceilings are frozen before fitting. Controls are mandatory but descriptive; no alternate model can replace the primary claim after viewing confirmation. Pre-change tests: 339 passed in 35.10s. Historical E0 remains unchanged. Seven-cell runtime preflight is still required before science.
