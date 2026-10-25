---
schema_version: 2
id: "SOAM-016"
title: "Benchmark withheld compositions and transfer to related tasks"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "xhigh"
milestone: "M5"
work_packages: ["WP-08"]
hypotheses: ["H5"]
depends_on: ["SOAM-015"]
labels: ["type:experiment", "priority:P2", "milestone:M5"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-016: Benchmark withheld compositions and transfer to related tasks

## Recommended thinking

**xhigh** — Design withheld compositions that distinguish reusable transformations from interpolation and leakage.

## Problem / hypothesis

Good prediction and retention can reflect memorization. H5 requires generalization to combinations or tasks not used to tune the system.

Specification: [research plan §12, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Create composable rotation, translation, scale, reflection where valid, and nonlinear transformations.
- Run withheld-composition and sequential shared-primitive transfer experiments against matched recurrent/associative references.

## Acceptance criteria

- [ ] Freeze split construction and leakage checks before tuning; distinguish interpolation, memorization, composition, and transfer.
- [ ] Compare learning a new related task after prior tasks with an otherwise matched independent-learning control.
- [ ] Ablate consolidation and scope separately while accounting for parameters, evidence, and compute.
- [ ] Publish per-family/seed results with an explicit uncertainty/effect-size plan and all negative transfer.

## Metrics / evidence

Withheld-composition NMSE, observations-to-target on new tasks, positive/negative transfer, retention, and compute.

## Dependencies

- [SOAM-015](SOAM-015-gate-4.md) — Gate 4: decide whether learned consolidation adds value over replay

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
