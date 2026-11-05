# Scientific and architectural review — 2026-11-05

Owner-requested review recorded in [SOAM-060](../tickets/SOAM-060-scientific-roadmap-review.md).
This is a planning assessment, not an experimental result. It refines v0.3 and its
conditional paths. Quantitative targets below are proposed protocol defaults;
SOAM-049/039/053 must adopt or justify revisions before fitting or confirmation.
Historical protocols, reports, H1–H8 wording, and completed decisions are unchanged.

## Assessment

SOAM is a plausible research programme for a useful sensorimotor memory mechanism.
It is not yet a sufficiently specified architecture for approaching human-like
sensorimotor intelligence. The most promising question is whether recurrent
associative computation can combine fast grounded acquisition, interference control,
and reusable action-conditioned structure at modest resource cost. Shared neurons,
attractors, or graph-free storage alone do not establish that combination.

The existing project has unusually useful experimental discipline: state/parameter/
evaluator separation, no-write prediction, reproducibility, explicit scaffolding,
and preserved negative results. Its evidence remains narrow. The substrate controls
have unresolved H1 claims; the [writer demonstration](../reports/LOCAL_WRITE_CONTRACT.md)
reduced immediate errors while worsening some held-out multistep predictions. The
[handover report](../reports/HANDOVER_HARNESS.md) verifies fixtures and software, not
measured trained-model superiority. These are reasons to isolate acquisition risk
early, not to assemble a larger system around an assumed solution.

My recommendation is to keep the unconventional mechanism research, reduce the
architectural commitments, and change the default progression to **useful dynamics
→ rapid retained acquisition → active disambiguation → compositional reuse**.
Concurrency/handover remains a possible diagnostic fork, rather than the mandatory
bridge between all these capabilities. A conventional or hybrid model may win any
stage without invalidating the platform's scientific purpose.

## Foundations, existing approaches, and limits

These are focused primary-source checks, not a systematic literature review or a
proof audit. Source-derived observations and SOAM-specific judgments are separated.

