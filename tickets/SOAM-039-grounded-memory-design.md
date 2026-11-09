---
schema_version: 2
id: "SOAM-039"
title: "Specify minimal grounded acquisition and retention"
type: "decision"
status: "ready"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-047", "SOAM-059"]
labels: ["type:decision", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-01"
updated: "2026-11-09"
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

## Named selection — SOAM-059, 2026-11-09

[SOAM-059](SOAM-059-research-fork-selection.md) is done/proceed and selects this
E2 protocol only; SOAM-047 is done/proceed. The [branch record](../reports/RESEARCH_FORK_SELECTION.md)
owns the routing envelope. SOAM-052 remains done/stop: no useful-sharing or
integration gate is bypassed. This ticket is **ready, not started or approved**.

- Candidate: G32, using its E1 development-selected offline settings on fresh
  base-training streams, with one bounded local-error writer limited to the
  candidate-state block of `gru.weight_hh`. Define and review the derivative,
  proposal equation, finite norm/storage budgets and rollback; freeze every other
  parameter during online writes. No architecture or offline tuning sweep.
- Task: one changed translation-action gain under fixed sensing. Prove observable
  identifiability with disclosed structural priors and nonzero excitation; protect
  recall and unaffected-command transitions. This is not full old/new regime
  retention under identical cues. No evaluator state or projection inverse enters
  learning, and held-out evaluation never supplies write targets.
- Compare exactly the writer, no-write, RLS residual, same-block online gradient,
  and bounded retrieval conditions. Count all offline and online exposure,
  sufficient statistics, records and live state. One-shot is one distinct target
  and one update; test reset persistence and held-out states/actions at
  0/1/2/4/8/16 observations. No replay arm, learned scopes or consolidation.
- Primary question: does recurrent writing improve reset-held-out free-8
  acquisition area over strong adaptive controls while protecting prior behavior?
  Adopt or justify the review's 20% area advantage and 0.005 retention bound;
  freeze absolute competence, multistep, uncertainty/precision, multiplicity,
  one-shot and stopping rules before fitting. A simple learner winning is valid.
- Entire later branch ceiling: 3,600 CPU seconds, 7,200 wall seconds, 2 GiB peak RSS,
  2 GiB cumulative artifacts, 16 offline fits maximum (2 fixture/calibration,
  3 development, 10 confirmation, 1 repeat). At most two update configurations per
  adaptive condition, 20 adaptation episodes/root and 16 distinct new transitions
  per episode; see the report for full exposure/evaluation limits. Charge failed
  attempts and all scientific calibration/audit work. No E1 budget is renewed.
- Require fresh E2 train/development/confirmation/fixture/diagnostic streams and
  base fits; E1 results are exposed design evidence. A whole-inventory calibrated
  preflight and source freeze must precede confirmation in later tickets.
- If a sound identifiable protocol, competent controls or finite feasible study
  cannot be specified within this envelope, record revise/stop and leave
  implementation unready. No automatic S32 rescue or substitute branch. Protocol
  approval is not empirical validation; later branches need a fresh routing decision.

## Scientific review disposition — 2026-11-05

**Essential next protocol** (R4; selected by SOAM-059 on 2026-11-09) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Protocol not started. Readiness only was established by SOAM-059 on 2026-11-09;
its report and verification record document prerequisite/body-condition checks.
Record actual RFC/manifest, sources, review and validation here when this ticket is
performed. Keep `decision: null` until that separate design review is complete.
