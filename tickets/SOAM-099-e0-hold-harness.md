---
schema_version: 2
id: "SOAM-099"
title: "Implement the paired stationary-horizon comparison"
type: "engineering"
status: "in_progress"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-098"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-21"
updated: "2026-11-21"
github_issue: null
decision: null
---

# SOAM-099: Implement the paired stationary-horizon comparison

## Recommended thinking

**high** — Preserve exact pairing, causal interfaces, historical contracts and reproducible bounded execution.

## Problem / hypothesis

[E0](../reports/STUDY_E0.md) showed favorable action/recovery proxies but unfavorable long stationary drift. The [owner](../docs/requests/e0_hold_2026_11_21.md) selected a longer zero-action training test. Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Implement the paired SHORT24/LONG128 harness without modifying historical E0 interfaces. Verify invariants and seven-cell fixture feasibility before trials.

Use [E0-HOLD v1](../docs/STUDY_E0_HOLD_PROTOCOL.md) and its [manifest](../docs/protocols/study_e0_hold_v1.json). Classification: **essential next**.

## Acceptance criteria

- [ ] Complete the bounded deliverable with checkable commands, artifacts and source/config/seed provenance.
- [ ] Preserve negative/inconclusive outcomes, verify applicable invariants/checks and leave later forks unselected.

## Metrics / evidence

Primary NAV32 paired stationary-error reduction of at least 5 degrees and final error at most 5 degrees; action/recovery/correction absolute guards and paired degradation margins. Twenty paired roots; NAV32/SYM32/GRU32 at SHORT24 and LONG128, plus PCA2. 147 scientific and seven fixture fits maximum. 7,200 CPU / 14,400 execution-wall seconds, 2 GiB RSS/artifacts. Numerical rules belong to the protocol.

## Dependencies

- [SOAM-098](SOAM-098-e0-hold-protocol.md) — required done; decision dependencies require proceed.

## Branch conditions

The new owner request explicitly selects this one follow-up. SOAM-097 proceed accepts earlier inconclusive evidence, not a positive geometry gate. No hierarchy/coupling/encoder/acquisition branch is activated. Earlier stop/revise/negative decisions remain intact.

## Completion record

Started after SOAM-098 done/proceed; the 339-test pre-change suite passed. Implementation, tests and resource fixture are pending.
