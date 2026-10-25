---
schema_version: 2
id: "SOAM-003"
title: "Define the grounded local-write contract and plastic parameters"
type: "engineering"
status: "done"
priority: "P1"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02"]
hypotheses: ["H2"]
depends_on: ["SOAM-002"]
labels: ["type:engineering", "priority:P1", "milestone:M2"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---

# SOAM-003: Define the grounded local-write contract and plastic parameters

## Recommended thinking

**high** — Define plastic parameter boundaries, grounded targets, and atomic updates without compromising no-write inference.

## Problem / hypothesis

Online writing needs an explicit, testable distinction between transient state, frozen ordinary parameters, and designated plastic weights.

Specification: [research plan §5, §9, §17](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

Gate 1 [decision](../reports/GATE_1_REVIEW.md) selects the width-37 low-rank model;
use the [verified checkpoint manifest](../reports/gate-1/checkpoints.json).
Only `recurrent.weight` (37×37) may be plastic; freeze all other parameters and
settings. Define grounded cue/target construction, norm caps, and rollback before
measured writer work. Retain GRU as a predictive reference; writer-isolating online
gradient controls must use the same low-rank plastic family. Use fresh evaluation
streams and review the gate's failure conditions.

- Implement one justified plastic weight or fast-adapter formulation behind a common writer interface.
- Define cue/target construction, bounded update proposals, commit/rollback, and grounded-evidence provenance.

## Acceptance criteria

- [x] Freeze encoder/readout/base parameters as specified by the Gate 1 decision; any exception is documented and ablated.
- [x] A real transition can produce an inspectable update proposal and atomic application or rollback.
- [x] Tests show non-designated parameters remain unchanged and imagined rollouts cannot invoke writing.
- [x] Log update norm/rank, bytes, time, data exposure, and the exact before/after checkpoint identities.

## Metrics / evidence

Write cost, changed-parameter set, update magnitude, immediate and multistep prediction before/after writes.

## Dependencies

- [SOAM-002](SOAM-002-gate-1.md) — Gate 1: review the substrate before online writing

## Completion record

Completed 2026-10-25. [Contract](../soam/plasticity/README.md),
[implementation/report](../reports/LOCAL_WRITE_CONTRACT.md),
[configuration](../reports/local-write-contract/config.json),
[provenance](../reports/local-write-contract/provenance.json),
[results](../reports/local-write-contract/results.json), and
[reproduction](../reports/local-write-contract/reproducibility.json).

Source commit: `917eff8eebe9ffdaada8908d763bcf0a7b5a7b68`; source fingerprint:
`cbcc1b19d4582b102acbeecd0bf2844f7ed834fb4a392db27ba484b911c1e2fa`.
All three Gate 1 low-rank checkpoints (seeds 11, 23, 47) were loaded by verified hash.
The bounded damped local-Jacobian outer-product rule modifies only `recurrent.weight`;
all other parameters/settings and the fixed encoder contract remain frozen.
Prediction snapshots have no writer capability. Proposals are inspectable and separate
from atomic in-process commits; exact one-level rollback, rejection, and audit records
are implemented. No global training, learned scope, or consolidation was added.

Validation: 27 tests before changes; 48 afterward (21 writer tests). Ruff and ticket
validation pass. Three one-write engineering runs and all three repeats match numerical
metrics and checkpoint contents; timings/receipt IDs excluded. Every rollback restores
weights and prediction metrics exactly. Commands and numerical/resource details are
in the report. A rounding-at-budget-boundary failure found during testing was fixed
with bounded numerical backoff before measured demonstrations.

**Negative result retained:** immediate observed-transition error improves in all
three examples, but seed 23's 48-step irregular NMSE worsens .05049 → .06697 and
other held-out regressions occur. This verifies the contract, not H2 acquisition.
SOAM-004 becomes ready to design and run the actual baseline comparison with fresh
confirmation data and preregistered observation/search/accuracy/retention budgets.
