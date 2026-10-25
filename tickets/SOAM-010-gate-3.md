---
schema_version: 2
id: "SOAM-010"
title: "Gate 3: evaluate functional scoping and beneficial sharing"
type: "decision"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M3"
work_packages: ["WP-05"]
hypotheses: ["H3"]
depends_on: ["SOAM-009"]
labels: ["type:decision", "priority:P1", "milestone:M3"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-010: Gate 3: evaluate functional scoping and beneficial sharing

## Recommended thinking

**high** — Assess the central scope hypothesis at matched acquisition accuracy and distinguish sharing from isolation.

## Problem / hypothesis

Functional scope learning is central to SOAM’s novelty. Reduced interference achieved only by task isolation is insufficient.

Specification: [research plan §10, §19](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Review learned versus heuristic scopes across isolated, shared, and noisy task families.
- Decide whether the measured benefit justifies using learned scopes downstream.

## Acceptance criteria

- [ ] Require retention comparisons at matched new-task accuracy and explicit shared-transfer evidence.
- [ ] Report consistency across seeds/families and the adaptation/compute trade-offs.
- [ ] Record proceed/revise/stop, including whether a heuristic reference remains preferable.
- [ ] A persistent failure produces a targeted architectural-revision ticket and keeps dependent learned consolidation unready.

## Metrics / evidence

Gate 3 retention/acquisition/transfer evidence and a documented interpretation of negative results.

## Dependencies

- [SOAM-009](SOAM-009-learned-scope.md) — Meta-train a constrained functional scope translator

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
Set frontmatter `decision` to `proceed`, `revise`, or `stop` only when the decision is documented.
