---
schema_version: 2
id: "SOAM-096"
title: "Execute the bounded E0 navigation pilot"
type: "experiment"
status: "backlog"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-094", "SOAM-095"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-21"
updated: "2026-11-21"
github_issue: null
decision: null
---

# SOAM-096: Execute the bounded E0 navigation pilot

## Recommended thinking

**high** — Verify causal interfaces, deterministic fitting, bounded execution and evaluator-only geometry without changing the frozen design.

## Problem / hypothesis

Can a learned recurrent population preserve and navigate orientation while recovering locally from perturbations? The [owner selection](../docs/requests/e0_2026_11_21.md) activates one narrow test under H1/H6. Earlier studies do not answer this question. Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Run only the frozen development selection, ten-root confirmation and prescribed exact repeat after the harness preflight passes. Preserve every failure and stop at the declared ceiling.

Use [E0 v1](../docs/STUDY_E0_PROTOCOL.md) and its [manifest](../docs/protocols/study_e0_v1.json). Classification: **essential next**.

## Acceptance criteria

- [ ] Reconcile all 58 prescribed scientific fits or document a stopped/invalid partial inventory.
- [ ] Archive configuration/source/seeds, raw metrics, checkpoints, resources, uncertainty and exact repeat checks in reports/STUDY_E0.md.

## Metrics / evidence

Free-64 sensory NMSE; grounded prediction; zero-action pose retention; transverse contraction with pose-preservation guard; tangent retention; correction on returning evidence. NAV32, SYM32, GRU32 and fitted PCA2 controls. Two development roots, ten confirmation roots and one four-model repeat. Frozen ceiling: 3,600 CPU / 7,200 execution-wall seconds, 2 GiB RSS and 1 GiB numerical artifacts. Protocol owns thresholds; reports own measured findings.

## Dependencies

- [SOAM-094](SOAM-094-e0-protocol.md) — required done; decision prerequisite must be proceed.
- [SOAM-095](SOAM-095-e0-harness.md) — required done; decision prerequisite must be proceed.

## Branch conditions

The November 21 owner selection activates only E0 v1. SOAM-093 proceed accepts inconclusive evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. Coupling, translation, attention, hierarchy, load/encoder sweeps and online acquisition require fresh routing.

## Completion record

Not started.
