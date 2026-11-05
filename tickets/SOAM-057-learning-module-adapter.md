---
schema_version: 2
id: "SOAM-057"
title: "Implement the recurrent learning-module task and controls"
type: "engineering"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M6"
work_packages: ["WP-00", "WP-02", "WP-10"]
hypotheses: ["H2", "H5", "H6"]
depends_on: ["SOAM-048", "SOAM-056"]
labels: ["type:engineering", "priority:P1", "milestone:M6"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-057: Implement the recurrent learning-module task and controls

## Recommended thinking

**high** — Build grounded acquisition and recognition fixtures with explicit memory accounting and protected inference.

## Problem / hypothesis

The approved small learning-module study needs an environment/task adapter, recurrent memory candidate, baseline stores, and invariant-tested acquisition.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Implement only the selected task, recurrent candidate, graph/point-cloud and other controls, and bounded learning policy through the platform.
- Provide fixtures for acquisition, feature ambiguity, relative movements/reference frames, repeated instances, pose changes, and negative recognition.
- Keep simulator geometry and object/pose labels out of candidate inference unless explicitly permitted as training-only scaffolding; log that exposure and isolate oracle controls.

## Acceptance criteria

- [ ] Run baseline tests before code edits; verify grounded target provenance, train/dev/test separation, persistent-write permissions, exact rollback, and snapshot/no-write inference.
- [ ] Verify graph/point-cloud memory is confined to labeled controls and environment/evaluator geometry; enumerate every persistent object and active-state allocation.
- [ ] Exercise all candidates and failure cases with deterministic fixtures and exact reproduction; archive source/config/seeds/protocol/software and actual commands.
- [ ] Document task and backend registration using existing platform interfaces; fixture success does not establish learning, composition, or Monty compatibility.

## Metrics / evidence

Planned engineering report: reports/RECURRENT_LEARNING_MODULE_HARNESS.md. Include transaction tests even if the later integrated writer ticket remains unfinished.

## Dependencies

- [SOAM-048](SOAM-048-platform-runner.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-056](SOAM-056-learning-module-protocol.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Branch conditions

Require the corresponding application protocol proceed and its explicit selection in the fork record. Implement only its bounded candidate set. All other application adapters remain deferred.

## Scientific review disposition — 2026-11-05

**Future capability** (R9/R10) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Future Monty-style extension after SOAM-056 and its acquisition/selection prerequisites; reuse validated smaller experiments. Do not implement a parallel acquisition stack or count this as an immediate-next task.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Preserve negative
outcomes; this ticket does not authorize other backlog work.
