---
schema_version: 2
id: "SOAM-059"
title: "Select one bounded research fork from the pilot evidence"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "MX"
work_packages: ["WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-051"]
labels: ["type:decision", "priority:P0", "milestone:MX"]
assignees: []
created: "2026-11-05"
updated: "2026-11-09"
github_issue: null
decision: "proceed"
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

- [x] Publish a branch record citing results and the reason competing branches were deferred; select no more than one experimental continuation.
- [x] Record proceed/revise/stop for the continuation decision. Proceed authorizes only the named bounded protocol, never a positive sharing/attractor claim.
- [x] Sharing-based integration additionally requires SOAM-052 proceed. A negative sharing result can still motivate an application control or diagnostic through this decision, with the failed claim explicitly retained.
- [x] Update selected ticket body conditions, readiness, and priority mirrors together. A corrective branch gets a fresh ID/protocol before implementation; preserve failed gates and use a fresh review instead of changing their outcomes.
- [x] Record finite compute/data limits, a decisive result, and a stopping/defer condition before any follow-up. Invalid or inconclusive evidence cannot select a supposedly validated mechanism.

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

Completed 2026-11-09. **Decision: proceed to SOAM-039's E2 protocol design only**,
using G32 with one bounded recurrent local-error writer on a changed translation
gain. The [branch record](../reports/RESEARCH_FORK_SELECTION.md) ranks acquisition,
active disambiguation, a single S32 diagnostic, a simpler reference and stopping;
it gives the selected task, decisive endpoint, resource/data ceiling, fresh-stream
requirements, stopping conditions and deferred alternatives. This is a labeled
conventional learner, not validated useful sharing or acquisition.

Verified SOAM-051 done with complete E1 v1+A1 evidence, SOAM-052 done/stop, and
SOAM-047 done/proceed. Absolute recall failure, passing relative guards, unresolved
causal precision, T32 equality, exact reproduction and reporting telemetry limits
are retained. The existing cumulative E1 ledger is closed and unchanged. No E1
retuning, corrective experiment, implementation or follow-up trial occurred.

Only SOAM-039 becomes P0/ready; its body now names this selection and bounded
conditions. SOAM-044/040/041 await their prerequisites; E3/attention remain unselected,
and SOAM-052-dependent work remains unready. README, hypothesis/routing/roadmap
status and priority/milestone mirrors were updated together. No new ticket or
remote issue is required for this already-planned alternative protocol.

Review base: `a4ddf9479fad06240a44030726ce6f99d2f25eb2`. Baseline `uv run pytest`:
190 passed in 17.59s. Final `uv run python scripts/check_tickets.py`, local-link,
metadata/body-condition, frozen-evidence preservation and `git diff --check` results
are recorded in [verification.json](../reports/research-fork-selection/verification.json).
The bounded Qwen extraction was unusable and rejected; direct evidence review was
used. The report flags the research-direction change for a possible joint blog/report,
clearly as a proposal grounded in E1; nothing was published.

**Next eligible action:** SOAM-039's RFC and finite E2 protocol/manifest, inside a
3,600 CPU-second / 7,200 wall-second, 2 GiB RSS / 2 GiB artifact ceiling and at most
16 base fits across later fixtures/development/confirmation/reproduction. Exact
criteria and preflight must precede implementation and execution. This completed
routing decision cannot activate another branch; later routing needs a fresh decision.
