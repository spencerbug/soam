---
schema_version: 2
id: "SOAM-068"
title: "Measure temporal assimilation and settling under matched evidence"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-066", "SOAM-067"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: null
---

# SOAM-068: Measure temporal assimilation and settling under matched evidence

## Recommended thinking

**high** — Separate sensory timing, state correction and internal computation while preserving information parity, scientific invariants and independent-root inference.

## Problem / hypothesis

The owner selects Study B after completed Study A. Ordinary R32 is competent but temporal assimilation remains untested. Historical SOAM-052 remains stop. See the [protocol](../docs/STUDY_B_PROTOCOL.md).

## Scope

Measure temporal assimilation and settling under matched evidence. Only this bounded study is selected; no acquisition, attention, integration, or online parameter updates.

## Acceptance criteria

- [x] Complete this phase with checkable source, protocol, tests or measured evidence.
- [x] Preserve information parity and historical negative results; report supported, negative, inconclusive, or invalid outcomes without post-confirmation changes.
- [x] Record resources, limitations, and implications for the next interface.

## Metrics / evidence

Pre-correction NMSE, correction/settling errors, free horizons, corruption/change guardrails, update/MAC/state/parameter accounting and paired-root intervals. Owner-approved ceiling: 7200 CPU seconds, 14400 execution wall seconds, 2 GiB peak RSS and 2 GiB artifacts.

## Dependencies

- [SOAM-066](SOAM-066-study-b-protocol.md) — completed evidence or proceed decision.
- [SOAM-067](SOAM-067-study-b-harness.md) — completed evidence or proceed decision.

## Branch conditions

The November 11 owner request is the fresh named selection. SOAM-066 owns the protocol/RFC and routing. Protocol proceed precedes implementation; verified implementation and immutable development-informed selections precede confirmation. The failed sharing gate is not a dependency and is not changed.

## Completion record

V1 complete: 16 fixture, 64 development, 160 confirmation and 16 repeat fits (256 total), no failures. All 80 prescribed reproduction checks match exactly. Independent audit regenerates input hashes and recomputes 1920 metrics from saved arrays. Frozen outcome is tradeoff, with precise exclusion of a 10 percent GA32 gain over PC32 and a failed corruption guard. See reports/STUDY_B.md and reports/study-b/. Source 0e03e0d / ae6754ce8e177d17ad5ee4590814e5176190bb3e301907a81603c996acb06602; receipt ea64dceeda1dd283e8fda8af11e434e0a63159561822f762cf40a395429b701d. All results are preserved; a separately routed magnitude-input supplement addresses a request-coverage limitation.
