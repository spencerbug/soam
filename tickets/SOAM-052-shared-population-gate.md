---
schema_version: 2
id: "SOAM-052"
title: "Review evidence for useful shared recurrence"
type: "decision"
status: "backlog"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-051"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-052: Review evidence for useful shared recurrence

## Recommended thinking

**xhigh** — Assess a prespecified benefit and interference trade-off without extending a minimal pilot into claims about concurrency, learning, or integration.

## Problem / hypothesis

A preferred shared architecture and passing engineering fixtures cannot authorize scientific claims or broad integration.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Review the complete minimal pilot against its frozen benefit, retention, causal-overlap, validity, and resource criteria.
- Record the supported mechanism and operating limits separately from the next-experiment selection in SOAM-059.

## Acceptance criteria

- [ ] Record proceed only for supported useful sharing with causal shared-unit evidence and satisfied guardrails; report attraction evidence separately.
- [ ] Record revise for a bounded unresolved/confounded result or stop for a clear failure of the tested claim; no advantage must not be relabeled success because recurrence runs.
- [ ] Do not require or claim concurrent binding/handover, acquisition, or integration from this pilot. A proceed permits testing those capabilities, subject to fork selection and their own criteria.
- [ ] Preserve failed gates. SOAM-059 may select a diagnostic or alternative application after negative evidence, but cannot convert it into a positive sharing result.

## Metrics / evidence

Planned report: reports/SHARED_POPULATION_GATE.md. SOAM-036 remains the historical v1 decision; neither it nor this design preference substitutes for this measured review.

## Dependencies

- [SOAM-051](SOAM-051-shared-population-study.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R1/R2/R3) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Implement, measure, or review E1 against the frozen protocol and review defaults. Report performance utility separately from attraction and from biological/semantic claims. Require matched random/disjoint lesions and a competent GRU; no capacity or information advantage may be relabeled a sharing effect.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Set decision to proceed,
revise, or stop only after completing the review.
