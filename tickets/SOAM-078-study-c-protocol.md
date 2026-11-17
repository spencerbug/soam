---
schema_version: 2
id: "SOAM-078"
title: "Specify hypothesis preservation under genuine ambiguity"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-077"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-14"
updated: "2026-11-14"
github_issue: null
decision: "proceed"
---

# SOAM-078: Specify hypothesis preservation under genuine ambiguity

## Recommended thinking

**xhigh** — Separate observability, retained state capacity, estimator competence and resource costs in the bounded C-H1 comparison.

## Problem / hypothesis

Does retaining two candidate states improve calibrated delayed inference beyond competent single-state controls? C-H1 operationalizes H1/H6; C-H2 scheduling and C-H3 learned allocation are separate, conditional questions.

## Scope

Follow the [owner request](../docs/requests/study_c_2026_11_14.md) and [C v1 protocol](../docs/STUDY_C_PROTOCOL.md). Only the first two-explanation experiment is selected. Preserve historical E1/A/B/B2 decisions.

## Acceptance criteria

- [x] Deliver this phase with reproducible evidence or an explicit negative, inconclusive or invalid outcome.
- [x] Enforce evidence parity, full-history ambiguity, pre-correction scoring and no-write inference.
- [x] Account for all mandatory neural/conventional controls, capacity, uncertainty and resources.
- [x] Record actual checks, provenance and the effect on subsequent eligibility.

## Metrics / evidence

Primary binary Brier score, paired independent-root intervals, ambiguity/accuracy/recovery guards, state and parameter counts, mean/p95 latency. The protocol owns the frozen contract and numerical manifest.

## Dependencies

- [SOAM-077](SOAM-077-study-b2-decision.md) — completed prerequisite; decisions require proceed.

## Branch conditions

The November 14 owner request and SOAM-078 select C-H1 only. SOAM-077's baseline recommendation is satisfied; SOAM-078 must accept the contract before implementation. SOAM-079 must verify invariants and feasibility before development/confirmation. SOAM-037 remains backlog under the failed SOAM-052 sharing gate. SOAM-053 is conceptual context only. Completing C-H1 does not select scheduling, acquisition, attention, object memory or another branch.

## Completion record

Protocol and observability/RFC review completed; **proceed** for C-H1 only. The [numerical manifest](../docs/protocols/study_c_v1.json) fixes comparisons, guards, roots and finite resources before fitting. Analytic full-history equivalence, candidate knowledge, distributional single-state controls, prior scoring and future branch boundaries were reviewed. Baseline before Study C code changes: `UV_CACHE_DIR=/private/tmp/soam-uv-cache uv run pytest` — 266 passed in 31.03s. Historical B2 committed as `a552034`; lint, 78-ticket validation and frozen-source/artifact hash checks passed. The local Qwen worker returned `Transport closed`; primary-agent review proceeds directly. At protocol approval, no Study C scientific fit had run.
