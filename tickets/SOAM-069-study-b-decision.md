---
schema_version: 2
id: "SOAM-069"
title: "Review temporal assimilation and recommend the sensory motion interface"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-068"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: "revise"
---

# SOAM-069: Review temporal assimilation and recommend the sensory motion interface

## Recommended thinking

**xhigh** — Separate sensory timing, state correction and internal computation while preserving information parity, scientific invariants and independent-root inference.

## Problem / hypothesis

The owner selects Study B after completed Study A. Ordinary R32 is competent but temporal assimilation remains untested. Historical SOAM-052 remains stop. See the [protocol](../docs/STUDY_B_PROTOCOL.md).

## Scope

Review temporal assimilation and recommend the sensory motion interface. Only this bounded study is selected; no acquisition, attention, integration, or online parameter updates.

## Acceptance criteria

- [x] Complete this phase with checkable source, protocol, tests or measured evidence.
- [x] Preserve information parity and historical negative results; report supported, negative, inconclusive, or invalid outcomes without post-confirmation changes.
- [x] Record resources, limitations, and implications for the next interface.

## Metrics / evidence

Pre-correction NMSE, correction/settling errors, free horizons, corruption/change guardrails, update/MAC/state/parameter accounting and paired-root intervals. Owner-approved ceiling: 7200 CPU seconds, 14400 execution wall seconds, 2 GiB peak RSS and 2 GiB artifacts.

## Dependencies

- [SOAM-068](SOAM-068-study-b-experiment.md) — completed evidence or proceed decision.

## Branch conditions

The November 11 owner request is the fresh named selection. SOAM-066 owns the protocol/RFC and routing. Protocol proceed precedes implementation; verified implementation and immutable development-informed selections precede confirmation. The failed sharing gate is not a dependency and is not changed.

## Completion record

Reviewed valid v1 evidence and retained its tradeoff outcome. See reports/STUDY_B_V1_DECISION.md. The requested magnitude-dependent gain comparison is incomplete because the v1 gate uses signed affine inputs. Revise scope coverage through one fresh SOAM-070 supplement based on completed SOAM-068 evidence; preserve v1, use fresh streams and the same cumulative budget. This revise decision does not unblock an implementation child.
