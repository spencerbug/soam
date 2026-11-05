---
schema_version: 2
id: "SOAM-037"
title: "Test attention and instance binding in shared populations"
type: "experiment"
status: "backlog"
priority: "P1"
recommended_thinking: "xhigh"
milestone: "M6"
work_packages: ["WP-10"]
hypotheses: ["H5", "H6"]
depends_on: ["SOAM-052", "SOAM-059"]
labels: ["type:experiment", "priority:P1", "milestone:M6"]
assignees: []
created: "2026-11-01"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-037: Test attention and instance binding in shared populations

## Recommended thinking

**xhigh** — Separate explanatory competition, attention allocation, and instance binding while preserving independent evidence.

## Problem / hypothesis

Concurrent handover must extend to compatible instances and competing explanations without mixing their states or treating internal cues as observations.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.3 shared-population revision — 2026-11-05

Use the population and handover conditions supported by SOAM-052. Test feature, relation, and action information with overlapping neurons while keeping concurrent instance bindings and evidence responsibility identifiable. Disjoint banks and shared-weight clones are controls.

The [v0.3 scope](../docs/RESEARCH_SPEC_V0_3.md) governs current topology and
platform use; earlier scope notes below retain dependency history only.

- Use the supported synthetic interface with two independently movable sensory/memory focuses and repeated object/part instances.
- Introduce controlled ambiguity, partial observations, misleading cues, and occlusion; retain explicit bindings and scheduling as disclosed scaffolding.
- Compare single-hypothesis, shared-state, independent-state, and cue/compatibility ablations within bounded capacity.

## Acceptance criteria

- [ ] Report role/instance mixing, overlap participation, stale state, and cross-function interference under causal unit/connection interventions; do not count separate cloned states as shared-neuron evidence.

- [ ] Preregister correspondence, identity-switch, false-commitment, uncertainty, recovery, and computation metrics with held-out instances and fixed seeds.
- [ ] Demonstrate or falsify coexistence of compatible instances and local competition among incompatible explanations; do not claim learned bindings when supplied.
- [ ] Test independently shifted sensory and memory attention and verify that one observation is not counted repeatedly through associative feedback.
- [ ] Publish supported synthetic control conditions or a documented failure/revision; richer encoder claims remain a separate branch.

## Metrics / evidence

Expected report: reports/ATTENTION_BELIEF_INSTANCES.md. Record all supplied roles/bindings, fixed projection identity, data exposure, model/state resources, and negative results.

## Dependencies

- [SOAM-052](SOAM-052-shared-population-gate.md) — required completed prerequisite; decision prerequisites require proceed and the branch conditions below.
- [SOAM-059](SOAM-059-research-fork-selection.md) — required completed prerequisite; decision prerequisites require proceed and the branch conditions below.

## Branch conditions

Start only after SOAM-052 supports useful sharing and SOAM-059 selects the concurrency fork. This is the first concurrent-instance and cue-driven handover extension: preregister source retention, successor calibration, false switches, binding errors, latency, and overlap controls before trials. If concurrent binding/handover fails, retain the single-state result and defer control/skills; select one bounded diagnostic or application alternative in a fresh routing decision. Success supplies only the measured conditions to SOAM-023.

## Scientific review disposition — 2026-11-05

**Future capability** (R5/R9/R10) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Retain as the richer integration/concurrency/control path with existing empirical prerequisites. E3 is a smaller independent supplied-policy test and does not pass this ticket or its gate. No human-like intelligence claim follows from completed components.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
