---
schema_version: 2
id: "SOAM-015"
title: "Gate 4: decide whether learned consolidation adds value over replay"
type: "decision"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M4"
work_packages: ["WP-07"]
hypotheses: ["H4"]
depends_on: ["SOAM-014"]
labels: ["type:decision", "priority:P1", "milestone:M4"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-015: Gate 4: decide whether learned consolidation adds value over replay

## Recommended thinking

**high** — Determine whether learned refinement adds value over replay and constrain downstream conclusions.

## Problem / hypothesis

Consolidation is supported only if useful gains survive a fair comparison with replay and acceptable regressions elsewhere.

Specification: [research plan §11, §19](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Review retention, prediction, capacity, and compute scaling evidence.
- Choose the consolidation reference and state what a negative learned-refinement result means.

## Acceptance criteria

- [ ] Identify a preregistered important metric with a meaningful advantage and quantify regressions and uncertainty.
- [ ] Report all extra observation, meta-training, and inference compute.
- [ ] Record proceed/revise/stop; a failure to beat replay is not automatically a rejection of the entire SOAM program.
- [ ] If proceeding with replay after a negative learned result, record that architectural revision explicitly and update downstream dependencies; do not present H4’s stronger claim as supported.

## Metrics / evidence

Gate 4 decision with the selected mechanism, compute budget, and exact supported/unsupported claims.

## Dependencies

- [SOAM-014](SOAM-014-consolidation-scaling.md) — Measure consolidation error recovery, compute, and fixed-size capacity

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
Set frontmatter `decision` to `proceed`, `revise`, or `stop` only when the decision is documented.
