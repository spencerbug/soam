# Analyze GRU Research Paths

**User:** Anonymous  
**Created:** 11/10/2026 7:25:06  
**Updated:** 11/10/2026 14:34:29  
**Exported:** 11/10/2026 15:12:41  
**Link:** [https://chatgpt.com/g/g-p-692551df89a081919fa575964c0c92ec-cortical-column-ai/c/6af31b31-7d20-83ea-849c-e159deaf0d7b](https://chatgpt.com/g/g-p-692551df89a081919fa575964c0c92ec-cortical-column-ai/c/6af31b31-7d20-83ea-849c-e159deaf0d7b)  

## Response:
11/10/2026, 7:47:17 AM · gpt-6-thinking

I’ll turn the research directions into sequential, copy-ready Codex assignments. I’ll check the E1 posts first so the prompts preserve the actual baselines, metrics, and experiment conventions, then specify controls, acceptance criteria, and artifacts for each stage.

> **Reviewing the research request**
>
> I’m identifying the exact reports, repository materials, and implementation constraints before drafting the prompt. I’ll keep the result focused on reproducible browser automation, evidence capture, and clear success criteria.
>
> **Reviewed the research request**
>
> 
>
> **Searched 3 websites**
>
> 
>
> **Planning experiment prompts**
>
> I’m organizing the work into sequential prompts: first a preflight, then five studies, followed by synthesis. I’ll distinguish completed baseline work from new experiments and require evidence capture, reproducibility, and explicit stopping criteria.
>
> **Structuring the research plan**
>
> I’m separating the work into sequential prompts so Codex can inspect the repository, select one justified fork, and run only the authorized experiment at each stage. I’m also avoiding ambiguous study IDs that could conflict with existing repository terminology.
>
> **Clarifying the research sequence**
>
> I’m treating these as separate, reversible stages: repository audit, fork selection, then one experiment at a time. Each stage should preserve the completed baseline, define controls, record provenance, and stop if the evidence fails its preregistered decision rule.
>
> **Designing the experiment sequence**
>
> I’m keeping the prompts sequential and reversible. I’ll have Codex preserve the completed baseline, resolve repository terminology, preregister controls, match compute budgets, and stop after each experiment for an evidence-based decision.
>
> **Planned and structured the experiment research sequence**
>
> 
>
> **Sequencing research prompts**
>
> I’m organizing the work into consecutive prompts so the agent can inspect the repository, preserve the completed baseline, select one justified fork, and run only the experiment currently authorized.
> 
> ```text
> # Prompt 0 — repository preflight and fork selection (DONE)
> 
> You are working in the SOAM repository. Before changing code or running expensive jobs, inspect the actual checkout, repository guidance, current branch, working tree, open tickets, experiment registry, and existing reports. Do not assume that published results and the current checkout are identical.
> 
> Read the completed E1 materials and confirm what is genuinely frozen, including configuration, seeds, train/test splits, model variants, metrics, checkpoints, plots, and provenance. Treat the existing E1 holdout as historical evidence if it has already been inspected. Do not silently reuse it as an untouched confirmation set.
> 
> Read and reconcile the repository’s existing experiment labels. Do not introduce ambiguous IDs such as “E2” or “E3” if those identifiers already refer to different work. Propose a temporary follow-up name, then use the project’s canonical naming convention only after checking the registry.
> 
> Run the smallest relevant baseline checks first. Record the exact commit, environment, configuration, dataset or generator version, and commands. Do not modify frozen E1 artifacts. Any change to shared utilities must be separately justified, tested, and reversible.
> 
> Create a short research decision record containing:
> 
> 1. What E1 established.
> 2. What E1 did not establish.
> 3. Which claims are descriptive rather than mechanistic.
> 4. Which proposed fork is currently most informative.
> 5. The smallest experiment that can distinguish the competing explanations.
> 6. The expected compute and storage budget.
> 7. The preregistered success, failure, and inconclusive outcomes.
> 8. The artifacts that must be produced before the next prompt.
> 
> Use the following current research questions as candidate forks, not as permission to run all of them:
> 
> - Whether gated recurrence provides a real advantage over matched non-gated recurrence.
> - Whether structured prediction and correction improve performance under sparse or unreliable observations.
> - Whether multiple persistent hypotheses help with ambiguous or switching contexts.
> - Whether fast plasticity helps acquire new object or sensor associations without changing slow weights.
> - Whether action-conditioned object and spatial prediction supports minimal navigation.
> 
> Before implementing anything substantial, select exactly one fork and explain why it has the highest information value after E1. If the repository is incomplete, inconsistent, or unable to reproduce the baseline, stop and report that instead of extending the experiment.
> 
> Do not treat biological analogies as evidence. For each analogy, write a testable computational hypothesis and identify an alternative explanation. Keep all conclusions proportional to the measured task.
> 
> At the end, report only the preflight findings, selected fork, planned design, and blockers. Do not launch the entire research program.
> ```
> 
> ```text
> # Prompt 1 — testing the gated-recurrence claim
> 
> Design and run one bounded follow-up study testing whether adaptive gating itself explains the observed retention or recall behavior.
> 
> First reproduce the relevant historical baseline from the repository. Then create a fresh confirmation split or generator seed that was not used to choose the design. Preserve the original task, observation protocol, training budget, optimizer family, evaluation procedure, and reporting conventions unless a deliberate change is documented.
> 
> State competing hypotheses before training:
> 
> - Adaptive gating provides a benefit beyond parameter count, width, optimization, and task simplicity.
> - The apparent benefit is explained by capacity, effective time constant, training dynamics, or the unusually low-dimensional task.
> - The result depends on the particular cue, action schedule, or role assignment rather than gating as a general mechanism.
> 
> Use matched comparisons including, where supported by the repository:
> 
> - A standard gated recurrent baseline.
> - A plain recurrent model with matched hidden-state size.
> - A fixed-leak or leaky-tanh model.
> - A non-gated model with a learned or fixed integration rate.
> - Update-only and reset-only gate ablations.
> - A wider non-gated model matched by parameter count.
> - A simple low-dimensional or structured-state reference model.
> - A larger gated model only as a capacity reference, not as the primary comparison.
> 
> Ensure that gate ablations are trained from scratch. Do not rely only on clamping gates after training, because that confounds mechanism removal with distribution shift. Post-training interventions may be included as secondary diagnostics.
> 
> Use paired seeds and a fresh test set. Keep model-selection data separate from confirmation data. Match training steps, optimizer opportunities, parameter budgets, hidden-state dimensions where meaningful, and evaluation compute. If exact matching is impossible, report the mismatch and analyze it rather than hiding it.
> 
> Measure more than one recall number, including:
> 
> - Recall after short and long unobserved intervals.
> - Normalized state or prediction error over time.
> - Reacquisition after a new observation.
> - Performance after controlled hidden-state perturbations.
> - Robustness to cue noise, wrong cues, action variation, and longer gaps.
> - Stability during free-running prediction.
> - Gate statistics conditioned on action, cue, role, and task phase.
> 
> Treat gate correlations as diagnostics, not proof of causality. Add controlled interventions where feasible, such as holding the same hidden state while changing the action or cue, or replacing a learned gate with a matched constant gate. Document exactly what is held fixed.
> 
> Preregister a practical effect criterion before confirmation testing. Choose the margin using the historical E1 variance and task scale, not a convenient result. Require uncertainty intervals and report null or inconclusive outcomes. Do not declare a mechanistic win because one metric improves while stability, robustness, or compute cost worsens.
> 
> Produce:
> 
> 1. A machine-readable run manifest.
> 2. Configurations and seeds.
> 3. Training and evaluation logs.
> 4. Gate and state diagnostics.
> 5. Aggregate metrics with uncertainty.
> 6. A comparison table against the historical E1 result.
> 7. A failure analysis.
> 8. A decision record stating whether the evidence supports gating, supports an alternative explanation, or is inconclusive.
> 
> Stop after this study. Do not begin scheduling, multi-hypothesis, plasticity, or navigation work in the same run.
> ```
> 
> ```text
> # Prompt 2 — testing prediction and correction scheduling
> 
> Design one bounded study of how an agent maintains state when observations are intermittent, delayed, noisy, masked, or contradictory.
> 
> Keep physical time separate from internal computation. Define the timestep semantics explicitly:
> 
> 1. Predict from the current state and action.
> 2. Apply the commanded transition.
> 3. Evaluate prediction before correction.
> 4. If an observation is available, assimilate it.
> 5. Record the corrected state without granting access to future information.
> 
> Compare fixed observation schedules such as every step, every two steps, every four steps, every eight steps, and a variable-gap schedule. Include missing observations, fresh observations, noisy observations, partial observations, and deliberately misleading observations. Preserve the same underlying trajectories across comparable conditions.
> 
> Compare a small set of clearly defined update rules:
> 
> - Simultaneous action and observation processing.
> - Predict-then-correct.
> - Snapshot, settle, then act.
> - A learned correction gain.
> - A fixed correction gain.
> - A no-write or no-correction control.
> - A simple reinitialization-from-observation control where applicable.
> - A classical or structured filter only if its assumptions and access to ground truth are explicit.
> 
> Do not allow extra internal settling steps to masquerade as extra physical time. Report both wall-clock or operation cost and performance. If one method gets more computation, include a compute-matched comparison.
> 
> Use a model such as:
> 
> `h_pred = F(h, action)`
> 
> followed, when an observation exists, by a correction whose inputs include the prediction, the observation residual, and an explicit availability mask. Keep action and observation masks separate. Include a no-observation condition that verifies the correction pathway cannot write state when no observation is present.
> 
> Evaluate:
> 
> - Prediction error before correction.
> - Correction error after assimilation.
> - Error area over each observation gap.
> - Reacquisition speed.
> - State snap magnitude.
> - Stability under wrong or contradictory cues.
> - Performance after long gaps.
> - Performance when observation quality changes.
> - Benefit per observation and per unit compute.
> 
> Include controls for observation exposure, number of internal updates, action schedule, trajectory difficulty, noise level, and parameter count. Do not use a full hidden state or future observation as an implicit oracle.
> 
> Before running the confirmation set, freeze the gap schedule, noise conditions, primary metric, practical effect threshold, and stopping rule. Use fresh trajectories and paired seeds. If scheduling helps only because it receives more observations, more updates, or a cleaner signal, label that as the explanation.
> 
> Produce reproducible artifacts, a timing diagram, an information-access audit, results by gap and noise condition, compute-normalized comparisons, and a decision record. Stop after this study.
> ```
> 
> ```text
> # Prompt 3 — testing persistent multiple hypotheses
> 
> Design a minimal ambiguity task that distinguishes maintaining several plausible explanations from merely increasing hidden-state capacity.
> 
> Use two or three candidate hypotheses with overlapping sensory features. Keep the task small enough to diagnose. The candidates should differ in reference frame, identity, object association, or context, but the model must not receive the correct identity as an input label.
> 
> Define the task so that partial observations genuinely leave alternatives plausible. Later actions, observations, or context should sometimes resolve the ambiguity. Include trials where:
> 
> - One candidate is correct.
> - Several candidates remain plausible for a long interval.
> - A previously inactive candidate becomes relevant.
> - The observation is misleading or missing.
> - Similar local features belong to different persistent objects.
> - The correct hypothesis changes after an explicit context transition.
> - No candidate should be selected with high confidence.
> 
> Compare:
> 
> - One recurrent state.
> - A centralized model with a larger matched state budget.
> - Independent recurrent states with shared parameters.
> - Independent recurrent states with separate parameters.
> - A tied multi-hypothesis model with an explicit soft weighting mechanism.
> - A hard-selection or winner-take-all control.
> - A simple structured filter or candidate bank, when feasible.
> 
> Match total state, parameter, and compute budgets. Report whether gains come from extra slots, extra processing, or better selective updating. Include a uniform-tracking control so selective attention is not compared only against an intentionally weak alternative.
> 
> Measure:
> 
> - Current-hypothesis accuracy.
> - Inactive-hypothesis retention.
> - Re-identification after delayed reattention.
> - Switching latency.
> - Forgetting and cross-hypothesis contamination.
> - False matches and false rejection.
> - Confidence calibration.
> - Performance when a hypothesis is never attended.
> - Compute and memory cost.
> - Performance under action-coupled updates while some hypotheses are unattended.
> 
> Avoid claims that a soft gate represents a specific biological mechanism unless the experiment directly tests that claim. Treat attention, processing allocation, and confidence weighting as distinct possibilities. Do not infer an internal “object” merely from a successful output; inspect whether the model preserves the relevant information under perturbation.
> 
> Use fresh generated trials, held-out combinations, controlled cue overlap, and paired seeds. Freeze the ambiguity schedule, primary metric, practical effect margin, and decision rule before confirmation. A result is positive only if multiple-hypothesis maintenance improves delayed resolution or retention beyond matched capacity and compute controls.
> 
> Produce the task specification, information-access audit, model diagrams, per-hypothesis diagnostics, failure cases, and a decision record. Stop after this study.
> ```
> 
> ```text
> # Prompt 4 — testing fast plasticity
> 
> Design a bounded study of rapid acquisition of new associations while slow parameters remain unchanged.
> 
> Separate the following mechanisms:
> 
> - A frozen slow recurrent model.
> - An explicit associative memory.
> - A prototype or key-value memory.
> - A Hebbian or delta-style update.
> - A recursive least-squares or online linear update.
> - A prediction-error- or novelty-gated write rule.
> - A confidence- or reliability-gated write rule.
> - A no-write control.
> - A rehearsal or fine-tuning control, clearly labeled as changing slow parameters.
> 
> Construct tasks in which the dynamics remain familiar but the sensor-to-object, feature-to-location, or object-to-action association is new. Generate held-out objects, trajectories, distractors, and feature combinations. Avoid trivial unique identifiers that reveal the answer immediately.
> 
> Specify whether fast memory is an explicit store, a temporary state, an external table, or a parameter update. Count storage, write operations, retrieval operations, and compute. During free imagination or prediction without observation, prohibit unannounced memory writes.
> 
> Evaluate:
> 
> - Acquisition after one, two, and several observations.
> - Retention after state reset.
> - Retention after learning additional objects.
> - Interference and collision.
> - False writes under noise.
> - False familiarity for unknown objects.
> - Out-of-distribution combinations.
> - Memory lifetime.
> - Capacity as the number of stored items grows.
> - Performance per memory byte and per update cost.
> - Performance when observations are contradictory or unreliable.
> 
> Use counterfactual no-write trials to show whether the system can predict without silently updating. Include a state-reset test that leaves learned slow parameters unchanged. Verify that the model cannot solve the task by merely memorizing generator identifiers or exploiting a fixed ordering.
> 
> Freeze the write rule, memory budget, primary metrics, and practical effect threshold before confirmation. Use independent objects and fresh combinations for testing. A positive result requires faster or more reliable acquisition than controls while preserving old associations and respecting the stated storage budget.
> 
> Produce memory traces, write and retrieval logs, collision examples, capacity curves, ablations, run manifests, and a decision record. Stop after this study.
> ```
> 
> ```text
> # Prompt 5 — testing action-conditioned object navigation
> 
> Start with the smallest navigable object task. Do not begin with a broad autonomous-agent claim.
> 
> Use nested tiers:
> 
> 1. Object pose estimation with egomotion and occlusion.
> 2. Landmark calibration and loop closure.
> 3. Independent object motion and egomotion, so the two sources of change can be separated.
> 4. Held-out compositional combinations as a later stretch tier.
> 
> Represent objects through observable feature slots or rendered observations. Provide commanded actions and any explicitly allowed timing information. Do not provide object identity, true pose, world coordinates, or hidden geometry as model inputs. Use ground-truth identity and pose only for scoring.
> 
> The model should predict observations or features under action and update object-related state when new evidence arrives. Define carefully whether an object is stationary, moving independently, occluded, or replaced. Include local-feature collisions so active exploration can disambiguate objects rather than receiving an obvious identifier.
> 
> Compare:
> 
> - A standard recurrent baseline.
> - A gated recurrent baseline.
> - A structured state estimator.
> - A simple graph or landmark memory.
> - A particle or hypothesis filter using the same available observations.
> - A model with explicit egomotion input.
> - A model without egomotion input.
> - A controlled observation-only model.
> 
> Treat any filter using known dynamics, privileged geometry, or oracle correspondence as an upper bound, not a fair learned baseline. Match observation exposure and action budgets.
> 
> Measure:
> 
> - Relocalization after an observation gap.
> - Identity and pose accuracy.
> - Prediction error before new evidence.
> - Correction error after new evidence.
> - Performance under viewpoint change and occlusion.
> - Egomotion and object-motion disentanglement.
> - Robustness to identity swaps and feature dropout.
> - Held-out layouts and compositions.
> - Compute, memory, and exploration cost.
> - Failure modes involving drift, aliasing, and false correspondence.
> 
> Do not claim that the model has learned a general spatial reference frame from one successful task. Require targeted ablations and transfer tests. If the first tier fails, diagnose whether the issue is observation ambiguity, dynamics, memory, action semantics, or optimization before adding complexity.
> 
> Freeze the tier, generator, primary metric, practical effect threshold, and decision rule before confirmation. Produce trajectories, predicted-versus-observed feature plots, correspondence traces, relocalization examples, ablations, and a decision record. Stop after this study.
> ```
> 
> ```text
> # Prompt 6 — synthesis and next decision
> 
> Read the completed experiment records without rerunning the whole program. Build a cross-study comparison that separates:
> 
> - Reproducible behavioral improvements.
> - Mechanistic evidence.
> - Capacity or optimization explanations.
> - Task-specific effects.
> - Compute or memory tradeoffs.
> - Negative and inconclusive results.
> - Unresolved confounds.
> 
> For every claimed improvement, identify the strongest matched control and whether the result survives fresh data, perturbation, and budget matching. Do not combine incompatible metrics into a single headline score without justification.
> 
> Create a compact evidence table with columns for hypothesis, test, control, primary metric, uncertainty, effect size, resource cost, failure mode, and decision. Mark each conclusion as supported, weakened, inconclusive, or not tested.
> 
> Propose only one next repository action:
> 
> - Freeze the result as a completed finding.
> - Run a narrowly specified replication.
> - Modify the task because a confound was discovered.
> - Reject the mechanism and pursue the strongest alternative explanation.
> - Stop because the evidence does not justify further expansion.
> 
> Update the research registry and reports only after checking that all artifacts, provenance, tests, and decision records are present. Do not rewrite historical conclusions to make them look stronger. Keep biological interpretations explicitly labeled as hypotheses or design inspirations unless the computational evidence supports a narrower claim.
> 
> End with a short progress report suitable for a research log and a separate list of unresolved questions. Do not start another experiment in the same run.
> ```
>
> **Sequenced research prompts**
>
> 
>
> **Inspected SOAM repository guidance, branches, documentation, and priorities**
>
> 
>
> Worked for 10m 18s

# SOAM Research Campaign - Codex Agent Prompts

I've structured this as a sequence of **six Codex assignments: one research-planning assignment followed by five progressively more ambitious experiments.** Each assignment is designed to produce implementation, experimental evidence, a scientific review, and a decision about what to investigate next.

I also checked your [github.com](https://github.com/spencerbug/soam?utm_source=chatgpt.com), including its agent instructions, experimental protocols, and existing research tickets.

There are two important considerations\:

- **E1 is a completed negative result for S32, not a failed research program.** The GRU's advantage is real under that protocol, but its cause remains unisolated. The frozen E1 results should remain unchanged. \[[SOAM E1 Results: Prediction, Sharing, and Recovery](https://spencerbug.github.io/research/soam-e1-results/?utm_source=chatgpt.com); [SOAM E1 Results: Prediction, Sharing, and Recovery](https://spencerbug.github.io/research/soam-e1-results/?utm_source=chatgpt.com)\]
- Your repository already uses E2 and E3 for other proposed experiments. I'll call these new investigations **Studies A-E** until Codex reconciles them with the existing ticket hierarchy.

Proposed research sequence

1. **Prompt 0 - Research campaign planning and experimental controls**
2. **Study A - Why did GRU outperform S32?**
3. **Study B - Temporal gating and sensory snapshots**
4. **Study C - Primed, tracking, and attended modes**
5. **Study D - Gated persistent memory and online plasticity**
6. **Study E - Navigable object-centered recurrent representations**

I would give Codex Prompt 0 first, followed by Study A. The later prompts are separate assignments, not permission to run five expensive experiments simultaneously.

---

## Prompt 0 - Establish the research campaign

Purpose: Integrate the new hypotheses into the existing SOAM research process without losing experimental rigor or rewriting E1.

**document: **

# SOAM Research Campaign: Adaptive Recurrent Sensorimotor Intelligence

You are the principal research engineer and scientific investigator for the Self-Organizing Attractor Memory (SOAM) project.

Your objective is to design a rigorous, experimentally grounded research campaign exploring how recurrent neural dynamics, adaptive gating, sensorimotor inference, attention, and plasticity could form reusable components of embodied intelligence.

This is not a request to implement a predetermined architecture. It is a request to **discover which mechanisms work, why they work, and when simpler alternatives are superior**.

## 1. Review the existing research

Repository: https://github.com/spencerbug/soam

Read the current checked-out repository, especially:

- `AGENTS.md`
- `PRIORITIES.md`
- `docs/RESEARCH_PATHS.md`
- `docs/RESEARCH_SPEC_V0_3.md`
- `docs/HYPOTHESES.md`
- `docs/SHARED_POPULATION_PROTOCOL.md`
- The E1 study and gate reports
- `tickets/SOAM-052-shared-population-gate.md`
- `tickets/SOAM-059-research-fork-selection.md`

Review the published E1 discussion:

https://spencerbug.github.io/blog/testing-shared-recurrent-memory/

https://spencerbug.github.io/blog/a-memory-can-settle-and-still-be-wrong/

https://spencerbug.github.io/research/soam-e1-results/

Check the actual branch, commits, ticket statuses, and local scientific artifacts. Do not assume the public default branch contains the latest research or that historical planning tickets reflect the final E1 execution state.

Do not alter the frozen E1 protocol, archived results, or historical gate outcome.

## 2. Research motivation

E1 tested a shared recurrent population with symmetric and asymmetric dynamics against multiple controls.

Important observations:

- S32 failed its absolute reconstruction criterion.
- G28 and G32 significantly outperformed S32 on short-horizon prediction under the tested protocol.
- G28 achieved approximately 0.0464 free-8 NMSE and 0.0196 recall NMSE.
- G32 achieved approximately 0.0377 free-8 NMSE and 0.0210 recall NMSE.
- L12 performed better than either GRU on the free-32 endpoint.
- The original recovery experiment demonstrated that state contraction is not necessarily accurate associative recovery.
- The latent environment has only two physical coordinates projected into twelve features.

These findings do not establish gating as the cause of GRU's success. They motivate controlled mechanistic experiments.

Our broader hypothesis is that **adaptive control of recurrent state evolution may be as important as the organization of recurrent connectivity itself**.

We want to investigate recurrent systems that can:

1. Reconstruct missing sensory information.
2. Maintain a useful internal hypothesis without continuously receiving observations.
3. Evolve that hypothesis using actions and elapsed time.
4. Correct predictions when new observations arrive.
5. Maintain multiple competing or complementary hypotheses.
6. Learn new persistent associations without corrupting established dynamics.
7. Eventually represent objects as navigable, action-conditioned dynamical memories.

## 3. Candidate architectural principles

Investigate these ideas without presupposing their correctness.

### Adaptive recurrent dynamics

The network learns how strongly each state component updates rather than relying entirely on a fixed recurrent integration coefficient.

### Separated sensory and motion influence

External sensory evidence and action-conditioned recurrent prediction may benefit from independently controlled coupling.

### Temporal inference phases

A possible processing cycle is:

1. Receive a sensory cue or snapshot.
2. Allow internal recurrent settling or pattern completion.
3. Evolve the inferred state under movement.
4. Receive another observation.
5. Compute prediction error and selectively correct the state.

The cycle may be continuous, event-driven, phase-based, or adaptively scheduled. Do not assume a fixed schedule is optimal.

### Three candidate operating modes

- **Primed:** a weakly activated candidate memory or belief hypothesis.
- **Tracking/calibrating:** a hypothesis that predicts motion and assimilates observations.
- **Attended:** a prioritized hypothesis receiving additional inference, action, or learning resources.

These are initially functional concepts, not claims that biological cortical columns literally have three discrete modes.

### Separate inference and plasticity

Transient hidden-state changes during inference must be distinguished from persistent associative-memory updates.

Novelty, reliability, attention, and prediction error may influence learning, but should not be assumed to make identical decisions.

## 4. Relevant biological inspiration

Prepare a concise, critically sourced theoretical mapping of:

- Hippocampal theta-phase encoding/retrieval separation.
- Basal ganglia and prefrontal working-memory gating.
- Continuous attractor dynamics and landmark-based correction.
- Corollary discharge and sensory prediction during movement.
- Neuromodulated three-factor plasticity and eligibility traces.

For each, distinguish experimental neuroscience evidence, computational models, and speculation about SOAM.

Do not use biological analogies as performance evidence.

## 5. Proposed experimental campaign

Review and rank five candidate studies:

**Study A:** Isolate why the GRU outperformed S32, including adaptive gating, capacity, training, and task simplicity.

**Study B:** Evaluate snapshot-based sensory assimilation, recurrent settling, motion prediction, and adaptive correction.

**Study C:** Evaluate primed, tracking, and attended control of multiple memory hypotheses.

**Study D:** Test independently gated persistent memory acquisition and its effect on interference and recall.

**Study E:** Integrate demonstrated mechanisms into minimal navigable object-centered sensorimotor representations.

Treat these as conditional research paths. Reconcile them with existing SOAM experiment names and tickets rather than reusing stable identifiers.

## 6. Scientific operating requirements

For every selected experiment:

- Write hypotheses and falsifiable predictions before full training.
- Identify the strongest simpler alternative explanations.
- Reuse the existing evaluation infrastructure where suitable.
- Preserve training/development/confirmation separation.
- Freeze the primary metrics, baselines, seeds, tuning budget, confidence-interval methodology, resource limits, and stopping criteria before confirmation.
- Treat independently trained roots, not correlated timesteps, as the primary statistical units where appropriate.
- Keep environment ground truth outside the model.
- Prevent future observations from leaking into free prediction.
- Report negative and inconclusive outcomes.
- Measure parameters, active state, memory, inference cost, and training cost.
- Verify reproducibility and existing repository invariants.
- Distinguish prediction accuracy, state stability, correct recovery, and persistent learning.
- Never declare an attractor merely because a hidden trajectory contracts.

Include cheap smoke tests and development experiments before expensive confirmation runs. Select compute limits using measured fixture costs and existing project conventions.

## 7. Immediate assignment

Do not execute all five studies.

First:

1. Audit the available E1 results and repository state.
2. Reconcile the proposed studies with SOAM-052, SOAM-059, and existing dependencies.
3. Produce a concise research campaign document with a dependency graph, hypotheses, expected information gain, estimated costs, and failure branches.
4. Select Study A as the preferred initial **mechanistic diagnostic**, unless your evidence-based comparison identifies a more informative lower-cost follow-up. Explain the choice.
5. Create or update only the tickets and lightweight protocol documents needed to authorize the selected bounded study. Follow the existing repository schema and governance.
6. Explicitly mark Studies B-E as proposed rather than active.
7. Run documentation, ticket, and relevant baseline checks.

Deliver a review of what E1 established, what remains unresolved, the proposed next experiment, and the specific result that would change our architectural direction.

Proceed with this bounded planning work autonomously. Do not launch an unapproved multi-study campaign or modify historical scientific evidence.

---

## Prompt A - Why did the GRU outperform S32?

Priority: highest. This experiment should isolate the actual computational advantage before adding more architecture.

**document: **

# Study A: Mechanistic Analysis of Adaptive Gating in Shared Recurrent Dynamics

## Research question

E1 showed that ordinary GRUs substantially outperformed the proposed S32 symmetric-plus-asymmetric recurrent network on reconstruction and short-horizon prediction.

Determine **why the GRU performed better**.

In particular, investigate whether its advantage comes from adaptive state-update gating, reset gating, parameter capacity, optimization behavior, or the low-dimensional structure of the task.

Do not assume gating is responsible merely because GRUs contain gates.

## 1. Hypotheses

### H1 - Adaptive state retention

Learned update gates allow a recurrent network to preserve some components of its state while rapidly updating others.

Prediction: removing input/state-dependent update gating should degrade the ability to alternate between reconstruction/maintenance and movement prediction, even after retraining at comparable capacity.

### H2 - Adaptive reset

The GRU reset mechanism enables selective changes in how prior hidden activity contributes to candidate updates.

Prediction: disabling adaptive reset should produce distinguishable deficits in specific regimes, potentially different from update-gate deficits.

### H3 - Optimization and capacity

The GRU advantage is primarily explained by parameterization, optimization, or additional effective capacity.

Prediction: well-trained non-gated recurrent networks of comparable cost can recover most of the performance gap.

### H4 - Task simplicity

The E1 task is approximately low-dimensional system identification, not a demanding associative-memory task.

Prediction: much of the GRU's success can be reproduced by compact learned dynamical models, and its advantage may shrink under longer-horizon or more structured generalization tests.

## 2. Experimental variants

Preserve existing G28, G32, S32, and L12 as historical references.

Implement a bounded family of new controls:

**A. Full GRU:** standard update and reset gates, retrained under the new protocol.

**B. Fixed-update GRU:** replace the adaptive update gate with a trainable but input-independent scalar or per-unit constant. Retain the GRU's other capabilities where technically appropriate.

**C. Fixed-reset GRU:** replace the adaptive reset gate with a constant, preserving adaptive update gating.

**D. Fixed-update-and-reset control:** remove both adaptive gates while retaining a comparable recurrent transformation.

**E. Gated leaky RNN:** start with a simple tanh recurrent core and replace its fixed leak with a learned gate depending on state, supplied role, and action.

**F. Gated S32:** introduce adaptive update gating into S32 without changing its symmetric/asymmetric recurrence hypothesis unnecessarily.

**G. Non-gated capacity control:** increase a conventional recurrent core's capacity or training allocation within a declared comparison budget.

You may narrow this family if initial analytical comparisons demonstrate redundancy. Explain any omissions.

Keep separate comparisons for approximately matched parameter count, active hidden-state size, and operation count. Do not claim exact parity across all three.

Use explicit equations and tests for each recurrence. Clearly distinguish a frozen gate, a learned constant gate, and a dynamically computed gate.

## 3. Training protocol

Start from the E1 synthetic feature environment.

Maintain:

- The same fundamental observations and action permissions.
- Separate reconstruction and transition objectives.
- Comparable cue corruption and masking.
- The existing free-8, free-32, grounded-32, and ten-step reconstruction endpoints.
- Independent roots and paired datasets across candidate models.

Because the previous E1 results have already been examined, reserve new confirmation streams for the new mechanistic hypotheses.

Before confirmation:

1. Verify the original candidate equations and result provenance.
2. Run small implementation correctness tests.
3. Calibrate training budgets and hyperparameter sensitivity on development data.
4. Check for optimization plateaus and severe undertraining.
5. Freeze variants, baselines, tuning budgets, primary endpoints, effect thresholds, uncertainty rules, and stopping criteria.

Do not use confirmation outcomes to choose a different GRU ablation.

## 4. Additional mechanistic diagnostics

### Gate behavior

Instrument hidden-state and gate trajectories.

Record:

- Update and reset values by time, hidden unit, task, and action magnitude.
- Gate behavior during zero-motion maintenance.
- Gate behavior during nonzero movement.
- Gate changes after contradictory or corrupted cues.
- Per-unit correlations between update rate and state evolution.

Determine whether the model develops meaningful differences between slowly and rapidly changing state components.

### Controlled interventions

With model state and observations held constant, vary the supplied action and task role.

Examine changes in candidate states and learned gates.

Include both:

- Post-training gate interventions, interpreted cautiously because they may create out-of-distribution behavior.
- Separately trained ablations, which are more informative about whether a gate is necessary to achieve the observed capability.

### State geometry

Investigate whether learned hidden states encode useful structure.

Use diagnostic-only decoding of the simulator's two latent coordinates.

Measure:

- Linear probe quality versus nonlinear probe quality.
- How hidden-state distances relate to physical positions.
- Whether action-induced motion produces coherent hidden trajectories.
- Whether representation dimensions are reused across recall and prediction.
- Whether trajectories collapse toward generic states.

These probes must not feed their labels or outputs back into the recurrent model.

### Recovery

Inject controlled hidden-state perturbations.

Measure both trajectory convergence and whether decoded outputs remain accurate.

Distinguish retention of an arbitrary hidden state from correction toward a useful state.

### Long-horizon behavior

Retain the L12 baseline.

Analyze why L12 performed better on the original free-32 evaluation than either GRU. Test whether recurrent prediction errors accumulate through phase drift, bias, contraction, or instability.

## 5. Decision criteria

Design a preregistered primary comparison that directly measures the effect of adaptive update gating on a competent matched nonadaptive control.

Require a practically meaningful performance advantage with appropriate uncertainty before claiming adaptive gating is beneficial.

Guard against:

- Improvements limited to one endpoint.
- Worse long-horizon prediction.
- Excessive parameter or compute overhead.
- Poor reconstruction.
- Benefits disappearing after fair retuning of non-gated alternatives.

Use development data to justify numerical thresholds, and freeze them before new confirmation runs.

Interpret outcomes as follows:

- **Supported:** adaptive gating produces a reproducible advantage not explained by the declared capacity/training controls.
- **Mixed:** gating helps one task or horizon but harms another.
- **Inconclusive:** uncertainty, model competence, or resource mismatches prevent attribution.
- **Negative:** well-controlled non-gated alternatives match or outperform the gated mechanism.

A negative result is an acceptable and valuable outcome.

## 6. Deliverables

Produce:

1. Implemented and tested model variants.
2. A frozen versioned protocol and manifest.
3. Reproducible development and confirmation runs within the agreed resource ceiling.
4. Comparison tables including root-level results and confidence intervals.
5. Gate-activation and hidden-state visualizations.
6. Perturbation, representation, and long-horizon diagnostics.
7. A scientific report distinguishing findings from interpretations.
8. A decision record identifying which mechanisms deserve retention.

Conclude by answering:

**Does adaptive gating offer a necessary or practically valuable capability beyond ordinary recurrent dynamics for the E1 family of tasks?**

Identify the smallest supported recurrent core to carry forward into Study B. Do not implement Study B as part of this assignment.

---

## Prompt B - Temporal gating, settling, and sensory snapshots

Priority: second. This is the most direct experiment for your idea of injecting features, allowing settling, evolving under movement, and only then correcting against another observation.

**document: **

# Study B: Temporal Gating of Sensory Assimilation and Action-Conditioned Recurrent Dynamics

## Research question

Can recurrent sensorimotor inference improve when sensory evidence, internal settling, and motion prediction have independently controlled influence?

The central hypothesis is that **a recurrent system should not necessarily integrate incoming sensory features with equal strength at every physical timestep**.

A stronger design might inject sensory evidence selectively, let the representation settle, evolve it under action, and assimilate a later observation using prediction error.

This investigation must separate any real benefit of temporal organization from simply performing more computation or receiving more observations.

## 1. Computational hypothesis

Represent the recurrent system as a predicted state followed by an optional sensory correction.

Conceptually:

    predicted_state = F(previous_state, action, dt)

    predicted_features = D(predicted_state)

    if observation_available:
        residual = observed_features - predicted_features
        corrected_state = C(predicted_state, residual, mask, gain)
    else:
        corrected_state = predicted_state

The model must distinguish:

- Predicted state before receiving current sensory information.
- Corrected state after receiving available information.
- Persistent parameters and any fast-memory state.

Introduce independently controlled channels for:

1. Sensory assimilation gain.
2. Action/motion influence.
3. Internal recurrent settling.
4. Optional learned confidence or uncertainty.

Do not introduce persistent online weight updates in this study.

## 2. Competing hypotheses

### H1 - Deliberate sensory assimilation

Separating prediction from observation correction improves state estimation under sparse, noisy, or intermittent sensing.

### H2 - Beneficial settling

Additional recurrent settling after a sensory cue improves pattern completion and future predictions, beyond merely repeating the input.

### H3 - Adaptive sensory gating

The optimal correction gain depends on observation reliability, prediction error, current state, and action context.

### H4 - No special temporal benefit

A conventional GRU receiving the same observations and actions can learn equivalent behavior without a manually structured sensory-update cycle.

This final hypothesis is a mandatory alternative.

## 3. Required model comparisons

**A. Conventional simultaneous-input GRU**

Provide action, available sensory features, and validity masks through a standard recurrent update.

**B. Predict-then-correct recurrent model**

Execute motion prediction and a separate fixed-gain correction when an observation is available.

**C. Snapshot/settle/predict/correct model**

After a cue, permit a bounded number of recurrent settling updates before the next action-conditioned prediction.

**D. Adaptive sensory-gain model**

Allow a learned gate to control how strongly an incoming observation changes the predicted state.

**E. Adaptive sensory and motion coupling**

Allow sensory influence and motion influence to vary independently, while maintaining one underlying recurrent state.

**F. Simple reinitialization/filtering controls**

Include a strong simple reference that reconstructs state from the latest available partial observation and propagates it between observations. Consider a fitted linear state-space or filtering baseline appropriate to the low-dimensional environment.

Retain the strongest viable GRU and linear reference from Study A.

Keep any oracle using simulator equations explicitly separate from learned, information-matched competitors.

## 4. Temporal simulation protocol

Extend the E1 environment to support intermittent observations.

Use an explicit event order:

1. Begin at the current posterior state.
2. Receive and execute action for physical interval t to t+1.
3. Predict features at t+1 before accessing the observation.
4. Record prediction error against evaluator-only ground truth.
5. If sensing is scheduled at t+1, reveal permitted observed features and masks.
6. Apply a correction.
7. Optionally execute bounded internal settling updates with zero physical-time advance.
8. Continue to the next physical interval.

Internal settling updates must not accidentally apply extra movement or advance the simulator clock.

Compare observations arriving:

- At every timestep.
- Every two timesteps.
- Every four timesteps.
- Every eight timesteps.
- At irregular but predetermined intervals.
- Only at the initial cue.

Also test:

- Partial observations.
- Missing observations.
- Sensor noise.
- Transient sensor corruption.
- Contradictory cues.
- Changes in movement magnitude and direction.
- Long intervals with no new sensory evidence.

All compared models must receive the same observation information at the same physical times for each trial.

## 5. Isolate settling from additional computation

A model that performs five hidden-state updates while another performs one has received more compute.

Use separate experiments for:

- Equal physical observations and equal recurrent-update budgets.
- Equal physical observations but additional explicitly costed settling.
- Adaptive settling versus fixed settling under matched maximum or average compute.
- A conventional recurrent control given an equivalent compute allowance.

Measure whether settling actually improves the inferred answer, not merely reduces the difference between successive states.

Test multiple plausible settling durations using development data, then freeze the selected comparisons before confirmation.

Record reconstruction error at each internal iteration and whether extra iterations begin to erase cue-specific information.

## 6. Adaptive correction experiments

Compare a fixed gain against gains depending on:

- Observation masks and known noise characteristics.
- Prediction residual.
- Previous hidden state.
- Action magnitude.
- Learned confidence.

Keep separate whether noise reliability is supplied as metadata or inferred.

Avoid treating large prediction error as proof that the incoming observation is trustworthy.

Include examples where the sensory observation is wrong and the motion-based prediction is approximately right.

The network should ideally avoid overwriting a reliable hypothesis with a corrupted snapshot.

Test whether sensory gating improves that robustness without causing unjustified resistance to genuine environmental changes.

## 7. Evaluation

Primary candidate endpoint:

Prediction accuracy over intermittent-observation trajectories, measured **before each sensory correction**.

Additional metrics:

- Reconstruction error after correction and settling.
- Free prediction error at 8 and 32 steps.
- Error growth during observation gaps.
- Recovery time after observations resume.
- Response to contradictory cues.
- Stability of cue-specific information.
- Sensitivity to sensor noise.
- Calibration of confidence, if modeled.
- Recurrent updates and FLOP/MAC estimates per physical timestep.
- Total active state and persistent parameter costs.

Distinguish a model that knows the correct state immediately after an observation from one that can correctly predict the next observation.

Report results both at fixed compute and along a compute/accuracy Pareto frontier.

## 8. Biological investigation

Prepare a focused research note connecting these experiments to:

- Hippocampal theta-associated encoding/retrieval phases.
- Continuous attractor path integration and landmark correction.
- Corollary discharge and predictive sensory modulation.
- Predictive processing and state estimation.

Identify which aspects have experimental biological support and which are only engineering analogies.

Do not use a fixed theta-like alternation merely because a biological oscillation exists. Compare fixed, event-driven, and learned schedules.

## 9. Decision

Determine whether sensory input is best treated as:

1. A continuously mixed component of recurrence.
2. A separate correction operation.
3. A periodic or event-driven snapshot.
4. An adaptively gated evidence source.

Select based on grounded accuracy, robustness, prediction, and resource cost.

Produce a complete scientific report, reproducible results, and a recommendation for the sensory/motion control interface.

Do not introduce multi-hypothesis attention or persistent online learning yet. Those are later studies.

---

## Prompt C - Primed, tracking/calibrating, and attended modes

Priority: third. This tests whether explicit modes add real capabilities beyond a single GRU or multiple independent recurrent states.

**document: **

# Study C: Adaptive Operating Modes and Concurrent Recurrent Hypotheses

## Research question

Can a recurrent memory system maintain multiple hypotheses while dynamically controlling which hypotheses are primed, actively tracked, or attended?

Investigate whether these operating modes improve sensorimotor continuity, ambiguity resolution, and computational efficiency.

The central idea is that **the same learned recurrent dynamics may serve different purposes depending on how sensory evidence, movement, attention, and internal state updates are gated**.

Do not assume that priming, tracking, and attention require three separate neural populations or three hard-coded states.

## 1. Functional definitions

### Primed

A candidate representation has been partially activated by current or prior evidence.

It may:

- Preserve a weak candidate hypothesis.
- Receive limited associative or recurrent computation.
- Remain eligible for future attention.
- Avoid overwriting another active hypothesis.

Priming does not imply that the candidate is correct.

### Tracking/calibrating

A candidate maintains a continuously evolving hypothesis.

It may:

- Predict changes from action or elapsed time.
- Correct its state when compatible observations arrive.
- Maintain estimated pose or other changing attributes.
- Remain active while another hypothesis receives attention.

Tracking need not imply strong sensory evidence at every timestep.

### Attended

A candidate receives additional processing priority.

It may:

- Receive additional recurrent inference updates.
- Influence selective sensing or action selection.
- Become the subject of higher-resolution prediction.
- Receive priority for later plasticity, if separately authorized.

Attention is not equivalent to writing memory. No persistent learning is required in this experiment.

## 2. Competing hypotheses

**H1:** Independently controlled operating modes improve simultaneous hypothesis maintenance and switching.

**H2:** Priming allows weak candidate memories to remain available without allocating full tracking computation.

**H3:** Attended hypotheses can receive additional processing without destroying unattended but valid hypotheses.

**H4:** Learned soft gates outperform rigid, externally supplied three-state mode assignments.

**H5:** Any observed benefit is explained by additional hidden-state capacity or multiple hypothesis slots rather than the gating policy.

H5 is essential to test.

## 3. Minimal experiment environment

Extend the successful Study B environment to include a small number of ambiguous hypotheses.

Start with two candidates; expand to three or four only if needed.

Create two distinct situations.

### Competing hypotheses

One observation sequence is initially consistent with two possible object identities or reference frames.

Movement and subsequent sensory observations gradually distinguish them.

At most one of the competing explanations is correct.

The system must preserve alternatives long enough to resolve ambiguity without immediately collapsing to an unsupported answer.

### Complementary hypotheses

Two distinct objects or environmental components are simultaneously present.

Both representations may be valid.

The system must track one while attending to the other and later recover the first without unnecessarily reconstructing its entire state.

Use synthetic feature generators that allow controlled ambiguity and overlap.

Keep object identity, hidden physical state, and true correspondence exclusively in the evaluator unless they are explicitly declared supplied scaffolding in a particular control.

## 4. Required model variants

**A. Single-state GRU**

One recurrent state encodes the complete current scene or belief. This is the simplest recurrent reference.

**B. Independent recurrent banks**

Each candidate maintains an independent recurrent network and state.

**C. Tied recurrent weights with separate hypothesis states**

Each candidate gets its own hidden state, but all candidates share one parameterized transition function.

This distinguishes multiple state instances from parameter sharing.

**D. Fixed three-mode controller**

Each candidate receives externally specified primed/tracking/attended control signals with documented deterministic rules.

**E. Learned soft-mode controller**

Learn continuous control values for sensory coupling, recurrent updates, and processing priority.

**F. Conventional multi-hypothesis filter**

Include a competent structured baseline that maintains candidate states and likelihoods without requiring the proposed neural mode organization.

Match total available hidden state, parameters, and computation where practical.

Account for active hypothesis slots, controller parameters, candidate scoring, and all concurrently retained state.

## 5. Core interventions

### Priming and activation

Present an ambiguous partial cue.

Measure whether multiple plausible candidates remain recoverable.

Present a later disambiguating observation and determine whether the correct candidate gains support.

Test unknown and incompatible cues, not just known examples.

### Tracking without attention

Attend to candidate A while candidate B continues evolving under action.

After an interval, return attention to B.

Measure continuity of B's pose and predicted sensory state.

Compare against freezing B and against running B with full computational allocation.

### Attention switching

Switch attention between candidates without resetting hidden states.

Measure:

- Accuracy immediately before and after switching.
- Switching latency.
- Processing cost.
- Interference between candidates.
- Whether incorrect hypotheses are unnecessarily reinforced.

### Conflicting evidence

Inject misleading, noisy, or incompatible sensory evidence.

Determine whether the system:

- Immediately collapses to the new interpretation.
- Maintains calibrated uncertainty.
- Recovers after the evidence is contradicted.
- Incorrectly treats its own settled state as proof of familiarity.

### Complementary composition

Present two simultaneously valid hypotheses.

Test whether the controller can keep both without forcing winner-take-all competition.

## 6. What should control the modes?

Investigate several candidate signals:

- Sensory evidence strength.
- Prediction residual.
- Hypothesis confidence.
- Action relevance.
- Current task priority.
- Expected information gain.
- Processing-budget constraints.

Distinguish externally supplied attention targets from learned attention decisions.

A learned controller must not receive true hypothesis identity, future observations, or evaluator labels at inference.

Use scheduled mode control as a baseline before claiming emergent mode discovery.

## 7. Evaluation

Report:

- Correct-hypothesis support and calibration.
- False confidence or false familiarity.
- Persistence of valid but unattended hypotheses.
- Re-attention reconstruction error.
- Pose and feature prediction error.
- State continuity across attention changes.
- Candidate interference.
- Unknown-cue rejection.
- Average and worst-case computation.
- Total parameter and hidden-state storage.
- Sensitivity to the number of simultaneous hypotheses.

When assessing convergence, verify the decoded state against the correct target rather than measuring contraction alone.

Use distinct metrics for competing explanations and simultaneously valid components.

## 8. Biological investigation

Study possible analogies to:

- Basal ganglia gating of working-memory updates.
- Cortical and thalamic attentional gain control.
- Hippocampal pattern completion and competing retrieval.
- Predictive tracking and working-memory maintenance.
- Neuromodulatory regulation of processing priority.

Present these as candidate functional correspondences, not proof of biological equivalence.

## 9. Decision

Determine whether the evidence supports:

- A single recurrent state with dynamic internal gating.
- Shared recurrent parameters with multiple hypothesis states.
- Independent recurrent banks.
- A hybrid involving shared recurrent dynamics and a separate controller.

Specifically answer:

**Do priming, tracking, and attending need to be explicit architectural modes, or can their useful behavior emerge from a smaller set of independently learned gates?**

Favor the simplest model that demonstrates correct hypothesis maintenance, sensory prediction, and controlled switching.

Do not proceed to persistent online learning without recording this decision and the relevant resource trade-offs.

---

## Prompt D - Gated learning and self-organizing persistent memory

Priority: fourth. This separates the network's ability to update its current beliefs from its ability to permanently remember new experiences.

**document: **

# Study D: Independently Gated Inference and Persistent Associative Plasticity

## Research question

Can a recurrent sensorimotor system acquire new persistent memories online while preserving previously learned dynamics and avoiding catastrophic interference?

Investigate whether persistent memory writing should be controlled independently from sensory assimilation, recurrent updates, and attention.

The critical distinction is:

**Updating the current recurrent state is not the same as learning a new persistent association.**

The system may need to correct its current interpretation without storing anything. Conversely, it may encounter genuinely new information that should survive state resets.

## 1. Research hypotheses

### H1 - Separation of state and weight adaptation

A stable recurrent dynamics core with separately controlled fast memory can learn new associations without continuously modifying its slow recurrent parameters.

### H2 - Independent write gating

Prediction error alone is not a sufficient learning signal.

Novelty, confidence, repeated evidence, and relevance may provide better control over persistent memory updates.

### H3 - State-independent retention

Newly acquired information persists after transient recurrent state is reset.

This distinguishes actual acquisition from merely carrying recent experiences in hidden activity.

### H4 - Structured associative references remain competitive

A simple episodic key-value store or online regression method may acquire and retain the same associations more efficiently than learned fast recurrent plasticity.

The experiment must include these alternatives.

## 2. Candidate architecture

Start with the smallest recurrent inference model supported by the preceding experiments.

Separate:

**Slow dynamics parameters**

Reusable transformations learned offline and held fixed during the initial online acquisition study.

**Transient recurrent state**

Current belief, pose, action-conditioned dynamics, and temporary information.

**Persistent fast memory**

An associative structure updated from grounded observations.

Possible realizations include:

- Fast recurrent weight corrections.
- Low-rank associative updates.
- Key-value associative memory.
- Hebbian or delta-rule updates.
- Eligibility traces followed by a separate write signal.

Do not implement all of these automatically.

Select a minimal representative family whose comparison can distinguish the central hypotheses.

For a recurrent fast-weight option, one possible formulation is:

    effective_weights = slow_weights + fast_weights

    hidden_next = recurrent_update(
        hidden,
        action,
        effective_weights
    )

    if grounded_evidence and write_gate:
        fast_weights = update_association(
            fast_weights,
            evidence,
            learning_rate,
            write_gate
        )

Ensure that the writing mechanism does not rely on hidden simulator state.

Persistent associative storage may instead be implemented outside the recurrent matrix. Account for that storage explicitly.

## 3. Candidate writing strategies

Compare at least:

**A. No online writing**

Freeze all persistent model parameters and memory. Permit only transient recurrent state updates.

**B. Always-write**

Commit an association after each eligible grounded observation.

**C. Prediction-error-triggered writing**

Use a bounded function of prediction error.

**D. Reliability/novelty-gated writing**

Use declared measures of evidence reliability, novelty, and current memory confidence.

**E. Attention-gated writing**

Require the relevant hypothesis to have sufficient processing priority before allowing updates.

**F. Strong conventional associative baseline**

Use a key-value episodic store, nearest-neighbor retrieval, or online ridge-style reference appropriate to the task.

Also include a controlled slow-weight fine-tuning baseline if feasible.

Don't assume attention-gated writing is beneficial. Attention can be wrong or overly narrow.

## 4. Learning environment

Introduce a sequence of related but distinct simulated objects or transformation families.

The environment should permit:

- Reusing previously learned dynamics.
- Acquiring a new object or feature association.
- Observing the same object from multiple poses.
- Encountering partially overlapping or misleading cues.
- Repeatedly revisiting old objects after learning new ones.

Train the reusable recurrent core on a separate collection of objects or trajectories.

Reserve new objects for online acquisition and confirmation.

Object IDs, exact hidden poses, and transformation parameters are evaluator data unless explicitly included in a separately labeled supervised control.

Design the task so that learning genuinely new persistent information is necessary.

Avoid an evaluation that can be solved by interpolating across the original training set or retaining the most recent observation in hidden state.

## 5. Acquisition procedure

For each new object or association:

1. Initialize the recurrent state from permitted observations.
2. Present one or more grounded sensory/action transitions.
3. Allow the candidate learning rule to update only its declared persistent memory.
4. Record changes in persistent memory.
5. Reset transient recurrent activity.
6. Present an incomplete or noisy cue.
7. Test whether the newly acquired information can be recovered.
8. Test action-conditioned predictions using the acquired representation.
9. Revisit previously learned objects and measure interference.

Test one-shot, few-shot, and repeated-observation acquisition separately.

An apparent improvement that disappears after resetting hidden activity is not persistent learning.

## 6. Write-gating stress tests

### Novel but correct information

The system encounters genuinely new information that should be remembered.

### Familiar information

Repeated observations should ideally not cause unnecessary memory growth or drift.

### Noisy observations

Large residuals caused by noise should not automatically create incorrect persistent associations.

### Wrong active hypothesis

A mistaken identity or pose estimate could corrupt the wrong memory.

Measure the resulting interference and whether confidence-aware gating reduces the problem.

### Imagination and prediction

Perform action-conditioned free rollouts without grounded observations.

Verify that no persistent state changes during these rollouts.

### Saturation and collisions

Introduce more stored associations than the memory comfortably supports.

Measure gradual degradation, interference, and possible false familiarity.

## 7. Metrics

Primary outcomes should include:

- Persistent recall after state reset.
- New-object acquisition accuracy.
- Old-object retention after sequential learning.
- Action-conditioned prediction for newly learned objects.

Also measure:

- Number of grounded observations required.
- Error reduction per observation.
- False writes and missed learning opportunities.
- Capacity as a function of persistent memory size.
- Interference between similar memories.
- Recovery after incorrect writes.
- Long-horizon prediction degradation.
- Compute and memory growth during acquisition.
- Read and write latency.
- Performance under matched memory budgets.

Count external storage and memory indexing costs in all comparisons.

## 8. Fast versus slow consolidation

In this study, keep slow dynamics fixed during the primary experiment.

You may perform diagnostic comparisons with slow-weight adaptation, but do not build a full sleep/replay/consolidation architecture yet.

Only propose a later consolidation experiment if the results establish a specific problem that consolidation could address.

For example:

- Fast memories grow without bound.
- Associations become unstable.
- Retrieval interferes with recurrent trajectories.
- Important memories cannot be retained at a fixed capacity.

The proposed consolidation mechanism must target the diagnosed problem.

## 9. Biological inspiration

Review:

- Hebbian associative plasticity.
- Three-factor learning rules.
- Synaptic eligibility traces.
- Neuromodulated learning.
- Complementary learning systems.
- Hippocampal rapid encoding versus slower distributed learning.

Explain which aspects inspire the architecture and which remain computational assumptions.

## 10. Decision

Determine whether persistent online memory is best represented as:

1. Plastic recurrent connections.
2. A separately gated associative store.
3. A combined recurrent-plus-associative mechanism.
4. A conventional explicit memory structure.

The desired outcome is not simply good performance after offline training.

It is **reproducible acquisition of new, useful information that survives hidden-state resets while preserving established capabilities**.

Deliver the implementation, protocol, full comparison, interference analysis, resource measurements, scientific report, and architectural decision.

Do not advance to learned consolidation or unlimited object-memory scaling without new evidence and a separate experimental decision.

---

## Prompt E - Navigable object-centered recurrent memory

Priority: fifth. This is the bridge between the smaller mechanistic experiments and the longer-term SOAM / Thousand Brains / embodied world-model research.

**document: **

# Study E: Object-Centered Navigable Recurrent Memory

## Research objective

Investigate whether learned recurrent dynamics can represent an object as a navigable sensorimotor memory, rather than merely reconstructing static patterns or predicting a generic time series.

The intended capability is:

**Partial sensory evidence activates a hypothesis about a familiar object. Actions update the estimated pose within its reference frame. The recurrent representation predicts which features should be encountered next, and new observations confirm or revise the hypothesis.**

This research is inspired by continuous attractor networks, NeuroSLAM, predictive world models, and the Thousand Brains Theory.

Do not assume that any of these inspirations establishes the proposed implementation as biologically correct.

## 1. Central research questions

### Q1 - Object-centered representation

Can recurrent state encode both object identity and relative pose, such that different observations of the same object correspond to navigable positions in a learned representation?

### Q2 - Action-conditioned movement

Can motor commands transform the internal representation so that future feature observations are accurately predicted?

### Q3 - Recognition from incomplete evidence

Can an unfamiliar viewpoint of a previously encountered object recover the correct object/reference-frame hypothesis?

### Q4 - Landmark correction

Can sensory observations correct drift caused by imperfect motion integration without destroying object identity?

### Q5 - Object dynamics versus egomotion

Can the system distinguish changes caused by the observer's motion from changes caused by an object's motion, using observation sequences and known self-actions?

### Q6 - Compositional reuse

Can independently learned objects or components eventually participate in relationships without requiring a separate recurrent model for every combination?

Q6 is a later extension. Do not treat compositional success as required for the first object-navigation demonstration.

## 2. Minimal environment

Begin with one simple synthetic object with a controllable local reference frame.

The object may contain several distinctive local sensory landmarks.

The observing agent has a pose relative to the object and can execute actions such as:

- Translation.
- Rotation.
- Movement toward or away from a feature.

The agent receives partial sensory observations that depend on relative pose.

Use a simple deterministic or noisy feature-generation model, preferably with a frozen feature encoder.

Avoid handing the recurrent model the true object coordinates, exact reference-frame transform, or the simulator's transition equations.

The model may receive proprioceptive motion commands and elapsed time.

The environment should be capable of producing different observations of the same object from different viewpoints.

It should also permit perceptual aliasing: different object locations may temporarily produce similar local observations.

Store simulator geometry only as environment and evaluator data, not as an automatically exposed object memory.

## 3. Candidate memory design

Investigate a separation between:

**Object/reference-frame hypothesis**

Which learned object or reference frame is currently being considered?

**Continuous pose state**

Where is the observer believed to be relative to that object?

**Sensorimotor dynamics**

How should the pose representation evolve after a commanded action?

**Feature prediction**

What observation should the agent expect from the predicted pose?

**Memory evidence**

What learned information supports the object hypothesis and which parts remain uncertain?

This separation is conceptual.

Test whether these functions require distinct neural mechanisms or can be implemented through different gates and projections of shared recurrent state.

One possible minimal implementation is:

    hypothesis = retrieve_candidate(partial_features)

    pose_state = initialize_or_restore(hypothesis)

    while navigating:
        pose_state = recurrent_motion_update(
            pose_state,
            commanded_action,
            dt
        )

        predicted_features = decode(pose_state, hypothesis)

        if observation_available:
            pose_state = assimilate_observation(
                pose_state,
                observation,
                predicted_features
            )

        output object/pose hypotheses and next-feature prediction

This is a proposed computational contract, not a prescribed architecture.

Use the smallest mechanism justified by the previous studies.

## 4. Required reference models

Compare against:

**A. Conventional GRU world model**

A GRU receiving the same feature/action sequences, trained for action-conditioned prediction and object recognition.

**B. GRU with explicit state correction**

The strongest conventional recurrent inference baseline from earlier studies.

**C. Structured localization/memory baseline**

An explicit learned landmark map, local graph, state-space filter, or another competent nonrecurrent representation.

**D. Recurrent continuous-state candidate**

A recurrent representation in which action drives pose evolution and sensory evidence corrects state.

**E. Recurrent-plus-associative-memory candidate**

Add persistent retrieval only if Study D demonstrated a useful mechanism and its resource cost is accounted for.

Any model given the true simulator motion or observation function must be labeled an oracle or privileged-information control rather than an information-matched competitor.

## 5. Experimental progression

### Stage 1 - Static object and controlled egomotion

The object is stationary and only the observer moves.

Test:

1. Learn or initialize an object's feature structure.
2. Start from an incomplete sensory cue.
3. Infer a candidate object and relative pose.
4. Apply a movement command.
5. Predict the next observation without receiving it.
6. Reveal a partial observation.
7. Correct the internal estimate.
8. Continue around the object.
9. Return to a previously visited viewpoint.

Evaluate whether the representation can recognize familiar views, maintain pose through observation gaps, and reduce accumulated drift upon reobserving landmarks.

This is the minimum initial study and should be completed before expanding scope.

### Stage 2 - Independent object motion

After Stage 1 is validated, introduce externally moving objects.

Create four controlled cases:

- Observer stationary, object stationary.
- Observer moving, object stationary.
- Observer stationary, object moving.
- Both observer and object moving.

Provide the model with its own action commands but no explicit optical-flow inputs.

Investigate whether it learns to predict self-motion-induced feature changes and identifies additional unexplained changes that are consistent with object motion.

Important: observation sequences alone may not uniquely identify egomotion versus object motion. Analyze observability and specify the external motion/action information necessary for disambiguation.

Test interventions that remove or corrupt self-motion information.

A model that predicts both cases accurately but cannot distinguish them has demonstrated prediction, not necessarily motion-source separation.

### Stage 3 - Multiple objects and relationships

Only after the preceding results justify it, introduce two or more learned objects.

Test:

- Reidentifying a previously encountered object.
- Maintaining multiple object hypotheses.
- Tracking relative pose across reference frames.
- Predicting observations under movement between related objects.
- Reusing known relationships in withheld configurations.

Do not build an unrestricted compositional or hierarchical memory system in the first implementation.

If Stage 3 requires substantial new capability, define a fresh study and gate.

## 6. Evaluation

### Object identification

Measure correct-object recognition, confusion among similar objects, unknown-object rejection, and confidence calibration.

### Pose estimation

Measure estimated relative position/orientation against evaluator ground truth, using an appropriate pose metric and reporting any unavoidable symmetry ambiguities.

### Sensorimotor prediction

Measure predicted versus actual future feature observations at multiple horizons.

### Navigation continuity

Measure how well the model tracks pose during missing observations, occlusion, and long action sequences.

### Landmark correction

Measure error before and after reobserving a landmark.

Distinguish useful calibration from snapping to a generic or incorrect attractor.

### Memory retrieval

Test incomplete and corrupted cues, unfamiliar viewpoints of known objects, and visually similar but distinct objects.

### Motion-source separation

Quantify performance when self-motion and object motion are separately manipulated.

### Resource efficiency

Record:

- Recurrent state size.
- Persistent object-memory storage.
- Parameter count.
- Compute per navigation step.
- Number of observations needed to learn an object.
- Retrieval and state-correction latency.

## 7. Investigating the geometry of recurrent memory

One of the most interesting questions is whether a continuous navigation manifold emerges in the learned recurrent state.

Visualize or probe:

- Hidden-state trajectories during motion.
- Similarity of states corresponding to nearby viewpoints.
- State changes induced by reversing an action.
- Return to a previous state after a closed motion loop.
- Response to small sensory perturbations.
- Distinct object identity versus continuously changing pose.

Use diagnostic probes without leaking their ground-truth labels into training unless explicitly part of a separate supervised control.

Do not claim a continuous attractor solely because the hidden representation appears smooth or approximately low-dimensional.

Require evidence about dynamics, perturbation response, state-dependent prediction, and meaningful correction.

## 8. Biological and theoretical foundations

Prepare a critical literature synthesis covering:

- Continuous attractor models for spatial integration.
- Head-direction and grid-cell models.
- Sensorimotor reference frames in Thousand Brains Theory.
- NeuroSLAM and learned localization systems.
- Predictive state representations and JEPA-style world models.
- Object permanence and action-conditioned sensorimotor prediction.

Identify which requirements are already solved by strong established methods.

The point is not to recreate all of SLAM inside a GRU. It is to test whether learned navigable recurrent memory offers useful flexibility, generalization, or representational reuse.

## 9. Experimental decision

Evaluate whether the demonstrated capabilities support a future architecture involving:

- Shared recurrent transformation dynamics.
- Multiple object/reference-frame hypotheses.
- Continuous pose representations.
- Controlled sensory correction.
- Associative retrieval and persistent acquisition.
- Separate attention and learning control.

Favor evidence over architectural elegance.

Conclude by answering:

**Can a learned recurrent memory become a navigable representation of an object, rather than merely an implicit predictor of the next sensory vector?**

Explain what distinguishes the observed behavior from a conventional GRU world model or an explicit localization filter.

Deliver a reproducible scientific study, clear negative controls, visualization of internal dynamics, an architectural decision, and a narrowly scoped proposal for the next experiment.

Do not claim human-like sensorimotor intelligence, autonomous object discovery, or compositional generalization unless those capabilities have been independently tested.

---

## Final prompt - Campaign synthesis and architectural decision

This is the prompt I'd use after the completed studies, or after an earlier result determines that proceeding would be unproductive. It prevents Codex from treating each experiment as one more component that automatically belongs in the eventual architecture.

**document: **

# SOAM Research Synthesis: What Architecture Has the Evidence Earned?

Review the completed research following E1, including adaptive recurrent gating, temporal sensory assimilation, recurrent hypothesis modes, persistent memory acquisition, and any object-centered navigation experiments actually completed.

Do not assume all proposed studies were executed. Distinguish tested mechanisms from deferred proposals.

Your task is to make a rigorous scientific assessment of what the evidence supports.

## 1. Evidence ledger

For every completed experiment, identify:

- The falsifiable hypothesis.
- The primary metric and outcome.
- The strongest reference model.
- Resource differences and limitations.
- The mechanism actually isolated.
- Negative and inconclusive findings.
- Remaining alternative explanations.
- Whether the result was reproduced on genuinely untouched confirmation data.

Separate:

**Demonstrated capability:** behavior observed under a defined protocol.

**Supported mechanism:** evidence that an architectural component materially contributes to that capability.

**Plausible explanation:** interpretation that remains unproven.

**Speculative extension:** an untested architectural idea or biological analogy.

## 2. Evaluate the emerging architecture

Assess whether the evidence justifies each candidate component:

1. Shared recurrent dynamics.
2. Adaptive hidden-state update gating.
3. Independent sensory/motion coupling.
4. Internal settling cycles.
5. Primed, tracking, and attended control modes.
6. Multiple maintained hypothesis states.
7. Independently gated persistent plasticity.
8. Associative object memory.
9. Continuous reference-frame navigation.
10. Action-conditioned behavior prediction.

For every component, classify it as:

- Essential under current evidence.
- Beneficial but replaceable.
- Unsupported or inconclusive.
- Unnecessary given a simpler alternative.
- Not yet tested.

Do not preserve a component merely because it appeared in the original SOAM architecture.

## 3. Propose a minimal viable research architecture

Design the smallest coherent implementation supported by the completed studies.

Show:

- State representation.
- Recurrent update equations.
- Sensory correction mechanism.
- Action influence.
- Persistent memory structure, if justified.
- Gating and attention control, if justified.
- Interfaces between independently supported components.

Explicitly identify where a conventional GRU, structured state-space model, associative memory, or other baseline remains preferable.

Separate inference-time state updates, persistent learning, and offline consolidation.

## 4. Compare with established research

Evaluate the resulting design against relevant established approaches, including:

- GRU and LSTM recurrent state-space models.
- Continuous attractor models.
- Hopfield/modern associative memory.
- Predictive coding and state estimation.
- Recurrent state-space world models.
- Hierarchical active-inference or belief-tracking approaches.
- Object-centered sensorimotor learning.

Use primary research sources where feasible.

Identify what SOAM genuinely adds, what it reproduces from known techniques, and what remains an untested hypothesis.

## 5. Research strategy

Propose the next three highest-value experimental questions.

Rank them by:

- Importance to embodied sensorimotor intelligence.
- Degree of uncertainty.
- Ability to distinguish competing mechanisms.
- Expected information gain.
- Implementation complexity.
- Compute/data cost.
- Dependency on previous findings.

Authorize only the highest-value bounded continuation through the repository's normal research-gate process.

## 6. Final deliverables

Produce:

1. A scientific synthesis report.
2. An evidence-supported minimal architecture specification.
3. A diagram of the inferred information and control flow.
4. An updated research hypothesis ledger.
5. A conditional experimental roadmap.
6. A publication-oriented summary of the most important positive and negative discoveries.

Be willing to conclude that simpler established models explain the results better than the proposed architecture.

The objective is not to validate SOAM as originally imagined. The objective is to discover a useful and scientifically defensible path toward recurrent embodied sensorimotor intelligence.

---

## How I'd use these with Codex

The first two assignments are the most important right now. Study A tells us whether adaptive gating explains E1's GRU advantage. Study B directly tests your snapshot-settling-motion-correction hypothesis, regardless of whether Study A ultimately favors a GRU or a different recurrent core.

**Research execution checklist** Track your progress

of  completed [Copy progress]

**One additional recommendation\:** Don't let Codex interpret an inconclusive experiment as a reason to automatically build something more complicated. Sometimes the most valuable next experiment is a better control, a more demanding task, or longer training of the existing baseline.

**Context summary\:** Seven sequential Codex prompts: planning, adaptive gating, temporal sensory assimilation, three-mode hypothesis control, persistent associative learning, navigable object memory, and final scientific synthesis. Preserve E1's negative result; advance through evidence-based gates, retaining strong GRU, linear, and structured-memory controls.

## Response:
11/10/2026, 2:18:07 PM · gpt-6-thinking

I’ll add this as a later-stage architecture-search track, not an immediate implementation task. The prompts will define the three topology families, require narrow within-family sweeps first, and establish a fair tournament protocol for comparing very different networks once the earlier recurrent-memory mechanisms are better understood.

> **Building study prompts**
>
> I’m framing several copy-ready prompts that extend the roadmap without prescribing implementation. I’ll emphasize fair comparisons, ablations, biological motivation, scaling, stability, and the distinction between learning dynamics and runtime inference.
>
> **Built study prompts**
>
> 
>
> **Extending the roadmap**
>
> I’m adding prompts that formalize architecture families, matched comparisons, biologically motivated mechanisms, scaling and stability tests, and a staged tournament with explicit falsification criteria and resource-normalized evaluation.
>
> **Extended the roadmap**
>
> 
>
> **Refining architecture studies**
>
> I’m separating family-specific sweeps from the final tournament, with matched tasks, parameter and compute budgets, frozen evaluation, multiple seeds, scaling tests, stability metrics, and explicit controls for routing, feedback, sparsity, reconstruction, and gated recurrence.
>
> **Refined architecture studies**
>
> 
>
> **Searched 11 websites**
>
> 
>
> Worked for 4m 1s

# SOAM Architecture Search - Additional Codex Research Prompts

I would add this as a **new, later-stage research track: Population Topology and Hierarchical Recurrent Intelligence**\.

Your observation about architecture search is especially important: early experiments should distinguish narrowly defined mechanisms, while later experiments can compare fundamentally different architectures on increasingly general capabilities.

I would organize it into three additional Codex prompts\:

1. **Prompt F - Architecture search roadmap\:** Define monolithic, stacked, and horizontal neural population families and their research dependencies.
2. **Prompt G - Controlled within-family architecture sweeps\:** Experimentally isolate the architectural advantages and limitations of each family.
3. **Prompt H - Cross-architecture tournament\:** Promote the strongest candidates into increasingly challenging embodied intelligence benchmarks.

One important theoretical distinction: **gating can improve gradient propagation without guaranteeing forward dynamical stability.** Research on GRU dynamics supports examining slow modes and recurrent Jacobians, while work on deep equilibrium networks highlights the need to test fixed-point stability explicitly. \[[Gating creates slow modes and controls phase-space complexity in GRUs and LSTMs](https://proceedings.mlr.press/v107/can20a.html?utm_source=chatgpt.com); [Stabilizing Equilibrium Models by Jacobian Regularization](https://proceedings.mlr.press/v139/bai21b.html?utm_source=chatgpt.com)\]

That makes large gated recurrent populations especially interesting, but not automatically stable.

## Prompt F - Add population topology research to the roadmap

Planning only. Do not run new experiments.

**document: **

# SOAM Future Research Track: Population Topology and Hierarchical Recurrent Intelligence

You are the principal research scientist responsible for extending the SOAM research roadmap.

We want to investigate whether embodied sensorimotor intelligence is better supported by a large monolithic recurrent population, a hierarchy of recurrent populations, or multiple horizontally connected recurrent populations.

This investigation is a future research track, not an immediate implementation request.

## 1. Research motivation

Current SOAM research focuses on individual recurrent systems, adaptive gating, sensory assimilation, persistent associative memory, and object-centered sensorimotor prediction.

Eventually we need to investigate how multiple recurrent populations should be organized.

Important questions include:

- Does scaling one densely recurrent population offer advantages over distributing the same capacity across smaller populations?
- Does hierarchy allow useful abstractions to emerge through dimensional compression, expansion, or feedback?
- Can separate recurrent populations exchange compact associative cues instead of their full internal representations?
- Can recurrent populations settle independently while exchanging information?
- Can one neural population simultaneously perform encoding, decoding, prediction, and associative completion?
- Does distributed specialization reduce interference or merely impose artificial boundaries?
- What organizational principles emerge when all architectures have comparable resource budgets?

Treat the possibility that a monolithic recurrent network is sufficient as a legitimate hypothesis.

We are not trying to validate cortical-column modularity by construction.

## 2. Define three architectural families

### Family A - Stacked hierarchical populations

Multiple recurrent populations arranged into successive processing levels.

Each population may maintain independent recurrent activity.

Neighboring populations exchange representations using learned projections.

Consider several distinct organizations.

**A1. Feedforward hierarchy**

Information progresses upward through multiple recurrent populations.

Each level may perform local recurrent settling before transmitting its output.

Higher levels may have fewer neurons than lower levels, producing compressed representations, or more neurons, producing expanded representations.

Investigate whether local settling improves the information passed upward.

**A2. Bidirectional recurrent hierarchy**

Each population sends information both upward and downward.

Lower-level activity incorporates predictions or contextual feedback from higher-level representations.

Each population may settle independently, while adjacent populations iteratively revise one another's state.

Study both synchronous and asynchronous update schedules.

**A3. Shared encoding/decoding populations**

Instead of separate encoder and decoder neural populations, one recurrent population may support both ascending inference and descending reconstruction.

Input and output projection matrices may be distinct, shared, transposed, or constrained.

Do not confuse sharing one recurrent state population with mathematically tying the encoder and decoder weights.

Compare:
- Separate encoder and decoder populations.
- Shared recurrent population with distinct input/output projections.
- Shared recurrent population with tied or approximately symmetric projections.
- Bidirectional reconstruction using recurrent dynamics.

**A4. Hierarchical equilibrium or predictive-correction systems**

Consider whether adjacent populations can iteratively settle toward mutually consistent representations.

Investigate whether this resembles amortized inference, predictive coding, or deep equilibrium computation.

Do not assume convergence or construct an energy function without proving the necessary assumptions.

### Family B - Horizontally distributed populations with routing

Multiple recurrent populations operate at approximately the same organizational level.

They maintain independent local state while communicating through a learned routing mechanism.

The routing layer is inspired by thalamocortical communication, but does not need to reproduce biological thalamic anatomy.

Potential communication mechanisms include:

**B1. Direct lateral communication**

Populations exchange learned messages over fixed connections.

**B2. Central message router**

A routing population receives compact messages and directs information to selected recipients.

**B3. Sparse associative cue routing**

Populations transmit compressed cue vectors or associative addresses rather than full hidden states.

Receiving populations use these cues to activate or calibrate local memory hypotheses.

**B4. Cross-population consensus**

Multiple populations provide evidence about a common hypothesis.

A learned or prescribed consensus mechanism determines whether representations should agree, compete, or remain complementary.

**B5. Learned conditional routing**

A controller adjusts which populations communicate based on task, uncertainty, relevance, and available compute.

Avoid introducing privileged object identities or simulator state into the router.

A routing mechanism is not automatically advantageous merely because it produces sparse messages. Measure routing cost, information loss, and interference.

### Family C - Large monolithic gated recurrent populations

One large recurrent state space supports multiple functions without explicit boundaries between neural populations.

Investigate progressively larger recurrent systems with:

- Dense recurrent connections.
- Adaptive update gates.
- Action-conditioned asymmetric dynamics.
- Symmetric or approximately symmetric associative interactions.
- Optional sparsity or structured connectivity.
- Multiple timescales.
- Potentially heterogeneous gating patterns.

Important question:

Can gating permit a large recurrent system to preserve useful state, learn complex dynamics, and maintain separable hypotheses without explicit architectural decomposition?

Distinguish trainability from forward stability.

Gating may mitigate vanishing gradients, but this does not establish that larger recurrent systems will exhibit well-behaved attractors, accurate free trajectories, or low interference.

Explicitly investigate these questions rather than assuming the answer.

## 3. Research principles

The three families should share a common abstract interface for:

- Sensory input and masks.
- Action-conditioned state updates.
- Optional recurrent settling.
- Sensory prediction.
- State correction.
- Hypothesis readout.
- Persistent memory interfaces when justified.

However, do not force every implementation into the same internal computation schedule if doing so artificially disadvantages an architecture.

A modular hierarchical architecture and a monolithic recurrent system may require different internal computation to solve the same external task.

Compare them using equal externally observable task requirements and explicitly measured resource budgets.

## 4. Architecture search strategy

Adopt a hierarchical search strategy.

### Phase 1 - Narrow mechanism comparisons

Within each family, vary one architectural property at a time.

Examples:

- Hierarchical depth.
- Projection dimensionality.
- Presence or absence of feedback.
- Number of populations.
- Routing sparsity.
- Local versus global settling.
- Dense versus sparse recurrence.
- Gate organization.

Keep experiments small enough to attribute performance differences to specific mechanisms.

### Phase 2 - Within-family sweeps

Explore combinations that are justified by Phase 1 evidence.

Identify a small number of Pareto-efficient candidates from each family.

### Phase 3 - Cross-family tournament

Compare the best candidates from each family on a common suite of increasingly demanding tasks.

Include conventional neural and structured-memory baselines.

### Phase 4 - Autonomous embodied tasks

Only after the earlier comparisons are informative, evaluate the strongest architectures on more general sensorimotor tasks requiring partial observation, active disambiguation, continual memory, multiple objects, and increasingly autonomous behavior.

Do not treat these phases as automatically authorized development milestones.

## 5. Research dependencies

This track should generally wait until earlier experiments have clarified:

1. Which recurrent update/gating mechanisms are useful.
2. Whether sensory assimilation benefits from distinct prediction/correction phases.
3. How single or multiple hypotheses are maintained.
4. Whether persistent associative memory is necessary.
5. Which minimal object-centered tasks can be evaluated reliably.

A negative result in an earlier study may simplify or redirect this track.

For example, if ordinary recurrent dynamics outperform a constrained Hopfield mechanism, permit ordinary GRU populations in the topology comparison.

Do not require a favored lower-level mechanism to win before investigating topology.

## 6. Scientific literature

Create a focused research map covering:

- Deep equilibrium networks and recurrent fixed-point inference.
- Predictive coding and hierarchical recurrent inference.
- Thalamocortical gating and distributed cognitive control.
- Modular recurrent networks and mixture-of-experts routing.
- Neural architecture search and multi-fidelity model selection.
- Gradient propagation and dynamical stability in gated recurrent networks.
- Associative memory capacity and interference in large recurrent populations.

Distinguish biological evidence, mathematical results, and proposed engineering mechanisms.

## 7. Required planning deliverables

Add a future research track to the appropriate SOAM roadmap documents.

Produce:

- A population topology research RFC.
- Explicit hypotheses for Families A, B, and C.
- A comparison of the three families' computational and memory characteristics.
- Proposed within-family experiment sequences.
- A staged architecture-search strategy.
- Prerequisites and decision gates.
- Resource budgeting principles.
- A list of capabilities deferred until after simpler experiments.
- A preliminary benchmark capability ladder.

Follow existing ticket and milestone conventions.

Do not reuse existing stable experiment or ticket identifiers.

Avoid creating a large number of speculative implementation tickets. Prefer a bounded roadmap and conditional research branches.

Do not implement, train, or benchmark the new architectures yet.

The goal is to incorporate population topology into the long-term research strategy while preserving the current critical path.

## Prompt G - Design controlled architecture sweeps within each family

Experimental protocol design. This prompt explicitly tackles the difficulty of comparing architectures with different depth, connectivity, and computation schedules.

**document: **

# SOAM Population Topology: Controlled Within-Family Architecture Sweeps

## Objective

Develop a rigorous experimental program for comparing variations within three recurrent architecture families:

A. Stacked hierarchical recurrent populations.

B. Horizontally distributed populations with learned communication and routing.

C. Large monolithic gated recurrent populations.

The primary research principle is:

**Narrow comparisons should isolate mechanisms. Broad comparisons should evaluate capability.**

Early architecture search must not become an unrestricted optimization tournament in which differences in architecture, training budget, input information, and hyperparameter tuning make the results uninterpretable.

This assignment is to design the protocol and conditionally scoped experiment inventory. Do not launch full training sweeps until the relevant research prerequisites and decision gates are satisfied.

## 1. Common task interface

Specify a common task interface supporting:

- Sensory feature vectors and validity masks.
- Action commands and physical elapsed time.
- Hidden recurrent state or states.
- Optional internal recurrent computation.
- Predicted next sensory observations.
- Optional object and pose hypotheses.
- A controlled sensory-correction operation.

Each architecture must receive the same externally available information for the same task.

The simulator owns physical state, object identity, true pose, and ground-truth future observations.

Do not leak these into neural architectures, routers, projection layers, or memory addresses.

Distinguish physical time from internal computational iterations.

An architecture may settle recurrent activity several times while the environment remains at the same physical timestep.

Every such iteration must be included in compute accounting.

## 2. Establish a controlled recurrent primitive

For the earliest topology experiments, use a common well-supported recurrent primitive wherever possible.

For example, if prior studies favor a GRU-like gated recurrent unit, use that primitive across monolithic, hierarchical, and modular candidates.

This helps isolate topology instead of comparing a GRU against a completely different rate equation.

Later experiments may allow family-specific mechanisms, but then architectural topology and recurrent mechanism must be treated as jointly varying factors.

Include conventional recurrent and structured-memory baselines appropriate to the task.

## 3. Family A: Stacked hierarchical populations

Investigate four major design dimensions.

### A1 - Depth

Compare:

- One recurrent population.
- Two recurrent populations.
- Three recurrent populations.
- Additional depth only if justified by evidence.

Adjust population widths to construct approximately parameter-matched candidates.

Measure how depth affects:

- Representation quality.
- Convergence.
- Free prediction.
- Information loss.
- Optimization.
- Compute latency.
- Sensory robustness.

### A2 - Dimensional compression and expansion

Compare constant-width, bottleneck, and expansion arrangements.

Examples:

    Input -> Wide -> Narrow

    Input -> Narrow -> Wide

    Input -> Wide -> Narrow -> Wide

Do not assume that narrower layers produce semantic abstraction automatically.

Use controlled probes to determine what information survives each transformation.

Test whether compressed representations preserve object identity, pose, action dynamics, or only whatever information minimizes the immediate training loss.

Keep information-bottleneck effects separate from depth effects.

### A3 - Feedforward versus bidirectional coupling

Compare:

1. Feedforward-only projections.
2. Feedforward projections with independent recurrent settling.
3. Bidirectional learned projections.
4. Bidirectional projections with iterative cross-layer correction.

For bidirectional models, distinguish two possible computations:

**Sequential inference**

Lower layers settle, send an estimate upward, and receive feedback afterward.

**Joint iterative inference**

Neighboring layers repeatedly exchange messages while converging toward mutually compatible states.

Do not claim that either procedure minimizes a global energy unless the required mathematical properties hold.

Measure whether feedback provides value beyond additional parameters and recurrent iterations.

### A4 - Same-population encoding and decoding

Test whether a population can support both upward encoding and downward reconstruction.

Compare:

- Distinct encoding and decoding populations.
- One recurrent population with distinct input/output projections.
- One recurrent population with tied or transposed projections.
- One population that supports both functions through mode-conditioned updates.

Include tasks where information must be reconstructed from an upper-layer hypothesis without access to the original lower-level input.

Otherwise, a shortcut may make the autoencoding result trivial.

Measure:

- Reconstruction accuracy.
- Preservation of latent identity.
- Response to partial cues.
- Interference between upward and downward processing.
- Whether the same recurrent state is genuinely reused.

A shared output projection or equal weight values are not evidence that the same neural population performs both functions.

## 4. Family B: Horizontal populations and routing

Investigate four independent factors.

### B1 - Number of recurrent populations

Start with small configurations such as two, four, and eight populations, adjusted for the total resource budget.

Determine whether additional populations help by supporting distinct hypotheses, specialized representations, or independent temporal dynamics.

### B2 - Communication mechanism

Compare:

1. No interpopulation communication.
2. Dense direct communication.
3. Fixed sparse communication.
4. Central learned routing.
5. Conditional top-k or sparse associative-message routing.

Measure message size, communication operations, routing latency, and retained communication state.

A router is part of the model and must count toward all resource budgets.

### B3 - Message representation

Compare transmitting:

- Full hidden-state projections.
- Compact learned embeddings.
- Associative cue vectors.
- Belief/confidence summaries.
- Structured messages containing distinct identity, pose, or uncertainty fields.

Distinguish fields provided by the task from fields learned by the network.

Avoid giving a modular architecture privileged role labels that monolithic competitors must infer.

Measure what information is lost during compression.

### B4 - Cross-population consensus

Study how populations reconcile inconsistent information.

Compare:

- Independent local beliefs.
- Weighted averaging.
- Learned attention over messages.
- Iterative consensus.
- Competition among incompatible hypotheses.

Create separate tasks for competing and complementary hypotheses.

A correct architecture must not merge two simultaneously valid objects simply because their representations communicate.

Measure convergence toward the correct interpretation, not merely agreement between populations.

Include routing failures, stale messages, and delayed communication.

## 5. Family C: Monolithic recurrent scaling

Investigate whether a single large recurrent population can support multiple functions through gating and internal specialization.

Vary:

- Recurrent population width.
- Recurrent connectivity density.
- Fixed versus adaptive update gates.
- Global versus per-unit gating.
- Symmetric versus asymmetric recurrent contributions.
- Action-conditioned transformations.
- Optional structural constraints such as normalization or spectral regularization.

### C1 - Capacity scaling

Use a bounded width progression chosen from measured baseline costs.

A provisional progression might include widths 16, 32, 64, and 128, but actual widths must be selected and frozen by the resource protocol.

Measure whether performance improves smoothly with parameter count, reaches a plateau, or deteriorates because of optimization or interference.

Dense recurrent parameter count ordinarily grows quadratically with population width. Report actual counts including gating, sensory projections, and readouts.

### C2 - Gating and gradient propagation

Analyze whether adaptive gating improves the ability to train larger recurrent populations across longer sequences.

Measure:

- Gradient norms over increasing unroll horizons.
- Vanishing and exploding gradient incidence.
- Sensitivity to initialization.
- Effective state retention timescales.
- Training convergence and variance across seeds.
- Performance after matching optimization effort.

### C3 - Forward dynamical stability

Treat forward stability as a separate scientific question.

Measure:

- Hidden-state boundedness.
- Long-horizon free prediction.
- Perturbation amplification.
- Correct recovery after perturbation.
- Local recurrent Jacobian singular values and relevant eigenvalues.
- State-space contraction and expansion.
- Sensitivity to sensory and action inputs.
- Temporal drift and spurious state collapse.

Where feasible, estimate finite-time perturbation growth or Lyapunov-like diagnostics.

Do not infer global stability from local Jacobian measurements alone.

Do not infer correct associative attraction from contraction alone.

### C4 - Gated Hopfield-like recurrence

If investigating symmetric associative connections with gating and asymmetric action dynamics, define the update equation precisely.

Consider whether gating preserves, modifies, or destroys any proposed energy-descent property.

A symmetric weight matrix does not by itself guarantee monotonic energy decrease in an arbitrarily gated, driven, discrete-time network.

If an energy function is proposed, specify its assumptions and either derive the result or label it a hypothesis.

Compare against ordinary gated recurrent networks rather than assuming the Hopfield-like constraints are superior.

### C5 - Emergent internal specialization

Investigate whether the monolithic population develops distinguishable representations or activity regimes for:

- Sensory reconstruction.
- Motion prediction.
- Identity maintenance.
- Pose tracking.
- Alternative hypotheses.
- Attention-dependent computation.

Use causal interventions in addition to visualization.

Do not interpret clustered neurons or linear probe accuracy as conclusive evidence of specialized functional modules.

## 6. Resource-equivalent comparisons

Parameter matching alone is insufficient.

Design comparisons along several independent resource dimensions:

**Total trainable parameters**

Include recurrent weights, gates, projections, router networks, readouts, and other learned components.

**Persistent and active memory**

Include all population states, inactive retained states, router state, persistent association tables, and caches.

**Inference computation**

Count recurrent updates, projections, routing, message passing, and settling iterations.

**Measured latency**

Record actual wall-clock inference latency under defined hardware and batch-size conditions.

**Training resources**

Record optimizer steps, unique grounded observations, total training operations, hyperparameter search trials, and elapsed compute.

**Communication**

For modular architectures, record bytes or scalars transmitted between populations, message frequency, and routing cost.

Use both:

1. Closely parameter-matched diagnostic comparisons.
2. Accuracy-versus-cost Pareto comparisons.

Do not claim that one architecture is universally more efficient based on matching only one resource.

A width reduction to match parameters may change representational capacity. Document that trade-off rather than hiding it.

## 7. Controlled search methodology

Implement a staged search protocol:

### Screening

Use small models, cheap datasets, and limited training runs to detect clear failures.

### Development

Evaluate plausible candidates on more seeds, stronger tasks, and declared resource comparisons.

### Confirmation

Freeze the selected configurations and evaluate them on reserved independent data.

Do not repeatedly tune on confirmation results.

Use matched hyperparameter-search opportunities and a finite total budget across families.

Include a limited robustness check with different reasonable optimization settings so that poor training is not mistaken for architectural inferiority.

## 8. Scientific deliverables

Produce a protocol defining:

- Explicit hypothesis for each architectural factor.
- Minimal representative models.
- Exact ablations.
- Relevant baseline families.
- Common task interfaces.
- Fair resource-accounting rules.
- Search budget and confirmation requirements.
- Decision thresholds.
- Expected failure cases.
- Within-family advancement criteria.

For each family, identify the minimum result that would justify a more expensive architecture sweep.

Explicitly identify which experiments can be shared between families and which require family-specific probes.

At the end, provide a plan for selecting no more than a small number of Pareto-efficient candidates from each family for a later cross-architecture tournament.

Do not execute the full sweeps in this planning assignment.

## Prompt H - Design the cross-architecture research tournament

Long-term benchmark design. Strong candidates advance through progressively more general tests of sensorimotor intelligence.

**document: **

# SOAM Architecture Tournament: From Controlled Dynamics to General Sensorimotor Intelligence

## Research objective

Design a multi-stage architecture evaluation system for comparing fundamentally different organizations of recurrent intelligence.

The primary architectural families are:

A. Hierarchically stacked recurrent populations.

B. Horizontally distributed recurrent populations with communication and routing.

C. Large monolithic gated recurrent populations.

Include competent conventional baselines and hybrids where scientifically justified.

The goal is not merely to discover which network wins on one benchmark.

The goal is to identify **which architectural principles become useful as tasks demand greater representation capacity, sensorimotor integration, ambiguity handling, compositional reuse, and continual learning**.

## 1. Fundamental principle

Architecture comparisons are most interpretable when competing models differ in only a few controlled properties.

However, very different architectures may become difficult to compare fairly on narrow mechanistic tests because they use different computation schedules, representations, and organization strategies.

A hierarchical network may perform multiple rounds of internal inference.

A horizontally modular network may preserve several simultaneous hypotheses.

A monolithic model may encode the same information implicitly in one large state.

We should not artificially prevent these approaches from exploiting their defining advantages.

Instead, distinguish two different experimental goals:

**Mechanistic experiments**

Control architectural differences tightly and isolate causal contributions.

**Capability tournaments**

Give architectures a common external task and resource constraints, allowing them to use different internal strategies.

As research advances, increase the emphasis on functional capability while retaining controlled ablations for explaining important differences.

## 2. Tournament entry requirements

Architectures become eligible only after completing appropriate within-family experiments.

Each candidate must provide:

- A reproducible implementation.
- A frozen architecture description.
- A record of its training and tuning resources.
- Measured inference and memory costs.
- Independent performance estimates.
- Known failure modes.
- A clear distinction between provided task scaffolding and learned representations.

Select a bounded Pareto-efficient set from each family.

Do not select a single family representative solely based on one noisy benchmark result.

Candidates that offer different accuracy/compute/memory trade-offs may all be worth advancing.

## 3. Benchmark ladder

Design progressively more demanding benchmark rounds.

### Round 0 - Computational and scientific sanity

Purpose: Validate common functionality and detect implementation errors.

Tasks:

- Feature reconstruction.
- Action-conditioned prediction.
- Short recurrent rollouts.
- Missing-feature recovery.
- Deterministic reproducibility checks.

Do not use this round to make broad architectural superiority claims.

The original E1 environment may be included as a sanity test, but its low-dimensional structure is unlikely to reveal the full benefits of population organization.

### Round 1 - Recurrent dynamics and representational capacity

Purpose: Test recurrent competence under a controlled, shared task distribution.

Include:

- Multiple learned transformation regimes.
- Longer action-conditioned rollouts.
- Partial observations.
- Noisy sensory correction.
- Rapid context switching.
- Hidden-state perturbations.
- Increased latent complexity.
- Interference between simultaneously relevant features.

Measure prediction accuracy, recovery, stability, and resource efficiency.

Architectures should receive the same observations, actions, and evaluation targets.

### Round 2 - Structured sensorimotor inference

Purpose: Determine whether population organization improves object-centered internal representations.

Tasks:

- Object identity from partial cues.
- Pose estimation and path integration.
- Action-conditioned feature prediction.
- Landmark correction.
- Multiple possible reference-frame hypotheses.
- Occlusion and changing visibility.
- Detection of inconsistent sensory evidence.

This round tests the usefulness of internal organization beyond ordinary sequence prediction.

Compare whether hierarchical feedback, routed populations, or monolithic recurrent representations provide advantages.

### Round 3 - Multi-object and compositional intelligence

Purpose: Evaluate the reuse and coordination of learned representations.

Tasks:

- Track multiple objects.
- Preserve object identity through occlusion.
- Maintain alternative hypotheses.
- Transfer learned transformations between related objects.
- Predict relationships between objects.
- Reuse learned components in withheld configurations.
- Resolve conflicting information across representations.

Measure performance as the number of interacting objects or hypotheses grows.

Include explicit structured-memory controls.

Do not describe success as compositional generalization unless the evaluation genuinely withholds relevant combinations.

### Round 4 - Active autonomous sensorimotor inference

Purpose: Move from passive prediction to purposeful information gathering.

Allow an agent to choose actions to reduce uncertainty or achieve sensorimotor goals.

Examples:

- Select a viewpoint that distinguishes ambiguous objects.
- Navigate around an object to recover its identity.
- Revisit a landmark to recalibrate pose.
- Choose observations needed to confirm a hypothesis.
- Plan short action sequences using learned predictions.

Separate world-model quality from action-policy quality.

At least one comparison should use a common planner or action-selection procedure across candidate world models.

A separate end-to-end comparison may allow learned policy differences, with those differences explicitly reported.

All candidates must operate under equivalent action budgets, observation access, and training allowances.

### Round 5 - Continual embodied memory

Purpose: Investigate whether architectures can accumulate useful experiences over longer sequences without destructive interference.

Tasks:

- Acquire unfamiliar object memories.
- Revisit familiar objects after learning new ones.
- Retain sensorimotor dynamics.
- Update incorrect beliefs.
- Reuse established representations.
- Operate under bounded memory.
- Recover from misleading observations.
- Generalize to new sequences of familiar components.

Use long-duration evaluation with independent held-out object families and environmental conditions.

Measure accuracy, acquisition cost, forgetting, memory growth, and inference latency.

This round is a future target, not an automatically authorized implementation stage.

## 4. Fairness and resource constraints

A scientifically defensible tournament must not rely on a single arbitrary parameter count.

Evaluate multiple resource regimes.

At minimum consider:

**Parameter-budget track**

Compare candidates with approximately equal total learned parameters.

**Inference-compute track**

Compare candidates given equivalent computational budgets per physical timestep.

**Memory-budget track**

Compare candidates with equivalent available persistent and active state storage.

**Training-budget track**

Compare architectures given equivalent training observations and comparable total optimization/search budgets.

**Unconstrained efficiency frontier**

Allow architectures to vary in size and report achievable accuracy versus measured resources.

These tracks answer different questions and should not be collapsed into one claim of fairness.

Include internal recurrent settling, routing, feedback projections, memory lookup, and inactive retained states in resource accounting.

Measure actual latency as well as estimated operations.

For architectures with conditional computation, report average and worst-case costs.

## 5. Tournament advancement

Use a multi-fidelity selection process.

### Preliminary screening

Run low-cost tests to eliminate clearly invalid or dominated implementations.

Do not automatically eliminate models merely because they converge slowly during training.

### Within-family qualification

Promote the strongest candidates from each architecture family using preregistered criteria.

### Cross-family comparison

Compare selected candidates on common held-out tasks under multiple resource budgets.

### Robustness confirmation

Retest promising advantages using additional seeds, independent trajectories, and relevant out-of-distribution conditions.

### Capability advancement

Advance models to more autonomous tasks only when there is sufficient evidence that the additional complexity addresses meaningful research questions.

Do not silently modify a frozen tournament after observing confirmation results.

A new benchmark or changed selection rule requires a versioned protocol and fresh confirmation evaluation.

## 6. Metrics and statistical interpretation

Use multiple outcome dimensions:

- Sensorimotor prediction accuracy.
- Associative recall accuracy.
- Correct hypothesis identification.
- Pose and reference-frame consistency.
- Recovery after perturbation.
- Transfer to withheld combinations.
- Continual retention.
- Action efficiency.
- Runtime and memory efficiency.
- Robustness across seeds and environment conditions.

Specify primary outcomes per round rather than constructing one universal accuracy score.

Avoid treating correlated trajectory steps as independent experimental replications.

Report uncertainty around both performance benefits and resource guardrails.

Use predeclared practical effect sizes and sufficient precision to distinguish meaningful improvements from noise.

An architecture may be preferable in one resource regime and inferior in another.

Such trade-offs are scientific findings, not failures of the tournament.

## 7. Causal architectural interpretation

Suppose the horizontal modular architecture wins on multi-object tracking.

Do not immediately conclude that cortical-column-style routing is responsible.

Possible explanations include:

- More available independent hidden states.
- Sparse communication.
- Reduced cross-task interference.
- Additional computational steps.
- Architectural specialization.
- Easier optimization.
- Greater effective capacity.
- Better matching between task and architectural inductive bias.

Design follow-up ablations to isolate the mechanism.

Similarly, a successful stacked hierarchy does not establish emergent abstraction merely because hidden layers differ.

A successful monolithic network does not establish that explicit modularity is unnecessary at larger scales.

For each major tournament result, identify the smallest causal follow-up needed to explain it.

## 8. Scaling laws and crossover analysis

An important goal is to identify whether performance advantages change with problem complexity.

Study scaling along separate axes:

- Total recurrent capacity.
- Number of concurrently relevant objects.
- Number of active hypotheses.
- Observation dimensionality.
- Prediction horizon.
- Action-space complexity.
- Memory capacity.
- Environmental ambiguity.
- Required temporal abstraction.

Investigate whether different architectural families show crossover points.

For example:

- A monolithic recurrent system may dominate at small task sizes.
- Hierarchical feedback may become advantageous as abstraction requirements increase.
- Horizontal routing may become useful as simultaneous independent hypotheses increase.

These are hypotheses to test, not predicted outcomes.

Model the relation between task complexity, computational cost, and performance.

Where possible, distinguish scaling trends from artifacts of limited optimization or mismatched resource allocation.

## 9. Hybrid architectures

Do not introduce hybrids during initial topology comparisons because they can obscure attribution.

After meaningful family-specific strengths and weaknesses have been identified, permit targeted hybrids.

Examples:

- Hierarchical populations with horizontal communication.
- Monolithic recurrent layers inside a larger modular architecture.
- Shared recurrent dynamics with thalamus-inspired routing.
- A large monolithic recurrent population with sparse dynamically recruited subpopulations.
- Hierarchical predictive correction combined with independent object-memory hypotheses.

Every new hybrid must address a diagnosed limitation and be compared against the simpler architecture from which it was derived.

Do not construct a hybrid merely because combining successful components appears intuitively attractive.

## 10. Biological interpretation

Maintain a critical separation between functional architecture and anatomical analogy.

Compare potential computational functions associated with:

- Cortical hierarchy.
- Recurrent cortical microcircuits.
- Thalamocortical routing.
- Distributed cortical communication.
- Local associative attractor dynamics.
- Attention-dependent neural gain.

Identify which findings are empirically grounded, which are computational theories, and which are SOAM-specific hypotheses.

The final architecture need not resemble biological anatomy if another organization performs better.

## 11. Required deliverables

Produce:

1. A versioned architecture tournament RFC.
2. A benchmark capability ladder.
3. A fair-comparison resource-accounting specification.
4. A multi-fidelity selection protocol.
5. A statistical evaluation and confirmation plan.
6. A procedure for preserving and reporting negative results.
7. A conditional dependency graph connecting earlier SOAM studies to the tournament.
8. A proposed architecture-scaling analysis.
9. Advancement and stopping criteria.
10. A plan for causal follow-up experiments after important tournament results.

Do not execute the tournament as part of this assignment.

The next implementation step must be selected through the existing evidence-driven research process.

## 12. Final research question

What organizational principles are genuinely beneficial for constructing recurrent systems capable of increasingly general embodied sensorimotor intelligence?

In particular:

**When does one shared recurrent population become less effective than several populations that communicate through learned hierarchical or horizontal relationships?**

Seek empirical scaling boundaries, causal explanations, and resource trade-offs rather than a predetermined winning architecture.

---

## Two ideas I'd emphasize in the planning

**First, treat topology and operating mode as orthogonal research dimensions.** Your primed/tracking/attended concept doesn't necessarily require three populations. A single monolithic network could exhibit those modes in different parts of its state, while a horizontal architecture could assign them to different populations, and a hierarchy could apply them at different abstraction levels.

**Second, the thalamic routing hypothesis has a strong computational motivation beyond biological resemblance.** A 2024 review discusses how thalamocortical circuits may coordinate distributed computation and promote efficient reuse. \[[Thalamocortical architectures for flexible cognition and efficient learning](https://pmc.ncbi.nlm.nih.gov/articles/PMC11305962/?utm_source=chatgpt.com)\] That supports investigating routing as a computational mechanism, while still requiring the experiments to show whether it outperforms simpler direct communication.

The most intriguing comparison may ultimately be **a large recurrent population with dynamically recruited subpopulations versus a collection of explicitly bounded recurrent populations with learned routing**\. Those architectures could begin to resemble each other functionally as they scale, even though their connectivity and state management differ.

I'd keep that as a future hypothesis rather than a fourth immediate architectural family.

**Compressed research summary\:** Added three future Codex prompts: F defines stacked, horizontal-routed, and monolithic recurrent families; G specifies controlled within-family architecture sweeps, including feedback, bidirectional encoding/decoding, thalamic routing, and gated-network scaling; H establishes a multi-fidelity tournament progressing from simple recurrence to autonomous continual sensorimotor intelligence. Compare multiple resource budgets, not parameters alone. Gating improves trainability but doesn't guarantee dynamical stability.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)