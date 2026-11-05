---
schema_version: 2
id: "SOAM-035"
title: "Measure frozen v1 cue-driven handover controls"
type: "experiment"
status: "ready"
priority: "P2"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-034"]
labels: ["type:experiment", "priority:P2", "milestone:M1"]
assignees: []
created: "2026-11-01"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-035: Measure frozen v1 cue-driven handover controls

## Recommended thinking

**xhigh** — Distinguish cue-induced recovery and concurrent calibration from externally forced switching, extra evidence, and resource differences.

## Problem / hypothesis

Test whether pre-calibrated candidates permit useful cue-driven cutover and whether circuit separation is needed under the bounded protocol.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Use the [frozen protocol](../docs/HANDOVER_PROTOCOL.md),
[implemented harness](../docs/HANDOVER_HARNESS.md), and
[engineering verification](../reports/HANDOVER_HARNESS.md). Fixture scores and
unfitted checkpoints are not measured evidence or trained baselines.
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

The 2026-11-05 [v0.3 revision](../docs/RESEARCH_SPEC_V0_3.md) retains this frozen v1 comparison as P2 supporting work. It remains eligible on its original prerequisites; its models, conditions, seeds, and thresholds are unchanged. It is no longer the default next task. New shared-population evidence belongs to SOAM-049–052.

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

- [SOAM-034](SOAM-034-handover-harness.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
