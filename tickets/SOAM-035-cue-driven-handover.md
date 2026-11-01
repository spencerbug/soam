---
schema_version: 2
id: "SOAM-035"
title: "Measure cue-driven concurrent attractor handover"
type: "experiment"
status: "backlog"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-034"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-035: Measure cue-driven concurrent attractor handover

## Recommended thinking

**xhigh** — Distinguish cue-induced recovery and concurrent calibration from externally forced switching, extra evidence, and resource differences.

## Problem / hypothesis

Test whether pre-calibrated candidates permit useful cue-driven cutover and whether circuit separation is needed under the bounded protocol.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Execute the frozen handover protocol, including repeated switches, misleading cues, perturbations, and sensory-feedback ablations.
- Keep persistent parameters fixed during evaluation; distinguish hand-set basins and offline fitting from learned attractor discovery.
- Report all prescribed shared/separated-state variants, including failed concurrency and any stale-state or source-retention failures.

## Acceptance criteria

- [ ] Publish all seed/condition results for switch latency, false switches, source retention, candidate calibration, recovery/collapse, and short prediction continuity.
- [ ] Compare equal-history cold/reconstruction controls and account for replay latency, cloned weights, state bytes, couplings, total compute, and sensory exposure.
- [ ] Show which effects survive cue/sensory ablations and which are attributable to a scripted scheduler or explicit state copying.
- [ ] Archive configuration/source/software provenance and reproduce the protocol-selected confirmation runs; report negative outcomes without changing frozen thresholds.

## Metrics / evidence

Expected report: reports/ATTRACTOR_HANDOVER.md. Include condition-level artifacts and the preregistered seed/split/resource plan; new test results cannot be reused as unseen tuning data.

## Dependencies

- [SOAM-034](SOAM-034-handover-harness.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
