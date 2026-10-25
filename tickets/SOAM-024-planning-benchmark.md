---
schema_version: 2
id: "SOAM-024"
title: "Benchmark navigation, changed dynamics, and planning horizons"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "high"
milestone: "M7"
work_packages: ["WP-11"]
hypotheses: ["H7"]
depends_on: ["SOAM-023"]
labels: ["type:experiment", "priority:P2", "milestone:M7"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
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

- Run navigation, changed motion/obstacles, and context switching with shared activity primitives.
- Sweep a bounded horizon/candidate budget and compare no adaptation with grounded fast updates.

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
