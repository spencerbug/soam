---
schema_version: 2
id: "SOAM-071"
title: "Implement magnitude inputs for sensory and motion gain"
type: "engineering"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-070"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: null
---

# SOAM-071: Implement magnitude inputs for sensory and motion gain

## Recommended thinking

**high** — Isolate a missing magnitude-dependent input capability using fresh streams while preserving the completed v1 tradeoff and cumulative resource ceiling.

## Problem / hypothesis

The owner requested magnitude-dependent sensory correction. V1 uses affine signed inputs, a limited gate that cannot directly represent magnitude. [SOAM-069](SOAM-069-study-b-decision.md) preserves that result and identifies this scope gap.

## Scope

Implement magnitude inputs for sensory and motion gain. Follow the [supplement protocol](../docs/STUDY_B_MAGNITUDE_PROTOCOL.md). One bounded corrective comparison, no new branch or budget.

## Acceptance criteria

- [x] Complete this phase with exact provenance, tests or measured evidence.
- [x] Keep v1 unchanged; use fresh data and freeze selections before confirmation.
- [x] Report all controls, resource costs and negative or inconclusive outcomes.

## Metrics / evidence

Same pre-correction endpoint and four guards as v1; GN32 versus PC32 and original GA32. Seven candidates, two settings, two development roots, ten confirmation roots and one prescribed repeat. At most 112 new fits within the original cumulative 7200 CPU / 14400 wall seconds and 2 GiB RSS/artifact ceiling.

## Dependencies

- [SOAM-070](SOAM-070-study-b-magnitude-protocol.md) — complete evidence or proceed contract.

## Branch conditions

The fresh routing record is SOAM-070, based on SOAM-068 completed evidence, not the revise decision SOAM-069. The original owner request authorizes completing this missing comparison. Protocol proceed precedes implementation; engineering verification and a frozen receipt precede confirmation. Historical gates and v1 remain unchanged.

## Completion record

Implemented GN32/GMN32/AMN32 with explicit residual RMS and action norm; unchanged PC16/PC32/GA32/FILTER2 controls. Five new channel/freshness/reproduction tests and 23 focused temporal tests pass. Full suite 238 tests passed; fixture passes with 546.25 projected additional CPU seconds and 300 MB projected artifacts, carrying v1 allocation. Source commit 2108447; no original v1 code or scientific result changed.
