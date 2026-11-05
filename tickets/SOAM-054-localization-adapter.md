---
schema_version: 2
id: "SOAM-054"
title: "Implement the active-disambiguation task and controls"
type: "engineering"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M6"
work_packages: ["WP-00", "WP-10"]
hypotheses: ["H1", "H6", "H7"]
depends_on: ["SOAM-048", "SOAM-053"]
labels: ["type:engineering", "priority:P1", "milestone:M6"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-054: Implement the active-disambiguation task and controls

## Recommended thinking

**high** — Enforce observation-only localization and consistent control budgets in a reusable task adapter.

## Problem / hypothesis

The approved localization study needs a small reproducible environment/adapter, selected models, and evaluator diagnostics.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Implement the selected 2D environment, permitted observation/self-motion packets, recurrent candidate, controls, and task-specific metrics through the platform.
- Provide fixtures for drift, ambiguous views, revisits, missing sensing, and false loop correction; keep true pose and loop labels inaccessible to learners.
- Implement only the learning policy selected by the protocol, including snapshot/commit/rollback invariants if grounded writes are used.

## Acceptance criteria

- [ ] Run the baseline suite before code edits; test observation/target separation, no-write prediction, random-stream isolation, and update timing.
- [ ] Run every fixture/control including negative cases, verify no hidden candidate graph/table inference, and account for all auxiliary state and supplied mappings.
- [ ] Reproduce fixtures exactly and publish config/source/seed/version/protocol identities and actual tests; no measured localization claim follows from fixtures.

## Metrics / evidence

Planned engineering report: reports/RECURRENT_LOCALIZATION_HARNESS.md. Preserve historical experiment entry points and use the common runner/artifact schema.

## Dependencies

- [SOAM-048](SOAM-048-platform-runner.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-053](SOAM-053-localization-protocol.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Branch conditions

Require the corresponding application protocol proceed and its explicit selection in the fork record. Implement only its bounded candidate set. All other application adapters remain deferred.

## Scientific review disposition — 2026-11-05

**Future capability** (R5) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Implement only E3. Test learner access to observation history, confidence output, supplied-policy inputs, action timing, no-information cases, and no-write rollouts. Include model-by-policy controls and capped failures; full mapping and online E2 integration are deferred.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Preserve negative
outcomes; this ticket does not authorize other backlog work.
