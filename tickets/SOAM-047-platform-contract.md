---
schema_version: 2
id: "SOAM-047"
title: "Define the shared-population experiment platform contract"
type: "decision"
status: "ready"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M0"
work_packages: ["WP-00", "WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-046"]
labels: ["type:decision", "priority:P0", "milestone:M0"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-047: Define the shared-population experiment platform contract

## Recommended thinking

**xhigh** — Choose a small reusable abstraction without building topology assumptions or unsupported energy claims into every experiment.

## Problem / hypothesis

The current harness implements one frozen handover protocol. A broader platform needs explicit contracts for interchangeable dynamics and tasks, including shared neurons across feature, relation, and action-relation functions.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Define only the state/parameter/observation/action, intervention, metric, and artifact contracts needed for E1; preserve historical entry points. Use an existing protocol document as the short RFC rather than creating another design layer.
- Specify the shared candidate, constrained disjoint control, GRU, and cheap linear sanity reference contract; extension points may describe later backends without implementing them.
- Define parameter/state/external-memory/exposure accounting and a finite tuning/time budget based on fixture timings. No general framework or new environment stack.
- Keep evaluator truth, future targets, live state, persistent parameters, and no-write rollout permissions explicit; no universal energy assumption.

## Acceptance criteria

- [ ] Publish concrete minimal signatures, one worked E1 flow, and one small example showing task-specific code does not leak into recurrence.
- [ ] Document the ownership/resource ledger, numerical reproducibility, invalid-run behavior, and preservation checks.
- [ ] Adopt the review measurement defaults or justify changes before fitting; specify the time/storage cap and equal-tuning rules.
- [ ] Record proceed/revise/stop in this decision ticket using the lightweight RFC convention; explicitly defer unneeded backend and application infrastructure.

## Metrics / evidence

Planned contract: docs/RECURRENT_PLATFORM_CONTRACT.md. Review existing handover and writer contracts, the v0.3 scope, and primary sources for the selected rules. Architecture evidence only; no scientific gate is passed.

## Dependencies

- [SOAM-046](SOAM-046-shared-platform-scope.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Branch conditions

The first delivery serves only the minimal SOAM-049 recall/transition pilot. Specify extension boundaries but implement no general backend catalogue. A second tiny task fixture checks reuse only; it is not a localization or learning-module study. Expand infrastructure only when a selected fork identifies a concrete missing capability.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R3/R6/R7/R11) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Set decision to proceed,
revise, or stop only after completing the review.
