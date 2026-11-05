# Interface boundaries

The [conditional research paths](RESEARCH_PATHS.md) govern follow-ups: first
measure one benefit of sharing, then select one experimental fork from the results.
Concurrency/handover and the two application studies are conditional extensions.

The [scientific review](SCIENTIFIC_REVIEW_2026_11_05.md) separates task utility,
mechanism attribution, learning, and active perception. Shared units remain a
candidate choice; conventional, separated, fast-memory/core and structured hybrids
remain legitimate alternatives. Use [lightweight RFCs](rfcs/README.md) inside existing
decision tickets, and expose actual memory lifetimes rather than naming every
functional responsibility a separate neural module.

## Current v0.3 shared-population direction

The [v0.3 scope](RESEARCH_SPEC_V0_3.md) makes overlapping recurrent neurons and
connections the preferred candidate for feature, relationship, and action-relation
functions. These are representational responsibilities, not mandatory separate
neural modules. Separate sensory adapters, readouts, evaluators, and write interfaces
remain useful software boundaries. Actual versus desired state, instance binding,
evidence provenance, and motor authority must remain identifiable even when encoded
in shared activity.

A shared tensor containing disjoint blocks, tied weights with cloned state, or an
external relation graph does not demonstrate neuronal sharing. The new protocol must
specify overlap/connectivity, directional/asymmetric updates, timescales, activity
allocation, causal interventions, and cross-function interference. Separated networks
remain controls; partial overlap and negative findings are legitimate outcomes.
No arbitrary asymmetric rule inherits a symmetric Hopfield convergence argument.

[SOAM-047](../tickets/SOAM-047-platform-contract.md) adopted the
[minimal platform contract](RECURRENT_PLATFORM_CONTRACT.md): explicit-state dynamics,
observed-data task adapters, frozen prediction, interventions, metrics and artifacts.
Offline fitting is separate; online learning plugins are deferred. A backend's
state/energy/update assumptions must be explicit. The runner supports independent
shared-mechanism, localization, and learning-module studies without requiring each
to implement the entire embodied SOAM architecture. No new implementation is claimed.

## Historical v0.2 research boundaries

The following records the v0.2 design and initial two-state scaffold. It is retained
for the implemented handover contract; current architecture preference and future
integration dependencies follow v0.3 and the priority tracker.

The [v0.2 specification](RESEARCH_SPEC_V0_2.md) prioritizes cue-driven attractor
switching and sensorimotor handover. The interfaces below describe broader research
boundaries. [SOAM-033](../tickets/SOAM-033-handover-protocol.md)
now freezes the first bounded signatures, candidate layouts, and controls in the
[handover protocol](HANDOVER_PROTOCOL.md). SOAM-034 implemented that bounded
contract in the [handover harness](HANDOVER_HARNESS.md), verified with fixtures;
the broader alternatives below remain experimental and empirical claims remain open.

| Boundary | State and responsibility |
| --- | --- |
| Sensory interface | Fixed projection of declared observations; actions are executed commands, not hidden world state |
| Circuit parameters | Persistent dynamics, readout, and cue couplings; initially hand-set or offline fitted and frozen during evaluation |
| Circuit instance | Independent transient state, instance binding, calibration history, and evidence support; parameters may be shared |
| Associative coupling | Content/context-dependent graded excitation; explicit target IDs or edge tables are labeled scaffolds/controls |
| Attention and belief coordination | Separate sensory focus, memory focus, hypothesis compatibility, and resource scheduling |
| Handover | Promote a calibrated candidate while preserving source/context as required; log reset, state copy, and role changes |
| Motor execution | Separate execution authority, phase, current estimate, desired outcome, and termination/interrupt conditions |
| Evidence and persistent learning | Grounded write proposals, validation, commit/rollback; introduced after switching is tested |

Primed, tracking, and attended are functional roles, not a requirement for three
permanent neural populations. A primed cue may be latent; a tracking instance must
actually process available sensorimotor evidence. The attended instance must not
overwrite another candidate's activity merely because both reuse the same weights.
Whether one shared population can represent those concurrent states is unproven.

