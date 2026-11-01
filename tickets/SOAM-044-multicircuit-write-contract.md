---
schema_version: 2
id: "SOAM-044"
title: "Implement the selected multi-circuit write contract"
type: "engineering"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-039"]
labels: ["type:engineering", "priority:P1", "milestone:M2"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-044: Implement the selected multi-circuit write contract

## Recommended thinking

**high** — Implement the selected persistent-state ownership and transactional invariants before replay or acquisition trials depend on them.

## Problem / hypothesis

The learning-design decision specifies a contract but does not implement it.
Evidence/replay infrastructure and empirical acquisition need a tested writer first.
Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Implement only the write representation and simple comparison rules selected in the learning protocol, preserving the old single-matrix writer for its historical branch.
- Separate generic parameters, associations, instance facts, and transient state; expose inspectable grounded proposals, bounded commit/discard, and exact rollback.
- Provide deterministic small fixtures for later replay/shadow-validation work. This ticket implements transactions, not performance-based shadow selection or empirical acquisition claims.

## Acceptance criteria

- [ ] Run the existing test suite before code changes and verify evidence provenance, target exclusion, permitted tensors/records, budgets, and deterministic proposal behavior.
- [ ] Test instance isolation, unchanged frozen knowledge, snapshot isolation, stale/tampered rejection, no-write inference, and exact rollback across every persistent object.
- [ ] Exercise each selected rule through the same transaction interface without tuning it on final evaluation data.
- [ ] Record exact tests, smoke configuration/source fingerprints, storage accounting, and limitations; contract correctness does not establish acquisition.

## Metrics / evidence

Expected engineering report: reports/MULTICIRCUIT_WRITE_CONTRACT.md. Include source,
software, configuration, fixture seeds, actual changed objects, and reproducibility.
Measured acquisition belongs to the subsequent experiment.

## Dependencies

- [SOAM-039](SOAM-039-grounded-memory-design.md) — completed design decision with proceed for the selected contract.

## Completion record

Not started. Record actual tests/commands and artifacts. The ticket was allocated
after the other v0.2 tickets to make the implementation dependency explicit; IDs
are stable identifiers, not execution order.
