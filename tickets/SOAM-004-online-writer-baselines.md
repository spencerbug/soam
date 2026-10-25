---
schema_version: 2
id: "SOAM-004"
title: "Benchmark online transition correction and changed dynamics"
type: "experiment"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02"]
hypotheses: ["H2"]
depends_on: ["SOAM-003"]
labels: ["type:experiment", "priority:P1", "milestone:M2"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-004: Benchmark online transition correction and changed dynamics

## Recommended thinking

**high** — Compare distinct online learning rules fairly and diagnose their effects on multistep dynamics.

## Problem / hypothesis

A local update rule must learn new or changed dynamics without ordinary end-to-end retraining, and must be compared with simpler alternatives.

Specification: [research plan §9, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Implement no adaptation, Hebbian, delta, local least-squares/RLS, and online-gradient references through the write interface.
- Evaluate unseen transitions and changes to angular speed or damping; include an explicit transition-table reference labeled as a baseline.

## Acceptance criteria

- [ ] Fix adaptation streams, observation budgets, hyperparameter search budgets, and new-task accuracy targets before evaluation.
- [ ] Keep all ordinary training frozen for associative methods and report the gradient reference separately.
- [ ] Compare acquisition curves and free multistep prediction at matched exposure, with storage/compute differences disclosed.
- [ ] Publish per-seed gains, instability, and failures; retain a no-adaptation control and avoid privileged state/context hints beyond the task inputs.

## Metrics / evidence

Observations-to-target, one-step/free NMSE versus writes, instability, update time/operations/bytes, and table storage cost.

## Dependencies

- [SOAM-003](SOAM-003-plastic-write-contract.md) — Define the grounded local-write contract and plastic parameters

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
