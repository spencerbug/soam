---
schema_version: 2
id: "SOAM-089"
title: "Review recurrent retrieval reliability and added settling benefit"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-088"]
labels: ["type:decision", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-18"
updated: "2026-11-18"
github_issue: null
decision: "proceed"
---

# SOAM-089: Review recurrent retrieval reliability and added settling benefit

## Recommended thinking

**xhigh** — Distinguish algebraic storage, correct completion, incremental settling
and complete-system value; preserve the adjusted precision rules and negative gates.

## Problem / hypothesis

Does the completed fixed PH768 pilot support reliable persistent retrieval, a
practical causal benefit from added settling, or an advantage over conventional
controls? Which single diagnostic would most reduce architectural uncertainty?

## Scope

Review [D-R1 v1](../docs/STUDY_D_R1_PROTOCOL.md), all mandatory contrasts/guards,
execution validity, resources and [measured evidence](../reports/STUDY_D_R1.md).
Accept a supported, negative or inconclusive scoped outcome. Interpret the post hoc
checkpoint audit separately. This decision neither runs a follow-up nor passes a
shared-population, learned-scope or integrated-system gate.

## Acceptance criteria

- [x] Verify source, frozen settings, data boundaries, completeness and cumulative resources.
- [x] Apply every frozen endpoint, guard and precision rule, including adverse evidence.
- [x] Separate storage preservation, recall quality, added settling and complete-system costs.
- [x] Record one scoped reference decision and at most one next recommendation, without execution.
- [x] Preserve historical outcomes and synchronize the hypothesis ledger, tickets and indexes.

## Metrics / evidence

Ten independent confirmation roots; adjusted 12-quantity family, .05 primary
practical margin, .10 contrast-width limit. Review all REG/KV/REG-LIFT contrasts,
retention/false-recall guards, full/partial cues, perturbation and cost curves,
5,497 exact repeated arrays and 2,100 independently reduced endpoints.

## Dependencies

- [SOAM-088](SOAM-088-recurrent-retrieval-study.md) — done, complete bounded study.

## Branch conditions

The owner's D-R1 instruction and fresh allocation authorize its result review.
Historical SOAM-052 stop, SOAM-069 revise and A/B/B2/C/D decisions stand. No D3/D4,
E0/F, coupling, capacity, replay, learned organization or downstream implementation
is activated. A future experiment needs fresh routing and its own frozen protocol.

## Completion record

**Proceed with acceptance of the scoped evidence and retained KV reference only.**
The [decision](../reports/STUDY_D_R1_DECISION.md) accepts valid execution and the
precise negative practical-settling result, +.02143 [.00982, .03661] against .05.
PH768's earlier-object accuracy, retention and accepted-wrong guards have established
failures. The secondary comparator intervals favor REG/KV/REG-LIFT but remain
categorically inconclusive under the frozen width cap. All quantities and complete
resource mismatches are retained. No positive retrieval, sharing or integration gate
is inferred from this decision's `proceed` metadata.

The post hoc checkpoint audit preserves all acquired codes in the final fourth-sequence
projectors at ten roots to numerical precision; it does not prove correct completion
or diagnose the failure's cause. The only next recommendation is a fresh fixed-size
retrieval/decoding diagnostic, with an explicitly privileged evaluator-only decode
ceiling. It is not a selected experiment or implementation authorization. No successor
ticket is activated and no extra fit, write or retrieval trial was executed.

Reviewed all 12 adjusted quantities, descriptive full/partial/perturbation comparisons,
worst-query examples, storage/latency arithmetic, reset/no-write boundaries and source
receipts. Plots were visually checked; legend/overlapping labels were corrected by
the separately versioned reporting script without touching frozen numerical source.
The owner's substantive blog notice distinguishes measured findings from proposals;
no publication or remote issue action occurred.

Actual checks: `uv run ruff check soam tests scripts` and `git diff --check` passed;
the full scientific suite previously passed 318 tests and remains unchanged.
`uv run python scripts/close_study_d_r1.py` verifies 110 frozen source files,
102 historical D source files and all 1,431 original archived files; its final index
covers 1,441 raw files and 21 report files. The existing independent audit verifies
5,497 exact repeated arrays and 2,100 endpoints. Final charged numerical/reporting
use is **651.423344 CPU / 652.182670 wall seconds, 428,195,840 B peak RSS and
572,385,949 artifact bytes before the closeout receipt**, below all accepted limits;
see [closeout](../reports/study-d-r1/closeout.json). Engineering and handwritten
unit tests are separate, as declared. There were no numerical failures or exclusions.

Hypothesis ledger, README/roadmap/research paths, proposal index and priority metadata
are synchronized. SOAM-052 stop, SOAM-069 revise and all earlier studies remain intact.
Final checks: `uv run python scripts/check_tickets.py` validates 90 tickets and two
templates; 511 local links resolve across 12 changed Markdown files; all 21 final
report hashes still match. Ruff and whitespace checks pass.
