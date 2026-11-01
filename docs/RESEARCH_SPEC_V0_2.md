# SOAM v0.2 — cue-driven embodied attractor dynamics

**Adopted:** 2026-11-01. **Status:** research scope and experimental interfaces;
mechanisms and scientific claims remain unproven.

## 1. Authority, provenance, and revision boundary

This amendment records the owner's October 31 architecture conversation
(`docs/ChatGPT-SOAM Architecture Baseline-20261031-2347.md`) and November 1 decisions:

- Put concurrent, cue-driven attractor switching ahead of the associative writer.
- Include an explicit attractor candidate and ordinary recurrent controls from the
  first measured experiment; prioritize switching over sophisticated prediction.
- Allow substantial initial scaffolding instead of simultaneously requiring
  unsupervised learning and self-organizing memory.
- Test attended, tracking, and primed roles with real sensorimotor feedback.
- Investigate whether concurrent roles need separate recurrent populations, cloned
  circuits, alternating banks, or columns/stacks; do not assume one population works.

The [v0.1 specification](RESEARCH_SPEC.md) remains a historical record. This amendment
supersedes its global interface freeze, single-substrate preference, writer-first
execution order, and mandatory learned-consolidation path to composition/grounding.
Its evidence standards, H1–H8 definitions, and historical experimental contracts
remain in force. [Gate 1](../reports/GATE_1_REVIEW.md) still authorizes only its recorded
low-rank writer study; it does not establish readiness for v0.2 attractor handover.

The current code models continuous 2D regimes using recurrent predictors, not an
explicit object graph. The conceptual shift is toward graded, stimulus-responsive
associations among dynamical patterns. An explicit discrete world graph is neither
a required representation nor a new implementation target. A graph may describe
observed relationships or serve as a labeled comparison without governing inference.

## 2. Research thesis and commitments

SOAM investigates whether interacting associative dynamical circuits can maintain
grounded local models, recruit and calibrate prospective representations, transfer
attention and control, and eventually acquire reusable sensorimotor skills without
destructive interference.

A pattern may describe a view, part, object, relation, or activity. It need only
support useful dynamics within its domain; a complete object reconstruction is not
required. Which domains exist and how their boundaries are learned are later research
questions. Hand-designed domains in early experiments are disclosed scaffolding.

Core functional commitments:

1. Partial cues can recruit candidates with graded activation.
2. A tracking candidate updates its own state from available observations and
   executed actions before it becomes attended.
3. A primed candidate may hold only a cue/activation state; it must not be credited
   with accurate continuous tracking unless that computation actually occurs.
4. Attention allocates influence and resources. It is distinct from activation,
   evidential support, and motor execution authority.
5. Competing explanations of the same evidence compete locally; compatible parts
   and instances may coexist. No global winner-take-all rule may silently eliminate
   all composition.
6. Sensory and memory attention are independently movable functional controls.
   Their neural realization is open, and early controllers may be scripted.
7. Estimated actual successor state and desired successor state are separate.
   Priming or intention is not evidence that a physical transition has succeeded.
8. State calibration, persistent generic knowledge, instance-specific memory, and
   simulator ground truth have separate ownership and update permissions.

## 3. Circuit topology is an early experimental variable

Circuit identity, learned parameters, active instance state, and physical/logical
population must not be conflated. Reusing one wheel model for several wheels may
require several independent activity states. This does not establish that one
neural population can maintain several attractors concurrently.

The first protocol compares a bounded subset of these alternatives and documents
the remainder as follow-ups:

| Candidate organization | Question and necessary accounting |
| --- | --- |
| One shared population | Can competing/tracking patterns coexist without collapse, destructive mixing, or losing the source state? |
| Separate parallel populations | Does state isolation enable concurrent calibration and reliable handover? Count all populations and couplings. |
| Shared parameters, separate states / cloned circuits | Can learned dynamics be reused while activity remains isolated? Distinguish tied parameters from copied parameters and copied state. |
| Alternating banks (flip-flop) | Can one bank attend while another tracks, then exchange roles without a reset or unauthorized state copy? Include stale-state and repeated-switch tests. |
| Columns or stacks | Can grouped or partially overlapping circuits support more concurrent roles? This is an organizational hypothesis, not a neuroscience claim. |

