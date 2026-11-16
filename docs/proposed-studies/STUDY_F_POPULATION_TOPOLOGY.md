# Codex prompt — Study F: Recurrent population topology roadmap and controlled search

**Status:** planning-only proposal. Do not run topology sweeps or implement a new platform until a fresh decision selects a bounded protocol.

## Mission

Plan a scientifically fair, staged comparison of **monolithic**, **hierarchically stacked**, **horizontally distributed/routed**, and **temporarily intermingled** recurrent populations for embodied sensorimotor reasoning. The fourth is a coupling *mechanism* that can coexist with any topology, not an assumed fourth winner.

Review the latest SOAM evidence, especially the November 14 Study C: https://spencerbug.github.io/research/soam-study-c/ . TWO16 uses two separate recurrent state instances and shared ordinary PC16 parameters; its Brier advantage over PC16/PC32 supports *factorized neural state* for a supplied two-regime ambiguity task, not physically coupled neurons, modular composition or primed/tracking/attended control. The conventional ADAPT1-C model stayed competitive and TWO16 had no practical declared advantage over ADAPT1-M on Brier. A reliable topology study must explain those alternatives rather than treating the result as proof of cortical columns.

## Search objective and hypotheses

F-H1 (stacking): Local recurrence plus upward/downward projections can produce useful abstractions, predictive correction or complexity scaling beyond a flat capacity-matched model.

F-H2 (horizontal): Independently evolving components and sparse learned routing can preserve simultaneous states and reduce interference or communication cost.

F-H3 (monolithic): A large densely connected gated recurrent population learns equivalent capabilities without explicit separate state banks; extra gating may improve trainability but not necessarily forward stability.

F-H4 (temporary intermingling): Gated bidirectional cross-population recurrence can enable new compositional sensorimotor predictions and joint settling **while preserving private dynamics**, not merely passing a one-way cue. See STUDY_F_GATED_INTERMINGLING.md.

F-H0: Simple conventional recurrent, factorized-state, or structured filtering models solve the tasks at lower total cost. A strong filter with multiple conditional branches is part of the controls, not a straw man.

## Candidate families

### A. Stacked recurrent populations

- Feedforward stack with local settling at each layer, examining width schedules: constant, compression, expansion and narrow-wide.
- Bidirectional adjacent-layer messaging: top-down reconstruction and bottom-up evidence; compare sequential passes with simultaneous iterative joint settling.
- Shared encoder/decoder **population** (one recurrent state supporting ascending and descending roles) versus separate encoder and decoder populations; separately test distinct, tied, transposed or learned projections. Sharing one population does not require tying projections.
- Predictive-correction or equilibrium-like iterative stack, but do not assert existence of a scalar energy or convergence without evidence. Record internal iterations as compute.
- Hypothesis: layers convey increasingly reusable structure rather than merely increasing depth; test with withheld compositions and causal interventions, not t-SNE alone.

### B. Horizontal populations with routing

- Disjoint maintained populations with no communication.
- Full direct lateral projections.
- Sparse learned cue messages / associative addresses.
- Central thalamus-inspired router, with router weights/state and dynamic routing decisions explicitly charged.
- Cross-pop consensus as a separate candidate; sometimes hypotheses compete, sometimes distinct objects coexist. Do not normalize complementary states into one winner.
- Allow supplied roles as labeled scaffold in early mechanism pilots, then test role selection without oracle identities. A routed hidden-state copy is not neuron-level intermingling.

### C. Large monolithic gated recurrence

- Within-family width sweeps (e.g. 16/32/64/128 only as provisional sizes), with matched training and progressively longer rollouts.
- Fixed-leak tanh, GRU/constant-gate, and gated symmetric/asymmetric recurrence as *separate tested mechanisms*, retaining simple strong references.
- Analyze gradients and Jacobians independently: gates can help gradient propagation but do not guarantee correct global attraction, safe long-horizon predictions, robustness or bounded recurrent dynamics at larger width.
- Search dense versus learned sparse/contextual connectivity, per-unit timescales, action/feature coupling, and emerging within-state specialization.
- Count O(n^2) dense parameter and multiply costs, gain/control and memory overhead.

