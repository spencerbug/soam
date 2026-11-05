---
schema_version: 2
id: "SOAM-038"
title: "Compare shared-population action-relation and skill reuse"
type: "experiment"
status: "backlog"
priority: "P1"
recommended_thinking: "xhigh"
milestone: "M7"
work_packages: ["WP-11", "WP-12"]
hypotheses: ["H5", "H7"]
depends_on: ["SOAM-024", "SOAM-037"]
labels: ["type:experiment", "priority:P1", "milestone:M7"]
assignees: []
created: "2026-11-01"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-038: Compare shared-population action-relation and skill reuse

## Recommended thinking

**xhigh** — Separate relational skill reuse from memorized state pairs and validate source/motor/successor coupling under feedback.

## Problem / hypothesis

A source and desired transformation may cue reusable action dynamics in shared neurons, but similar-looking transitions need not permit the same action.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.3 shared-population revision — 2026-11-05

Express feature, source/target relationship, and action-relation information through the same supported recurrent population. A skill is a dynamical pattern/mode, not necessarily a dedicated circuit. Compare a separated action-memory network and explicit pair-table control.

The [v0.3 scope](../docs/RESEARCH_SPEC_V0_3.md) governs current topology and
platform use; earlier scope notes below retain dependency history only.

- Use a bounded scaffolded skill library and validated synthetic control task; compare source-only, explicit state-pair table, relational associative retrieval, and ordinary feedback-controller references.
- Track source state, motor phase, and estimated successor concurrently; keep desired successor separate and allow actions within or across perceptual handovers.
- Include an explicit dynamical skill candidate with disclosed basins/cues and held-out source-target combinations, parameters, and applicability constraints.

## Acceptance criteria

- [ ] Test held-out feature/relation/action combinations and shared-unit/asymmetric-connection ablations, reporting motor completion, negative transfer, and representation interference.

- [ ] Preregister held-out pairs/families, constraint changes, seed/split budgets, success metrics, and inappropriate-reuse rejection criteria.
- [ ] Compare skill reuse and closed-loop completion with no-feedback and no-successor-tracking ablations under disclosed total resources.
- [ ] Verify separate motor authority, interrupt/termination behavior, actual-versus-desired state, and no persistent memory writes from imagined outcomes.
- [ ] Report negative transfer and distinguish supplied skills/associations from learned retrieval and learned motor dynamics.

## Metrics / evidence

Expected report: reports/ASSOCIATIVE_SKILL_TRANSFER.md. Record skill fitting/exposure, controller/weight/state/library storage, executed versus imagined transitions, and switch/control latency.

## Dependencies

- [SOAM-024](SOAM-024-planning-benchmark.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-037](SOAM-037-attention-belief-instances.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Branch conditions

If skill transfer fails while search succeeds, retain search as a scoped control option for SOAM-026 and leave learned skill reuse unsupported. Revise retrieval/binding only through a bounded follow-up; do not make all skill mechanisms prerequisites.

## Scientific review disposition — 2026-11-05

**Future capability** (R5/R9/R10) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Retain as the richer integration/concurrency/control path with existing empirical prerequisites. E3 is a smaller independent supplied-policy test and does not pass this ticket or its gate. No human-like intelligence claim follows from completed components.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
