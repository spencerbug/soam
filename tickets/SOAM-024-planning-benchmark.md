---
schema_version: 2
id: "SOAM-024"
title: "Benchmark navigation, changed dynamics, and planning horizons"
type: "experiment"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M7"
work_packages: ["WP-11"]
hypotheses: ["H7"]
depends_on: ["SOAM-023"]
labels: ["type:experiment", "priority:P1", "milestone:M7"]
assignees: []
created: "2026-10-25"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-024: Benchmark navigation, changed dynamics, and planning horizons

## Recommended thinking

**high** — Separate planning gains from model accuracy, reactive control strength, and computational budget.

## Problem / hypothesis

Planning must improve actual goal-directed behavior and adapt after environmental changes rather than only score imagined trajectories.

Specification: [research plan §14](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.3 shared-population revision — 2026-11-05

Benchmark planning through shared feature/relation/action dynamics, with separated-function and ordinary recurrent controls. Keep estimated outcomes and desired outcomes distinct even if their neural encodings overlap.

The [v0.3 scope](../docs/RESEARCH_SPEC_V0_3.md) governs current topology and
platform use; earlier scope notes below retain dependency history only.

### Historical v0.2 scope revision — 2026-11-01

Under the [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md), first test closed-loop synthetic control with frozen persistent memory and sensory recalibration. Compare source-only selection with current-plus-successor information and separate motor authority from attention. Grounded persistent adaptation is an optional later comparison only after SOAM-041 proceeds; lack of a writer must not block this initial control benchmark.

### Bounded work

- Run navigation, changed motion/obstacles, and context switching with shared activity primitives.
- Sweep a bounded horizon/candidate budget and compare reactive, source-only, and successor-aware search. Add grounded fast-update comparisons only under the validated later learning contract.

## Acceptance criteria

- [ ] Report control failures from cross-function interference and compare action-conditioned/asymmetry ablations with unchanged observation and compute accounting.

- [ ] Use fixed real-interaction budgets and held-out goals/task instances.
- [ ] Compare reactive control, model-based search, and available model variants with compute/information differences reported.
- [ ] Measure the connection between prediction quality and realized goal success, including model-exploitation failures.
- [ ] Report replanning latency, recovery after changed dynamics, and retained earlier skills.

## Metrics / evidence

Experiments 7A–7D: success, adaptation interactions, retention, horizon sensitivity, risk, and compute.

## Dependencies

- [SOAM-023](SOAM-023-action-search.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Branch conditions

If predictions are adequate but control fails, isolate the search/controller in one bounded diagnostic; if prediction is inadequate, return to a separately scoped model study. Only demonstrated reliable search permits learned proposals (SOAM-025). Do not train a proposal head to conceal model failure.

## Scientific review disposition — 2026-11-05

**Future capability** (R5/R9/R10) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Retain as the richer integration/concurrency/control path with existing empirical prerequisites. E3 is a smaller independent supplied-policy test and does not pass this ticket or its gate. No human-like intelligence claim follows from completed components.

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
