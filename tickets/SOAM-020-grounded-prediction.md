---
schema_version: 2
id: "SOAM-020"
title: "Train recurrent prediction and assimilation on rendered observations"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "high"
milestone: "M6"
work_packages: ["WP-10"]
hypotheses: ["H6"]
depends_on: ["SOAM-019"]
labels: ["type:experiment", "priority:P2", "milestone:M6"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-020: Train recurrent prediction and assimilation on rendered observations

## Recommended thinking

**high** — Calibrate recurrent prediction and assimilation while preventing access to hidden simulator state.

## Problem / hypothesis

A successor hidden state is not the observed sensory embedding. The recurrent predictor needs explicit, calibrated assimilation under the new observation interface.

Specification: [research plan §5, §13](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

Under the [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md), retain this rendered-observation branch while using the selected circuit organization when available. It extends the simple fixed-sensing experiments rather than delaying them. Record whether prediction gains arise from encoding/readout or recurrent dynamics.

### Bounded work

- Train the readout and observation-assimilation mechanism with the encoder frozen.
- Compare free prediction, grounded correction, and a comparable ordinary recurrent baseline.

## Acceptance criteria

- [ ] Demonstrate correction toward observed evidence without passing hidden world state into inference.
- [ ] Separate encoder/readout/assimilation effects with controlled ablations.
- [ ] Report one-step/multistep error, correction latency, and stability across fixed seeds.
- [ ] Save observation, action, context, and outcome provenance for later memory comparisons.

## Metrics / evidence

Grounded/free prediction, recovery after sensory discrepancy, observation cost, and rollout stability.

## Dependencies

- [SOAM-019](SOAM-019-frozen-encoders.md) — Build rendered observations and frozen encoder comparisons

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
