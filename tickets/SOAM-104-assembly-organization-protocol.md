---
schema_version: 2
id: "SOAM-104"
title: "Specify assembly organization dynamics and freeze the bounded pilot"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-103"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-22"
updated: "2026-11-22"
github_issue: null
decision: "proceed"
---

# SOAM-104: Specify assembly organization dynamics and freeze the bounded pilot

## Recommended thinking

**xhigh** — Derive one explicit learning/dynamics mechanism and a causal test that distinguishes learned routes from common input, generic recurrence, supplied topology, and state freezing.

## Problem / hypothesis

The [AO-1 plan](../docs/proposed-studies/STUDY_ASSEMBLY_ORGANIZATION.md) selects
learned assembly organization under dense fixed sensory input. This ticket freezes
the [protocol](../docs/STUDY_ASSEMBLY_ORGANIZATION_PROTOCOL.md) and its
[numeric manifest](../docs/protocols/study_ao1_v1.json). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

Complete the mathematical specification, ordinary analytical checks, and one
bounded pilot protocol/manifest as the lightweight RFC. Select one task and one
organization intervention. Define supplied, fitted, and learned quantities. No
training or autonomous search occurs in this design ticket; any tiny untrained
counterexample check must have its finite inputs/limits recorded first. Lean is
optional for a settled theorem and is not an implementation prerequisite.

## Acceptance criteria

- [x] Specify the exact state update, directed/reciprocal connections, initialization/correction, readout, action timing, learning rule/objective, and competition/activity constraints; distinguish training loss from dynamical energy.
- [x] Keep sensory projection fixed and dense, with no prescribed entry subset, assembly labels, tree or layers in the candidate. Declare input rank, N/d, drive normalization, and capacity accounting.
- [x] Analyze boundedness, local stability assumptions, legitimate action response, and counterexamples; distinguish derivations, numerical checks, and empirical hypotheses. Do not require an emergence theorem or a positive analytic result.
- [x] Freeze a small observable multi-factor task with held-out combinations, no privileged training/evaluation inputs, and a reproducible discovery/intervention procedure using permitted data only.
- [x] Select competent ordinary, symmetric, separated, and conventional/structured controls; if hysteresis is included, use fixed thresholds and cross its presence with the selected organization pressure.
- [x] Freeze primary selective-mediation endpoint, practical margin, prediction/retention/navigation/recovery guards, root-level intervals and precision rules, and valid-negative/inconclusive/invalid classifications.
- [x] Freeze finite configurations, train/development/confirmation streams, exact repeat, fixture limits, data exposure, total fit counts, compute/storage caps and stopping rules before fitting; use a fresh AO-1 namespace.
- [x] Review information/resource parity, causal identifiability, feasibility and branch conditions; record proceed/revise/stop and its implementation consequences.

## Metrics / evidence

Deliverables: [protocol](../docs/STUDY_ASSEMBLY_ORGANIZATION_PROTOCOL.md),
[manifest](../docs/protocols/study_ao1_v1.json),
[design audit](../docs/analysis/AO1_DESIGN_AUDIT.md) and
[raw algebra checks](../docs/analysis/ao1_design_checks.json).
The protocol owns equations/algorithms and the manifest owns numerical constants;
the earlier planning document links to this contract. E0/E0-HOLD and the scoped
primary sources informed the review; their empirical outcomes are unchanged.

## Dependencies

- [SOAM-103](SOAM-103-assembly-organization-plan.md) — fresh planning selection, required done/proceed.

## Branch conditions

AO-1 is the single selected design path. E0-HYS is unselected and is not a required
pre-experiment. SOAM-042/043 integration, RIM coupling, online structural learning,
and broader architecture sweeps remain deferred. Protocol proceed accepts a test,
not organization, attraction, or semantic understanding.

## Completion record

Completed November 22, 2026 after committing the earlier planning changes as
`c121d69`. SOAM-103 was done/proceed before this work began.

**Decision: proceed to SOAM-105 only.** The protocol's design-review section accepts
one bounded test of connection cost plus activity-power regulation in directed
leaky recurrence. Dense fixed input has width 24 including masks and population 96.
The task combines two poses with three attributes; two attribute combinations are
held out. Hysteresis is absent in v1. Seven mandatory model families, four settings
each, three development roots and twenty confirmation roots yield 231 scientific
fits including seven exact repeats. The manifest fixes sixteen simultaneous
criteria and CPU/wall/RSS/artifact ceilings before any learning.

The finite untrained audit passed all seven checks. Its Jacobian discrepancy is
3.25e-11. Intentional counterexamples show stable memory without routes and lack
of an inherited symmetric energy guarantee. No theorem of tree emergence is
claimed. The audit records seed 20261122, versions, hashes, timing and memory.
Design-source baseline is `c121d69`; final files are fingerprinted with the audit
and subsequent commit. No trained-model results or AO-1 timing preflight exist.

Validation: `UV_CACHE_DIR=/private/tmp/soam-uv-cache uv run --offline --no-sync pytest`
passed **348 tests** (one existing TorchScript deprecation warning) before adding
the standalone audit script. Ruff format/check passed for that script. Its one
declared execution passed, and hash reconstruction verified the final manifest
differs from the audited version only in status and blindfolded-action naming.
`uv run python scripts/check_tickets.py` passed all 108 tickets and two GitHub
templates; `git diff --check` passed. All 642 local Markdown file links in the
changed/new documents were checked.

Bounded Qwen interface extraction was incomplete; the primary agent checked the
needed navigation/hold interfaces directly. No worker output was treated as
architectural authority or empirical evidence.

SOAM-105 is ready for the exact harness and resource preflight. Its full-inventory
projection must meet the frozen margin before any scientific fit. SOAM-106/107
remain backlog; E0-HYS, RIM coupling and integrated SOAM-042/043 remain unselected.
Protocol acceptance passes no empirical gate. The joint blog/report remains
planned for the first measured experiment and review, not this design decision.
