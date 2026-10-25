---
schema_version: 1
id: "SOAM-026"
title: "Gate 7: assess planning benefit and safe memory separation"
type: "decision"
status: "backlog"
priority: "P2"
milestone: "M7"
work_packages: ["WP-11", "WP-12"]
hypotheses: ["H7"]
depends_on: ["SOAM-024", "SOAM-025"]
labels: ["type:decision", "priority:P2", "milestone:M7"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-026: Gate 7: assess planning benefit and safe memory separation

## Problem / hypothesis

Useful imagined trajectories must improve real action selection without quietly writing imagined experience into persistent memory.

Specification: [research plan §14, §19](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Review reactive/search/learned-proposal comparisons and changed-dynamics recovery.
- Audit persistent-weight and evidence-buffer separation during planning.

## Acceptance criteria

- [ ] Require improved realized goal completion under the predefined comparisons and reported compute budgets.
- [ ] Document evidence that model quality predicts control quality and identify failure conditions.
- [ ] Verify no persistent-memory writes occur during candidate simulation.
- [ ] Record proceed/revise/stop and define the planning component selected for continual integration.

## Metrics / evidence

Gate 7 success, replanning, resource, and no-write-inference evidence.

## Dependencies

- [SOAM-024](SOAM-024-planning-benchmark.md) — Benchmark navigation, changed dynamics, and planning horizons
- [SOAM-025](SOAM-025-action-proposals.md) — Learn goal-conditioned action proposals after search is reliable

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
Set frontmatter `decision` to `proceed`, `revise`, or `stop` only when the decision is documented.
