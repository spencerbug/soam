---
schema_version: 1
id: "SOAM-008"
title: "Build shared-scope and noisy-evidence task families"
type: "experiment"
status: "backlog"
priority: "P1"
milestone: "M3"
work_packages: ["WP-04", "WP-05"]
hypotheses: ["H3"]
depends_on: ["SOAM-007"]
labels: ["type:experiment", "priority:P1", "milestone:M3"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-008: Build shared-scope and noisy-evidence task families

## Problem / hypothesis

A translator that isolates every context can retain old tasks while preventing useful sharing. Redundant and misleading observations also need distinct treatment.

Specification: [research plan §10](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Create contexts with shared rotation primitives and different translations.
- Generate familiar/correct, changed, and noisy/misleading transition streams with separated task-family splits.

## Acceptance criteria

- [ ] Ground-truth sharing/noise labels are evaluator-only and cannot enter the writer or translator inputs.
- [ ] Correcting a shared primitive has a measurable benefit for another context; isolated corrections have protected-context checks.
- [ ] Predefine transfer, spurious-write, redundant-write, and adaptation criteria.
- [ ] Publish deterministic train/meta-validation/test family generators and verify split separation.

## Metrics / evidence

Beneficial cross-context transfer, redundant/spurious write rates, robustness versus observation noise, and retention.

## Dependencies

- [SOAM-007](SOAM-007-heuristic-scopes.md) — Compare unfiltered, sparse, random, and sensitivity-based scopes

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
