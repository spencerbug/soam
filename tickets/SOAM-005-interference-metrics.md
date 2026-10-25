---
schema_version: 1
id: "SOAM-005"
title: "Measure interference and learning without resets"
type: "experiment"
status: "backlog"
priority: "P1"
milestone: "M2"
work_packages: ["WP-03"]
hypotheses: ["H2", "H8"]
depends_on: ["SOAM-004"]
labels: ["type:experiment", "priority:P1", "milestone:M2"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-005: Measure interference and learning without resets

## Problem / hypothesis

Improving a new transition may damage old behavior. The project needs functional interference measurements rather than weight-change size alone.

Specification: [research plan §9, §10, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Add task-by-training-stage error matrices, signed old-task error changes, and forgetting relative to each task’s historical best.
- Run prolonged no-reset sequences with revisits, context switches, and successive grounded updates.

## Acceptance criteria

- [ ] Validate metrics on controlled no-op, beneficial, and deliberately destructive updates.
- [ ] Separate preserving old predictions from matching reliable old observation targets so legitimate corrections are not penalized blindly.
- [ ] Report acquisition and retention jointly, including cumulative drift and confidence/spread across seeds.
- [ ] Save before/after protected trajectories and an evaluation-only evidence set excluded from adaptation.

## Metrics / evidence

Old-task error increase, forgetting, transfer sign, accumulated drift, observations-to-adapt, and protected-rollout disruption.

## Dependencies

- [SOAM-004](SOAM-004-online-writer-baselines.md) — Benchmark online transition correction and changed dynamics

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
