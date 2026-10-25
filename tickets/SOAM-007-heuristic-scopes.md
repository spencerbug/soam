---
schema_version: 1
id: "SOAM-007"
title: "Compare unfiltered, sparse, random, and sensitivity-based scopes"
type: "experiment"
status: "backlog"
priority: "P1"
milestone: "M3"
work_packages: ["WP-04"]
hypotheses: ["H3"]
depends_on: ["SOAM-006"]
labels: ["type:experiment", "priority:P1", "milestone:M3"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-007: Compare unfiltered, sparse, random, and sensitivity-based scopes

## Problem / hypothesis

Before learning a translator, establish whether simple scope filters reduce interference at comparable adaptation performance.

Specification: [research plan §10, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Apply unfiltered, fixed sparse, random sparse, and sensitivity-based masks to the same reference writer.
- Introduce isolated context-specific corrections and evaluate every protected context.

## Acceptance criteria

- [ ] Match update sparsity/rank where applicable and report mask-estimation compute.
- [ ] Compare retention at matched new-task accuracy, not merely equal learning rate or iteration count.
- [ ] Fit sensitivity statistics only from allowed training/evidence data.
- [ ] Report adaptation-retention curves and failures across multiple seeds.

## Metrics / evidence

Old-task error increase at matched new-task error, speed of adaptation, sparsity/rank, mask cost, and rollout stability.

## Dependencies

- [SOAM-006](SOAM-006-gate-2.md) — Gate 2: decide whether local acquisition is viable

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
