# SOAM: Self-Organizing Attractor Memory

Architecture, theory, hypotheses, and experimental research plan

**Version:** 0.1
**Date:** October 25, 2026
**Status:** Historical v0.1 research specification — original interface freeze and execution order superseded by [v0.2](RESEARCH_SPEC_V0_2.md) on 2026-11-01. Original claims, experiment provenance, and gate decisions remain preserved below.

Source: the project owner's specification supplied at repository creation. This is a
Markdown transcription with normalized mathematical notation and compact prose;
all 23 sections, hypotheses, experiments, gates, and work packages are retained.
Operational choices for the first experiment live in `EXPERIMENTS.md`, not in this
interface-level specification. References below are supplied starting points, not a
completed literature review.

## 1. Executive summary

SOAM is a proposed architecture for continually learning embodied world models.
Rather than maintaining separate learned representations, memory databases, and
predictive models, it attempts to encode persistent knowledge directly in the
weights and dynamics of a recurrent neural network. Observations activate regions
of recurrent state space; actions drive transitions; behavioral contexts select
potentially overlapping dynamical regimes.

Knowledge acquisition has two complementary mechanisms:

- **Fast associative learning:** observed prediction error is translated by a learned
  scope translator into a bounded corrective weight update, preferentially affecting
  the dynamics responsible for the error.
- **Slow consolidation:** a learned iterative process revisits experience, tests
  candidate weight modifications with recurrent simulations, and improves coherence,
  stability, and reuse of learned dynamics.

An initially stable, frozen JEPA-style sensory encoder provides grounded features.
An action head proposes candidate actions, the recurrent model simulates their
consequences, and a goal evaluator selects useful trajectories. The objective is
persistent, compositional, reusable, navigable knowledge without explicit graph
management or repeated global retraining—not merely another recurrent world model.

## 2. Core research hypothesis

A shared recurrent dynamical substrate, updated through locally corrective
associative learning and simulation-guided consolidation, can organize accumulated
experiences into stable, reusable dynamical structures while preserving previously
learned behavior.

| ID | Hypothesis | Required evidence |
| --- | --- | --- |
| H1 | One substrate encodes multiple context-dependent regimes | Accurate transitions and robust context switching |
| H2 | Fast corrections acquire new transitions online | Rapid prediction-error reduction without global retraining |
| H3 | Learned scope translation limits functional interference | Better retention at matched new-task accuracy than unfiltered updates |
| H4 | Iterative consolidation improves organization | Better retention, prediction, or capacity than replay-only baselines |
| H5 | Consolidation discovers reusable transformations | Positive transfer to withheld contexts and action compositions |
| H6 | Partial observations recover latent context | Robust belief recovery under missing or ambiguous inputs |
| H7 | Recurrent planning improves control | Higher goal success than controlled reactive baselines |
| H8 | The system supports cumulative learning | Continued acquisition without unacceptable forgetting |

H1–H4 are foundational. H5 is the primary test of self-organization and compositional
reuse. H6–H8 establish relevance to embodied intelligence.

## 3. Architectural principles

1. **Persistent knowledge in dynamics:** no required graph of individually allocated
   object nodes. Persistent weights can support fixed points, limit cycles, manifolds,
   metastable trajectories, or other recurring patterns. An activity such as raking
   leaves may be a family of trajectories, not a stationary attractor.
2. **Actions change state evolution:** the primary prediction is a successor internal
   state; observation prediction is a readout of that state.
3. **Stable sensory representations:** initially freeze the sensory encoder to avoid
   invalidating associations through representation drift.
4. **Immediate recording:** fast local acquisition should not require full-network
   retraining after every observation; direct associative correction is the starting point.
5. **Functional plasticity scopes:** change the smallest useful subset of dynamics
   compatible with preservation; scopes can be distributed, overlapping, and shared.
6. **Grounded consolidation:** observed transitions, replay, and preservation tests
   must constrain consolidation. Internal simulation alone cannot establish physical truth.
7. **No learning from imagination by default:** planning changes temporary activity,
   not persistent weights. Grounded learning and explicitly validated consolidation
   alone may modify persistent parameters.

## 4. System architecture

### 4.1 Primary components