| Foundation / primary source | Established result or reported evidence | What it does not establish for SOAM |
| --- | --- | --- |
| [Hopfield (1982)](https://pmc.ncbi.nlm.nih.gov/articles/PMC346238/) | Content-addressable recovery through recurrent collective dynamics in a specified model | Arbitrary asymmetric recurrence need not inherit its convergence conditions; useful embodied learning is a separate claim |
| [Chaudhry et al. (2023), Long Sequence Hopfield Memory](https://arxiv.org/abs/2306.04532) | Specified nonlinear asymmetric associative models support sequence-memory analyses and experiments | Replaying a stored sequence does not establish action-contingent transitions, online grounding, or compositional skills |
| [Burak and Fiete (2009)](https://arxiv.org/abs/0811.1826) | Continuous-attractor models can integrate velocity, with organization/noise-dependent drift | A stable bump or accurate odometry does not solve sensory correspondence, mapping, or uncertainty |
| [Driscoll et al. (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11239504/) | Trained recurrent networks exhibit shared dynamical motifs and task-reuse analyses | Motif reuse can occur in conventional RNNs; it is neither unique to Hopfield models nor evidence of unsupervised physical concepts |
| [Ramsauer et al.](https://arxiv.org/abs/2008.02217), [Schlag et al. (2021)](https://arxiv.org/abs/2102.11174) | Particular associative updates connect to attention or fast-weight formulations; the latter studies a delta-like correction | Renaming an attention or delta-rule update is not a novel architecture; recurrent grounding and lifetime of learned memory must be demonstrated |
| [Predictive Representations of State](https://proceedings.neurips.cc/paper/2001/hash/1e4d36177d71bbb3558e43af9577d70e-Abstract.html) | Predictive state offers an alternative to representing a hidden-world-state distribution in controlled systems | SOAM need not reconstruct a complete scene graph to maintain task-useful beliefs, but predictive sufficiency still requires tests |
| [Monty capability paper (2025)](https://arxiv.org/abs/2507.04494) | Reports sensorimotor object/pose learning, structured representations, policies, and module communication | Replacing structured memory removes useful inductive biases; a recurrent substitute must recover their function rather than merely omit their data structure |
| [NeuroSLAM authors' implementation](https://github.com/cognav/NeuroSLAM) | Combines recurrent pose processing with an experience-map component | It is a hybrid reference, not precedent for graph-free SLAM |
| [Bajcsy et al., Revisiting Active Perception](https://arxiv.org/abs/1603.02729) | Organizes the role of action in perception and uncertainty reduction | Passive prediction alone is an inadequate test of embodied information gathering; our proposed toy experiment remains much narrower |
| [DreamerV3](https://arxiv.org/abs/2301.04104), [TD-MPC2](https://arxiv.org/abs/2310.16828) | Strong learned-world-model approaches to behavior and continuous control | They are appropriate richer-stage references, not mandatory large implementations for a tiny memory experiment or proof of human-like learning |

The Driscoll publisher page/full-text access was restricted during this review;
primary-source indexed excerpts supported the narrow observation above. Exact
mechanism/equation replication still belongs to the relevant protocol. No claim is
made that this list is exhaustive or that all 2026 developments were surveyed.

The speculative conjunction is: one overlapping population will simultaneously
support content recovery, directed motion, instance binding, rapid persistent writes,
and reuse with manageable interference. Each term is plausible in some settings;
the conjunction is untested. Storage capacity and recall guarantees do not imply
identifiable causal structure, credit assignment, calibrated belief, or good control.

## Prioritized recommendations and gaps

Classification is relative to the immediate E1 pilot: **E = essential for the next
experiment; P = parallel research investigation; F = future capability**. F includes
high-value near follow-ups; it does not mean unimportant. Each recommendation has
one class and a traceable owner. No automatic additional experimental branch is opened.

| Rank / ID | Class | Recommendation and scientific risk | Ticket action |
| --- | --- | --- | --- |
| 1 / R1 | E | Make usefulness and mechanism attribution separate. Overlap alone may reflect a coordinate choice; generic shared RNNs already share units. Compare a constrained disjoint form and causal interventions in the declared unit basis. | Strengthen 049–052; no new ticket |
| 2 / R2 | E | Specify action-conditioned relation generalization, not just stored sequence replay or feature decoding. Include reversed/shuffled actions and withheld states within known transformations. | 049/050/051 |
| 3 / R3 | E | Freeze primary endpoint, meaningful margin, retention limits, split hierarchy, and data/parameter/state/tuning/compute budgets. A lucky seed or information advantage must not pass. | 047–052; common measurement contract below |
| 4 / R4 | F | Test few-observation acquisition before skills or full concurrency. Separate persistent learning from transient state correction and exact-example retrieval. | Move 039/044/040/041 earlier; remove skill and replay prerequisites |
| 5 / R5 | F | Add a small active-disambiguation task with calibrated uncertainty and intervention. Passive localization is insufficient for the embodied thesis. | Refocus 053–055; preserve NeuroSLAM inspiration, defer full mapping |
| 6 / R6 | E | Permit ordinary, separated, predictive-state, and hybrid alternatives. Graph-free memory is a tested candidate constraint, not a universal design virtue. | 047/049/059; candidate storage ledger |
| 7 / R7 | E | Build the smallest reusable runner around a decisive experiment. Avoid a generic framework, new environment stack, or simultaneous backend catalogue. | Narrow 047/048; tiny second fixture only if it exposes an actual coupling |
| 8 / R8 | P | Resolve specific theoretical questions about attraction, integration, fast weights, and representational equivalence using primary papers and small analyses. | 030; 045 only when its mechanism addresses a diagnosed limitation |
| 9 / R9 | F | Require withheld recombination and causal action interventions before composition claims; stable identity is a distinct challenge. | 031/016–018; Monty-style 056–058 remains a later option |
| 10 / R10 | F | Defer learned scopes/consolidation, recruitment/growth, learned action heads, richer encoders, and robot deployment until simpler mechanisms expose a need. | Existing conditional tickets retained; no new capability backlog |
| 11 / R11 | E | Separate hypotheses, consequential architecture decisions, implementation, and evidence with a short RFC attached to an existing decision ticket. | RFC guide; 047/049/039/053 |
| 12 / R12 | E | Preserve ticket-level traceability and negative gates. Prefer one selected follow-up by information gain/cost, not completing the architecture diagram. | 059; full disposition ledger below |

Missing longer-term capabilities include identifying causes from interventions,
learning sensor and action calibration, uncertainty over objects and correspondence,
object permanence, reference-frame changes, multi-object interaction/contact,
novelty detection, purposeful exploration, temporal abstraction, and retention over
long task sequences. R4/R5 address small pieces first. Multimodal perception,
body-model learning, manipulation, social learning, and language are **F**, recorded
as limitations rather than new tickets. We cannot infer proximity to human-level
intelligence from a count of implemented components.

## Architectural alternatives and a minimal mathematical contract

**E / R6:** keep the shared asymmetric candidate, a disjoint version with the same
observation/readout assumptions, and a small well-tuned GRU as the initial core
comparison. A simple action-conditioned linear/local predictor is a cheap task
sanity reference. Separate same-width mechanism ablations from capacity comparisons:
masking connectivity changes capacity and sparsity as well as sharing. Report both;
do not attribute every difference to neurons being shared.

**P / R8:** consider a fixed recurrent reservoir with learned readout, predictive-state
models, sparse assemblies, continuous attractor state plus associative fast memory,
and a conventional recurrent core with episodic retrieval. These offer alternative
ways to allocate stability, plasticity, and state estimation. A fast-memory/core
split is especially relevant if recurrent writes disrupt trajectories. None is
licensed for implementation merely by appearing here.

**F / R10:** use a small explicit structured-memory model as an application baseline;
consider full Monty, Dreamer, or TD-MPC2 only when the task and resource budget warrant
it. Conventional baselines must be competent, but should not become larger research
projects than the candidate. Report all offline training and selection costs.

An illustrative contract, not an approved mechanism, is

`h[t+1] = F_theta(h[t], a[t], z[t], c[t]; dt)`

`z_hat[t+1], belief[t+1] = D_phi(h[t+1])`

`theta_after = theta_before + U(grounded_transition, declared_memory)`.

`z[t]` is absent in free rollout; no future observations or truth enter the model.
For a selected leaky-rate candidate one may test
`tau * dh/dt = -h + sigma((W_s + W_d(a,c))h + Bz + b)`.
Define symmetry, masks, normalization, integrator, timescale, and cue removal exactly.
Separate recovery connections and directional modulation may act on the same units;
that equation is neither a stability proof nor a demand for distinct neuron banks.
Declare all fast matrices/caches persistent or transient by their actual lifetime.
A hidden-state reset after a write must not erase a claimed persistent memory.

## Proposed measurable demonstration sequence

Demonstration labels below are views over existing thematic M0–M8, not new ticket
schema milestones. The next three highest-value experiments are E1, E2, E3. After
E1, select one using SOAM-059; E2 is the default preference if the mechanism is
usable. E3 can instead use a conventional candidate after a negative sharing result.
No positive E1 result is mandatory for learning about alternative architectures.

| Demo / class | Capability and hypothesis | Minimum implementation / controls | Proposed quantitative decision | Dependencies, risk, next decision |
| --- | --- | --- | --- | --- |
| D0 / E | Trustworthy measurement, no scientific performance claim | Existing provenance/tests plus minimal runner; deterministic analytic fixture and known failure | 100% declared invariant checks; exact same-environment deterministic reproduction excluding timing; no target leakage | 047/048; risk is building a framework before a task; permits only E1 execution |
| D1 = E1 / E | Useful shared action-conditioned recurrence; operational H1 and directional mechanism | Fixed projection, one small action-conditioned transform family, supplied structure/offline fit; shared candidate, disjoint form, GRU, cheap linear sanity reference | At least 10% lower held-out transition NMSE than the strongest required comparator, positive paired 95% interval for improvement; recall degradation upper bound at most 0.005 NMSE; causal-overlap/action ablations and all-seed finite trajectories | 049–052; risk is capacity/decoder confounding; 059 selects learning, disambiguation, concurrency, diagnostic, or stop |
| D2 = E2 / F, next preferred | Persistent rapid acquisition without erasing prior behavior; operational H2, with H3 guardrail | One changed identifiable transformation parameter; freeze initial sensor; one selected writer; no-write, delta/RLS, online-gradient, and bounded retrieval references | At least 20% smaller normalized acquisition-error area over 0/1/2/4/8/16 distinct new transitions than strongest adaptive comparator; old-task NMSE increase upper bound at most 0.005; one-shot claim separately needs at least 20% reduction after one distinct new observation versus no-write and a positive advantage over adaptive controls | 039→044→040→041; no skills/concurrency/replay-stack prerequisite; risk is memorizing a point or state calibration; permits bounded belief/control integration or a credit-assignment diagnostic |
| D3 = E3 / F, next alternative | Move to resolve ambiguity, maintain belief, and reach a simple goal; operational H6/H7 | Tiny aliased 2D task, fixed sensor, few actions; candidate and GRU beliefs crossed with informative/fixed policy, plus a small same-data filter/structured reference | At least 20% fewer capped actions to correct localization/goal than strongest same-information reference, positive paired 95% improvement interval; success at least 90%, false confident commitments at most 5%; Brier deterioration at most 0.01 | 053–055; policy supplied and counted, no full SLAM/skills pipeline; risk is policy or privileged-map advantage; enables a narrow active-sensorimotor claim, not human intelligence |
| D4 / F | Reuse learned transformations on withheld combinations and poses | Existing task plus withheld recombinations; independent learning and retrieval controls; causal motif/binding ablations | Proposed 15% lower withheld-composition error, positive paired interval, prior-retention bound 0.005 NMSE; distinguish zero-shot transfer from faster acquisition | 031/016–018 or selected 056–058; requires actual primitive competence and later protocol review, not extra labels supplying the answer |
| D5 / F | Continual closed-loop demonstration with interruptions and revisits | Integrate only validated mechanisms; fixed memory; reactive, replay, and conventional recurrent controls | Proposed at least 20% fewer observations to criterion on related later tasks versus prior-experience-ablated learner; old-task success drop at most 5 percentage points; no capacity growth | 027/028 retain all empirical prerequisites; broad perceptual/robotics claims remain future; decide whether richer sensing is justified |

These margins are engineering decision proposals, not literature-derived biological
constants. Protocol decisions may revise them with a written task/noise/compute
justification **before fitting/confirmation**. Later changes require a new version
and fresh confirmation streams. A negative result with sufficient precision rejects
the tested practical advantage; a wide interval is inconclusive, not equivalence.
Guardrails and validity precede benefit interpretation. D4/D5 are provisional future
targets, not ready protocols. Attractor-specific conclusions additionally require
recovery/persistence tests under declared forcing conditions; a task benefit can be
useful while attraction remains unsupported.

## The next three experiments in operational detail

**E1 / E, SOAM-049–052.** Use continuous observations of a small low-dimensional
transform task and a fixed projection. Withhold input states and action combinations
within the declared task distribution; keep any stronger composition split separate.
Vary the implemented overlap with at most one partial-overlap diagnostic condition.
Use matched perturbation norms and equal-sized random/disjoint lesions, then compare
cue/action ablations and readout-only effects. Causal sensitivity in the declared
unit basis supports a mechanistic claim; rotation-dependent activation overlap is
not a basis-invariant measure of semantic sharing. Do not make successful handover,
learned concepts, or online plasticity a requirement for this experiment.

**E2 / F, SOAM-039/044/040/041.** Introduce an identifiable scalar or low-dimensional
change, such as a known transform family's gain, after offline competence is fixed.
One observation can identify a parameter only under supplied structure and suitable
excitation; it cannot determine an arbitrary transition function. Record that prior.
Use new grounded exposures at budgets 0, 1, 2, 4, 8, 16; evaluate unseen states/actions
and retained tasks after each budget with no writes. Reset transient state before
recall to distinguish persistence from contextual adaptation. Prohibit repeated
optimization/replay in the one-shot condition; count every update, history read,
and target exposure. A separate fixed-small-replay arm may be included only if the
protocol can implement it locally without the later consolidation stack. Compare
sample and compute efficiency separately. Report one-shot recall, one-shot
parameter adaptation, and generalization as distinct findings.

**E3 / F, SOAM-053–055.** Construct two locally indistinguishable situations requiring
different actions, with a short probe motion that reveals which situation holds.
Use a declared small action selector and cross model choice with active versus fixed
sensing. This separates improved inference from a better scripted policy. Compare
models on replayed equal observation histories for representation analysis, and on
paired initial environments/action budgets for closed-loop evaluation: different
policies naturally produce different histories. Include an ablation that removes
future-discriminating information and require calibrated uncertainty rather than
false certainty. Known-map/true-dynamics filters are labeled upper bounds; a fair
comparison learns or receives the same information as the candidate. There is no
claim of full SLAM or learned information-seeking policy.

The **smallest convincing embodied demonstration** combines the supported D2 memory
with the D3 task: learn one changed local transition from a small observation budget,
retain it after a state reset, use a probe action to resolve an aliased situation,
and achieve a held-out goal while retaining an earlier task. First establish D2 and
D3 independently so an integration failure is interpretable. Winning E1 alone is a
useful mechanism result, but is not evidence of rapid embodied learning.

## Measurement and reproducibility contract (E / R3)

Proposed confirmation seeds: 11, 23, 47, 71, 101, 131, 173, 211, 257, 307. Reserve
separate development streams/seeds (e.g. 401, 409, 419), task instances, and split
namespaces; no reuse of historical tests as unseen evidence. Use at least 20 paired
held-out episodes per seed/condition, averaging within seed before inference.
Pair initialization/data where meaningful; resample seed-level differences for a
prespecified paired 95% interval, not individual correlated trajectory steps.
Ten seeds are a practical proposal, not a guarantee of power; freeze the precision
and maximum-budget/inconclusive rule in the protocol.

Define NMSE denominator and a numerical floor from training/development data; do
not normalize each model differently. Freeze the strongest-comparator selection
rule using development only, and report against every mandatory reference so a weak
chosen comparator cannot conceal another reference's success. Proposed relative
improvement is `(reference_error - candidate_error) / max(reference_error, 1e-6)`.
If floor effects dominate, classify the comparison as uninformative and revise the
task before confirmation. Guardrail bounds use paired uncertainty, not just means.

Limit tuning to at most eight declared configurations per fitted candidate for the
initial protocol; report untrained/supplied candidates separately. Before tuning,
use engineering fixture timings to set a finite CPU/GPU-hour and storage cap in the
manifest. Stop at the cap and report incomplete/inconclusive results rather than
expand it silently. Try to match total persistent storage/parameters and live-state
budget within 10%; if impossible, report a small predeclared resource curve and avoid
claims of exact matching. Include readouts, copies, external memories, supplied
patterns, recurrent iterations, and all offline training. Same-width mechanism
ablations answer a different question and must be labeled accordingly.

Freeze configs, split generators, numerical settings, seed lists, source commit and
fingerprint, software versions, hardware, target/exposure counts, operation estimates,
wall time, and checkpoints. Reproduce one preselected full confirmation seed across
all conditions; fixtures alone do not count. Inference and imagined rollouts cannot
write persistent memory or consume future observations. Run the existing suite
before code modifications; this review itself changes documentation only.

## Organization, abandonment, and traceability

**E / R11:** [HYPOTHESES.md](HYPOTHESES.md) owns operational claims and links to the
unchanged historical hypotheses. [RFC guidance](rfcs/README.md) supplies a short
problem/alternatives/mechanism/evaluation/decision record inside existing decision
work. A protocol's numerical manifest owns frozen trial details. Engineering tickets
implement that contract; reports own measured evidence; gates interpret it. Reuse
one document when an RFC and protocol are the same decision. Avoid parallel copies
of equations or thresholds that can drift apart.

**E / R6/R12:** abandon unconditional claims that sharing is superior, that a graph
is intrinsically undesirable, that asymmetric recurrence inherits a general energy
guarantee, or that all future branches should be implemented. Preserve these as
falsifiable candidate choices where appropriate. Cancel no completed work and do
not discard negative results. Eliminate the mandatory skill/concurrency and full
shadow/replay dependency chain before the first acquisition study.

**P / R8:** retain focused literature/theory work and alternative formulations, with
read-only or small analytic investigations preceding any implementation request.
**F / R9/R10:** postpone full Monty integration, complete SLAM, rich perception,
learned motor libraries, growth, learned consolidation, and real hardware. Do not
turn the missing-capability list into new tickets now.

The [ticket disposition ledger](TICKET_REVIEW_2026_11_05.md) covers every pre-existing
ID and the review record, including unchanged and deferred work. Only one new ticket
(SOAM-060, this review) is allocated. No implementation, experiment, or empirical
gate is marked complete by this review.
