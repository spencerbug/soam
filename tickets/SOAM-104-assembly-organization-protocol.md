---
schema_version: 2
id: "SOAM-104"
title: "Specify assembly organization dynamics and freeze the bounded pilot"
type: "decision"
status: "ready"
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
decision: null
---

# SOAM-104: Specify assembly organization dynamics and freeze the bounded pilot

## Recommended thinking

**xhigh** — Derive one explicit learning/dynamics mechanism and a causal test that distinguishes learned routes from common input, generic recurrence, supplied topology, and state freezing.

## Problem / hypothesis

The [AO-1 plan](../docs/proposed-studies/STUDY_ASSEMBLY_ORGANIZATION.md) selects
learned assembly organization under dense fixed sensory input. Its equations and
primary measurement remain proposals, not a frozen experiment. Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

Complete the mathematical specification, ordinary analytical checks, and one
bounded pilot protocol/manifest as the lightweight RFC. Select one task and one
organization intervention. Define supplied, fitted, and learned quantities. No
training or autonomous search occurs in this design ticket; any tiny untrained
counterexample check must have its finite inputs/limits recorded first. Lean is
optional for a settled theorem and is not an implementation prerequisite.

## Acceptance criteria

- [ ] Specify the exact state update, directed/reciprocal connections, initialization/correction, readout, action timing, learning rule/objective, and competition/activity constraints; distinguish training loss from dynamical energy.
- [ ] Keep sensory projection fixed and dense, with no prescribed entry subset, assembly labels, tree or layers in the candidate. Declare input rank, N/d, drive normalization, and capacity accounting.
- [ ] Analyze boundedness, local stability assumptions, legitimate action response, and counterexamples; distinguish derivations, numerical checks, and empirical hypotheses. Do not require an emergence theorem or a positive analytic result.
- [ ] Freeze a small observable multi-factor task with held-out combinations, no privileged training/evaluation inputs, and a reproducible discovery/intervention procedure using permitted data only.
- [ ] Select competent ordinary, symmetric, separated, and conventional/structured controls; if hysteresis is included, use fixed thresholds and cross its presence with the selected organization pressure.
- [ ] Freeze primary selective-mediation endpoint, practical margin, prediction/retention/navigation/recovery guards, root-level intervals and precision rules, and valid-negative/inconclusive/invalid classifications.
- [ ] Freeze finite configurations, train/development/confirmation streams, exact repeat, fixture limits, data exposure, total fit counts, compute/storage caps and stopping rules before fitting; use a fresh AO-1 namespace.
- [ ] Review information/resource parity, causal identifiability, feasibility and branch conditions; record proceed/revise/stop and its implementation consequences.

## Metrics / evidence

Expected deliverables: `docs/STUDY_ASSEMBLY_ORGANIZATION_PROTOCOL.md` and
`docs/protocols/study_ao1_v1.json`, plus analytical evidence within that protocol.
The protocol will own equations and numerical criteria; the planning document must
link to it rather than become a conflicting second contract. Review E0/E0-HOLD and
the scoped sources in the AO-1 plan. No numeric margins or fit inventory are adopted
merely by creating this ticket. Measured drift reduction is not a required design
outcome; an unidentifiable or infeasible candidate may receive revise/stop.

## Dependencies

- [SOAM-103](SOAM-103-assembly-organization-plan.md) — fresh planning selection, required done/proceed.

## Branch conditions

AO-1 is the single selected design path. E0-HYS is unselected and is not a required
pre-experiment. SOAM-042/043 integration, RIM coupling, online structural learning,
and broader architecture sweeps remain deferred. Protocol proceed accepts a test,
not organization, attraction, or semantic understanding.

## Completion record

Not started. Record the selected equations, analytical checks, frozen contract,
review, validation commands, source baseline, and scoped decision. No trials run.
