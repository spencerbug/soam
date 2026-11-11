---
schema_version: 2
id: "SOAM-064"
title: "Measure adaptive gating under the frozen Study A protocol"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1"]
depends_on: ["SOAM-062", "SOAM-063"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: null
---

# SOAM-064: Measure adaptive gating under the frozen Study A protocol

## Recommended thinking

**high** — Separate gate adaptivity from capacity, optimization, task rank and uncertainty while preserving historical evidence.

## Problem / hypothesis

The [owner-selected Study A](../docs/requests/study_a_2026_11_11.md) asks why the GRU beat S32. E1 did not isolate gates. A negative mechanistic result is acceptable; historical SOAM-052 remains stop.

## Scope

Measure adaptive gating under the frozen [Study A v2 protocol](../docs/STUDY_A_PROTOCOL_V2.md), preserving v1 calibration. Study B and acquisition implementation are excluded.

## Acceptance criteria

- [x] Complete development, frozen confirmation and the prescribed repeat within the cumulative ceiling; retain every model/root and failed attempt.
- [x] Report root-level uncertainty, gate/state/intervention/recovery/horizon diagnostics, historical provenance and scientific limits.
- [x] Preserve E1 and the closed v1 calibration; report the inconclusive primary result without changing thresholds after confirmation.

## Metrics / evidence

Protocol and manifest; recurrence/information/no-write tests; development and confirmation root-level NMSE, uncertainty, diagnostic trajectories, resource/provenance records as applicable. Total study ceiling: 3,600 CPU / 7,200 wall seconds, 2 GiB RAM/artifacts. No remote publication.

## Dependencies

- [SOAM-062](SOAM-062-study-a-protocol.md) — completed evidence or proceed contract required.
- [SOAM-063](SOAM-063-study-a-harness.md) — completed evidence or proceed contract required.

## Branch conditions

The owner's November 11 request selects only Study A. This is a fresh corrective diagnostic based on completed SOAM-051, not a child of the failed SOAM-052 decision. SOAM-039 acquisition is deferred. Protocol proceed precedes engineering; verified engineering and a frozen development-informed receipt precede confirmation. Scientific competence and precision can yield an inconclusive completed study.

## Completion record

Completed 2026-11-11. [Scientific report](../reports/STUDY_A.md), [tables](../reports/study-a/tables.md), [root results](../reports/study-a/root-results.md), [full statistics](../reports/study-a/statistics.json), [independent audit](../reports/study-a/audit.json), [resource accounting](../reports/study-a/resource-final.json), and [verification](../reports/study-a/verification.json) retain the evidence. All 252 authorized fitted executions completed: 24 fixtures, 96 development, 120 confirmation, 12 repeat; no failed fits, exclusions or replacements. One pre-confirmation receipt-serialization failure is preserved and charged. Historical E1 source hashes still match.

The frozen adaptive-update practical-benefit result is **inconclusive**: G32's paired-root J gain over FU38 is 9.9172%, below the 10% point threshold, with adjusted interval [0.6950%,19.5834%]; the free-32 guardrail is unresolved. No confirmation-driven retuning occurred. Source identity `study-a-v2-receipt-repair-1`, commit `44824b7884965bb4ad49166143427bdd43e87452`, source aggregate `6e05f7437dc1f37527da85cf0c4231fd0dcba082ec5747f8b4f141e534c43959`. Confirmation receipt structured-content SHA-256 `e51ce6c25e0f4dd56864672ac8fe64f1d488bba7ee726d9ee0706d7ec1acefc8`; independent roots 9301,9311,9319,9323,9337,9341,9343,9349,9371,9377. The prescribed root-9301 repeat matches all nine numerical hash fields exactly.

Executed phase commands: `UV_CACHE_DIR=/tmp/soam-uv-cache uv run --offline python -m soam.gating.runner --phase PHASE --output runs/study-a-v2`, for fixture/development/freeze/confirmation/repeat/report; the engineering record documents the failed freeze and reviewed repair. Final `UV_CACHE_DIR=/tmp/soam-uv-cache uv run --offline pytest`: **215 passed in 24.83s**. Independent NumPy reduction of 600 headline metrics agrees within 1.11e-16. Numerical work consumed about 17.8 CPU minutes and 1.20 GiB peak RSS, with about 1.42 GiB artifacts, within the original ceiling. Exact figures and completion checks are linked above.

## V1 development preserved

All 48 development fits completed, but the non-gated controls did not plateau. V1 is closed before confirmation. Await v2 engineering checks; SOAM-062 records the reviewed bounded schedule amendment.

V2 subsequently completed after the verified fixture, fresh development streams and immutable receipt. [Engineering history](../reports/STUDY_A_IMPLEMENTATION.md) records the sequence; the statements above describe the preserved pre-confirmation v1 stopping point.
