---
schema_version: 2
id: "SOAM-105"
title: "Implement and verify the assembly organization pilot harness"
type: "engineering"
status: "backlog"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-104"]
labels: ["type:engineering", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-22"
updated: "2026-11-22"
github_issue: null
decision: null
---

# SOAM-105: Implement and verify the assembly organization pilot harness

## Recommended thinking

**high** — Implement a frozen mechanism and causal evaluator while enforcing input provenance, discovery/test separation, no-write inference, and meaningful counterexample fixtures.

## Problem / hypothesis

The [AO-1 plan](../docs/proposed-studies/STUDY_ASSEMBLY_ORGANIZATION.md) needs a
small verified implementation of the eventual SOAM-104 contract. Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

Implement only the accepted candidate, controls, task and interventions. Reuse
existing infrastructure where its contracts fit; preserve archived E0/E0-HOLD code
and data. This is a harness/fixture task, not scientific confirmation or a generic
framework for topology search.

## Acceptance criteria

- [ ] Confirm SOAM-104 done/proceed and inspect its exact protocol/manifest and body conditions before source changes; run the existing `uv run pytest` suite first.
- [ ] Implement exact updates, learning, dense fixed input and normalization, separate parameters/state/evaluator truth, and all mandatory controls.
- [ ] Verify no-write inference, no hidden/future-target input, action timing, split isolation, fixed thresholds when used, and deterministic seed/config reproduction.
- [ ] Verify causal intervention accounting and locked discovery procedure. Include protocol-defined common-input/flat-network negative fixtures and a labeled supplied-route fixture; passing fixtures is not emergence evidence.
- [ ] Exercise declared collapse/freezing/instability cases and undefined-metric handling; verify the evaluator does not reward stable but useless states.
- [ ] Complete relevant tests, independent equation/metric checks and finite resource preflight with the frozen margin; stop and document infeasibility rather than extend the allocation.

## Metrics / evidence

Expected report: `reports/STUDY_ASSEMBLY_ORGANIZATION_HARNESS.md`, recording actual
tests, fixture seeds, source/config hashes, versions, exposure/resource counts and
preflight results. Only fixture data may be used here; no confirmation-driven
mechanism changes. Scientific fits belong to SOAM-106 after readiness review.

## Dependencies

- [SOAM-104](SOAM-104-assembly-organization-protocol.md) — requires completed protocol decision with proceed.

## Completion record

Not started. No implementation or engineering fixture has run for AO-1.
