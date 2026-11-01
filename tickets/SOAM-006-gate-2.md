---
schema_version: 2
id: "SOAM-006"
title: "Gate 2: decide whether local acquisition is viable"
type: "decision"
status: "backlog"
priority: "P2"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2"]
depends_on: ["SOAM-004", "SOAM-005"]
labels: ["type:decision", "priority:P2", "milestone:M2"]
assignees: []
created: "2026-10-25"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-006: Gate 2: decide whether local acquisition is viable

## Recommended thinking

**high** — Judge local acquisition against retention and stability evidence before opening scope learning.

## Problem / hypothesis

Downstream scoping and consolidation should start from a writer with demonstrated usefulness or an explicitly justified trade-off.

Specification: [research plan §9, §19](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

Under the [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md), this remains a bounded historical low-rank acquisition branch, not the next primary task or a prerequisite for cue-driven handover. Preserve Gate 1 checkpoints, plastic-tensor limits, and the existing rule comparisons. Its results do not establish multi-circuit learning; SOAM-039–041 cover that later contract and empirical gate.

### Bounded work

- Compare acquisition, retention, and stability across writer baselines.
- Select a reference writer or revise the representation if associative writes fail.

## Acceptance criteria

- [ ] State whether local writes improve held-out new predictions within the predefined observation budget.
- [ ] Include multistep and old-context evidence; a one-step-only improvement cannot establish viability.
- [ ] Record proceed/revise/stop with the selected rule, frozen parameters, and known trade-offs against online gradients.
- [ ] If no tested writer is viable, preserve the negative result and create a representation-revision ticket instead of advancing automatically.

## Metrics / evidence

Gate 2 evidence matrix covering acquisition, retention, update cost, and recurrent stability.

## Dependencies

- [SOAM-004](SOAM-004-online-writer-baselines.md) — Benchmark online transition correction and changed dynamics
- [SOAM-005](SOAM-005-interference-metrics.md) — Measure interference and learning without resets

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
Set frontmatter `decision` to `proceed`, `revise`, or `stop` only when the decision is documented.
