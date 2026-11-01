---
schema_version: 2
id: "SOAM-004"
title: "Benchmark online transition correction and changed dynamics"
type: "experiment"
status: "ready"
priority: "P2"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02"]
hypotheses: ["H2"]
depends_on: ["SOAM-003"]
labels: ["type:experiment", "priority:P2", "milestone:M2"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
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

### v0.2 scope revision — 2026-11-01

Under the [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md), this remains a bounded historical low-rank acquisition branch, not the next primary task or a prerequisite for cue-driven handover. Preserve Gate 1 checkpoints, plastic-tensor limits, and the existing rule comparisons. Its results do not establish multi-circuit learning; SOAM-039–041 cover that later contract and empirical gate.

### Bounded work

Use the [SOAM-003 write contract](../soam/plasticity/README.md) and preserve the
[reported multistep regressions](../reports/LOCAL_WRITE_CONTRACT.md). Its example
limits are untuned engineering defaults, not the acquisition protocol. Keep the
online-gradient comparison on the same low-rank substrate/plastic parameter family;
retain GRU as an architectural reference. Use fresh confirmation streams distinct
from substrate controls and the contract demonstration.

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
