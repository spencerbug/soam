---
schema_version: 2
id: "SOAM-109"
title: "Resolve graph modulation dynamics and freeze the bounded routing pilot"
type: "decision"
status: "ready"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-108"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-23"
updated: "2026-11-23"
github_issue: null
decision: null
---

# SOAM-109: Resolve graph modulation dynamics and freeze the bounded routing pilot

## Recommended thinking

**xhigh** — Resolve the tension between multi-step graph recruitment, preserved recurrent memory, economical two-state gating, and a defensible joint stability argument before fitting.

## Problem / hypothesis

[SOAM-108](SOAM-108-gated-assembly-direction-and-theory.md) freezes the direction
and [initial theory](../docs/GATED_ASSEMBLY_ROUTING_THEORY.md), not an empirical
protocol. Its compatibility gate is an energy-consistent reference with one binary
split in its limiting form. The theory's later dormant-state and recruitment
variants are analytical candidates outside the earlier numerical audit. None is
an accepted final mechanism. Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

Select one smallest mechanism capable of a causal graph-recruitment test. Define its
exact updates, learning and information boundary, conduct a distinct skeptical
review and precision/resource preflight, and freeze a fresh bounded protocol only
if justified. No automatic implementation or numerical budget follows from the old
AO-1 v1 decision. Theory may conclude revise/stop; do not substitute a flat-gating
experiment for the owner's mediated-recruitment question without resolving the intent mismatch.

## Owner clarification — November 23

The direction permits a learned graph: multiple entry populations, branching,
merging, shared recipients and cycles. The second field is the modulation network.
Activity can recruit disinhibition, making existing recurrent pathways influential
without changing weights. Mostly-dark/default-inhibited activity is an optional
candidate, not a mandatory topology or numerical sparsity target. Distinguish
stored associations in weights, dormant activity, and protected live transient
state. A one-step input classifier cannot by itself establish multi-step recruitment.
This clarification changes the design scope, not readiness or numerical allocation.

Modulation may also continue settling through its own learned recurrence after a
sensory or content cue is withdrawn. The owner's terms **associative modulation**
or **dynamic associative modulation** name this optional question. Cue-driven
recruitment and subsequent autonomous modulation can coexist in the same two-state
system; continuous content forcing is not required by the direction.

## Contract and decision order

The task is to determine whether a two-state content/modulation system can learn
useful causal recruitment across populations under dense fixed input, and to
specify the smallest discriminating pilot if a defensible mechanism is available.
It does not require positive learned evidence, capacity growth, or every allowed
graph motif to appear. No root, entry subset, module boundary or routing graph is
assigned to candidate neurons. The task may supply observable factor structure
and evaluation probes, with that scaffolding disclosed.

First resolve mechanism feasibility, memory semantics and the causal claim. Then
design the empirical protocol. A proceed decision requires the complete protocol
and preflight below. A supported revise/stop decision can complete this ticket
with the derivation/counterexample and explicit disposition of each protocol item
as not reached; it does not require fabricating a protocol for an infeasible
mechanism or unblock implementation.

Mostly-dark activity is optional. Select whether the pilot requires dormant
recall, maintained episode state, or both for specifically declared information;
do not require every inactive population to be both silent and actively holding
its previous state. Two fields means two retained scalars per indexed unit;
derived signals and extra weight matrices must be counted but are not extra state.

Distinguish cue source, ongoing drive and modulation recurrence. For the specific
content-driven recruitment claim, a modulation system with no causal path from
content at any time, including initialization, is a control/alternative explanation.
With identical sensory history, modulation initialization and any stochastic draws,
changing content cannot change that system's modulation trajectory. Such a system
may still perform useful modulation-only graph inference. By contrast, content may
cue a modulation state whose later autonomous trajectory carries that influence;
removing content drive after cueing does not make its history content-independent.
No particular direct cross matrix or reciprocal energy construction is required:
content may influence a recipient through intermediate modulation states.

If associative modulation is selected, distinguish removing external observation
from additionally removing content-to-modulation drive. Specify the dynamics of
each condition and test useful recovery from partial or perturbed cues; merely
holding a mask or converging is insufficient. This remains an optional mechanism
question, not a mandatory additional arm, new allocation or established memory claim.

## Acceptance criteria

