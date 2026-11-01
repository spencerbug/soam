---
schema_version: 2
id: "SOAM-021"
title: "Evaluate partial observations, ambiguity, and context recovery"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "xhigh"
milestone: "M6"
work_packages: ["WP-10"]
hypotheses: ["H6"]
depends_on: ["SOAM-020", "SOAM-036"]
labels: ["type:experiment", "priority:P2", "milestone:M6"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-021: Evaluate partial observations, ambiguity, and context recovery

## Recommended thinking

**xhigh** — Design ambiguous observations and recovery tests that distinguish uncertainty maintenance from premature collapse.

## Problem / hypothesis

Occluded or ambiguous observations require retaining useful uncertainty and recovering when evidence returns. Known-context full-observation tests cannot establish H6.

Specification: [research plan §13, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

The [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md) removes learned consolidation as a prerequisite and adds the empirical handover gate. SOAM-037 tests basic belief/instance behavior earlier with synthetic observations; this ticket tests richer rendered/noisy/ambiguous sensing. Compare only validated available memory mechanisms.

### Bounded work

- Introduce noise, missing frames, occlusion, and observations compatible with multiple latent states.
- Compare the available SOAM memory mechanisms with matched ordinary recurrence, including unknown/ambiguous context cases.

## Acceptance criteria

- [ ] Define observation/model uncertainty metrics and a competing-hypothesis or other justified belief representation before evaluation.
- [ ] Measure recovery after informative observations return, including false commitment and re-localization/context errors.
- [ ] Ablate encoder, assimilation, writer/scope, replay, and consolidation where present.
- [ ] Use held-out sensory/task conditions and disclose the selected handover/belief mechanisms and any validated learning mechanisms. Learned consolidation is not required.

## Metrics / evidence

Belief/context recovery, ambiguity calibration, false commitment, prediction through occlusion, and recovery latency.

## Dependencies

- [SOAM-020](SOAM-020-grounded-prediction.md) — required completed prerequisite; decision prerequisites require proceed.
- [SOAM-036](SOAM-036-handover-gate.md) — required completed prerequisite; decision prerequisites require proceed.

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
