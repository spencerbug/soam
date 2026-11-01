---
schema_version: 2
id: "SOAM-011"
title: "Implement a bounded grounded evidence buffer and replay baseline"
type: "engineering"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M4"
work_packages: ["WP-06"]
hypotheses: ["H4"]
depends_on: ["SOAM-044"]
labels: ["type:engineering", "priority:P1", "milestone:M4"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-011: Implement a bounded grounded evidence buffer and replay baseline

## Recommended thinking

**high** — Implement evidence and replay across the selected circuit/instance write contract while preserving validation and provenance boundaries.

## Problem / hypothesis

Grounded learning needs a bounded record of real experience and a simple replay baseline. Evidence storage must remain distinct from predictive state and persistent instance facts.

Specification: [research plan §4, §11, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

The [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md) replaces the dependency on the historical writer gate with SOAM-044, which implements the multi-circuit contract selected by SOAM-039. This ticket supplies a simple replay reference before complex consolidation; it does not require a learned consolidator.

### Bounded work

- Store actual encoded observations, actions, context, outcomes, and provenance under a fixed byte/entry budget.
- Implement recent/representative replay using the contract selected in SOAM-039; reuse existing writer transactions only where their assumptions hold.

## Acceptance criteria

- [ ] Exclude imagined transitions from grounded evidence unless separately labeled and never treated as truth.
- [ ] Document sampling/eviction and evidence reliability; keep final evaluation records separate.
- [ ] Compare no consolidation and replay with matched observations and reported additional update compute.
- [ ] Test provenance, capacity limits, deterministic sampling, and replay’s retention/multistep effects.

## Metrics / evidence

Buffer bytes, coverage, replay iterations/time, acquisition retention, and free-rollout error.

## Dependencies

- [SOAM-044](SOAM-044-multicircuit-write-contract.md) — implemented and tested multi-circuit writer; the upstream design decision must proceed.

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
