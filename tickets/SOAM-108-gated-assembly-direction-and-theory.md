---
schema_version: 2
id: "SOAM-108"
title: "Freeze gated assembly routing direction and derive initial theory"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-104"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-23"
updated: "2026-11-23"
github_issue: null
decision: "proceed"
---

# SOAM-108: Freeze gated assembly routing direction and derive initial theory

## Recommended thinking

**xhigh** — Preserve the owner's conditional tree-routing question while deriving coupled-state energy, isolation, and stability constraints without supplying the desired organization.

## Problem / hypothesis

On November 23 the owner requested: "Let's freeze the direction then, and start
working through the math and theory." The preceding clarification selects two
coupled state fields on the same indexed units: sensorimotor content and soft
receptiveness. Dense fixed input reaches potential recipients broadly; learned
upstream decisions should causally select downstream receptiveness. Selective
recurrent gating must protect associations while preserving their internal support.
Apply the [common completion requirements](README.md#completion-requirements).

AO-1 v1 tests one selective pathway, not this conditional branching mechanism.
Preserve SOAM-104 done/proceed, its protocol/manifest/audit and all earlier measured
outcomes. SOAM-105–107 remain unrun and are now unselected backlog. No v1 numerical
allocation transfers to the new direction.

## Scope

Freeze the scientific direction, not an empirical protocol. Own the lightweight RFC
in [the initial theory](../docs/GATED_ASSEMBLY_ROUTING_THEORY.md). Derive one
energy-compatible reference and decisive counterexamples; compare simpler
explanations; define the smallest next discriminating question. No model fitting,
learned organization claim, implementation of a research model, or publication.
Only the theory document's predeclared finite untrained algebra audit may run.

## Acceptance criteria

- [x] Record required constraints versus candidate mechanisms and preserve the owner’s tree-like access question, current selection, and historical contracts.
- [x] Derive sensory/recurrent gating, fixed-point preservation and isolation conditions, a joint-energy reference, and limitations of a single soft mask.
- [x] Review two serious simpler alternatives, causal false positives, sensorimotor boundaries, resource costs, and capacity claim limits.
- [x] Predeclare and execute only finite untrained equation/counterexample checks; retain provenance, actual results and failures without treating them as learned evidence.
- [x] Record a scoped proceed/revise/stop decision, unresolved design work, next eligible ticket, and successful ticket/link/diff checks.

## Metrics / evidence

Review the owner discussion, AO-1 v1, E0/E0-HOLD measured zero-input drift,
and primary sources cited in the theory. The algebra audit checks derivatives,
energy dissipation and explicit counterexamples; it estimates no empirical effect
or uncertainty interval. No scientific precision, seed or compute allocation is
frozen by this direction decision.

## Dependencies

- [SOAM-104](SOAM-104-assembly-organization-protocol.md) — done/proceed for the preserved earlier design; not evidence for the replacement mechanism.

## Completion record

Started November 23 from source `5f8333ba1086d15cef3a6db7ef88a9e3c3a623d3` after
checking SOAM-104 and the owner’s replacement selection. Assignees remain empty
because no real project handle is known. Baseline `uv run pytest`: 348 passed,
one existing TorchScript deprecation warning, 22.05 seconds. No existing experiment
code or frozen protocol has been modified.


**Decision: proceed to SOAM-109 design only.** The owner-selected direction is
frozen as learned tree-like conditional access through paired content/receptiveness
states and selective sensory/recurrent gating. The [theory](../docs/GATED_ASSEMBLY_ROUTING_THEORY.md)
derives exact fixed-point preservation, conditional isolation/local bounds,
reciprocal terms for one symmetric joint energy, and its stability/integrator limits.
The binary compatibility gate is an analytical reference, not the accepted final
mechanism or a tree. [SOAM-109](SOAM-109-gated-assembly-protocol.md) is P0/ready,
xhigh, for the remaining mechanism/learning and fresh protocol decision. SOAM-105–107
are unrun/unselected backlog; SOAM-104 and five v1 contract/audit files remain
unchanged. No model fit, integration gate, capacity benefit or new empirical
allocation is accepted.

The predeclared single [algebra audit](../scripts/check_gated_routing_theory.py)
passed ten checks; [raw results](../docs/analysis/gated_routing_theory_checks.json)
record all 64 cases, supplied counterexamples, exact settings and hashes. Maximum
manual/autograd error 3.33e-16; centered finite-difference error 4.38e-10; equilibrium
linearization error 1.11e-16. Measured CPU .956371 s, wall 1.254945 s, RSS
290,455,552 bytes and artifact 19,130 bytes were within the frozen audit limits.
There were zero numerical failures/retries or fitting updates. Ruff initially
reported loop-variable bindings; explicit partial bindings fixed them before the
only numerical run. A bare-Python artifact-read command failed due to the absent
pyenv interpreter; `uv run python` succeeded. The audit itself used uv throughout.

Validation: `uv run ruff format scripts/check_gated_routing_theory.py` and
`uv run ruff check scripts/check_gated_routing_theory.py` pass. Final `uv run pytest`
passed 348 tests in 17.48 s with the same existing TorchScript warning. The exact
audit command appears in the theory. `uv run python scripts/check_tickets.py`
validates 110 tickets and two templates; `git diff --check` passes. An inline
local-target audit validated 662 Markdown targets before this completion entry and
667 afterward; script/config hashes match the saved audit, and five historical v1
files were verified unchanged. Final status, link, Ruff and diff checks passed
after the done/proceed and successor-ready updates.

Qwen extraction job `5905a0809c3e444799e1e0f63da785e2` returned an incomplete
three-ticket extraction (only SOAM-107, without requested line references). The
primary agent checked all affected ticket evidence directly; no worker output
controlled the theory or decision. No additional agent was spawned.

Research usefulness: the owner's correction prevents substituting a single-path
or flat-mask test for conditional tree-like access. The analysis caught sensory
masking mistaken for intrinsic stability, removal of supporting recurrence,
soft-mask leakage, separate energies mistaken for joint stability, and supplied
partitions mistaken for learned trees. The analytical work narrows the next design
choice; it does not measure a memory improvement. Only the above audit/test timing
is recorded; total research time is not inferred. The owner was notified that
this architectural clarification merits the eventual joint blog/report as theory,
not an empirical result. No publication, remote issue, push or commit was performed.


## Later owner clarification — November 23

The owner generalized trees to graphs and named the second field modulation:
multiple entry populations may recruit disinhibition of further populations,
allowing branching, merging, reuse and cycles. The earlier tree-specific language
in this completed record is historical and is superseded as a topology constraint.
The [theory's graph/dormancy addendum](../docs/GATED_ASSEMBLY_ROUTING_THEORY.md#9-owner-clarification-multiple-entry-graphs-and-possible-dormancy)
and SOAM-109 now preserve causal multi-step recruitment without requiring a tree.
Mostly-dark activity is a possible mechanism, not a frozen sparsity requirement.
Dormant memories in weights are distinct from retained live state; suppressing
recurrence is not automatically a defect for the dormant-recall contract.

The addendum derives a source/recipient-gated energy alternative and an explicit
content-to-modulation cross-matrix interaction analytically, including the
reciprocal terms needed for the joint energy and the extra parameter cost.
It is outside the earlier numerical audit, which remains unchanged and valid for
its stated equations only. No code, model fit, experiment budget or historical
outcome changed. SOAM-108 remains done/proceed and SOAM-109 ready; this is a scope
clarification, not completion or activation of the next full protocol.

Clarification validation: `uv run python scripts/check_tickets.py` accepts 110
tickets and two templates; `git diff --check` passes; 669 local Markdown targets
resolve. Original audit script/config hashes and five historical v1 files remain
unchanged. No numerical audit or pytest rerun was needed for these documentation-
only changes; the new analytical variant is explicitly outside the earlier ten
checks. The local worker rejected the single-ticket patch request because it
exceeded its one-chunk input limit; the primary agent made and reviewed the scoped
edits directly. No worker patch was applied.
