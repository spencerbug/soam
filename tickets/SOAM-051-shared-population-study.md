---
schema_version: 2
id: "SOAM-051"
title: "Measure the benefit and interference of shared recurrence"
type: "experiment"
status: "backlog"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01", "WP-08"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-050"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-051: Measure the benefit and interference of shared recurrence

## Recommended thinking

**xhigh** — Distinguish shared neuronal computation from state multiplexing, overpowered decoders, and resource-dependent performance.

## Problem / hypothesis

Test whether the frozen shared-population candidates retain useful feature, relation, and action information through cue-driven transitions without destructive mixing.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Run only the frozen minimal recall/transition pilot and finite tuning/confirmation budget.
- Evaluate the single primary benefit endpoint, feature-retention/interference guardrails, causal overlap, and action/symmetry ablations against separated and ordinary recurrent controls.
- Classify results using the prespecified outcome rules, keeping all seeds and budget mismatches. No online acquisition or concurrent handover extension in this ticket.

## Acceptance criteria

- [ ] Publish the primary effect and uncertainty, guardrail outcomes, seed-level failures, all controls, and causal-overlap evidence.
- [ ] Distinguish no meaningful advantage from inadequate precision, and directional failure from recall failure or numerical invalidity.
- [ ] Archive complete source/config/seeds/software/numerical settings, exposure, scaffolds, timing/storage/compute, checkpoints and confirmation reproduction.
- [ ] Preserve negative outcomes without adapting the experiment to them; send complete evidence to the sharing gate and fork-selection decision. No experimental fork is automatically launched.

## Metrics / evidence

Planned report: reports/SHARED_POPULATION_STUDY.md. Use only frozen protocol seeds, splits, thresholds, and budgets. Report fixed-point/cycle recovery separately from forced tracking and ordinary prediction.

## Dependencies

- [SOAM-050](SOAM-050-shared-population-candidates.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R1/R2/R3) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Implement, measure, or review E1 against the frozen protocol and review defaults. Report performance utility separately from attraction and from biological/semantic claims. Require matched random/disjoint lesions and a competent GRU; no capacity or information advantage may be relabeled a sharing effect.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Preserve negative
outcomes; this ticket does not authorize other backlog work.
