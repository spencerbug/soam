---
schema_version: 2
id: "SOAM-059"
title: "Select one bounded research fork from the pilot evidence"
type: "decision"
status: "backlog"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "MX"
work_packages: ["WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-051"]
labels: ["type:decision", "priority:P0", "milestone:MX"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-059: Select one bounded research fork from the pilot evidence

## Recommended thinking

**xhigh** — Distinguish a negative mechanism finding from a justified next experiment and prevent branching from becoming an unlimited search.

## Problem / hypothesis

The pilot may support sharing, reveal interference, show no benefit, or fail to identify
an effect. A scientific gate cannot double as unconditional authorization for every
future experiment. Use the [research paths](../docs/RESEARCH_PATHS.md).

## Scope

- Review the full E1 evidence, validity, guardrails, budgets, and separate SOAM-052 claim outcome. Rank alternatives by expected architectural information per implementation/compute cost.
- Select at most one next experiment. Default preference is E2 minimal acquisition (SOAM-039) if a usable candidate and task exist; E3 active disambiguation (SOAM-053) is the next alternative. Concurrency SOAM-037, recurrent attention SOAM-045, and other diagnostics need a specific information-gain rationale.
- A negative sharing result can select a labeled alternative learner or belief model without asserting useful shared neurons. Name the exact protocol, candidate, decisive endpoint, resource cap, deferred options, and fresh data.
- Allow at most one diagnostic follow-up per pilot failure mode in the initial allocation. Later successful studies require a fresh routing decision and explicit edge updates before the next experiment; this ticket is not an indefinitely mutable controller.

## Acceptance criteria

- [ ] Publish a branch record citing results and the reason competing branches were deferred; select no more than one experimental continuation.
- [ ] Record proceed/revise/stop for the continuation decision. Proceed authorizes only the named bounded protocol, never a positive sharing/attractor claim.
- [ ] Sharing-based integration additionally requires SOAM-052 proceed. A negative sharing result can still motivate an application control or diagnostic through this decision, with the failed claim explicitly retained.
- [ ] Update selected ticket body conditions, readiness, and priority mirrors together. A corrective branch gets a fresh ID/protocol before implementation; preserve failed gates and use a fresh review instead of changing their outcomes.
- [ ] Record finite compute/data limits, a decisive result, and a stopping/defer condition before any follow-up. Invalid or inconclusive evidence cannot select a supposedly validated mechanism.

## Metrics / evidence

Expected record: reports/RESEARCH_FORK_SELECTION.md. Evidence is the complete pilot
report and preregistered outcome classifications, not imagined results. The routing
decision depends on the completed experiment, so a negative SOAM-052 outcome does
not make it unreachable. Later branching uses the same record format and fresh
bounded decisions where required; this ticket is not a permanent automatic controller.

## Dependencies

- [SOAM-051](SOAM-051-shared-population-study.md) — complete experiment, including negative results; no positive result is presumed.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R4/R5/R12) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Not started. No fork has been selected. Record actual evidence, decision, selected
protocol/ticket, budget, deferred alternatives, and downstream readiness.
