---
schema_version: 2
id: "SOAM-048"
title: "Implement the reusable recurrent-dynamics experiment runner"
type: "engineering"
status: "backlog"
priority: "P0"
recommended_thinking: "high"
milestone: "M0"
work_packages: ["WP-00"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-047"]
labels: ["type:engineering", "priority:P0", "milestone:M0"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-048: Implement the reusable recurrent-dynamics experiment runner

## Recommended thinking

**high** — Implement reproducibility and ownership contracts across distinct task/backend combinations while protecting existing experiment paths.

## Problem / hypothesis

A reusable runner should execute multiple recurrent experiments without copying orchestration or forcing them into the handover-specific model.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Implement only the core interfaces and minimal backends/fixtures selected by the platform contract, with configuration-driven task/backend/learning-policy selection.
- Provide deterministic fixtures for recall/transition and one distinct sensorimotor task; reuse existing provenance, snapshot, metrics, and artifact utilities where compatible.
- Implement finite sweep execution, structured failed-run records, resume/overwrite rules, state/parameter/storage/compute accounting, and capability checks. Preserve historical CLIs, protocols, and results.

## Acceptance criteria

- [ ] Run uv run pytest before existing code changes; pass relevant invariant tests and the full suite after implementation.
- [ ] Execute both fixture tasks through the same runner with at least two compatible backend configurations; demonstrate a small new task/backend registration without editing runner control flow.
- [ ] Verify separate random streams, no target leakage, no persistent or live-state writes during prediction, snapshot isolation, and exact same-environment reproduction excluding timing.
- [ ] Archive fixture configs, seeds, source/version fingerprints, resource counts, actual commands, failure-path checks, and extension documentation; fixtures do not count as research evidence.

## Metrics / evidence

Planned engineering report: reports/RECURRENT_PLATFORM.md. Use a small fixed fixture matrix, record active-state bytes and persistent storage separately, and regression-check the existing handover contract.

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Branch conditions

The first delivery serves only the minimal SOAM-049 recall/transition pilot. Specify extension boundaries but implement no general backend catalogue. A second tiny task fixture checks reuse only; it is not a localization or learning-module study. Expand infrastructure only when a selected fork identifies a concrete missing capability.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R7) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Keep only the runner utilities required by E1 and preserve existing commands. A tiny second fixture may check an actual interface coupling; it must not become a second environment or research study.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Preserve negative
outcomes; this ticket does not authorize other backlog work.