Begin with two live state instances as a tractable scaffold and a single-population
control; the protocol must justify an explicit attractor realization. An additional
primed cue may remain latent rather than consuming a full running circuit. Increase
the number of simultaneously tracked candidates only in a bounded, separately
budgeted comparison. Do not implement every topology in the initial sprint.

Physical separation here means separate recurrent populations or state storage,
not a requirement for separate processors. Record parameter sharing, active-state
bytes, cloned weights, coupling weights, step counts, peak simultaneous instances,
and scheduling latency. Cloning/copying can be useful scaffolding but is not evidence
of associative recall, learned transfer, or an emergent handover mechanism.

## 4. First milestone: cue-driven switching with grounded continuity

The next task is [SOAM-033](../tickets/SOAM-033-handover-protocol.md): select a small
candidate set and preregister a switching protocol. Engineering and trials follow
in SOAM-034/035; the new handover decision is SOAM-036. No research gate is passed
by this amendment.

Use a small simulated sensorimotor task with overlapping local observation domains,
a fixed sensory projection, and executed actions. Provide sufficient observability
for the initial test, then explicitly introduce ambiguous or missing observations.
Persistent parameters stay fixed during measured handover trials. Offline fitting
and hand-set dynamics are both allowed if their data and supplied structure are
reported. Rich encoders, learned decoders, and accurate long-horizon world modeling
are not initial prerequisites.

The primary questions are whether a cue can recruit the intended pattern, whether
it remains independently calibrated while another is attended, and whether control
of the representation can transfer without loss of relevant state. Include repeated
switches, misleading cues, no-cue controls, and perturbations of source and candidate.

Required comparisons:

- Explicit attractor candidate versus conventional recurrent prediction/control.
- Pre-tracked successor versus cold initialization versus reconstruction from the
  same available observation history at handover, with replay cost counted.
- A justified shared-population versus separated-state comparison under reported
  total parameter, active-state, sensory-exposure, and compute budgets.
- Cue coupling present/absent/shuffled, and sensory correction present/absent.
- Scripted target selection or oracle correspondence only as labeled controls.
  Measure cue response independently from a scheduler's explicit selection command.

Switch latency, false switching, source retention, successor calibration, and
post-switch continuity are primary. Simple grounded one-step/free short-rollout
prediction supplies a minimum usefulness check: a decoder must not hide collapse
or an incorrect internal state. Better encoders/readouts may later improve prediction,
but cannot substitute for successful switching or rescue a failed dynamics claim.

Freeze numerical success/failure thresholds, seeds, splits, observation budgets,
candidate count, and compute limits before confirmation trials. This scope document
does not invent those thresholds or claim that an untested topology will pass.

## 5. Attraction evidence is separate from successful routing

Specify the dynamical system, state variables, fixed/time-varying inputs, and target
set or trajectory family for every attraction claim. Recovery toward a point,
manifold, or cycle is not interchangeable with exact trajectory synchronization.
Measure perturbation recovery, cue completion, persistence after cue removal where
appropriate, and failure/collapse. Disclose any ongoing external forcing.

A controller selecting a buffer, a scripted state reset, tanh boundedness, and a
good predictive score do not establish attraction. An engineered attractor is a
positive control for mechanism feasibility, not a learned attractor or evidence
of self-organization. The handover gate must distinguish behavioral feasibility,
attractor evidence, and dependence on scaffolding. If only scripted routing works,
revise the mechanism before claiming cue-driven attractor switching.

## 6. Subsequent embodied scope

After a bounded handover proceed decision:

1. **Beliefs and instances:** independently move sensory/memory attention, retain
   competing interpretations, maintain compatible repeated instances, and test
   evidence correspondence and re-identification (SOAM-037). Shared weights must
   not imply shared instance state. Associative predictions cannot count again as
   independent sensory evidence.
2. **Early control:** introduce known goal costs and simple candidate search on the
   validated synthetic interface (SOAM-023/024). Actions may continue within one
   representation or across handovers; motor authority is separately arbitrated.
   Richer rendered-observation evaluation remains SOAM-019–022.
