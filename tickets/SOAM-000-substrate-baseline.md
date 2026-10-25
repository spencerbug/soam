---
schema_version: 1
id: "SOAM-000"
title: "Record the reproducible substrate baseline"
type: "engineering"
status: "done"
priority: "P0"
milestone: "M0"
work_packages: ["WP-00", "WP-01"]
hypotheses: ["H1"]
depends_on: []
labels: ["type:engineering", "priority:P0", "milestone:M0"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-000: Record the reproducible substrate baseline

## Problem / hypothesis

The initial infrastructure and substrate sprint are implemented. Preserve the measured starting point without treating implementation completion as confirmation of H1.

Specification: [research plan §7, §8, §22](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Archive the four-model, three-seed benchmark and seed-11 exact reproduction.
- Record the current limitations: partial independence of separate cores, unequal variant budgets, known contexts, and long-horizon drift.

## Acceptance criteria

- [x] Deterministic generator, runner, frozen projection, four recurrent variants, switching, and perturbation diagnostics are available.
- [x] Fifteen tests pass; all twelve model/seed runs pass the recorded engineering readiness screen.
- [x] All four full-length seed-11 repeats match numerical metrics, checkpoint weights, and saved trajectories.
- [x] The report distinguishes substrate readiness from reuse, continual learning, and self-organization.

## Metrics / evidence

Existing NMSE, perturbation, stability, parameter/compute, provenance, and reproduction records.

## Dependencies

None.

## Completion record

Completed evidence: [baseline report](../reports/BASELINE.md), [readiness checks](../reports/substrate/readiness.json), [reproduction](../reports/substrate/reproducibility.json). Benchmark source commit: `e861742bd3c2393d7870461771e55bb5f9cd3199`. This closes the initial sprint, not the broader H1 research question.