- [ ] Derive a compact two-state sensory/recurrent gate capable of causal multi-step recruitment, including how content can affect another recipient's receptiveness, or document the specific limitation without hiding added states, cross matrices or roles. Require recruitment from near-zero recipient activity only if the dormant variant is selected.
- [ ] Compare modulation without any content influence with content-dependent alternatives analytically; distinguish cue history, ongoing drive and autonomous modulation recurrence, and identify which causal claim each can test. Associative modulation remains optional. For a viable candidate, specify a joint-energy or other explicit stability argument, support-edge removal, leakage, the selected dormant/live memory contract, and genuine-change recovery.
- [ ] Specify fixed dense input, supplied versus learned structure, initialization/readout, integration and no-write inference. If actions are included, define action timing, predict-before-new-evidence scoring and no action replay during settling. If the pilot is stationary, declare action prediction and action selection untested rather than import a full navigation study.
- [ ] Define the exact persistent learning rule and a pressure for useful organization; distinguish the state energy from the fitting objective, and prevent mask-controlled scoring from rewarding blindness.
- [ ] For proceed, freeze one observable task affording linked causal recruitment and held-out reuse, with discovery/confirmation separation and matched flat/feedforward/ordinary-recurrent controls under declared total resources. Select one small discriminating motif; allow multiple entries and shared recipients without requiring every motif or imposing graph topology on candidate neurons.
- [ ] Preflight practical margins, independent-unit counts, uncertainty and precision rules for primary mediated recruitment and all usability guards; explain outcomes whose intervals are directional but too wide.
- [ ] Before any exploratory fit, declare a finite development allocation, permitted adjustments, stopping rules and exposure ledger; otherwise restrict work to explicitly bounded untrained checks. Freeze fresh confirmation streams and a full resource inventory before confirmation.
- [ ] Record proceed/revise/stop and create or explicitly revise only the necessary implementation handoff after the protocol decision; preserve AO-1 v1 and all historical outcomes and integration gates.

## Metrics / evidence

For proceed, deliver a new versioned gated-routing protocol and numeric manifest,
analytical/supplied-fixture evidence, primary sources, and the scoped decision.
For revise/stop, deliver the supported limitation and the item dispositions
specified above; a numerical protocol is not required. No thresholds, sample
sizes, trained results or empirical resource estimates exist yet. The SOAM-108
algebra audit is not a timing calibration or
validation of a graph-recruitment evaluator. Lean remains optional and theorem-specific.

## Dependencies

- [SOAM-108](SOAM-108-gated-assembly-direction-and-theory.md) — requires done/proceed for this design continuation only.

## Branch conditions

This is the single selected next design task. SOAM-105–107 retain the unrun,
unselected AO-1 v1 contract; they cannot be silently reused for this mechanism.
E0-HYS, full integration, online structural learning and a general capacity-scaling
campaign remain unselected. A capacity benefit is not a required positive outcome.

## Completion record

Ready after SOAM-108 done/proceed on November 23. Not started. The later November 23
graph/modulation clarification is incorporated; full protocol
work remains unstarted. No new empirical protocol, model implementation, exploratory
fit or confirmation allocation is accepted.

## Self-consistency review — November 23

The core direction is coherent as a research/design task; the equations, learning
rule, memory contract and empirical test are deliberately unresolved. This review
does not establish that a learned useful mechanism exists. Three wording tensions
were corrected: optional dormancy had become mandatory in the recruitment item;
input-only modulation was not distinguished from a content-driven mechanism;
and permission to revise/stop conflicted with unconditional protocol deliverables.
Graph motifs and action timing are now explicitly conditional on the chosen pilot
instead of requiring all graph capabilities or a full sensorimotor study at once.

A subsequent owner clarification separates autonomous settling after cueing from
structural independence from content. The earlier wording was too broad: recurrent
associative modulation can coexist with content-driven recruitment. This optional
question is retained without adding a required experiment or claiming learned recall.
Clarification validation: the ticket validator still passes 110 tickets and two
templates; `git diff --check` passes. A focused audit verified 67 local links in
the three affected documents, unchanged original audit source hashes/configuration,
and five unchanged historical v1 files. No code or numerical checks were rerun.

No inherent contradiction was found between two state fields and additional
coupling weights, cyclic connectivity and convergence under fixed input, or
dormant activity and persistent memory weights. Strict fixed-input energy descent
does exclude sustained nonstationary cycles for that candidate; any such behavior
would need another dynamical contract. Stored recall is not guaranteed merely
because weights remain unchanged.

Readiness remains ready: this is a requirements review, not execution of the full
protocol task. The strongest simpler explanations remain flat selection and extra
ordinary recurrent state. Causal influence on modulation, matched-resource controls,
and usable recall/correction guard against declaring their performance a recruitment
success. No new code, fitting, numerical audit, allocation, ticket or empirical
claim was introduced. Earlier source/config hashes and historical v1 remain intact.

Review validation: `uv run python scripts/check_tickets.py` passes 110 tickets
and two templates; `git diff --check` passes. An inline audit checked 328 local
links in the three affected documents, original audit source/config hashes, and
five unchanged historical v1 files. No numerical audit or pytest rerun was needed
for these documentation-only corrections. Qwen extraction job
`65c11467694041c09a042589d74ed011` returned relevant phrases but incomplete source
coverage and inaccurate line offsets; the primary agent verified the cited
requirements directly. No worker recommendation determined an architectural choice.
