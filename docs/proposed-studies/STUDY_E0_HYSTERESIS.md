# State hysteresis for stable navigable memory

**Historical retention proposal, unrun and currently unselected.** The owner has
selected [Assembly organization and selective routing](STUDY_ASSEMBLY_ORGANIZATION.md)
under [SOAM-103](../../tickets/SOAM-103-assembly-organization-plan.md). That plan
includes learned organization from the outset and dense input without prescribed
entry neurons. Hysteresis remains an optional mechanism; this narrower E0-HYS
proposal and its numerical protocol are preserved and are not prerequisites.

November 22, 2026 · [SOAM-102](../../tickets/SOAM-102-state-hysteresis-protocol.md)
· [Experiment protocol](../STUDY_E0_HYSTERESIS_PROTOCOL.md)

The proposed mechanism gives neurons different degrees of resistance to changing
their current state. A shared recurrent population could learn to use some units
for responsive processing and others for persistent information. The immediate
question is whether that improves retention while preserving action navigation
and correction. The broader hypothesis is that learned connections among such
units could support selective access to overlapping memory assemblies.

## What motivates the experiment

[E0-HOLD](../../reports/STUDY_E0_HOLD.md) reduced NAV32's mean stationary orientation
error from 12.33° to 5.70° after 128 steps. The remaining error was precisely above
the five-degree target, and recovery noninferiority remained unresolved. Its
declared joint fix therefore failed. Longer stationary training helped, but the
experiment did not establish the cause of the remaining drift.

This is drift of the **decoded orientation with frozen parameters**, not turnover
of a biological memory code across days. The model already represents one object
through a continuous family of orientations. Keeping the same assembly selected
would not, by itself, stop orientation from drifting within that assembly.

## Excitability and persistence are different controls

Excitability affects how readily a neuron responds. A high activation threshold
does not guarantee a selective response or persistent memory: it can simply make
the neuron difficult to recruit. Hysteresis makes response depend on the previous
state, allowing different conditions for changing a state and retaining it.

