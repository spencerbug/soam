---
schema_version: 1
id: "SOAM-014"
title: "Measure consolidation error recovery, compute, and fixed-size capacity"
type: "experiment"
status: "backlog"
priority: "P1"
milestone: "M4"
work_packages: ["WP-07"]
hypotheses: ["H4"]
depends_on: ["SOAM-013"]
labels: ["type:experiment", "priority:P1", "milestone:M4"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-014: Measure consolidation error recovery, compute, and fixed-size capacity

## Problem / hypothesis

A single successful correction does not establish a useful consolidation mechanism or a favorable compute/capacity trade-off.

Specification: [research plan §11, §17](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Run sequential-context retention and deliberately disruptive-write recovery experiments.
- Sweep a bounded, preregistered iteration budget and number/complexity of regimes with fixed parameter capacity.

## Acceptance criteria

- [ ] Hold observations fixed when varying consolidation computation.
- [ ] Compare learned refinement and replay across the same task orders and seeds.
- [ ] Report capacity only against explicit old/new error and stability thresholds, including saturated failures.
- [ ] Preserve observations, configs, source identities, measured memory/time, and full acquisition/retention curves.

## Metrics / evidence

Experiments 4A–4D: retention, repair without losing new knowledge, gain versus iterations, and capacity versus regimes.

## Dependencies

- [SOAM-013](SOAM-013-learned-consolidator.md) — Train a learned iterative low-rank consolidator

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
