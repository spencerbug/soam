---
schema_version: 2
id: "SOAM-019"
title: "Build rendered observations and frozen encoder comparisons"
type: "engineering"
status: "ready"
priority: "P2"
recommended_thinking: "medium"
milestone: "M6"
work_packages: ["WP-09"]
hypotheses: ["H6"]
depends_on: ["SOAM-002"]
labels: ["type:engineering", "priority:P2", "milestone:M6"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-019: Build rendered observations and frozen encoder comparisons

## Recommended thinking

**medium** — Integrate controlled rendering and frozen encoder interfaces with explicit provenance and invariant checks.

## Problem / hypothesis

The initial projection operates on fully observable 2D state. Grounding needs an observation interface and rendered inputs before richer sensory claims.

Specification: [research plan §13](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

This remains an eligible supporting branch under the [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md). It is not a prerequisite for the first switching experiment, which uses fixed simple sensing. Better encoders/readouts may improve prediction later but do not substitute for cue-driven switching evidence.

### Bounded work

- Generate controlled shape scenes with known latent dynamics and a fixed encoder interface.
- Compare hand-designed features, random projection, simple pretrained self-supervision, and an appropriate frozen JEPA-style encoder.

## Acceptance criteria

- [ ] Keep simulator hidden state evaluator-only; model input must pass through the selected observation/encoder interface.
- [ ] Version renderer, encoder checkpoint, preprocessing, feature dimensions, and licensing/source provenance.
- [ ] Verify frozen parameters and stable embeddings; calibrate/train the recurrent readout separately.
- [ ] Use small synthetic scenes first and report feature quality, storage, latency, and whether complex encoding improves the controlled task.

## Metrics / evidence

Feature/control sufficiency, grounded prediction, frozen-weight integrity, encoder bytes/time, and data exposure.

## Dependencies

- [SOAM-002](SOAM-002-gate-1.md) — Gate 1: review the substrate before online writing

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.

This branch remains eligible after historical Gate 1; the switching protocol is the default next task. Rich sensing does not block that synthetic experiment.
