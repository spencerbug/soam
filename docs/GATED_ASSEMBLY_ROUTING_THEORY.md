# Gated assembly routing: direction and initial theory

November 23, 2026 · [SOAM-108](../tickets/SOAM-108-gated-assembly-direction-and-theory.md)
· Source baseline `5f8333ba1086d15cef3a6db7ef88a9e3c3a623d3`

**Direction frozen; empirical protocol not frozen.** The owner selects learned
graph-based control of sensory access and recurrent exchange through two state
fields on the same indexed units. This document is the owning lightweight RFC
and initial mathematical analysis. It does not select final neuron equations,
learning rules, a supplied graph, a numerical pilot, or a capacity conclusion.
The later November 23 owner clarification in section 9 generalizes trees to
multiple-entry graphs and names the second field modulation. Sparse default
inhibition is a candidate, not a required outcome.
The [AO-1 v1 protocol](STUDY_ASSEMBLY_ORGANIZATION_PROTOCOL.md), manifest and audit
remain unchanged and unrun scientifically; SOAM-105–107 are unselected backlog.

## 1. Preserve the question

Can broad, redundant sensory access coexist with learned conditional recruitment
that admits evidence to relevant assemblies, protects other associations, and
reuses the same population across contexts? Routing means a causal chain of
receptiveness decisions; the observation need not be relayed as a packet down
that chain. Multiple entry populations, branching, merging, reuse and structural
cycles are allowed; trees are a special case. Independent flat selection alone
does not demonstrate activity-mediated recruitment through the graph.

Required constraints are dense fixed sensory projection, two dynamical states
per computational unit, learned rather than assigned assembly/entry/relay roles,
selective sensory and recurrent influence, and preservation of useful associative
support where active state must be retained. No privileged factor labels, hard
entry subset, or graph topology enters inference
or the learning target. Sensory missingness remains observation metadata. Ordinary
prediction, transient activity, persistent learning and evaluator truth stay separate.

Candidate choices remain open: gate parameterization, reciprocal content-to-gate
feedback, a joint energy versus another stability argument, symmetry/directionality,
competition, and the learning pressure that could produce useful graph organization.
Attenuation in [0,1] is the minimal starting family; amplification is not required
by this selection. Hysteresis and Lean remain optional, with fixed thresholds if
hysteresis is selected. Biological excitatory/inhibitory identity is not inferred
from two computational state variables or from signed model weights.

The [E0-HOLD report](../reports/STUDY_E0_HOLD.md) measured residual zero-action
error with no new observations. Sensory inhibition cannot directly remove that
existing zero-input drift. Learned organization could change the intrinsic dynamics,
but this is an untested indirect mechanism. Intrinsic drift, sensory interference,
cross-population interference and legitimate updating must remain distinct endpoints.

## 2. Information and time contracts

Let x be the currently available observation, including declared availability
metadata. Two fixed dense maps give s=P_h x and r=P_g x. For an illustrative
equal-total-drive construction with N>=d, each map may have orthonormal columns
scaled by 1/sqrt(2); then ||s||^2+||r||^2=||x||^2. The stacked map still has rank
at most d. This is redundant access, not extra independent information or free
capacity. Actual task normalization remains for the successor protocol.

Unit i stores content h_i and modulation/openness g_i; inhibition is 1-g_i, not a third
retained state. Both fields may receive the same unmasked observation through
their fixed maps. The mask can therefore react to evidence it blocks from content.
Whether it also receives content feedback is a mechanism question below.

The owner also proposes **associative modulation**, or **dynamic associative
modulation**: expose the modulation field to a cue, then allow its learned recurrence
to continue settling after cue withdrawal. Cue source, ongoing drive and recurrent
state evolution are separate choices. Earlier content can influence the subsequent
modulation trajectory through the state it established, even when current content
drive is absent. This can coexist with content-driven graph recruitment; it does
not require a third retained field or continuous content forcing.

