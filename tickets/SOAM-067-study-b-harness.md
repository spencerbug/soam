---
schema_version: 2
id: "SOAM-067"
title: "Implement and verify temporal assimilation comparisons"
type: "engineering"
status: "in_progress"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-066"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: null
---

# SOAM-067: Implement and verify temporal assimilation comparisons

## Recommended thinking

**high** — Separate sensory timing, state correction and internal computation while preserving information parity, scientific invariants and independent-root inference.

## Problem / hypothesis

The owner selects Study B after completed Study A. Ordinary R32 is competent but temporal assimilation remains untested. Historical SOAM-052 remains stop. See the [protocol](../docs/STUDY_B_PROTOCOL.md).

## Scope

Implement and verify temporal assimilation comparisons. Only this bounded study is selected; no acquisition, attention, integration, or online parameter updates.

## Acceptance criteria

- [ ] Complete this phase with checkable source, protocol, tests or measured evidence.
- [ ] Preserve information parity and historical negative results; report supported, negative, inconclusive, or invalid outcomes without post-confirmation changes.
- [ ] Record resources, limitations, and implications for the next interface.

## Metrics / evidence

Pre-correction NMSE, correction/settling errors, free horizons, corruption/change guardrails, update/MAC/state/parameter accounting and paired-root intervals. Owner-approved ceiling: 7200 CPU seconds, 14400 execution wall seconds, 2 GiB peak RSS and 2 GiB artifacts.

## Dependencies

- [SOAM-066](SOAM-066-study-b-protocol.md) — completed evidence or proceed decision.

## Branch conditions

The November 11 owner request is the fresh named selection. SOAM-066 owns the protocol/RFC and routing. Protocol proceed precedes implementation; verified implementation and immutable development-informed selections precede confirmation. The failed sharing gate is not a dependency and is not changed.

## Completion record

Not completed.
