---
schema_version: 2
id: "SOAM-050"
title: "Implement the bounded shared-population comparison"
type: "engineering"
status: "done"
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

- Implement [E1 v1](../docs/SHARED_POPULATION_PROTOCOL.md) and its [frozen manifest](../docs/protocols/shared_population_v1.json), including seven fitted families and the no-fit T32 tied-state diagnostic. Verify exact intact equivalence and independent-bank lesion behavior; E1 does not isolate a performance benefit of neuron overlap from parameter tying.
- Implement only the minimal recall/transition candidates, controls, overlap intervention, and diagnostics frozen in SOAM-049 through the small common runner.
- Verify genuine recurrent unit overlap and no hidden role-specific memories; implement supplied structure/offline fitting exactly as declared.
- Provide finite fixtures for recall, directional transitions, cross-function interference, perturbations, and resource accounting. Concurrent binding, handover, application adapters, and online learning are deferred.

Record the full-inventory, 2×-margin timing/storage feasibility check before SOAM-051
fitting. Failure requires a new protocol decision/version, not silent trial reduction.

## Acceptance criteria

- [x] Run the baseline suite before code changes and verify selected equations with small independent numerical cases.
- [x] Test shared-unit participation, action indexing, target exclusion, no-write inference, state ownership, and reproducibility.
- [x] Exercise all pilot conditions and failure paths with archived config/source/seeds/software/protocol hashes and resource counts.
- [x] Preserve historical handover paths; passing fixtures does not select a research fork or establish useful sharing.

## Metrics / evidence

Engineering report: [SHARED_POPULATION_HARNESS.md](../reports/SHARED_POPULATION_HARNESS.md).
The full-inventory storage projection failed; other resource projections passed.
Fixture values are not confirmation results. SOAM-061 owns the corrective decision.

## Dependencies

- [SOAM-048](SOAM-048-platform-runner.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-049](SOAM-049-shared-population-protocol.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R1/R2/R3) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Implement, measure, or review E1 against the frozen protocol and review defaults. Report performance utility separately from attraction and from biological/semantic claims. Require matched random/disjoint lesions and a competent GRU; no capacity or information advantage may be relabeled a sharing effect.

## Completion record

Started 2026-11-05. Verified SOAM-048 done and SOAM-049 done/proceed; E1 v1 governs
implementation. Baseline: 110 tests passed in 14.55s before code changes. No assignee
handle is known. Scientific fitting and measured trials remain SOAM-051.

Completed 2026-11-05. Follow-on baseline: 144 tests passed in 14.67s before further
code changes. Delivered task streams, packed candidates/T32, observed-only Adam/ridge
mechanics, interventions, paired-root inference rules, artifact replay and preflight.
Final `UV_CACHE_DIR=/tmp/soam-uv-cache uv run pytest`: **171 passed in 16.24s**;
targeted Ruff check/format passed. The engineering command
`uv run python -m soam.shared.runner --output runs/shared-harness-v1-final` exercised
181 cells per execution, exactly replayed 1,560 arrays, and recorded two expected
nonfinite failures. Fourteen tiny fixture fits use isolated streams, two stages of
one update each and batch two; they are not the SOAM-051 fitting schedule.

`uv run python -m soam.shared.runner --mode preflight --output runs/shared-preflight-v1`
performed no optimizer updates. The 119-fit/27,820-cell projection failed the artifact
ceiling: 12,680,048,016 projected bytes with 2× margin versus 8,589,934,592 allowed.
Other checks passed. The [report and compact evidence](../reports/SHARED_POPULATION_HARNESS.md)
record source/config/seeds/software, exact timings, resource counts and limitations.
This completes the engineering ticket with a negative feasibility result, not study
readiness. [SOAM-061](SOAM-061-e1-artifact-feasibility.md) must resolve it under a fresh
versioned decision; SOAM-051 remains backlog. No scientific fits or confirmation data ran.
