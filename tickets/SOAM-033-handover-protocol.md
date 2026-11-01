---
schema_version: 2
id: "SOAM-033"
title: "Specify cue-driven handover and circuit-layout controls"
type: "research"
status: "ready"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-032"]
labels: ["type:research", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-033: Specify cue-driven handover and circuit-layout controls

## Recommended thinking

**xhigh** — Separate attractor recruitment from scripted routing and choose a bounded topology comparison before coding.

## Problem / hypothesis

The first v0.2 question is whether attended, tracking, and primed roles support cue-driven handover with grounded continuity. Prediction is a minimum usefulness check, not the main optimization target.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Specify a small synthetic sensorimotor task, fixed projection, declared cues, and fixed persistent weights during measured trials.
- Compare an explicit attractor candidate and ordinary recurrent control; choose a bounded shared-population versus separated-state comparison. Evaluate parallel circuits, shared-weight clones, alternating banks, and columns/stacks as design alternatives without requiring all implementations.
- Define circuit/instance interfaces, primed-state cost, cue coupling, calibration, scheduling, and source retention. Review focused primary sources for the chosen attractor mechanism.

## Acceptance criteria

- [ ] Publish a protocol with equations, input conditions, scaffold ledger, topology/parameter/state ownership, and testable attraction and switching claims.
- [ ] Preregister multiple fixed seeds, train/development/confirmation streams, numeric thresholds, observation/compute budgets, failure handling, and a bounded trial matrix.
- [ ] Include pre-tracking, cold start, equal-history reconstruction, cue removal/shuffling, sensory-feedback ablation, single-population control, and labeled oracle correspondence.
- [ ] Measure dynamical recruitment separately from explicit selection; define recovery/collapse tests and simple post-switch prediction/continuity checks. Explain what a negative result rules out.

## Metrics / evidence

Protocol artifact: docs/HANDOVER_PROTOCOL.md (to be created). Record selected candidate equations, source references, numerical settings, metrics and budgets; no empirical claim is required to complete this planning task.

## Dependencies

- [SOAM-032](SOAM-032-embodied-scope-revision.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
