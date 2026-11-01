---
schema_version: 2
id: "SOAM-025"
title: "Learn goal-conditioned action proposals after search is reliable"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "high"
milestone: "M7"
work_packages: ["WP-12"]
hypotheses: ["H7"]
depends_on: ["SOAM-024"]
labels: ["type:experiment", "priority:P2", "milestone:M7"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-025: Learn goal-conditioned action proposals after search is reliable

## Recommended thinking

**high** — Train action proposals against a reliable search reference without confounding policy and world-model quality.

## Problem / hypothesis

A learned action head is justified only after the predictor/search baseline can solve the controlled task.

Specification: [research plan §14, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

Under the [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md), learned proposal heads remain an optional efficiency study once search is reliable. They are not a prerequisite for the control gate. SOAM-038 addresses content-addressable reusable action dynamics, a distinct claim from learning a proposal distribution.

### Bounded work

- Start with imitation of successful search or a documented bounded policy-learning method.
- Compare learned proposals with uniform/enumerated candidates and preserve known goal costs before considering a learned critic.

## Acceptance criteria

- [ ] Specify search reliability criteria before starting policy training; defer if the preceding benchmark does not meet them.
- [ ] Separate planner-generated training targets from held-out evaluation goals.
- [ ] Compare success at matched candidate/model-call budgets and report policy-training cost.
- [ ] Keep imagined-policy optimization separate from persistent world-memory updates and document any later critic extension as a new ticket.

## Metrics / evidence

Success per candidate/model call, sample efficiency, inference latency, policy cost, and failure rate.

## Dependencies

- [SOAM-024](SOAM-024-planning-benchmark.md) — Benchmark navigation, changed dynamics, and planning horizons

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
