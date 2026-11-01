---
schema_version: 2
id: "SOAM-034"
title: "Implement the bounded concurrent-attractor handover harness"
type: "engineering"
status: "backlog"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-00", "WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-033"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-034: Implement the bounded concurrent-attractor handover harness

## Recommended thinking

**high** — Implement independent live state, cue pathways, and reproducible controls without encoding the desired result in the scheduler.

## Problem / hypothesis

Existing recurrence and switching baselines do not expose independently calibrated candidates or distinguish a bank swap from cue-driven attraction.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Implement only the topology/candidate matrix selected by the handover protocol; adapt existing baselines without changing historical configurations.
- Expose independent live states, graded cue activity, role/scheduling traces, sensorimotor correction, and persistent-state fingerprints.
- Instrument state copies, resets, parameter tying/cloning, peak concurrency, history replay, and all per-step/model-call costs.

## Acceptance criteria

- [ ] Implement explicit attractor and ordinary recurrent candidates plus the selected population-separation controls.
- [ ] Test candidate-state isolation, repeated role swaps, sensor/action timing, evaluator-only truth, deterministic seeds, and no persistent writes during handover or imagined rollouts.
- [ ] Provide a smoke run for all prescribed controls and an artifact schema recording cues, roles, calibration, handovers, and resource costs; smoke success is not scientific evidence.
- [ ] Run the baseline test suite before code edits, relevant tests afterwards, and ticket validation; record exact outcomes and implementation limitations.

## Metrics / evidence

Engineering report plus smoke config/source fingerprints and reproducibility checks. Full confirmation trials belong to the next experiment, not this harness ticket.

## Dependencies

- [SOAM-033](SOAM-033-handover-protocol.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
