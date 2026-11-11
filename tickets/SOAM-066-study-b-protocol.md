---
schema_version: 2
id: "SOAM-066"
title: "Specify and select temporal sensory assimilation"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-047", "SOAM-064", "SOAM-065"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-11"
github_issue: null
decision: "proceed"
---

# SOAM-066: Specify and select temporal sensory assimilation

## Recommended thinking

**xhigh** — Separate sensory timing, state correction and internal computation while preserving information parity, scientific invariants and independent-root inference.

## Problem / hypothesis

The owner selects Study B after completed Study A. Ordinary R32 is competent but temporal assimilation remains untested. Historical SOAM-052 remains stop. See the [protocol](../docs/STUDY_B_PROTOCOL.md).

## Scope

Specify and select temporal sensory assimilation. Only this bounded study is selected; no acquisition, attention, integration, or online parameter updates.

## Acceptance criteria

- [x] Complete this phase with checkable source, protocol, tests or measured evidence.
- [x] Preserve information parity and historical negative results; report supported, negative, inconclusive, or invalid outcomes without post-confirmation changes.
- [x] Record resources, limitations, and implications for the next interface.

## Metrics / evidence

Pre-correction NMSE, correction/settling errors, free horizons, corruption/change guardrails, update/MAC/state/parameter accounting and paired-root intervals. Owner-approved ceiling: 7200 CPU seconds, 14400 execution wall seconds, 2 GiB peak RSS and 2 GiB artifacts.

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — completed evidence or proceed decision.
- [SOAM-064](SOAM-064-study-a-experiment.md) — completed evidence or proceed decision.
- [SOAM-065](SOAM-065-study-a-decision.md) — completed evidence or proceed decision.

## Branch conditions

The November 11 owner request is the fresh named selection. SOAM-066 owns the protocol/RFC and routing. Protocol proceed precedes implementation; verified implementation and immutable development-informed selections precede confirmation. The failed sharing gate is not a dependency and is not changed.

## Completion record

Protocol/RFC review complete. The owner request selects this single fork, with the explicitly accepted 7200 CPU / 14400 wall second ceiling. Verified SOAM-047/065 proceed and SOAM-064 complete. Primary endpoints, guards, seeds, candidate inventory, tuning, stopping and information boundaries are defined before fitting. Ordinary RNN replaces the copied GRU requirement per the owner override; historical comparisons are preserved. Baseline uv run pytest: 215 passed in 20.38s. Qwen bulk extraction returned invalid empty findings and was rejected; direct source review supplied verification. Proceed accepts the experimental test, not its hypothesis.
