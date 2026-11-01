---
schema_version: 2
id: "SOAM-042"
title: "Test predictive specialization and association refinement at fixed capacity"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "xhigh"
milestone: "M4"
work_packages: ["WP-06", "WP-07"]
hypotheses: ["H4", "H5"]
depends_on: ["SOAM-041"]
labels: ["type:experiment", "priority:P2", "milestone:M4"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-042: Test predictive specialization and association refinement at fixed capacity

## Recommended thinking

**xhigh** — Distinguish learned organization from supplied partitions, extra memory, and ordinary replay effects.

## Problem / hypothesis

A fixed pool of circuits may learn useful predictive domains and associations, but competition could collapse or fragment representations.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Compare one bounded specialization/association-refinement mechanism with frozen organization and ordinary replay using the validated learning contract.
- Keep circuit count, total persistent capacity, and evidence budget fixed. Hand-specified boundaries are a labeled control; true regime/part labels remain evaluator-only.
- Measure occupancy, domain overlap, collapse/fragmentation, handover continuity, retention, and held-out reuse; do not add dynamic growth, split/merge controllers, or flow.

## Acceptance criteria

- [ ] Preregister the organization rule, budgets, held-out families, important improvement metric, and unacceptable regression thresholds.
- [ ] Show which domains/associations change through learning and test their causal contribution with freezing or shuffling ablations.
- [ ] Compare against replay at disclosed compute/storage cost and report negative specialization, unstable boundaries, and interference.
- [ ] Preserve source/config/seed and all outcomes; any capacity expansion or new structural operation requires a separate follow-up.

## Metrics / evidence

Expected report: reports/FIXED_CAPACITY_ORGANIZATION.md. Include capacity saturation and supplied-versus-learned structure audit; attractive state plots alone are insufficient.

## Dependencies

- [SOAM-041](SOAM-041-multicircuit-acquisition-gate.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
