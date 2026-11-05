---
schema_version: 2
id: "SOAM-034"
title: "Implement the bounded concurrent-attractor handover harness"
type: "engineering"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-00", "WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-033"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-034: Implement the bounded concurrent-attractor handover harness

## Recommended thinking

**high** — Implement independent live state, cue pathways, and reproducible controls without encoding the desired result in the scheduler.

## Problem / hypothesis

Existing recurrence and switching baselines do not expose independently calibrated candidates or distinguish a bank swap from cue-driven attraction.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Implementation contract: [handover protocol v1](../docs/HANDOVER_PROTOCOL.md) and
[numerical manifest](../docs/protocols/handover_v1.json), completed by SOAM-033.
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Implement only the topology/candidate matrix selected by the handover protocol; adapt existing baselines without changing historical configurations.
- Expose independent live states, graded cue activity, role/scheduling traces, sensorimotor correction, and persistent-state fingerprints.
- Instrument state copies, resets, parameter tying/cloning, peak concurrency, history replay, and all per-step/model-call costs.

## Acceptance criteria

- [x] Implement explicit attractor and ordinary recurrent candidates plus the selected population-separation controls.
- [x] Test candidate-state isolation, repeated role swaps, sensor/action timing, evaluator-only truth, deterministic seeds, and no persistent writes during handover or imagined rollouts.
- [x] Provide a smoke run for all prescribed controls and an artifact schema recording cues, roles, calibration, handovers, and resource costs; smoke success is not scientific evidence.
- [x] Run the baseline test suite before code edits, relevant tests afterwards, and ticket validation; record exact outcomes and implementation limitations.

## Metrics / evidence

Engineering report plus smoke config/source fingerprints and reproducibility checks. Full confirmation trials belong to the next experiment, not this harness ticket.

## Dependencies

- [SOAM-033](SOAM-033-handover-protocol.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Completed 2026-11-01. Delivered the isolated `soam.handover` package, fixture CLI,
five candidate layouts, history/intervention/probe controls, observed-only fitting
primitives, and [artifact schema](../docs/HANDOVER_HARNESS.md).
See the [engineering report](../reports/HANDOVER_HARNESS.md) for actual commands,
initialization/scheduling details, coverage, limitations, and retained negative results.

Baseline `UV_CACHE_DIR=/tmp/soam-uv-cache uv run pytest`: 48 passed before code edits.
Final same command: 86 passed, including 38 new handover cases. Ruff passed;
`UV_CACHE_DIR=/tmp/soam-uv-cache uv run python scripts/check_tickets.py` validated
46 tickets; `git diff --check` passed.

`uv run soam-handover-smoke` with the recorded cache override completed all 62
cells and 30 fixture probe evaluations in `runs/handover-fixture-v3`. The same CLI
with `--repeat-from` completed `runs/handover-fixture-v3-repeat` and matched 1,239
arrays in 72 NPZ files plus deterministic records exactly. Compact
[coverage](../reports/handover-harness/coverage.json),
[reproduction](../reports/handover-harness/reproducibility.json), and
[source/configuration provenance](../reports/handover-harness/provenance.json) are retained.

Source commit `6ed54ae4fa28eea52b858bef2a9f916ec7c04b6a` plus dirty working-tree
fingerprint `194e9b5478fcfada2e66dc6ded1b2f62f463b1a2eea110871ee8ad1a5f7738e0`;
fixture seed 11, split 3, one paired base episode index. GRU smoke weights remain
unfitted; mocked optimizer unit tests do not generate measured training data.
The Qwen review timed out without output; direct review/tests supplied the fallback.
No development or confirmation data were generated and no scientific gate passed.
SOAM-035 is ready; SOAM-036 remains backlog.
