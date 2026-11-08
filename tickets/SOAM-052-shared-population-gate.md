---
schema_version: 2
id: "SOAM-052"
title: "Review evidence for useful shared recurrence"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-051"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-05"
updated: "2026-11-08"
github_issue: null
decision: "stop"
---

# SOAM-052: Review evidence for useful shared recurrence

## Recommended thinking

**xhigh** — Assess a prespecified benefit and interference trade-off without extending a minimal pilot into claims about concurrency, learning, or integration.

## Problem / hypothesis

A preferred shared architecture and passing engineering fixtures cannot authorize scientific claims or broad integration.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Apply the outcome precedence and claim limits in [E1 v1](../docs/SHARED_POPULATION_PROTOCOL.md). T32 can reproduce the shared candidate on separate-role episodes; even a positive pilot supports a useful shared implementation, not a uniquely causal performance advantage of physical neuron sharing over tied parameters.
- Review the complete minimal pilot against its frozen benefit, retention, causal-overlap, validity, and resource criteria.
- Record the supported mechanism and operating limits separately from the next-experiment selection in SOAM-059.

## Acceptance criteria

- [x] Record proceed only for supported useful sharing with causal shared-unit evidence and satisfied guardrails; report attraction evidence separately.
- [x] Record revise for a bounded unresolved/confounded result or stop for a clear failure of the tested claim; no advantage must not be relabeled success because recurrence runs.
- [x] Do not require or claim concurrent binding/handover, acquisition, or integration from this pilot. A proceed permits testing those capabilities, subject to fork selection and their own criteria.
- [x] Preserve failed gates. SOAM-059 may select a diagnostic or alternative application after negative evidence, but cannot convert it into a positive sharing result.

## Metrics / evidence

Completed report: [SHARED_POPULATION_GATE.md](../reports/SHARED_POPULATION_GATE.md). SOAM-036 remains the historical v1 decision; neither it nor this design preference substitutes for this measured review.

## Dependencies

- [SOAM-051](SOAM-051-shared-population-study.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R1/R2/R3) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Implement, measure, or review E1 against the frozen protocol and review defaults. Report performance utility separately from attraction and from biological/semantic claims. Require matched random/disjoint lesions and a competent GRU; no capacity or information advantage may be relabeled a sharing effect.

## Completion record

Started 2026-11-08 after verifying SOAM-051 is done with all acceptance items checked,
the full E1 v1+A1 report and scientific reproduction. The body requires a validity,
resource and frozen-criteria review; it does not require new experiments. Baseline
`uv run pytest`: 190 passed in 15.80s. Gate decision remains open during the audit.


### Decision — stop, 2026-11-08

The [full gate report](../reports/SHARED_POPULATION_GATE.md) applies the frozen
[E1 v1 precedence](../docs/SHARED_POPULATION_PROTOCOL.md) after auditing validity,
information parity, resources, uncertainty and guardrails. All acceptance items are
satisfied; the conditional proceed criterion is evaluated and **not met**. This is
**stop for the tested S32 useful-sharing claim**, not rejection of all shared neurons
or termination of the experiment platform. Recommended thinking remains **xhigh**:
clear absolute failure must be separated from passing relative guards, unresolved
causal precision and physical-overlap non-identifiability.

- Governing outcome: `recall_interference_or_failure`, specifically absolute recall
  failure. Mean 0.077657, ordinary 95% root interval [0.068287, 0.086725], maximum
  allowed 0.02. Every root mean fails. Relative retention guard upper bounds
  -0.008635 and 0.000726 both satisfy 0.005; no destructive-interference conclusion.
- No invalidating scientific defect or incomplete inventory is identified. Two
  reporting-attempt RSS measurements and the first terminal diagnosis remain
  unavailable; capture-wrapper config hashing and L12 generic exposure fields are
  resolved using actual settings/traces/source. The report explicitly qualifies
  telemetry and efficiency claims rather than assuming missing resources are zero.
- Utility fails the all-reference criterion; both GRUs have lower primary error in
  every root. D16 meets its individual benefit criterion, D25 misses precision,
  L12 is inconclusive, and GRU widths prohibit the frozen precise-no-benefit label.
  Six causal contrasts have positive adjusted bounds but all miss width caps;
  none is a precise failure. Recovery is `diagnostic_criteria_not_met`.
- T32's exact intact equality and T32/D16 opposite-bank isolation remain central:
  660 prediction arrays per property rechecked exactly. Unit-basis intervention
  effects do not identify a unique prediction advantage of physical overlap,
  semantic neurons, concurrent binding, or unavoidable memory savings.
- Reviewed complete 119-fit/27,820-cell evidence. The new read-only
  [audit](../reports/shared-population-gate/audit.json) verifies all prior compact
  checksums, both raw archive seals, all 77 new fits/25,300 cells, 53,900 paired
  training references, 4,620 base evaluation references, selection ordering,
  source/calibration/config identity and adjusted/ordinary bootstrap bounds.
  Reproduction independently remains exact: 11,764 arrays / 7,280 references /
  9,603 records. No new fit, condition, observation, retuning or budget extension.
- Source freeze `fe9925f796af0a835a509cbef3bded4be3783fa3`; execution HEAD
  `7b3dea667cd65626af259a6ccbf0e17e0d8e96f6`; reviewed evidence commit `8e46d78`;
  source digest `b52329efaa0a4927337691e60a5b610ed08984b884aef8dd5b7b12801f2408c9`.
  Neural config 1 / L12 config 0, primary G32, ten confirmation roots and seed-11
  repeat are unchanged. Exact provenance and artifact links are in the report.
- `uv run pytest`: 190 passed in 15.80s. `uv run python reports/shared-population-gate/audit.py`:
  all checks pass. Final `uv run python scripts/check_tickets.py` and whitespace/link
  checks are recorded in [verification.json](../reports/shared-population-gate/verification.json).
  Gate audit adds 62.041096 CPU seconds to conservative accounting; cumulative
  2,906.209410 CPU, 461.320613 overhead CPU and 680,181,226 artifact bytes stay
  within original ceilings. The original SOAM-051 ledger is unchanged.

Proceed is unsupported; revise would incorrectly let unresolved secondary criteria
or hypothetical retuning displace the earlier clear recall failure. Preserve this
failed gate permanently. A later corrective protocol/review must be fresh, with
fresh confirmation streams as applicable; it cannot edit this stop into proceed.
Sharing-dependent concurrency/control/composition/organization remains unready.
The next eligible task is **SOAM-059 routing**, not executed here, and no follow-up
experiment or replacement architecture is selected. Historical gates retain their
scope. The separation of competence, retention, intervention sensitivity,
identifiability and useful recovery merits a joint blog post/report; nothing was
published. Qwen's invalid extraction was rejected and the primary audit used instead.
