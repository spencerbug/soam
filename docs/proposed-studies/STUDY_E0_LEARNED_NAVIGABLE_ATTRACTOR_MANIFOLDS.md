# SOAM Study E0 — Learning Navigable Attractor Manifolds

## Research objective

You are an AI research engineer working on **Self-Organizing Attractor Memory (SOAM)**, an experimental research project investigating recurrent neural dynamics as a foundation for embodied sensorimotor intelligence.

Inspect the existing SOAM repository, completed Studies A, B, and C, and the planned studies before beginning. Follow existing experimental conventions, benchmark methodology, documentation practices, and reproducibility standards.

This study introduces a new hypothesis:

**A recurrent neural network can learn a low-dimensional, navigable attractor manifold from sensorimotor experience, where corrective dynamics stabilize the representation while action-conditioned dynamics move the representation along physically meaningful trajectories.**

The long-term SOAM vision is an atlas of connected attractor manifolds representing objects, poses, transformations, affordances, and relationships. A robot would navigate this atlas through actions, sensory observations, and internally generated predictions.

Study E0 should investigate the most fundamental prerequisite for this vision: can recurrent dynamics learn an attracting, controllable representation of a continuous physical state?

This is a focused, falsifiable research experiment, not an attempt to build the complete atlas architecture.

## 1. Theoretical motivation

Conventional associative memories are often conceptualized as energy landscapes containing isolated local minima. A corrupted representation moves toward an attractor and eventually settles.

An embodied world model requires something more expressive.

Imagine a neural state space containing a valley or ravine. Neural activity is attracted toward the bottom of the valley, but can move along its length without losing stability.

Two complementary processes govern its evolution:

- **Transverse dynamics:** Correct perturbations perpendicular to the manifold, restoring a coherent internal representation.
- **Tangential dynamics:** Move along the manifold according to actions, learned transitions, or intrinsic dynamics.

A useful conceptual model is:

\[
\dot h=-\nabla E(h)+F_{\parallel}(h,a)
\]

where \(h\) is the recurrent state, \(E\) represents an attractive potential, and \(F_{\parallel}\) represents action-dependent motion tangent to the manifold.

This equation is a conceptual starting point, not an architectural requirement.

General asymmetric recurrent networks may not admit a global scalar energy function. The important property is an attracting invariant manifold with controllable dynamics along it.

For a discrete-time RNN, the corresponding hypothesis can be expressed as:

\[
h_{t+1}=F_{\theta}(h_t,o_t,a_t)
\]

We want the network to learn a manifold \(\mathcal M\) such that:

1. Recurrent states near \(\mathcal M\) converge toward it.
2. Different positions on \(\mathcal M\) remain distinguishable.
3. With zero action and no new observations, the represented physical state remains approximately stationary.
4. Nonzero actions move the recurrent state along \(\mathcal M\) in predictable directions.
5. Sensory observations can correct errors without destroying the continuity of the representation.
6. The representation generalizes to action sequences not observed during training.

Crucially, **success must be demonstrated in the recurrent state dynamics, not merely inferred from accurate output predictions.**

## 2. Primary research questions

**RQ1 — Emergent geometry**

Can a recurrent network trained on sensorimotor sequences spontaneously develop a low-dimensional attracting manifold?

Does this geometry emerge in a conventional GRU, or does it require additional inductive biases?

**RQ2 — Stability versus navigation**

Can the network simultaneously achieve:

- Strong stability perpendicular to the manifold.
- Approximately neutral stability along the manifold when stationary.
- Controlled bidirectional movement along the manifold when actions are applied?

Does stronger attraction interfere with navigability?

**RQ3 — Genuine dynamic structure**

How can we distinguish a learned attractor manifold from a network that simply encodes position or memorizes recurrent trajectories?

Does the internal geometry survive hidden-state perturbations, extended sensory deprivation, and unfamiliar action sequences?

**RQ4 — Learning versus architectural enforcement**

How much geometric structure can emerge from ordinary sequence-learning objectives?

Which minimal architectural or training modifications improve attractor stability without prescribing the desired manifold explicitly?

**RQ5 — Recurrent population organization**

Would separating corrective and navigational functions into distinct but mutually coupled recurrent populations improve performance?

Can specialized functions emerge without manually assigning every neuron to a fixed role?

Treat RQ5 as exploratory. The first four questions take priority.

## 3. Experimental environment

Start with the simplest nontrivial continuous system: **a single object whose orientation can rotate through 360 degrees**.

Its physical configuration space has circular topology:

\[
\theta\in S^1
\]

\[
\theta_{t+1}=(\theta_t+\omega_t\Delta t)\bmod 2\pi
\]

The system receives intermittent, partial, noisy sensory observations and an action input indicating rotational velocity.

Its recurrent state must maintain an internal representation of orientation and update it as the object rotates.

### Observations

Construct synthetic sensory features using nonlinear, potentially overlapping tuning functions of orientation.

Avoid directly providing perfect absolute orientation as an input.

Support:

- Observation noise.
- Partial feature visibility.
- Missing observations.
- Ambiguous individual features.
- Different sensory resolutions.

