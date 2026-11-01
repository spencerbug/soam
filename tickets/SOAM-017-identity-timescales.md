---
schema_version: 2
id: "SOAM-017"
title: "Test identity preservation and reusable temporal structure"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "high"
milestone: "M5"
work_packages: ["WP-08"]
hypotheses: ["H5"]
depends_on: ["SOAM-016"]
labels: ["type:experiment", "priority:P2", "milestone:M5"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-017: Test identity preservation and reusable temporal structure

## Recommended thinking

**high** — Isolate identity preservation and temporal reuse from memorization and simple dynamical persistence.

## Problem / hypothesis

Reusable transformations should coexist with object identity and distinct temporal scales rather than erasing them.

Specification: [research plan §12](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

Under the [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md), include repeated instances using shared circuit parameters with independent states, and distinguish supplied bindings from learned identity preservation. Test continuity across cue-driven handover and temporal skill phases without requiring a fixed world graph or hierarchy.

### Bounded work

- Build multiple objects sharing dynamics but carrying stable identity features.
- Introduce fast oscillations inside slower trajectories and changing activity contexts without hard-coding a hierarchy.

## Acceptance criteria

- [ ] Keep object-identity and temporal-composition evaluation splits separate from training.
- [ ] Measure identity retention/re-identification alongside transformation transfer and prediction.
- [ ] Compare implicit dynamics with a simple explicitly structured baseline labeled as such, if needed.
- [ ] Publish evidence distinguishing reusable timescale structure from fitting observed sequence patterns.

## Metrics / evidence

Identity errors, held-out transformation transfer, prediction by timescale/horizon, and forgetting after context changes.

## Dependencies

- [SOAM-016](SOAM-016-composition-transfer.md) — Benchmark withheld compositions and transfer to related tasks

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
