---
schema_version: 2
id: "SOAM-065"
title: "Review Study A mechanisms and the smallest retained core"
type: "decision"
status: "backlog"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1"]
depends_on: ["SOAM-064"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: null
---

# SOAM-065: Review Study A mechanisms and the smallest retained core

## Recommended thinking

**xhigh** — Separate gate adaptivity from capacity, optimization, task rank and uncertainty while preserving historical evidence.

## Problem / hypothesis

The [owner-selected Study A](../docs/requests/study_a_2026_11_11.md) asks why the GRU beat S32. E1 did not isolate gates. A negative mechanistic result is acceptable; historical SOAM-052 remains stop.

## Scope

Review Study A mechanisms and the smallest retained core. Follow the [Study A protocol](../docs/STUDY_A_PROTOCOL.md); Study B and acquisition implementation are excluded.

## Acceptance criteria

- [ ] Complete the bounded deliverables for this phase, with reproducible evidence and limitations.
- [ ] Preserve the E1 source/results and report negative or inconclusive findings without changing thresholds after confirmation.

## Metrics / evidence

Protocol and manifest; recurrence/information/no-write tests; development and confirmation root-level NMSE, uncertainty, diagnostic trajectories, resource/provenance records as applicable. Total study ceiling: 3,600 CPU / 7,200 wall seconds, 2 GiB RAM/artifacts. No remote publication.

## Dependencies

- [SOAM-064](SOAM-064-study-a-experiment.md) — completed evidence or proceed contract required.

## Branch conditions

The owner's November 11 request selects only Study A. This is a fresh corrective diagnostic based on completed SOAM-051, not a child of the failed SOAM-052 decision. SOAM-039 acquisition is deferred. Protocol proceed precedes engineering; verified engineering and a frozen development-informed receipt precede confirmation. Scientific competence and precision can yield an inconclusive completed study.

## Completion record

In progress for protocol design only; subsequent phases remain unstarted.
