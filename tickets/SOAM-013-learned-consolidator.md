---
schema_version: 2
id: "SOAM-013"
title: "Train a learned iterative low-rank consolidator"
type: "experiment"
status: "backlog"
priority: "P3"
recommended_thinking: "xhigh"
milestone: "M4"
work_packages: ["WP-07"]
hypotheses: ["H4"]
depends_on: ["SOAM-010", "SOAM-012", "SOAM-041"]
labels: ["type:experiment", "priority:P3", "milestone:M4"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-013: Train a learned iterative low-rank consolidator

## Recommended thinking

**xhigh** — Develop unrolled learned weight refinement with stable optimization and a fair replay comparison.

## Problem / hypothesis

Determine whether learned iterative corrections provide value beyond conventional replay under grounded validation.

Specification: [research plan §11, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

The [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md) makes learned refinement conditional. Before starting, cite a measured replay/retention limitation from the multi-circuit acquisition evidence, name the metric to improve, and document why the selected representation supports a low-rank proposal. If no such need is established, remain deferred even when metadata dependencies are complete. This branch is not a prerequisite for early composition, grounding, control, or the simple fixed-capacity organization study.

### Bounded work

- Use compressed weight/error/scope/interference statistics to propose low-rank corrections.
- Train with a bounded meta-learning/unrolled procedure and commit only through shadow validation.

## Acceptance criteria

- [ ] Compare no consolidation, replay-only, and learned refinement at matched or explicitly reported observation and compute budgets.
- [ ] Keep meta-training and final task families separate; include model/optimizer/buffer memory in accounting.
- [ ] Measure retention, prediction, changed-task adaptation, and the cost of candidate rejection.
- [ ] Publish negative outcomes if learned refinement cannot beat replay; do not introduce flow matching in this ticket.

## Metrics / evidence

Retention/prediction gain versus replay, update rank, meta-training cost, online consolidation cost, and stability.

## Dependencies

- [SOAM-010](SOAM-010-gate-3.md) — required completed prerequisite; decision prerequisites require proceed.
- [SOAM-012](SOAM-012-shadow-validation.md) — required completed prerequisite; decision prerequisites require proceed.
- [SOAM-041](SOAM-041-multicircuit-acquisition-gate.md) — required completed prerequisite; decision prerequisites require proceed.

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