Ensure the combined observations contain enough information to make the task learnable.

### Actions

Include positive, negative, and zero rotational velocities, with varying magnitudes and durations.

Generate randomized trajectories rather than only fixed demonstrations.

### Learning

Begin with offline training using sensory prediction, reconstruction, or other sequence-based learning objectives.

Do not require persistent online weight updates or self-organizing memory insertion for E0. Those mechanisms belong to subsequent work and Study D.

Avoid directly supervising the desired hidden-state geometry using ground-truth angle coordinates in the primary experiment.

Ground-truth orientation may be used for environment generation and evaluation.

## 4. Models and baselines

Use parameter-matched models and comparable training budgets wherever possible.

### Baseline A — Conventional estimator

Implement a compact conventional state estimator or Bayesian filter appropriate to the synthetic environment.

This establishes how well the task can be solved without learned recurrent attractor geometry.

### Baseline B — Standard GRU

Train a conventional GRU on exactly the same observations, actions, and predictive objectives.

This is an essential baseline.

Previous SOAM studies demonstrated that GRUs can perform surprisingly well. Do not assume that a standard GRU lacks attractive manifold dynamics.

Analyze its learned recurrent geometry using the same tests as all other models.

### Candidate C — Geometry-aware recurrent network

Investigate a recurrent architecture or training objective that encourages:

- Attraction toward coherent recurrent states.
- Preservation of distinct positions along the learned manifold.
- Action-conditioned movement.
- Stability under zero action.

Possible mechanisms include controlled recurrent asymmetry, state consistency losses, local contraction regularization, and action-conditioned transition operators.

These are candidates, not requirements.

Prefer the smallest modification capable of testing the hypothesis.

### Candidate D — Coupled recurrent populations (optional)

If justified by the initial findings, investigate two coupled populations that can develop complementary functions.

One may predominantly support corrective dynamics, while another supports action-conditioned navigation.

Allow bidirectional interaction and mutual settling.

Do not assume predefined specialization is optimal. Compare constrained specialization against learned specialization where feasible.

Defer larger population architectures and complex compositional structures to future studies.

## 5. Evaluation methodology

Prediction accuracy alone is insufficient.

The experiment must independently characterize the internal recurrent dynamics.

### A. Manifold emergence and topology

Collect recurrent states across different orientations and action sequences.

Analyze:

- Intrinsic dimensionality.
- Local smoothness.
- State-space continuity.
- Whether equivalent physical orientations map to consistent nearby representations.
- Whether a closed rotation produces a closed recurrent trajectory.
- Whether the learned geometry is consistent with circular topology.

Use PCA and nonlinear manifold visualization for exploration, supplemented by quantitative intrinsic-dimensionality and topology tests where appropriate.

Do not treat a visually convincing PCA or UMAP plot as proof of an attractor.

### B. Off-manifold perturbation recovery

Take a recurrent state corresponding to a known orientation.

Perturb its hidden state without providing new observations.

Measure:

- Whether it returns toward a coherent recurrent state.
- Recovery time.
- Displacement along the manifold after recovery.
- Whether the represented orientation is preserved.
- Maximum recoverable perturbation magnitude.

Use multiple perturbation directions and magnitudes.

Where possible, distinguish perturbations tangent to the learned manifold from perturbations normal to it.

**This test is central to distinguishing genuine attractive dynamics from ordinary trajectory prediction.**

### C. Neutral stability

Initialize the network at multiple positions along the learned manifold.

Remove observations and apply zero action.

Test whether the network:

- Preserves its orientation estimate.
- Avoids collapsing toward a small set of preferred states.
- Avoids drifting around the manifold.
- Maintains stability over substantially longer horizons than those seen during training.

A network that collapses to one fixed point does not satisfy the intended hypothesis.

### D. Action-conditioned navigation

Apply positive, negative, zero, and variable-velocity actions.

Evaluate:

- Directional consistency.
- Proportionality between action and movement.
- Reversibility.
- Closed-loop accuracy after one or more rotations.
- Generalization to unfamiliar action compositions.
- Accumulated error during long sensory-free trajectories.

Test whether the same internal geometry is traversed in different directions instead of creating unrelated trajectories for different action histories.

### E. Local dynamical stability

Analyze the recurrent update Jacobian around learned states.

For the zero-input discrete-time system, seek evidence of:

- Contractive modes normal to the manifold, with eigenvalue magnitudes below one.
- Approximately neutral tangent modes, with eigenvalues near one.
- No dominant unstable modes that destroy the representation.

Examine how action inputs alter these dynamics.

Account for the possibility that finite-time dynamics, non-normal Jacobians, and imperfectly learned manifolds complicate local eigenvalue analysis.

Do not interpret Jacobian eigenvalues alone as sufficient proof.

### F. Sensory correction and calibration

Allow the network to navigate without observations, accumulating uncertainty or drift.

Then reintroduce noisy sensory evidence.

Evaluate whether sensory correction restores alignment with the physical state while preserving coherent manifold dynamics.

