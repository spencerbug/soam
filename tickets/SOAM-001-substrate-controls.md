---
schema_version: 2
id: "SOAM-001"
title: "Strengthen substrate controls and budget comparisons"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1"]
depends_on: ["SOAM-000"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-001: Strengthen substrate controls and budget comparisons

## Recommended thinking

**high** — Design fair capacity controls and unseen-switch evaluations without leaking test evidence into tuning.

## Problem / hypothesis

The current screen passes, but separate cores share sensory interfaces, context variants have unequal parameter counts, and switch timing is regular. These gaps limit the case for proceeding to plasticity.

Specification: [research plan §8, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Compare the additive reference with a conventional GRU, fully independent per-context predictors, and budget-matched shared variants.
- Test unseen switch schedules, held-out action paths, and perturbation responses at multiple horizons; retain the original benchmark.

## Acceptance criteria

- [x] Freeze development/test streams, parameter tolerances, compute accounting, and readiness criteria before running the new comparison.
- [x] Report total parameters, exposure, runtime, and the switching semantics of each baseline; disclose any required sensory reset for independent predictors.
- [x] Run multiple fixed seeds and report per-context, per-horizon, switching, motion-collapse, and perturbation metrics.
- [x] Publish negative results and identify which claims about shared structure remain untested; do not tune on the original test set.

## Metrics / evidence

One-step/free NMSE, switch recovery, long-horizon drift, invalid rates, paired perturbation gaps, motion energy, parameter bytes and runtime.

## Dependencies

- [SOAM-000](SOAM-000-substrate-baseline.md) — Record the reproducible substrate baseline

## Completion record

Completed 2026-10-25. [Report](../reports/SUBSTRATE_CONTROLS.md),
[protocol](../docs/SUBSTRATE_CONTROLS.md), [resolved config](../reports/substrate-controls/config.json),
[provenance](../reports/substrate-controls/provenance.json),
[results](../reports/substrate-controls/results.json), and
[exact reproduction](../reports/substrate-controls/reproducibility.json).

Source commit: `7238e6ce69ce5a4e561960b290a2222e5e16aeb5`; source fingerprint:
`6c0ae5c4344472957ab472298751be9348de55863012ae9f8ce2045df20af269`.
Six variants × seeds 11, 23, 47: 18/18 completed. Six seed-11 repeats match metrics,
checkpoint weights, and saved trajectories exactly (timings excluded).

**Mixed result:** 17/18 pass the preregistered screen; additive seed 23 fails irregular
accuracy (.2527 > .25). Thresholds were not changed. Long-horizon drift remains;
shared structure/reuse is not established. Independent models use predicted-feature
handoffs at switches, disclosed in the report. Raw output used 1.37 GB, above the
initial 1 GB estimate; original plus repeat runs took 228.14 seconds.

Validation: `uv run pytest` — 15 passed before changes, 27 afterward;
`uv run ruff check soam tests scripts` and `uv run python scripts/check_tickets.py` passed.
Six-variant smoke completed. Full run/repeat/reproduction and report commands are
recorded in the linked protocol/report. Cache environment overrides used writable
temporary paths. The report includes negative results, per-context/horizon metrics,
compute/storage accounting, switching semantics, and limitations.

This completes the experiment and makes SOAM-002 eligible; it does not decide Gate 1
or permit downstream writing before that decision is complete with `proceed`.