### Population organization and resource ownership

Compare a bounded selection of one shared population, separate parallel circuits,
shared-weight/separate-state clones, alternating (flip-flop) banks, and columns/stacks.
Two separate live states are an initial scaffold, not a selected final architecture.
Columns/stacks need a precise definition of coupling and scheduling before trials;
no biological equivalence is assumed. Physical neural-population separation does
not require separate processors.

For each candidate, record which parameters are tied/copied, which states are
independent/copied, cue pathways, sensory routing, update schedule, peak concurrency,
and total parameter/state/buffer/compute cost. A bank swap is an attention operation;
it establishes attractor switching only if cue-dependent dynamical recruitment and
recovery are demonstrated independently. Repeated handovers must reveal stale or
overwritten state. Do not introduce a mandatory discrete object graph.

### Initial interaction and evidence contract

1. Receive the current permitted observation and the last executed action.
2. Propagate attended/tracking states and apply sensory correction where available.
3. Emit graded cues; recruit or update candidates within the declared resource budget.
4. Compare explanatory support and compatibility without double-counting internal
   predictions as new observations. Keep contradictory hypotheses distinct.
5. Transfer attentional influence according to the declared scaffold or cue dynamics;
   log which mechanism actually caused the switch.
6. Decode a simple prediction to check retained state and continuity. Later, select
   an action using separate execution authority and observe its real consequence.

All of these initially leave persistent parameters unchanged. Prediction snapshots
also isolate every candidate state and any evidence buffers from live interaction.
Desired successor states cannot initialize an estimated actual state as if observed.
Oracle labels, known correspondence, and explicit switch schedules belong in a
scaffold ledger and labeled comparison, never silently in the evaluated learner.

### Deferred learning and action design

Keep generic circuit parameters, instance-specific persistent facts, and live state
separate. One reusable model may serve several instances. A proposed future skill
memory maps current state plus desired transformation/context to feedback-driven
motor dynamics; it need not allocate a separate skill for every state pair.
Actions may persist across attentional handovers. Unsupervised circuit discovery,
dynamic recruitment, split/merge rules, learned attention, and full motor learning
are deferred until controlled mechanisms can be measured.

## Existing v0.1 implementation (preserved)

The implementation currently contains conventional recurrent baselines. All functions have
explicit state inputs and outputs; model modules hold parameters, never the active
belief state.

| Boundary | v0.1 contract | Initial implementation |
| --- | --- | --- |
| Encoder | `encode(observation) -> z` | Fixed orthonormal projection of synthetic observation |
| Observation assimilation | `assimilate(h_pred, z, context) -> h_obs` | Convex blend with learned sensory-state projection |
| Recurrent memory | `step(h, action, context) -> h_next` | Leaky tanh, additive/gated/low-rank context |
| Readout | `decode(h) -> z_pred` | Trained linear map |
| Fast writer | evidence → proposed parameter delta | [Grounded bounded proposals, explicit commit, one-level rollback](../soam/plasticity/README.md); H2 unproven |
| Scope translator | local statistics + proposed delta → constrained delta | Deferred |
| Consolidator | weights + grounded evidence → validated provisional weights | Deferred |
| Planner | state + candidate actions + goal → selected action | Deferred |

`rollout` starts from one observation, then uses only hidden state, supplied actions,
and supplied context. It never sees future observations or ground-truth world state.
Grounded one-step evaluation assimilates each real observation between predictions.
The fixed projection has an inverse only for diagnostic plots; predictors cannot
call that inverse. Full observability and known context are deliberate first-stage
simplifications. There is no context inference or uncertainty representation yet.

The separate-core baseline has disjoint per-context transition matrices and shared
sensory initialization/readout. It carries a single active hidden state across switches
without resetting it. This is partial independence, not a fully independent ensemble;
the limitation is explicit in the protocol. No explicit object graph is used in inference.
