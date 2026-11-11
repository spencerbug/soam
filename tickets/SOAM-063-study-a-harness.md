---
schema_version: 2
id: "SOAM-063"
title: "Implement and verify Study A recurrences and diagnostics"
type: "engineering"
status: "in_progress"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1"]
depends_on: ["SOAM-062"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: null
---

# SOAM-063: Implement and verify Study A recurrences and diagnostics

## Recommended thinking

**high** — Separate gate adaptivity from capacity, optimization, task rank and uncertainty while preserving historical evidence.

## Problem / hypothesis

The [owner-selected Study A](../docs/requests/study_a_2026_11_11.md) asks why the GRU beat S32. E1 did not isolate gates. A negative mechanistic result is acceptable; historical SOAM-052 remains stop.

## Scope

Implement and verify Study A recurrences and diagnostics. Follow the [Study A protocol](../docs/STUDY_A_PROTOCOL.md); Study B and acquisition implementation are excluded.

## Acceptance criteria

- [x] Complete the bounded deliverables for this phase, with reproducible evidence and limitations.
- [x] Preserve the E1 source/results and report negative or inconclusive findings without changing thresholds after confirmation.

## Metrics / evidence

Protocol and manifest; recurrence/information/no-write tests; development and confirmation root-level NMSE, uncertainty, diagnostic trajectories, resource/provenance records as applicable. Total study ceiling: 3,600 CPU / 7,200 wall seconds, 2 GiB RAM/artifacts. No remote publication.

## Dependencies

- [SOAM-062](SOAM-062-study-a-protocol.md) — completed evidence or proceed contract required.

## Branch conditions

The owner's November 11 request selects only Study A. This is a fresh corrective diagnostic based on completed SOAM-051, not a child of the failed SOAM-052 decision. SOAM-039 acquisition is deferred. Protocol proceed precedes engineering; verified engineering and a frozen development-informed receipt precede confirmation. Scientific competence and precision can yield an inconclusive completed study.

## Completion record

Completed 2026-11-11 at source f897515. Implemented isolated soam/gating package, all requested recurrences (GL via tested exact FR folding), fresh paired E1 data, bounded phases, source snapshots, immutable receipt, root inference, diagnostic-only probes, intervention/recovery/long-horizon plots and exact reproduction checks. Baseline 190 tests passed; full suite with 22 added tests: 212 passed in 27.15s; final additional statistical-classification test: all 23 Study A tests passed in 1.71s. Ruff check/format and 66-ticket validator pass. All 12 short fixture fits completed; [calibration](../runs/study-a-v1/fixture/calibration.json) projects 970.43 CPU seconds with margin versus 3,238.72 available. Peak RSS 300,662,784 bytes, archived fixture/source 14,039,128 bytes. Fixture execution consumed 1.280906 CPU seconds; no confirmation data generated. Equations, stream separation, no-write inference, probe isolation, gate folding, resource matching, paired-root statistics, budget stopping and deterministic mini-fits tested. Local worker review was unsuccessful; its out-of-scope command was rejected and no worker action executed. Direct review used. Fixture success is engineering evidence only.

## V2 implementation amendment

Implementing the reviewed common decay schedule, new stream version and cumulative cross-version ledger before v2 execution. Original v1 fixture evidence above remains unchanged.