This is an optional research question, not an established associative-memory result.
If selected, distinguish blindfolding external observation from additionally
isolating modulation from content drive. Useful completion/recovery from partial
or perturbed cues must be distinguished from simply holding a mask or converging
to a generic state. Specify any changed coupling dynamics: removing only one side
of a reciprocal interaction does not inherit the joint-energy proof below.

Use t for physical transitions and k or continuous settling time for internal
inference. The original analysis holds the available observation fixed during
internal settling; a cue-withdrawal variant must specify its input/coupling switches.
Repeated processing is not additional sensory exposure, and cannot replay an executed
action. The initial analysis is a stationary, zero-action subproblem. A successor
must specify a separate action/transition interface and predict-before-new-evidence
scoring before any sensorimotor study. Quieting a gate cannot silently erase an
executed action. No inference, intervention or imagined trajectory writes weights.

## 3. What isolation actually requires

Consider the general continuous content rule

```text
tau_h * dh_i/dk = -h_i + tanh(u_i)
u_i = sum_j W_ij C_ij(g) h_j + g_i s_i + b_i
```

C is an effective recurrent connection gate, not necessarily an independently
stored N-by-N gate state. At fixed g and input, h* is stationary exactly when
h*=tanh((W elementwise C)h* + g elementwise s + b). Closing g_i removes only
sensory drive; recurrence and leak still move h_i unless this equality holds.

For a discovered region B to be unaffected by arbitrary content changes in A,
the cross matrix (W elementwise C)[B,A]=0 is sufficient (and necessary for
arbitrary independent perturbations through an injective tanh at finite drive).
Insensitivity to arbitrary external x changes also needs diag(g_B)P_h[B,:]=0.
Neither condition establishes that the remaining B dynamics has a useful stable
memory. Outgoing protection of A requires the other cross direction separately.
These are analysis sets, not neuron groups supplied to the learner.

Changing gates preserves a particular h* at fixed input only if

```text
[(W elementwise C_new) - (W elementwise C_old)] h*
    + (g_new - g_old) elementwise s = 0.
```

This exact condition follows from tanh being injective. Symmetry or a decreasing
energy alone does not imply it. Cutting a supporting edge can destroy an attractor.

If a region's fixed-gate update map is L-Lipschitz with L<1 on an invariant local
region, an additive drive perturbation of norm at most eta shifts its equilibrium
by at most eta/(1-L), provided both equilibria lie in that region. Use the same
induced norm and tanh's Lipschitz bound. eta must include residual cross influence,
sensory leakage and gate changes. This is a conditional local bound, not a global
contraction requirement or proof of multiple memories. Uniform global contraction
on one convex invariant domain would instead imply a unique fixed point there.

### Scalar masks: a useful counterexample

Receiver gating C_ij=g_i removes both interference and supporting input when a
unit closes. Sender/receiver gating C_ij=g_i*g_j also removes recurrence inside
the closed population. This can implement dormancy if inactive memories remain
retrievable from persistent weights; it does not preserve arbitrary ongoing content
state. The owner’s later sparse-activity hypothesis makes this a legitimate
alternative to the compatibility gate, not an automatic design defect.
Multiplying the whole state update by zero explicitly
freezes it; it supplies neither recovery nor associative completion.

A minimal two-state compatibility gate is instead

```text
C_ii = 1
C_ij = g_i*g_j + (1-g_i)*(1-g_j), i != j.
```

At binary gates this preserves open-open and closed-closed connections while
cutting open-closed exchange. Diagonals are explicitly preserved. It supplies a
compatibility rule, not assembly membership. It is an analytical reference only:
all closed regions still exchange with each other, so it does not isolate several
background active states or establish causal graph recruitment. Soft endpoints epsilon and 1-epsilon
leave cross transmission 2*epsilon*(1-epsilon) and same-class off-diagonal gain
1-2*epsilon*(1-epsilon). At epsilon=.1 these are .18 and .82. Thus softness affects
both leakage and internal support. Gates of .5 give off-diagonal gain .5, not
complete access. The ungated control must explicitly use C=1.

