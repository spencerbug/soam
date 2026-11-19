---
schema_version: 2
id: "SOAM-091"
title: "Implement and verify the evaluator-only decoding diagnostic"
type: "engineering"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-090"]
labels: ["type:engineering", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-19"
updated: "2026-11-19"
github_issue: null
decision: null
---

# SOAM-091: Implement and verify the evaluator-only decoding diagnostic

## Recommended thinking

**high** — Preserve historical model code while enforcing no-write inference, independent diagnostic scoring and reproducible archives.

## Problem / hypothesis

[D-R1](../reports/STUDY_D_R1_DECISION.md) preserved stored codes in audited checkpoints while ordinary recall failed. Can the fixed decoder use those codes when completion is removed? The [owner selected this diagnostic](../docs/requests/retrieval_diagnostic_2026_11_19.md).

## Scope

Implement only the frozen D-R2 evaluator, resource/source checks and scientific invariant tests.

Use [D-R2 v1](../docs/STUDY_D_R2_PROTOCOL.md) and its [manifest](../docs/protocols/study_d_r2_v1.json). Classification: **essential next**.

## Acceptance criteria

- [x] Reuse unchanged PH768, KV and REG-LIFT models and record all resources.
- [x] Verify target isolation, reset/no-write, code scoring, source identity and deterministic repeat.
- [x] Run relevant tests and the required full suite; record actual outcomes.

## Metrics / evidence

Exact acquired-code minus cue-only canonical accuracy, adjusted exact-code adequacy, minimum free-coordinate code discrepancy, decoded NMSE, free-rollout errors, KV/REG-LIFT references, ten independent roots and one prescribed repeat. Fresh 900 CPU / 1,800 execution-wall seconds, 2 GiB RSS, 1 GiB artifacts, 12 fit attempts. Numerical findings belong in reports/STUDY_D_R2.md.

## Dependencies

- [SOAM-090](SOAM-090-retrieval-decoding-protocol.md) — required done; decision prerequisites require proceed.

## Branch conditions

The November 19 request selects only this diagnostic. SOAM-089 proceed accepts scoped negative evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. No E0, D3/D4, learned organization, coupling or later branch is activated.

## Completion record

Started after SOAM-090 completed with proceed. Baseline full suite passed 318 tests. Reuse historical model code unchanged; add the isolated evaluator and scientific invariants.

Completed the isolated evaluator in `soam/decoding/` and ten scientific tests in `tests/test_decoding.py`. Historical retrieval/acquisition modules are unchanged. Ordinary inference receives only memory, masked cue and actions; exact-code diagnostics take copied evaluator arrays and no model reference. Each acquired snapshot is scored equally. All four final sequence projectors and full raw arrays are archived per root. Resource limits, source freeze, finite schedule, failure receipts and an independent reduction/repeat audit are implemented.

Validation: `uv run pytest tests/test_decoding.py tests/test_retrieval.py` — 25 passed; `uv run pytest` — 328 passed in 24.41 seconds; `uv run ruff check soam tests scripts` and `git diff --check` passed; ticket validator passed 94 tickets and two templates. Existing Torch JIT deprecation warning retained.

Worker extraction `cf1d5d4beda549529dd89d83a3d4e138` omitted existing tests; primary review checked the actual encoder/projector/reset/no-write/hidden-mask tests directly. Harness review `82385fa538a949d0b740e0711eb906ec` aborted after contradictory partial summaries; no unverified approval claim was accepted, no action was proposed, and primary review completed the exact code/test inspection. The numerical fixture belongs to SOAM-092 and has not run at this completion point.
