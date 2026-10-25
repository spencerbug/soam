---
schema_version: 2
id: "SOAM-011"
title: "Implement a bounded grounded evidence buffer and replay baseline"
type: "engineering"
status: "backlog"
priority: "P1"
recommended_thinking: "medium"
milestone: "M4"
work_packages: ["WP-06"]
hypotheses: ["H4"]
depends_on: ["SOAM-006"]
labels: ["type:engineering", "priority:P1", "milestone:M4"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-011: Implement a bounded grounded evidence buffer and replay baseline

## Recommended thinking

**medium** — Implement bounded evidence storage and conventional replay using the established writer contract.

## Problem / hypothesis

A learned consolidator needs a simple replay baseline and a bounded record of real experience that is not a second persistent world model.

Specification: [research plan §4, §11, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Store actual encoded observations, actions, context, outcomes, and provenance under a fixed byte/entry budget.
- Implement recent/representative replay using the existing corrective writer.

## Acceptance criteria

- [ ] Exclude imagined transitions from grounded evidence unless separately labeled and never treated as truth.
- [ ] Document sampling/eviction and evidence reliability; keep final evaluation records separate.
- [ ] Compare no consolidation and replay with matched observations and reported additional update compute.
- [ ] Test provenance, capacity limits, deterministic sampling, and replay’s retention/multistep effects.

## Metrics / evidence

Buffer bytes, coverage, replay iterations/time, acquisition retention, and free-rollout error.

## Dependencies

- [SOAM-006](SOAM-006-gate-2.md) — Gate 2: decide whether local acquisition is viable

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
