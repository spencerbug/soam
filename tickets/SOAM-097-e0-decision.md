---
schema_version: 2
id: "SOAM-097"
title: "Review E0 navigation and local recovery evidence"
type: "decision"
status: "backlog"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-096"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-21"
updated: "2026-11-21"
github_issue: null
decision: null
---

# SOAM-097: Review E0 navigation and local recovery evidence

## Recommended thinking

**xhigh** — Separate a finite empirical dynamics test from claims of continuous attraction and later module readiness.

## Problem / hypothesis

Can a learned recurrent population preserve and navigate orientation while recovering locally from perturbations? The [owner selection](../docs/requests/e0_2026_11_21.md) activates one narrow test under H1/H6. Earlier studies do not answer this question. Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Review validity, seven joint criteria, paired control comparisons, uncertainty and resources. Accept negative or inconclusive evidence and recommend at most one next experiment without activating it.

Use [E0 v1](../docs/STUDY_E0_PROTOCOL.md) and its [manifest](../docs/protocols/study_e0_v1.json). Classification: **essential next**.

## Acceptance criteria

- [ ] Classify each model using the frozen joint endpoint/precision rules without claiming an exact continuous attractor.
- [ ] Record a scoped proceed/revise/stop evidence decision in reports/STUDY_E0_DECISION.md; preserve earlier gates and later conditional branches.

## Metrics / evidence

Free-64 sensory NMSE; grounded prediction; zero-action pose retention; transverse contraction with pose-preservation guard; tangent retention; correction on returning evidence. NAV32, SYM32, GRU32 and fitted PCA2 controls. Two development roots, ten confirmation roots and one four-model repeat. Frozen ceiling: 3,600 CPU / 7,200 execution-wall seconds, 2 GiB RSS and 1 GiB numerical artifacts. Protocol owns thresholds; reports own measured findings.

## Dependencies

- [SOAM-096](SOAM-096-e0-study.md) — required done; decision prerequisite must be proceed.

## Branch conditions

The November 21 owner selection activates only E0 v1. SOAM-093 proceed accepts inconclusive evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. Coupling, translation, attention, hierarchy, load/encoder sweeps and online acquisition require fresh routing.

## Completion record

Not started.
