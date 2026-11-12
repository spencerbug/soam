---
schema_version: 2
id: "SOAM-073"
title: "Review both Study B versions and select the inference interface"
type: "decision"
status: "backlog"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-068", "SOAM-072"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: null
---

# SOAM-073: Review both Study B versions and select the inference interface

## Recommended thinking

**xhigh** — Isolate a missing magnitude-dependent input capability using fresh streams while preserving the completed v1 tradeoff and cumulative resource ceiling.

## Problem / hypothesis

The owner requested magnitude-dependent sensory correction. V1 uses affine signed inputs, a limited gate that cannot directly represent magnitude. [SOAM-069](SOAM-069-study-b-decision.md) preserves that result and identifies this scope gap.

## Scope

Review both Study B versions and select the inference interface. Follow the [supplement protocol](../docs/STUDY_B_MAGNITUDE_PROTOCOL.md). One bounded corrective comparison, no new branch or budget.

## Acceptance criteria

- [ ] Complete this phase with exact provenance, tests or measured evidence.
- [ ] Keep v1 unchanged; use fresh data and freeze selections before confirmation.
- [ ] Report all controls, resource costs and negative or inconclusive outcomes.

## Metrics / evidence

Same pre-correction endpoint and four guards as v1; GN32 versus PC32 and original GA32. Seven candidates, two settings, two development roots, ten confirmation roots and one prescribed repeat. At most 112 new fits within the original cumulative 7200 CPU / 14400 wall seconds and 2 GiB RSS/artifact ceiling.

## Dependencies

- [SOAM-068](SOAM-068-study-b-experiment.md) — complete evidence or proceed contract.
- [SOAM-072](SOAM-072-study-b-magnitude-experiment.md) — complete evidence or proceed contract.

## Branch conditions

The fresh routing record is SOAM-070, based on SOAM-068 completed evidence, not the revise decision SOAM-069. The original owner request authorizes completing this missing comparison. Protocol proceed precedes implementation; engineering verification and a frozen receipt precede confirmation. Historical gates and v1 remain unchanged.

## Completion record

Not completed.
