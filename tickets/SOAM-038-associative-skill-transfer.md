---
schema_version: 2
id: "SOAM-038"
title: "Compare associative skill retrieval across held-out transitions"
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
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-038: Compare associative skill retrieval across held-out transitions

## Recommended thinking

**xhigh** — Separate relational skill reuse from memorized state pairs and validate source/motor/successor coupling under feedback.

## Problem / hypothesis

A source and desired transformation may cue a reusable action circuit, but similar-looking transitions need not permit the same action.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Use a bounded scaffolded skill library and validated synthetic control task; compare source-only, explicit state-pair table, relational associative retrieval, and ordinary feedback-controller references.
- Track source state, motor phase, and estimated successor concurrently; keep desired successor separate and allow actions within or across perceptual handovers.
- Include an explicit dynamical skill candidate with disclosed basins/cues and held-out source-target combinations, parameters, and applicability constraints.

## Acceptance criteria

- [ ] Preregister held-out pairs/families, constraint changes, seed/split budgets, success metrics, and inappropriate-reuse rejection criteria.
- [ ] Compare skill reuse and closed-loop completion with no-feedback and no-successor-tracking ablations under disclosed total resources.
- [ ] Verify separate motor authority, interrupt/termination behavior, actual-versus-desired state, and no persistent memory writes from imagined outcomes.
- [ ] Report negative transfer and distinguish supplied skills/associations from learned retrieval and learned motor dynamics.

## Metrics / evidence

Expected report: reports/ASSOCIATIVE_SKILL_TRANSFER.md. Record skill fitting/exposure, controller/weight/state/library storage, executed versus imagined transitions, and switch/control latency.

## Dependencies

- [SOAM-024](SOAM-024-planning-benchmark.md) — required completed prerequisite; decision prerequisites must record proceed.
- [SOAM-037](SOAM-037-attention-belief-instances.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
