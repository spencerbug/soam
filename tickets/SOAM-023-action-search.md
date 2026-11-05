---
schema_version: 2
id: "SOAM-023"
title: "Implement candidate action search and known goal costs"
type: "engineering"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M7"
work_packages: ["WP-11"]
hypotheses: ["H7"]
depends_on: ["SOAM-052", "SOAM-037"]
labels: ["type:engineering", "priority:P1", "milestone:M7"]
assignees: []
created: "2026-10-25"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-023: Implement candidate action search and known goal costs

## Recommended thinking

**high** — Integrate concurrent belief states with bounded action search while keeping motor authority, imagined states, and live memory isolated.

## Problem / hypothesis

Separate the value of an accurate world model from policy-learning quality by testing simple action search first.

Specification: [research plan §14](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.3 shared-population revision — 2026-11-05

Use the conditions supported by SOAM-052 and SOAM-037. Candidate planning rollouts snapshot the complete shared population; feature, relation, action, current-state, and goal activity may overlap, while estimated actual state and desired state remain logically distinguishable.

The [v0.3 scope](../docs/RESEARCH_SPEC_V0_3.md) governs current topology and
platform use; earlier scope notes below retain dependency history only.

### Historical v0.2 scope revision — 2026-11-01

The [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md) replaces the richer-sensing gate dependency with the handover gate and synthetic belief experiment. Begin only in observation/action conditions supported by their reports; if the belief experiment fails to supply usable states, revise before control trials. Use simple sensing and known goal costs defined on permitted observations/model outputs. A handover is not automatically an action, and a motor action need not end at a perceptual switch.

### Bounded work

- Add exhaustive search or MPC over a small discrete action space and a known, documented goal cost.
- Simulate candidate successors, execute one selected action, observe, and replan.

## Acceptance criteria

- [ ] Verify imagined rollouts cannot overwrite live shared activity or persistent memory; distinguish attention shifts from motor authority and account for every rollout copy.

- [ ] Tests prove candidate rollouts do not mutate persistent weights, evidence buffers, or the active real-world state.
- [ ] Only executed/observed transitions can trigger grounded writes; initial search freezes persistent memory and all candidate simulations isolate live states.
- [ ] Implement reactive and simple search/oracle references with their information advantages explicitly labeled.
- [ ] Record candidate count, horizon, model calls, success, risk/collision costs, and latency.

## Metrics / evidence

Goal success, steps-to-goal, model error along plans, failures, simulated transitions, and planning time.

## Dependencies

- [SOAM-052](SOAM-052-shared-population-gate.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-037](SOAM-037-attention-belief-instances.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Future capability** (R5/R9/R10) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Retain as the richer integration/concurrency/control path with existing empirical prerequisites. E3 is a smaller independent supplied-policy test and does not pass this ticket or its gate. No human-like intelligence claim follows from completed components.

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
