# Hypotheses and operational evidence ledger

Updated 2026-11-17. The historical [v0.1 H1–H8 statements](RESEARCH_SPEC.md) retain
their wording and provenance. The rows below are operational questions, not new
schema IDs or retroactive changes to those statements. Scientific criteria and
proposed numerical defaults live in the [review](SCIENTIFIC_REVIEW_2026_11_05.md);
frozen experiment criteria belong to the corresponding protocol/manifest.

SOAM-049 now freezes [E1 v1](SHARED_POPULATION_PROTOCOL.md) and its
[manifest](protocols/shared_population_v1.json). Its T32 control exposes an
identifiability limit: separate-role episodes cannot establish a performance
advantage of physical neuron overlap over tied weights. The test concerns a useful
shared implementation and unit-basis causal participation, with that limitation.
The [completed E1 v1+A1 measurements](../reports/SHARED_POPULATION_STUDY.md) record
absolute recall failure for S32 while both relative retention guards pass. Both GRUs
have lower primary error; all six causal precision criteria remain unresolved.
T32 is exactly equivalent and recovery accuracy fails despite distance contraction.
No useful E1 sharing benefit is established; this scoped result does not reject
shared neurons generally. [SOAM-052](../reports/SHARED_POPULATION_GATE.md) now records
**stop for the tested S32 useful-sharing claim**, applying absolute recall failure
before benefit; the scientific comparison is valid with disclosed reporting telemetry
limits. Positive interventions do not override unresolved precision or T32's limit,
and contraction does not establish useful recovery. Broader historical H1/H5/H6
remain open; this narrow failed gate is preserved. [SOAM-059](../reports/RESEARCH_FORK_SELECTION.md)
historically selected one E2 protocol design: ordinary G32 with a bounded recurrent
writer versus simple learning controls. The November 11 owner-selected Study A
superseded that current selection; SOAM-039 is backlog and acquisition/retention
remain unmeasured. Neither routing choice changes an E1 result or gate criterion.

| Historical claim / operational question | Prediction and importance | Convincing experiment / baselines | Success or failure evidence | Negative-result interpretation / class / tickets |
| --- | --- | --- | --- | --- |
| H1: multiple regimes; useful sharing | Shared recurrence should improve an explicit behavior/resource trade-off, not merely activate the same units | E1 action-conditioned transitions and causal overlap/action lesions; disjoint matched-information recurrence, GRU, linear reference | Proposed 10% error benefit with positive paired interval, recall guardrail 0.005 NMSE and finite rollouts; separate recovery evidence | No gain challenges useful sharing in this task, not all recurrence; poor precision is inconclusive. E, 049–052 |
| H1 mechanism subquestion: directed attraction | Controlled recurrent recovery and action-dependent transitions should survive removal of irrelevant drive without collapse | E1 small perturbation/cue-removal tests; symmetric-only and restoring-term ablations with identical external forcing | Proposed diagnostic: halve distance to the declared target set within 10 unforced updates with useful motion retained, versus restoring-term ablation; define phase/set distance appropriately and freeze completion/false-capture limits | Prediction may be useful without attraction; reject only the unsupported mechanism claim. E, 049/050/052 |
| H2: fast grounded acquisition | Few new observations should improve held-out behavior and survive a transient-state reset | E2 changed identifiable dynamics; no-write, delta/RLS, online gradient, bounded retrieval | Proposed 20% acquisition-area gain plus retention bound; separate one-exposure test and update/exposure ledger | Point memorization, contextual calibration, and persistent learning differ; failed recurrent writes motivate a fast-memory/core split or simpler learner. F, 039/044/040/041 |
| H3: learned scopes limit interference | A learned routing rule should preserve old functions at matched new-task accuracy while allowing positive transfer | Later fixed/random/sensitivity/learned masks with shared and isolated changes; E2 first establishes interference | Proposed at least 20% less protected-task error increase at new-task NMSE within 0.005 of the comparator, plus positive transfer on a related task and no extra exposure; freeze compute and uncertainty rules | If simple masks or unfiltered writes suffice, do not implement learned routing. If all fail, revisit writable representation. F, 007–010; E2 is a guardrail, not H3 confirmation |
| H4: consolidation improves organization | Refinement should add value beyond replay at equal grounded data and reported compute | Replay versus selected iterative refinement; shadow validation only when needed | Proposed at least 10% lower held-out error than replay at equal evidence and declared compute, positive paired interval, retention guardrail 0.005 NMSE and no extra capacity | Replay sufficiency rejects the complex mechanism's necessity; it does not reject memory learning. F, 011–015/042/043 |
| H5: consolidation discovers reusable transformations; separate broader reuse question | Learned primitives should support withheld recombination or faster related-task learning | D4 independent learning, retrieval, ordinary RNN, supplied-binding controls and causal motif lesions | Proposed 15% withheld-composition gain; no primitive/role labels leaking withheld combinations; distinguish zero-shot from few-shot | Similar activity or successful replay is not composition. Reuse without consolidation supports the broader question but not the historical mediation claim. F, 031/016–018/056–058 |
| H6: partial observations recover context | Belief should stay uncertain under aliasing and recover after informative sensing | E3 ambiguous paired worlds; fixed/active sensing, GRU, same-data filter, labeled oracle bound | Success/false-commitment/calibration guardrails plus capped-action endpoint; irreducibly ambiguous trials must remain uncertain | Collapse may indicate insufficient representation, identifiability, or calibration; richer encoder alone may not fix it. F, 053–055; later 037/020–022 |
| H7: recurrent planning benefits control | Model-dependent action selection should improve realized goal achievement or information efficiency | E3 supplied information-seeking policy crossed with models; later search versus reactive/equal-budget controls | Proposed 20% action-efficiency gain, 90% success, <=5% false confident commitments; no privileged future targets | Separate policy, model, and state-estimation failures. Better prediction alone does not establish control benefit. F, 053–055/023–026/038 |
| H8: cumulative learning | Related experience should reduce subsequent acquisition cost while retaining earlier competence | D5 fixed-capacity task sequences, prior-experience ablation, continual gradients/replay/task-specific references | Proposed 20% fewer observations to criterion, <=5 percentage-point old-task success loss; all storage and transfer failures disclosed | More stored episodes is not improved learning ability; fixed-capacity failure may justify a later budgeted structural study. F, 027/028 |

