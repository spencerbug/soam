---
schema_version: 2
id: "SOAM-081"
title: "Review candidate-state benefit and conditional scheduling"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-080"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-14"
updated: "2026-11-14"
github_issue: null
decision: "proceed"
---

# SOAM-081: Review candidate-state benefit and conditional scheduling

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

- [SOAM-080](SOAM-080-study-c-experiment.md) — completed prerequisite; decisions require proceed.

## Branch conditions

The November 14 owner request and SOAM-078 select C-H1 only. SOAM-077's baseline recommendation is satisfied; SOAM-078 must accept the contract before implementation. SOAM-079 must verify invariants and feasibility before development/confirmation. SOAM-037 remains backlog under the failed SOAM-052 sharing gate. SOAM-053 is conceptual context only. Completing C-H1 does not select scheduling, acquisition, attention, object memory or another branch.

## Completion record

**Proceed with acceptance of the scoped C-H1 result and reference recommendations
only.** The [decision](../reports/STUDY_C_DECISION.md) answers all five research
questions and selects no subsequent experiment. [Measured evidence](../reports/STUDY_C.md)
supports TWO16 over PC16 and the equally wide retained-state PC32 control. The
conventional mixture's advantage over the collapsed reference is precisely smaller
than the frozen .01 Brier practical margin; no meaningful recurrent advantage over
that mixture is established. Retain ADAPT1-C as the compact conventional reference
and TWO16 as the faster recurrent implementation, with full cost accounting.

The nominal ambiguity pass does not extend to the coherent-fault/genuine-change
cause pair: the same evidence yields overconfident outputs. C-H2 scheduling, C-H3
learned allocation and complementary objects remain unselected. The decision gives
the conditions for a later scheduling protocol without implementing one.

Reviewed the frozen protocol, development selection, all nine mandatory models,
ten independent confirmation roots, adjusted primary/guard intervals, secondary
failure cases, calibration, costs and the SOAM-080 audit. All 67 fits completed;
1,530 repeated arrays match exactly and 810 independently reduced values agree
within 1.6653e-16. The full core suite passed 285 tests before confirmation.
Resource ceilings pass. The documented resource-export reporting repair does not
change the source receipt or scientific outcomes. See SOAM-080 for actual commands,
source fingerprint, root/configuration receipt and final resource record.

Historical SOAM-052 stop and SOAM-069 revise remain unchanged. SOAM-037 and all other
conditional branches remain unactivated. The owner was notified of the measured
finding and limitation as potential joint blog/report material; nothing was published.

Final repository checks: `uv run ruff check soam tests scripts` passed;
`uv run python scripts/check_tickets.py` validated 82 tickets and two templates;
`git diff --check` passed. All 95 frozen source hashes and 2,092 indexed raw artifact
hashes were rechecked after documentation updates.
