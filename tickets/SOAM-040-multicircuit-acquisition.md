---
schema_version: 2
id: "SOAM-040"
title: "Benchmark grounded multi-circuit acquisition and instance retention"
type: "experiment"
status: "backlog"
priority: "P1"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-039", "SOAM-012"]
labels: ["type:experiment", "priority:P1", "milestone:M2"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-040: Benchmark grounded multi-circuit acquisition and instance retention

## Recommended thinking

**xhigh** — Measure genuine acquisition without confusing state calibration, instance recall, and generic parameter changes.

## Problem / hypothesis

Grounded updates must improve held-out behavior while preserving unrelated circuit and instance knowledge.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Evaluate the implemented multi-circuit learning contract using bounded evidence and shadow validation; keep its frozen protocol and transaction limits.
- Compare no writing, the selected associative rule, a same-representation gradient reference, and simple replay at matched evidence exposure.
- Test changed dynamics and isolated instance exceptions, including revisits and no-reset sequences; keep topology/capacity fixed.

## Acceptance criteria

- [ ] Run baseline tests before code edits and verify no-write inference, target exclusion, generic/instance isolation, rollback, and reproducibility.
- [ ] Publish acquisition curves, later instance recall, old-task retention, handover recovery, and free multistep effects for all seeds.
- [ ] Use development-only acceptance/tuning and untouched confirmation data; disclose every write/history/replay exposure and storage/compute cost.
- [ ] Retain harmful writes and failed rules in the report; do not add capacity or unfreeze unapproved parameters to rescue results.

## Metrics / evidence

Expected report: reports/MULTICIRCUIT_ACQUISITION.md. Configuration/source/seed/software artifacts and replay/shadow costs follow the common evidence requirements.

## Dependencies

- [SOAM-039](SOAM-039-grounded-memory-design.md) — required completed prerequisite; decision prerequisites must record proceed.
- [SOAM-012](SOAM-012-shadow-validation.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
