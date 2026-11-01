---
schema_version: 2
id: "SOAM-039"
title: "Select a grounded multi-circuit learning contract"
type: "decision"
status: "backlog"
priority: "P1"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3", "H4"]
depends_on: ["SOAM-036", "SOAM-037", "SOAM-038"]
labels: ["type:decision", "priority:P1", "milestone:M2"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-039: Select a grounded multi-circuit learning contract

## Recommended thinking

**xhigh** — Choose writable representations and credit assignment from observed circuit failures while preserving generic and instance memory.

## Problem / hypothesis

The historical single-matrix writer is one comparison, not a validated writer for the expanded architecture. A bounded design decision must precede persistent multi-circuit learning.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Define evidence responsibility, writable parameters/associations/instance facts, frozen generic knowledge, and state calibration boundaries.
- Compare reusing the old transaction/rule with bounded associative alternatives and same-representation online-gradient references; do not require a successful historical writer gate to consider another representation.
- Specify simple replay and shadow-validation contracts and a preregistered acquisition experiment; identify observed needs for scope filters without presuming a learned translator.

## Acceptance criteria

- [ ] Record proceed/revise/stop for one bounded contract with cue/target construction, norm/storage limits, evidence provenance, and no-write prediction invariants.
- [ ] Define how a one-instance exception is written and later recalled without corrupting generic dynamics or another instance.
- [ ] Specify fresh acquisition/retention streams, simple baselines, validation/test separation, and repeatable failure handling before implementation.
- [ ] Explain departures from the old plastic-tensor contract and retain its results; planning proceeds only to empirical acquisition, not directly to integration.

## Metrics / evidence

Expected design/protocol: docs/MULTICIRCUIT_LEARNING_PROTOCOL.md. Cite handover, belief, and skill evidence; this is a design decision and does not establish H2/H3/H4.

## Dependencies

- [SOAM-036](SOAM-036-handover-gate.md) — required completed prerequisite; decision prerequisites must record proceed.
- [SOAM-037](SOAM-037-attention-belief-instances.md) — required completed prerequisite; decision prerequisites must record proceed.
- [SOAM-038](SOAM-038-associative-skill-transfer.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
Set decision to proceed, revise, or stop only when the review is complete.
