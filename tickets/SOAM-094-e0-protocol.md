---
schema_version: 2
id: "SOAM-094"
title: "Select and freeze the single-population E0 pilot"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-093"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-21"
updated: "2026-11-21"
github_issue: null
decision: "proceed"
---

# SOAM-094: Select and freeze the single-population E0 pilot

## Recommended thinking

**xhigh** — Separate a finite empirical dynamics test from claims of continuous attraction and later module readiness.

## Problem / hypothesis

Can a learned recurrent population preserve and navigate orientation while recovering locally from perturbations? The [owner selection](../docs/requests/e0_2026_11_21.md) activates one narrow test under H1/H6. Earlier studies do not answer this question. Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Freeze the single-population task, model equations, independent streams, endpoint family, precision rules and finite budget. Review information parity and preserve earlier gates.

Use [E0 v1](../docs/STUDY_E0_PROTOCOL.md) and its [manifest](../docs/protocols/study_e0_v1.json). Classification: **essential next**.

## Acceptance criteria

- [x] Record the owner selection and protocol/manifest with supplied versus learned structure explicit.
- [x] Review causality, baseline competence, precision, compute limits and historical gate preservation before implementation.

## Metrics / evidence

Free-64 sensory NMSE; grounded prediction; zero-action pose retention; transverse contraction with pose-preservation guard; tangent retention; correction on returning evidence. NAV32, SYM32, GRU32 and fitted PCA2 controls. Two development roots, ten confirmation roots and one four-model repeat. Frozen ceiling: 3,600 CPU / 7,200 execution-wall seconds, 2 GiB RSS and 1 GiB numerical artifacts. Protocol owns thresholds; reports own measured findings.

## Dependencies

- [SOAM-093](SOAM-093-retrieval-decoding-decision.md) — required done; decision prerequisite must be proceed.

## Branch conditions

The November 21 owner selection activates only E0 v1. SOAM-093 proceed accepts inconclusive evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. Coupling, translation, attention, hierarchy, load/encoder sweeps and online acquisition require fresh routing.

## Completion record

**Proceed with the bounded E0 v1 contract only.** Manual review confirms fresh owner routing, SOAM-093 done/proceed for evidence acceptance, and no dependence on a passed historical E1 gate. The equations distinguish supplied symmetry/skew structure from learned representation. The primary is absolute feasibility with local geometry and correction guards; prediction alone cannot pass. The conventional baseline has equal sensory targets but explicit structural priors; parameter/state mismatches are reported. Ten independent roots, 28 adjusted intervals, fixed widths, 58 scientific fits and a 3,600 CPU-second ceiling are frozen before fitting. Resource preflight remains required before trials. Pre-change `uv run pytest`: 328 passed in 19.04s. Local worker audit timed out; primary verified the reusable helpers directly. No scientific result is claimed.
