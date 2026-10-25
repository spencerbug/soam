---
schema_version: 2
id: "SOAM-029"
title: "Conditionally investigate flow-based consolidation"
type: "experiment"
status: "backlog"
priority: "P3"
recommended_thinking: "xhigh"
milestone: "MX"
work_packages: ["WP-07"]
hypotheses: ["H4"]
depends_on: ["SOAM-015"]
labels: ["type:experiment", "priority:P3", "milestone:MX"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-029: Conditionally investigate flow-based consolidation

## Recommended thinking

**xhigh** — Define useful flow endpoints and account for parameter symmetries before comparing weight-space refinement.

## Problem / hypothesis

Weight-space flow matching is an optional extension, justified only after useful learned iterative correction has been established.

Specification: [research plan §5, §11, §20](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Define improved endpoints using grounded behavior and functional trajectory descriptors.
- Investigate parameter symmetries and compare flow-based refinement with the accepted learned/replay references.

## Acceptance criteria

- [ ] Start only if Gate 4 explicitly found useful learned iterative refinement; a proceed-with-replay revision does not satisfy this prerequisite.
- [ ] Define endpoint construction, symmetry handling, training distribution, and compute budget before fitting a flow.
- [ ] Compare functional gains and stability at matched or disclosed extra compute.
- [ ] Retain a negative result without making flow matching a prerequisite for the main program.

## Metrics / evidence

Functional endpoint quality, retention/prediction, flow stability, symmetry sensitivity, and training/inference cost.

## Dependencies

- [SOAM-015](SOAM-015-gate-4.md) — Gate 4: decide whether learned consolidation adds value over replay

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.

Optional branch. It is not a dependency of any required ticket. Its conditional readiness must be reviewed manually even when SOAM-015 is done.
