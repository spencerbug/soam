---
schema_version: 2
id: "SOAM-027"
title: "Integrate an extended continual embodied-learning benchmark"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "xhigh"
milestone: "M8"
work_packages: ["WP-13"]
hypotheses: ["H8"]
depends_on: ["SOAM-018", "SOAM-022", "SOAM-026", "SOAM-041", "SOAM-043"]
labels: ["type:experiment", "priority:P2", "milestone:M8"]
assignees: []
created: "2026-10-25"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-027: Integrate an extended continual embodied-learning benchmark

## Recommended thinking

**xhigh** — Integrate continual acquisition, retention, transfer, grounding, and planning into a controlled long-duration benchmark.

## Problem / hypothesis

The program’s central question is whether accumulated experience improves subsequent learning while retaining earlier competence.

Specification: [research plan §15, §17](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.3 shared-population revision — 2026-11-05

Integrate only shared-population mechanisms supported by the new empirical gate and later acquisition/organization gates. Reuse common experiment infrastructure. Localization and learning-module tracks are independent evidence sources, not mandatory prerequisites or automatic gate passes.

The [v0.3 scope](../docs/RESEARCH_SPEC_V0_3.md) governs current topology and
platform use; earlier scope notes below retain dependency history only.

### Historical v0.2 scope revision — 2026-11-01

The [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md) adds empirical multi-circuit acquisition and organization decisions and explicitly retains the richer-grounding gate. The design decision SOAM-039 is not sufficient evidence. Integrate only configurations and scaffold limits selected by those gates, including any explicitly selected fixed-organization control; do not imply unsupervised learning or self-organization when unsupported.

### Bounded work

- Combine multiple objects, re-identification, changed dynamics, shared motor primitives, novel compositions, and interrupted/resumed tasks.
- Progress from small 2D tasks to a justified richer simulation only after the fixed-size system is characterized.

## Acceptance criteria

- [ ] Freeze the total shared-population and auxiliary-memory budget; separately report cross-function transfer, interference, instance binding, and every imported application mechanism or scaffold.

- [ ] Predefine task orders, interruption schedules, fixed capacity, exposure budgets, and unacceptable-forgetting thresholds.
- [ ] Compare the integrated system with ordinary continual gradients, replay, task-specific and mechanism-ablated references.
- [ ] Periodically measure old-task retention, acquisition of new related tasks, transfer, planning, consolidation cost, and stability.
- [ ] Report saturation and adverse transfer without adding capacity to hide failure; any growth policy requires a separate later ticket.

## Metrics / evidence

Continual learning curves, old/new-task errors, forward/backward transfer, planning success, capacity, wall time and total memory.

## Dependencies

- [SOAM-018](SOAM-018-gate-5.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-022](SOAM-022-gate-6.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-026](SOAM-026-gate-7.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-041](SOAM-041-multicircuit-acquisition-gate.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-043](SOAM-043-organization-gate.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Future capability** (R5/R9/R10) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Retain as the richer integration/concurrency/control path with existing empirical prerequisites. E3 is a smaller independent supplied-policy test and does not pass this ticket or its gate. No human-like intelligence claim follows from completed components.

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
