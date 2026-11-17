---
schema_version: 2
id: "SOAM-085"
title: "Review persistent memory benefit and cheapest reliable mechanism"
type: "decision"
status: "backlog"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-084"]
labels: ["type:decision", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-17"
updated: "2026-11-17"
github_issue: null
decision: null
---

# SOAM-085: Review persistent memory benefit and cheapest reliable mechanism

## Recommended thinking

**xhigh** — Separate persistent acquisition from transient recall, evaluate strong simpler controls, and preserve information/resource parity.

## Problem / hypothesis

Does bounded grounded experience yield post-reset object knowledge and retention, and does one rank-one fast operator improve on explicit memory and online regression?

## Scope

Follow the [owner selection](../docs/requests/study_d_2026_11_17.md) and [D v1 protocol](../docs/STUDY_D_PROTOCOL.md). D0–D2 only; D3/D4, learned write gates, replay and integration are deferred.

## Acceptance criteria

- [ ] Complete this bounded phase with evidence or documented negative/inconclusive/invalid outcome.
- [ ] Verify reset, no-write inference, evidence parity, source identity and resource limits.
- [ ] Preserve every mandatory comparator, independent-root uncertainty and historical outcome.
- [ ] Record actual checks, artifacts and implications for the next ticket.

## Metrics / evidence

Post-reset canonical/free prediction, one/few-shot curves, sequential retention, unknown rejection, resource costs and exact repeat. The versioned protocol/manifest owns frozen criteria.

## Dependencies

- [SOAM-084](SOAM-084-study-d-experiment.md) — completed prerequisite; decision requires proceed.

## Branch conditions

The November 17 owner request selects this fresh fork; the superseded SOAM-059 selection is not reused. SOAM-082 must accept the protocol before implementation; SOAM-083 must verify invariants and fixture feasibility before development/confirmation. SOAM-052 stays stop. No downstream integration or D3/D4 branch is activated by completion.

## Completion record

Not started.