| Component | Responsibility |
| --- | --- |
| Sensory encoder | Stable features from observations, eventually video/touch/proprioception |
| Recurrent dynamical memory | Persistent knowledge in weights; transient internal state and beliefs |
| Context interface | Activity, goals, constraints; switches regimes without necessarily writing weights |
| Predictive readout | Recurrent state to expected sensory features |
| Action proposal head | Candidate actions from state, goal, and context |
| Goal evaluator | Trajectory goal progress, risk, and uncertainty |
| Fast associative writer | Immediate corrective update from grounded evidence |
| Learned scope translator | Route/filter writes to reduce interference and encourage useful sharing |
| Slow consolidator | Iteratively evaluate and refine proposed persistent changes |
| Episodic evidence buffer | Limited real observations, features, actions, context, outcomes; a validation reference, not a second world model |

### 4.2 Information flow

Real interaction:

1. Receive and encode observations.
2. Assimilate sensory evidence into the recurrent state/belief.
3. Propose actions and predict their successor states.
4. Evaluate imagined outcomes; choose and execute an action.
5. Observe the actual outcome and compute prediction error.
6. Apply a scoped associative update and record grounded evidence.

Slow consolidation:

1. Select recent and representative old experiences.
2. Construct provisional weights and simulate relevant action-conditioned trajectories.
3. Compare predictions with grounded evidence and quantify old-behavior disruption.
4. Generate further corrections.
5. Accept or reject according to validation criteria.

## 5. Mathematical model

### 5.1 Sensory representation

\[
z_t = E_\theta(x_t).
\]

Initially freeze the encoder. Early experiments use synthetic features or a fixed
projection. A frozen encoder need not preserve every variable needed for control.

### 5.2 Recurrent state dynamics

\[
h_{t+1}=F_W(h_t,a_t,c_t).
\]

An initial bounded baseline is

\[
h_{t+1}=(1-\alpha)h_t+\alpha\tanh(Wh_t+U_a a_t+U_c c_t+b).
\]

The leak \(\alpha\) sets the update timescale. This is a baseline, not the presumed
final attractor model. Compare additive context with gates and low-rank modulation;
additive input may inadequately distinguish regimes.

### 5.3 Sensory readout

\[
\hat z_{t+1}=D_\psi(\hat h_{t+1}),\qquad
 e_{t+1}=z_{t+1}-\hat z_{t+1},\qquad
 \mathcal L_{\rm pred}=\|z_{t+1}-\hat z_{t+1}\|_2^2.
\]

The readout must be calibrated to the recurrent representation; it need not be
frozen from initialization. Stochastic observations and incompatible futures may
require other latent objectives rather than averaging.

### 5.4 Sensory state correction

Predicted recurrent states and sensory features are different objects:

\[
h_{t+1}^{\rm obs}=A_\rho(\hat h_{t+1},z_{t+1},c_{t+1}).
\]

Start with projection and recurrent correction; later consider probabilistic
belief updates retaining competing hypotheses. Reality must correct internal drift.

### 5.5 Fast associative learning

A linear reference is

\[
\hat v=W_{\rm assoc}k,\qquad
\Delta W_{\rm raw}=\eta(v-\hat v)k^\top.
\]

The cue may combine state, action, and context; the target may encode observed
successor state or recurrent correction. This delta rule is not automatically
appropriate for every recurrent parameter. Test multistep stability explicitly.

### 5.6 Learned scope translation

\[
\Delta W_{\rm scoped}=G_\phi(h_t,a_t,c_t,e_{t+1},\Delta W_{\rm raw},S_t).
\]

\(S_t\) summarizes sensitivity or prior functional scope. Updates can be sparse,
masked, or low rank. Initially use \(\Delta W_{\rm scoped}=M_\phi\odot\Delta
W_{\rm raw}\), with a learned or heuristic gate. Later predict low-rank factors or
transform update directions themselves.

### 5.7 Functional preservation

For protected contexts \(q_i\), let \(R(W,q_i)\) denote predicted trajectories:

\[
\mathcal L_{\rm preserve}=\sum_i\omega_i
\|R(W+\Delta W,q_i)-R(W,q_i)\|^2.
\]

