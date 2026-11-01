# SOAM Architecture Baseline

**User:** Anonymous  
**Created:** 10/30/2026 23:59:40  
**Updated:** 10/31/2026 23:01:46  
**Exported:** 10/31/2026 23:47:13  
**Link:** [https://chatgpt.com/g/g-p-692551df89a081919fa575964c0c92ec-cortical-column-ai/c/6ae575bb-68dc-83ea-926a-567e123f2d68](https://chatgpt.com/g/g-p-692551df89a081919fa575964c0c92ec-cortical-column-ai/c/6ae575bb-68dc-83ea-926a-567e123f2d68)  

## Prompt:
10/30/2026, 11:59:48 PM

Starting a new focused thread for this

SOAM — Focused Architecture Context Splice

Self-Organizing Attractor Memory | October 2026

1. Current Research Direction

We are developing a theory of Self-Organizing Attractor Memory (SOAM) as a distributed, associative, predictive memory system inspired by cortical attractor dynamics.

The central hypothesis is that many cognitive functions—memory, recognition, prediction, continuous sensorimotor navigation, discrete transitions, compositionality, and attention—may emerge from a relatively small collection of shared attractor computational primitives.

The latest direction is more specific:

Memory patterns are not passive representations. They are stateful, functional circuits that can receive sensory and action inputs, continuously update their internal states, predict observations and actions, and associatively excite other functional circuits.

Multiple circuits can remain active at different strengths simultaneously. Some are being actively attended to, others are tracking sensorimotor state in anticipation of becoming relevant, and many others are only weakly primed.

Attention controls which representation becomes the dominant interpretive and potentially action-controlling circuit.

The architecture is intended to support recursive composition and smooth transitions between representations without repeatedly reconstructing entire object models.

This is a research hypothesis, not an established neuroscience model.

2. Fundamental Unit: The Predictive Attractor Circuit

A memory pattern is conceptualized as a reusable, stateful dynamical circuit.

It has several possible capabilities:

* Associative activation: A partial cue can activate or complete the pattern.
* Internal state: Maintains a locally continuous or discrete representation, such as orientation, position, viewpoint, or behavioral context.
* Sensorimotor integration: Incorporates sensory features and actions to update its state.
* Prediction: Predicts subsequent sensory embeddings or observations.
* Action proposals: May generate or evaluate candidate actions, depending on the circuit’s function.
* Associative output: Partially excites other related patterns, including constituents, successors, alternative interpretations, and more abstract concepts.
* Attention modulation: Can be weakly primed, actively tracking, or dominant.
* Learning: Can potentially update its internal representation and its relationships with other circuits.

Conceptually:

Inputs:
    Current sensory features
    Executed actions
    Contextual associative excitation
    Attention / control signals
Predictive circuit:
    Update internal state
    Calibrate against sensory evidence
    Predict subsequent features
    Optionally propose actions
    Generate associative excitation for related circuits
Outputs:
    Updated internal state
    Predicted sensory features
    Optional proposed actions
    Prediction error / confidence
    Cues to other memory patterns

The exact structure is not yet fixed. A circuit could correspond to an object, part of an object, viewpoint, spatial region, behavior, relationship, or abstract concept.

Importantly, one circuit need not reconstruct or represent the entirety of an object. It may encode only the locally relevant view or dynamical state, while associations to other patterns provide access to additional information.

3. Graded Activation and Simultaneous Hypotheses

A major principle is that activating one memory pattern causes partial activation of related patterns.

These partially activated patterns are not necessarily dormant pointers. Some may already be operating as predictive circuits, continuously updating their state from incoming sensorimotor evidence.

We currently distinguish three functional levels:

Primed: A pattern receives weak associative excitation and becomes a potential future state.

Tracking: A candidate pattern has enough activation to maintain and calibrate its own continuous state using sensorimotor evidence.

Attended: A pattern is selected as the dominant interpretive and potentially action-controlling circuit.

These levels may be continuous rather than strict categories.

Multiple hypotheses may track simultaneously, while only a limited number receive detailed processing and one may dominate the current focus.

The system therefore maintains a distributed field of active, partially active, and potentially transitioning representations.

The hypothesis is that this allows memory to prepare useful successor states before they’re needed.

4. Dual Attention: Sensory Attention and Memory Attention

This is one of the most recent and important architectural ideas.

SOAM may require two coupled but independently movable attention mechanisms.

Sensory attention

Selects which features, locations, or portions of incoming sensory information receive priority.

For example, looking at a car and then shifting visual attention toward one wheel.

Memory attention

Selects which internal predictive circuit becomes the dominant interpretive model and potentially receives authority to propose or control actions.

For example, switching the dominant memory representation from the car to the wheel.

Their relationship

When sensory and memory attention align, the attended circuit successfully explains the selected sensory evidence.

When they do not align, that mismatch may indicate an ongoing transition, an incorrect hypothesis, an anticipated observation, or the need to learn something new.

The two attention processes can move in either order:

* Bottom-up: Sensory attention changes first; matching memory circuits calibrate, and memory attention follows.
* Top-down: Memory attention primes a predicted object or feature, directing sensory attention to seek confirming evidence.

Neither attention process necessarily requires the other to move immediately.

The central operation is predictive correspondence between selected sensory evidence and selected internal representations.

Dual attention is currently a functional hypothesis; it does not necessarily imply two anatomically separate controllers.

5. Compositionality Through Concurrent Associative Circuits

Our current compositionality hypothesis is different from building hierarchical object models by explicitly assembling complete representations.

A dominant attractor pattern can contain many weak associative cues to other attractor patterns, which may become independently active and calibrated without replacing the dominant pattern.

Consider examining a car.

The active car representation contains partial cues associated with wheels, doors, windows, different views, damage, and other properties.

Those cues excite related circuits.

A wheel circuit might begin tracking its location and orientation relative to the current car-centered sensorimotor reference frame.

Other wheel circuits can simultaneously track different positions.

All of these can coexist with the dominant car representation.

When attention shifts to a particular wheel, its already-calibrated circuit becomes dominant through increased excitation and pattern completion.

The car representation can remain active as contextual memory.

The same mechanism could then transition from the wheel to a tire, tread pattern, or material feature.

This suggests recursive composition through selective associative activation, rather than requiring a fully reconstructed symbolic hierarchy.

Competition versus composition

An important distinction emerged:

* Competing hypotheses propose alternative explanations of the same sensory evidence.
* Compositional hypotheses describe compatible aspects of reality, potentially at different scales.

The car and wheel representations may both be correct simultaneously. Two competing wheel identities for the same observed region might not both be correct.

The computations can look similar because both involve partially activated, calibrated candidate circuits.

An important distinction is the source of associative excitation:

* A primary object hypothesis may be activated strongly by external sensory evidence.
* Its constituent hypotheses may initially be excited by the primary object’s internal associative cues.
* Those constituents may subsequently acquire direct sensory support.

Cue provenance is useful for understanding relationships but is not, by itself, sufficient to determine whether hypotheses compete or compose.

Compatible circuits must also maintain consistent relational predictions.

6. Pre-Calibrated Transitions and Smooth Handover

A key idea is that potential successor circuits begin calibrating before attention switches to them.

Each sufficiently activated candidate receives relevant sensorimotor information and updates its local state.

For example:

1. The car circuit is attended.
2. Cues to several wheel circuits are weakly active.
3. Available sensory evidence and movement update candidate wheel states.
4. Sensory attention shifts toward a wheel.
5. The matching wheel circuit receives stronger excitation and completes its pattern.
6. Memory attention transitions to that circuit.
7. Predictive processing and possibly action control continue using its already-calibrated reference frame.

This avoids having to perform global retrieval and localization from scratch every time attention changes.

It also creates a potential mechanism for seamless transitions between:

* Different views of an object.
* Objects and their constituent parts.
* Neighboring spatial reference frames.
* Alternative perceptual interpretations.
* Abstract and concrete concepts.
* Different behavioral contexts.

However, not every transition is a simple reversible coordinate transformation.

For overlapping representations of the same physical state, transition consistency or conjugacy is desirable: moving before or after switching reference frames should produce equivalent results.

For part–whole transitions or behavioral mode changes, the mapping may be partial, asymmetric, or noninvertible.

Smooth handover primarily means preserving relevant state and predictive continuity, not necessarily generating identical actions.

7. Reusable Patterns and Instance-Specific Context

Another important discussion concerned repeated or visually identical components.

For example, a car has four wheels.

The architecture does not necessarily need four complete copies of a generic wheel model.

The car representation can contain distinguishable contextual cues associated with each wheel’s position, properties, and sensorimotor relationships.

Selective attention amplifies one of those cues and recruits the reusable wheel circuit in the appropriate context.

The selected wheel’s continuous state can be calibrated using the movement or transformation that led attention to that instance.

Additional cues, including language such as “front-left wheel,” might further disambiguate similar instances.

The remaining challenge is ensuring that instance-specific learning—such as discovering one damaged wheel—updates the correct contextual memory without incorrectly modifying generic wheel knowledge or other wheel instances.

Context preservation, selective learning, and interference control remain open problems.

8. Distributed Neural Populations and Attractor Logic

We do not currently assume that every memory pattern occupies the same neural population or that every pattern has a completely separate population.

A plausible architecture involves multiple partially overlapping assemblies, with learned connectivity, excitation, inhibition, and gating controlling interactions.

Some assemblies might encode continuous ring-like or other manifold dynamics. Others might contribute contextual transitions or associative recruitment.

Distinct circuit functions could emerge from tightly coupled subpopulations or shared computational dimensions.

Useful overlap may facilitate associative retrieval and generalization. Excessive overlap can create interference and unwanted mixed states.

The broader hypothesis is that a collection of attractor operations might form a general computational vocabulary:

* Pattern completion
* Associative priming
* Continuous state navigation
* Discrete switching
* Speculative calibration
* Contextual excitation
* Attentional selection
* Compositional recruitment
* Predictive readout
* Associative learning

The goal is to explore whether combinations of these primitives naturally produce cognitive capabilities rather than separately engineering every capability.

9. Relationship to Graph-Based Implementations

We previously explored representing SOAM as an explicit graph of locally continuous dynamical systems.

This remains a possible experimental implementation, but the current conceptual architecture should not be reduced to a conventional graph with one object per node and discrete edges between objects.

A graph approximation would need to reproduce:

* Partial, graded activation.
* Multiple simultaneously operating predictive circuits.
* Content-addressable recruitment beyond explicit neighboring edges.
* Continuous sensorimotor calibration.
* Context-dependent associative excitation.
* Compositional relations and multiple instances.
* Selective attention and predictive control handovers.

An explicit graph could serve as an inspectable computational approximation.

A neural-attractor implementation could potentially unify more of these operations through recurrent dynamics.

Which approach provides the better foundation remains open. The functional architecture should be investigated independently of this implementation choice.

10. What Is Not Currently Central

Earlier discussions introduced additional architecture and learning mechanisms that should not be treated as fixed requirements in the next discussion.

These include:

* Separate context, place, and action-relation attractor modules.
* A mandatory distinction between discrete and continuous neural populations.
* Diffusion or flow matching as the required consolidation mechanism.
* Specific JEPA encoder/decoder designs.
* Long-horizon action experts.
* A fixed object-level graph hierarchy.
* A complete robotic control system.
* Language as a mandatory component.

These may eventually become relevant, but none is required to understand the currently emerging core idea.

Fast associative learning and long-term self-organization remain important ambitions, but their implementations are not resolved.

11. Main Open Architectural Questions

The most relevant unresolved questions are now:

1. Circuit representation: What exactly constitutes a predictive memory circuit, and how are its local continuous states represented and updated?
2. Associative excitation: How does a dominant pattern generate selective, graded cues that recruit other circuits without overwhelming them?
3. Simultaneous computation: How can multiple candidate circuits remain active and calibrated without destructive interference or excessive computational cost?
4. Dual attention: How do sensory attention and memory attention interact, and what determines when one follows the other?
5. Compositional consistency: How do compatible circuits preserve relationships between their local states, especially across part–whole reference frames?
6. Instance-specific learning: How are reusable concepts kept separate from contextual memories of particular instances?
7. Predictive control: How do active circuits generate feature predictions and optional action proposals, and how is actual control authority selected?
8. Learning and self-organization: How can new circuits, associations, and transitions form without destabilizing existing memory?

These should be approached as testable hypotheses, not settled design decisions.

12. Current Central Thesis

SOAM may be understood as a distributed collection of reusable, predictive, sensorimotor dynamical circuits connected through graded associative excitation.

At any moment, one or more circuits provide the dominant interpretation of selected sensory evidence, while related circuits remain partially active, predicting and calibrating potential future states.

Two coupled attention processes—one over sensory information and another over internal representations—coordinate which evidence is examined and which circuit interprets or controls it.

Compositionality may arise when compatible circuits are simultaneously active and relationally constrained. Recognition and ambiguity resolution may arise when competing circuits seek to explain the same observations. Transitions become smooth because candidate circuits can be calibrated before attention commits to them.

The overarching research hypothesis is that memory, perception, attention, prediction, and compositional reasoning may emerge from different configurations of the same underlying associative dynamical principles.

Suggested starting point for the next conversation

Continue developing the architecture from this predictive circuit + graded associative activation + dual attention + pre-calibrated handover formulation.

Focus on how these mechanisms actually interact computationally, particularly how sensory attention and memory attention establish correspondence, how compatible circuits maintain compositional relationships, and how predictive circuits exchange control.

Avoid reintroducing older architectural modules unless a specific problem demands them.

The priority is to develop a coherent, minimal, testable theory of these interacting mechanisms—not to accumulate additional cognitive subsystems merely because analogous subsystems exist in the brain.

## Response:
10/30/2026, 11:59:57 PM · gpt-6-thinking

> **Defining the loop**
>
> I’m treating this as a working baseline, not a request to formalize everything yet. I’ll focus next on the minimal update loop, circuit interfaces, and correspondence between predictions and sensory features across scales.
>
> **Clarifying attention roles**
>
> I’m keeping the shared action stream as the baseline, with circuits differing mainly in sensory routing and computational allocation. I’m separating activation, attention, and motor control, then testing whether attention selects among predicted instances without requiring winner-take-all behavior.
>
> **Defined the loop and clarified attention roles**
>
> 
>
> Worked for 13s

This is our working baseline for SOAM going forward. I'll treat the architecture in this context splice as the current research direction, without reintroducing earlier modules or assumptions unless we discover a specific computational need for them.

I think we've reached an interesting transition in the research: **we have a reasonably coherent functional hypothesis, and now need to establish whether a minimal dynamical system can actually produce the behaviors we're describing.**

The important shift is that we're no longer treating memory as a collection of representations connected by retrieval operations. We're treating memory as a **distributed system of interacting, predictive processes**, where retrieval, attention, navigation, and composition may be different manifestations of the same dynamics.

## Where I'd focus next

I see three tightly coupled problems that would be especially productive to investigate.

1\. **Predictive correspondence.** How does a circuit determine which subset of sensory evidence corresponds to its internal state? How can several circuits simultaneously explain different aspects of the same sensory stream?

2\. **Relational consistency.** How do concurrently active circuits constrain one another? For example, how can a car circuit and four wheel circuits maintain mutually consistent positions while each independently integrates movement?

3\. **Attentional arbitration.** What actually changes when a circuit becomes dominant? Does it receive more computational resources, stronger sensory coupling, greater influence over other circuits, authority over actions, or some combination?

One distinction I would preserve carefully is that **activation, attention, and control authority are not necessarily the same variable**\.

A circuit may be strongly active without being the focus of attention. A circuit may be attended without controlling behavior. And multiple compatible circuits may simultaneously contribute to the current interpretation.

That separation may be essential to making compositionality work.

## My proposed first principle

**Attention should primarily redistribute influence and computational resources among already-operating predictive circuits, rather than necessarily creating or retrieving their states from scratch.**

This is a hypothesis we can test, not an assumption we need to bake into every implementation.

I'd start by defining a single predictive circuit's minimum state, input/output interface, and update rule. Then connect two circuits and determine whether associative priming, independent calibration, relational consistency, and smooth handover can emerge from their interactions.

If those operations work with two circuits, we have a foundation for investigating distributed composition at scale.

**Context capsule\:** SOAM baseline established: graded associative predictive circuits, simultaneous calibration, dual sensory/memory attention, compositional relationships, and pre-calibrated transitions. Next research priority: minimal circuit dynamics, predictive correspondence, relational consistency, and attention arbitration.

## Prompt:
10/31/2026, 12:01:55 AM

One thing I wanted to maybe expand on from this attention beam idea is that within an attention beam there is a belief beam. There's a set of competing hypotheses. So for the external, or I guess extrinsic attention, there would be competing hypothesis for explanations of that sensory input. For the intrinsic attention, there will be multiple tracking and primed cues, multiple yeah, yeah multiple tracking and primed attractor patterns that would be possibly competing for how they fit in the attended patterns. So those might be compositional components or transitional schema

## Response:
10/31/2026, 12:02:02 AM · gpt-6-thinking

> **Modeling belief beams**
>
> I’m distinguishing extrinsic beams that select sensory explanations from intrinsic beams that expand memory-linked candidates. They should exchange evidence asymmetrically, compete within relevant roles, and coexist when relational bindings remain compatible.
>
> **Refining joint inference**
>
> I’m separating two questions: what sensory evidence explains, and what memory-linked relation should guide the next focus. Each beam competes locally, while compatible object parts, transitions, and bindings can remain jointly active.
>
> **Modeled belief beams and refined joint inference**
>
> 
>
> Worked for 16s

I think this is an important refinement. You're proposing that **attention isn't a single selected representation, but a focused region of computation containing multiple competing and compatible hypotheses.**

And critically, this applies to both extrinsic (sensory) attention and intrinsic (memory) attention.

What makes this interesting is that the two belief beams are doing somewhat different kinds of inference.

## 1\. Two attention beams, each containing a belief beam

Illustrative hypotheses and scores, not measured probabilities. The two beams exchange predictive evidence and associative cues.

The extrinsic belief beam asks\:

**"What could explain the sensory information I'm attending to?"**

The intrinsic belief beam asks\:

**"What other patterns could be relevant to the memory pattern I'm attending to, and how do they relate to it?"**

That second question is more powerful than ordinary associative retrieval. It includes hypotheses about the structure of the current representation and possible future attentional states.

## 2\. Competition and composition happen within the belief beams

I would make one important distinction.

Not every candidate in a belief beam should compete for whether it is *true*\.

Consider the intrinsic belief beam associated with a car circuit.

| Candidate | Relationship | Behavior |
|--------|--------|--------|
| Front-left wheel | Constituent | Coexists and tracks |
| Front-right wheel | Constituent | Coexists and tracks |
| Door | Constituent | Coexists and tracks |
| Different view of car | Transitional | Pre-calibrates |
| Alternative car identity | Competing explanation | Competes if mutually exclusive |

The front-left and front-right wheel aren't competitors for existence. But they might compete for **which one receives attention next**\.

That suggests two distinct kinds of competition\:

- **Explanatory competition\:** Which hypotheses can account for the same evidence or occupy the same relational role?
- **Attentional competition\:** Which of several valid, compatible hypotheses should receive greater processing resources or become dominant?

This is potentially very important because otherwise a winner-take-all mechanism would suppress the very compositionality we're trying to produce.

## 3\. An intrinsic hypothesis may be more than an attractor identity

Here's a refinement I'd consider.

The belief beam may need to contain hypotheses of the form\:

$$
h_i=(C_i,R_i,B_i,S_i)
$$

Where\:

- $C_i$\: Candidate attractor circuit.
- $R_i$\: Proposed relationship to the attended circuit (part-of, next-view, alternative-to, etc.).
- $B_i$\: Instance-specific binding, such as front-left wheel.
- $S_i$\: Candidate's current internal dynamical state.

In pseudocode\:

```text
hypothesis = {
    circuit,
    relation_to_focus,
    instance_binding,
    local_state
}
```

That would allow the same generic wheel circuit to participate in multiple relational hypotheses while preserving the identity and position of each wheel.

It also suggests that competing hypotheses may disagree about **relationships**, not just what object is present.

For example, a candidate visual feature might be interpreted as part of the attended object, a separate object behind it, or a reflection. The same sensory evidence could support competing relational interpretations.

## 4\. The beams can iteratively constrain each other

Imagine attending to a car\:

1. The car circuit recruits wheel, door, and other candidate circuits into its intrinsic belief beam.
2. Those circuits begin calibrating using available sensorimotor evidence.
3. Extrinsic sensory attention shifts toward a circular feature.
4. Its sensory belief beam considers wheel, hubcap, shadow, etc.
5. The intrinsically primed wheel circuit provides contextual support to the wheel explanation.
6. The sensory evidence, in turn, strengthens the matching wheel circuit and its proposed relationship to the car.
7. Memory attention can shift to the wheel without destroying the car's contextual representation.

Crucially, this should be bidirectional but not circularly self-confirming: an intrinsic prediction can't count as independent sensory evidence for itself. Actual observed features must still constrain the system.

## 5\. An emerging architectural principle

I think we can express the new idea as follows\:

**An attention beam defines where computational resources are concentrated; a belief beam maintains the set of hypotheses being evaluated within that focus.**

Extrinsic attention concentrates processing on sensory evidence and maintains hypotheses explaining it.

Intrinsic attention concentrates processing on an active memory circuit and maintains hypotheses about related circuits, their relational bindings, and possible transitions.

Both belief beams permit graded activation, simultaneous tracking, and selective competition. The beams influence one another through predictive correspondence.

One subtle but important consequence: the intrinsic belief beam isn't necessarily a list of objects. It may be a **distributed frontier of possible compositional and transitional states**, many of which are already dynamically evolving.

That would make an attended attractor not just a representation of what the system believes, but an entry point into an entire neighborhood of actively maintained possibilities.

I think the next question worth examining is whether these two belief beams actually need different computational mechanisms, or whether **the same recurrent attractor dynamics can perform both forms of inference, with the distinction arising only from where their excitation originates and what their hypotheses are constrained to explain.**

That would bring us closer to the minimal shared computational primitives we're looking for.

**Context capsule\:** SOAM attention beams now contain belief beams. Extrinsic hypotheses explain selected sensory evidence; intrinsic hypotheses represent associated circuits, relational bindings, and candidate transitions. Distinguish explanatory competition from competition for attention; compatible hypotheses can remain active concurrently. The beams interact through predictive correspondence.

## Prompt:
10/31/2026, 12:11:34 AM

This is turning up to be perhaps quite a complicated attractor circuit. I think it's still possible, but shown that each attractor element has to do a lot. But maybe not. Because on the other hand, a Hotfield network can already do a lot of this stuff if you take out the attention and belief beam stuff. You have, you can create associative memories that contain cues to other memories. And you would need to add attention beams, belief beams, and rules about which part of an attractor is convening and which part of an attractor is collaborating. That's a little more speculative. But I don't think that's impossible. The attention beams would be external to the attractor circuits
The sensory motor calibration is also a bit of speculative, but I also think that's definitely something that's possible. Some way that you could basically whatever you are any of the attended or tracking patterns become encapsulated and somehow get aligned with the recent history of sensory motor feedback coming from the robot. So it actually acts as a tracking system so that can transition into that state seamlessly
I feel like I'm repeating myself a bit here from some of the stuff we've already stated, but it's just helping me to just go over it again and again and again and refine it and refine it.

## Response:
10/31/2026, 12:11:41 AM · gpt-6-thinking

> **Structuring the architecture**
>
> I’m separating Hopfield retrieval, local state dynamics, external beams, arbitration, and tracking. Classic Hopfield networks support pattern completion, but simultaneous independent attractors likely require modular or structured extensions.
>
> **Structured the architecture**
>
> 
>
> **Refining attractor dynamics**
>
> I’m checking precise distinctions among multiple-attractor retrieval, continuous attractor networks, hippocampal preplay, and neural tracking filters. The key question is which capabilities belong inside each attractor versus external coordination mechanisms.
>
> **Clarifying functional layers**
>
> I’m distinguishing associative recall from continuous tracking: Hopfield dynamics retrieve stored patterns, while continuous attractors maintain trajectories. External beams can arbitrate hypotheses, route observations, and compare competing predictions without making every memory circuit implement everything.
>
> **Separating runtime responsibilities**
>
> I’m treating repeated refinement as useful: each attractor owns local content and dynamics, while reusable attention beams handle masking, routing, competition, compatibility, calibration, and scheduling across currently active hypotheses.
>
> **Searched 11 websites**
>
> 
>
> Worked for 20s

I think this repetition is actually helping us simplify the architecture. Each time we revisit it, we're separating what an attractor fundamentally needs to do from what the larger system can do *with* attractors.

And your observation that **attention beams should be external to the attractor circuits** is particularly important. It potentially removes a tremendous amount of complexity from each individual circuit.

I'm starting to see a much simpler architecture.

## 1\. The attractor itself might be relatively simple

Consider what we already get from established research\:

- **Hopfield networks\:** Associative retrieval, pattern completion, and content-addressable memory. Modern Hopfield networks can also retrieve weighted combinations of stored patterns, with a mathematical relationship to transformer attention. \[[Hopfield Networks Is All You Need](https://mlanthology.org/iclr/2021/ramsauer2021iclr-hopfield/?utm_source=chatgpt.com); [Hopfield-Fenchel-Young Networks: A Unified Framework for Associative Memory Retrieval](https://www.jmlr.org/papers/v26/24-1961.html?utm_source=chatgpt.com)\]
- **Continuous attractor networks\:** Persistent states, movement along low-dimensional manifolds, path integration, and correction using external sensory cues. \[[Attractor and integrator networks in the brain](https://www.nature.com/articles/s41583-022-00642-0?utm_source=chatgpt.com); [Sensory feedback in a bump attractor model of path integration.](https://pubmed.ncbi.nlm.nih.gov/26754972/?utm_source=chatgpt.com)\]
- **Associative connectivity\:** Learned associations can recruit related representations, although ordinary Hopfield retrieval doesn't automatically provide independently operating successor circuits.

So these are not three entirely new problems we're trying to solve.

The speculative part is whether we can combine them into a reusable memory substrate supporting many simultaneously operating circuits.

## 2\. External attention could organize relatively simple circuits

Here's how I would currently divide the responsibilities.

Conceptual separation of control from distributed memory dynamics. Calibration could be implemented within the circuits, through shared processing, or both.

The attractor circuits would need only a few basic operations\:

1. Activate from partial cues.
2. Maintain and update their internal state.
3. Respond to sensorimotor input when sufficiently activated.
4. Produce predicted features and associative excitation.

Meanwhile, the external attention machinery determines which circuits to activate, which receive additional sensory evidence, and which hypotheses compete or cooperate.

**The attractor itself doesn't necessarily need to know whether it's competing or collaborating.**

That distinction could be expressed in the constraints between active hypotheses: two circuits explaining mutually exclusive identities for the same object compete, while two circuits representing different parts of that object may cooperate.

This could considerably simplify the recurrent dynamics.

## 3\. Sensorimotor calibration may be less speculative than it first appears

There's a direct connection to state estimation.

Suppose a wheel circuit has a state representing its current orientation, position, and viewpoint. As the robot moves, we can predict how that state changes. Incoming sensory evidence then corrects its estimate.

Conceptually\:

$$
\hat{s}_{t+1}^{(i)}=f_i(s_t^{(i)},a_t)
$$

$$
s_{t+1}^{(i)}=\operatorname{Correct}_i(\hat{s}_{t+1}^{(i)},o_{t+1},g_i)
$$

Where $g_i$ controls how strongly the circuit incorporates sensory corrections.

```text
for each active circuit:
    predict next state from executed action

    if sensory evidence is available:
        correct predicted state

    update prediction confidence
```

That's closely related to a Bayesian filter, except we're investigating whether the prediction and correction can be implemented through learned attractor dynamics.

There is substantial precedent for continuous attractors integrating motion and correcting accumulated drift from sensory landmarks. \[[Sensory feedback in a bump attractor model of path integration.](https://pubmed.ncbi.nlm.nih.gov/26754972/?utm_source=chatgpt.com); [Multisensory coding of self-motion and its contribution to navigation](https://www.nature.com/articles/s41583-025-00970-x?utm_source=chatgpt.com)\]

The important additional SOAM hypothesis is **speculative calibration of candidate circuits that are not currently attended**\.

That creates some genuine challenges. A candidate must know which observation corresponds to its representation and how to map shared movement into its own reference frame. Recent sensorimotor history may help, but it cannot uniquely localize every candidate if observations are ambiguous or insufficient.

Still, we don't need to solve that problem for every conceivable circuit immediately.

## 4\. There's a much smaller experiment hiding here

I'd actually be inclined to temporarily remove belief beams, composition, and most of the attention architecture.

Start with just two attractor circuits representing overlapping views of the same simulated object.

The first is attended. The second is associatively activated and begins tracking the same sensorimotor stream in its own reference frame.

After several movements, switch attention.

Measure whether the second circuit correctly predicts the object's current state **without needing a new global retrieval and localization operation**\.

Compare that against a version where the second circuit remains dormant until the attention switch.

If the pre-calibrated circuit achieves lower transition error or latency, we have evidence for one of SOAM's most distinctive hypotheses.

Then we can investigate competing and compositional hypotheses without changing the fundamental mechanism.

## 5\. An important simplification

There's another consequence of your observation that I particularly like.

The memory patterns might not require dedicated, permanently instantiated computational circuits.

Instead, associative memory could store learned circuit parameters or patterns, while a limited number of active dynamical instances are allocated to represent whichever hypotheses currently matter.

A primed hypothesis might just require a small activation score. A tracking hypothesis requires a dynamic state. An attended hypothesis receives greater computational resources and sensory coupling.

This gives us a possible path toward scalability without demanding that millions of memories continuously execute.

And the external attention beams could regulate that allocation.

I would keep that as an implementation possibility rather than a fixed requirement, but it substantially reduces the apparent computational burden.

**The emerging simplification is that SOAM doesn't necessarily need sophisticated attractors. It may need relatively ordinary associative and continuous attractor dynamics, orchestrated by a relatively sophisticated allocation and attention mechanism.**

That doesn't make the overall research problem easy. But it relocates much of the complexity from every individual memory circuit into the interactions between circuits.

And I think that's an important architectural improvement.

**Context capsule\:** SOAM refinement: attention/belief beams are external to memory circuits. Core circuits may combine associative retrieval, local attractor dynamics, sensorimotor state estimation, and associative output. Competition/composition may be relationship-level constraints rather than intrinsic circuit modes. First test: pre-calibrated versus cold-start attentional handover between two overlapping reference frames.

## Prompt:
10/31/2026, 9:37:52 AM

Also as far as geometric object modeling, each attractor pattern only needs to hold enough geometric information to track it for a brief portion, until it transitions to another view, subcomponent, super component, navigation or other object,. Where that dividing line is between what can be contained in a particular pattern vs a neighboring one, is a result of competition

## Response:
10/31/2026, 9:38:05 AM · gpt-6-thinking

> **Modeling transient attractors**
>
> I’m framing each attractor as a local chart with limited geometric memory. Competition determines switching boundaries, while costs for prediction error, complexity, overlap, and switching discourage fragmented or unstable representations.
>
> **Refining competitive charts**
>
> I’m treating validity as a learned region, not a fixed duration. Each attractor tracks only geometry needed for prediction, while competing models negotiate transitions; continuity and specialization prevent collapse or excessive fragmentation.
>
> **Modeled transient attractors and refined competitive charts**
>
> 
>
> **Anchoring the framework**
>
> I’m checking whether this idea aligns with established work on predictive experts and learned partitions. The strongest analogy is adaptive gating: models specialize where their predictions work best, then hand off when another model becomes more reliable.
>
> **Balancing local predictions**
>
> I’m adding an important constraint: competition must compare equivalent predictions. Overlapping experts can negotiate handoffs, while hierarchy and cooperation handle part–whole relationships; otherwise winner-take-all learning may create redundant or fragmented charts.
>
> **Testing the hypothesis**
>
> I’m distinguishing a useful hypothesis from a guaranteed result: adaptive competition may produce task-dependent boundaries, but regularization, reuse, overlap, and switching costs are needed to avoid fragmentation, collapse, or unstable handoffs.
>
> **Anchored the framework, balanced predictions, and tested the hypothesis**
>
> 
>
> **Searched 10 websites**
>
> 
>
> Worked for 1m 15s

I think this is a significant addition to the SOAM hypothesis, because it suggests that **the boundaries between memory patterns could be learned through competition, rather than defined by a predetermined decomposition of the world.**

And that has a particularly interesting consequence\:

**An attractor pattern doesn't need to model an entire object. It only needs enough information to predict and track the object within its own region of sensorimotor experience.**

When another pattern becomes better suited to the current sensory evidence, viewpoint, scale, or activity, attention can transition to it.

This suggests a kind of **self-organizing atlas of local predictive models**\.

## 1\. Each attractor has a domain of predictive validity

Imagine examining a car.

[![Pilihan Perawatan Salon Mobil yang Bikin Mobil Mengkilap - Scuto](https://images.openai.com/static-rsc-4/LJ-B1nd0kAtas8zPKIzCgJwgPswXbmInfGAMJvnPVv6dr0lnf-h0Z9uMN64EfT98xbonOA08_O8o8bjWr9jZ-LnS4kt4T2BLP4ZW8bKRipex9Nlk9sB_vPKCtpCgwakDfEvWe1aw94Ndp-4AHnQwKLALMR7PREws1Bn32O8X6iAenLSVFO5tBNEgfNcFMJm0?purpose=fullsize)](https://scutokelapagading.com/pilihan-perawatan-salon-mobil/)

[![Image](https://images.openai.com/static-rsc-4/sQ8fbOuus7z0cGCg4rmfUl8FxZ5ttABb-XNVIOcaQkK-Cz8Aaoer5ALInPVBMR9OLhb1CadK9drXZqa3_F4zJL5UWzXSxuO44XUgqhlzcahGle_46q3c2EzRerKCvX3Fw0-DBusiAg03ZYYBNYxPU_IwU2nM1jfy40Tq8-BEKeaFXt-izoIbqZfsTQRHlJLo?purpose=fullsize)](https://www.bn.dk/brugte-biler/5414245)

[![Jak zapsat kola do technického průkazu - Portál řidiče](https://images.openai.com/static-rsc-4/Rl_pWMvmRWK-Ql8gq3M5cN3pAIMoI6KJzZXRpjeLkMaIQdN8XWMEdTJt88xOHFUPYJqERF3XORYBA3xR80v8yMs9BK_GxIdpiWlQPlm2x4Y0ejnC0vO4MJEIF7M7yMG0IubqHvCxLyOddPbr6aDISxWxrvi7LMCYhsF8_ZFKrsXqS12_h9pS2OwodXKgvJz6?purpose=fullsize)](https://www.portalridice.cz/clanek/jak-zapsat-jine-kola-do-technickeho-prukazu)

[![KS74XTH CUPRA Formentor CUPRA Formentor VZ2 2.0 TSI DSG-auto 4Drive 333 7-speed automatic in stock at CUPRA Oldham](https://images.openai.com/static-rsc-4/pZmL47aUUjT-25jE1xjgew1LddtYpH5O9y8BeJSjP5d8-apSoY2Ye0ENzj5gFuUTjrajxN0FP8BfbFyS6Zcn8aSqGhkjPyCt_8VKrogvzo72rOm21O2H0LhaV5tMLazlUcVfSEGLaRBx9wZGpWwj7278qeD5x1F-_ABmJWGN-MxcKrVrfyEvX-bv9NOYawix?purpose=fullsize)](https://www.swanswaygarages.com/vehicle-details/cupra-formentor-cupra-formentor-vz2-20-tsi-dsg-auto-4drive-333-7-speed-automatic-ks74xth-1/)

[![Car Body Types Explained | LeaseLoco](https://images.openai.com/static-rsc-4/oZS4cwyrTZKCQu7VdDnKBn7Huukn0b1OEUgsivO_xca0FDZL-cYPC6m1Obh3gczczLKPJvd6vwR01PwMJFhkMyqpKABk93O78C02gEj2pwDf7PPnq_-4vsR2ZNzZQBNtzQNY1TfGOJ2sPgvUNEBXuOe4GP2EUe4eXKH34h3gCN138m_8rsoq87j9w7HlzcHp?purpose=fullsize)](https://www.leaseloco.com/blog/car-body-types)

[![Car tire close up](https://images.openai.com/static-rsc-4/RW34PxQ6KUl7pGjHQCL7SwR1x732MTUomylQm1pDe1nwvr_sAIiLsPIEzRNh4c30FuGEA351BFtGYXXbNAgRdOmZgLepGF-IduLJErIkpzJ_NxDc89EcJUknMQLFQKojZvNrv6IwzJt6s9gIAIIleMYWkXSWZbWUgEs5SRGGG_ysuiM2a4eQYQJ-ZrhRdDDV?purpose=fullsize)](https://media.gettyimages.com/id/518425648/photo/car-tire-close-up.jpg?b=1&c=9HKqn7BBZvPVltLqnwqsga6XEJho9ob-q579BJXaWvE%3D&k=20&s=612x612&w=0)

[![Inventory Photography | OnSite Dealer Solutions](https://images.openai.com/static-rsc-4/7OJB0arpqYFLCU0QPPtO6FkpW-ICzTo1M1mxlp6eeHt4XjBa_aiSmNmhdai1gj4l2kRWHxThBNIsTF2TznACLhddMHtZgDW7OHdsnXtGGXzbJEu1rIEuA_eiy7MmB0Cp6S83WF7_FT2ildR7ClXwyfLay7nvNtXtGB5whQJUsQ2Vaox6ItAFu1INcfaJObZf?purpose=fullsize)](https://onsitedealersolutions.com/custom-dealer-solutions/inventory-photography/)

One attractor might contain sufficient geometry to track the car from a front three-quarter viewpoint. As you move around it, that attractor updates its continuous internal state.

But it doesn't necessarily need to predict the appearance of the entire rear of the car, the underside, or the detailed geometry of its wheels.

Those might be handled by other attractors.

What's interesting is that the boundaries don't necessarily correspond to physical parts or fixed angular intervals.

They might emerge wherever the current attractor becomes less effective at maintaining a coherent predictive state than some alternative.

This is analogous to covering a complicated geometric manifold with overlapping local coordinate charts, except the charts themselves are learned through experience.

## 2\. Competition determines the boundaries

Here's where I think your idea becomes especially interesting.

Suppose two attractors can explain overlapping portions of the same sensorimotor experience.

- Circuit A predicts the car well from frontal viewpoints.
- Circuit B predicts it better from side viewpoints.
- Both can track it reasonably well from a front-quarter viewpoint.

Their competition determines which circuit should dominate in that overlapping region.

The corresponding learning process could gradually specialize their predictive domains.

This has a precedent in Mixture of Experts research. Jacobs, Jordan, Nowlan, and Hinton demonstrated in 1991 that competing expert networks can learn to divide a problem into specialized regions without a predefined partition. \[[Adaptive Mixtures of Local Experts](https://pubmed.ncbi.nlm.nih.gov/31141872/?utm_source=chatgpt.com); [Abstract: Adaptive Mixtures of Local Experts](https://www.cs.utoronto.ca/~hinton/absps/jjnh91.html?utm_source=chatgpt.com)\]

SOAM would extend this idea from static expert selection to **stateful, predictive, associative dynamical circuits**\.

We could formulate attentional selection approximately as\:

$$
S_i=-E_i+\alpha A_i-\lambda T_i
$$

Where\:

- $E_i$\: Prediction error for the evidence circuit $i$ is trying to explain.
- $A_i$\: Associative support for that circuit.
- $T_i$\: Cost of transitioning to it from the current circuit.

```text
For each candidate circuit:
    predict incoming observations
    compare predictions with evidence
    calculate associative support
    estimate transition cost
    calculate selection score

If a competing circuit becomes reliably better:
    transfer dominant attention
    retain relevant tracking states
```

The transition penalty prevents constant switching when two circuits perform similarly.

The key distinction is that this competition occurs between alternative explanations of comparable evidence. A car circuit and wheel circuit can remain jointly active because they explain compatible aspects of the world.

## 3\. The learning rule determines the geometry of memory

One important caveat: competition alone doesn't guarantee useful specialization.

An unconstrained system might learn one gigantic attractor that attempts to model everything. Alternatively, it might fragment experience into thousands of tiny attractors with constant transitions.

We probably need learning pressures favoring\:

- Accurate local predictions.
- Stable continuous tracking within a circuit.
- Limited circuit complexity.
- Reliable transitions between overlapping circuits.
- Reuse of previously learned patterns.

The resulting boundaries could emerge from the balance between predictive accuracy, representational complexity, and transition costs.

And importantly, **the boundaries would exist in sensorimotor state space, not necessarily ordinary three-dimensional space.**

The same geometric viewpoint might belong to different attractors depending on the robot's activity, attention, movement, or contextual interpretation.

## 4\. An object becomes a navigable collection of partial models

This suggests an intriguing alternative to conventional geometric object modeling.

Instead of learning one complete 3D representation of a car, SOAM might learn a collection of overlapping predictive circuits whose relationships allow the robot to explore the car continuously.

At any given moment, only a small subset needs to maintain precise geometry.

The rest of the object's representation can remain latent in associative memory until needed.

There is one important requirement: overlapping circuits must learn consistent state correspondences. Otherwise, attention might transition smoothly in appearance while silently losing track of object identity or position.

That makes pre-calibration especially valuable. Both circuits can briefly track the same physical state before the handover.

## 5\. The deeper implication

I think we may be approaching a more precise description of what self-organization means in SOAM.

It's not merely organizing memories into an associative graph.

**It's learning how to partition experience into locally predictable dynamical regimes, while simultaneously learning the associations and transitions that connect them.**

And those partitions needn't form a strict hierarchy. A circuit's domain might overlap another because of viewpoint, physical composition, temporal sequence, or behavioral context.

We could therefore end up with object-like, part-like, place-like, and activity-like patterns without explicitly imposing those categories beforehand.

Whether this actually emerges is a major experimental question. But it's a substantially more concrete hypothesis than simply expecting attractor networks to develop compositional representations.

**Context capsule\:** SOAM geometric memories may be locally valid predictive models rather than complete objects. Competition and learning determine their domains of validity; overlapping domains allow pre-calibrated transitions. The central challenge is learning useful partitions without excessive fragmentation or monolithic representations.

## Prompt:
10/31/2026, 10:23:18 AM

Here’s another example to think about motor movement transitions, let’s say I’m trying to put pants on my 18mo old daughter, which I just did :p but maybe has applications in care providing robots
The pants go on part way, then they shake the bottom of the pants legs to try to get her feet in. If I were a robot brain, I don’t know which orientation or how much amplitude to shake the pant leg, but there might be some action chunk cue on the current attractor that’s attended to as the current state of the pants around the legs. The shake action transitions to the next point where the pant leg cuff is over the foot.  So some portion of the action cue needs to be stored in the atttactot circuit, and allow that to transition to the next state. The action is also simultaneously the calibration of the next attractor state

## Response:
10/31/2026, 10:23:27 AM · gpt-6-thinking

> **Framing movement transitions**
>
> I’m treating this as a robotics concept involving motor primitives, affordances, belief-state updates, and action-conditioned perception. I’ll connect the transition from shaking fabric to covering a foot with hierarchical control and contact-rich manipulation.
>
> **Refining transition learning**
>
> I’m distinguishing stored action associations from fixed trajectories: the robot retrieves a parameterized policy, probes the cloth-foot relationship, updates its belief, and safely adapts amplitude, orientation, and timing.
>
> **Refined movement transition learning concepts**
>
> 
>
> **Segmenting adaptive skills**
>
> I’m framing the action cue as a retrieval link to a closed-loop skill, while segmentation emerges from controllable effects. I’m tracking competing outcomes and using small exploratory actions to resolve uncertainty.
>
> **Formalizing adaptive transitions**
>
> I’m representing each transition as a cue-linked policy with predicted successors, observations, and stopping conditions. The robot updates competing outcome beliefs after every action, rather than assuming the intended configuration occurred.
>
> **Clarifying calibration**
>
> I’m separating physical progress from belief calibration: the same gentle motion advances the task while revealing tension, contact, or alignment. Segmentation can occur mid-motion when observations show the next controllable state.
>
> **Modeling competing successors**
>
> I’m representing the cuff scenario with competing successor hypotheses: successful placement, heel obstruction, or slippage. Each action advances cloth movement while updating confidence, using tactile evidence, predicted effects, comfort limits, and early stopping.
>
> **Formalized adaptive skill transitions and modeled competing successors**
>
> 
>
> **Unifying action roles**
>
> I’m treating each movement as simultaneously changing the world, gathering evidence, and preparing a successor controller. The next attractor remains conditional until sensory feedback confirms it, preventing premature commitment.
>
> **Unified action roles**
>
> 
>
> **Searched 17 websites**
>
> 
>
> Worked for 1m 49s

That's a really good example, especially because putting pants on a toddler involves deformable objects, uncertain geometry, changing contact points, and another person who may move unpredictably. Yet the movement can be surprisingly intuitive once you've learned it.

I think you've identified something important about SOAM\:

**An action can simultaneously be a means of transitioning between attractors and a means of calibrating the attractor you're transitioning toward.**

And this potentially connects motor skills, active perception, and memory navigation using the same mechanism.

## 1\. The current attractor contains an affordance for reaching the next one

Imagine the currently attended pattern represents\:

*The pant leg is partially around the child's foot, but the cuff hasn't passed over the heel.*

That attractor doesn't necessarily need to represent the entire pair of pants, the child's anatomy, or a complete dressing procedure.

It only needs enough local information to track the current cloth-foot relationship and predict what movements might change it.

Stored within its associative structure could be cues to\:

- A successor attractor: *cuff has passed over the foot*\.
- A motor primitive: *oscillate the pant leg while guiding it upward*\.
- A predicted outcome: *the fabric advances while the foot remains approximately stationary*\.
- Alternative outcomes: *the fabric catches, twists, or slips away*\.

Importantly, the current attractor needn't contain all the details of the motor primitive. It could contain an **associative cue that recruits a learned motor policy**, whose parameters are adjusted using current sensorimotor feedback.

This preserves our goal of keeping individual attractor circuits relatively simple.

## 2\. The action is also a sensorimotor experiment

The shaking motion has three effects at once.

It changes the physical configuration of the pants. It generates new sensory evidence about how the fabric is interacting with the foot. And it helps determine which successor attractor is becoming the correct representation.

For example, the robot might initially be uncertain whether the cuff is catching on the heel or simply needs to be pulled upward. Small oscillations produce tactile and visual feedback that distinguishes those possibilities.

The next attractor can already be partially activated, predicting what successful progress should look and feel like.

But there's an important subtlety: **pre-calibration doesn't mean assuming the transition has succeeded.** The candidate successor is still a hypothesis until sensory evidence supports it.

The current attractor can remain dominant while the successor's predicted state becomes increasingly well constrained.

## 3\. Actions could be learned transitions between predictive circuits

I think we could represent the basic operation as\:

$$
A \xrightarrow{\pi_{AB}} B
$$

Here, $\pi_{AB}$ is a feedback-driven motor policy associated with the transition from attractor $A$ to attractor $B$\.

The policy needn't specify a fixed shake amplitude, direction, or duration. Those could be adapted continuously through feedback.

```text
A = attended attractor
B = primed successor attractor

retrieve motor policy associated with A → B

while B is not sufficiently confirmed:
    choose small movement using sensory feedback
    execute movement
    update A's state
    update B's predicted state and confidence

    if excessive force or unexpected contact:
        interrupt or select recovery

handover attention when B explains the evidence
```

This resembles the *options* framework in hierarchical reinforcement learning, where temporally extended actions have initiation conditions, internal policies, and termination conditions. \[[Between MDPs and semi-MDPs: A framework for temporal abstraction in reinforcement learning](https://www.sciencedirect.com/science/article/pii/S0004370299000521?utm_source=chatgpt.com); [The Option-Critic Architecture \| Proceedings of the AAAI Conference on Artificial Intelligence](https://ojs.aaai.org/index.php/AAAI/article/view/10916?utm_source=chatgpt.com)\]

But in SOAM, the interesting addition is that the destination is a predictive attractor whose state is being prepared and calibrated throughout execution.

The action is not merely an instruction to move from memory A to memory B. It's part of the dynamical process that makes B applicable.

## 4\. This may influence where attractor boundaries form

Your previous observation about competing geometric models becomes even more interesting when we include actions.

Perhaps attractor boundaries are determined not only by **where one pattern stops predicting observations accurately**, but also by **where a different pattern becomes better suited to controlling movement and predicting its consequences**\.

The pants sliding over the foot might be one continuously tracked dynamical regime. Once the cuff clears the heel, another regime takes over, with a different geometry, different affordances, and different useful motor primitives.

We wouldn't necessarily need to predefine these stages. In principle, learning could discover the boundaries from prediction errors, successful actions, and reliable handovers.

This is relevant to actual assistive robotics. Researchers have demonstrated robotic trouser dressing with visual and tactile state estimation and recovery from snagging, while more recent systems combine visual policies with force constraints for safer dressing assistance. \[[Bottom Dressing by a Dual-Arm Robot Using a Clothing State Estimation Based on Dynamic Shape Changes - Kimitoshi Yamazaki, Ryosuke Oya, Kotaro Nagahama, Kei Okada, Masayuki Inaba, 2016](https://journals.sagepub.com/doi/10.5772/61930?utm_source=chatgpt.com); [Force-Constrained Visual Policy: Safe Robot-Assisted Dressing via Multi-Modal Sensing \| IEEE Journals &amp; Magazine](https://ieeexplore.ieee.org/document/10465608/?utm_source=chatgpt.com)\]

## 5\. A possible unifying principle

What I find most interesting here is that we're starting to blur the distinction between perception and action without requiring a completely new subsystem.

An attractor maintains a predictive state. Associated cues recruit possible successors and motor policies. The external attention mechanism selects among them. Executed actions modify the environment and generate the observations needed to calibrate the successor.

**The same predictive transition mechanism could support both moving attention through memory and physically moving the world into a state that another memory pattern can represent.**

That is potentially a powerful unification.

The key question I'd want to explore next is whether the *action policy itself* can be represented as an attractor-like dynamical pattern, or whether it should remain a separate motor primitive recruited by associative cues. We don't need to decide that yet, but it directly affects how broadly we can reuse the SOAM computational primitives.

**Context capsule\:** SOAM action transitions: the attended attractor associates current state with candidate successor circuits and feedback-driven motor primitives. Executed movements both advance physical state and provide evidence for calibrating successors. Attentional handover is based on observed correspondence, not merely action completion. Attractor boundaries may emerge from predictability and controllability together.

## Prompt:
10/31/2026, 12:52:39 PM

So what is the data storage of action transition?

Maybe it’s a complementary attractor network that contains mappings from actions to attractor phase transitions and cues back to actions? I don’t know. Or maybe there’s a sensorimotor beam that detects cues from the current attractor and can execute the corresponding action chunk, or maybe action only happens at transitions, and attractors are passive listeners when not changing. Let’s say you’re doing an action in the current attractor, so the attractor stores the current state of action, and you are calibrating the next state you will transitions to, the current cue and the be attractor state combine  form a mapping to the action, and that determines how the next attractor state will be calibrated for seamless action transition. I don’t know I’m just throwing ideas out there and seeing what sticks

## Response:
10/31/2026, 12:52:46 PM · gpt-6-thinking

I’ll compare the possible places to store action transitions—inside attractors, between them, or in a complementary motor system—and look for a minimal design that preserves the pre-calibrated handover idea.

> **Formulating transition memory**
>
> I’m framing this as a factorized memory: current state, intended target, context, action primitive, and expected sensory outcome bind into one transition. I’ll compare associative, predictive-control, and hybrid-system interpretations, then suggest a compact architecture.
>
> **Formulated transition memory**
>
> 
>
> **Refining transition memory**
>
> I’m treating transitions as reusable relational memories, not extra states: they bind the current attractor, intended successor, context, action primitive, phase, and predicted sensory effects. Feedback can update confidence, execution, and calibration as the transition unfolds.
>
> **Refined transition memory**
>
> 
>
> **Comparing control layouts**
>
> I’m distinguishing three options: embed transition cues in the current attractor, use reusable motor primitives, or represent transitions as relational action policies. The third seems most flexible, while phase dynamics remain inside each executable primitive.
>
> **Specifying the controller**
>
> I’m expressing a transition memory as \(M(A,B,c)\rightarrow(\pi,\beta)\): policy and termination rules conditioned on current state, intended successor, context, observations, and motor phase. I’m also separating execution, prediction, sensory correction, and calibration rather than treating the target as already achieved.
>
> **Binding higher-order cues**
>
> I’m considering a sparse, factorized association binding current-state, target-state, context, and action-primitive patterns. Its payload can include parameters, predicted changes, and success or failure signatures, avoiding a huge lookup tensor.
>
> **Compared layouts, specified the controller, and bound higher-order cues**
>
> 
>
> **Searched 15 websites**
>
> 
>
> Worked for 1m 6s

I think your latest idea is getting at something very important: **the action might not be stored in either the source or destination attractor. It might be stored in the learned relationship between them.**

And I particularly like your suggestion that the current attractor and the partially calibrated successor attractor jointly cue an action. That gives the motor system information about both **where it is now and where it's trying to go**\.

This suggests three distinct things we might want to store\:

1. **State memory\:** What the current attractor represents and how it evolves.
2. **Transition memory\:** Which action or motor skill can take the system from one predictive regime toward another.
3. **Motor memory\:** How that action unfolds over time, including its phase, feedback, and adjustments.

These don't necessarily require three different neural networks. They're three functional roles that we could implement through associative connectivity and recurrent dynamics.

## 1\. The action could live in a relationship between attractors

Suppose\:

- $A$ \= The current attractor, representing the pant leg partially around the foot.
- $B$ \= A candidate successor attractor, representing the cuff clearing the heel.
- $M$ \= A learned motor primitive, such as a gentle oscillatory movement combined with upward motion.

The memory relationship might be\:

```svg
<svg viewBox="0 0 340 209" width="100%" xmlns="http://www.w3.org/2000/svg"><rect x="5" y="9" width="132" height="53" rx="10" stroke="#3986C8" fill="#3986C8" fill-opacity=".12" /><rect x="203" y="9" width="132" height="53" rx="10" stroke="#3986C8" fill="#3986C8" fill-opacity=".12" /><g fill="currentColor" text-anchor="middle"><text x="71" y="31" font-size="12" font-weight="600">Attractor A</text><text x="71" y="46" font-size="10">Current state</text><text x="269" y="31" font-size="12" font-weight="600">Attractor B</text><text x="269" y="46" font-size="10">Target hypothesis</text></g><path d="M137 35 H203" stroke="#0D9488" stroke-width="1.5" stroke-dasharray="4 3" /><g stroke="#B17CDB" stroke-width="1.6" fill="none"><path d="M71 62 V89 L170 115" /><path d="M269 62 V89 L170 115" /></g><rect x="79" y="115" width="182" height="46" rx="10" stroke="#B17CDB" fill="#B17CDB" fill-opacity=".12" /><text x="170" y="134" text-anchor="middle" fill="currentColor" font-size="12" font-weight="600">Associative transition</text><text x="170" y="148" text-anchor="middle" fill="currentColor" font-size="10">Retrieve + parameterize action M</text><path d="M170 161 V177" stroke="#0D9488" stroke-width="1.5" /><path d="M165 172 L170 178 L175 172" stroke="#0D9488" stroke-width="1.5" fill="none" /><text x="170" y="195" font-size="11" text-anchor="middle" fill="currentColor">Feedback-driven motor execution</text></svg>
```

The transition association is conditioned on both attractors, rather than being a fixed action attached only to A.

The associative memory would answer something like\:

*Given the currently active pattern, its local state, this candidate destination, and the present context, which motor behavior is likely to move us toward the destination?*

This differs from storing a fixed instruction such as "shake the pant leg" inside attractor A.

The same current state could lead to different actions depending on the desired successor. And the same motor primitive could be reused for many different transitions.

## 2\. Where would the transition data actually be stored?

I'd provisionally favor a **factorized associative memory** rather than a complete motor controller inside every perceptual attractor.

The source attractor contains cues to possible successors and their associated actions. The transition association stores the conditional relationship between the source, destination, and motor skill. A reusable motor circuit stores the dynamics of the action itself.

That motor circuit could be another attractor network, particularly for rhythmic actions like shaking. But it doesn't have to be. It could initially be an ordinary recurrent controller.

There is already relevant work here: Dynamic movement primitives $DMPs) represent discrete and rhythmic motor behaviors using dynamical systems with attractor properties. The 2013 paper *From Dynamic Movement Primitives to Associative Skill Memories* is especially close to this part of your hypothesis, because it explores learned, reusable motor skills and associative recall. \[[Dynamical movement primitives: learning attractor models for motor behaviors](https://pubmed.ncbi.nlm.nih.gov/23148415/?utm_source=chatgpt.com); [From dynamic movement primitives to associative skill memories](https://www.sciencedirect.com/science/article/pii/S0921889012001716?utm_source=chatgpt.com)\]

A simplified transition memory might look like this\:

Learned transition association

Retrieval key

Current attractor + current local state + candidate successor + desired successor state + context

---

Associative output

Motor primitive cue + initial parameters + expected sensory changes + termination conditions

---

Motor execution state

Current phase, feedback, parameter adjustments, and progress toward the successor

The association could eventually be encoded through distributed connection weights instead of a literal record.

In particular, the current and destination patterns might jointly excite a motor pattern through higher-order or factorized associative connections. That would let a motor skill be selected by a combination of cues rather than either cue independently.

## 3\. The action controller and the successor attractor evolve together

Here's the part of your proposal I find most compelling.

Once the action is selected, it doesn't simply execute and then trigger a memory transition.

**The motor dynamics and the successor's state-estimation dynamics run simultaneously, coupled through actual sensorimotor feedback.**

In the pants example, the action might begin with a small oscillation. The successor circuit predicts how the cuff's position and contact configuration should evolve. Each observation corrects that prediction. The motor controller adjusts its movement based on the discrepancy.

Mathematically, we could start with\:

$$
u_t=\pi_M(x_{A,t},\hat{x}_{B,t},x_B^*,\phi_t,y_t)
$$

Where \(x_A$ is the current circuit state, $\hat{x}_B$ is the successor's estimated current state, $x_B^*$ is the desired state, $\phi$ is the motor primitive's phase, and $y$ is sensory feedback.

The successor's tracking state then updates using the executed movement and resulting observation.

```text
A = attended circuit
B = candidate successor
M = motor skill cued by (A, B, context)

while executing M:
    generate action using A, B, and motor phase
    execute action
    observe consequences

    update A's state
    update B's tracking estimate
    correct motor parameters from feedback

    if B is sufficiently supported:
        permit attentional handover

    if action is unsafe or ineffective:
        stop or select recovery behavior
```

Notice that the successor's desired state is different from its estimated actual state. We don't want the system to confuse *trying to make B true* with evidence that B has already become true.

This also gives us an answer to your question about actions occurring only during transitions.

At a coarse timescale, an action chunk can be treated as a transition. But at a finer timescale, motor control may continue entirely within one attractor's domain. An action can also span several perceptual handovers.

So I wouldn't make action execution dependent on a discrete attentional transition.

## 4\. Do we need a sensorimotor belief beam?

Possibly, although I wouldn't add it as a mandatory third attention system yet.

There is an interesting neuroscience connection: Affordance competition hypothesis, proposed by Paul Cisek, describes multiple potential actions being partially specified in parallel, with competition gradually selecting one for execution. Action specification and selection can continue during movement. \[[Cortical mechanisms of action selection: the affordance competition hypothesis](https://pmc.ncbi.nlm.nih.gov/articles/2440773/?utm_source=chatgpt.com)\]

That's remarkably compatible with your belief beam concept.

We could interpret competing candidate motor skills as an action-oriented extension of the intrinsic belief beam. The currently attended perceptual state, candidate successor states, and sensorimotor feedback all contribute to their relative activation.

One motor skill eventually gains execution authority, but alternatives can remain primed for recovery.

Crucially, **motor execution authority is different from perceptual attention**\. The current attractor might remain attended even while a motor primitive is actively transforming the environment toward a successor.

This doesn't require a new attention beam until we establish that ordinary associative competition and control gating are insufficient.

## 5\. What I would test first

I would test your joint-cue hypothesis directly.

Train a simple simulated system with two partially overlapping attractor states and several reusable motor primitives. Have the action chosen from the combination of the current local state and a candidate destination, not solely from the current attractor.

Then compare a source-only action association against the joint source-destination association.

The main tests would be whether the same source can support different goal-directed actions, whether the same motor skill transfers to different transitions, and whether continuous calibration improves successor-state handover.

If that works, we could investigate storing the motor primitive itself in a complementary attractor network.

I think this avoids prematurely committing to another large subsystem.

## 6\. The emerging principle

What I like most about this direction is that it gives actions two closely related roles\:

**Perceptual transitions\:** Movement changes which predictive representation best explains the world.

**Causal transitions\:** Movement deliberately changes the world so that a desired successor representation becomes applicable.

The same learned transition association could participate in both.

And action itself helps generate the sensory evidence used to decide whether the transition has succeeded.

That suggests a compact hypothesis\:

**SOAM could store sensorimotor skills as conditional, associative transformations between predictive attractor states, with active motor dynamics continuously calibrating both the current and prospective representations.**

The remaining question isn't necessarily whether the motor skill is *another kind of attractor*\. It's whether ordinary associative connectivity can learn the three-way binding between **current state, desired successor, and motor behavior** without requiring a specialized transition representation.

That's the part I would investigate next.

**Context capsule\:** Proposed SOAM action memory is factorized: perceptual attractors store local state and associative cues; transition associations bind source, destination, context, and motor skills; reusable motor dynamics maintain action phase and feedback control. Actions and successor-state calibration evolve concurrently. Motor authority and perceptual attention remain distinct. Joint source-destination action retrieval is the next hypothesis to test.

## Prompt:
10/31/2026, 10:54:55 PM

Ok so we associate a current state and the next state combination with an action, but that’s a lot of possibilities, how do we reuse skills?

Let’s say the action memory is also an attractor content addressable memory, so that similar but unfamiliar state transitions should trigger the same action attractor? There might be some caveats with that but

## Response:
10/31/2026, 10:55:02 PM · gpt-6-thinking

I’ll look at how an action attractor could generalize across unfamiliar transitions, especially what should be stored as reusable skill dynamics versus what must be calibrated for each situation.

> **Framing reusable skills**
>
> I’m treating this as a robotics design idea: map state transitions and affordances to reusable attractor policies, while preserving equivariance and adding parameters for context, contact, and goal variation.
>
> **Framed reusable skills**
>
> 
>
> **Refining the memory**
>
> I’m separating transition similarity from action validity: the same displacement can require different skills. Retrieval should combine relational cues, affordances, preconditions, predicted success, and risk, then adapt a stable motor policy.
>
> **Refined the memory**
>
> 
>
> **Searched 11 websites**
>
> 
>
> Worked for 43s

Yes. I think a **content-addressable action attractor network** is a promising way to solve the combinatorial problem, and it fits naturally with the rest of SOAM.

The crucial insight is that **we shouldn't need to memorize a different action for every pair of attractor states. We should learn reusable attractors representing families of sensorimotor transformations.**

So even if the system has never encountered a particular state transition, a sufficiently similar *kind of transition* could activate a previously learned motor skill.

That gives us three forms of generalization\:

- **Perceptual generalization\:** Different observations activate the same object or state representation.
- **Transition generalization\:** Different source-destination pairs activate the same transformation or motor skill.
- **Motor generalization\:** The retrieved skill adapts its trajectory, force, amplitude, and timing to the current situation.

That third point is important. We want an action attractor to retrieve a *dynamical behavior*, not necessarily an exact recorded sequence of motor commands.

## 1\. The action memory becomes another associative network

```svg
<svg viewBox="0 0 340 265" width="100%" xmlns="http://www.w3.org/2000/svg"><g fill="currentColor" text-anchor="middle" font-size="11"><text x="76" y="16" font-weight="600">Current attractor</text><text x="264" y="16" font-weight="600">Successor attractor</text></g><rect x="8" y="25" width="136" height="44" rx="8" fill="#3986C8" fill-opacity=".12" stroke="#3986C8" /><rect x="196" y="25" width="136" height="44" rx="8" fill="#3986C8" fill-opacity=".12" stroke="#3986C8" /><text x="76" y="44" text-anchor="middle" fill="currentColor" font-size="11">State A</text><text x="76" y="58" text-anchor="middle" fill="currentColor" font-size="10" opacity=".7">Cloth partly stuck</text><text x="264" y="44" text-anchor="middle" fill="currentColor" font-size="11">State B</text><text x="264" y="58" text-anchor="middle" fill="currentColor" font-size="10" opacity=".7">Cloth moves freely</text><g fill="none" stroke="#7B8F9A" stroke-width="1.4"><path d="M76 69 V91 L170 110" /><path d="M264 69 V91 L170 110" /></g><rect x="75" y="109" width="190" height="39" rx="9" fill="#0D9488" fill-opacity=".12" stroke="#0D9488" /><text x="170" y="124" text-anchor="middle" fill="currentColor" font-size="11" font-weight="600">Transition representation</text><text x="170" y="138" text-anchor="middle" fill="currentColor" font-size="10">Relative change + constraints</text><path d="M170 148 V165" stroke="#0D9488" stroke-width="1.5" /><rect x="29" y="165" width="282" height="88" rx="11" stroke="#B080DE" fill="#B080DE" fill-opacity=".06" /><text x="170" y="182" text-anchor="middle" fill="currentColor" font-size="11" font-weight="600">Content-addressable action memory</text><g font-size="10" text-anchor="middle" fill="currentColor"><rect x="40" y="193" width="79" height="45" rx="8" fill="#B080DE" fill-opacity=".10" stroke="#B080DE" stroke-opacity=".4" /><text x="79.5" y="211">Pull</text><text x="79.5" y="225">attractor</text><rect x="130" y="193" width="80" height="45" rx="8" fill="#B080DE" fill-opacity=".24" stroke="#B080DE" /><text x="170" y="211" font-weight="600">Oscillate</text><text x="170" y="225">attractor</text><rect x="221" y="193" width="79" height="45" rx="8" fill="#B080DE" fill-opacity=".10" stroke="#B080DE" stroke-opacity=".4" /><text x="260.5" y="211">Rotate</text><text x="260.5" y="225">attractor</text></g></svg>
```

Several action patterns can be partially activated by the transition cue; the strongest valid candidate can be recruited and parameterized.

This is similar in spirit to existing work on [Associative Skill Memories](https://www.sciencedirect.com/science/article/pii/S0921889012001716?utm_source=chatgpt.com) and dynamical movement primitives, where reusable motor behaviors are represented as dynamical systems and associated with sensory context. \[[From dynamic movement primitives to associative skill memories](https://www.sciencedirect.com/science/article/pii/S0921889012001716?utm_source=chatgpt.com); [Towards Associative Skill Memories](https://is.mpg.de/am/publications/pastor_towards_2012?utm_source=chatgpt.com)\]

But we're proposing a potentially tighter coupling: the action memory itself participates in graded associative activation, while both the current and successor perceptual attractors continue tracking.

## 2\. The trick is encoding the transition, not memorizing the pair

Suppose the robot learns to oscillate a pant leg to help it slide over a foot. Later, it encounters a sleeve caught around an arm.

Those are different perceptual attractors, but they may have a similar underlying transition\:

*Flexible material is constrained around an object → controlled oscillation reduces resistance → material advances.*

That suggests constructing a transition representation\:

$$
z_\Delta = g(s_A,s_B^*,c)
$$

Where\:

- $s_A$\: Current perceptual state.
- $s_B^*$\: Desired successor state.
- $c$\: Relevant context, including contact geometry and constraints.
- $z_\Delta$\: Learned representation of the desired transformation.

The important point is that $g$ should learn features relevant to the action, rather than simply subtracting two arbitrary latent vectors.

Then the action memory retrieves a suitable skill\:

$$
k^*=\arg\max_k\left[
\operatorname{sim}(z_\Delta,m_k)
+\beta P_k
-\lambda R_k
\right]
$$

Here, $m_k$ is an action attractor's retrieval pattern, $P_k$ its predicted probability of success in the current context, and $R_k$ its estimated risk or constraint violation.

```text
transition = encode(current, desired, context)

candidates = action_memory.retrieve(transition)

for each candidate:
    predict likelihood of success
    check applicability and constraints

activate best valid action attractor
adapt its parameters through feedback
```

The action attractor could therefore have a broad basin of attraction covering many unfamiliar but functionally related transitions.

## 3\. An action attractor could encode an entire family of movements

Consider the action attractor for oscillation.

Its central recurrent dynamics might encode the general behavior, while continuous state dimensions parameterize it.

**Reusable oscillation skill**

One dynamical pattern, continuously adjustable

(Illustrative)

Amplitude  %

> **Slider**
>
> Current value unavailable.
>
> **Range:** 0.1 to 1
>
> **Step:** 0.05

Frequency  %

> **Slider**
>
> Current value unavailable.
>
> **Range:** 0.1 to 1
>
> **Step:** 0.05

Forward progression  %

> **Slider**
>
> Current value unavailable.
>
> **Range:** 0 to 1
>
> **Step:** 0.05

A toy trajectory illustrating parameterized skill reuse, not a physical controller. The same oscillatory dynamics can produce many movements.

An oscillation is particularly interesting because it could be represented by a limit-cycle attractor rather than a fixed-point attractor. That's already well studied in dynamical motor control. \[[Dynamical movement primitives: learning attractor models for motor behaviors](https://pubmed.ncbi.nlm.nih.gov/23148415/?utm_source=chatgpt.com); [Learning an Autonomous Dynamic System to Encode Periodic Human Motion Skills.](https://pubmed.ncbi.nlm.nih.gov/38743538/?utm_source=chatgpt.com)\]

So motor memory might naturally contain dynamical attractors of different kinds: stable postures, rhythmic movements, trajectories, and feedback-driven behaviors.

This would let SOAM reuse more of the same mathematical machinery.

## 4\. The biggest caveat: similarity is not the same as interchangeability

I see three challenges.

**First, the attractor basins must represent functional similarity.** Two state transitions might look geometrically similar but require very different motor actions because of friction, stiffness, contact forces, or the fragility of the manipulated object.

**Second, the motor skill needs contextual parameters.** Oscillating a towel and manipulating clothing around a child's foot may involve related dynamics but very different permissible forces. A retrieved skill should not execute until its applicability and safety constraints are satisfied.

**Third, the action memory needs bidirectional prediction.** A transition cue should retrieve candidate skills, but activating a skill should also predict the sensory consequences and candidate successor states. That gives the system a way to evaluate whether the retrieved skill is appropriate before and during execution.

A paper on transferring robotic tool-use skills specifically addresses why movement generalization alone is insufficient without accounting for task and environmental constraints. \[[A Dynamic Movement Primitives-Based Tool Use Skill Learning and Transfer Framework for Robot Manipulation](https://livrepository.liverpool.ac.uk/3190099/?utm_source=chatgpt.com)\]

## 5\. There's a potentially elegant unification here

Consider where we've arrived\:

| Memory function | Attractor computation |
|--------|--------|
| Recognize current state | Pattern completion |
| Track current state | Continuous attractor dynamics |
| Anticipate successor | Associative excitation |
| Find an appropriate action | Content-addressable skill retrieval |
| Execute action | Parameterized motor dynamics |
| Verify transition | Predictive correspondence |
| Learn from outcome | Associative updating |

Perhaps we don't need to build a completely separate kind of memory for actions.

The action memory could be another population of predictive dynamical attractors, specialized through learning to represent transformations rather than perceptual configurations.

And here's the part I particularly like about your proposal\:

**The action attractor can be active simultaneously with the source and destination perceptual attractors.**

You could have three coupled dynamical processes\:

- The source circuit estimates what's happening now.
- The action circuit maintains the unfolding motor behavior.
- The successor circuit predicts and calibrates what the world is becoming.

All three continually exchange information. The resulting sensory feedback can adjust the action, update both perceptual states, and eventually trigger attentional handover.

That seems like a more natural architecture than retrieving an action, executing it blindly, and then checking whether the destination was reached.

And it gives us a particularly interesting research hypothesis\:

**Could functional motor skills emerge as attractor basins over families of predictable state transformations, rather than being explicitly assigned to individual state-transition pairs?**

If so, SOAM might learn reusable motor skills and discover their domains of applicability through the same associative competition and self-organization we're proposing for perceptual memory.

That strikes me as a worthwhile hypothesis to test.

**Context capsule\:** Action memory may be a content-addressable attractor network whose patterns encode reusable families of sensorimotor transformations. Source and desired successor states generate a transition cue that recruits and parameterizes motor dynamics. Functional similarity, not merely visual similarity, must determine reuse. Source, action, and successor attractors can operate concurrently, coupled through prediction and feedback.

## Prompt:
10/31/2026, 10:59:36 PM

Lastly I Don’t know how learning and self organizing memory work. Any ideas?

## Response:
10/31/2026, 10:59:46 PM · gpt-6-thinking

I think the key is to separate fast learning from slower reorganization: how SOAM records a new experience immediately, versus how it decides whether to modify an existing attractor, create a new one, or reorganize their relationships. I’ll anchor that in existing continual-learning and self-organizing-map research, then propose a minimal mechanism we could actually test.

> **Designing research directions**
>
> I’m identifying niche research areas for self-organizing dynamical models, online creation after failure, sensory boundaries, hard negatives, and hippocampal event segmentation. I’m also considering a conceptual architecture combining prediction, responsibility, adaptation, and episodic storage.
>
> **Designed research directions**
>
> 
>
> **Refining adaptive mechanisms**
>
> I’m distinguishing transition errors from genuinely new events: localized surprises should update relationships, while persistent unexplained mismatches create provisional episodes. I’m also incorporating uncertainty, context-specific credit, replay, consolidation, merging, splitting, pruning, and protected reusable knowledge.
>
> **Structuring learning timescales**
>
> I’m combining diffusion with fast one-shot episode formation, novelty-based vigilance, replay, topology growth, competitive maps, and local-model mixtures. The core design uses separate inference, episodic-writing, structural-growth, and consolidation timescales.
>
> **Separating adaptation pathways**
>
> I’m distinguishing state calibration from persistent learning: attractor states can adjust immediately, associations can bind in one shot, and structural changes should wait for replay, validation, and evidence that existing models cannot explain the residual.
>
> **Refined adaptive mechanisms, learning timescales, and adaptation pathways**
>
> 
>
> **Building adaptive architecture**
>
> I’m organizing the design around prediction, uncertainty, and multiple learning timescales: calibrate current states quickly, bind transitions immediately when justified, and delay structural growth until replay confirms persistent residuals.
>
> **Built adaptive architecture**
>
> 
>
> **Searched 16 websites**
>
> 
>
> Worked for 1m 40s

I think there's a promising way to approach this without introducing an entirely separate, highly sophisticated memory-organizing system.

**What if SOAM organizes itself through the same competition, prediction, and associative dynamics that we've already proposed for perception and action?**

The key would be to distinguish two questions\:

- **Learning\:** How does experience change an existing memory?
- **Self-organization\:** How does the system decide which memories should exist, what each should represent, and how they should be connected?

I would explore a system with **fast associative learning and slower structural self-organization**, both driven by predictive evidence.

## 1\. Four basic learning operations

Rather than requiring one universal weight-update rule to solve everything, consider four operations\:

| Operation | When it happens | What changes |
|--------|--------|--------|
| **Refine** | An existing circuit explains the experience, but imperfectly | Its local predictive dynamics |
| **Associate** | Two circuits exhibit a reliable relationship or transition | Associative connections and transition mappings |
| **Recruit** | Existing circuits consistently cannot explain a novel experience | A provisional new memory pattern |
| **Reorganize** | Accumulated experience reveals redundant, overlapping, or poorly separated memories | Circuit boundaries, associations, and potentially circuit structure |

The interesting thing is that these operations have established research precedents.

Adaptive Resonance Theory $ART) uses match/mismatch processes to balance learning new categories against preserving existing ones. Growing Neural Gas incrementally adds units and relationships based on accumulated errors. And Complementary Learning Systems provides a theoretical basis for rapid memory formation followed by slower integration with existing knowledge. \[[Adaptive Resonance Theory: How a brain learns to consciously attend, learn, and recognize a changing world](https://www.sciencedirect.com/science/article/pii/S0893608012002584?utm_source=chatgpt.com); [A Growing Neural Gas Network Learns Topologies](https://papers.neurips.cc/paper_files/paper/1994/hash/d56b9fc4b0f1be8871f5e1c40c0067e7-Abstract.html?utm_source=chatgpt.com); [Why there are complementary learning systems in the hippocampus and neocortex: insights from the successes and failures of connectionist models of learning and memory](https://pubmed.ncbi.nlm.nih.gov/7624455/?utm_source=chatgpt.com)\]

None of these directly solves SOAM, but together they suggest that the basic mechanisms we need are plausible.

## 2\. The most important distinction: calibration is not learning

We've discussed predictive circuits continuously calibrating their internal states from sensorimotor evidence.

But we should distinguish the circuit's momentary state from its persistent memory.

Let\:

$$
x_i(t)=\text{current dynamic state of circuit }i
$$

$$
\theta_i=\text{persistent learned parameters of circuit }i
$$

When the robot moves around a car, the wheel circuit's orientation estimate changes. That's calibration: updating \(x_i(t)$\.

When the robot discovers something new about how wheels behave, its predictive dynamics might change. That's learning: updating $\theta_i$\.

And when it discovers that one particular wheel is damaged, perhaps neither the generic wheel model nor its state should change permanently. Instead, the system writes an instance-specific memory associated with that wheel.

This distinction gives us three different kinds of information\:

Dynamic state

What is happening now?

Learned model

How does this usually work?

Specific memory

What happened to this instance?

This matters because **SOAM should be capable of remembering something after one encounter without immediately changing its general understanding of the world**\.

That might be the foundation of stable one-shot learning.

## 3\. How could learning happen continuously?

Imagine every active predictive circuit receives sensory evidence, predicts what should happen next, and compares its prediction with reality.

The resulting prediction errors provide a potential learning signal.

But we don't want to update every activated circuit. That's especially important now that SOAM supports multiple simultaneous hypotheses.

Suppose a car circuit and four wheel circuits are active. When one wheel turns, we shouldn't indiscriminately modify all five representations.

Instead, learning could be weighted by **which circuits were responsible for explaining which observations**\.

A simple proposed objective is\:

$$
\mathcal L =
\sum_{t,i} r_{i,t}\,\ell(\hat z_{i,t+1},z_{i,t+1})
+\lambda K
+\mu\mathcal L_{\mathrm{retention}}
$$

Here\:

- $r_{i,t}$ measures how strongly circuit $i$ is supported as an explanation for its assigned sensory evidence.
- $\ell$ is its prediction error, ideally uncertainty-weighted.
- $K$ measures the complexity of the memory system.
- $\mathcal L_{\mathrm{retention}}$ penalizes damage to previously learned capabilities.

Compatible circuits can both receive learning credit; responsibilities need only compete where explanations are mutually exclusive.

The complexity penalty encourages the system to reuse existing patterns rather than create a new one for everything.

The retention penalty helps prevent new experiences from destroying old knowledge.

The objective describes what we'd like to achieve, not a proven neural learning rule.

## 4\. What happens when something unexpected occurs?

I would treat persistent prediction error as a signal to investigate memory structure-not automatically as a command to create a new attractor.

**Existing circuit explains the observation**

Update its dynamic state. Refine its learned predictions when new, reliable information is available.

**Current circuit fails, another explains it**

Strengthen the transition association, including the conditions and coordinate mapping for handover. A new circuit may be unnecessary.

**No existing circuit explains the experience**

Store an immediate episodic trace. Recruit a provisional pattern if the mismatch is reliable and cannot be resolved by recalibration.

**Repeated experiences reveal a better organization**

Split an overgeneralized circuit, merge redundant circuits, or adjust their domains of predictive validity.

This is closely related to structure learning: a model may need to expand its repertoire of latent states or reduce redundant ones. That's been investigated in active-inference models of concept learning. \[[An Active Inference Approach to Modeling Structure Learning: Concept Learning as an Example Case](https://pmc.ncbi.nlm.nih.gov/articles/PMC7250191/?utm_source=chatgpt.com); [Frontiers \| An Active Inference Approach to Modeling Structure Learning: Concept Learning as an Example Case](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2020.00041/full?utm_source=chatgpt.com)\]

An important safeguard is that temporary uncertainty, occlusion, or incorrect localization should not trigger permanent memory creation.

## 5\. How could associations and motor skills learn?

I think this is where we can exploit associative memory most directly.

When two circuits repeatedly activate together, their associative connection can strengthen. When one consistently becomes active after another under a particular action, the system can learn a conditioned transition.

But simple Hebbian co-activation is insufficient to distinguish *part-of*, *causes*, *follows*, and *alternative-to* relationships. Those need evidence from temporal order, sensorimotor transformations, and relational consistency.

For example, a wheel and car moving together across multiple observations provides evidence for a persistent spatial relationship. A motor skill followed by a successful state change provides evidence about an action's effects.

The system could learn associations among current state, desired successor, motor-skill attractor, and observed consequences.

For the pants example, several successful episodes might gradually strengthen an association between a particular fabric-contact configuration and a gentle oscillatory skill.

Once learned, the motor attractor can be reused for unfamiliar but functionally similar transitions, while continued feedback updates its applicability and parameters.

Failures are informative too: they might narrow the skill's valid operating domain, rather than weaken the entire generic skill.

## 6\. What would slower self-organization actually do?

This is where I would introduce replay, but not necessarily diffusion models or another complicated neural subsystem.

The system periodically reactivates stored experiences and tests whether its existing memory organization can explain them efficiently.

A proposed organization rule could be\:

Retain the smallest collection of predictive circuits that can explain the relevant experiences, preserve important exceptions, and support reliable transitions and actions.

This might produce several structural changes.

**Splitting\:** One attractor accumulates conflicting predictions for two sensorimotor regimes. Creating two specialized circuits reduces error enough to justify the added complexity.

**Merging\:** Two circuits are found to have nearly identical predictive dynamics, action affordances, and compatible contexts. Their memories may be consolidated into one reusable pattern.

**Boundary adjustment\:** Two neighboring circuits improve their predictive accuracy by expanding or contracting their domains. Their pre-calibrated overlap provides a region where attentional handover remains reliable.

**Association refinement\:** Frequently useful relationships strengthen, while misleading or redundant associations weaken.

The crucial part is evaluating reorganizations against previously stored experiences, not just recent ones. Otherwise the system could continually rewrite its own memory and forget older knowledge.

This is essentially the stability-plasticity problem. Replay and interleaving are established approaches, though making them work efficiently in SOAM would be an open engineering challenge. \[[Complementary learning systems](https://pubmed.ncbi.nlm.nih.gov/22141588/?utm_source=chatgpt.com); [Incorporating rapid neocortical learning of new schema-consistent information into complementary learning systems theory](https://pubmed.ncbi.nlm.nih.gov/23978185/?utm_source=chatgpt.com)\]

## 7\. A minimal prototype learning loop

Here's how I'd try to implement the first experiment.

```text
for each sensorimotor observation:

    # Inference: no permanent memory changes yet
    activate candidate circuits from sensory and associative cues
    update candidate local states
    predict observations and action consequences
    determine which circuits explain which evidence

    # Fast learning
    if existing circuits explain the experience:
        refine local predictions when justified
        reinforce useful associations and transitions

    elif a valid successor explains the experience:
        learn or refine the handover relationship

    else:
        record an episodic trace
        recruit provisional memory if novelty is reliable

    # Slower structural learning
    periodically:
        replay recent and older experiences
        test candidate circuit splits and merges
        adjust domains and associations
        retain changes only if overall performance improves
```

For the earliest prototype, the memory circuits could be simple local recurrent predictors rather than full Hopfield networks. That would let us test the learning and organization rules independently of the eventual neural implementation.

I'd measure predictive accuracy, number of recruited circuits, one-shot recall, action-transfer success, handover accuracy, and forgetting after learning new experiences.

## 8\. A possibility I find especially interesting

Our earlier hypothesis was that competition could establish the boundaries of locally valid predictive attractors.

Perhaps **self-organization is the longer-timescale consequence of that same competition**\.

During perception, circuits compete to explain observations.

During learning, circuits compete to receive responsibility for experiences.

During consolidation, alternative memory organizations compete to explain the accumulated history more efficiently.

In this formulation, competition and predictive correspondence aren't just mechanisms for *using* memory. They also participate in determining *what memory becomes*\.

That's a compelling potential unification, though it's far from guaranteed that one set of local neural rules can implement all three processes.

And I think it exposes the next fundamental research question\:

**Can we devise a local associative plasticity rule that simultaneously supports one-shot writing, learned transition associations, and gradual specialization of attractor domains-without catastrophic interference?**

If that works, then structural operations like split and merge might be approximated by changes in distributed connectivity and attractor basins rather than requiring an explicit graph-editing controller.

That would bring us much closer to the self-organizing recurrent memory you're envisioning.

**Context capsule\:** Proposed SOAM learning consists of fast episodic/associative writing, local predictive refinement, and slower structural reorganization. Competition assigns learning responsibility and helps shape attractor domains. Persistent mismatch can trigger new patterns, while successful handovers strengthen transitions. Replay supports split/merge decisions and protects older memories. Central unresolved problem: a biologically plausible or computationally efficient local plasticity rule that unifies these operations.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)