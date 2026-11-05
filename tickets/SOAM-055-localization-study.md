---
schema_version: 2
id: "SOAM-055"
title: "Measure active disambiguation and belief-guided behavior"
type: "experiment"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M6"
work_packages: ["WP-01", "WP-10"]
hypotheses: ["H1", "H6", "H7"]
depends_on: ["SOAM-054"]
labels: ["type:experiment", "priority:P1", "milestone:M6"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-055: Measure active disambiguation and belief-guided behavior

## Recommended thinking

**high** — Attribute closed-loop gains to belief and informative action without confusing policy scaffolding or privileged map access with intelligence.

## Problem / hypothesis

Test the frozen localization protocol and retain its limits as a small analogue of NeuroSLAM.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Run the frozen E3 active/fixed-policy and candidate/reference comparisons on paired environments and untouched confirmation seeds.
- Measure capped actions-to-correct-goal, success, false confident commitments, Brier calibration and drift; analyze equal-history belief diagnostics separately from closed-loop observations.

## Acceptance criteria

- [ ] Publish the primary paired effect and uncertainty plus all success/calibration guardrails and per-seed failures.
- [ ] Attribute effects using the model-by-policy comparison, action/feedback ablations and irreducibly ambiguous controls. Count supplied policy and map information.
- [ ] Archive complete source/config/seeds/software/numerical settings, sensing/execution exposure, state/storage/time/compute and preselected confirmation reproduction.
- [ ] Distinguish active localization/goal completion from full SLAM, learned exploration, online acquisition or broad embodied intelligence. A negative result completes the study without activating another branch.

## Metrics / evidence

Planned report: reports/RECURRENT_LOCALIZATION.md. Success/failure criteria come from the frozen task protocol, not from selecting favorable plots or seeds.

## Dependencies

- [SOAM-054](SOAM-054-localization-adapter.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Branch conditions

On a reproducible primary-endpoint gain, propose one bounded generalization task or integration review; do not auto-expand. On isolated drift/aliasing or acquisition/binding failure, propose one diagnostic with frozen budget and new data. On no advantage, prefer the simpler reference or stop this mechanism. On invalid/inconclusive evidence, repair or obtain the prespecified additional evidence before scientific claims. Record the outcome, selected/deferred alternatives, and fresh decision/protocol needed for further trials; this experiment does not grant its own continuation approval.

## Scientific review disposition — 2026-11-05

**Future capability** (R5) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Preserve negative
outcomes; this ticket does not authorize other backlog work.
