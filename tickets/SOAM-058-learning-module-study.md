---
schema_version: 2
id: "SOAM-058"
title: "Measure recurrent learning-module acquisition and recognition"
type: "experiment"
status: "backlog"
priority: "P1"
recommended_thinking: "xhigh"
milestone: "M6"
work_packages: ["WP-02", "WP-08", "WP-10"]
hypotheses: ["H2", "H5", "H6"]
depends_on: ["SOAM-057"]
labels: ["type:experiment", "priority:P1", "milestone:M6"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-058: Measure recurrent learning-module acquisition and recognition

## Recommended thinking

**xhigh** — Distinguish acquired sensorimotor structure and useful sharing from supplied labels, memorized trajectories, and extra memory.

## Problem / hypothesis

Test whether recurrent memory can learn and use the frozen feature/location task against explicit structural-memory and recurrent controls.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Run all fixed seeds, acquisition budgets, held-out objects/poses/trajectories/combinations, and ambiguity/revisit conditions specified by the protocol.
- Measure recognition, pose, acquisition efficiency, next-feature prediction, uncertainty, retention, and causal overlap/action ablations with complete resource accounting.
- Keep learned storage separate from evidence buffers and transient activity; freeze persistent parameters during inference and prediction evaluation.

## Acceptance criteria

- [ ] Publish complete condition/seed results, failed learning cases, uncertainty, and resource trade-offs against graph/point-cloud, no-learning, separated, and ordinary recurrent references.
- [ ] Archive source/config/seed/software/numerical settings, data exposure, scaffolds, learned memory/checkpoints, timing/compute, and confirmation reproduction.
- [ ] Distinguish memory acquisition, recognition, re-identification, and held-out compositional transfer; acceptable negative results do not require expanding capacity or changing thresholds.
- [ ] Record a bounded follow-up recommendation. Do not claim full Monty replacement, general object learning, neuroscience validation, or pass the integrated H2/H5/H6 gates from this task alone.

## Metrics / evidence

Planned report: reports/RECURRENT_LEARNING_MODULE.md. Respect the frozen protocol and distinguish graph-free candidate results from explicitly structured controls.

## Dependencies

- [SOAM-057](SOAM-057-learning-module-adapter.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Branch conditions

On a reproducible primary-endpoint gain, propose one bounded generalization task or integration review; do not auto-expand. On isolated drift/aliasing or acquisition/binding failure, propose one diagnostic with frozen budget and new data. On no advantage, prefer the simpler reference or stop this mechanism. On invalid/inconclusive evidence, repair or obtain the prespecified additional evidence before scientific claims. Record the outcome, selected/deferred alternatives, and fresh decision/protocol needed for further trials; this experiment does not grant its own continuation approval.

## Scientific review disposition — 2026-11-05

**Future capability** (R9/R10) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Future Monty-style extension after SOAM-056 and its acquisition/selection prerequisites; reuse validated smaller experiments. Do not implement a parallel acquisition stack or count this as an immediate-next task.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Preserve negative
outcomes; this ticket does not authorize other backlog work.
