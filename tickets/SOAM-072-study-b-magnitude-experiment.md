---
schema_version: 2
id: "SOAM-072"
title: "Measure magnitude-sensitive correction on fresh streams"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-070", "SOAM-071"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: null
---

# SOAM-072: Measure magnitude-sensitive correction on fresh streams

## Recommended thinking

**high** — Isolate a missing magnitude-dependent input capability using fresh streams while preserving the completed v1 tradeoff and cumulative resource ceiling.

## Problem / hypothesis

The owner requested magnitude-dependent sensory correction. V1 uses affine signed inputs, a limited gate that cannot directly represent magnitude. [SOAM-069](SOAM-069-study-b-decision.md) preserves that result and identifies this scope gap.

## Scope

Measure magnitude-sensitive correction on fresh streams. Follow the [supplement protocol](../docs/STUDY_B_MAGNITUDE_PROTOCOL.md). One bounded corrective comparison, no new branch or budget.

## Acceptance criteria

- [x] Complete this phase with exact provenance, tests or measured evidence.
- [x] Keep v1 unchanged; use fresh data and freeze selections before confirmation.
- [x] Report all controls, resource costs and negative or inconclusive outcomes.

## Metrics / evidence

Same pre-correction endpoint and four guards as v1; GN32 versus PC32 and original GA32. Seven candidates, two settings, two development roots, ten confirmation roots and one prescribed repeat. At most 112 new fits within the original cumulative 7200 CPU / 14400 wall seconds and 2 GiB RSS/artifact ceiling.

## Dependencies

- [SOAM-070](SOAM-070-study-b-magnitude-protocol.md) — complete evidence or proceed contract.
- [SOAM-071](SOAM-071-study-b-magnitude-harness.md) — complete evidence or proceed contract.

## Branch conditions

The fresh routing record is SOAM-070, based on SOAM-068 completed evidence, not the revise decision SOAM-069. The original owner request authorizes completing this missing comparison. Protocol proceed precedes implementation; engineering verification and a frozen receipt precede confirmation. Historical gates and v1 remain unchanged.

## Completion record

Completed 112 fits (7 fixture, 28 development, 70 confirmation, 7 repeat), no failures. Frozen receipt `4d6ee69672cb521b924a59d475c0282b451520503411f78964e3da76b96b2dfb`; source commit `21084476c334dd4d683dde056f0522ad3947b547`, fingerprint `7c2b3d21e32ea875f5ae9e7914fd4e099bb57ceaa8abe68163fc5ebc77d8833b`. All 28 repeat hash checks match, and independent reduction of 840 values matches. Fresh roots and selected settings are in the [report](../reports/STUDY_B.md) and [receipt](../reports/study-b-magnitude/confirmation-receipt.json). Outcome: negative practical advantage; GN32 gains 1.61% over PC32 and 0.035% over GA32, with both adjusted intervals excluding the declared 10% benefit. All eight guard margins pass. V1 remains unchanged. The [cumulative ledger](../reports/study-b/resource-final.json) totals 368 fits, 1422.60 CPU seconds, 0.822 GiB peak RSS and 0.517 GiB artifacts. Full suite: 238 tests passed; see [verification](../reports/STUDY_B_IMPLEMENTATION.md). Commands: all six phases of `uv run python -m soam.temporal.magnitude`, independent `scripts/finalize_study_b.py`, and the prescribed repeat. No exclusions, retries or new branch.