Preserving every old output can prevent legitimate corrections. Combine preservation
with actual observation targets, weighted by evidence reliability.

### 5.8 Slow consolidation

Starting from post-write provisional weights:

\[
W^{(k+1)}=W^{(k)}+\epsilon V_\omega(W^{(k)},C_k),
\]

where \(C_k\) includes replay, errors, protected behaviors, and other useful signals.

\[
\mathcal L_{\rm cons}=\lambda_1\mathcal L_{\rm grounded}
+\lambda_2\mathcal L_{\rm retention}
+\lambda_3\mathcal L_{\rm rollout}
+\lambda_4\mathcal L_{\rm complexity}.
\]

Seek weights explaining new evidence while preserving/improving useful dynamics.
Flow matching is an optional later extension.

### 5.9 Action selection and planning

\[
a_t\sim\pi_\phi(a\mid h_t,g,c_t),\qquad
\hat h_{t+k+1}=F_W(\hat h_{t+k},\hat a_{t+k},c_t),
\]

\[
J=\sum_{k=1}^{H}\gamma^{k-1}
[r(\hat h_{t+k},g)-\beta u(\hat h_{t+k})].
\]

Execute the first action of the best plan, observe, and replan. Initially use known
goal costs and simple candidate search; learn action proposals/critics only after
prediction is reasonably reliable.

## 6. Experimental methodology

Every experiment needs a precise hypothesis, controlled synthetic/simulated task,
simpler baseline, multiple random seeds, time- or context-separated train/evaluation,
explicit success criteria, diagnostic plots, and documented failures. Match memory,
compute, and data exposure where possible. Extra compute cannot silently count as
an architectural advantage.

Core metrics:

- One-step and multistep latent prediction error.
- Retention on earlier tasks and interference in protected behaviors.
- Observations needed to acquire changed dynamics.
- Divergent, invalid, or otherwise undesired trajectory frequency.
- Context recovery with incomplete observations.
- Transfer to withheld/new related tasks; goal-directed planning success.
- Behaviors stored under fixed capacity/error criteria.
- Operations, time, and memory per update.

## 7. Stage 0 — Infrastructure and reproducibility

Use Python and PyTorch. Separate synthetic environments, encoders, recurrence,
plasticity, consolidation, planning, evaluation, experiments, tests, scripts, and
reports. Make all experiments configuration-driven.

Deliver deterministic sequence generation, train/evaluation runners, parameter and
metric logs, weight-update/trajectory plots, comparison utilities, and reproducible
baseline configs. Weight-update diagnostics become active when writing is implemented.

**Exit:** identical seeds reproduce numerical results within expected tolerances;
every result traces to its configuration and commit.

## 8. Stage 1 — Recurrent dynamical substrate (H1)

**1A: Multiple regimes.** Synthetic 2D contexts: clockwise rotation,
counterclockwise rotation, rotation plus translation/nonlinear perturbation. Encode
through a fixed higher-dimensional projection. Train successor internal-state and
sensory-feature prediction. Compare independent context predictors, shared additive,
shared gated, and shared low-rank context modulation.

**1B: Switching.** Change context midsequence without resetting recurrent activity.
Measure trajectory adaptation speed and usefulness of retained state.

**1C: Perturbation recovery.** Perturb recurrent state and test return toward the
intended trajectory family. Distinguish trajectory recovery from fixed-point collapse.

**Exit:** accurate multistep prediction, reliable switches, bounded trajectories under
reasonable perturbations, evidence of useful shared structure. Independent baselines
must have equivalent total parameter budgets. Sharing alone does not establish reuse.

## 9. Stage 2 — Fast associative learning (H2)

**2A: Online correction.** Pretrain a substrate, freeze ordinary training, introduce
unseen transitions, and write designated recurrent parameters. Compare no adaptation,
Hebbian, delta-rule, local least-squares/RLS, and conventional online gradients.

**2B: Changed dynamics.** Change angular speed, friction, or another regime property;
measure adaptation speed.

**2C: No-reset learning.** Long sequences with revisits, context switches, and incremental
writes; measure retention and accumulated drift.

**Exit:** improvement after few observations, reliable multistep prediction, and explicit
advantages/trade-offs versus simple online baselines. If raw writes fail, revise the
update representation before advancing.

