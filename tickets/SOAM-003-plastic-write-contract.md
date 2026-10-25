---
schema_version: 1
id: "SOAM-003"
title: "Define the grounded local-write contract and plastic parameters"
type: "engineering"
status: "backlog"
priority: "P1"
milestone: "M2"
work_packages: ["WP-02"]
hypotheses: ["H2"]
depends_on: ["SOAM-002"]
labels: ["type:engineering", "priority:P1", "milestone:M2"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-003: Define the grounded local-write contract and plastic parameters

## Problem / hypothesis

Online writing needs an explicit, testable distinction between transient state, frozen ordinary parameters, and designated plastic weights.

Specification: [research plan §5, §9, §17](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Implement one justified plastic weight or fast-adapter formulation behind a common writer interface.
- Define cue/target construction, bounded update proposals, commit/rollback, and grounded-evidence provenance.

## Acceptance criteria

- [ ] Freeze encoder/readout/base parameters as specified by the Gate 1 decision; any exception is documented and ablated.
- [ ] A real transition can produce an inspectable update proposal and atomic application or rollback.
- [ ] Tests show non-designated parameters remain unchanged and imagined rollouts cannot invoke writing.
- [ ] Log update norm/rank, bytes, time, data exposure, and the exact before/after checkpoint identities.

## Metrics / evidence

Write cost, changed-parameter set, update magnitude, immediate and multistep prediction before/after writes.

## Dependencies

- [SOAM-002](SOAM-002-gate-1.md) — Gate 1: review the substrate before online writing

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
