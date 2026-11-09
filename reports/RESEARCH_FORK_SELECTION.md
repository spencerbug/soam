# Research fork selection — SOAM-059

2026-11-09. **Decision: proceed to SOAM-039's E2 protocol design only.** Select
one minimal acquisition study using **G32 plus one bounded recurrent local-error
writer**, labeled as a conventional recurrent learner. The decisive architectural
question is whether writing into this predictive core earns its complexity over
keeping the core fixed and learning a small residual or retaining examples.
No E2 protocol is approved, writer implemented, data generated, or trial run here.

The [E1 study](SHARED_POPULATION_STUDY.md) and
[SOAM-052 stop decision](SHARED_POPULATION_GATE.md) remain authoritative and
unchanged. This selection does not promote S32, validate useful sharing, or resolve
the T32 identifiability limit. SOAM-059 is a completed, single-use routing decision;
it cannot later activate a second fork without a fresh decision and explicit edges.

## Evidence that permits this choice

Review base: `a4ddf9479fad06240a44030726ce6f99d2f25eb2`. The full study, gate,
historical [local-write report](LOCAL_WRITE_CONTRACT.md), current scope,
[hypotheses](../docs/HYPOTHESES.md), [routing rules](../docs/RESEARCH_PATHS.md),
and selected/deferred ticket conditions were reviewed before choosing a branch.
The following is an interpretation of existing evidence, not another E1 analysis
or a new result. The gate's complete tables and audits retain all comparisons.

