---
schema_version: 2
id: "SOAM-007"
title: "Compare unfiltered, sparse, random, and sensitivity-based scopes"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "high"
milestone: "M3"
work_packages: ["WP-04"]
hypotheses: ["H3"]
depends_on: ["SOAM-006"]
labels: ["type:experiment", "priority:P2", "milestone:M3"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-007: Compare unfiltered, sparse, random, and sensitivity-based scopes

## Recommended thinking

**high** — Design comparable masks and sensitivity controls while separating localization from task isolation.

## Problem / hypothesis

Before learning a translator, establish whether simple scope filters reduce interference at comparable adaptation performance.

Specification: [research plan §10, §16](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

Under the [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md), this is a conditional scoping branch attached to the historical acquisition study. It does not gate early handover, belief tracking, or control. Relate interference/sharing results to evidence responsibility and generic-versus-instance credit, but do not assume that a context mask solves multi-circuit credit assignment. Application to a different plastic representation requires a separately specified comparison. Learned scopes are candidates, not a mandatory architecture component.

### Bounded work

- Apply unfiltered, fixed sparse, random sparse, and sensitivity-based masks to the same reference writer.
- Introduce isolated context-specific corrections and evaluate every protected context.

## Acceptance criteria

- [ ] Match update sparsity/rank where applicable and report mask-estimation compute.
- [ ] Compare retention at matched new-task accuracy, not merely equal learning rate or iteration count.
- [ ] Fit sensitivity statistics only from allowed training/evidence data.
- [ ] Report adaptation-retention curves and failures across multiple seeds.

## Metrics / evidence

Old-task error increase at matched new-task error, speed of adaptation, sparsity/rank, mask cost, and rollout stability.

## Dependencies

- [SOAM-006](SOAM-006-gate-2.md) — Gate 2: decide whether local acquisition is viable

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