Status: the E1 v1 S32 useful-sharing claim is stopped; broader strong scientific
claims remain open. Historical Gate 1 and writer
contract readiness retain their limited recorded scope; handover fixtures are not
empirical evidence. E = essential next; P = parallel investigation; F = future
capability relative to E1. Primary-source precedents establish particular models or
empirical findings, not this conjunction of capabilities.

A report updates evidence links and supported conditions, not historical wording.
A failed decision stays failed. The fork record may authorize a new question with a
fresh protocol and confirmation set, never retroactively revise the prior outcome.

## Study A mechanism questions — 2026-11-11

[Study A v2](STUDY_A_PROTOCOL_V2.md), SOAM-062–065, is complete after the owner
selected it before acquisition. A-H1 adaptive retention; A-H2 adaptive reset;
A-H3 capacity/optimization; A-H4 low-dimensional system identification remain
subquestions of historical H1. The [report](../reports/STUDY_A.md) finds the frozen
adaptive-update practical benefit **inconclusive**: paired-root gain 9.92% versus
a 10% minimum and unresolved free-32 protection. Ordinary R32 is competent; the
GRU family improves short-horizon accuracy at higher training CPU, while learned
constant updates and low-order dynamics have favorable long-horizon results.
These findings do not establish necessity, useful attractors, associative-memory
complexity, compositionality or biological validity. The [decision](../reports/STUDY_A_DECISION.md)
recommends R32 as the smallest tested competent neural starting core, an explicit
post-study simplicity/accuracy judgment. The subsequent owner-selected Study B is complete through SOAM-066–073.
Historical H2–H4 meanings and SOAM-052 stop are unchanged.

## Study B temporal inference questions — 2026-11-11

[Study B v1](STUDY_B_PROTOCOL.md) operationalizes B-H1 deliberate sensory correction,
B-H2 useful zero-time settling, B-H3 adaptive sensory gain, and B-H4 conventional
recurrence sufficiency under historical H1/H6. The [completed report](../reports/STUDY_B.md)
finds better prediction from separate correction than the tested mixed-input
controls. Bounded settling helps within SET32, but its cost and corruption tradeoff
do not justify a mandatory default. V1's primary adaptive-gain result is a tradeoff;
the separately frozen [magnitude supplement](STUDY_B_MAGNITUDE_PROTOCOL.md) precisely
excludes the declared 10% practical gain. This does not imply zero effect or failure
of all possible adaptive gates. Conventional recurrence remains a mandatory
alternative; finite comparisons do not prove universal necessity of temporal structure.

