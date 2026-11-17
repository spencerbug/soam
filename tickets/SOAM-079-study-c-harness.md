---
schema_version: 2
id: "SOAM-079"
title: "Implement and verify the two-candidate inference comparison"
type: "engineering"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-078"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-14"
updated: "2026-11-14"
github_issue: null
decision: null
---

# SOAM-079: Implement and verify the two-candidate inference comparison

## Recommended thinking

**high** — Separate observability, retained state capacity, estimator competence and resource costs in the bounded C-H1 comparison.

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

- [SOAM-078](SOAM-078-study-c-protocol.md) — completed prerequisite; decisions require proceed.

## Branch conditions

The November 14 owner request and SOAM-078 select C-H1 only. SOAM-077's baseline recommendation is satisfied; SOAM-078 must accept the contract before implementation. SOAM-079 must verify invariants and feasibility before development/confirmation. SOAM-037 remains backlog under the failed SOAM-052 sharing gate. SOAM-053 is conceptual context only. Completing C-H1 does not select scheduling, acquisition, attention, object memory or another branch.

## Completion record

Pre-implementation baseline: `UV_CACHE_DIR=/private/tmp/soam-uv-cache uv run pytest` — 266 passed in 31.03s. Historical B2 committed as `a552034`; lint, 78-ticket validation and frozen-source/artifact hash checks passed. The local Qwen worker returned `Transport closed`; primary-agent review proceeded directly. This baseline preceded all Study C fitting.

Implementation completed under `soam/ambiguity/`; no historical source changed.
Validation: 19 targeted scientific-invariant tests passed; the full suite before the
final timing-loop equivalence test passed 284 tests in 26.37s; lint passed. The
[observability check](../reports/study-c/observability.json) verifies paired complete
histories and visible rank. The [fixture projection](../reports/study-c/fixture-projection.json)
passes: 2790.86 projected CPU seconds, 1,534,194,316.5 projected artifact bytes,
399,523,840 projected RSS bytes, including stated margins. Actual fixture: five fits,
5.900456 CPU seconds, no failure; the 67-fit plan is below the 70-fit ceiling.
The timed inference loop exactly matches archived state/probability inference.
This is engineering acceptance, not evidence for C-H1.

The final full core suite, including timing-loop equivalence, passed 285 tests in 26.93s before confirmation.
