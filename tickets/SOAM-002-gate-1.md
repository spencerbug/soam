---
schema_version: 2
id: "SOAM-002"
title: "Gate 1: review the substrate before online writing"
type: "decision"
status: "ready"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1"]
depends_on: ["SOAM-001"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-002: Gate 1: review the substrate before online writing

## Recommended thinking

**high** — Weigh substrate evidence, residual H1 limitations, and the conditions for proceeding to plasticity.

## Problem / hypothesis

Engineering readiness and scientific confirmation are different. Record a bounded decision about whether this substrate is adequate for local-acquisition experiments.

Specification: [research plan §8, §19, §22](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Review the original report and strengthened controls.
- Choose a documented reference substrate or specify a targeted revision.

## Acceptance criteria

- [ ] Cite configuration/commit-linked evidence for prediction, switching, stability, and budget comparisons.
- [ ] Record decision as proceed, revise, or stop; a proceed decision states the exact claims and residual H1 limitations.
- [ ] Define the designated reference checkpoint, allowed plastic parameter family, and failure conditions for the next study without implementing writes here.
- [ ] Update the priority table; if revision is needed, create linked follow-up tickets and keep dependent implementation unready.

## Metrics / evidence

Review the [SOAM-001 report](../reports/SUBSTRATE_CONTROLS.md), including the additive
seed-23 failure, independent handoff semantics, and GRU perturbation sensitivity.

Decision record against the preregistered criteria, with uncertainty and unresolved reuse questions.

## Dependencies

- [SOAM-001](SOAM-001-substrate-controls.md) — Strengthen substrate controls and budget comparisons

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
Set frontmatter `decision` to `proceed`, `revise`, or `stop` only when the decision is documented.
