# Work packages and completion criteria

The [v0.2 specification](RESEARCH_SPEC_V0_2.md) was adopted on 2026-11-01.
The [priority tracker](../PRIORITIES.md) owns execution order and mirrored ticket
metadata. Work-package and milestone numbers are thematic categories, not a required
sequence. Existing results and Gate 1 remain historical evidence with their original
limits; no new experiment has been run by this documentation revision.

## Immediate work

[SOAM-033](../tickets/SOAM-033-handover-protocol.md) defines the first cue-driven
handover protocol. Follow with a bounded harness (SOAM-034), measured trials
(SOAM-035), and a new empirical decision (SOAM-036). Test attended, tracking, and
primed roles with sensorimotor feedback. Switching is primary; simple prediction
checks guard against collapse and loss of state.

Choose a small explicit-attractor/recurrent comparison and a population-separation
comparison. Shared populations, parallel circuits, shared-weight clones, alternating
banks, and columns/stacks remain alternatives. No mandatory discrete world graph,
single-population concurrency, or unsupervised discovery is assumed. Record supplied
cues, basins, routing, bindings, and schedules, and separate them from observed
attractor dynamics. See [architecture boundaries](ARCHITECTURE.md).

## Package status and ticket map

| Package | Current scope and criterion | Tickets / decisions |
| --- | --- | --- |
| WP-00 | Preserve deterministic harness/provenance and historical reproduction; extend state/cue instrumentation for the chosen experiment | SOAM-000 done; [SOAM-034](../tickets/SOAM-034-handover-harness.md) planned |
| WP-01 | Historical six-model controls and limited Gate 1 complete; new cue-driven recruitment, concurrent calibration, and handover untested | SOAM-001/002 done; [SOAM-033](../tickets/SOAM-033-handover-protocol.md), [SOAM-035](../tickets/SOAM-035-cue-driven-handover.md), [SOAM-036](../tickets/SOAM-036-handover-gate.md) |
| WP-02 | Historical bounded writer implemented; acquisition unproven. Later design, implement, and test a multi-circuit write contract | [SOAM-003](../tickets/SOAM-003-plastic-write-contract.md) done; SOAM-004/006 comparison branch; [SOAM-039](../tickets/SOAM-039-grounded-memory-design.md), [SOAM-044](../tickets/SOAM-044-multicircuit-write-contract.md), [SOAM-040](../tickets/SOAM-040-multicircuit-acquisition.md), [SOAM-041](../tickets/SOAM-041-multicircuit-acquisition-gate.md) |
| WP-03 | Retention/interference across contexts and later generic/instance memory, including multistep and handover effects | [SOAM-005](../tickets/SOAM-005-interference-metrics.md), SOAM-039–041 |
| WP-04 | Conditional fixed/random/sensitivity scope comparison; task isolation is not useful sharing | [SOAM-007](../tickets/SOAM-007-heuristic-scopes.md), [SOAM-008](../tickets/SOAM-008-scope-task-families.md) |
| WP-05 | Conditional learned scope compared with simple masks at matched acquisition; not required for early switching/control | [SOAM-009](../tickets/SOAM-009-learned-scope.md), [SOAM-010](../tickets/SOAM-010-gate-3.md) |
| WP-06 | Grounded bounded evidence/replay and shadow validation after the multi-circuit write contract is implemented | [SOAM-011](../tickets/SOAM-011-evidence-and-replay.md), [SOAM-012](../tickets/SOAM-012-shadow-validation.md) |
| WP-07 | Fixed-capacity organization compared with replay/frozen organization; learned iterative refinement only for a documented unmet need | [SOAM-042](../tickets/SOAM-042-fixed-capacity-organization.md), [SOAM-043](../tickets/SOAM-043-organization-gate.md); optional SOAM-013–015 |
| WP-08 | Composition planning and held-out reuse/identity tests distinguish supplied bindings from learned reusable structure | [SOAM-031](../tickets/SOAM-031-compositional-dynamics-planning.md), [SOAM-016](../tickets/SOAM-016-composition-transfer.md), [SOAM-017](../tickets/SOAM-017-identity-timescales.md), [SOAM-018](../tickets/SOAM-018-gate-5.md) |
| WP-09 | Fixed sensing first; rendered/frozen-encoder comparisons are a separate eligible supporting branch | [SOAM-019](../tickets/SOAM-019-frozen-encoders.md) |
| WP-10 | Early synthetic attention/instances after handover; richer prediction/ambiguity afterwards, without mandatory learned consolidation | [SOAM-037](../tickets/SOAM-037-attention-belief-instances.md); [SOAM-020](../tickets/SOAM-020-grounded-prediction.md), [SOAM-021](../tickets/SOAM-021-partial-belief-recovery.md), [SOAM-022](../tickets/SOAM-022-gate-6.md) |
| WP-11 | Simple synthetic search/control before complex learning; current/successor states, motor authority, and no-write imagination | [SOAM-023](../tickets/SOAM-023-action-search.md), [SOAM-024](../tickets/SOAM-024-planning-benchmark.md), [SOAM-026](../tickets/SOAM-026-gate-7.md) |
| WP-12 | Content-addressable skill retrieval and feedback dynamics; learned proposal heads are optional efficiency work | [SOAM-038](../tickets/SOAM-038-associative-skill-transfer.md); [SOAM-025](../tickets/SOAM-025-action-proposals.md) |
| WP-13 | Integrate only after composition, richer grounding, control, empirical acquisition, and organization decisions | [SOAM-027](../tickets/SOAM-027-continual-benchmark.md), [SOAM-028](../tickets/SOAM-028-continual-review.md) |

## Historical evidence and supporting work

The [substrate controls](../reports/SUBSTRATE_CONTROLS.md) record 17/18 screening
passes, an additive seed-23 failure, six seed-11 exact repeats, and unresolved H1
claims. The [writer report](../reports/LOCAL_WRITE_CONTRACT.md) records 48 passing
tests for that implementation and multistep regressions despite immediate error
reduction. Preserve both; neither establishes concurrent attractor dynamics.

[SOAM-032](../tickets/SOAM-032-embodied-scope-revision.md) records scope adoption only.
[SOAM-030](../tickets/SOAM-030-theory-literature.md) retains a bounded literature map;
[SOAM-029](../tickets/SOAM-029-optional-flow.md) remains conditional. No unfinished
legacy research ticket is closed by v0.2. Planning decisions do not pass empirical
gates, and completing implementation does not establish a scientific hypothesis.

Dynamic growth, structural split/merge, unrestricted cloning, learned attention,
natural-video encoders, and physical robotics require separately scoped follow-ups.
The initial population comparison must stay bounded rather than implement every
possible circuit organization.
