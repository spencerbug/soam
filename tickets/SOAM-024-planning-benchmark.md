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
updated: "2026-11-01"
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

### v0.2 scope revision — 2026-11-01

Under the [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md), first test closed-loop synthetic control with frozen persistent memory and sensory recalibration. Compare source-only selection with current-plus-successor information and separate motor authority from attention. Grounded persistent adaptation is an optional later comparison only after SOAM-041 proceeds; lack of a writer must not block this initial control benchmark.

### Bounded work

- Run navigation, changed motion/obstacles, and context switching with shared activity primitives.
- Sweep a bounded horizon/candidate budget and compare reactive, source-only, and successor-aware search. Add grounded fast-update comparisons only under the validated later learning contract.

## Acceptance criteria

- [ ] Use fixed real-interaction budgets and held-out goals/task instances.
- [ ] Compare reactive control, model-based search, and available model variants with compute/information differences reported.
- [ ] Measure the connection between prediction quality and realized goal success, including model-exploitation failures.
- [ ] Report replanning latency, recovery after changed dynamics, and retained earlier skills.

## Metrics / evidence

Experiments 7A–7D: success, adaptation interactions, retention, horizon sensitivity, risk, and compute.

## Dependencies

- [SOAM-023](SOAM-023-action-search.md) — Implement candidate action search and known goal costs

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
