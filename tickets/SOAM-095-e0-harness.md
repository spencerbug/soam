---
schema_version: 2
id: "SOAM-095"
title: "Implement and verify the E0 navigation harness"
type: "engineering"
status: "in_progress"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-094"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-21"
updated: "2026-11-21"
github_issue: null
decision: null
---

# SOAM-095: Implement and verify the E0 navigation harness

## Recommended thinking

**high** — Verify causal interfaces, deterministic fitting, bounded execution and evaluator-only geometry without changing the frozen design.

## Problem / hypothesis

Can a learned recurrent population preserve and navigate orientation while recovering locally from perturbations? The [owner selection](../docs/requests/e0_2026_11_21.md) activates one narrow test under H1/H6. Earlier studies do not answer this question. Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Implement the frozen four-model pilot, scientific invariant tests, provenance, bounded execution, raw arrays and resource preflight. No unselected mechanism or numerical tuning.

Use [E0 v1](../docs/STUDY_E0_PROTOCOL.md) and its [manifest](../docs/protocols/study_e0_v1.json). Classification: **essential next**.

## Acceptance criteria

- [ ] Verify no-write inference, separate evidence/targets, fresh streams, exact absent-cue behavior, geometry diagnostics and reproducibility.
- [ ] Pass the full tests, ticket checks and finite fixture resource projection before scientific fitting.

## Metrics / evidence

Free-64 sensory NMSE; grounded prediction; zero-action pose retention; transverse contraction with pose-preservation guard; tangent retention; correction on returning evidence. NAV32, SYM32, GRU32 and fitted PCA2 controls. Two development roots, ten confirmation roots and one four-model repeat. Frozen ceiling: 3,600 CPU / 7,200 execution-wall seconds, 2 GiB RSS and 1 GiB numerical artifacts. Protocol owns thresholds; reports own measured findings.

## Dependencies

- [SOAM-094](SOAM-094-e0-protocol.md) — required done; decision prerequisite must be proceed.

## Branch conditions

The November 21 owner selection activates only E0 v1. SOAM-093 proceed accepts inconclusive evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. Coupling, translation, attention, hierarchy, load/encoder sweeps and online acquisition require fresh routing.

## Completion record

Started after SOAM-094 done/proceed. The pre-change suite passed 328 tests. Implementation and resource preflight are pending; no scientific fitting has begun.