## 10. Stage 3 — Learned functional scope translator (H3)

**3A: Isolated correction.** Introduce one context-specific error, measure all contexts;
compare unfiltered delta, fixed sparse masks, random sparse masks, sensitivity masks,
and learned translation.

**3B: Overlapping scope.** Give A/C a shared rotation but distinct translations; modify
the shared primitive and test benefit to both. Complete task isolation is insufficient.

**3C: Novelty versus correction.** Present familiar/correct, changed, and noisy/misleading
transitions. Test redundant-update suppression, useful correction, and noise resistance.

Start with meta-training over synthetic families using tractable local statistics:

\[
\mathcal L_{\rm scope}=\mathcal L_{\rm new}
+\lambda\mathcal L_{\rm preserve}+\beta\|\Delta W\|_F^2.
\]

**Exit at matched new-task accuracy:** lower interference, beneficial shared transfer,
acceptable adaptation speed, and consistent multi-seed/task-family results. A 50%
reduction in old-task error increase is an illustrative target requiring validation.

## 11. Stage 4 — Slow memory consolidation (H4)

**11.1 Replay first.** Repeated corrective updates on recorded transitions establish
whether a sophisticated consolidator is needed.

**11.2 Constrained consolidation.** Evaluate candidate changes against recent/old real
observations, multistep action-conditioned rollouts, context switches, and stability.
Use shadow weights and commit only validated changes.

**11.3 Learned consolidation.** A recurrent generator proposes low-rank corrections
from provisional weights/compressed statistics, replay errors, scope/interference,
and prior consolidation outcomes. Consider truncated unrolled optimization/meta-learning.

**11.4 Flow-based consolidation.** Only after useful learned iterative correction,
learn weight-space trajectories from provisional to improved endpoints. Define
improvement explicitly and account for functionally equivalent parameterizations;
functional trajectory descriptors may be preferable to raw weight distance.

Experiments: **4A** sequential-context retention; **4B** repair of locally helpful but
globally disruptive writes; **4C** iterations/compute with observations held fixed;
**4D** capacity scaling in a fixed parameter budget.

**Exit:** improve retention, prediction, adaptation, or capacity without unacceptable
regressions; beat replay under a reported compute budget. Failure to beat replay is
evidence against the learned consolidator's necessity, not the entire architecture.

## 12. Stage 5 — Compositional self-organization (H5)

This is the decisive test of reusable organization.

**5A: Reusable transformations.** Rotate, translate, scale, reflect where applicable,
and apply context-dependent nonlinear maps; withhold compositions of known primitives.

**5B: Shared dynamics.** Sequential A=rotation+translation, B=translation+damping,
C=rotation+damping; compare C acquisition after A/B with independent learning.

**5C: Identity versus state.** Objects share dynamics but retain stable identity features.

**5D: Temporal abstraction.** Fast oscillations within slow trajectories and contexts;
look for reusable timescales without forcing an explicit hierarchy prematurely.

Distinguish memorization (seen transitions), interpolation (near trained states),
composition (withheld combinations), and transfer (faster/better genuinely new learning).

**Exit:** statistically reliable withheld-composition or related-task gains over matched
recurrent/associative baselines. Retention without transfer is memory maintenance,
not the stronger self-organization claim.

## 13. Stage 6 — JEPA integration and grounded recovery (H6)

Start with rendered shapes/simple simulated moving, rotating, interacting objects,
not natural video. Compare hand-designed state features, fixed random projection,
simple pretrained self-supervision, and suitable frozen JEPA-style encoders.

Train action-conditioned recurrent successor states and feature readout. Introduce
noise, occlusion, and missing frames; measure belief maintenance and recovery.
Create observations compatible with multiple hidden states; assess useful uncertainty
rather than premature commitment.

**Exit:** accurate grounded multistep prediction and partial-observation recovery better
than comparable recurrence without the proposed memory mechanisms.

## 14. Stage 7 — Action prediction and planning (H7)

Use exhaustive search/MPC over a small discrete space before learning action proposals.
Then consider goal-conditioned policy imitation, policy optimization, or imagined-rollout
actor-critic training. Begin with known state-based goal costs before a learned critic.

