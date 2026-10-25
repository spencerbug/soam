---
schema_version: 2
id: "SOAM-023"
title: "Implement candidate action search and known goal costs"
type: "engineering"
status: "backlog"
priority: "P2"
recommended_thinking: "medium"
milestone: "M7"
work_packages: ["WP-11"]
hypotheses: ["H7"]
depends_on: ["SOAM-022"]
labels: ["type:engineering", "priority:P2", "milestone:M7"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-023: Implement candidate action search and known goal costs

## Recommended thinking

**medium** — Implement bounded candidate search and known goal costs against established model interfaces.

## Problem / hypothesis

Separate the value of an accurate world model from policy-learning quality by testing simple action search first.

Specification: [research plan §14](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Add exhaustive search or MPC over a small discrete action space and a known, documented goal cost.
- Simulate candidate successors, execute one selected action, observe, and replan.

## Acceptance criteria

- [ ] Tests prove candidate rollouts do not mutate persistent weights, evidence buffers, or the active real-world state.
- [ ] Only executed/observed transitions can trigger grounded writes.
- [ ] Implement reactive and simple search/oracle references with their information advantages explicitly labeled.
- [ ] Record candidate count, horizon, model calls, success, risk/collision costs, and latency.

## Metrics / evidence

Goal success, steps-to-goal, model error along plans, failures, simulated transitions, and planning time.

## Dependencies

- [SOAM-022](SOAM-022-gate-6.md) — Gate 6: review sensory grounding and belief recovery

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
