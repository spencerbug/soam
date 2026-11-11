---
schema_version: 2
id: "SOAM-065"
title: "Review Study A mechanisms and the smallest retained core"
type: "decision"
status: "done"
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
decision: "proceed"
---

# SOAM-065: Review Study A mechanisms and the smallest retained core

## Recommended thinking

**xhigh** — Separate gate adaptivity from capacity, optimization, task rank and uncertainty while preserving historical evidence.

## Problem / hypothesis

The [owner-selected Study A](../docs/requests/study_a_2026_11_11.md) asks why the GRU beat S32. E1 did not isolate gates. A negative mechanistic result is acceptable; historical SOAM-052 remains stop.

## Scope

Review Study A mechanisms and the smallest retained core. Follow the [Study A v2 protocol](../docs/STUDY_A_PROTOCOL_V2.md); Study B and acquisition implementation are excluded.

## Acceptance criteria

- [x] Review all frozen primary/guardrail/resource/precision checks and preserve the inconclusive scientific result.
- [x] Identify the smallest tested competent core, distinguish accuracy from competence, and record retention/defer decisions for each mechanism.
- [x] Preserve historical E1 outcomes; do not activate or implement Study B or acquisition.

## Metrics / evidence

Protocol and manifest; recurrence/information/no-write tests; development and confirmation root-level NMSE, uncertainty, diagnostic trajectories, resource/provenance records as applicable. Total study ceiling: 3,600 CPU / 7,200 wall seconds, 2 GiB RAM/artifacts. No remote publication.

## Dependencies

- [SOAM-064](SOAM-064-study-a-experiment.md) — completed evidence or proceed contract required.

## Branch conditions

The owner's November 11 request selects only Study A. This is a fresh corrective diagnostic based on completed SOAM-051, not a child of the failed SOAM-052 decision. SOAM-039 acquisition is deferred. Protocol proceed precedes engineering; verified engineering and a frozen development-informed receipt precede confirmation. Scientific competence and precision can yield an inconclusive completed study.

## Completion record

Completed 2026-11-11 after SOAM-064's complete inventory, exact repeat and independent audit. **Proceed is scoped to accepting the [decision record](../reports/STUDY_A_DECISION.md) and R32 starting-reference recommendation**, not support for the frozen adaptive-update hypothesis. That scientific result remains **inconclusive**; G32 improves short-horizon accuracy, but 9.92% primary gain misses the 10% minimum and free-32 protection is unresolved.

R32 (32 units, fixed leak 0.5, 2,412 parameters) is the smallest tested competent neural core; selection is an explicit post-study simplicity/accuracy judgment, not a preregistered minimal-width proof. Preserve G32/FU38 and L2/L12 references; reset adaptation remains an optional mechanism comparison; do not require adaptive update or S32 constraints. No next experiment is selected. SOAM-039 remains backlog and SOAM-052 remains stop.

Evidence: [report](../reports/STUDY_A.md), [tables](../reports/study-a/tables.md), [audit](../reports/study-a/audit.json), [repeat](../reports/study-a/reproduction.json), [resource accounting](../reports/study-a/resource-final.json) and [completion checks](../reports/study-a/verification.json). Final full suite: 215 passed in 24.83s; ticket validation/Ruff/link checks are recorded there. Experiment source commit 44824b7884965bb4ad49166143427bdd43e87452 and all roots/configurations remain fixed in the receipt. Owner notified of blog relevance; no publication performed.