One scalar mask is not proven incapable of graph recruitment or hierarchical behavior: dynamics
and learned connectivity could encode a conditional sequence. However, this
particular compatibility rule provides only one binary split in its limiting
form. This limits simultaneous compartmentalization, not all dynamic graphs.
A static split must not be relabeled mediated graph recruitment. Any extra
branch codes, gate fields or edge parameters must be explicitly selected and counted.

## 4. A joint-energy reference with exact reciprocal terms

This derivation establishes a possible energy-consistent coupled system. It is
not the final experiment candidate or a theorem of learned organization. Assume
finite fixed s,r,b, symmetric W and V, C as above, T>0, positive time constants,
h in (-1,1)^N and g in (0,1)^N. V connects gate states. Define

```text
Phi(h) = .5 * [(1+h)*log(1+h) + (1-h)*log(1-h)]
Psi(g) = T * [g*log(g) + (1-g)*log(1-g)]

E(h,g;s,r) = sum_i Phi(h_i) + sum_i Psi(g_i)
  - .5 * sum_ij W_ij*C_ij(g)*h_i*h_j
  - .5 * g^T V g - sum_i b_i*h_i - sum_i r_i*g_i
  - sum_i g_i*s_i*h_i.
```

Use the continuous extension 0*log(0)=0 for boundary energies. This energy is
bounded below on the compact state box for finite weights and input. Differentiation
gives the required content and gate drives:

```text
u_i = sum_j W_ij*C_ij*h_j + b_i + g_i*s_i
v_i = (V*g)_i + r_i + s_i*h_i
      + h_i * sum_{j != i} W_ij*h_j*(2*g_j-1)

dE/dh_i = atanh(h_i) - u_i
dE/dg_i = T*logit(g_i) - v_i

tau_h * dh_i/dk = tanh(u_i) - h_i
tau_g * dg_i/dk = sigmoid(v_i/T) - g_i.
```

The s_i*h_i term is the reciprocal of sensory gating; the final term in v is
the reciprocal of changing recurrent coupling. Dropping either generally breaks
this energy calculation. The gate depends on pattern agreement, not just total
activity magnitude: squaring or pooling content would define a different mechanism.

Monotonicity of tanh and sigmoid gives, term by term,

```text
(atanh(h_i)-u_i) * (tanh(u_i)-h_i) <= 0
(T*logit(g_i)-v_i) * (sigmoid(v_i/T)-g_i) <= 0.
```

Consequently dE/dk<=0, with equality in the interior only when both fields are
stationary. The rate equations point inward at the state-box boundaries. For
finite fixed weights/input their drives are bounded, so trajectories eventually
remain away from the singular derivative boundaries. The usual invariant-set
argument then approaches the equilibrium set; it does not promise the correct
memory, a unique equilibrium, a useful basin, a tree, or a capacity advantage.

At an interior equilibrium, let D_h=diag(1-h_i^2) and
D_g=diag(g_i*(1-g_i)/T). The joint linearization is

```text
J = -diag(D_h/tau_h, D_g/tau_g) * Hessian(E).
```

A positive-definite joint Hessian therefore gives local asymptotic stability:
J is similar to a symmetric negative-definite matrix. Checking each field's
diagonal Hessian block separately is insufficient; the cross block matters.
For example, diagonal blocks +1 with off-diagonal coupling -2 give a saddle.

Two separately descending energies do not supply this joint result. In particular,
an independent gate rule that sees only x,g generally cannot be coordinate descent
on the above energy: its h derivatives would omit the reciprocal cross terms.
This is an integrability restriction on this potential construction, not a proof
that one-way controllers cannot be stable or admit some other Lyapunov function.

Arbitrary directed W,V are not covered. Symmetric coupling can still have unequal
effective directional sensitivity through different operating gains, but does not
guarantee parent-child organization. A directed dissipative alternative needs its
own derivation. Changing input adds external-work terms to dE/dk. Discrete Euler
updates do not inherit continuous-time descent at arbitrary step sizes; even
Euler on dot(z)=-z increases z^2/2 at step size 3. No numerical integrator or
action dynamics is frozen by this reference.

## 5. Smallest discriminating study to design next

