# Codex prompt — Study F coupling pilot: Gated intermingling and mutual settling of recurrent populations

**Status:** future conditional experiment; this document is a detailed *draft prompt*, not an active protocol. It may be selected independently of a whole-family F tournament once a minimal complementary-component task and strong controls exist.

## Research motivation

Study C (https://spencerbug.github.io/research/soam-study-c/) showed that two separate neural state instances sharing one fitted recurrent function outperformed single-state neural controls on a bounded supplied-motion-regime task. Both states were fully updated, never jointly recurrently coupled, and represented **competing** explanations. The result supports explicitly retaining alternative states; it does not demonstrate that multiple neural populations can temporarily combine their dynamics to support **complementary** simultaneous roles.

Investigate a different proposed mechanism: give populations their own dynamics and functional roles; enable gated, possibly bidirectional interpopulation connections; allow the combined dynamical system to mutually settle; disable those connections when the relationship is no longer relevant. The coupling should support expanded/compositional capabilities while leaving independent component memories usable. Components might encode an object pose and an object identity, two jointly present objects, or a relation/action context. Do not enforce these named roles as the only valid neural interpretation.

Core question:

**Can two or more independently useful recurrent populations temporarily become an interacting recurrent system whose jointly settled state yields useful information absent from each population alone, without wiping out or spuriously merging their constituent states?**

## Candidate contract and semantics

For a pilot, use two populations A and B with private recurrent states hA and hB and pretrained self dynamics FA/FB. Their actions and observations are separate streams where the environment allows them; a coupled relationship may be indicated by a *permitted* context cue, not truth about hidden causes.

At each physical step:
1. Advance the physical action-conditioned dynamics of both modules **once**.
2. Decode and score prior predictions **before** observing the new cue.
3. Correct each module from its own permitted evidence and masks.
4. If coupling is enabled, run a bounded number K of **internal joint-settling iterations at zero physical time**.
5. Read joint and individual task predictions; optionally turn off coupling while preserving both private states.

Illustrative coupled iteration (to be specified exactly by the protocol):

    input_A = WA @ hA + g_BA * C_BA(hB, context) + local_A
    input_B = WB @ hB + g_AB * C_AB(hA, context) + local_B

    next_hA = blend(hA, activation(input_A), local_leak_A)
    next_hB = blend(hB, activation(input_B), local_leak_B)

    hA, hB = next_hA, next_hB   # simultaneous, not secretly sequential

The gates g_AB and g_BA may be fixed, context-controlled or learned, scalar or low-dimensional; treat each as a controlled factor. Distinguish a cross-population message that merely feeds a decoder from actual recurrent coupling that changes both populations' subsequent internal dynamics. A low-rank off-diagonal block coupling is a useful minimal mechanism.

A more explicit joint block-weight design is:

    W_joint = [[W_AA, gate_BA * C_BA],
               [gate_AB * C_AB, W_BB]]

W_AA and W_BB remain private intra-population operators. Enabling off-diagonal blocks permits mutual recurrent influence. Turning gates off must recover the declared independent update law; test the degree to which *state* can return to correct independent trajectories after previously being influenced. No global contraction or energy guarantee is assumed.

**No external transition cheating:** do not pre-store correct object transitions, exact component relation graphs or evaluator labels in the controller. A supplied coupling/role cue in early tests is declared scaffolding and equal across all controls. Later generalization must use cue-based or learned selection; the external scheduler cannot simply output the true next state.

## F-coupling scientific hypotheses

- FC-H1: Bounded, genuine bidirectional recurrent coupling improves joint prediction or inference on held-out *combinations* compared with uncoupled independent modules and one-way cue exchange.
- FC-H2: Coupling gates permit reuse of private learned attractor-like or predictive states with acceptable post-decoupling retention and interference.
- FC-H3: Repeated mutual settling provides benefit beyond a single cross-population message/MLP readout at **matched computation**.
- FC-H4: Role-dependent dynamic gating improves conditional composition beyond always-on cross-coupling, while avoiding spurious agreement of inconsistent populations.
- FC-H5: Low-rank or sparse off-diagonal coupling offers a better capacity/accuracy/stability frontier than fully dense coupling.
- FC-H0: Concatenation plus a trained joint readout, direct one-way routing, a two-layer recurrent stack or a monolithic network with equivalent state/parameters/updates suffices.

Do not assume mutual settling is an energy minimization process. Test that convergence is toward the *correct compositional prediction*, not a fixed, wrong, or collapsed pattern.

## Minimal complementary-component task

Create two simultaneously existing processes with individually learnable sensorimotor structure and a relationship whose effect is testable.

Example conceptual construction:
- Population A learns object-relative viewpoint/pose dynamics.
- Population B learns a movable component, obstacle, or action-relation context with its own persistent identity and dynamics.
- A combined task requires correctly predicting an interaction or contextual constraint that neither individual module can infer alone.

An alternative is two independently moving landmarks/objects whose relative relationship determines a third sensory feature or action affordance. The relation must be learned from training examples, not looked up from simulator metadata.

**Critical:** benchmark includes (1) independent tasks where A/B should remain separated, (2) compatible compositions where collaboration helps, and (3) incompatible cues where agreement would be wrong. Withhold specific pairings or action compositions from training but ensure compositional generalization is information-theoretically possible. Do not reward memorized IDs or task-specific oracle composition labels.

Start with two small states (e.g. 16+16 versus a width-32 control), but select actual widths using a frozen parameter/compute budget. Reuse C's PC16/TWO16-style recurrence only if its equations and training contract are appropriate; C's mutually exclusive motion alternatives are **not** themselves the complementary target.

## Stage 1 — prove factorization before coupling

Train/test A and B independently for their own tasks with private recurrent state, stable prediction/correction and useful partial-cue recovery. Establish their individual competence and memory preservation. When possible, freeze their private weights for the first coupling pilot to isolate effects of cross-population interactions; if end-to-end tuning is needed, include an explicit separately labeled comparison.

Measure whether each module recognizes its component after hidden-state resets (if persistent memory is claimed), action reversals, and held-out viewpoints. Do not assert attractors merely from bounded tanh activity.

## Stage 2 — controlled communication and coupling ablations

At minimum compare:

- I0: independent modules + concatenated joint readout (no cross-recurrent influence).
- I1: one-way A->B feedforward cue; same communication dimension.
- I2: two-way single-step messages without joint settling (routing-only control).
- I3: always-on bidirectional cross-recurrent coupling.
- I4: context-gated bidirectional coupling with K>0 joint-settling steps.
- I5: K-matched no-coupling extra self-settling (controls added compute).
- I6: monolithic recurrent width ~= sum of active module widths, with capacity/tuning budget disclosed.
- Optional structured/explicit relational baseline whose learned relation structure comes only from training evidence.

Test separate dimensions after minimal screening: coupling on/off, gated versus ungated, one-way versus reciprocal, K={0,1,2,4} (provisional), coupling rank, and compatibility/incompatibility. Predeclare the finite sweep inventory and stop at first scientifically decisive level.

The full network during coupling must not quietly share recurrent state storage beyond what the resource comparison counts. If A/B retain anchors or protected private copies, include their memory and update costs. A monolith may retain any implicit separation its learning discovers; do not artificially prevent that control from adapting.

## Stage 3 — mutual settling and decoupling

Run controlled sequences:

1. Present partial evidence to A and B separately; let each obtain a meaningful prior.
2. Activate cross-population gates using the same allowed relation cue/context for all relevant models.
3. Run one or more synchronous internal iterations while holding physical time, actions and observations fixed; record both evolving states, losses and messages.
4. Decode joint relation/output *and* individual A/B outputs. Test if valid composition emerges without merging away component identity.
5. Remove cross-population coupling and continue independent action-conditioned tracking of A and B.
6. Re-present independent cues and measure recovery of previously learned individual states.
7. Later recombine with an unseen component pairing.

Check whether joint output improves while individual components remain distinguishable. If gating causes irreversible overwrite, spurious consensus or oscillation, record that failure.

A settled fixed point is not necessarily a correct attractor. Test target-directed perturbation recovery and long-horizon behavior. Record spectral/Jacobian and empirical perturbation diagnostics while avoiding unsupported global-stability claims.

## Stage 4 — optional learned coupling gate

Only if controlled fixed gating demonstrates a concrete tradeoff:
- use a small gate conditioned on available cues, predicted residual, compatibility scores or task context;
- compare a prespecified simple compatibility heuristic and fixed gate;
- train on disjoint combinations and test held-out pairings;
- avoid true relation labels, future evidence or externally supplied next-state IDs at inference;
- charge controller fit cost and inference overhead.

Separate the ability to **decide when to couple** from the ability to **settle usefully once coupled**. A positive gating-policy gain is not evidence that off-diagonal recurrent coupling caused the capacity gain.

## Measurements and fairness

Primary candidate endpoint: held-out combined-task action-conditioned prediction or relational identification, with independent component retention and recovery as hard guardrails. Include correct rejection of incompatible compositions; joint agreement is not a success metric by itself.

Report:
- Joint prediction and unseen-pair transfer.
- A/B independent prediction before, during, and after coupling.
- Identity/pose continuity under independent action.
- Perturbation recovery toward correct states; error vs number of settling iterations.
- Information leakage and spurious binding/false familiarity.
- Coupling-on/off hysteresis, oscillation, collapse, and wrong fixed points.
- Routing/coupling message dimension, number of active projections, gated weight storage.
- Total trainable parameters, private weights, coupling weights, caches, active/retained state, training exposure, inner iterations and measured mean/p95 inference latency.
- Effects under matched params, fixed physical observations, fixed inference-compute, and a multi-budget Pareto frontier.

Within-family comparisons should isolate factors; don't conflate two state banks with reciprocal coupling, learned gates, larger width, extra settling and additional supervision. A 32-wide single population, 16+16 pair, and two projected layers may have substantially different parameter counts; match/measure, never claim exact parity without arithmetic.

A finding about gradient propagation does not prove forward stability. For energy-like models specify full driven dynamics, damping and symmetry assumptions before claiming convergence.

## Method, stopping and decision

Before full experiments: inspect current repository and published C artifact provenance, establish an observability/information test, write lightweight protocol and manifest, unit-test equal evidence, fix candidate inventory, select independent root counts and fresh train/dev/confirmation streams, choose primary effect threshold and guardrails, finite training/CPU/GPU/memory/latency ceilings and stop conditions. Run tiny screening first; preserve every invalid or negative outcome. Freeze confirmation without looking at its data, and independently reduce result arrays. No imagined rollout writes persistent weights.

Decision branches:
- Positive reciprocal coupling with retention -> test the minimal useful gate/rank or another withheld composition under a fresh protocol.
- Routing-only or concat/readout equally good -> keep simpler communication; no claim for intermingling.
- Coupling improves joint task but destroys individual memory -> report composition/interference tradeoff; do not promote.
- Monolith dominates at matched resources -> retain monolithic reference; investigate topology only with a concrete scaling gap.
- Incorrect or spurious settling -> diagnose dynamical stability and evidence; don't hide with oracle resets.
- Unidentifiable task -> revise observability before interpreting performance.

Do not implement a full stacked/horizontal/monolithic tournament, new sensory encoder, generalized thalamic router, action planner or autonomous consolidation as part of this pilot. Don't alter historical E1/C gates or call these networks biologically validated cortical columns.

Deliver versioned protocol, implementation/tests, ablation matrix, paired root-level outcomes, state/settling traces, resource Pareto, scientific report and a *single* evidence-based next-step proposal.

**Final question:** Does temporarily gated mutual recurrent settling create useful, reusable *compositional* capability that independent populations, one-way cues, and a competent monolithic model cannot provide at comparable total cost—while preserving the populations' own memories?
