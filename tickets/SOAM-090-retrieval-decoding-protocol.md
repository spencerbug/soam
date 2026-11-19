---
schema_version: 2
id: "SOAM-090"
title: "Specify and select the fixed retrieval-versus-decoding diagnostic"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-089"]
labels: ["type:decision", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-19"
updated: "2026-11-19"
github_issue: null
decision: "proceed"
---

# SOAM-090: Specify and select the fixed retrieval-versus-decoding diagnostic

## Recommended thinking

**xhigh** — Separate acquired-code fidelity from ordinary cue completion without leaking evaluator identity or rewriting a failed gate.

## Problem / hypothesis

[D-R1](../reports/STUDY_D_R1_DECISION.md) preserved stored codes in audited checkpoints while ordinary recall failed. Can the fixed decoder use those codes when completion is removed? The [owner selected this diagnostic](../docs/requests/retrieval_diagnostic_2026_11_19.md).

## Scope

Freeze one primary gap, exact-code adequacy guard, fixed PH768/KV/REG-LIFT controls, fresh streams and a finite allocation.

Use [D-R2 v1](../docs/STUDY_D_R2_PROTOCOL.md) and its [manifest](../docs/protocols/study_d_r2_v1.json). Classification: **essential next**.

## Acceptance criteria

- [x] Record owner routing and verify completed evidence dependencies.
- [x] Freeze the protocol, manifest, resource ceiling and stopping rule before fitting.
- [x] Review diagnostic identifiability, privileged-data boundaries and inference precision; record proceed/revise/stop.

## Metrics / evidence

Exact acquired-code minus cue-only canonical accuracy, adjusted exact-code adequacy, minimum free-coordinate code discrepancy, decoded NMSE, free-rollout errors, KV/REG-LIFT references, ten independent roots and one prescribed repeat. Fresh 900 CPU / 1,800 execution-wall seconds, 2 GiB RSS, 1 GiB artifacts, 12 fit attempts. Numerical findings belong in reports/STUDY_D_R2.md.

## Dependencies

- [SOAM-089](SOAM-089-recurrent-retrieval-decision.md) — required done; decision prerequisites require proceed.

## Branch conditions

The November 19 request selects only this diagnostic. SOAM-089 proceed accepts scoped negative evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. No E0, D3/D4, learned organization, coupling or later branch is activated.

## Completion record

Started November 19. Read current priorities, historical contracts, D-R1 report/decision and relevant source. Pre-change full suite: 318 passed (`uv run pytest`, 17.33 seconds); north-star documentation committed as `4d0d128`. Protocol review is in progress.

**Proceed:** primary review accepts the fixed protocol and conservative allocation under the November 19 instruction. Exact codes and true association identity are evaluator-only; all acquired snapshots are scored equally, and no oracle score selects a code or updates the model. This diagnoses the cue-to-output path without isolating basin geometry, clamps or aliasing. The two-quantity adjusted family, width rule, no-tuning schedule, independent roots and resource stop are frozen before fitting.

Read-only little-coder review `c68d445e826548e6976686635d622764` checked counts, decisions and information boundaries. Primary review verified its findings against the files; clarified that PH768 names the PH-FULL arm and explicitly recorded inherited generator namespace and training counts. No worker action was proposed or executed. `uv run python scripts/check_tickets.py` validated all 94 tickets before acceptance. This proceed accepts a test, not a positive mechanism claim.
