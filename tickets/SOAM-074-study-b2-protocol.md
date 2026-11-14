---
schema_version: 2
id: "SOAM-074"
title: "Specify and select robust Kalman correction"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-073"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: "proceed"
---

# SOAM-074: Specify and select robust Kalman correction

## Recommended thinking

**xhigh** — Separate statistical identifiability, numerical validity and root-level evidence in a finite correction search.

## Problem / hypothesis

FILTER2 has strong ordinary prediction and a corruption failure; B2 tests the smallest robust corrector.

## Scope

Specify and select robust Kalman correction. Follow [B2 v1](../docs/STUDY_B2_PROTOCOL.md). Owner explicitly selects B2 after completed B; no other branch or Study C implementation.

## Acceptance criteria

- [x] Complete this phase with measured evidence or explicit negative/inconclusive findings.
- [x] Preserve A/B source, results and decisions; enforce no-write and causal scoring.
- [x] Record exact provenance, resource use, tests and all mandatory controls.

## Metrics / evidence

[B2 manifest](../docs/protocols/study_b2_v1.json) owns endpoints, finite allocation and fresh roots. Ordinary J, balanced corruption, genuine-change guards and real inference cost.

## Dependencies

- [SOAM-073](SOAM-073-study-b-interface-decision.md) — completed evidence or proceed contract.

## Branch conditions

SOAM-074 is the fresh routing decision under the owner's explicit B2 assignment; SOAM-073 proceeds only for the interface. Historical SOAM-069 revise and SOAM-052 stop remain immutable. Protocol proceed precedes implementation; tests and fixture precede development; immutable receipt precedes confirmation. SOAM-077 completes before any fresh selection of C.

## Completion record

Decision: proceed for bounded B2 v1 only. Reviewed Study B code, protocol, final decision, historical results and public A/B evidence. Protocol fixes causal API, independently fitted roots, primary family, ambiguity control and new 1800 CPU/3600 wall seconds, 2 GiB RSS/1 GiB artifact limits. Baseline suite before changes: `uv run pytest`, 238 passed in 16.94s. The interface review SOAM-073 is done/proceed; owner explicitly selects B2. Staged extensions remain conditional on development, with no confirmation tuning. Protocol acceptance is not a scientific benefit claim.
