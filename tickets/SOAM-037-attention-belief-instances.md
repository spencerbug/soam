---
schema_version: 2
id: "SOAM-037"
title: "Test dual attention and concurrent instance beliefs"
type: "experiment"
status: "backlog"
priority: "P1"
recommended_thinking: "xhigh"
milestone: "M6"
work_packages: ["WP-10"]
hypotheses: ["H5", "H6"]
depends_on: ["SOAM-036"]
labels: ["type:experiment", "priority:P1", "milestone:M6"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-037: Test dual attention and concurrent instance beliefs

## Recommended thinking

**xhigh** — Separate explanatory competition, attention allocation, and instance binding while preserving independent evidence.

## Problem / hypothesis

Concurrent handover must extend to compatible instances and competing explanations without mixing their states or treating internal cues as observations.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Use the supported synthetic interface with two independently movable sensory/memory focuses and repeated object/part instances.
- Introduce controlled ambiguity, partial observations, misleading cues, and occlusion; retain explicit bindings and scheduling as disclosed scaffolding.
- Compare single-hypothesis, shared-state, independent-state, and cue/compatibility ablations within bounded capacity.

## Acceptance criteria

- [ ] Preregister correspondence, identity-switch, false-commitment, uncertainty, recovery, and computation metrics with held-out instances and fixed seeds.
- [ ] Demonstrate or falsify coexistence of compatible instances and local competition among incompatible explanations; do not claim learned bindings when supplied.
- [ ] Test independently shifted sensory and memory attention and verify that one observation is not counted repeatedly through associative feedback.
- [ ] Publish supported synthetic control conditions or a documented failure/revision; richer encoder claims remain a separate branch.

## Metrics / evidence

Expected report: reports/ATTENTION_BELIEF_INSTANCES.md. Record all supplied roles/bindings, fixed projection identity, data exposure, model/state resources, and negative results.

## Dependencies

- [SOAM-036](SOAM-036-handover-gate.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