```python
state = assimilate_observation(observation)
plans = generate_candidate_action_sequences(action_head, state, goal)
for plan in plans:
    trajectory = simulate(world_model, state, plan, update_weights=False)
    score[plan] = evaluate(trajectory, goal)
execute(best_plan(score).first_action)
next_observation = observe()
learn_from_actual_transition()
```

Experiments: **7A** navigation after learning motion; **7B** changed motion/obstacles
and fast replanning; **7C** partly shared hierarchical activities; **7D** horizon and
candidate-count effects on success, error, and compute.

**Exit:** better goal completion than reactive policies, reliable replanning after
changes, no persistent writes during imagination, and an established connection
between model quality and planning success.

## 15. Stage 8 — Continual embodied learning (H8)

Progress from simple 2D tasks to richer simulated manipulation/navigation. Introduce
multiple objects, occlusion/re-identification, changed object dynamics, shared motor
primitives, activity contexts, unseen action compositions, and long interruptions.

Periodically measure old-task retention, new adaptation, fixed-capacity limits, transfer,
planning, consolidation cost, and stability. The central test is whether experience
improves learning of related new tasks, not simply the number of memorized examples.

## 16. Required baselines and ablations

| System | Purpose |
| --- | --- |
| Explicit graph/transition table | Structured-memory reference, explicitly a baseline |
| Ordinary RNN/GRU | Conventional recurrence |
| Independent task-specific RNNs | Reference avoiding cross-task interference |
| Shared recurrence with online gradients | Continual-learning reference |
| Associative recurrence without scope | Isolate fast writing |
| Associative memory with fixed masks | Isolate learned scope benefit |
| Scope without consolidation | Isolate localized plasticity |
| Replay consolidation | Simple slow-learning reference |
| Learned iterative consolidation | Test main consolidation hypothesis |
| Flow-based consolidation | Test additional generative refinement value |
| Reactive policy | Isolate imagination-based control benefit |

Ablate encoder, readout, action conditioning, scope translator, replay, and consolidation
independently. Equalize parameter counts and computation where possible; report mismatches.

## 17. Failure modes and contingencies

- **A — Unstable recurrence:** bounded activations, spectral/norm constraints, smaller
  writes, protect sensitive modes, gated/low-rank alternatives.
- **B — Poor successor dynamics after writes:** separate a fast adapter from fixed
  recurrence, local least-squares, online-gradient comparison. Fast local acquisition
  is required; a particular delta-rule formula is not.
- **C — Scope learns isolation:** deliberately shared tasks, transfer objectives,
  penalties for unnecessary exclusive allocation, beneficial-sharing examples.
- **D — Consolidation forgets:** shadow validation, better replay coverage, constrained
  low-rank changes, rollback/trust regions.
- **E — Memorization without composition:** withheld-composition objectives,
  transformation consistency, equivariance, explicit modular biases if needed.
  Predictive compression alone may be insufficient.
- **F — Unreliable long imagination:** shorter horizons, uncertainty costs, frequent
  replanning, multiple hypotheses, sensory grounding.
- **G — Fixed-capacity saturation:** measure efficiency/interference, then investigate
  sparse connectivity, controlled growth, compression, and forgetting policies.
  Characterize fixed-size systems before expanding them.

## 18. Implementation roadmap

| Package | Deliverable | Dependencies |
| --- | --- | --- |
| WP-00 | Experiment harness and baseline RNN | None |
| WP-01 | Context-conditioned regimes | WP-00 |
| WP-02 | Local associative writing | WP-01 |
| WP-03 | Behavioral interference metrics | WP-02 |
| WP-04 | Heuristic scope filtering | WP-03 |
| WP-05 | Learned scope translator | WP-04 |
| WP-06 | Replay consolidation | WP-03 |
| WP-07 | Learned iterative consolidation | WP-05, WP-06 |
| WP-08 | Compositional transfer benchmark | WP-07 |
| WP-09 | Frozen encoder interface | WP-01 |
| WP-10 | Grounded recurrent prediction | WP-09 |
| WP-11 | Action search and goal evaluation | WP-10 |
| WP-12 | Learned action proposal head | WP-11 |
| WP-13 | Continual embodied benchmark | WP-08, WP-12 |

