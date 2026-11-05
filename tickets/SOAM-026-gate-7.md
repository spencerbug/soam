---
schema_version: 2
id: "SOAM-026"
title: "Gate 7: assess planning benefit and safe memory separation"
type: "decision"
status: "backlog"
priority: "P1"
recommended_thinking: "high"
milestone: "M7"
work_packages: ["WP-11", "WP-12"]
hypotheses: ["H7"]
depends_on: ["SOAM-024", "SOAM-038"]
labels: ["type:decision", "priority:P1", "milestone:M7"]
assignees: []
created: "2026-10-25"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-026: Gate 7: assess planning benefit and safe memory separation

## Recommended thinking

**high** — Judge realized planning benefit and verify that imagined trajectories never write persistent memory.

## Problem / hypothesis

Useful imagined trajectories must improve real action selection without quietly writing imagined experience into persistent memory.

Specification: [research plan §14, §19](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.3 shared-population revision — 2026-11-05

Review the shared-population control and skill results with explicit cross-function interference and actual/desired-state audits. Successful motor routing alone cannot establish attractor-mediated control or useful neuronal sharing.

The [v0.3 scope](../docs/RESEARCH_SPEC_V0_3.md) governs current topology and
platform use; earlier scope notes below retain dependency history only.

### Historical v0.2 scope revision — 2026-11-01

The [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md) replaces mandatory learned-proposal training with the associative skill comparison. Review simple search and skill reuse; include learned proposals only if available. Negative skill-transfer results must remain explicit and constrain any proceed to the validated control behavior.

### Bounded work

- Review reactive/search/associative-skill comparisons, available learned proposals, and changed-dynamics recovery.
- Audit persistent-weight and evidence-buffer separation during planning.

## Acceptance criteria

- [ ] State whether shared activity causally contributes to control and whether motor authority/no-write invariants survive the prescribed overlap and action ablations.

- [ ] Require improved realized goal completion under the predefined comparisons and reported compute budgets.
- [ ] Document evidence that model quality predicts control quality and identify failure conditions.
- [ ] Verify no persistent-memory writes occur during candidate simulation.
- [ ] Record proceed/revise/stop and define the planning component selected for continual integration.

## Metrics / evidence

Gate 7 success, replanning, resource, and no-write-inference evidence.

## Dependencies

- [SOAM-024](SOAM-024-planning-benchmark.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-038](SOAM-038-associative-skill-transfer.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Future capability** (R5/R9/R10) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Retain as the richer integration/concurrency/control path with existing empirical prerequisites. E3 is a smaller independent supplied-policy test and does not pass this ticket or its gate. No human-like intelligence claim follows from completed components.

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
Set frontmatter `decision` to `proceed`, `revise`, or `stop` only when the decision is documented.
