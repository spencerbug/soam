---
schema_version: 2
id: "SOAM-087"
title: "Implement and verify the bounded D-R1 retrieval harness"
type: "engineering"
status: "in_progress"
priority: "P0"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-086"]
labels: ["type:engineering", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-18"
updated: "2026-11-18"
github_issue: null
decision: null
---

# SOAM-087: Implement and verify the bounded D-R1 retrieval harness

## Recommended thinking

**high** — Implement a fixed scientific contract with coupled projector, energy,
observability, reset, uncertainty and resource-accounting invariants. Escalate any
mechanism or endpoint change to the protocol owner instead of tuning the implementation.

## Problem / hypothesis

The [accepted D-R1 protocol](../docs/STUDY_D_R1_PROTOCOL.md) needs a minimal verified
implementation before its candidate competence or nonlinear-settling contribution
can be evaluated. Historical D's direct map does not implement this retrieval law.

## Scope

Implement the [v1 manifest](../docs/protocols/study_d_r1_v1.json) in a new
`soam/retrieval/` package: PH768, the one-cycle intervention, REG-LIFT, unchanged D
reference equations on fresh streams, paired full/partial queries, bounded phase
runner, independent reduction and reporting. Preserve historical code/contracts.
One candidate only; no general framework or unselected scientific branch.

## Acceptance criteria

- [ ] Run the existing nonempty suite before code changes; preserve historical D source/results.
- [ ] Verify projector writes, repeated/dependent patterns, symmetry, zero effective diagonal,
  energy descent, mask handling, fixed decoder, exact first-cycle identity and finite stopping.
- [ ] Cover reset/no-write, core preservation, data separation, forbidden-input poisoning,
  same-observation parity, query-order invariance, deterministic replay and correctly scored failure.
- [ ] Verify raw REG conjugate-gradient/direct equivalence within protocol tolerances.
- [ ] Implement the complete frozen trial inventory, allocation gate, provenance, cumulative
  limits, phase receipts, archive protection and independent endpoint reconstruction.
- [ ] After explicit fresh numerical allocation acceptance, execute only the single-root
  timing fixture; verify 2x projected resources and reserve before development.
- [ ] Record exact commands/checks, source/config identity, fixture costs and any invalid,
  infeasible or negative result; do not imply that passing engineering fixtures proves recall.

## Metrics / evidence

The protocol owns equations and statistical criteria. Hand-constructed software
fixtures are engineering work. The scientific timing fixture, development competence
screen, calibration, confirmation, repeat and reporting consume the proposed new
7200 CPU / 14400 wall seconds, 2 GiB RSS / 2 GiB artifacts. The owner explicitly approved the allocation on November 18; the
[acceptance receipt](../docs/requests/study_d_r1_allocation_2026_11_18.json) binds the manifest and ceilings. No inherited
D budget and no autonomous Qwen trial control.

## Dependencies

- [SOAM-086](SOAM-086-recurrent-retrieval-protocol.md) — done/proceed for the contract only.

## Branch conditions

The owner's November 18 instruction begins the previously selected D-R1 fork.
Implementation is eligible under SOAM-086. Numerical execution additionally requires
fresh allocation acceptance; do not interpret ready status as that acceptance.
SOAM-052 remains stop. D3/D4, E0/F, coupling, learned roles and replay stay deferred.
Allocate the experiment ticket only when this bounded engineering work is verified;
its development screen may stop before confirmation without requiring success.

## Completion record

Implementation started November 18 following explicit allocation acceptance.
The baseline suite passed 303 tests before code changes (SOAM-086); no source changed
between that check and this start. Numerical phases require frozen committed source.