Use small independently reviewable work packages with tests, metrics, assumptions,
and explicit completion criteria.

## 19. Research decision gates

1. **Representation:** represent and switch among useful regimes.
2. **Acquisition:** local writes improve predictions without global retraining.
3. **Scoping:** filter harmful interference while allowing beneficial transfer.
4. **Consolidation:** demonstrate advantage over replay.
5. **Composition:** reuse transformations beyond observed examples.
6. **Grounding:** observations cue and correct internal dynamics.
7. **Planning:** imagined trajectories improve action choice.

Interesting pictures are insufficient. Failed gates motivate targeted revision.
Persistent Gate 3 failure is especially serious because functional-scope learning
is central to the proposed novelty.

## 20. Theoretical questions for parallel research

- **Regimes:** conditions for stable/metastable regimes in one network; context-controlled
  transitions; which attractors support navigation?
- **Sensitivity/scope:** can local statistics estimate causal weight contributions and
  approximate update projections without full BPTT? Can protected scopes overlap?
- **Capacity/interference:** dependence on dimension, sparsity, rank, and horizon;
  precision versus generalization trade-offs.
- **Consolidation:** useful configurations inaccessible to local correction; sufficiency
  of replay; weight flows under parameter symmetries/equivalent functions.
- **Composition:** objectives for shared primitives; distinguishable identity,
  transformation, reference-frame factors; when explicit biases are necessary.
- **Planning/learning:** informative actions; observation uncertainty versus model
  inadequacy; planning gains from consolidation without direct policy optimization.

## 21. Literature and starting references

These user-supplied references are foundations/comparisons, not complete SOAM solutions.
The bibliography has not yet been independently reviewed in this repository.

1. Davis et al. (2021), *Compositional Memory in Attractor Neural Networks with One-Step
   Learning*. Recurrent attractor graphs, context-dependent transitions, rapid local
   learning. <https://www.cs.umd.edu/~grpdavis/papers/compositionality.pdf>
2. Schlag et al. (2021), *Linear Transformers Are Secretly Fast Weight Programmers*.
   Fast associative programming. <https://arxiv.org/abs/2102.11174>
3. Yang et al. (2024), *Parallelizing Linear Transformers with the Delta Rule over
   Sequence Length*. <https://arxiv.org/abs/2406.06484>
4. *Flexible Multitask Computation in Recurrent Networks Utilizes Shared Dynamical
   Motifs* (2024). <https://www.nature.com/articles/s41593-024-01668-6>
5. *V-JEPA 2 — Self-Supervised Video Models Enable Understanding, Prediction and
   Planning* (2025). <https://arxiv.org/abs/2506.09985>
6. *DreamerV3 — Mastering Diverse Control Tasks Through World Models* (2025).
   <https://www.nature.com/articles/s41586-025-08744-2>

Further review: learned plasticity, continual learning, fast/slow memory, recurrent
attractor theory, predictive coding, equivariance, constrained weight-space optimization.

## 22. Recommended immediate sprint

Focus exclusively on the substrate:

1. Synthetic context-conditioned environment with configurable actions.
2. Simple bounded recurrent transition model.
3. Accurate rollouts for at least two distinct regimes.
4. Context switching without resetting activity.
5. Perturbation recovery and instability measurement.
6. Report losses, one-step/multistep error, trajectories, switching, and stability.

Do not implement JEPA, learned scope, consolidation, or action expert in this sprint.
Ask whether the candidate substrate reliably represents and navigates regimes enough
to justify investigating online associative plasticity. If no, revise the substrate;
if yes, proceed to fast associative writing.

## 23. Final research position

SOAM is a hypothesis about acquisition, localization, reorganization, and reuse of
persistent dynamical knowledge. Its contribution would not be a new RNN alone, a
JEPA objective, or a planning policy, but their integration with immediate associative
writes, learned functional scopes, grounded consolidation, and cumulative reuse.

Object recognition or robotic control alone is not decisive. The evidence must show
that accumulated experience improves knowledge integration and transfer without
wholesale retraining or manual memory organization.

**Architecture v0.1 is frozen at the interface level. Mathematical mechanisms,
connectivity, learning rules, and consolidation algorithms remain experimental.**
