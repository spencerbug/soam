# Priority and milestone tracker

Updated: 2026-11-01. The owner adopted the [v0.2 switching-first scope](docs/RESEARCH_SPEC_V0_2.md).
Cue-driven concurrent attractor handover now leads; the associative writer is a
separate comparison branch. This is an evidence-driven order, not a calendar or
blanket authorization to execute all tickets.

Ticket frontmatter owns metadata; this tracker owns execution order and milestone
summaries. See [ticket conventions](tickets/README.md), [agent instructions](AGENTS.md),
and the [work-package map](docs/ROADMAP.md).

## Current work and readiness

SOAM-032 records the documentation revision. The next bounded task is
[SOAM-033](tickets/SOAM-033-handover-protocol.md), the handover protocol and circuit
organization comparison. Its implementation and experiment remain backlog until
prerequisites finish. No handover gate has passed and no v0.2 experiment has run.

SOAM-004, SOAM-019, and SOAM-030 remain eligible supporting branches; readiness does
not make them the default next task. The historical [Gate 1](reports/GATE_1_REVIEW.md)
proceeds only for its recorded low-rank writer contract. Its negative results and
unresolved H1 claims remain unchanged. M1 now contains new unfinished handover work
in addition to those completed controls.

## Priority and status legend

- **P0:** next critical-path protocol, engineering, experiment, or decision.
- **P1:** subsequent core interfaces, embodied controls, acquisition, and evidence infrastructure.
- **P2:** later integration/transfer, supporting research, or retained comparison branches.
- **P3:** conditional optional mechanisms; not hidden prerequisites of the main path.
- **ready:** prerequisites satisfied; **backlog:** planned/unscheduled or dependencies incomplete;
  **in_progress:** active; **blocked:** exceptional impediment; **done:** deliverables/evidence complete;
  **cancelled:** superseded with a recorded reason/replacement.

