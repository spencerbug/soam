---
schema_version: 2
id: "SOAM-042"
title: "Test overlapping assembly organization at fixed capacity"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "xhigh"
milestone: "M4"
work_packages: ["WP-06", "WP-07"]
hypotheses: ["H4", "H5"]
depends_on: ["SOAM-041", "SOAM-052"]
labels: ["type:experiment", "priority:P2", "milestone:M4"]
assignees: []
created: "2026-11-01"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-042: Test overlapping assembly organization at fixed capacity

## Recommended thinking

**xhigh** — Distinguish learned organization from supplied partitions, extra memory, and ordinary replay effects.

## Problem / hypothesis

A fixed shared population may learn useful overlapping assemblies and associations, but competition could collapse or fragment representations.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.3 shared-population revision — 2026-11-05

Study organization of overlapping assemblies/connectivity within a fixed shared population. Separate circuits are controls, not the unit of organization assumed by the primary candidate. Report supplied versus learned overlap and whether specialization merely partitions away all sharing.

The [v0.3 scope](../docs/RESEARCH_SPEC_V0_3.md) governs current topology and
platform use; earlier scope notes below retain dependency history only.

- Compare one bounded specialization/association-refinement mechanism with frozen organization and ordinary replay using the validated learning contract.
- Keep total neuron count, persistent capacity, active-state capacity, and evidence budget fixed. Hand-specified boundaries are a labeled control; true regime/part labels remain evaluator-only.
- Measure occupancy, domain overlap, collapse/fragmentation, handover continuity, retention, and held-out reuse; do not add dynamic growth, split/merge controllers, or flow.

## Acceptance criteria

- [ ] Measure learned overlap, cross-function transfer/interference, occupancy and collapse with causal freezing/shuffling controls; count all units, weights, live states, and auxiliary memories.

- [ ] Preregister the organization rule, budgets, held-out families, important improvement metric, and unacceptable regression thresholds.
- [ ] Show which domains/associations change through learning and test their causal contribution with freezing or shuffling ablations.
- [ ] Compare against replay at disclosed compute/storage cost and report negative specialization, unstable boundaries, and interference.
- [ ] Preserve source/config/seed and all outcomes; any capacity expansion or new structural operation requires a separate follow-up.

## Metrics / evidence

Expected report: reports/FIXED_CAPACITY_ORGANIZATION.md. Include capacity saturation and supplied-versus-learned structure audit; attractive state plots alone are insufficient.

## Dependencies

- [SOAM-041](SOAM-041-multicircuit-acquisition-gate.md) — required completed prerequisite; decision prerequisites require proceed and applicable body conditions.
- [SOAM-052](SOAM-052-shared-population-gate.md) — required completed prerequisite; decision prerequisites require proceed and applicable body conditions.

## Scientific review disposition — 2026-11-05

**Future capability** (R9/R10) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Remain deferred. Shared overlapping-assembly organization now explicitly requires the sharing gate as well as acquisition, because the early E2 path no longer inherits sharing/concurrency prerequisites. If the mechanism needs replay/shadow infrastructure, require SOAM-011/012 before those operations; do not silently add them to E2.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
