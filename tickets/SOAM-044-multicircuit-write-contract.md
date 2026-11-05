---
schema_version: 2
id: "SOAM-044"
title: "Implement bounded acquisition candidates and write invariants"
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
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-044: Implement bounded acquisition candidates and write invariants

## Recommended thinking

**high** — Implement the selected persistent-state ownership and transactional invariants before replay or acquisition trials depend on them.

## Problem / hypothesis

The learning-design decision specifies a contract but does not implement it.
Evidence/replay infrastructure and empirical acquisition need a tested writer first.
Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Implement only the E2 representation/rules and comparison learners selected in SOAM-039, reusing existing transaction code where compatible and preserving the historical writer branch.
- Expose auditable grounded updates, memory snapshots, finite budgets and exact rollback; distinguish persistent learned objects, evidence history, and transient activity.
- Provide deterministic fixtures for new-transition exposure, reset-and-recall, retention, and update timing. No general learned-scope, skill, multi-instance, or consolidation subsystem.

## Acceptance criteria

- [ ] Run the baseline suite before code changes; verify grounded targets, stream separation, permitted writes, update/exposure counts, and finite memory.
- [ ] Test no-write inference, target exclusion, reset persistence, unchanged frozen parameters, stale/tampered rejection where transactions are used, and exact rollback.
- [ ] Exercise every selected adaptive/retrieval baseline under the same observation schedule; instrument repeated reads, offline fitting and compute.
- [ ] Reproduce fixtures and archive source/config/seeds/versions/protocol hashes; this establishes engineering correctness only.

## Metrics / evidence

Expected engineering report: reports/SHARED_POPULATION_WRITE_CONTRACT.md. Include source,
software, configuration, fixture seeds, actual changed objects, and reproducibility.
Measured acquisition belongs to the subsequent experiment.

## Dependencies

- [SOAM-039](SOAM-039-grounded-memory-design.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Future capability** (R4) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Not started. Record actual tests/commands and artifacts. The ticket was allocated
after the other v0.2 tickets to make the implementation dependency explicit; IDs
are stable identifiers, not execution order.