SOAM-069's revise is preserved; SOAM-070–072 complete the missing magnitude test on
fresh streams. [SOAM-073](../reports/STUDY_B_DECISION.md) accepts separate correction,
PC16 as the small robust neural reference and FILTER2 as the strong accuracy/resource
reference with a corruption failure. It selects no next experiment. Fixed physical
evidence, pre-correction scoring, independent-root intervals, corrupted-versus-genuine-
change guardrails and explicit costs govern these scoped conclusions. The post hoc
recovery-baseline repair changes no primary result. Persistent learning, attention,
multi-hypothesis inference and biological validation remain outside scope.

## Study B2 robust correction — 2026-11-11

SOAM-074–077 operationalize H1/H6, preserving prior claims: B2-Q1 innovation reliability
(raw versus covariance-normalized); Q2 hard versus continuous rejection; Q3 bounded
measurement covariance adaptation; Q4 corruption versus genuine change with causal
history; Q5 statistical versus conditionally learned reliability; Q6 smallest useful
accuracy/robustness/resource tradeoff. [B2 v1](STUDY_B2_PROTOCOL.md) owns frozen tests.
A plausible coherent sensor offset and real displacement can have identical evidence;
no estimator can resolve that pair without additional information or assumptions.
No result implies shared neurons, attractors, learned organization or neuroscience.

B2 completed2026-11-12: [report](../reports/STUDY_B2.md) supports ADAPT1's52.69%
balanced-corruption improvement and NISEMP's45.01%, both under frozen ordinary/change
guards. Calibration and redundant measurement structure explain a useful scoped
benefit; coherent identical evidence remains unidentifiable. Temporal/hybrid screens
failed change protection. Heavy-tail and learned controllers were deferred, not
falsified. Statistical root uncertainty and actual runtime/storage costs are explicit;
this Torch implementation is slower than PC16 despite fewer MACs and fitted weights.
[SOAM-077](../reports/STUDY_B2_DECISION.md) selects conventional references only.
No operating-mode, hypothesis-management, attractor or shared-population claim passes.

## Study C hypothesis preservation — 2026-11-14

[SOAM-078 / C v1](STUDY_C_PROTOCOL.md) selects C-H1: retained candidate states may
improve proper uncertainty scores, delayed disambiguation and recovery beyond a
competent single state. Capacity and conventional-mixture explanations remain
mandatory alternatives. C-H2 selective computation and C-H3 learned allocation are
conditional separate studies; no operating-mode claim follows from C-H1. These
operationalize H1/H6 without changing historical definitions or the E1/A/B/B2 gates.

C-H1 completed under the frozen protocol. [Measured evidence](../reports/STUDY_C.md)
supports TWO16's probability-quality benefit over PC16 and PC32, including the
capacity control and all guards. The retained conventional mixture's .00157 Brier
gain is precisely below the .01 practical margin; TWO16 has no declared practical
accuracy advantage over that mixture. This supports the supplied neural conditional
factorization on this task, not a universal requirement for multiple retained states.
The [decision](../reports/STUDY_C_DECISION.md) recommends ADAPT1-C and the faster
TWO16 implementation for their respective tradeoffs. Nominal indistinguishable-world
uncertainty is preserved, but coherent-fault/genuine-change cause pairs produce
strong overconfidence. General ambiguity handling, C-H2 and C-H3 remain unsupported;
no next experiment or historical gate change follows.

## Study D persistent acquisition — 2026-11-17

[SOAM-082 / D v1](STUDY_D_PROTOCOL.md) selects D0–D2 under the owner's new routing
request. D-H1 operationalizes H2: new grounded object-specific information must
survive complete transient reset. D-H4 compares one rank-one associative recurrent
operator with bounded key-value storage and mask-aware online regression; H3 enters
as a sequential-retention guard, not confirmation of learned functional scopes.
Appearance and relationship are independent; the fixed sensor, reversible action
family, stable appearance correspondence and proprioceptive reference are supplied
scaffolding. The FAST block is algebraically a direct delta map / normalized online
gradient, so no uniquely recurrent advantage follows from renaming it. D-H2 whole-
model refitting, D-H3 selective writes, D3/D4, attraction and organization remain
untested. The versioned protocol owns the numerical hypotheses and stop rules.

D0–D2 complete: the [report](../reports/STUDY_D.md) supports persistent acquisition
and retention for KV under the frozen criteria. REG and FAST learn isolated objects
but fail sequential protection, with adjusted retention lower bounds above .02.
The FAST practical benefit is precisely negative against both controls. This is
scoped conventional-memory support and a negative result for one linear delta
operator, not a universal rejection of recurrent plasticity or a sharing/attractor
gate pass. [SOAM-085](../reports/STUDY_D_DECISION.md) accepts the evidence and KV
reference only; no later branch is activated.
