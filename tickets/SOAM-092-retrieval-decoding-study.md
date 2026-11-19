---
schema_version: 2
id: "SOAM-092"
title: "Execute the fixed retrieval-versus-decoding diagnostic"
type: "experiment"
status: "in_progress"
priority: "P0"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-090", "SOAM-091"]
labels: ["type:experiment", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-19"
updated: "2026-11-19"
github_issue: null
decision: null
---

# SOAM-092: Execute the fixed retrieval-versus-decoding diagnostic

## Recommended thinking

**high** — Execute the frozen schedule, inspect failures and distinguish independent roots from nested queries.

## Problem / hypothesis

[D-R1](../reports/STUDY_D_R1_DECISION.md) preserved stored codes in audited checkpoints while ordinary recall failed. Can the fixed decoder use those codes when completion is removed? The [owner selected this diagnostic](../docs/requests/retrieval_diagnostic_2026_11_19.md).

## Scope

Run one fixture, ten fresh confirmation roots and one prescribed repeat; independently reduce saved evidence.

Use [D-R2 v1](../docs/STUDY_D_R2_PROTOCOL.md) and its [manifest](../docs/protocols/study_d_r2_v1.json). Classification: **essential next**.

## Acceptance criteria

- [ ] Freeze source and confirm fixture-based feasibility before confirmation.
- [ ] Account for all 12 planned fits, all arms, failures, source/data exposure and resources.
- [ ] Report adjusted primary/guard intervals, code discrepancies, references and exact reproduction.

## Metrics / evidence

Exact acquired-code minus cue-only canonical accuracy, adjusted exact-code adequacy, minimum free-coordinate code discrepancy, decoded NMSE, free-rollout errors, KV/REG-LIFT references, ten independent roots and one prescribed repeat. Fresh 900 CPU / 1,800 execution-wall seconds, 2 GiB RSS, 1 GiB artifacts, 12 fit attempts. Numerical findings belong in reports/STUDY_D_R2.md.

## Dependencies

- [SOAM-090](SOAM-090-retrieval-decoding-protocol.md) — required done; decision prerequisites require proceed.
- [SOAM-091](SOAM-091-retrieval-decoding-harness.md) — required done; decision prerequisites require proceed.

## Branch conditions

The November 19 request selects only this diagnostic. SOAM-089 proceed accepts scoped negative evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. No E0, D3/D4, learned organization, coupling or later branch is activated.

## Completion record

Started after SOAM-090 done/proceed and SOAM-091 done. Source will be committed before the fixed fixture; confirmation requires fixture feasibility. All 328 tests pass.
