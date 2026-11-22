# Assembly organization and selective routing

November 22, 2026 · AO-1 planning scope ·
[SOAM-103](../../tickets/SOAM-103-assembly-organization-plan.md) ·
[Owner selection](../requests/assembly_organization_2026_11_22.md)

The next question is whether a recurrent population can learn selective pathways
among persistent representations while every neuron remains accessible to a dense,
fixed sensory projection. Learned organization is part of the first mechanism
study. Tree-like structure, semantic reuse, and reduced drift are outcomes to test;
they are not supplied architecture or assumed consequences of hysteresis.

This document retains the conceptual planning scope. The subsequently accepted
[SOAM-104 protocol](../STUDY_ASSEMBLY_ORGANIZATION_PROTOCOL.md) and
[manifest](../protocols/study_ao1_v1.json) own the exact equations, algorithms and
numeric contract. SOAM-104 is done/proceed; SOAM-105 is ready for implementation
and resource preflight. No model implementation or scientific fitting has started.
The earlier [E0-HYS design](../STUDY_E0_HYSTERESIS_PROTOCOL.md) remains
an unrun, unselected retention diagnostic; it is not a prerequisite for AO-1.

## Question and evidence

Can learned connectivity create reusable, selective causal routes through a single
population while preserving task-relevant state and allowing action-driven change?
The proposed organizing pressure is to incorporate evidence and predict action
consequences with limited interference, connection resources, and activity.
SOAM-104 selects L1 connection cost and soft activity-power regulation as one
bundled learning intervention. The sketches and alternatives below explain the
planning space; only the accepted protocol defines v1, which omits hysteresis.

[E0](../../reports/STUDY_E0.md) left its joint navigation/retention criterion
inconclusive. [E0-HOLD](../../reports/STUDY_E0_HOLD.md) reduced stationary error from
12.33 to 5.70 degrees but failed the declared joint fix and left recovery
noninferiority unresolved. Those results motivate preserving both retention and
navigation guards. They do not diagnose a missing hierarchy or demonstrate that
organization will solve drift. The completed decisions and all numerical results
remain unchanged.

