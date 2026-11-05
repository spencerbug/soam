---
schema_version: 2
id: "SOAM-056"
title: "Specify a Monty-style recurrent learning-module study"
type: "decision"
status: "backlog"
priority: "P1"
recommended_thinking: "xhigh"
milestone: "M6"
work_packages: ["WP-02", "WP-08", "WP-10"]
hypotheses: ["H2", "H5", "H6"]
depends_on: ["SOAM-047", "SOAM-059", "SOAM-041"]
labels: ["type:decision", "priority:P1", "milestone:M6"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-056: Specify a Monty-style recurrent learning-module study

## Recommended thinking

**xhigh** — Separate learning-module responsibilities from graph storage and test whether shared recurrent memory can acquire sensorimotor structure without hidden explicit models.

## Problem / hypothesis

Explore a Monty-style learning module whose core learned feature/location/relationship memory is recurrent dynamics instead of point clouds or graphs. This is an experimental analogue, not an existing drop-in integration.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Review and pin official Monty learning-module documentation/source. Define one small object/pose recognition task using local fixed features, relative movement, and declared reference frames.
- Specify shared-population feature/location/relation/action dynamics, observed-data acquisition, recognition, evidence/uncertainty, and next-observation prediction. Include held-out poses, ambiguous features, repeated instances, revisits, and limited withheld combinations.
- Compare with a small explicit point-cloud/graph memory, ordinary recurrent learner, frozen/no-learning candidate, and separated-function control under matched exposure and reported total resources.
- Define an independently bounded learning contract with writable objects, grounded targets, validation/rollback, offline versus online exposure, train/dev/test object/trajectory splits, and no-write inference. Reuse platform transactions; do not wait for or claim completion of the later integrated SOAM writer.
- Keep geometry in environment/evaluator and labeled controls. Exclude hidden per-object graphs/tables from the recurrent candidate; count supplied object IDs, reference frames, readouts, caches, and any evidence buffer.

## Acceptance criteria

- [ ] Publish concrete task/input/output/state/learning interfaces, source comparison, numerical criteria, and a finite experiment manifest before implementation.
- [ ] Define acquisition sample efficiency, recognition/pose error, uncertainty/false matches, re-identification, next-feature prediction, interference, and held-out transfer metrics.
- [ ] Test directional/action dependence and shared-neuron participation causally; distinguish recognition, associative recall, and learned compositional structure.
- [ ] Record proceed/revise/stop with graph/control boundaries and failure acceptance. Defer full Monty API integration, multi-module voting, rich sensing, and robotics to separate tasks.

## Metrics / evidence

Planned protocol: docs/RECURRENT_LEARNING_MODULE_PROTOCOL.md. Start from [official Monty learning modules](https://docs.thousandbrains.org/docs/learning-modules); verify exact source revision and baseline behavior during protocol work. No compatibility or neuroscience equivalence is presumed.

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — required completed prerequisite; decision prerequisites require proceed and applicable body conditions.
- [SOAM-059](SOAM-059-research-fork-selection.md) — required completed prerequisite; decision prerequisites require proceed and applicable body conditions.
- [SOAM-041](SOAM-041-multicircuit-acquisition-gate.md) — required completed prerequisite; decision prerequisites require proceed and applicable body conditions.

## Branch conditions

Start only when SOAM-059 explicitly selects this learning-module protocol as the next experiment. Mere dependency completion is insufficient. It may be selected after a negative sharing result to test a labeled conventional/separated reference or a new hypothesis; state that distinction. Freeze one primary application endpoint and numerical go/no-go criteria. Do not implement both application branches by default.

## Scientific review disposition — 2026-11-05

**Future capability** (R9/R10) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Defer the larger Monty-style recurrent learning-module replacement until narrow E2 acquisition is supported and the fork is explicitly selected. Reuse E2 memory where justified; do not duplicate its acquisition harness or silently infer object/pose generalization. Preserve graph/point-cloud controls and the original module question.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Set decision to proceed,
revise, or stop only after completing the review.
