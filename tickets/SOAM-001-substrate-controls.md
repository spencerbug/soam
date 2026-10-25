---
schema_version: 2
id: "SOAM-001"
title: "Strengthen substrate controls and budget comparisons"
type: "experiment"
status: "ready"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1"]
depends_on: ["SOAM-000"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-001: Strengthen substrate controls and budget comparisons

## Recommended thinking

**high** — Design fair capacity controls and unseen-switch evaluations without leaking test evidence into tuning.

## Problem / hypothesis

The current screen passes, but separate cores share sensory interfaces, context variants have unequal parameter counts, and switch timing is regular. These gaps limit the case for proceeding to plasticity.

Specification: [research plan §8, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Compare the additive reference with a conventional GRU, fully independent per-context predictors, and budget-matched shared variants.
- Test unseen switch schedules, held-out action paths, and perturbation responses at multiple horizons; retain the original benchmark.

## Acceptance criteria

- [ ] Freeze development/test streams, parameter tolerances, compute accounting, and readiness criteria before running the new comparison.
- [ ] Report total parameters, exposure, runtime, and the switching semantics of each baseline; disclose any required sensory reset for independent predictors.
- [ ] Run multiple fixed seeds and report per-context, per-horizon, switching, motion-collapse, and perturbation metrics.
- [ ] Publish negative results and identify which claims about shared structure remain untested; do not tune on the original test set.

## Metrics / evidence

One-step/free NMSE, switch recovery, long-horizon drift, invalid rates, paired perturbation gaps, motion energy, parameter bytes and runtime.

## Dependencies

- [SOAM-000](SOAM-000-substrate-baseline.md) — Record the reproducible substrate baseline

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
