---
schema_version: 2
id: "SOAM-012"
title: "Validate consolidation candidates with shadow weights and rollback"
type: "engineering"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M4"
work_packages: ["WP-06", "WP-07"]
hypotheses: ["H4"]
depends_on: ["SOAM-011"]
labels: ["type:engineering", "priority:P1", "milestone:M4"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-012: Validate consolidation candidates with shadow weights and rollback

## Recommended thinking

**high** — Design grounded acceptance and rollback rules that preserve evidence separation and parameter integrity.

## Problem / hypothesis

A locally useful consolidation update can damage protected behavior. Candidate parameters must be evaluated before they become persistent memory.

Specification: [research plan §5, §11, §17](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Create a shadow-weight transaction with grounded, retention, rollout, context-switch, and stability checks.
- Define evidence-aware trust limits and atomic commit/reject/rollback.

## Acceptance criteria

- [ ] A rejected candidate leaves persistent parameters bit-identical; accepted changes have reproducible evidence and provenance.
- [ ] Repeated proposal selection uses a validation subset, while final reporting uses untouched tests.
- [ ] Deliberately disruptive updates are detected and rollback is verified.
- [ ] Document tolerances before trials and report validation computation and selection bias risks.

## Metrics / evidence

Acceptance/rejection rate, old/new error changes, rollback integrity, validation exposure, and wall time.

## Dependencies

- [SOAM-011](SOAM-011-evidence-and-replay.md) — Implement a bounded grounded evidence buffer and replay baseline

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