Dependencies on decisions require done plus decision: proceed, including body-specific
conditions. Revise/stop keeps dependents unready until an explicit plan revision.
A planning decision permits only its scoped next work, not an empirical claim.
Thinking levels are advisory; see the [rubric](tickets/README.md#recommended-thinking-levels).

## Milestones

IDs remain thematic groups for provenance; their numbers do not impose execution order.

| Milestone | Focus | Exit evidence / decision | State |
| --- | --- | --- | --- |
| M0 | Reproducible infrastructure | Historical baseline SOAM-000; harness reuse | Initial sprint complete |
| M1 | Substrate and cue-driven handover | Historical Gate 1 preserved; new SOAM-033–036 test attractor recruitment, concurrency, sensorimotor cutover | Historical controls complete; new handover study planned |
| M2 | Grounded acquisition | Historical SOAM-003–006 branch; multi-circuit design/implementation/experiment/gate SOAM-039/044/040/041 | Old contract complete; both acquisition claims open |
| M3 | Conditional functional scopes | SOAM-007–010; limited interference with beneficial sharing | Deferred comparison branch |
| M4 | Replay and organization | SOAM-011/012 infrastructure; fixed-capacity SOAM-042/043; optional learned SOAM-013–015 | Planned; learned refinement conditional |
| M5 | Compositional reuse | SOAM-031 planning, SOAM-016–018 held-out reuse/identity; supplied structure disclosed | Planned after basic concurrency |
| M6 | Attention, beliefs, and grounding | Early synthetic SOAM-037; richer sensing SOAM-019–022 | Synthetic beliefs follow handover; richer branch eligible |
| M7 | Control and associative skills | SOAM-023/024/038/026; optional proposal efficiency SOAM-025 | Planned before complex learning |
| M8 | Continual embodied learning | SOAM-027/028 after composition, grounding, control, empirical acquisition, organization decisions | Planned |
| MX | Scope and supporting research | SOAM-032 scope adoption; SOAM-030 evidence map; SOAM-029 conditional flow | Documentation revision; optional research retained |

## Execution and dependency changes

Primary initial path: SOAM-032 → SOAM-033 → SOAM-034 → SOAM-035 → SOAM-036 →
SOAM-037 → SOAM-023 → SOAM-024 → SOAM-038. This tests switching first, then beliefs
and simple control. An explicit attractor candidate and recurrent controls start
together; sophisticated prediction and unsupervised organization are not required.

Composition planning/testing and richer sensing then supply distinct evidence.
SOAM-039 selects a later learning contract and SOAM-044 implements it; SOAM-011/012 implement evidence/replay
and validation, followed by acquisition SOAM-040/041 and organization SOAM-042/043.
SOAM-027 requires empirical outcomes, not merely the SOAM-039 design decision.

The v0.2 revision explicitly changes these dependency edges; existing gate outcomes
are not rewritten:

| Ticket | Removed dependency | Added prerequisite / reason |
| --- | --- | --- |
| SOAM-011 | SOAM-006 | SOAM-044 implements the multi-circuit contract selected by SOAM-039 |
| SOAM-013 | — | SOAM-041 plus documented replay inadequacy; learned refinement remains conditional |
| SOAM-016 | SOAM-015 | SOAM-031 and SOAM-037 supply composition design and concurrent-instance evidence |
| SOAM-021 | SOAM-015 | SOAM-036; rich-sensing SOAM-020 remains required |
| SOAM-023 | SOAM-022 | SOAM-036 and SOAM-037 support narrower synthetic control first |
| SOAM-026 | SOAM-025 | SOAM-038 tests skill reuse; learned proposals become optional |
| SOAM-027 | — | SOAM-022, SOAM-041, SOAM-043 add grounding/acquisition/organization gates |
| SOAM-031 | — | SOAM-036 grounds later composition planning in a tested organization |

No unfinished legacy ticket is closed by this scope adoption. SOAM-031 retains its
unfinished source review and composition-mechanism planning. Historical local-write
and learned-scope results cannot substitute for multi-circuit evidence. Growth,
cloning policies beyond the selected protocol, split/merge, and flow are not implicit
implementation authorization.

## Ordered ticket queue

Order selects among eligible tickets; it never bypasses dependencies or body conditions.
Stable ticket IDs are unchanged. Independent supporting work may proceed when useful.

| Order | Ticket | Priority | Status | Milestone | Thinking | Depends on |
| --- | --- | --- | --- | --- | --- | --- |
| 00 | [SOAM-000: Record the reproducible substrate baseline](tickets/SOAM-000-substrate-baseline.md) | P0 | done | M0 | medium | — |
| 01 | [SOAM-001: Strengthen substrate controls and budget comparisons](tickets/SOAM-001-substrate-controls.md) | P0 | done | M1 | high | [SOAM-000](tickets/SOAM-000-substrate-baseline.md) |
| 02 | [SOAM-002: Gate 1: review the substrate before online writing](tickets/SOAM-002-gate-1.md) | P0 | done | M1 | high | [SOAM-001](tickets/SOAM-001-substrate-controls.md) |
| 03 | [SOAM-003: Define the grounded local-write contract and plastic parameters](tickets/SOAM-003-plastic-write-contract.md) | P1 | done | M2 | high | [SOAM-002](tickets/SOAM-002-gate-1.md) |
| 04 | [SOAM-032: Adopt the switching-first embodied attractor scope](tickets/SOAM-032-embodied-scope-revision.md) | P0 | done | MX | xhigh | — |
| 05 | [SOAM-033: Specify cue-driven handover and circuit-layout controls](tickets/SOAM-033-handover-protocol.md) | P0 | ready | M1 | xhigh | [SOAM-032](tickets/SOAM-032-embodied-scope-revision.md) |
| 06 | [SOAM-034: Implement the bounded concurrent-attractor handover harness](tickets/SOAM-034-handover-harness.md) | P0 | backlog | M1 | high | [SOAM-033](tickets/SOAM-033-handover-protocol.md) |
| 07 | [SOAM-035: Measure cue-driven concurrent attractor handover](tickets/SOAM-035-cue-driven-handover.md) | P0 | backlog | M1 | xhigh | [SOAM-034](tickets/SOAM-034-handover-harness.md) |
| 08 | [SOAM-036: Review cue-driven handover and select the supported circuit organization](tickets/SOAM-036-handover-gate.md) | P0 | backlog | M1 | xhigh | [SOAM-035](tickets/SOAM-035-cue-driven-handover.md) |
| 09 | [SOAM-037: Test dual attention and concurrent instance beliefs](tickets/SOAM-037-attention-belief-instances.md) | P1 | backlog | M6 | xhigh | [SOAM-036](tickets/SOAM-036-handover-gate.md) |
| 10 | [SOAM-023: Implement candidate action search and known goal costs](tickets/SOAM-023-action-search.md) | P1 | backlog | M7 | high | [SOAM-036](tickets/SOAM-036-handover-gate.md), [SOAM-037](tickets/SOAM-037-attention-belief-instances.md) |
| 11 | [SOAM-024: Benchmark navigation, changed dynamics, and planning horizons](tickets/SOAM-024-planning-benchmark.md) | P1 | backlog | M7 | high | [SOAM-023](tickets/SOAM-023-action-search.md) |
| 12 | [SOAM-038: Compare associative skill retrieval across held-out transitions](tickets/SOAM-038-associative-skill-transfer.md) | P1 | backlog | M7 | xhigh | [SOAM-024](tickets/SOAM-024-planning-benchmark.md), [SOAM-037](tickets/SOAM-037-attention-belief-instances.md) |
| 13 | [SOAM-026: Gate 7: assess planning benefit and safe memory separation](tickets/SOAM-026-gate-7.md) | P1 | backlog | M7 | high | [SOAM-024](tickets/SOAM-024-planning-benchmark.md), [SOAM-038](tickets/SOAM-038-associative-skill-transfer.md) |
| 14 | [SOAM-031: Plan research on compositional dynamical motifs and learned pattern detectors](tickets/SOAM-031-compositional-dynamics-planning.md) | P2 | backlog | M5 | xhigh | [SOAM-036](tickets/SOAM-036-handover-gate.md) |
| 15 | [SOAM-016: Benchmark withheld compositions and transfer to related tasks](tickets/SOAM-016-composition-transfer.md) | P2 | backlog | M5 | xhigh | [SOAM-031](tickets/SOAM-031-compositional-dynamics-planning.md), [SOAM-037](tickets/SOAM-037-attention-belief-instances.md) |
| 16 | [SOAM-017: Test identity preservation and reusable temporal structure](tickets/SOAM-017-identity-timescales.md) | P2 | backlog | M5 | high | [SOAM-016](tickets/SOAM-016-composition-transfer.md) |
| 17 | [SOAM-018: Gate 5: assess compositional reuse rather than memory maintenance](tickets/SOAM-018-gate-5.md) | P2 | backlog | M5 | xhigh | [SOAM-017](tickets/SOAM-017-identity-timescales.md) |
| 18 | [SOAM-019: Build rendered observations and frozen encoder comparisons](tickets/SOAM-019-frozen-encoders.md) | P2 | ready | M6 | medium | [SOAM-002](tickets/SOAM-002-gate-1.md) |
| 19 | [SOAM-020: Train recurrent prediction and assimilation on rendered observations](tickets/SOAM-020-grounded-prediction.md) | P2 | backlog | M6 | high | [SOAM-019](tickets/SOAM-019-frozen-encoders.md) |
| 20 | [SOAM-021: Evaluate partial observations, ambiguity, and context recovery](tickets/SOAM-021-partial-belief-recovery.md) | P2 | backlog | M6 | xhigh | [SOAM-020](tickets/SOAM-020-grounded-prediction.md), [SOAM-036](tickets/SOAM-036-handover-gate.md) |
| 21 | [SOAM-022: Gate 6: review sensory grounding and belief recovery](tickets/SOAM-022-gate-6.md) | P2 | backlog | M6 | high | [SOAM-021](tickets/SOAM-021-partial-belief-recovery.md) |
| 22 | [SOAM-039: Select a grounded multi-circuit learning contract](tickets/SOAM-039-grounded-memory-design.md) | P1 | backlog | M2 | xhigh | [SOAM-036](tickets/SOAM-036-handover-gate.md), [SOAM-037](tickets/SOAM-037-attention-belief-instances.md), [SOAM-038](tickets/SOAM-038-associative-skill-transfer.md) |
| 23 | [SOAM-044: Implement the selected multi-circuit write contract](tickets/SOAM-044-multicircuit-write-contract.md) | P1 | backlog | M2 | high | [SOAM-039](tickets/SOAM-039-grounded-memory-design.md) |
| 24 | [SOAM-011: Implement a bounded grounded evidence buffer and replay baseline](tickets/SOAM-011-evidence-and-replay.md) | P1 | backlog | M4 | high | [SOAM-044](tickets/SOAM-044-multicircuit-write-contract.md) |
| 25 | [SOAM-012: Validate consolidation candidates with shadow weights and rollback](tickets/SOAM-012-shadow-validation.md) | P1 | backlog | M4 | high | [SOAM-011](tickets/SOAM-011-evidence-and-replay.md) |
| 26 | [SOAM-040: Benchmark grounded multi-circuit acquisition and instance retention](tickets/SOAM-040-multicircuit-acquisition.md) | P1 | backlog | M2 | xhigh | [SOAM-039](tickets/SOAM-039-grounded-memory-design.md), [SOAM-012](tickets/SOAM-012-shadow-validation.md) |
| 27 | [SOAM-041: Review grounded multi-circuit acquisition and retention](tickets/SOAM-041-multicircuit-acquisition-gate.md) | P1 | backlog | M2 | high | [SOAM-040](tickets/SOAM-040-multicircuit-acquisition.md) |
| 28 | [SOAM-042: Test predictive specialization and association refinement at fixed capacity](tickets/SOAM-042-fixed-capacity-organization.md) | P2 | backlog | M4 | xhigh | [SOAM-041](tickets/SOAM-041-multicircuit-acquisition-gate.md) |
| 29 | [SOAM-043: Review fixed-capacity organization before continual integration](tickets/SOAM-043-organization-gate.md) | P2 | backlog | M4 | xhigh | [SOAM-042](tickets/SOAM-042-fixed-capacity-organization.md) |
| 30 | [SOAM-027: Integrate an extended continual embodied-learning benchmark](tickets/SOAM-027-continual-benchmark.md) | P2 | backlog | M8 | xhigh | [SOAM-018](tickets/SOAM-018-gate-5.md), [SOAM-022](tickets/SOAM-022-gate-6.md), [SOAM-026](tickets/SOAM-026-gate-7.md), [SOAM-041](tickets/SOAM-041-multicircuit-acquisition-gate.md), [SOAM-043](tickets/SOAM-043-organization-gate.md) |
| 31 | [SOAM-028: Review cumulative learning evidence and the next research cycle](tickets/SOAM-028-continual-review.md) | P2 | backlog | M8 | xhigh | [SOAM-027](tickets/SOAM-027-continual-benchmark.md) |
| 32 | [SOAM-004: Benchmark online transition correction and changed dynamics](tickets/SOAM-004-online-writer-baselines.md) | P2 | ready | M2 | high | [SOAM-003](tickets/SOAM-003-plastic-write-contract.md) |
| 33 | [SOAM-005: Measure interference and learning without resets](tickets/SOAM-005-interference-metrics.md) | P2 | backlog | M2 | high | [SOAM-004](tickets/SOAM-004-online-writer-baselines.md) |
| 34 | [SOAM-006: Gate 2: decide whether local acquisition is viable](tickets/SOAM-006-gate-2.md) | P2 | backlog | M2 | high | [SOAM-004](tickets/SOAM-004-online-writer-baselines.md), [SOAM-005](tickets/SOAM-005-interference-metrics.md) |
| 35 | [SOAM-007: Compare unfiltered, sparse, random, and sensitivity-based scopes](tickets/SOAM-007-heuristic-scopes.md) | P2 | backlog | M3 | high | [SOAM-006](tickets/SOAM-006-gate-2.md) |
| 36 | [SOAM-008: Build shared-scope and noisy-evidence task families](tickets/SOAM-008-scope-task-families.md) | P2 | backlog | M3 | high | [SOAM-007](tickets/SOAM-007-heuristic-scopes.md) |
| 37 | [SOAM-009: Meta-train a constrained functional scope translator](tickets/SOAM-009-learned-scope.md) | P2 | backlog | M3 | xhigh | [SOAM-008](tickets/SOAM-008-scope-task-families.md) |
| 38 | [SOAM-010: Gate 3: evaluate functional scoping and beneficial sharing](tickets/SOAM-010-gate-3.md) | P2 | backlog | M3 | high | [SOAM-009](tickets/SOAM-009-learned-scope.md) |
| 39 | [SOAM-013: Train a learned iterative low-rank consolidator](tickets/SOAM-013-learned-consolidator.md) | P3 | backlog | M4 | xhigh | [SOAM-010](tickets/SOAM-010-gate-3.md), [SOAM-012](tickets/SOAM-012-shadow-validation.md), [SOAM-041](tickets/SOAM-041-multicircuit-acquisition-gate.md) |
| 40 | [SOAM-014: Measure consolidation error recovery, compute, and fixed-size capacity](tickets/SOAM-014-consolidation-scaling.md) | P3 | backlog | M4 | high | [SOAM-013](tickets/SOAM-013-learned-consolidator.md) |
| 41 | [SOAM-015: Gate 4: decide whether learned consolidation adds value over replay](tickets/SOAM-015-gate-4.md) | P3 | backlog | M4 | high | [SOAM-014](tickets/SOAM-014-consolidation-scaling.md) |
| 42 | [SOAM-025: Learn goal-conditioned action proposals after search is reliable](tickets/SOAM-025-action-proposals.md) | P2 | backlog | M7 | high | [SOAM-024](tickets/SOAM-024-planning-benchmark.md) |
| 43 | [SOAM-029: Conditionally investigate flow-based consolidation](tickets/SOAM-029-optional-flow.md) | P3 | backlog | MX | xhigh | [SOAM-015](tickets/SOAM-015-gate-4.md) |
| 44 | [SOAM-030: Maintain a focused theory and literature evidence map](tickets/SOAM-030-theory-literature.md) | P2 | ready | MX | high | [SOAM-000](tickets/SOAM-000-substrate-baseline.md) |

## Housekeeping check

Run the ticket validator before finishing changes: uv run python scripts/check_tickets.py.

No remote issues are created by this tracker. A completed ticket does not itself
establish attraction, learning, compositionality, or neuroscientific validity.