Classical Hopfield networks already provide collective persistence through
recurrent attractors. Explicit local hysteresis is an additional controllable
mechanism, not a capability universally absent from Hopfield networks.
[Hopfield's original model](https://www.dna.caltech.edu/courses/cs191/paperscs191/Hopfield82.pdf)
and [recurrent bistability experiments](https://pmc.ncbi.nlm.nih.gov/articles/PMC3270576/)
motivate that distinction.

Excitability has biological precedents in memory allocation and linking:
[Cai and colleagues](https://www.nature.com/articles/nature17955) manipulated
excitability and ensemble overlap in a contextual-memory study. That supports a
role in organizing which neurons participate in memories; it does not demonstrate
the proposed router/leaf mechanism or validate this computational intervention.

## A concrete first mechanism

E0-HYS uses a simple stateful **play operator**, a standard mathematical hysteresis
element. Each neuron receives the recurrent model's proposed next value. If that
proposal lies inside a narrow band around its current value, it stays where it is.
Outside the band, it moves toward the proposal, retaining the specified offset.
The previous neural state itself supplies the operator's memory; no external
memory bank or additional recurrent state is introduced.

Compare the same band width for every neuron with a distribution containing equal
numbers of narrower and wider bands. The assignment is fixed randomly before
training. Recurrent weights can adapt to it, but no units receive object labels,
router/leaf labels, assembly boundaries or a tree. This tests learning **with
supplied heterogeneity**, not learning the heterogeneity itself.

The owner explicitly selected fixed thresholds for this first mechanism test.
Neurons therefore do not learn which threshold to take. Prediction errors train
their incoming/outgoing connections, initializer and readout: using a persistent
unit to carry information that helps later predictions can reduce the training
loss, while retaining information that should change can increase it. There is no
explicit reward for becoming a router or leaf. Whether useful specialization
results, or some units merely become unused, is an empirical question. Learning
threshold values would be a separate intervention with its own fixed-threshold
and learned-timescale controls.

The [play-operator literature](https://doi.org/10.1109/TAC.2013.2281859) supplies a
precise local mechanism. Its use here is a proposed SOAM intervention, not a claim
that this operator is a new invention or a detailed model of neuronal physiology.

## The first experiment

Keep 32 recurrent units, twelve sensory features, twelve mask indicators, one
action input and the original fixed sensory projection. Larger populations, sparse
input fan-out and encoders are held for separate questions. All learned families
receive the same observations and the longer stationary training recipe.

| Comparison | Reason |
| --- | --- |
| Existing NAV32 | Measure improvement against the current mechanism |
| Uniform slower updates | Detect apparent retention caused by sluggish dynamics |
| Different ordinary update speeds across neurons | Separate hysteresis from heterogeneous time constants |
| Uniform hysteresis | Test the persistence mechanism without heterogeneity |
| Heterogeneous hysteresis | Test the owner's proposed distribution of persistence |
| Symmetric action connections with heterogeneous hysteresis | Retain the directional-connection control |
| GRU32 and fitted PCA2 estimator | Keep conventional recurrence and the strongest existing accuracy reference |

The primary comparison is heterogeneous hysteresis against a conventional NAV-family
reference selected using development data only. Require at least a one-degree
reduction in stationary error and final error at most five degrees, together with
all navigation and recovery guards. A separate comparison asks whether varied band
widths outperform uniform band widths. Every mandatory reference is reported;
winning that narrow contrast does not establish superiority over PCA2 or GRU32.

The protocol reserves twenty independent confirmation roots, finite tuning grids
and an exact repeat. Its numerical contract includes small actions, reversals,
movement after a long hold, repeated stationary observations, and perturbations
both inside and outside likely deadbands. A supplied zero-action state freeze is
an evaluation control: excellent holding with no recovery must not pass.

## What could go wrong

A deadband may hold an incorrect state, suppress small actions, delay a reversal,
or reduce the resolution of represented orientations. A slowly changing input can
become pinned until sufficient drive accumulates. Related pinning problems occur
in particular continuous-attractor models, although their mechanism differs from
this intervention. [Burak and Fiete](https://doi.org/10.1371/journal.pcbi.1000291)
motivate testing low-velocity response explicitly.

Training may compensate for the deadband by amplifying action drive or changing
the hidden representation. That is part of the tested learned system, so the
evaluation includes action magnitudes absent from training and records state and
weight statistics. The method may also fail to train under the bounded recipe;
that would concern this implementation and budget, not every possible hysteretic
network.

## Connectivity and the missing hierarchy mechanism

The owner's subsequent clarification emphasizes **who receives input from whom**:
some units receive strong external drive, others receive most of their relevant
drive through those units, and further assemblies receive selectively through the
intermediate ones. That is a claim about connectivity and effective influence.
Hysteresis specifies a local dependence on retained state; it supplies neither
these paths nor a learning rule that organizes them. E0-HYS is therefore a
retention experiment, not a theoretical derivation of emergent routing.

A useful local description of a recurrent system is

`d h[t+1] = J[t] d h[t] + B[t] d x[t]`,

where J is the derivative of the update with respect to current neural state and
B is its derivative with respect to external evidence. These are infinitesimal
influences in fixed coordinates, not information measured in bits. Along a fixed
trajectory, an input perturbation propagates through B, then J[t+1] B, then
J[t+2] J[t+1] B. This distinguishes direct sensory access from influence mediated
by successive neural populations. Finite interventions are also necessary when
threshold crossings change the active paths.

For E0-HYS, B is zero during blindfolded prediction; input influence occurs through
initialization and sensory correction at cue events. Those maps are currently dense.

For the proposed E0-HYS prediction rule, away from switching boundaries, define
M=diag(m_i), where m_i=1 when the play operator follows its proposal and m_i=0
when it retains h_i. Let G=diag(1-tanh(u_i)^2), where u is the recurrent preactivation,
and A=S+(a/.12)K. Direct differentiation gives

`J = (I-M) + M[(1-alpha)I + alpha G A]`, with alpha=.5.

For different neurons i and j, `J_ij = m_i * alpha * G_ii * A_ij`.
Thus a large connection can have little local effect if the receiver is saturated
or remains inside its deadband. The holding neuron still sends its stored value
to other neurons; holding blocks changes to its own value, not its outgoing
connections. The local derivative at a switching boundary is insufficient, and
finite perturbations can open a previously closed path.

Stronger weights may increase causal influence under fixed operating conditions,
but do not by themselves establish greater task-relevant information transfer.
Redundant signals, saturation, noise and competing recurrent paths matter. A
[neocortical-network simulation study](https://pmc.ncbi.nlm.nih.gov/articles/PMC2997390/)
provides one model-specific example in which stronger internal coupling eventually
reduces transmission of external information. Root-like units need not contain
more information than leaves: they might carry a coarse selection signal while
other pathways carry fine detail. If every detail must cross a small root
bottleneck, later units cannot recover information already discarded there.

There are two concrete limitations in the current design:

- At zero action A=S is symmetric. It can represent an undirected tree-shaped
  connection graph, and unequal operating gains can produce unequal effective
  influence. Symmetry does not, however, supply an independently learned one-way
  root-to-leaf connection hierarchy. Action-dependent skew coupling vanishes at rest.
- The learned initializer and correction matrices can directly drive every unit.
  No sensory-access budget makes downstream units depend on an intermediate route.
  Dense connections and the current single-orientation loss need not favor a
  hierarchical solution over a flat one.

Heterogeneous hysteresis is compatible with independent units, a flat recurrent
network, clusters or a hierarchy. For example, removing all inter-neuron connections
leaves the local hysteresis intact and removes any mediated route. A tree therefore
does not follow from threshold heterogeneity alone. No claim is made that the
current prediction objective proves or preferentially learns a tree.

Before an emergence experiment, a mathematical design must specify the sensory
access constraints, allowable directed/reciprocal connectivity, competition or
wiring cost, learning objective/rule, and an operational definition of selective
branching. One candidate hypothesis is that limited sensory fan-out plus competitive
connection learning makes input-mediated pathways useful, while recurrent support
and hysteresis stabilize selected assemblies. This is not yet a selected mechanism
or a sufficiency theorem. Hard-coding layers would demonstrate a supplied topology;
any claim of emergence must identify the structure left for learning to discover.

**Subsequent scope clarification:** limited sensory fan-out is one possible scaffold,
not a mathematical requirement. The selected [AO-1 plan](STUDY_ASSEMBLY_ORGANIZATION.md)
instead tests learned effective routing with dense fixed sensory access. It leaves
the connectivity/learning rule for explicit design and does not infer hierarchy
from a low-rank input projection or the hysteresis operator.

## How the assembly hypothesis would be tested later

The desired organization separates **selecting a memory** from **moving within
that memory**. Selection could resist distracting cues while orientation remains
responsive to legitimate actions. Learned connectivity would need to make that
separation useful; threshold differences alone do not specify branches.

A conditional follow-up would use multiple related objects, with independently
varying identity, shape, action response and pose. Include cross-cutting attributes
so that one privileged tree is not the only useful solution. For example, objects
could share a shape family while differing in an opening transformation, or share
the transformation across shape families. Keep input width fixed and family labels
evaluator-only; disclose any supplied task structure.

Before claiming learned routing, that follow-up would need to show:

- Particular assemblies influence access to a selective subset of other memories,
  beyond simply responding frequently or having large readout weights.
- Lesions of a candidate broad assembly affect several related memories, while
  lesions of a specialized assembly have a narrower effect. Compare equal-size,
  activity- and influence-matched random lesions and direct readout lesions.
- Disrupting communication between the proposed assemblies impairs selection;
  directly cueing the destination still permits recall. This distinguishes a route
  from destruction of the stored representation or decoder.
- The organization predicts behavior on withheld combinations and resists
  distractors while preserving movement within the selected memory.

Assemblies and analysis thresholds must be identified on development data and
tested on fresh streams. A flat recurrent network, a supplied modular/tree control
and ordinary recurrence would be mandatory alternatives. A dendrogram can always
be drawn; it is not causal evidence of a tree. Overlapping routing is an allowed
outcome, and dense recurrent updates do not become logarithmic retrieval merely
because their activity appears hierarchical.

This later design is conditional. E0-HYS can support a useful retention mechanism
without finding hierarchy, or reject the tested mechanism while leaving other
assembly-based approaches open. Its outcome should determine the next fork.