### D. Dynamic gated intermingling as an orthogonal coupling axis

Given two or more independently meaningful recurrent populations, temporarily activate cross-population synaptic/message influence, allow *bidirectional recurrent settling*, then decouple while preserving component integrity. Compare direct state interactions, low-rank block coupling and routing-only communication. The narrowly scoped pilot is in STUDY_F_GATED_INTERMINGLING.md. Do not equate shared parameter code, concatenation or running two state banks with actual joint dynamics.

## Staged and fair architecture search

**F0 — contracts and task taxonomy.** Identify what architectural functions are being tested and the *smallest common external task*: partial-cue recall, action-conditioned prediction, complementarity, ambiguous alternatives, relation binding and held-out combination reuse. Keep clean observation permission/evidence identical; allow justified internal update schedules at costed budgets.

**F1 — within-family single-factor sweeps.** For each family, vary one mechanism at a time (depth, feedback, routing, gate schedule, coupling strength). Use a common competent recurrent primitive whenever isolating topology; match total trainable parameter count approximately and report differences. Do not confound every design dimension.

**F2 — family-specific pairwise Pareto screens.** Compare root-level performance at fixed train exposure, parameter budget, active/retained state, inference compute and measured latency as separate tracks. Include all projections, readouts, router, communication, repeated settling, temporary workspace and external storage. Equal parameters alone does not equal resource equivalence.

**F3 — common capability tournament.** Once within-family candidates are credible, use a preregistered series: reconstruction & dynamics -> genuine ambiguity & corruption -> complementary components -> object-relative navigation -> withheld relational composition -> active sensing -> continual memory, advancing only when earlier findings justify the next stage. Use independent held-out tasks, multiple resource regimes, proper probability scores and uncertainty guards, not a single arbitrary leaderboard metric.

**F4 — causal post-tournament ablation.** When a family wins, identify whether gain came from state factorization, parameter tying, communication, extra inference iterations, supplied roles, or optimization. A winner is not automatically evidence of anatomical cortical-column equivalence.

## Explicit Study C bridge

Two **competing** trajectory hypotheses under a known two-regime task are *not* two complementary object subcircuits that should necessarily converge. Before coupling, construct tasks with **coexisting** components whose states/actions and relationship outputs have an unambiguous physical meaning. The two-state C result motivates testing representations and selective messaging; it does not establish that joint settling is helpful. A structurally aware single-state control and conventional filter mixture remain mandatory. The coherent false-evidence failure should be tested with an explicit missing-cause/unknown hypothesis as a separate factor; coupling must not be credited for information it cannot obtain.

## Biological inspiration

Compare cortical hierarchy, thalamocortical gating, distributed modularity, continuous attractors, predictive coding, deep equilibrium and mixture-of-experts literature as *possible computational analogies*. Any reciprocity/stability claim needs local Jacobian tests or a conditional derivation; symmetric weights with action-conditioned/asymmetric, gated, discrete updates do not automatically minimize a Hopfield energy.

## Deliverables and explicit boundary

Produce one lightweight topology RFC; operational hypotheses; common task API; within-family ablation matrices; minimal baselines; numerical resource budgets; seed/split/confirmation policy; promotion/stopping criteria; risk ledger; and one selected candidate next pilot (if evidence supports one). Preserve failure modes and deferred branches. Map proposed tickets only using valid existing conventions and unused IDs after checking the real working branch. Don't change completed gate records, schedule GPU training, publish an issue or implement the full tournament. A separate routing decision is required.

**Final question:** At what task complexity and resource regime, if any, do depth, horizontal communication or temporary gated coupling add practical capabilities beyond monolithic recurrence or structured state estimation?
