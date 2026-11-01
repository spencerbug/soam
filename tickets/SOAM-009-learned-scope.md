---
schema_version: 2
id: "SOAM-009"
title: "Meta-train a constrained functional scope translator"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "xhigh"
milestone: "M3"
work_packages: ["WP-05"]
hypotheses: ["H3"]
depends_on: ["SOAM-008"]
labels: ["type:experiment", "priority:P2", "milestone:M3"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-009: Meta-train a constrained functional scope translator

## Recommended thinking

**xhigh** — Design and debug meta-learned plasticity with interacting acquisition, preservation, and sharing objectives.

## Problem / hypothesis

Test whether a learned update filter improves the adaptation-retention trade-off beyond unfiltered and heuristic masks.

Specification: [research plan §5, §10, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

Under the [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md), this is a conditional scoping branch attached to the historical acquisition study. It does not gate early handover, belief tracking, or control. Relate interference/sharing results to evidence responsibility and generic-versus-instance credit, but do not assume that a context mask solves multi-circuit credit assignment. Application to a different plastic representation requires a separately specified comparison. Learned scopes are candidates, not a mandatory architecture component.

### Bounded work

- Start from tractable local state/action/error/sensitivity statistics and a constrained mask or low-rank output.
- Meta-train using new-task prediction, evidence-aware preservation, and update-size objectives.

## Acceptance criteria

- [ ] Separate meta-training, development, and held-out task families; report both outer-loop and online compute.
- [ ] Compare against every heuristic scope at matched new-task accuracy and compatible update budgets.
- [ ] Measure beneficial shared transfer as well as isolated-task retention and noise rejection.
- [ ] Treat the illustrative 50% interference reduction as a protocol choice to preregister, not a guaranteed outcome; publish uncertainty and failed seeds.

## Metrics / evidence

Interference reduction at matched acquisition, transfer, adaptation speed, noise resistance, translator parameters and compute.

## Dependencies

- [SOAM-008](SOAM-008-scope-task-families.md) — Build shared-scope and noisy-evidence task families

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
