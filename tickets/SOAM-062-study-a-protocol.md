---
schema_version: 2
id: "SOAM-062"
title: "Specify and select the Study A gating protocol"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1"]
depends_on: ["SOAM-047", "SOAM-051"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: "proceed"
---

# SOAM-062: Specify and select the Study A gating protocol

## Recommended thinking

**xhigh** — Separate gate adaptivity from capacity, optimization, task rank and uncertainty while preserving historical evidence.

## Problem / hypothesis

The [owner-selected Study A](../docs/requests/study_a_2026_11_11.md) asks why the GRU beat S32. E1 did not isolate gates. A negative mechanistic result is acceptable; historical SOAM-052 remains stop.

## Scope

Specify and select the Study A gating protocol. Follow the [Study A protocol](../docs/STUDY_A_PROTOCOL.md); Study B and acquisition implementation are excluded.

## Acceptance criteria

- [x] Complete the bounded deliverables for this phase, with reproducible evidence and limitations.
- [x] Preserve the E1 source/results and report negative or inconclusive findings without changing thresholds after confirmation.

## Metrics / evidence

Protocol and manifest; recurrence/information/no-write tests; development and confirmation root-level NMSE, uncertainty, diagnostic trajectories, resource/provenance records as applicable. Total study ceiling: 3,600 CPU / 7,200 wall seconds, 2 GiB RAM/artifacts. No remote publication.

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — completed evidence or proceed contract required.
- [SOAM-051](SOAM-051-shared-population-study.md) — completed evidence or proceed contract required.

## Branch conditions

The owner's November 11 request selects only Study A. This is a fresh corrective diagnostic based on completed SOAM-051, not a child of the failed SOAM-052 decision. SOAM-039 acquisition is deferred. Protocol proceed precedes engineering; verified engineering and a frozen development-informed receipt precede confirmation. Scientific competence and precision can yield an inconclusive completed study.

## Completion record

Completed protocol/RFC review 2026-11-11. Proceed to bounded engineering and development under [Study A v1](../docs/STUDY_A_PROTOCOL.md) and its [numerical manifest](../docs/protocols/study_a_v1.json). Owner approved 3,600 CPU / 7,200 wall seconds and 2 GiB RAM/artifacts. Confirmed SOAM-047 proceed and SOAM-051 complete; depends on evidence, not the failed sharing gate. Historical source-file hashes all match confirmation provenance b52329efaa0a4927337691e60a5b610ed08984b884aef8dd5b7b12801f2408c9 at base aca071ff884696955d96172d3f6251cf4f5ae11c. Original equations and E1 endpoint tables verified. Baseline: UV_CACHE_DIR=/tmp/soam-uv-cache uv run --offline pytest, 190 passed in 33.08s (default cache inaccessible). Worker extraction failed and was rejected; direct review used. Scientific identifiability: primary matched FU38 plus state/capacity/MAC controls; FR/GL equivalence explicitly avoids a redundant fit. Fresh streams, paired-root uncertainty, no-write/target separation and finite stopping contract are defined. Confirmation still requires development-informed immutable receipt and calibrated inventory; no hypothesis is accepted by this proceed.