The [hypothesis ledger](../HYPOTHESES.md#assembly-organization-and-selective-routing)
owns the operational claims. AO-1 is a bounded offline-learning mechanism pilot,
independent of the later integrated organization study SOAM-042/043. It cannot pass
that study's sharing/acquisition gates or establish the full historical H5 claim.

## Supplied conditions and learned organization

| Supplied and disclosed | Left for learning and measurement |
| --- | --- |
| Fixed-size population, modest sensory width, dense fixed projection, observation/action interface | Which neurons and collective modes become sensory-responsive or recurrently supported |
| Learning rule, finite fitting budget, activity/connection constraints | Useful recurrent connections and effective directional influence |
| Related observation sequences with cross-cutting factors and actions | Reusable representations and selective pathways between them |
| Fixed heterogeneous thresholds if that arm is included; assignment independent of sensory weights | How learned connections use those units; thresholds themselves remain fixed |
| Evaluation interventions and discovery procedure frozen before confirmation | Assembly membership, overlap, and routes inferred from permitted training/development activity |

Do not supply neuron groups, root/leaf labels, layer assignments, a tree, or a hard
mask restricting sensory entry neurons in the main candidate. Sensory missingness
masks are observation data, not neural entry masks. Dense anatomical connectivity
is permitted; sparse effective influence is a possible result, not a prerequisite.
Any supplied partition used by a control must be labeled and counted.

Offline gradient-based fitting is the initial practical candidate for credit
assignment. Local plasticity is an alternative only if the mathematical design
selects it with an explicit rule and comparable budget. Ordinary prediction
training alone is not evidence of learned organization. Online acquisition,
structural growth/rewiring, consolidation, and biologically local learning remain
separate questions. Persistent parameters are frozen during all evaluation.

## Mathematical planning scope and accepted specification

SOAM-104 completes this work in the [protocol](../STUDY_ASSEMBLY_ORGANIZATION_PROTOCOL.md).
It selects separate fixed sensory correction and directed leaky prediction, rather
than simultaneous sensory/action settling, to preserve predict-before-evidence
scoring. The following sketch is retained as planning context, not executable v1.

For an input x in R^d and N recurrent units, start from a dense fixed map P in
R^(N x d), N greater than d. The linear drive P x has rank at most d. This provides
population directions without direct drive from this map, not automatically
protected individual neurons. Nonlinearities and recurrence can propagate input
into other directions; expansion alone proves neither specialization nor stability.
Count every actual input channel, including availability indicators, in d.

A candidate family to analyze, rather than an accepted update contract, is:

```text
u_t = beta P x_t + R h_t + sum_k a_t[k] K_k h_t + b
q_t = (1 - alpha) h_t + alpha phi(u_t)
h_(t+1) = H_delta(q_t, h_t)
```

R is learned and may be directed at zero action. A symmetric-only restriction is a
control. H_delta is identity on q when delta is zero; fixed play hysteresis is an
optional persistence arm, not the study's definition. No assembly blocks are
prescribed. SOAM-104 must either select and complete this family or replace it with
one explicit alternative, giving the reason. It must specify initialization,
sensory correction, readout, action timing, parameter constraints, and the exact
learning update. The sketch must not silently replace the existing predict ->
score before evidence -> correct evaluation contract or replay an action during
internal settling. Initializers and correction maps must also be audited for
unreported direct input paths and supplied roles.

Input normalization is an experimental factor, not a side effect of N. For example,
P^T P = I keeps ||beta P x||^2 = beta^2 ||x||^2 fixed while average drive power per
neuron falls with N. Keeping per-neuron drive fixed instead increases total drive.
Declare the convention, effective input rank/covariance, and external-to-recurrent
drive measurements. Hold d fixed if N varies, and include a gain-matched control
before attributing a scaling effect to spare neurons. The first pilot should use
one declared N/d setting unless a finite size contrast is essential to its claim;
do not turn this plan into an open topology/ratio sweep.

The learning objective must distinguish prediction, retention of still-relevant
information, and activity/connection costs. A penalty on all state changes would
reward freezing and conflict with action navigation and sensory correction.
Ground-truth factors, semantic categories, or desired neural groups must not enter
the candidate's training loss. SOAM-104 must specify an observable-data-based
retention target, or omit that training penalty and use retention as evaluation.
Competition may act through normalization, a connection budget, or another bounded
rule; activity regulation needs its own equation. Do not bundle unspecified rules
under an unexplained "energy minimization" label.

Analyze at least these distinct questions:

- What breaks symmetry so that neurons or modes specialize, and what makes a
  route useful beyond common sensory drive? Coactivation alone does not specify
  preferential forward influence.
- Which quantities are bounded? Which regions or trajectories recover from
  perturbations? Strong recurrent weights and bounded activations do not prove
  either recovery or useful memory.
- Does the exact state update admit a decreasing energy or another stability
  argument under explicit assumptions? A training loss is not a state Lyapunov
  function; a symmetric-core proof does not automatically cover directed coupling,
  discrete time, hysteresis, or changing inputs.
- Which counterexamples remain possible: flat recurrence, independent persistent
  units, collapse to one assembly, dead units, direct sensory shortcuts, arbitrary
  clustering, or action-insensitive freezing? Do the proposed rules exclude them,
  merely discourage them, or leave them for empirical discrimination?

Use ordinary derivations and small algebraic/numerical checks first. A theorem of
global contraction would, under its usual assumptions, force a unique fixed point;
it cannot simply be adopted as proof of multiple memories. Lean is optional for a
stable, valuable theorem with explicit assumptions, such as invariant-region or
local perturbation bounds. It is not a prerequisite for the pilot, and verification
of an idealized model does not verify the PyTorch implementation or semantic claims.

## Smallest useful task and comparisons

Use one small synthetic task containing shared factors, distinguishing details,
and overlapping action applicability. A possible task has common geometry across
objects, independent appearance/detail, and a transformation relevant to only some
objects. Those examples guide task design, not class labels supplied to the model.
Observation sequences must contain enough evidence to distinguish the evaluated
cases. Truly aliased cases require uncertainty-aware scoring rather than impossible
correct-selection targets. A single orientation circle is insufficient for the
routing claim.

Select one learning/organization intervention and a finite candidate matrix in
SOAM-104. Mandatory comparisons are ordinary recurrence without the selected
organization pressure, symmetric-only dynamics, a separated-population reference,
and a competent conventional predictor or structured-memory reference on the same
observations. A family may serve two control roles only with explicit justification.
Match tuning opportunity and disclose all resource/prior mismatches. The E0 PCA2
reference must not be assumed competent on a different multi-factor task without
checking its representational adequacy.

If explicit hysteresis remains in the candidate, cross the selected organization
pressure on/off with hysteresis on/off; use fixed thresholds and paired assignments.
Separate any additional claim about heterogeneous thresholds from the primary
routing claim. Do not inherit E0-HYS's eight-family inventory, margins, seeds, or
allocation. A hand-wired routing example may validate the evaluator as a labeled
fixture; it cannot count as learned organization.

## Measurements and causal interpretation

The primary question is selective causal mediation with useful behavior. A candidate
primary quantity is the excess impairment of predicted dependent functions over
unrelated functions after interrupting a discovered route, relative to matched
control disruptions. SOAM-104 must define the exact quantity, comparator, useful
effect margin, uncertainty, and guardrails before fitting. Loss of accuracy after
lesioning an arbitrary important neuron is insufficient.

Discover candidate assemblies/routes using a predeclared procedure on training or
development streams; lock the procedure, per-fit discovery data access, intervention
selection, and thresholds before confirmation. Test on fresh episodes and withheld
factor/action combinations, not the episodes used to choose the route. A valid
outcome is that no reproducible route can be identified. Do not force clusters into
a tree or select attractive examples from confirmation activity.

Required evidence categories:

- **Mediation:** interrupt outgoing connections from a proposed source while
  preserving downstream direct sensory input. Compare with weight-, activity-, and
  intervention-size-matched controls as appropriate. Test reverse-direction effects
  and common-input explanations. Calibrate off-distribution lesion effects.
- **Specificity and reuse:** distinguish broad impairment, selective downstream
  impairment, and reuse across related held-out cases. Report assembly overlap and
  whether the learned solution simply partitions into independent populations.
- **Functional guards:** grounded one-step prediction, blindfolded action prediction,
  blindfolded zero-action drift, stationary prediction with sensory cues, cue-return
  correction, perturbation recovery, and interference with retained information.
  Include small actions, reversal, and release after a hold to expose freezing.
- **Organization:** effective influence and causal ordering are stronger evidence
  than weight magnitude or activation correlation. Multi-stage branching would
  support a narrower hierarchy claim; a useful overlapping graph is also allowed.
  Stable decoding from changing neurons is distinct from stable individual activity.

A downstream rescue can help distinguish route interruption from destruction of
the downstream representation. If included, define donor data and intervention
rules before confirmation; count the extra state/information and label it as a
diagnostic intervention, not ordinary model performance or autonomous retrieval.
Semantic organization requires held-out task-relevant reuse; visual clusters,
similarity to supplied factor labels, and lower drift alone do not establish it.

## Execution sequence and freezing requirements

| Ticket | Bounded deliverable | Readiness after SOAM-104 |
| --- | --- | --- |
| [SOAM-103](../../tickets/SOAM-103-assembly-organization-plan.md) | Adopt this scope and preserve the earlier design/history | Done/proceed for scope |
| [SOAM-104](../../tickets/SOAM-104-assembly-organization-protocol.md) | Complete equations and analytical checks; select one candidate/task; freeze a bounded protocol and manifest | Done/proceed for protocol; no fits |
| [SOAM-105](../../tickets/SOAM-105-assembly-organization-harness.md) | Implement exact rules, causal evaluator, counterexample fixtures, invariants, and resource preflight | Ready; not started |
| [SOAM-106](../../tickets/SOAM-106-assembly-organization-study.md) | Execute only the frozen development/confirmation inventory and exact repeat | Backlog until protocol and harness complete |
| [SOAM-107](../../tickets/SOAM-107-assembly-organization-decision.md) | Review organization evidence and retention/navigation trade-offs | Backlog until measured evidence complete |

The mathematical work may use tiny, enumerated, untrained counterexample checks;
record their inputs and limits before running them. Any exploratory learning is
development data, requires a finite protocol allocation before fitting, and cannot
later be presented as unseen confirmation. If exploratory findings change the
mechanism or endpoint, version the protocol and reserve fresh confirmation streams.

The completed SOAM-104 review freezes the exact update/learning equations and allowed
adjustments; finite model/configuration inventory; data exposure and held-out factors;
train/development/test seeds; discovery/intervention procedure; primary endpoint and
functional guards; practical margins; independent-root uncertainty and precision
rules; fit/repeat/fixture counts; CPU/wall/RSS/artifact limits; and stopping/failure
classification. A preliminary timing fixture may inform the budget but cannot be
used for scientific tuning. No positive result is required for ticket completion.

Use a new AO-1 namespace; do not reuse historical confirmation as unseen data or
spend E0-HYS's unused allocation. Count all parameters, projections, gates, buffers,
stored patterns, readouts, active/cloned state, offline passes, replay, and
intervention discovery cost. Preserve observation/target/evaluator separation and
no-write inference. The implementation must pass the existing suite before source
changes and relevant invariant/reproducibility checks afterward.

## Decision boundaries

Supported selective routing requires its frozen causal criterion and functional
guards. Useful prediction without selective mediation supports a predictor, not a
routing mechanism. Selective mediation with damaged retention/navigation is a
trade-off, not the joint capability. A useful graph can support routing while the
tree hypothesis remains unsupported. Adequately precise negatives, imprecise
inconclusive results, and invalid execution must remain distinct.

SOAM-107 may recommend at most one next bounded fork based on the evidence. It
cannot automatically activate a population tree, RIM coupling, online rewiring,
capacity expansion, HTM/learned-encoder sweeps, biological validation, or full SOAM
integration. Broad local-plasticity comparisons and Lean formalization remain
optional supporting work requiring a concrete question.

The owner plans a joint blog/report after the first AO-1 experiment and evidence
review. Publication should explain the tested mechanism, controls, measured results
and limitations, including a negative or inconclusive outcome. A concept-only
article is not the next task.

## Related work and limits of the analogy

[Litwin-Kumar and Doiron (2014)](https://www.nature.com/articles/ncomms6319) model
assembly formation using plasticity, inhibitory regulation, and synaptic
normalization. Those are precedents for candidate regulators, not the equations
or energy principle of AO-1 and not evidence of its proposed routing hierarchy.
[Mengistu et al. (2016)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004829)
find more functional hierarchy with connection costs in evolved networks whose
default architecture is already layered and feedforward. That motivates a possible
organizing pressure without proving emergence in an unpartitioned recurrent model.
[Lean](https://lean-lang.org/faq/) supports general mathematical and software
verification; choosing it depends on the theorem's value and specification maturity.
