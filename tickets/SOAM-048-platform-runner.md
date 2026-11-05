---
schema_version: 2
id: "SOAM-048"
title: "Implement the reusable recurrent-dynamics experiment runner"
type: "engineering"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M0"
work_packages: ["WP-00"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-047"]
labels: ["type:engineering", "priority:P0", "milestone:M0"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-048: Implement the reusable recurrent-dynamics experiment runner

## Recommended thinking

**high** — Implement reproducibility and ownership contracts across distinct task/backend combinations while protecting existing experiment paths.

## Problem / hypothesis

A reusable runner should execute multiple recurrent experiments without copying orchestration or forcing them into the handover-specific model.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Implement the [v1 platform contract](../docs/RECURRENT_PLATFORM_CONTRACT.md): configuration-driven task/backend selection, supplied-only leaky and linear fixtures, and rejection of fitting/online-write requests. No general learning-policy plugin layer.
- Provide deterministic fixtures for recall/transition and one distinct sensorimotor task; reuse existing provenance, snapshot, metrics, and artifact utilities where compatible.
- Implement finite sweep execution, structured failed-run records, resume/overwrite rules, state/parameter/storage/compute accounting, and capability checks. Preserve historical CLIs, protocols, and results.

Use the contract's eight-cell fixture matrix, failure case and repeat under its
combined 60-CPU-second/120-wall-second, 1-GiB-RSS and 256-MiB-artifact ceilings.
No partial-cell resume or automatic retries in v1. SOAM-050 owns scientific backends
and offline fitting after SOAM-049; this runner ticket remains engineering-only.

## Acceptance criteria

- [x] Run uv run pytest before existing code changes; pass relevant invariant tests and the full suite after implementation.
- [x] Execute both fixture tasks through the same runner with at least two compatible backend configurations; demonstrate a small new task/backend registration without editing runner control flow.
- [x] Verify separate random streams, no target leakage, no persistent or live-state writes during prediction, snapshot isolation, and exact same-environment reproduction excluding timing.
- [x] Archive fixture configs, seeds, source/version fingerprints, resource counts, actual commands, failure-path checks, and extension documentation; fixtures do not count as research evidence.

## Metrics / evidence

Delivered [engineering report](../reports/RECURRENT_PLATFORM.md),
[implementation/extension guide](../docs/RECURRENT_PLATFORM_RUNNER.md),
[configuration](../configs/platform-fixture.json) and
[reproduction record](../reports/recurrent-platform/reproduction.json).

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Branch conditions

The first delivery serves only the minimal SOAM-049 recall/transition pilot. Specify extension boundaries but implement no general backend catalogue. A second tiny task fixture checks reuse only; it is not a localization or learning-module study. Expand infrastructure only when a selected fork identifies a concrete missing capability.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R7) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Keep only the runner utilities required by E1 and preserve existing commands. A tiny second fixture may check an actual interface coupling; it must not become a second environment or research study.

## Completion record

Completed 2026-11-05 after committing SOAM-049 as `ce29de0`. Verified SOAM-047
done/proceed and the fixture-only branch conditions; set in_progress before changes.
No assignee handle is known.

Implemented `soam.platform` with observed-only packets, task-owned truth/scoring,
supplied leaky/linear models, explicit transient state, private frozen prediction,
initial perturbation/full-rollout clamp capabilities, and strict failure rejection.
Added the `soam-platform-fixture` entry point and bounded original/repeat orchestration.
Registered-task/backend extension is tested without changing runner control flow.
The historical harness and frozen contracts remain unchanged.

Actual validation:

- `UV_CACHE_DIR=/tmp/soam-uv-cache uv run pytest`: baseline **86 passed in 16.21s**;
  final **110 passed in 14.92s**, including 24 new platform cases.
- `UV_CACHE_DIR=/tmp/soam-uv-cache uv run ruff check soam/platform tests/test_platform.py`
  and corresponding `ruff format --check`: passed.
- `UV_CACHE_DIR=/tmp/soam-uv-cache uv run soam-platform-fixture --output runs/platform-fixture-v1`:
  eight cells plus one expected-invalid case per pass; exact repeat of 137 arrays
  in 33 NPZ files. Combined CPU 0.532955s, wall 0.639720s, peak RSS 282,181,632 bytes,
  artifacts 249,062 bytes, within every declared combined ceiling.
- Artifact audit verified 109 hashes, exact physical artifact-byte total and all
  52 captured source hashes. Compact evidence is linked in the report; full archives
  remain under `runs/platform-fixture-v1/`.
- `UV_CACHE_DIR=/tmp/soam-uv-cache uv run python scripts/check_tickets.py` and
  `git diff --check`: passed. Historical preservation and local-link audits passed.

Source base `ce29de0deb59a1804d4f9c883bb79029792c65cd`, dirty implementation fingerprint
`d0ce56276aaa715aa217106cec320519660b154a4e5e1680d1076bdf44e213b9`.
Fixture root 9001, indices 0/1, projection 1729; CPU float32/float64 metrics,
Python 3.12.13, Torch 2.14.1, NumPy 2.5.4, one thread and deterministic operations.
The worker was busy; direct implementation/testing was used without worker changes.
The editable entry point was refreshed with authorized `uv sync --extra dev --locked`.

SOAM-050 is now ready because both required decisions/engineering dependencies and
body conditions are satisfied. It has not started. No fitting, study split, H1
claim, application fork, publication or remote issue update occurred in SOAM-048.