The largest architectural uncertainty is whether a cheap gate can protect content
while producing genuinely conditional, multi-step recruitment rather than ordinary flat
selection. The preferred explanation is learned recurrent content/receptiveness
coordination. Serious alternatives are (a) an instantaneous input-conditioned gate
that selects a flat subnetwork, and (b) stable ordinary recurrence plus sparse fixed
connectivity, with gate state supplying only extra parameters/memory. The one-way
recurrent controller remains a useful simpler mechanism alternative to joint feedback.
If its modulation state has no causal dependence on content at any time, including
initialization, it cannot establish content-driven recruitment when sensory history,
modulation initialization and any stochastic draws are held fixed. It can still test
whether modulation without content influence suffices for performance. This is
different from cue-initiated autonomous settling: content history can remain causal
through the modulation state after its driving cue is withdrawn. Autonomous
modulation is not restricted to a control arm.
An actual content-driven route can pass through intermediate modulation states;
the direct L interaction in section 9 is an option, not a mandatory architecture.
Supporting comparisons do not activate separate experimental branches.

Recommend one bounded, stationary partial-cue/distractor/change task containing
at least two linked recruitment events and shared factors, with multiple possible
entry populations and a shared downstream recipient as useful graph motifs.
These are evaluation/task proposals, not supplied candidate groups or topology.
Leave its exact generator and budgets to SOAM-109. All observations remain densely
available; no region labels, graph targets or privileged context enter training.
Entry/relay/recipient sets
must be discovered using training-side data, then locked before fresh evaluation.
The task may supply factor structure without assigning a neural graph, but that
scaffolding must be disclosed. Linked interventions distinguish a local mediated
path from independent flat selection; neither a path nor a merge alone establishes
a general useful graph. Cycles are allowed, not a compulsory pilot topology.

Keep input identical while intervening on the discovered upstream routing state
or its outgoing gate influence. Measure whether it changes downstream access,
whether the intermediate decision mediates the later change, and whether unrelated
recipients and recalled content remain usable. Include matched flat/common-input
and generic-disruption controls, restoration, and relevant cue changes that must
reopen access. Time order and clusters alone can falsely report routed recruitment.
Intervention states/clones are evaluator resources, never extra inference evidence.

Separate zero-input intrinsic drift, distractor interference, cross-population
interference and correct updating. Score against unmasked targets; shutting all
gates cannot remove errors from the objective. A capacity claim later needs
correctly retrievable associations/combinations across declared total budgets,
with false recall and retention guards. No superlinear claim follows from counting
possible masks, input expansion, a graph diagram or one successful size.

Outcome consequences: if flat gating matches the benefit, retain that simpler
explanation; if mediated recruitment appears without usable retained/retrievable content, reject the
joint mechanism claim; if retention fails with no input, address intrinsic support;
if the joint benefit passes, design a later resource-counted reuse/capacity test.
Do not run all these follow-ups or transfer v1's 231-fit budget. Cost now is one
finite algebra audit; fit cost and statistical precision are not yet estimated.
SOAM-109 must preflight both the primary endpoint and joint guards before freezing
sample counts, margins, intervals, width caps and compute limits.

## 6. Learning, accounting and adversarial review

The initial derivation does not learn. Future offline fitting must improve held-out
completion and selective updating from observation sequences; runtime settling
remains transient inference. Persistent acquisition after resets, executed-action
prediction and autonomous action selection remain untested. This is a component
question relevant to sensorimotor memory, not a demonstration of learning through play.

The reference stores 2N transient scalars, two recurrent matrices W,V, two fixed
dense maps, biases and any output readout. Symmetric W,V together have N(N+1)
independent coefficients if both diagonals are stored, or 2N^2 scalars when stored
densely. C adds no fitted coefficients in this example but its construction and
matrix products cost work and possibly temporary N^2 storage. Count all maps,
gate recurrence, gate histories, readouts, precision, fitting, settling latency and
diagnostic clones. Compare ordinary recurrence with comparable total resources,
not merely equal content width. Sharing an index does not establish biological
identity or the historical shared-population gate.

