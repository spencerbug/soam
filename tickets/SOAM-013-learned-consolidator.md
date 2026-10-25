---
schema_version: 1
id: "SOAM-013"
title: "Train a learned iterative low-rank consolidator"
type: "experiment"
status: "backlog"
priority: "P1"
milestone: "M4"
work_packages: ["WP-07"]
hypotheses: ["H4"]
depends_on: ["SOAM-010", "SOAM-012"]
labels: ["type:experiment", "priority:P1", "milestone:M4"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-013: Train a learned iterative low-rank consolidator

## Problem / hypothesis

Determine whether learned iterative corrections provide value beyond conventional replay under grounded validation.

Specification: [research plan §11, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

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

- [SOAM-010](SOAM-010-gate-3.md) — Gate 3: evaluate functional scoping and beneficial sharing
- [SOAM-012](SOAM-012-shadow-validation.md) — Validate consolidation candidates with shadow weights and rollback

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
