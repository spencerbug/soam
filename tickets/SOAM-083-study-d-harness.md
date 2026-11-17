---
schema_version: 2
id: "SOAM-083"
title: "Implement and verify bounded persistent memory controls"
type: "engineering"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-082"]
labels: ["type:engineering", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-17"
updated: "2026-11-17"
github_issue: null
decision: null
---

# SOAM-083: Implement and verify bounded persistent memory controls

## Recommended thinking

**high** — Separate persistent acquisition from transient recall, evaluate strong simpler controls, and preserve information/resource parity.

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

- [SOAM-082](SOAM-082-study-d-protocol.md) — completed prerequisite; decision requires proceed.

## Branch conditions

The November 17 owner request selects this fresh fork; the superseded SOAM-059 selection is not reused. SOAM-082 must accept the protocol before implementation; SOAM-083 must verify invariants and fixture feasibility before development/confirmation. SOAM-052 stays stop. No downstream integration or D3/D4 branch is activated by completion.

## Completion record

SOAM-082 is done/proceed; implementation started after 285 baseline tests passed.

Completed source `2270743`: observation-only interfaces, fixed learned recurrent core, NOWRITE/KV/REG/FAST, D1/D2 evaluator, finite phase runner, independent reduction, snapshots and report renderer. Baseline 285 tests passed before edits; full implementation suite 303 passed in 26.83s, including 18 D invariants. Ruff and 86-ticket validation passed. Full-inventory root-30011 fixture completed all four candidates in 2.25 CPU seconds; projected remaining allocation with 2x margin 106.44 CPU seconds and 385234896 bytes. RSS 293404672 bytes. See `runs/study-d-v1/fixture/projection.json`, source snapshot, individual result/fit records and ledger. Core probe error 2.51e-16; inputs identical across candidates, source frozen before fixture. FAST sequential interference is preserved as a fixture observation, not a confirmation claim or validity failure. Development may proceed without changing settings or guards.
