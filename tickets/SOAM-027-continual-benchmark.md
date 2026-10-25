---
schema_version: 1
id: "SOAM-027"
title: "Integrate an extended continual embodied-learning benchmark"
type: "experiment"
status: "backlog"
priority: "P2"
milestone: "M8"
work_packages: ["WP-13"]
hypotheses: ["H8"]
depends_on: ["SOAM-018", "SOAM-026"]
labels: ["type:experiment", "priority:P2", "milestone:M8"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-027: Integrate an extended continual embodied-learning benchmark

## Problem / hypothesis

The program’s central question is whether accumulated experience improves subsequent learning while retaining earlier competence.

Specification: [research plan §15, §17](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Combine multiple objects, re-identification, changed dynamics, shared motor primitives, novel compositions, and interrupted/resumed tasks.
- Progress from small 2D tasks to a justified richer simulation only after the fixed-size system is characterized.

## Acceptance criteria

- [ ] Predefine task orders, interruption schedules, fixed capacity, exposure budgets, and unacceptable-forgetting thresholds.
- [ ] Compare the integrated system with ordinary continual gradients, replay, task-specific and mechanism-ablated references.
- [ ] Periodically measure old-task retention, acquisition of new related tasks, transfer, planning, consolidation cost, and stability.
- [ ] Report saturation and adverse transfer without adding capacity to hide failure; any growth policy requires a separate later ticket.

## Metrics / evidence

Continual learning curves, old/new-task errors, forward/backward transfer, planning success, capacity, wall time and total memory.

## Dependencies

- [SOAM-018](SOAM-018-gate-5.md) — Gate 5: assess compositional reuse rather than memory maintenance
- [SOAM-026](SOAM-026-gate-7.md) — Gate 7: assess planning benefit and safe memory separation

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
