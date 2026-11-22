---
schema_version: 2
id: "SOAM-102"
title: "Design the state hysteresis and navigability experiment"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-101"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-22"
updated: "2026-11-22"
github_issue: null
decision: "proceed"
---

# SOAM-102: Design the state hysteresis and navigability experiment

**Current routing notice:** [SOAM-103](SOAM-103-assembly-organization-plan.md)
selects [Assembly organization and selective routing](../docs/proposed-studies/STUDY_ASSEMBLY_ORGANIZATION.md)
as the next design path. This ticket remains done/proceed for its completed
retention design. E0-HYS is unrun and currently unselected, not an AO-1 prerequisite.
The historical decision and numerical contract below are preserved.

## Recommended thinking

**xhigh** — Distinguish explicit hysteresis, ordinary slow updates, useful continuous-state retention and the stronger claim of learned assembly routing.

## Problem / hypothesis

The owner requests a written proposal and experiment design following the
[E0-HOLD decision](../reports/STUDY_E0_HOLD_DECISION.md). Heterogeneous state
persistence might reduce drift without suppressing legitimate actions or recovery.
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Design one bounded single-population mechanism experiment and document the
conditional assembly-routing hypothesis. Classification: **essential next** for
the design at adoption; the subsequent SOAM-103 selection brings bounded learned
organization into the next design question. This completed task does not
execute training, implement a model, publish, or change a completed result.

## Acceptance criteria

- [x] Record the owner selection and distinguish it from SOAM-101's unactivated optimization recommendation.
- [x] Specify equations, controls, data/splits, primary endpoint, guardrails, inference, resources and stopping rules.
- [x] Explain what would constitute hierarchy evidence and why the first test cannot establish it.
- [x] Review consistency, links, ticket metadata and numerical inventory; record the design decision.

## Metrics / evidence

The [proposal](../docs/proposed-studies/STUDY_E0_HYSTERESIS.md),
[protocol](../docs/STUDY_E0_HYSTERESIS_PROTOCOL.md) and
[manifest](../docs/protocols/study_e0_hys_v1.json) define eight fitted families,
105 development fits, 160 fresh confirmation fits, eight exact repeats and eight
engineering fixtures. Nineteen simultaneous root intervals separate the primary
retention/navigation conjunction from the secondary heterogeneity contrast.
No measured hysteresis result is available or implied by protocol completion.

## Dependencies

- [SOAM-101](SOAM-101-e0-hold-decision.md) — done/proceed for evidence acceptance only.

## Branch conditions

The [November 22 owner request](../docs/requests/state_hysteresis_2026_11_22.md)
selects design of this corrective mechanism study and explicitly keeps thresholds
fixed for the first test.
Historical E0 inconclusive, E0-HOLD negative joint fix, and E1 sharing stop remain
unchanged. No integrated organization gate is bypassed; no tree is supplied or assumed.

## Completion record

**Proceed with E0-HYS v1 design only.** The written proposal and numerical contract
are complete; implementation and trials remain unstarted. This is the fresh
owner-selected design after SOAM-101, not an amendment to its completed outcome or
an activation of its conditional optimization recommendation.

Manual review covers the exact play equation and gradients, fixed thresholds versus
learned use of units, unchanged information interfaces, slow/heterogeneous-leak and
conventional controls, development-only selection, precision-qualified decisions,
small-action pinning, reversal/release and small-perturbation guards, finite resource
ceilings, and the inability of this single-orientation task to establish hierarchy.
The conditional routing proposal specifies causal evidence rather than treating
clusters or low drift as a tree. A later hierarchy study needs fresh routing.

Reviewed evidence: [E0](../reports/STUDY_E0.md),
[E0-HOLD](../reports/STUDY_E0_HOLD.md), their decisions, and the current navigation
and hold interfaces. Primary research is linked beside its scoped claims in the
proposal/protocol. Design source baseline is
`047e2b81496a41dbf96537e11c39b4d17e54c1d4`; this documentation has no fitted source
fingerprint, checkpoints or measured results. The local Qwen read-only harness
(job `9731751fa43a42d691b9134085392bab`) timed out and its partial extraction
contained errors; the primary agent checked relevant source directly and used no
unverified worker finding.

Validation: `uv run --offline --no-sync python scripts/check_tickets.py` accepts
103 tickets and two templates; `git diff --check` passes. An inline standard-library
audit checks configuration counts, 273-fit inventory, twenty confirmation roots,
nineteen intervals/eighteen primary quantities, disjoint root lists, coefficient
means and local Markdown targets. Algebra-only scalar checks confirm zero-width
identity and history-dependent retained interiors. These are document/math checks,
not trained-model invariant tests. No numerical source or historical empirical
report was modified; no training or full pytest run was needed for these document
changes. The future harness still owes all declared invariant and preflight checks.

The selective-persistence versus emergent-routing distinction is a substantive
concept for a future joint blog/report; the owner is notified. Publication is not
part of this design request.

**November 22 connectivity clarification:** the owner distinguished input-rooted
connection pathways from temporal hysteresis. The proposal now contains the local
Jacobian derivation, the role of receiver gain/deadbands, and the current symmetric
core/dense input limitations. This strengthens the scope boundary: the accepted
protocol tests retention only, with no theoretical sufficiency or emergence claim
for routing. Numerical criteria and fixed-threshold selection are unchanged.

Clarification validation: ticket validation and `git diff --check` pass. An
algebra-only eight-coordinate central-difference audit, exercising both retained
and following branches away from boundaries, agrees with the derived Jacobian to
maximum absolute error 2.68e-11. This checks the derivative, not hierarchy formation;
no fit or scientific evaluation was run.