3. **Action memory:** source plus desired transformation/context cues a reusable,
   feedback-driven skill (SOAM-038). Source, motor phase, and prospective successor
   can evolve concurrently. Compare source-only, pair-table, relational retrieval,
   and ordinary controller references; test held-out pairs and inappropriate skill
   reuse under changed constraints. Fixed skill libraries are scaffolding, not
   discovered skills. A mandatory third attention beam is not adopted.
4. **Grounded learning:** choose a bounded write representation and credit-assignment
   contract only after those interfaces are exercised (SOAM-039), then implement its
   transaction invariants (SOAM-044) before evidence/replay infrastructure. Test acquisition
   and instance-specific exceptions against retention (SOAM-040/041). Reuse the
   transaction invariants, not an untested assumption that the old matrix update
   suffices. SOAM-004–010 remain a separate local-write/scoping comparison branch.
5. **Organization:** test predictive specialization/association adjustment at fixed
   capacity against frozen organization and ordinary replay (SOAM-042/043). Learned
   boundaries must be distinguished from supplied labels. Dynamic recruitment,
   growth, split/merge controllers, and diffusion/flow are deferred extensions;
   they cannot be silently added to hide saturation or failures.
6. **Integration:** combine the validated composition, sensing, control, acquisition,
   and organization branches in SOAM-027/028. Broader manipulation and richer sensing
   follow small simulated tasks. A full robot, language, and neuroscience equivalence
   are not initial requirements.

Learned scope translation and learned iterative consolidation remain candidates.
Their failure does not block unrelated switching, basic beliefs, or simple control.
They must outperform simpler alternatives on the problem they are intended to fix.

## 7. Claim map and scaffold removal

Retain H1–H8 and WP-00–WP-13 identifiers to preserve provenance; no ticket schema
change is required. New mechanisms are operational subquestions, not retroactive
changes to historical hypothesis wording.

| Existing claim | v0.2 operational question |
| --- | --- |
| H1: multiple regimes | Cue completion, concurrent states, and grounded handover; a separated circuit bank alone does not prove the original shared-substrate claim |
| H2: rapid acquisition | Grounded updates to circuit/association/instance memory after the interface is chosen |
| H3: limited interference | Evidence responsibility and generic-versus-instance credit, with beneficial sharing |
| H4: consolidation | Grounded replay and organization compared with more complex refinement |
| H5: reuse | Held-out circuit/instance/skill combinations with causal ablations |
| H6: belief recovery | Partial sensing, uncertainty, correspondence, and independently movable attention |
| H7: useful planning | Realized control benefit from current/successor states and reusable action dynamics |
| H8: cumulative learning | Improved subsequent acquisition with retained competence and finite resources |

Every protocol records a scaffold ledger: supplied patterns, basins, cue weights,
domain boundaries, correspondences, instance/role labels, selection schedules,
skill libraries, goals, and controllers. State which are frozen, fitted, or learned;
identify how each affects the claim. Remove one scaffold at a time after the basic
operation is measurable. Any simulator-derived label used as an oracle must be
isolated from the evaluated learner. No privileged future observation is permitted.

## 8. Migration and gate interpretation

The [priority tracker](../PRIORITIES.md) owns execution order and the
[roadmap](ROADMAP.md) maps packages to current work. M0–M8 remain thematic groups,
not a sequential calendar. M1 now includes a new, unfinished handover study alongside
the completed historical substrate controls. Existing decision outcomes are unchanged.

SOAM-032 records adoption of this scope only. SOAM-033 is the next bounded task.
SOAM-044 was allocated later to separate the future write-contract implementation
from replay and acquisition; its ID does not place it after integration.
SOAM-031 remains unfinished composition research; this amendment does not satisfy
its primary-source and mechanism-planning criteria. No unfinished legacy ticket
is closed by adopting v0.2. Dependencies changed for early belief/control and
composition are documented in their tickets. A planning decision may authorize
an experiment, but empirical integration gates still require measured evidence.

All experiments retain the v0.1 requirements for seeds, source/configuration hashes,
versions, data exposure, parameter/storage counts, compute, reproducibility,
independent train/development/test streams, negative outcomes, and no-write inference.
