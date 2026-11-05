---
schema_version: 2
id: "SOAM-033"
title: "Specify cue-driven handover and circuit-layout controls"
type: "research"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-032"]
labels: ["type:research", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-033: Specify cue-driven handover and circuit-layout controls

## Recommended thinking

**xhigh** — Separate attractor recruitment from scripted routing and choose a bounded topology comparison before coding.

## Problem / hypothesis

The first v0.2 question is whether attended, tracking, and primed roles support cue-driven handover with grounded continuity. Prediction is a minimum usefulness check, not the main optimization target.

Specification: [SOAM v0.2](../docs/RESEARCH_SPEC_V0_2.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Specify a small synthetic sensorimotor task, fixed projection, declared cues, and fixed persistent weights during measured trials.
- Compare an explicit attractor candidate and ordinary recurrent control; choose a bounded shared-population versus separated-state comparison. Evaluate parallel circuits, shared-weight clones, alternating banks, and columns/stacks as design alternatives without requiring all implementations.
- Define circuit/instance interfaces, primed-state cost, cue coupling, calibration, scheduling, and source retention. Review focused primary sources for the chosen attractor mechanism.

## Acceptance criteria

- [x] Publish a protocol with equations, input conditions, scaffold ledger, topology/parameter/state ownership, and testable attraction and switching claims.
- [x] Preregister multiple fixed seeds, train/development/confirmation streams, numeric thresholds, observation/compute budgets, failure handling, and a bounded trial matrix.
- [x] Include pre-tracking, cold start, equal-history reconstruction, cue removal/shuffling, sensory-feedback ablation, single-population control, and labeled oracle correspondence.
- [x] Measure dynamical recruitment separately from explicit selection; define recovery/collapse tests and simple post-switch prediction/continuity checks. Explain what a negative result rules out.

## Metrics / evidence

Artifacts: [handover protocol v1](../docs/HANDOVER_PROTOCOL.md) and
[numerical manifest](../docs/protocols/handover_v1.json). These specify candidate
equations, reviewed sources, numerical settings, metrics, and budgets; they contain
no empirical result.

## Dependencies

- [SOAM-032](SOAM-032-embodied-scope-revision.md) — required completed prerequisite; decision prerequisites must record proceed.

## Completion record

Completed 2026-11-01 against source commit
`6ed54ae4fa28eea52b858bef2a9f916ec7c04b6a`, with the protocol and manifest added in
the working tree. No runtime code, historical experiment configuration, or result
was changed. Artifact SHA-256 fingerprints:

- Protocol: `b0deaca9e98601bb7ba7252f677b1cae5416b5315f6778c8ecf9d6a51dbeb6c9`.
- Manifest: `79875fee3b53bb00c385d6572dfa309e7f359371b449c2266d59261076b79611`.

The protocol defines an engineered key-attractor/ring candidate, a one-state
bottleneck, tied separate-state GRUs, and shared-population GRUs. It freezes the
requested controls, input/state ownership, separate recruitment and output-selection
metrics, and a scaffold ledger. Broader cloning/stack designs remain deferred.
Focused primary-source review and access limits are recorded in protocol §10;
the Ramsauer full PDF was inaccessible, so only its abstract and authors' public
description support that entry. Qwen's focused API extraction omitted the projection
file and supplied unreliable line references; the relevant APIs were checked directly.

Static review used `UV_CACHE_DIR=/tmp/soam-uv-cache uv run python` with inline
assertions: JSON parsing, 62 unique episode cells, complete 0..191 visibility
coverage, distinct split IDs, 9,920 confirmation / 2,480 development episode counts,
and 192 unique probe initial conditions per seed passed. PyTorch module
instantiation verified 3,699 / 7,059 / 3,819 trainable parameters for G2/GS24/GS9.
Hadamard orthogonality and the autonomous energy-gradient identity passed; no
trajectory was simulated. Final review corrected the shared controls to receive
the same supplied action gains as the separate-state control.

`UV_CACHE_DIR=/tmp/soam-uv-cache uv run python scripts/check_tickets.py` passed
for all 45 tickets; local documentation links and `git diff --check` passed.
No pytest run was needed for this documentation/manifest-only task. No model was
fitted and no fixture, development, or confirmation trajectory was evaluated.
Seeds [11,23,47,71,101], stream separation, fixed budgets, and negative-result
handling are preregistered choices, not measured outcomes.

SOAM-034 is now ready to implement and test this contract. SOAM-035/036 remain
backlog. This completion passes no empirical gate and establishes no attractor,
concurrency, learning, or neuroscientific result.
