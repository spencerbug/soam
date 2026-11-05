---
schema_version: 2
id: "SOAM-039"
title: "Specify minimal grounded acquisition and retention"
type: "decision"
status: "backlog"
priority: "P1"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-047", "SOAM-059"]
labels: ["type:decision", "priority:P1", "milestone:M2"]
assignees: []
created: "2026-11-01"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-039: Specify minimal grounded acquisition and retention

## Recommended thinking

**xhigh** — Isolate persistent rapid learning from state calibration, memorization, and extra exposure before adding skills or consolidation.

## Problem / hypothesis

A small number of grounded observations should improve held-out action-conditioned behavior while retaining prior competence. Existing local-write regressions make this an early risk to test. The historical single-matrix rule remains a comparison, not the selected solution. See E2 in the scientific review.

## Scope

- Select one usable candidate from the evidence and one identifiable low-dimensional changed-dynamics task with fixed sensing. Supply necessary structural priors explicitly; one observation cannot identify an arbitrary unknown transition function.
- Define writable objects, grounded targets, no-write evaluation, bounded proposals, exact rollback, and a state-reset recall test. Reuse SOAM-003 transaction invariants only where the representation fits.
- Compare the selected rule with no-write, delta/RLS, ordinary online-gradient, and bounded retrieval references at equal new observations and reported compute. Count all offline pretraining and history/replay exposures.
- Freeze budgets 0/1/2/4/8/16 distinct new transitions, held-out states/actions, retained tasks, acquisition-area and one-shot endpoints, and confirmation streams. Do not require concurrency, skills, generic instance-exception machinery, or the full replay/shadow-consolidation stack.

## Acceptance criteria

- [ ] Publish the short RFC and finite E2 protocol/manifest, adopting the proposed review margins or justifying changes before fitting.
- [ ] Make one-shot mean one distinct new observation and one declared update, without hidden replay or repeated target optimization; distinguish exact-example recall from parameter adaptation and generalization.
- [ ] Specify reset-transient-state/preserve-memory tests, no-write rollouts, target exclusion, rollback and finite storage; acquisition and retention must both be measured.
- [ ] Define fair adaptive and retrieval baselines, exposure/compute accounting, uncertainty, stop rules, and negative-result interpretations.
- [ ] Record proceed/revise/stop for a minimal experiment; a positive learning design does not pass H2/H3.

## Metrics / evidence

Expected protocol: docs/SHARED_POPULATION_LEARNING_PROTOCOL.md (stable planned path). Review the local-write report and selected pilot evidence. E2 acquisition area, one-exposure held-out error, old-task retention, reset persistence, multistep regressions, and update cost are required.

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — required completed prerequisite; decision prerequisites require proceed and applicable body conditions.
- [SOAM-059](SOAM-059-research-fork-selection.md) — required completed prerequisite; decision prerequisites require proceed and applicable body conditions.

## Branch conditions

Require named E2 selection in SOAM-059, or an explicitly revised edge to a fresh routing decision. A negative sharing result may select a labeled alternative learner. Earlier skills/concurrency requirements are removed only for this minimal acquisition experiment; no integration gate is bypassed.

## Scientific review disposition — 2026-11-05

**Future capability** (R4) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
Set decision to proceed, revise, or stop only when the review is complete.