Distinct skeptical pass: the strongest simpler explanation is a flat conditional
subnetwork with more dynamical state. A counterexample is the compatibility gate's
single bipartition: it can protect one group without activity-mediated recruitment. A second is cutting
edges that maintain a fixed point, despite satisfying the joint energy theorem.
The most serious evaluator false success is assigning routes to correlated common-
input responses and calling generic lesion sensitivity mediated recruitment.
Locked discovery plus matched, stage-specific causal interventions is essential.
Remaining risks include self-confirming gates, all-closed/all-open solutions,
saturation mistaken for stability, initialization error, and an input-driven mask
that cannot distinguish identical observations under different stored contexts.

Primary-source context: [Hopfield (1984)](https://www.rctn.org/bruno/public/papers/hopfield84.pdf)
provides symmetric graded-response energy reasoning. The coupled energy and gate
derivatives above are derived here, not imported as a theorem from that paper.
[Spratling (2008)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2576514/) analyzes input-
targeted inhibitory feedback and a specific predictive-coding/competition equivalence;
it is a close mechanism precedent, not this learned gate or a capacity result.
[Mengistu et al. (2016)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004829)
study connection cost and hierarchy in evolved networks with supplied layered
feedforward architecture. Their result does not establish emergence in this system.

## 7. Predeclared finite algebra audit

The following allocation was written before execution. Run once, untrained, using
Python/Torch on CPU, float64, one thread and deterministic operations. No optimizer,
task-data generation, model selection, fitted exploration, learned tree search or
trajectory sweep is permitted. Defects may be corrected and rerun within the
cumulative limits, with every attempt recorded. The code reads this exact JSON.

<!-- algebra-audit-config:start -->
```json
{
  "version": 1,
  "seed": 20261123,
  "dimension": 4,
  "samples": 64,
  "temperature": 0.7,
  "tau_content": 1.0,
  "tau_gate": 2.0,
  "finite_difference_epsilon": 0.000001,
  "gradient_tolerance": 0.00000001,
  "dissipation_tolerance": 0.000000000001,
  "cpu_seconds": 60,
  "wall_seconds": 120,
  "rss_bytes": 1073741824,
  "artifact_bytes": 10485760
}
```
<!-- algebra-audit-config:end -->

Check (1) manual energy derivatives against autograd and centered finite differences,
and the joint linearization at one constructed equilibrium;
(2) continuous dE/dk and inward boundary fields; (3) binary compatibility versus
receiver/outer-product gates, soft leakage and diagonal preservation; (4) loss of
a supplied fixed point when supporting connections are cut; (5) nonzero motion
without sensory drive; (6) reciprocity mismatch when gate feedback is omitted;
(7) positive diagonal Hessian blocks with an unstable joint saddle; and (8) the
explicit Euler counterexample. The 64 draws use h in [-.7,.7], g in [.15,.85],
s,r,b as .3 times standard normal, and W,V as .2 times symmetrized standard
normal matrices. Fixed counterexamples are defined in the accompanying script;
none is a learned model or a capacity measurement.

The audit must save resolved settings, all checks/failures, numerical versions,
source commit, script/config/source fingerprints, seed, timing, peak RSS, exact
sample exposure and zero fitted-parameter updates. Its checks validate equations
and counterexamples only; they do not certify the proposed future causal evaluator.

## 8. Completion and next decision

The one declared execution of [the audit script](../scripts/check_gated_routing_theory.py)
passed all ten checks, including resources. [Raw results](analysis/gated_routing_theory_checks.json)
retain the complete configuration, 64 per-case diagnostics and source fingerprints.
Maximum manual/autograd gradient discrepancy was 3.33e-16; centered finite-difference
discrepancy was 4.38e-10, below 1e-8. The equilibrium linearization discrepancy was
1.11e-16. Every sampled continuous energy rate was negative (maximum -0.323656).
These samples support the implementation of the written derivation, not a
universal theorem established by simulation.

The supplied supporting-edge counterexample changes an exact fixed-point residual
from zero to -0.308687 per unit when its supporting cross edges are cut. Soft
cross leakage is .18 at gates .1/.9. Neither is a learned empirical result.
Measured CPU was .956371 seconds, wall 1.254945 seconds, peak RSS 290,455,552 bytes,
and output 19,130 bytes, within the finite allocation. There were zero fitting
updates, scientific observation records, numerical failures or numerical retries.
An initial Ruff loop-binding warning was corrected before the sole numerical run.
A bare-Python artifact-read command failed because the pyenv version was absent;
reading with `uv run python` succeeded without rerunning the audit.

Command: `uv run python scripts/check_gated_routing_theory.py --output
docs/analysis/gated_routing_theory_checks.json`. CPU is process time including
imports; wall starts inside main before Torch import. Source/config hashes, Python
and Torch versions, thread count and deterministic settings are in the raw record.

**Proceed to [SOAM-109](../tickets/SOAM-109-gated-assembly-protocol.md) design only.**
The direction and initial analytical foundation are accepted; this is not a frozen
experiment, proof of learned hierarchy, or a resolution of E0/E0-HOLD drift.
The next protocol must resolve a compact modulation rule capable of the
graph-recruitment test, the exact learning pressure, independent versus reciprocal
mask dynamics, discrete
integration and action timing, and a fresh finite experimental contract. These are
scientific design tasks, not an additional human approval ceremony.


## 9. Owner clarification: multiple-entry graphs and possible dormancy

Later November 23, the owner generalized the routing structure to graphs and named
the second field the **modulation network**. Several populations may admit the
same broadly distributed observation. Their evolving activity may recruit
modulation that inhibits or disinhibits other populations; pre-existing connections
then become influential, allowing further recruitment. Branching, merging, shared
recipients and loops are permitted. Multiple entries alone could still form a
forest; no acyclicity, unique parent or single root is required. The initial tree
wording is superseded as a topology constraint, while causal sequential recruitment
and learned organization remain the question. No new empirical branch is activated.

Separate three graphs: persistent potential connections W (and modulation
connections V), the state-dependent effective connections W_ij*C_ij(g), and the
causal recruitment relationships established by interventions. Effective gating
changes influence without writing or adding persistent connections. Dense sensory
availability does not mean every population is strongly active or receptive.
A population-level graph is an analysis of neuron dynamics, not a supplied routing
registry. Modules and memberships must not be prescribed to make the result appear.

"Dark" has two distinct meanings that the protocol must resolve:

- **Dormant activity:** content activity relaxes toward zero; stored associations
  survive in weights and must be correctly recalled after reactivation. Arbitrary
  episode-specific hidden state need not survive. Gating alone makes no persistent
  writes, but later training can still interfere with old weights.
- **Protected live state:** an ongoing representation remains active internally
  while sensory/external exchange is attenuated. This needs internal support or an
  explicitly supplied hold operation; low receptiveness is not zero activity.

The owner proposes mostly-dark activity as a possibility. The earlier instruction
to preserve every closed population's recurrence is therefore conditional on
retaining live state, not a universal architectural requirement. Preserve dormant
recall and currently needed live information as separate experimental contracts.
Do not add an uncounted latent copy of h behind a zero exported activity.

### Analytical dormant-state alternative (not numerically audited)

A simple source-and-recipient gate becomes relevant again when dormant recall is
the intended contract. Let a=g elementwise h be a derived signal, not a third
stored state; C_ij=g_i*g_j including the diagonal. For a fixed observation:

```text
u_i = g_i * [(W*a)_i + s_i + b_i]
tau_h * dh_i/dk = tanh(u_i) - h_i
```

At a clamped g_i=0, h_i decays exponentially to zero. Connections between active
units can transmit; low-gate units emit and receive weakly. This implements an
active subgraph, not separate isolation among all simultaneously active groups.
That selectivity still depends on learned W and modulation. Receiver gating alone
also does not instantly stop a previously active source from transmitting.

For symmetric W,V, retain the section 4 Phi/Psi and use

```text
E_dark = sum Phi(h_i) + sum Psi(g_i)
         - .5*a^T*W*a - sum_i g_i*(s_i+b_i)*h_i
         - .5*g^T*V*g - r^T*g

v_i = (V*g)_i + r_i + h_i*[(W*a)_i + s_i + b_i]
tau_g * dg_i/dk = sigmoid(v_i/T) - g_i.
```

The chain rule gives dE_dark/dh_i=atanh(h_i)-u_i and
dE_dark/dg_i=T*logit(g_i)-v_i, so the same continuous monotonicity argument applies
under fixed-input/symmetry assumptions. The content bias is gated here; an ungated
nonzero bias would prevent exact dark-state decay. This is an analytical extension,
not a selected final mechanism, learned result, or an additional numerical audit.
The existing ten-check artifact covers the earlier compatibility-gate equations
only and remains unchanged. A future numerical check requires its own declaration.

The minimal E_dark gate feedback above is proportional to the recipient's h_i.
At h_i=0 it cannot directly detect another unit's content through that term;
recruitment initially relies on r and V*g. To express active-content recruitment
of a dormant recipient explicitly, one analytical option adds a learned cross
matrix L (L_ij sends content j to modulation i) through a scalar interaction:

```text
E_recruit = E_dark - g^T*L*a

u_i = g_i * [(W*a)_i + s_i + b_i + (L^T*g)_i]
v_i = (V*g)_i + r_i + (L*a)_i
      + h_i * [(W*a)_i + s_i + b_i + (L^T*g)_i].
```

The new (L*a)_i term can recruit modulation even when the recipient h_i=0. The
g_i*(L^T*g)_i content term and h_i*(L^T*g)_i gate term are required reciprocal
derivatives, not optional feedback decorations. L need not be symmetric: the two
cross derivatives come from the same scalar energy, while W,V retain the stated
symmetry assumptions. Both fields still use the section 4 tanh/sigmoid rate
equations, so the continuous dissipation argument follows by the same chain rule.
At a clamped g_i=0, the content drive still vanishes and h_i decays to zero.

This supplies an explicit mathematical route from active content to downstream
modulation while retaining two state fields. It adds N^2 dense coefficients and
the L/L^T products if implemented densely; no third state, gate controller, or
topology labels are free. Sparsity or factorization of L would be new specified
choices. This unaudited analytical option is not yet the selected pilot: a learned
graph, correct retrieval, default sparsity, and interference protection do not
follow from the energy proof. Static flat selection and ungated extra-state
recurrence remain required competing explanations.

A supplied or learned negative modulation bias could make low gain the default;
its value, sparsity pressure and inference cost must be specified. An entirely
closed system whose modulation receives only silenced content can fail to start.
Direct unmasked input to modulation, as already allowed, provides a possible
recruitment path without hard-assigned entry neurons. Finite sigmoid drives give
soft leakage rather than exact binary silence. Too-strong inhibition can prevent
entry; too-weak inhibition can recruit almost everything. Neither extreme proves
useful sparse organization. Static gain control and flat recurrent selection remain
serious simpler explanations to compare with content-dependent recruitment.

Structural cycles are compatible with a recurrent equilibrium. The strict joint
energy descent proved for constant input rules out nonstationary periodic orbits
in its interior; it does not prohibit cyclic connections or finite transient
recruitment. Sustained traversal requires a different dynamical/forcing contract.
More-dark activity does not establish storage, latency or compute savings unless
those are measured; no capacity multiplication is inferred from a sparse graph.

SOAM-109 must now test causal multi-step recruitment and useful reactivation,
allowing shared recipients and multiple entries, rather than require a learned
tree. Exact activity sparsity, feedback and live-state retention choices remain
open. The algebra, historical outcomes, no-write/sensorimotor boundaries, and fresh
protocol/precision/resource requirements are preserved.

The later SOAM-109 self-consistency review clarifies that dormant reactivation is
required only for a selected dormant variant; otherwise the memory endpoint follows
the declared live-state/recall task. A stationary mechanism pilot can leave action
prediction untested. The allowed graph family is not a demand to exhibit every
motif in one pilot. A supported feasibility revise/stop can finish the decision
without fabricating an empirical protocol. These clarify the design contract and
change none of the numerical equations or earlier audit results.
