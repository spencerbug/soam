---
schema_version: 2
id: "SOAM-022"
title: "Gate 6: review sensory grounding and belief recovery"
type: "decision"
status: "backlog"
priority: "P2"
recommended_thinking: "high"
milestone: "M6"
work_packages: ["WP-10"]
hypotheses: ["H6"]
depends_on: ["SOAM-021"]
labels: ["type:decision", "priority:P2", "milestone:M6"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-022: Gate 6: review sensory grounding and belief recovery

## Recommended thinking

**high** — Assess grounded recovery against appropriate memory ablations and remaining observability limitations.

## Problem / hypothesis

Planning requires internal predictions that external observations can reliably cue and correct.

Specification: [research plan §13, §19](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Review full, missing, noisy, and ambiguous sensory conditions.
- Choose the observation/belief model suitable for action-search experiments.

## Acceptance criteria

- [ ] Compare grounded recovery with a matched recurrent model lacking the proposed memory mechanisms.
- [ ] Record failure cases where uncertainty collapses or grounding is insufficient for control.
- [ ] Record proceed/revise/stop and define supported observation/action conditions.
- [ ] Keep privileged simulator state confined to evaluator/known goal cost interfaces explicitly documented for planning.

## Metrics / evidence

Gate 6 grounding, partial-recovery, and uncertainty evidence.

## Dependencies

- [SOAM-021](SOAM-021-partial-belief-recovery.md) — Evaluate partial observations, ambiguity, and context recovery

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
Set frontmatter `decision` to `proceed`, `revise`, or `stop` only when the decision is documented.
