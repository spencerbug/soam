---
schema_version: 2
id: "SOAM-030"
title: "Maintain a focused theory and literature evidence map"
type: "research"
status: "ready"
priority: "P2"
recommended_thinking: "high"
milestone: "MX"
work_packages: []
hypotheses: ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8"]
depends_on: ["SOAM-000"]
labels: ["type:research", "priority:P2", "milestone:MX"]
assignees: []
created: "2026-10-25"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-030: Maintain a focused theory and literature evidence map

## Recommended thinking

**high** — Critically map primary literature to falsifiable SOAM claims, assumptions, and unresolved theoretical questions.

## Problem / hypothesis

The supplied starting bibliography has not been independently reviewed. Theoretical questions should produce testable predictions and baseline choices, not unsupported architectural claims.

Specification: [research plan §20, §21](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.3 shared-population revision — 2026-11-05

Expand the bounded evidence map to symmetric versus asymmetric Hopfield dynamics, sequence/cycle memory, continuous attractors, overlapping assemblies, recurrent attention, NeuroSLAM, and Monty learning modules. Use primary sources and distinguish inspiration from reproduction. Protocol tickets may do their narrower reviews independently.

The [v0.3 scope](../docs/RESEARCH_SPEC_V0_3.md) governs current topology and
platform use; earlier scope notes below retain dependency history only.

### Historical v0.2 scope revision — 2026-11-01

The [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md) adds a bounded early focus on cue-driven switching, simultaneous versus separated attractor populations, shared-parameter independent states, and sensorimotor correction. Review primary sources for selected mechanisms and controls; columns/stacks are hypotheses without an adopted neuroscience equivalence. The protocol ticket may perform the narrower literature review needed for its own design without waiting for this whole map.

### Bounded work

- Verify the six starting references against primary sources and record exact claims, assumptions, and limitations.
- Create a bounded first-pass map of regime capacity, local sensitivity/scope, interference, consolidation symmetries, composition, and planning uncertainty.

## Acceptance criteria

- [ ] For each new experiment family, record the exact update/learning assumptions, state and map representation, failure modes, and one concrete control or falsification test; do not infer general stability from symmetry results.

- [ ] Each source has a verified citation and a concise evidence note distinguishing the paper’s result from SOAM’s hypothesis.
- [ ] Each theoretical area maps to an experiment/ticket, measurable prediction, and falsification condition.
- [ ] Record missing evidence and conflicting results without expanding into an unbounded literature search.
- [ ] Close the initial map with a dated report; create separate bounded follow-ups for ongoing literature maintenance.

## Metrics / evidence

Source coverage and concrete experiment/baseline implications; no new empirical performance claim.

## Dependencies

- [SOAM-000](SOAM-000-substrate-baseline.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Parallel research investigation** (R8) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the focused source map in the review, but keep this broader literature ticket unfinished. Prioritize specific open questions (asymmetry/recovery, fast-memory lifetime, coordinate-dependent overlap, active perception). No exhaustive reading prerequisite before E1 and no new implementation from citations alone.

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
