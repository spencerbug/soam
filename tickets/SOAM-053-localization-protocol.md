---
schema_version: 2
id: "SOAM-053"
title: "Specify active disambiguation with recurrent sensorimotor beliefs"
type: "decision"
status: "backlog"
priority: "P1"
recommended_thinking: "xhigh"
milestone: "M6"
work_packages: ["WP-01", "WP-10"]
hypotheses: ["H1", "H6", "H7"]
depends_on: ["SOAM-047", "SOAM-059"]
labels: ["type:decision", "priority:P1", "milestone:M6"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-053: Specify active disambiguation with recurrent sensorimotor beliefs

## Recommended thinking

**xhigh** — Separate belief quality from policy quality and information advantage in an aliased closed-loop task.

## Problem / hypothesis

A sensorimotor memory should retain uncertainty and use an informative action to distinguish locally identical situations requiring different outcomes. This small NeuroSLAM-inspired task tests active perception rather than building full SLAM. See E3 in the review.

## Scope

- Specify a tiny aliased 2D task with fixed local features, noisy self-motion, a short discriminating probe, and a simple held-out goal. Declare the observation/action interface and what prior geometry is supplied.
- Cross a selected recurrent candidate and GRU with the same supplied informative-action and fixed-action policies; include a small same-data belief/structured reference. Known-map/true-dynamics filters are labeled upper bounds, not equal-information baselines.
- Compare equal recorded histories for representation diagnostics and paired initial environments/bounded sensing costs for closed-loop behavior. Include no-information and misleading-cue trials; require uncertainty under irreducible ambiguity.
- Freeze capped actions-to-correct-goal as primary, success/false-confidence/Brier guardrails, seed/split/compute budgets and finite tuning. Persistent memory is frozen in this first active-perception study; combining E2 writes is a later integration experiment.

## Acceptance criteria

- [ ] Publish a minimal RFC/protocol with task identifiability, policy/model factorization, information parity, and the full scaffold/storage ledger.
- [ ] Adopt E3 quantitative defaults or justify changes before fitting; define the failure cap and confidence threshold for false commitments.
- [ ] Include action-removal/shuffling, feedback ablation, ambiguous no-information controls, and informative-versus-fixed action comparison.
- [ ] Report pose/goal success, capped action cost, uncertainty calibration, false commitments and drift separately; no full SLAM claim.
- [ ] Record proceed/revise/stop for this bounded task; defer learned exploration, full mapping, richer vision and physical robotics.

## Metrics / evidence

Expected protocol: docs/RECURRENT_LOCALIZATION_PROTOCOL.md (stable path). Use E3 review defaults once frozen. Review NeuroSLAM for pose/mapping boundaries and active-perception sources for the task rationale; no exact NeuroSLAM reproduction is required.

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — required completed prerequisite; decision prerequisites require proceed and the branch conditions below.
- [SOAM-059](SOAM-059-research-fork-selection.md) — required completed prerequisite; decision prerequisites require proceed and the branch conditions below.

## Branch conditions

Start only after named E3 selection by SOAM-059 or a fresh routing decision whose edge is explicitly substituted. This may follow negative sharing results using a labeled alternative. E2 success is not required for frozen-memory active disambiguation; combined learning and active control need a later scoped integration decision.

## Scientific review disposition — 2026-11-05

**Future capability** (R5/R6/R11) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Set decision to proceed,
revise, or stop only after completing the review.
