---
schema_version: 2
id: "SOAM-075"
title: "Implement and verify robust correction and corruption controls"
type: "engineering"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-074"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-12"
github_issue: null
decision: null
---

# SOAM-075: Implement and verify robust correction and corruption controls

## Recommended thinking

**high** — Separate statistical identifiability, numerical validity and root-level evidence in a finite correction search.

## Problem / hypothesis

FILTER2 has strong ordinary prediction and a corruption failure; B2 tests the smallest robust corrector.

## Scope

Implement and verify robust correction and corruption controls. Follow [B2 v1](../docs/STUDY_B2_PROTOCOL.md). Owner explicitly selects B2 after completed B; no other branch or Study C implementation.

## Acceptance criteria

- [x] Complete this phase with measured evidence or explicit negative/inconclusive findings.
- [x] Preserve A/B source, results and decisions; enforce no-write and causal scoring.
- [x] Record exact provenance, resource use, tests and all mandatory controls.

## Metrics / evidence

[B2 manifest](../docs/protocols/study_b2_v1.json) owns endpoints, finite allocation and fresh roots. Ordinary J, balanced corruption, genuine-change guards and real inference cost.

## Dependencies

- [SOAM-074](SOAM-074-study-b2-protocol.md) — completed evidence or proceed contract.

## Branch conditions

SOAM-074 is the fresh routing decision under the owner's explicit B2 assignment; SOAM-073 proceeds only for the interface. Historical SOAM-069 revise and SOAM-052 stop remain immutable. Protocol proceed precedes implementation; tests and fixture precede development; immutable receipt precedes confirmation. SOAM-077 completes before any fresh selection of C.

## Completion record

Implemented correction-only solve/Joseph controls and T1–T10 benchmark with exact identical-evidence pair. `uv run pytest`: 257 passed in 16.19s; targeted 19 passed. Historical audit refit and 216 arrays reproduce exactly; existing source fingerprint unchanged. Fixture 19.64 CPU seconds, projection 553.79 CPU seconds. Initial storage estimate omitted batch scaling; corrected full-detail estimate failed 1 GiB. Preserved failed receipt and adopted pre-development archive A1 with all error arrays plus bounded diagnostic traces; `uv run python scripts/calibrate_study_b2_storage.py` passes. Artifacts: `runs/study-b2-v1/audit`, `fixture`, `fixture-storage-correction` and `fixture-storage-a1`. No scientific screening used to choose these engineering changes. Qwen extraction timed out; bounded harness review aborted without findings, so direct equation checks and invariant tests were used. Phase 2 mechanisms remain conditional and will be tested before use.
