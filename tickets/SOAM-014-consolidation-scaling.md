---
schema_version: 2
id: "SOAM-014"
title: "Measure consolidation error recovery, compute, and fixed-size capacity"
type: "experiment"
status: "backlog"
priority: "P3"
recommended_thinking: "high"
milestone: "M4"
work_packages: ["WP-07"]
hypotheses: ["H4"]
depends_on: ["SOAM-013"]
labels: ["type:experiment", "priority:P3", "milestone:M4"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-014: Measure consolidation error recovery, compute, and fixed-size capacity

## Recommended thinking

**high** — Disentangle capacity, recovery, and compute effects without changing data exposure or hiding regressions.

## Problem / hypothesis

A single successful correction does not establish a useful consolidation mechanism or a favorable compute/capacity trade-off.

Specification: [research plan §11, §17](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

The [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md) retains this conditional learned-consolidation branch and its negative outcomes. It evaluates the mechanism selected for SOAM-013; completion is not required for early belief, composition, or control tests. Simple replay and fixed organization remain legitimate controls; the separate organization gate determines the v0.2 integration configuration.

### Bounded work

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