| Audit dimension | Supporting artifact and finding | Constraint on this decision |
| --- | --- | --- |
| Validity and completeness | [Gate audit](shared-population-gate/audit.json), [study inventory](shared-population-study/confirmation/inventory.json): 42 development + 70 confirmation + 7 repeat fits, 27,820 cells; no scientific failures, exclusions, retries or seed replacements | A completed negative experiment can inform a different question; it cannot be called invalid merely because S32 failed |
| Provenance and reproduction | [Provenance](shared-population-study/confirmation/provenance.json), [resolved config](shared-population-study/confirmation/config.json), [reproduction](shared-population-study/confirmation/reproduction.json): frozen source and selected settings; exact repeat of 11,764 arrays, 7,280 input references and 9,603 records | Retain source/config distinction and all development selections. Repetition adds no independent root and is not cross-platform validation |
| Information parity | Gate checks 53,900 training references and 4,620 base scoring references; common masked sensing, role flags and action histories, no evaluator truth or future observations in free prediction | Preserve equal observations and disclose supplied task structure in E2; equal information does not mean equal capacity or compute |
| Outcome precedence | [Gate outcome table](SHARED_POPULATION_GATE.md#uncertainty-guardrails-and-outcome-precedence): S32 recall 0.077657, ordinary 95% root interval [0.068287, 0.086725], versus 0.02 maximum; every root fails | Governing outcome remains `recall_interference_or_failure`, specifically absolute recall failure; no rescue through a later utility or diagnostic result |
| Retention and uncertainty | Both adjusted relative retention guards pass; all six causal contrasts miss their precision caps. Neither the required-reference comparisons nor their widths establish frozen precise-no-benefit/equivalence | Do not infer destructive cross-function interference, causal absence, or equivalence. Joint fitting's recall improvement does not isolate a multitask effect: no equal-duration recall-only control was fitted |
| Predictive alternatives | [Complete statistics](shared-population-study/confirmation/statistics.json): G32 free-8 0.037692 [0.029909, 0.045716]; G28 0.046443 [0.039819, 0.052585]; S32 0.086825 [0.074820, 0.098609]. Both GRUs beat S32 in every root | There is a usable predictive starting point for protocol design, not evidence that a GRU can learn online or that its gates caused the advantage |
| Sharing and attraction | [Gate intervention and recovery sections](SHARED_POPULATION_GATE.md#shared-unit-intervention-evidence-and-t32): exact S32/T32 behavior and bank isolation; recovery usefulness fails despite contraction | Shared parameters and separate role states can produce identical intact behavior. E2 cannot establish uniquely useful physical overlap, global attraction or semantic neurons |
| Prior writing risk | [SOAM-003 report](LOCAL_WRITE_CONTRACT.md): immediate error decreased in all three demonstration seeds, but some held-out multistep errors worsened | Test persistent generalization and protected behavior before building scopes, replay or consolidation; do not transfer that writer's engineering verification to a GRU |

G32 was E1's **development-selected primary reference**, not a new winner chosen
by changing the primary horizon. Its development transition/recall errors
0.031548/0.015432 passed the reference competence screen (0.15/0.03). Its confirmation
recall 0.020987 [0.016440, 0.025873] does **not** certify the S32 recall maximum of
0.02. G28 has fewer parameters (3,988 versus 4,940) and a lower recall mean
0.019600, but its interval [0.016060, 0.023641] also crosses 0.02 and its primary
prediction mean is higher. These are reasons to retain the already selected G32
as one provisional substrate, not to run a G28/G32 search. G32's extra parameters,
all gates/readouts and 32-unit state must be counted. Fresh E2 competence and
identifiability checks remain mandatory; E1 does not pass them in advance.

The gate's conservative cumulative ledger is **2,906.209410 CPU seconds,
2,956.593458 wall seconds, 461.320613 overhead CPU seconds, and 680,181,226 artifact
bytes**. Measured peak RSS is 853,032,960 bytes. The original limits remain 14,400
CPU seconds, 28,800 wall seconds, 1,200 overhead CPU seconds, 2 GiB RSS and 8 GiB
artifacts. See the [original ledger](shared-population-study/confirmation/final-ledger.json)
and `conservative_cumulative_ledger` in the gate audit. **E1 is closed; unused
allocation is not permission for more E1 fits.** This routing review is documentation
and engineering verification outside the trial ledger, not a reset or new charge
to E1 scientific exposure.

Three reporting qualifications persist: the raw config hash identifies its capture
wrapper rather than resolved scientific settings; generic L12 exposure fields are
not gradient-update counts; and two failed reporting extractions lack separate RSS
measurements and the first terminal diagnosis. They were conservatively charged
177+44 CPU/wall seconds. No identified defect invalidates the numerical comparison,
but flawless end-to-end RSS compliance or resource efficiency is not established.

## Ranking the continuations

This is an ordinal judgment of decision value relative to work, not a numerical
estimate of expected information or a measured runtime comparison. Costs include
new interfaces, controls, auditing and confirmation, not just model fitting.

| Rank | Continuation | Architectural decision it could change | Implementation / compute burden and disposition |
| --- | --- | --- | --- |
| 1 | **Minimal acquisition: SOAM-039, G32 with one bounded writer** | Recurrent-core plasticity versus a stable predictor with a simpler adaptive memory; distinguishes persistent generalization from state calibration | Moderate: a changed-gain task, one GRU write adapter and four simple controls. Reuses fixed sensing, fitting and evaluator machinery. Hard allocation below; selected because a usable predictor and an identifiable low-dimensional task exist |
| 2 | Active disambiguation: SOAM-053 | Whether a frozen recurrent belief earns its cost over a same-data structured belief under informative actions | Moderate/high: new aliased task, model × policy controls, uncertainty calibration and closed-loop accounting. Valuable, but would leave the already observed write/generalization risk unresolved; unselected |
| 3 | One S32 diagnostic: equal-duration recall-only versus joint training | Whether the offline schedule, rather than cross-task benefit, explains the observed recall improvement; might motivate one future training revision | Lower implementation burden than E2, but fresh fitting/confirmation and its own protocol still required. Does not identify physical-overlap benefit or decide where new memories should be stored. No evidence of failed mean retention to justify partial-overlap rescue. No diagnostic selected or allocated |
| 4 | Simpler reference alone: linear/RLS predictor or bounded retrieval | Whether this narrow prediction task needs a recurrent learner at all | Low/moderate. L12 is mixed: free-32 0.057183, but grounded-32 0.329105 and recall 0.087339; secondary horizon cannot replace free-8. Strong simple learners are mandatory *within E2*, avoiding a separate baseline-only experiment |
| 5 | Stop additional research now | Commit to the existing negative boundary without testing acquisition | Zero implementation/trial cost and a legitimate option. Not selected because a small, distinguishable acquisition question remains; it becomes the fallback if that question cannot be specified or afforded without expanding this envelope |

Shared concurrency (SOAM-037) is **ineligible**, not a lower-ranked experiment:
it needs SOAM-052 proceed, which is absent. Recurrent attention (SOAM-045) is
deferred: recall failure motivates a question, but E1 does not isolate a retrieval
mechanism that attention would fix; a new backend would mix mechanism and training
changes. The learning-module extension (SOAM-056) needs SOAM-041 proceed and fresh
selection. Historical writer/handover and encoder work retain their statuses but
are not selected by this decision. No corrective diagnostic ticket is created.

## The single selected continuation

**Owner:** [SOAM-039](../tickets/SOAM-039-grounded-memory-design.md), next eligible
at P0/ready, xhigh. Its required RFC/protocol remains
`docs/SHARED_POPULATION_LEARNING_PROTOCOL.md` with a new versioned E2 manifest.
Those artifacts are not created or frozen by this routing record. SOAM-039 must
review the exact equations, interfaces, numerical criteria and finite inventory
before any implementation in SOAM-044. SOAM-040 measures it; SOAM-041 judges it.
These are stages of this one branch, not four automatically active tickets.

**Candidate:** G32 with E1-selected offline configuration 1 (learning rate 0.003,
100 recall-only + 300 joint updates, batch 16), refitted on fresh base-training
streams. No architecture or offline hyperparameter search. One local, normalized,
bounded error-correction rule may write only the 32×32 candidate-state block of
`gru.weight_hh`. Input weights, reset/update-gate blocks, biases, initializer,
readout and sensing stay fixed during online acquisition. The proposed rule maps
observed successor-feature error through the fixed readout and local GRU derivative
to a bounded outer-product correction. This is a candidate for SOAM-039 to specify
and falsify, not an implemented or verified GRU writer. It is neither the historical
low-rank writer nor a validated associative attractor mechanism. If a sound rule
cannot be defined in this scope, SOAM-039 must revise/stop, not silently substitute
S32, a new core or an external fast-weight architecture.

**Task:** change one scalar gain multiplying the first translation command in
the E1-style two-dimensional transform, with the same fixed 12-feature projection.
Freeze the gain range, nonzero excitation and held-out state/action cells in E2.
The changed family is supplied to every learner; the actual gain, latent state,
projection inverse and evaluator targets are not inference inputs. Grounded updates
receive the same observed before/action/after feature records. Fully observed
calibration pairs use nonzero affected command `a1`, with rotation command `a0`
and other translation command `a2` zero. Under the supplied transform family,
`z_next - 0.98*z = a1*b_g`: the observable coefficient vector `b_g` is identifiable
without supplying the projection or latent position. It is the projected effect
of the changed scalar gain, not an inferred semantic neuron or arbitrary dynamics.
SOAM-039 must formalize this identifiability argument and how baseline coefficients
are learned from counted offline observations; held-out actions must test beyond
the calibration command and input point.
An arbitrary unknown transition function is not identifiable from one example.
Hold the gain fixed within each adaptation episode and reset to the same base
checkpoint between episodes, preventing accumulation of earlier changed-gain data.

Evaluate new states and commands after **0/1/2/4/8/16 distinct transitions**, with
no writes or evaluation-target access. Reset transient state and reinitialize from
a permitted new cue while preserving the learned parameters or reference store.
Protect feature recall and transitions with the affected command set to zero.
This measures retention of **unaffected behavior**, not simultaneous retention of
contradictory old and new gains under an identical cue. Full regime/context retention,
learned routing and continual task sequences remain deferred. Evaluation under full
versus masked cues must be explicit; neither may be silently swapped to rescue error.

**Five conditions, not a backend sweep:** the candidate writer; the same G32 with
no writes; an RLS action-residual learner on the frozen G32; an ordinary one-step
online-gradient learner on the same writable block; and bounded observed-transition
retrieval with a frozen G32 fallback. RLS is the selected delta/RLS-family reference,
not a sixth arm. All receive the same priors and grounded schedule. Freeze each
reference's update/readout rule and verify competence rather than handcuffing it
to the candidate's proposal algebra. Count parameter deltas, RLS sufficient
statistics, at most 16 stored transition records per adaptation episode, snapshots,
rollback copies, history reads, offline fitting and all repeated uses. An external
learner is a labeled alternative, not shared recurrent acquisition. No optional
replay arm, extra capacity, learned scope or consolidation is included.

**Decisive endpoint:** normalized held-out free-8 acquisition-error area over the
fixed *linear* observation-count axis, after state reset, paired by independent
root. SOAM-039 must adopt or justify the review's proposed ≥20% reduction against
the strongest adaptive reference, with multiplicity-aware intervals and a frozen
precision cap, and a protected-task NMSE-increase upper bound ≤0.005. Report every
mandatory comparison, not only the best-looking one. Separate absolute competence,
grounded one-step and free-32 guardrails, harmful writes, and exact reset persistence.
A one-shot claim separately needs ≥20% improvement after one distinct observation
versus no-write and a positive advantage over adaptive controls, under frozen
uncertainty rules. No replay or repeated target optimization can count as one shot.
These are routing requirements/proposed review margins; SOAM-039 owns their exact
normalization, family-wise error, precision and outcome precedence before fitting.

## Finite allocation, fresh data and stopping

This is a **new proposed branch ceiling**, not a runtime forecast or an E1 extension.
SOAM-039 may tighten it. If the mandatory study cannot fit, it must record revise/stop
and seek a fresh routing decision; it may not increase the ceiling or drop a required
control to fit. No part is spent on experiments by SOAM-059.

| Resource | Maximum for the entire E2 branch, including failed attempts |
| --- | --- |
| Scientific CPU / wall | 3,600 CPU seconds / 7,200 elapsed seconds, single CPU worker; no GPU or parallel trial workers |
| Memory / artifacts | 2 GiB peak process RSS / 2 GiB cumulative artifacts, including failed outputs and reports |
| Offline neural fits | 16 total: at most 2 fixture/calibration, 3 development, 10 independent confirmation roots, 1 exact repeat; no fit replacement. Reuse each root's base fit across its five learning conditions |
| Offline exposure per fit | At most the E1 selected schedule: 6,400 recall records and 4,800 eight-transition episodes (38,400 transitions); no additional pretraining or grid. Separate normalization stream at most 2,048 base-train records |
| Online tuning | At most 2 fixed configurations per adaptive condition on the 3 development roots; no-write has one. No confirmation selection, additional rules, or post-result threshold search |
| Changed-dynamics exposure | At most 20 adaptation episodes per root, each with 16 distinct new transitions, shared across conditions/configurations; 4,800 distinct pairs across the 15 non-repeat roots at maximum inventory. The repeat reuses its original pairs |
| Evaluation | At most 20 held-out query trajectories per adaptation episode, observation budget and task slice (changed dynamics, unaffected transitions, recall); horizons at most 32, with free-8 primary. SOAM-039 must enumerate all grounded/free/reset comparisons inside the runtime/storage cap |
| Reproduction | One prescribed confirmation root, all five conditions and required numerical outputs; counts against every applicable cap, adds no independent sample |

The compute ceiling is a deliberate small-study limit. E1's largest new fit cost
36.121810 CPU seconds; multiplying that observed cost by 16 gives about 578 seconds
for base fits, leaving most of the proposed hour for adaptation, scoring and audits.
That is only a planning comparison: it does not predict E2 timing or establish
feasibility. The new write/control workload and complete archive must be calibrated.

Calibration, fitting, online updates, scoring, inference, diagnostics, reproduction,
archive/audit/report work and failed trial attempts share the same cumulative CPU,
wall and artifact limits. A future preflight must project the **whole** inventory
with a declared safety margin and capture RSS, then freeze reviewed source. Routine
unit tests and this documentation review are engineering checks, not scientific
trials; their costs are not evidence of scientific efficiency. No unused phase
allowance refunds failed work or authorizes extra seeds. These maxima are intentionally
more specific than a generic compute budget, but do not replace the E2 manifest.

All E1 development and confirmation evidence is now exposed and may motivate this
design only. Use a distinct E2 protocol/version namespace and disjoint train,
development, confirmation, diagnostic and fixture stream keys. Freeze the exact
root list and seed/component derivation before fitting; fresh base models as well
as changed-gain observations and scoring trajectories are required. Reusing E1's
architecture, selected settings and fixed sensing is disclosed prior knowledge;
reusing E1 checkpoints or scoring episodes as unseen E2 evidence is prohibited.
Pair methods on identical observations, hold scoring states/actions out of online
updates, and aggregate uncertainty at independent roots rather than transitions
or repeated reset probes. Ten roots are a ceiling, not a guarantee of precision.

Stop at the earliest applicable boundary:

1. **Protocol:** if identifiability, fair controls, a fresh baseline competence
   screen or a whole-study budget cannot be specified within this envelope,
   SOAM-039 records revise/stop. No implementation or scientific data generation
   follows merely from SOAM-059 proceed. Later development must pass the frozen
   competence/nontrivial-learning screen before confirmation; no new core or
   gain range may be selected using confirmation outcomes.
2. **Engineering/preflight:** reject leakage, broken reset/no-write ownership,
   unsafe/nonfinite updates, rollback failures or an over-budget projection before
   confirmation. Freeze equations, thresholds, selected development settings,
   inventory and reviewed source; do not spend confirmation to debug them.
3. **Execution:** a hard limit or scientific validity failure stops execution under
   the owning protocol. Retain failed seeds and all charges; record exact invalid
   or incomplete status. No replacement, rescue tuning or extension.
4. **Inference:** adequate negative evidence stops the tested recurrent-write claim;
   poor precision remains inconclusive. A simple reference winning redirects belief
   toward a stable core with simpler memory, without asserting all recurrent writes
   impossible. Only a precise retained advantage supports this narrow writer on
   this task. SOAM-041 reviews the result; even success requires a fresh routing
   decision before any next experiment or integration.

## Eligibility and architectural consequences

| Ticket / branch | Dependency and body-condition audit | State after this decision |
| --- | --- | --- |
| SOAM-059 | SOAM-051 done; complete E1 and SOAM-052 done/stop reviewed; no positive sharing dependency | done/proceed, selecting E2 protocol design only |
| SOAM-039 | SOAM-047 done/proceed and SOAM-059 done/proceed; explicitly named E2 selection | **ready, P0, xhigh**; design not started here |
| SOAM-044 / 040 / 041 | Need SOAM-039 proceed, implementation and measured evidence respectively | backlog; no protocol, implementation, experiment or acquisition gate completed |
| SOAM-053 / 045 | Ordinary dependencies can be complete, but named E3/attention selection is absent | backlog; do not infer eligibility from the DAG alone |
| SOAM-037 and sharing-dependent control/composition/organization | SOAM-052 is stop; its proceed condition remains unsatisfied | backlog; no edge bypass or rewritten gate |
| SOAM-056 and application descendants | No module selection and SOAM-041 not complete/proceed | backlog |
| SOAM-004 / 019 / 030 / 035 | Historical/supporting readiness unchanged | ready at P2, not selected or started |

Architectural beliefs should change in two ways. First, ordinary recurrence is a
serious substrate choice, and new learning should have to outperform a competent
simple memory rather than inherit priority from the SOAM name. Second, persistent
acquisition and protection deserve a small direct test before more infrastructure.
The cause of S32's poor recall, the role of GRU gating, uniquely useful physical
overlap, useful attraction, context retention and online learning superiority remain
unresolved. This routing choice supplies no new empirical support for them.

Recommendation traceability: **essential next** is SOAM-039's bounded E2 design
(R4/R6/R11/R12); **parallel research** remains unactivated, focused SOAM-030 support
on a concrete protocol question (R8); active disambiguation (R5/R6), concurrency,
attention, learned scopes/organization and integration remain **deferred capabilities**.
The one-diagnostic-per-failure allowance is unused and is not preauthorization.

## Verification and publication flag

Baseline `uv run pytest`: **190 passed in 17.59s** before edits. This is a
documentation/decision change only. Final ticket validation, changed-link checks,
metadata/body-condition review and preservation checks are recorded in
[verification.json](research-fork-selection/verification.json). The original
E1 source, protocol/manifest/A1, selections, ledgers, empirical reports and completed
gate tickets remain unchanged. No experiment, remote issue or publication occurred.

The Qwen read-only extraction job `1d3c4b21824c4fce8adc19f3d4f055bd` returned no
usable findings or requested citations. It was rejected; relevant ticket conditions
were read directly. The primary agent chose this route. No worker edited files,
ran trials or approved its own actions.

**Joint blog/report flag:** following a negative sharing gate with an ordinary
recurrent predictor and strong simple learning controls is a substantive change
in research direction. A future joint piece could explain why prediction, persistent
acquisition, protection and attraction require separate evidence. The measured
foundation is E1/SOAM-052; G32 writing and the changed-gain task are proposals, not
results. Nothing is published by this flag.
