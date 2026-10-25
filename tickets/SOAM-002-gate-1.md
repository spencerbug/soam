---
schema_version: 2
id: "SOAM-002"
title: "Gate 1: review the substrate before online writing"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1"]
depends_on: ["SOAM-001"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: "proceed"
---

# SOAM-002: Gate 1: review the substrate before online writing

## Recommended thinking

**high** — Weigh substrate evidence, residual H1 limitations, and the conditions for proceeding to plasticity.

## Problem / hypothesis

Engineering readiness and scientific confirmation are different. Record a bounded decision about whether this substrate is adequate for local-acquisition experiments.

Specification: [research plan §8, §19, §22](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Review the original report and strengthened controls.
- Choose a documented reference substrate or specify a targeted revision.

## Acceptance criteria

- [x] Cite configuration/commit-linked evidence for prediction, switching, stability, and budget comparisons.
- [x] Record decision as proceed, revise, or stop; a proceed decision states the exact claims and residual H1 limitations.
- [x] Define the designated reference checkpoint, allowed plastic parameter family, and failure conditions for the next study without implementing writes here.
- [x] Update the priority table; if revision is needed, create linked follow-up tickets and keep dependent implementation unready.

## Metrics / evidence

Review the [SOAM-001 report](../reports/SUBSTRATE_CONTROLS.md), including the additive
seed-23 failure, independent handoff semantics, and GRU perturbation sensitivity.

Decision record against the preregistered criteria, with uncertainty and unresolved reuse questions.

## Dependencies

- [SOAM-001](SOAM-001-substrate-controls.md) — Strengthen substrate controls and budget comparisons

## Completion record

Completed 2026-10-25. **Decision: proceed**, bounded to local-acquisition research on
all three width-37 low-rank checkpoints; retain GRU as a predictive reference.
The user selected this direction during the interactive review.

[Gate decision](../reports/GATE_1_REVIEW.md) records evidence, alternatives, claim
limits, the plasticity contract, and failure conditions. [Checkpoint manifest](../reports/gate-1/checkpoints.json)
identifies seeds 11/23/47, exact local paths, and verified hashes; seed 11 is only
the implementation fixture. Allowed plastic tensor: `recurrent.weight` (37×37);
all other persistent parameters/settings stay frozen. No writes implemented here.

Reviewed the original report and SOAM-001's 18-trial controls, 17 screen passes,
additive seed-23 failure, six exact repeats, budget comparisons, perturbation
sensitivity, and long-horizon drift. Measured source commit:
`7238e6ce69ce5a4e561960b290a2222e5e16aeb5`; config/source fingerprints in the manifest.
Full H1 reuse and all stronger SOAM claims remain open. Fresh evaluation streams and
preregistered acquisition/retention limits are required before writer experiments.

Validation: loaded six existing checkpoints and checked identities, shapes, and
SHA-256 hashes; verified cited table entries; `uv run python scripts/check_tickets.py`
and relative link checks passed. No new experiments or software tests were needed
for this documentation-only decision; prior 27-test results remain SOAM-001 evidence.

SOAM-003 and SOAM-019 become ready. SOAM-003 is next on the primary path; future
implementation is not started merely by completing this gate.
