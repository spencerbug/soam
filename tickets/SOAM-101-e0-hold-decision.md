---
schema_version: 2
id: "SOAM-101"
title: "Review stationary drift improvement and navigation guardrails"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-100"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-21"
updated: "2026-11-21"
github_issue: null
decision: "proceed"
---

# SOAM-101: Review stationary drift improvement and navigation guardrails

## Recommended thinking

**xhigh** — Separate horizon effects, compute mismatch, precision and noninferiority from an unrestricted architecture claim.

## Problem / hypothesis

[E0](../reports/STUDY_E0.md) showed favorable action/recovery proxies but unfavorable long stationary drift. The [owner](../docs/requests/e0_hold_2026_11_21.md) selected a longer zero-action training test. Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Accept valid supported, tradeoff, negative or inconclusive evidence. Distinguish meaningful improvement from a fixed drift problem; recommend at most one unactivated next fork.

Use [E0-HOLD v1](../docs/STUDY_E0_HOLD_PROTOCOL.md) and its [manifest](../docs/protocols/study_e0_hold_v1.json). Classification: **essential next**.

## Acceptance criteria

- [x] Complete the bounded deliverable with checkable commands, artifacts and source/config/seed provenance.
- [x] Preserve negative/inconclusive outcomes, verify applicable invariants/checks and leave later forks unselected.

## Metrics / evidence

Primary NAV32 paired stationary-error reduction of at least 5 degrees and final error at most 5 degrees; action/recovery/correction absolute guards and paired degradation margins. Twenty paired roots; NAV32/SYM32/GRU32 at SHORT24 and LONG128, plus PCA2. 147 scientific and seven fixture fits maximum. 7,200 CPU / 14,400 execution-wall seconds, 2 GiB RSS/artifacts. Numerical rules belong to the protocol.

## Dependencies

- [SOAM-100](SOAM-100-e0-hold-study.md) — required done; decision dependencies require proceed.

## Branch conditions

The new owner request explicitly selects this one follow-up. SOAM-097 proceed accepts earlier inconclusive evidence, not a positive geometry gate. No hierarchy/coupling/encoder/acquisition branch is activated. Earlier stop/revise/negative decisions remain intact.

## Completion record

Started after SOAM-100 completed all frozen fits/repeats and the independent audit. Reviewing the precise residual-drift failure, unresolved recovery noninferiority, mandatory controls and scoped follow-up recommendation.

**Proceed with acceptance of valid negative evidence for the declared joint fix.**
The [decision](../reports/STUDY_E0_HOLD_DECISION.md) preserves the 6.63463-degree
paired improvement and the precise remaining 5.69773-degree error above the five-degree
target. Eleven of thirteen criteria pass; recovery-ratio noninferiority is unresolved.
Action prediction passes its declared degradation margin, not a claim of unchanged
performance in every direction. GRU/SYM/PCA comparisons remain descriptive controls.

Reviewed matching source/initialization/data, equal episode weighting, zero extra
observations, finite inventory, inference purity, all guard intervals/precision rules,
20 roots, 147 scientific fits, 189 exact arrays, 54 exact tensors, and the independent
980-metric/13-interval audit. All resource limits pass; historical E0's 148 source hashes
remain unchanged. The source/config/software/seed records and 621-file archive hashes
are linked from SOAM-100 and the report; the full raw archive is local, not published.

The sole conditional recommendation is a fresh fixed optimization-budget comparison
at the 128-step horizon, replaying the same prefix corpus. Declining late training
loss motivates that question but does not establish an optimization diagnosis or
promise a fix. No successor, coupling, hierarchy or other experiment is activated.
Earlier negative/inconclusive gates remain intact. Owner notified of the blog/report-worthy
retention-versus-other-dynamics distinction; no publication or remote issue action.

Final closeout checks: Ruff passes for the harness/tests/independent analysis scripts; the validator accepts 102 tickets and two templates; all checked local Markdown links resolve. Archived analysis hashes match the executed sources. Source tests remain 348/348 passing, with no subsequent numerical-source changes. No raw payloads were added to Git.
