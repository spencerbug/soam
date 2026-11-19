---
schema_version: 2
id: "SOAM-092"
title: "Execute the fixed retrieval-versus-decoding diagnostic"
type: "experiment"
status: "done"
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

- [x] Freeze source and confirm fixture-based feasibility before confirmation.
- [x] Account for all 12 planned fits, all arms, failures, source/data exposure and resources.
- [x] Report adjusted primary/guard intervals, code discrepancies, references and exact reproduction.

## Metrics / evidence

Exact acquired-code minus cue-only canonical accuracy, adjusted exact-code adequacy, minimum free-coordinate code discrepancy, decoded NMSE, free-rollout errors, KV/REG-LIFT references, ten independent roots and one prescribed repeat. Fresh 900 CPU / 1,800 execution-wall seconds, 2 GiB RSS, 1 GiB artifacts, 12 fit attempts. Numerical findings belong in reports/STUDY_D_R2.md.

## Dependencies

- [SOAM-090](SOAM-090-retrieval-decoding-protocol.md) — required done; decision prerequisites require proceed.
- [SOAM-091](SOAM-091-retrieval-decoding-harness.md) — required done; decision prerequisites require proceed.

## Branch conditions

The November 19 request selects only this diagnostic. SOAM-089 proceed accepts scoped negative evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. No E0, D3/D4, learned organization, coupling or later branch is activated.

## Completion record

Started after SOAM-090 done/proceed and SOAM-091 done. Source will be committed before the fixed fixture; confirmation requires fixture feasibility. All 328 tests pass.

Completed all frozen phases with `uv run python -m soam.decoding.runner fixture`, `confirmation`, `repeat`, and `report`. All 12 planned core fits and 36 model-by-root evaluations completed; no failed attempts, exclusions, retries, added roots or tuning. The [report](../reports/STUDY_D_R2.md), [statistics](../reports/study-d-r2/statistics.json), [verification](../reports/study-d-r2/verification.json), and [resources](../reports/study-d-r2/resource-final.json) record all evidence.

Result: precision-qualified **inconclusive**. Exact-code accuracy 1.0; PH768 .776339; paired gap .223661 [.153571,.290179], width .136607 exceeds the frozen .10 cap. All 40 final projectors preserve their acquired codes, residual <=3.94e-14. KV 1.0 and REG-LIFT .960714 are descriptive references. All 87 repeated arrays and 42 checkpoint tensors match exactly; independent reduction verifies 210 metrics and all acquired codes; all 110 historical source hashes match.

Source commit `924acd8c3f32af9abfbd77ff69f8bab3030b01cb`, fingerprint `0df3abe0ec7906dea1d1978280709f99f3111b2c06fff066d759559ad3fba577`; CPU float64 deterministic Torch with one intra-op/inter-op thread. Fixture root 50011; confirmation roots 53003,53009,53027,53029,53051,53057,53059,53063,53069,53077; repeat 53003, all in fresh namespace. Per fit 2,048 training transitions; per root 256 grounded acquisition snapshots and 224 earlier-object query cues, no replay. All settings/configuration/software versions and per-arm costs are archived.

Numerical use before closeout: 26.703657 CPU / 26.829175 execution-wall seconds; peak RSS 366,903,296 B; 348,491,815 bytes before the final receipt. Fixture projection passed before confirmation. The 328-test full suite, Ruff and ticket validation passed before execution. The figure was visually checked after reporting. No code or criterion changed after the source freeze.
