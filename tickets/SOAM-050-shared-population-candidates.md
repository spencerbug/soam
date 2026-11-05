---
schema_version: 2
id: "SOAM-050"
title: "Implement the bounded shared-population comparison"
type: "engineering"
status: "backlog"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-00", "WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-048", "SOAM-049"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-050: Implement the bounded shared-population comparison

## Recommended thinking

**high** — Implement exact dynamical rules and fair controls while verifying genuine unit overlap and strict inference ownership.

## Problem / hypothesis

The selected shared-population protocol needs runnable candidates, controls, interventions, and diagnostics before measured comparisons.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Implement only the minimal recall/transition candidates, controls, overlap intervention, and diagnostics frozen in SOAM-049 through the small common runner.
- Verify genuine recurrent unit overlap and no hidden role-specific memories; implement supplied structure/offline fitting exactly as declared.
- Provide finite fixtures for recall, directional transitions, cross-function interference, perturbations, and resource accounting. Concurrent binding, handover, application adapters, and online learning are deferred.

## Acceptance criteria

- [ ] Run the baseline suite before code changes and verify selected equations with small independent numerical cases.
- [ ] Test shared-unit participation, action indexing, target exclusion, no-write inference, state ownership, and reproducibility.
- [ ] Exercise all pilot conditions and failure paths with archived config/source/seeds/software/protocol hashes and resource counts.
- [ ] Preserve historical handover paths; passing fixtures does not select a research fork or establish useful sharing.

## Metrics / evidence

Planned engineering report: reports/SHARED_POPULATION_HARNESS.md. Record precise parameter, neuron, state, buffer, readout, and compute counts. Fixture values are not confirmation results.

## Dependencies

- [SOAM-048](SOAM-048-platform-runner.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-049](SOAM-049-shared-population-protocol.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R1/R2/R3) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Implement, measure, or review E1 against the frozen protocol and review defaults. Report performance utility separately from attraction and from biological/semantic claims. Require matched random/disjoint lesions and a competent GRU; no capacity or information advantage may be relabeled a sharing effect.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Preserve negative
outcomes; this ticket does not authorize other backlog work.
