---
schema_version: 2
id: "SOAM-082"
title: "Specify and select post-reset persistent acquisition"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-047", "SOAM-081"]
labels: ["type:decision", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-17"
updated: "2026-11-17"
github_issue: null
decision: "proceed"
---

# SOAM-082: Specify and select post-reset persistent acquisition

## Recommended thinking

**xhigh** — Separate persistent acquisition from transient recall, evaluate strong simpler controls, and preserve information/resource parity.

## Problem / hypothesis

Does bounded grounded experience yield post-reset object knowledge and retention, and does one rank-one fast operator improve on explicit memory and online regression?

## Scope

Follow the [owner selection](../docs/requests/study_d_2026_11_17.md) and [D v1 protocol](../docs/STUDY_D_PROTOCOL.md). D0–D2 only; D3/D4, learned write gates, replay and integration are deferred.

## Acceptance criteria

- [x] Complete this bounded phase with evidence or documented negative/inconclusive/invalid outcome.
- [x] Verify reset, no-write inference, evidence parity, source identity and resource limits.
- [x] Preserve every mandatory comparator, independent-root uncertainty and historical outcome.
- [x] Record actual checks, artifacts and implications for the next ticket.

## Metrics / evidence

Post-reset canonical/free prediction, one/few-shot curves, sequential retention, unknown rejection, resource costs and exact repeat. The versioned protocol/manifest owns frozen criteria.

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — completed prerequisite; decision requires proceed.
- [SOAM-081](SOAM-081-study-c-decision.md) — completed prerequisite; decision requires proceed.

## Branch conditions

The November 17 owner request selects this fresh fork; the superseded SOAM-059 selection is not reused. SOAM-082 must accept the protocol before implementation; SOAM-083 must verify invariants and fixture feasibility before development/confirmation. SOAM-052 stays stop. No downstream integration or D3/D4 branch is activated by completion.

## Completion record

Preflight complete: historical reports read; all 95 Study C frozen source hashes verified. Baseline 285 tests passed, Ruff and 82-ticket validation passed before D implementation. Prior work committed as `bf15033`. Protocol and manifest reviewed before fitting; no D fits had executed at that review.

Protocol review: **proceed for D0–D2 only**. Analytic one-snapshot identifiability, independent appearance/relationship sampling, missing-cue ambiguity, mask-aware regression, exact FAST/direct-map equivalence, finite always-write inventory, root-level inference and the approved budget are explicit. The simpler memory may win; arbitrary recurrent plasticity and D-H2/D-H3 remain untested. The numerical manifest was frozen before any D fit. Ticket validator: 86 tickets passed. No positive scientific claim follows.
