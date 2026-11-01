---
schema_version: 2
id: "SOAM-041"
title: "Review grounded multi-circuit acquisition and retention"
type: "decision"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-040"]
labels: ["type:decision", "priority:P1", "milestone:M2"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-041: Review grounded multi-circuit acquisition and retention

## Recommended thinking

**high** — Evaluate acquisition and protection together and separate this empirical gate from the preceding design decision.

## Problem / hypothesis

Successful switching or an approved learning design does not establish persistent useful learning.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Review all acquisition/retention results and the isolation, rollback, and evidence-origin audit.
- Select a supported simple learning/replay configuration or prescribe a bounded revision; record observed scope/consolidation limitations.

## Acceptance criteria

- [ ] Record proceed/revise/stop against the frozen acquisition/retention criteria, including negative seeds and resource trade-offs.
- [ ] Require improvement beyond state-only calibration and the written transition, with retained unrelated instances and useful multistep behavior.
- [ ] State which generic/association/instance memory claims are supported; do not infer learned self-organization.
- [ ] Authorize fixed-capacity organization only on a proceed; keep integration dependent on this empirical outcome.

## Metrics / evidence

Expected report: reports/MULTICIRCUIT_ACQUISITION_GATE.md with exact report/artifact references and outstanding learning failures.

## Dependencies

- [SOAM-040](SOAM-040-multicircuit-acquisition.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
Set decision to proceed, revise, or stop only when the review is complete.