Compare against the robust correction mechanisms investigated in Study B2 where relevant.

### G. Generalization and failure modes

Test:

- Longer-than-training sequences.
- Novel velocities and action compositions.
- Increased observation noise.
- Extended occlusions.
- Hidden-state perturbations during active motion.
- Initializations away from observed training trajectories.

Determine whether failures arise from inaccurate geometry, weak attraction, incorrect action dynamics, or limitations in state observability.

## 6. Critical ablations

At minimum, compare:

1. Standard predictive training versus geometry-aware training.
2. With and without action conditioning.
3. With and without hidden-state perturbations during training.
4. Different recurrent state sizes.
5. Different strengths of any attraction or stability regularization.

If coupled populations are investigated, compare them against parameter-matched single-population controls.

For every proposed architectural improvement, determine whether its advantage comes from actual geometric stability or simply additional parameters, training data, or optimization advantages.

Use multiple random seeds and report uncertainty.

## 7. Success criteria and falsifiability

Before examining final held-out results, define operational metrics and quantitative success thresholds appropriate to the baseline performance.

A successful experiment should demonstrate that at least one learned recurrent model:

- Supports a coherent, continuous representation of orientation.
- Exhibits measurable attraction back toward its learned state manifold after transverse perturbations.
- Preserves distinguishable states along the manifold with zero action.
- Supports reliable bidirectional action-conditioned navigation.
- Generalizes to unseen action trajectories.
- Achieves these properties through learned dynamics rather than hardcoded coordinate integration or an explicitly imposed circular latent representation.

A particularly important result would be demonstrating that improvements in transverse stability **do not require sacrificing tangential controllability**.

A negative result is valuable.

For example:

- Predictive GRUs may perform well without forming robust attracting manifolds.
- Stability regularization may cause collapse into isolated fixed points.
- Strong correction may erase position information.
- Action conditioning may create trajectories that do not share a coherent manifold.
- An explicitly structured model may outperform learned geometry while offering little generalization advantage.

Report these results rather than optimizing only for confirmation of the hypothesis.

## 8. Scope boundaries

**Do not attempt the following in E0:**

- Multiple independently learned objects.
- Hierarchical or compositional object relationships.
- Branching graphs of attractor manifolds.
- Full visual SLAM.
- Complex learned action policies.
- Persistent online memory insertion.
- A complete cortical-column architecture.
- An implementation of the full SOAM atlas.

These are potential follow-up studies.

E0 should answer whether a single, nontrivial navigable manifold can be learned and rigorously characterized.

## 9. Deliverables

Produce:

**Research plan**
- Formal hypotheses and competing explanations.
- Literature review covering continuous attractors, line/ring attractors, slow manifolds, asymmetric recurrent networks, and action-conditioned path integration.
- Experimental configurations and preregistered evaluation criteria.

**Implementation**
- Reproducible synthetic environment.
- Models and baselines.
- Training and evaluation scripts.
- Deterministic seeds and configuration tracking.
- Automated tests.

**Analysis**
- Prediction performance comparisons.
- Learned-state geometry visualizations.
- Perturbation recovery curves.
- Drift and navigation error measurements.
- Local dynamical stability analysis.
- Ablation results and uncertainty estimates.

**Research report**
- What was demonstrated.
- What was not demonstrated.
- Whether the standard GRU already develops relevant dynamics.
- Whether explicit attractor-oriented inductive biases help.
- Which aspects are learned versus architecturally imposed.
- Implications for SOAM.

Follow the repository's established study reporting conventions and prepare findings suitable for publication on the associated research blog.

## 10. Connection to the future SOAM atlas

The broader hypothesis is that embodied intelligence may benefit from a memory system that learns not only stored states, but the geometry of valid transformations between states.

A future SOAM system could represent:

- An object as a navigable configuration manifold.
- An action as a transformation or control field on that manifold.
- A relationship as a constraint coupling multiple manifolds.
- A context as a modulation of accessible states and transitions.
- A learned atlas as connected local manifolds with reusable transition dynamics.

However, these are long-term architectural hypotheses rather than conclusions of E0.

The central research question remains:

**Can a recurrent neural network discover a representation that is simultaneously attractive, stable, navigable, and predictive, without being explicitly programmed with the geometry of the physical state space?**

## 11. Execution instructions

Begin by reviewing the existing SOAM experiments and identifying reusable infrastructure.

Then:

1. Produce a concise experimental design and identify the strongest alternative explanations.
2. Establish the conventional estimator and GRU baselines.
3. Characterize whether the GRU already develops attracting manifold dynamics.
4. Introduce the minimal geometry-aware modification justified by the evidence.
5. Run controlled comparisons and ablations.
6. Investigate coupled recurrent populations only if their inclusion answers a clearly identified unresolved question.
7. Publish a reproducible report with quantitative evidence and limitations.

Prioritize scientific interpretability over architectural complexity.

**The goal is not to construct a system that looks like an attractor manifold. The goal is to discover whether useful attracting and navigable geometry can emerge through learning, and what conditions make that emergence possible.**