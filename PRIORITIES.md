# Priority and milestone tracker

Updated: 2026-11-11. The owner adopted the [v0.3 shared-population experiment
platform scope](docs/RESEARCH_SPEC_V0_3.md). Overlapping neurons for features,
relationships, and action relations are the preferred architecture hypothesis.
Separated networks remain controls. The program also supports independent Hopfield
and recurrent-dynamics experiment families, including localization and sensorimotor
learning modules. This ordering is not blanket authorization to execute the backlog.

Ticket frontmatter owns metadata; this tracker owns ordering and milestone summaries.
See [ticket conventions](tickets/README.md), [agent instructions](AGENTS.md), and
[work-package map](docs/ROADMAP.md). Stable IDs and historical filenames are preserved.

The [scientific review](docs/SCIENTIFIC_REVIEW_2026_11_05.md), [hypothesis ledger](docs/HYPOTHESES.md),
and [ticket dispositions](docs/TICKET_REVIEW_2026_11_05.md) sharpen the next questions
to E1 useful dynamics, E2 rapid retained acquisition, and E3 active disambiguation.
E1 is complete with a negative sharing gate. SOAM-059 historically selected E2
protocol design; the owner superseded that current selection with Study A. Study A
is complete, and no next experiment is selected.

## Current work and readiness

**Study B selected by the owner, November 11.** SOAM-066 is in progress for the temporal assimilation protocol and bounded architecture search informed by Study A. SOAM-067–069 follow sequentially. The accepted ceiling is 7200 CPU / 14400 execution wall seconds and 2 GiB RSS/artifacts. Acquisition and all other forks remain unselected.

**November 11: Study A complete.** SOAM-062 done/proceed, SOAM-063/064 done, and SOAM-065 done/proceed for the [R32 core recommendation](reports/STUDY_A_DECISION.md) only. The [scientific result](reports/STUDY_A.md) is inconclusive for the frozen practical adaptive-update claim. All 120 confirmation fits and 12 prescribed repeats completed within the cumulative ceiling; 215 tests pass. No next experiment is selected, Study B is unimplemented, and SOAM-039 remains backlog pending fresh routing. Historical E1 evidence and SOAM-052 stop remain unchanged.


[SOAM-046](tickets/SOAM-046-shared-platform-scope.md) records initial v0.3 adoption;
[SOAM-060](tickets/SOAM-060-scientific-roadmap-review.md) records this scientific review.
SOAM-047 is done with `decision: "proceed"` for the [minimal platform contract](docs/RECURRENT_PLATFORM_CONTRACT.md).
SOAM-049 is done with `decision: "proceed"` for the [E1 v1 protocol](docs/SHARED_POPULATION_PROTOCOL.md)
and [manifest](docs/protocols/shared_population_v1.json), with the T32 identifiability limit explicit.
SOAM-048 delivered the [fixture-verified platform runner](reports/RECURRENT_PLATFORM.md).
SOAM-050 delivered the [E1 engineering harness](reports/SHARED_POPULATION_HARNESS.md):
171 passing tests, 181 fixture cells per execution and exact replay of 1,560 arrays.
Its full-inventory preflight failed the artifact projection (11.81 GiB with 2× margin
versus 8 GiB), while compute and RSS checks passed. That engineering phase included no scientific fits.
SOAM-061 completed with `decision: "proceed"` for [archive addendum A1](docs/E1_ARCHIVE_A1.md).
The [replacement calibration](reports/E1_ARCHIVE_A1.md) passes all limits, including
5.27 GiB projected artifacts with 2× margin. All 190 tests pass.
Historical [SOAM-052](tickets/SOAM-052-shared-population-gate.md)
is done with **decision: stop** for the tested S32 useful-sharing claim. The
[gate report](reports/SHARED_POPULATION_GATE.md) accepts the complete scientific
comparison with disclosed reporting telemetry limitations and applies the frozen
absolute-recall failure before benefit. Relative retention guards pass; both GRUs
have lower primary error; causal precision remains unresolved and T32 limits
physical-overlap attribution. [SOAM-051](reports/SHARED_POPULATION_STUDY.md) remains
complete with 119 fits/27,820 cells and exact reproduction; source, selections,
negative results and allocation are preserved. No sharing-dependent child is unblocked.
[SOAM-059](reports/RESEARCH_FORK_SELECTION.md) is done/proceed for one E2 protocol:
G32 with a bounded recurrent writer, versus no-write/RLS/online-gradient/retrieval
controls, on an identifiable changed action gain. That selection is superseded by
the November 11 owner override; SOAM-039 and downstream implementation/trial tickets
remain backlog. Its historical separate ceiling is 3,600 CPU /
7,200 wall seconds, 2 GiB RSS / 2 GiB artifacts and 16 base fits maximum; no E2
protocol is yet approved and no branch implementation or trial has begun.

SOAM-033/034 completed the frozen [handover protocol](docs/HANDOVER_PROTOCOL.md),
[numerical manifest](docs/protocols/handover_v1.json), and [fixture-verified harness](reports/HANDOVER_HARNESS.md).
SOAM-035 remains ready at P2 with its frozen experimental contract intact; SOAM-036
remains backlog. They are retained comparisons, not the primary architecture path.
No measured handover study or shared-population empirical gate has passed.

SOAM-004, SOAM-019, and SOAM-030 remain ready supporting branches. Historical
[Gate 1](reports/GATE_1_REVIEW.md) authorizes only its recorded writer study and leaves
its negative results and unresolved H1 claims intact. Readiness does not select a
supporting task automatically; a new primary experiment requires fresh routing.

## Priority and status legend

- **P0:** next primary contract, runner, shared-population experiment, or decision.
- **P1:** independent application tracks and subsequent core beliefs/control/learning.
- **P2:** later integration, supporting research, or retained comparison branches.
- **P3:** conditional optional mechanisms; never hidden prerequisites.
- **ready:** prerequisites satisfied; **backlog:** unscheduled or dependencies incomplete;
  **in_progress:** active; **blocked:** exceptional impediment; **done:** evidence/deliverables complete;
  **cancelled:** superseded with reason and replacement.

Decision prerequisites require done plus decision: proceed and all body conditions.
Negative experiments may complete; revise/stop decisions keep dependents unready.
Planning and fixture verification do not establish scientific results. Thinking
levels are advisory and follow the [rubric](tickets/README.md#recommended-thinking-levels).

## Milestones

IDs are thematic provenance groups, not sequential dates or compulsory stages for every experiment.

| Milestone | Focus | Exit evidence / decision | State |
| --- | --- | --- | --- |
| M0 | Reusable recurrent experiment infrastructure | Historical harnesses plus the minimal SOAM-047 contract and SOAM-048 runner/invariant fixtures | Minimal runner delivered; exact fixture repeat and 110 passing tests; no scientific gate |
| M1 | Shared populations and recurrent dynamics | SOAM-049–052 test one sharing benefit with interference guardrails and explicit T32 claim limits; SOAM-059 selects the next fork | E1 harness delivered; v1 storage failure preserved; SOAM-061 A1 proceed; 119 fits/27,820 cells complete; absolute recall failure, exact repeat; SOAM-052 done/stop for tested useful sharing; dependent integration unready; Study A complete/inconclusive practical update benefit; SOAM-065 proceeds with R32 reference recommendation only |
| M2 | Grounded acquisition | Early E2 through SOAM-039/044/040/041: few-observation learning with retained generalization; no skill/concurrency/replay-stack prerequisite | Historical contract complete; SOAM-059 selection superseded by Study A; SOAM-039 backlog pending fresh routing; acquisition unmeasured |
| M3 | Conditional functional scopes | SOAM-007–010; limited interference with beneficial sharing | Deferred comparison branch |
| M4 | Replay and overlapping organization | SOAM-011/012, SOAM-042/043 at fixed capacity; optional SOAM-013–015 | Planned; learned refinement conditional |
| M5 | Compositional reuse | SOAM-031, SOAM-016–018; held-out feature/relation/action reuse and identity | Planned after shared-population evidence |
| M6 | Grounding and independent applications | E3 active disambiguation SOAM-053–055; later SOAM-037/019–022 and module SOAM-056–058 after acquisition | Conditional alternatives awaiting named fork selection, contract/runner, and own decisions |
| M7 | Control and shared action relations | SOAM-023/024/038/026; optional SOAM-025 | Planned after supported shared beliefs/handover |
| M8 | Continual embodied integration | SOAM-027/028 require composition, grounding, control, acquisition, organization outcomes | Planned; application success alone does not pass integration gates |
| MX | Scope and supporting research | SOAM-046 adoption and SOAM-060 review; SOAM-030 evidence map; SOAM-045 optional recurrent attention; SOAM-029 optional flow | SOAM-059 routing preserved; Study A delivered under owner override; no next experiment selected |

## Execution paths and dependency changes

Primary path: SOAM-047 minimum contract → SOAM-049 minimal benefit protocol;
SOAM-048 runner + SOAM-049 → SOAM-050 → SOAM-061 corrective feasibility decision → SOAM-051. The pilot measures one primary
benefit of sharing with recall/interference guardrails and is now complete with a
negative gate. The subsequent Study A diagnostic is complete; acquisition, concurrent
handover and broad backend work remain deferred.

SOAM-052 completed the scientific review with stop; its failed gate remains intact.
SOAM-059 is historically done/proceed for **E2 via SOAM-039** using ordinary G32
under the [bounded branch record](reports/RESEARCH_FORK_SELECTION.md). The owner
selected Study A instead; its completed SOAM-065 decision recommends R32 without
activating Study B or acquisition. SOAM-039/044/040/041 remain backlog pending fresh
routing and their own prerequisites. E3 and attention remain backlog despite
completed ordinary dependencies because their named-selection conditions are false.
No sharing-dependent edge changes. Later experiments need fresh routing, not reuse
of SOAM-059. See [conditional paths and outcome table](docs/RESEARCH_PATHS.md).

| Result / selection | Eligible next path | Conditions |
| --- | --- | --- |
| Acquisition selected | SOAM-039 → SOAM-044 → SOAM-040 → SOAM-041 | Platform contract and named fork selection; no skills or full replay/shadow stack; alternatives may follow a negative sharing result |
| Useful sharing; concurrency selected | SOAM-037 → supported SOAM control/skill path | SOAM-052 proceed and SOAM-059 explicit selection; usable measured binding/handover before control |
| Interference or directional failure | One new bounded diagnostic protocol | Fresh ID, fixed capacity/budget, failed gate preserved, fresh confirmation data |
| Active disambiguation selected | SOAM-053 → SOAM-054 → SOAM-055 | SOAM-047 and SOAM-059 proceed, then own protocol proceed and runner; no positive sharing gate required |
| Later learning module selected | SOAM-056 → SOAM-057 → SOAM-058 | Same routing rules plus SOAM-041 acquisition proceed; other applications stay backlog |
| Specific retrieval/cue limitation | Optional SOAM-045 design study | Explicit selection and a falsifiable reason for this alternative |
| No supported advantage / invalid / exhausted budget | Simpler reference, bounded repair, defer, or stop | Preserve uncertainty and negative findings; no automatic expansion |

SOAM-039 now depends on SOAM-047/059 instead of SOAM-052/037/038. SOAM-040 depends
on SOAM-039/044 instead of SOAM-012. SOAM-042 explicitly retains SOAM-052 plus
SOAM-041; SOAM-056 adds SOAM-041. These changes separate minimal acquisition from
later shared organization and preserve the latter's evidence requirements.

Later acquisition/organization and application outcomes also branch as specified in
the research-path table and ticket bodies. Frontmatter dependencies remain AND;
body conditions are additional eligibility checks. Corrective protocols depend on
completed evidence, not a failed decision. Successful correction requires a fresh
review and an explicit downstream dependency revision. Unselected forks remain
backlog. The old frozen v1 handover and writer comparison branches are preserved.

The [v0.2 scope](docs/RESEARCH_SPEC_V0_2.md) preserves the earlier dependency
rationale and gate meanings. No completed gate outcome or historical report changes.
Shared neurons do not erase evidence provenance, actual/desired distinctions, or
motor authority. Separated states, explicit maps, and graph/point-cloud memories
remain labeled controls, with every auxiliary resource counted.

## Ordered ticket queue

Order is a preference within the selected path. It never schedules all alternatives or overrides evidence/branch conditions.

| Order | Ticket | Priority | Status | Milestone | Thinking | Depends on |
| --- | --- | --- | --- | --- | --- | --- |
| 00 | [SOAM-000: Record the reproducible substrate baseline](tickets/SOAM-000-substrate-baseline.md) | P0 | done | M0 | medium | — |
| 01 | [SOAM-001: Strengthen substrate controls and budget comparisons](tickets/SOAM-001-substrate-controls.md) | P0 | done | M1 | high | [SOAM-000](tickets/SOAM-000-substrate-baseline.md) |
| 02 | [SOAM-002: Gate 1: review the substrate before online writing](tickets/SOAM-002-gate-1.md) | P0 | done | M1 | high | [SOAM-001](tickets/SOAM-001-substrate-controls.md) |
| 03 | [SOAM-003: Define the grounded local-write contract and plastic parameters](tickets/SOAM-003-plastic-write-contract.md) | P1 | done | M2 | high | [SOAM-002](tickets/SOAM-002-gate-1.md) |
| 04 | [SOAM-032: Adopt the switching-first embodied attractor scope](tickets/SOAM-032-embodied-scope-revision.md) | P0 | done | MX | xhigh | — |
| 05 | [SOAM-033: Specify cue-driven handover and circuit-layout controls](tickets/SOAM-033-handover-protocol.md) | P0 | done | M1 | xhigh | [SOAM-032](tickets/SOAM-032-embodied-scope-revision.md) |
| 06 | [SOAM-034: Implement the bounded concurrent-attractor handover harness](tickets/SOAM-034-handover-harness.md) | P0 | done | M1 | high | [SOAM-033](tickets/SOAM-033-handover-protocol.md) |
| 07 | [SOAM-046: Adopt shared-population recurrent experimentation scope](tickets/SOAM-046-shared-platform-scope.md) | P0 | done | MX | high | — |
| 08 | [SOAM-060: Review scientific direction and refine evidence-driven milestones](tickets/SOAM-060-scientific-roadmap-review.md) | P0 | done | MX | xhigh | — |
| 09 | [SOAM-047: Define the shared-population experiment platform contract](tickets/SOAM-047-platform-contract.md) | P0 | done | M0 | xhigh | [SOAM-046](tickets/SOAM-046-shared-platform-scope.md) |
| 10 | [SOAM-049: Specify a minimal test of the benefit of shared recurrence](tickets/SOAM-049-shared-population-protocol.md) | P0 | done | M1 | xhigh | [SOAM-047](tickets/SOAM-047-platform-contract.md) |
| 11 | [SOAM-048: Implement the reusable recurrent-dynamics experiment runner](tickets/SOAM-048-platform-runner.md) | P0 | done | M0 | high | [SOAM-047](tickets/SOAM-047-platform-contract.md) |
| 12 | [SOAM-050: Implement the bounded shared-population comparison](tickets/SOAM-050-shared-population-candidates.md) | P0 | done | M1 | high | [SOAM-048](tickets/SOAM-048-platform-runner.md), [SOAM-049](tickets/SOAM-049-shared-population-protocol.md) |
| 13 | [SOAM-061: Resolve E1 artifact feasibility before scientific fitting](tickets/SOAM-061-e1-artifact-feasibility.md) | P0 | done | M1 | high | [SOAM-049](tickets/SOAM-049-shared-population-protocol.md), [SOAM-050](tickets/SOAM-050-shared-population-candidates.md) |
| 14 | [SOAM-051: Measure the benefit and interference of shared recurrence](tickets/SOAM-051-shared-population-study.md) | P0 | done | M1 | xhigh | [SOAM-050](tickets/SOAM-050-shared-population-candidates.md), [SOAM-061](tickets/SOAM-061-e1-artifact-feasibility.md) |
| 15 | [SOAM-052: Review evidence for useful shared recurrence](tickets/SOAM-052-shared-population-gate.md) | P0 | done | M1 | xhigh | [SOAM-051](tickets/SOAM-051-shared-population-study.md) |
| 16 | [SOAM-059: Select one bounded research fork from the pilot evidence](tickets/SOAM-059-research-fork-selection.md) | P0 | done | MX | xhigh | [SOAM-051](tickets/SOAM-051-shared-population-study.md) |
| 17 | [SOAM-039: Specify minimal grounded acquisition and retention](tickets/SOAM-039-grounded-memory-design.md) | P0 | backlog | M2 | xhigh | [SOAM-047](tickets/SOAM-047-platform-contract.md), [SOAM-059](tickets/SOAM-059-research-fork-selection.md) |
| 18 | [SOAM-044: Implement bounded acquisition candidates and write invariants](tickets/SOAM-044-multicircuit-write-contract.md) | P1 | backlog | M2 | high | [SOAM-039](tickets/SOAM-039-grounded-memory-design.md) |
| 19 | [SOAM-040: Measure one-shot and few-observation acquisition with retention](tickets/SOAM-040-multicircuit-acquisition.md) | P1 | backlog | M2 | xhigh | [SOAM-039](tickets/SOAM-039-grounded-memory-design.md), [SOAM-044](tickets/SOAM-044-multicircuit-write-contract.md) |
| 20 | [SOAM-041: Review rapid acquisition and retained generalization](tickets/SOAM-041-multicircuit-acquisition-gate.md) | P1 | backlog | M2 | high | [SOAM-040](tickets/SOAM-040-multicircuit-acquisition.md) |
| 21 | [SOAM-053: Specify active disambiguation with recurrent sensorimotor beliefs](tickets/SOAM-053-localization-protocol.md) | P1 | backlog | M6 | xhigh | [SOAM-047](tickets/SOAM-047-platform-contract.md), [SOAM-059](tickets/SOAM-059-research-fork-selection.md) |
| 22 | [SOAM-054: Implement the active-disambiguation task and controls](tickets/SOAM-054-localization-adapter.md) | P1 | backlog | M6 | high | [SOAM-048](tickets/SOAM-048-platform-runner.md), [SOAM-053](tickets/SOAM-053-localization-protocol.md) |
| 23 | [SOAM-055: Measure active disambiguation and belief-guided behavior](tickets/SOAM-055-localization-study.md) | P1 | backlog | M6 | high | [SOAM-054](tickets/SOAM-054-localization-adapter.md) |
| 24 | [SOAM-056: Specify a Monty-style recurrent learning-module study](tickets/SOAM-056-learning-module-protocol.md) | P1 | backlog | M6 | xhigh | [SOAM-047](tickets/SOAM-047-platform-contract.md), [SOAM-059](tickets/SOAM-059-research-fork-selection.md), [SOAM-041](tickets/SOAM-041-multicircuit-acquisition-gate.md) |
| 25 | [SOAM-057: Implement the recurrent learning-module task and controls](tickets/SOAM-057-learning-module-adapter.md) | P1 | backlog | M6 | high | [SOAM-048](tickets/SOAM-048-platform-runner.md), [SOAM-056](tickets/SOAM-056-learning-module-protocol.md) |
| 26 | [SOAM-058: Measure recurrent learning-module acquisition and recognition](tickets/SOAM-058-learning-module-study.md) | P1 | backlog | M6 | xhigh | [SOAM-057](tickets/SOAM-057-learning-module-adapter.md) |
| 27 | [SOAM-037: Test attention and instance binding in shared populations](tickets/SOAM-037-attention-belief-instances.md) | P1 | backlog | M6 | xhigh | [SOAM-052](tickets/SOAM-052-shared-population-gate.md), [SOAM-059](tickets/SOAM-059-research-fork-selection.md) |
| 28 | [SOAM-023: Implement candidate action search and known goal costs](tickets/SOAM-023-action-search.md) | P1 | backlog | M7 | high | [SOAM-052](tickets/SOAM-052-shared-population-gate.md), [SOAM-037](tickets/SOAM-037-attention-belief-instances.md) |
| 29 | [SOAM-024: Benchmark navigation, changed dynamics, and planning horizons](tickets/SOAM-024-planning-benchmark.md) | P1 | backlog | M7 | high | [SOAM-023](tickets/SOAM-023-action-search.md) |
| 30 | [SOAM-038: Compare shared-population action-relation and skill reuse](tickets/SOAM-038-associative-skill-transfer.md) | P1 | backlog | M7 | xhigh | [SOAM-024](tickets/SOAM-024-planning-benchmark.md), [SOAM-037](tickets/SOAM-037-attention-belief-instances.md) |
| 31 | [SOAM-026: Gate 7: assess planning benefit and safe memory separation](tickets/SOAM-026-gate-7.md) | P1 | backlog | M7 | high | [SOAM-024](tickets/SOAM-024-planning-benchmark.md), [SOAM-038](tickets/SOAM-038-associative-skill-transfer.md) |
| 32 | [SOAM-031: Plan research on compositional dynamical motifs and learned pattern detectors](tickets/SOAM-031-compositional-dynamics-planning.md) | P2 | backlog | M5 | xhigh | [SOAM-052](tickets/SOAM-052-shared-population-gate.md) |
| 33 | [SOAM-016: Benchmark withheld compositions and transfer to related tasks](tickets/SOAM-016-composition-transfer.md) | P2 | backlog | M5 | xhigh | [SOAM-031](tickets/SOAM-031-compositional-dynamics-planning.md), [SOAM-037](tickets/SOAM-037-attention-belief-instances.md) |
| 34 | [SOAM-017: Test identity preservation and reusable temporal structure](tickets/SOAM-017-identity-timescales.md) | P2 | backlog | M5 | high | [SOAM-016](tickets/SOAM-016-composition-transfer.md) |
| 35 | [SOAM-018: Gate 5: assess compositional reuse rather than memory maintenance](tickets/SOAM-018-gate-5.md) | P2 | backlog | M5 | xhigh | [SOAM-017](tickets/SOAM-017-identity-timescales.md) |
| 36 | [SOAM-019: Build rendered observations and frozen encoder comparisons](tickets/SOAM-019-frozen-encoders.md) | P2 | ready | M6 | medium | [SOAM-002](tickets/SOAM-002-gate-1.md) |
| 37 | [SOAM-020: Train recurrent prediction and assimilation on rendered observations](tickets/SOAM-020-grounded-prediction.md) | P2 | backlog | M6 | high | [SOAM-019](tickets/SOAM-019-frozen-encoders.md), [SOAM-048](tickets/SOAM-048-platform-runner.md) |
| 38 | [SOAM-021: Evaluate partial observations, ambiguity, and context recovery](tickets/SOAM-021-partial-belief-recovery.md) | P2 | backlog | M6 | xhigh | [SOAM-020](tickets/SOAM-020-grounded-prediction.md), [SOAM-052](tickets/SOAM-052-shared-population-gate.md) |
| 39 | [SOAM-022: Gate 6: review sensory grounding and belief recovery](tickets/SOAM-022-gate-6.md) | P2 | backlog | M6 | high | [SOAM-021](tickets/SOAM-021-partial-belief-recovery.md) |
| 40 | [SOAM-011: Implement a bounded grounded evidence buffer and replay baseline](tickets/SOAM-011-evidence-and-replay.md) | P1 | backlog | M4 | high | [SOAM-044](tickets/SOAM-044-multicircuit-write-contract.md) |
| 41 | [SOAM-012: Validate consolidation candidates with shadow weights and rollback](tickets/SOAM-012-shadow-validation.md) | P1 | backlog | M4 | high | [SOAM-011](tickets/SOAM-011-evidence-and-replay.md) |
| 42 | [SOAM-042: Test overlapping assembly organization at fixed capacity](tickets/SOAM-042-fixed-capacity-organization.md) | P2 | backlog | M4 | xhigh | [SOAM-041](tickets/SOAM-041-multicircuit-acquisition-gate.md), [SOAM-052](tickets/SOAM-052-shared-population-gate.md) |
| 43 | [SOAM-043: Review fixed-capacity organization before continual integration](tickets/SOAM-043-organization-gate.md) | P2 | backlog | M4 | xhigh | [SOAM-042](tickets/SOAM-042-fixed-capacity-organization.md) |
| 44 | [SOAM-027: Integrate an extended continual embodied-learning benchmark](tickets/SOAM-027-continual-benchmark.md) | P2 | backlog | M8 | xhigh | [SOAM-018](tickets/SOAM-018-gate-5.md), [SOAM-022](tickets/SOAM-022-gate-6.md), [SOAM-026](tickets/SOAM-026-gate-7.md), [SOAM-041](tickets/SOAM-041-multicircuit-acquisition-gate.md), [SOAM-043](tickets/SOAM-043-organization-gate.md) |
| 45 | [SOAM-028: Review cumulative learning evidence and the next research cycle](tickets/SOAM-028-continual-review.md) | P2 | backlog | M8 | xhigh | [SOAM-027](tickets/SOAM-027-continual-benchmark.md) |
| 46 | [SOAM-035: Measure frozen v1 cue-driven handover controls](tickets/SOAM-035-cue-driven-handover.md) | P2 | ready | M1 | xhigh | [SOAM-034](tickets/SOAM-034-handover-harness.md) |
| 47 | [SOAM-036: Review frozen v1 handover evidence](tickets/SOAM-036-handover-gate.md) | P2 | backlog | M1 | xhigh | [SOAM-035](tickets/SOAM-035-cue-driven-handover.md) |
| 48 | [SOAM-004: Benchmark online transition correction and changed dynamics](tickets/SOAM-004-online-writer-baselines.md) | P2 | ready | M2 | high | [SOAM-003](tickets/SOAM-003-plastic-write-contract.md) |
| 49 | [SOAM-005: Measure interference and learning without resets](tickets/SOAM-005-interference-metrics.md) | P2 | backlog | M2 | high | [SOAM-004](tickets/SOAM-004-online-writer-baselines.md) |
| 50 | [SOAM-006: Gate 2: decide whether local acquisition is viable](tickets/SOAM-006-gate-2.md) | P2 | backlog | M2 | high | [SOAM-004](tickets/SOAM-004-online-writer-baselines.md), [SOAM-005](tickets/SOAM-005-interference-metrics.md) |
| 51 | [SOAM-007: Compare unfiltered, sparse, random, and sensitivity-based scopes](tickets/SOAM-007-heuristic-scopes.md) | P2 | backlog | M3 | high | [SOAM-006](tickets/SOAM-006-gate-2.md) |
| 52 | [SOAM-008: Build shared-scope and noisy-evidence task families](tickets/SOAM-008-scope-task-families.md) | P2 | backlog | M3 | high | [SOAM-007](tickets/SOAM-007-heuristic-scopes.md) |
| 53 | [SOAM-009: Meta-train a constrained functional scope translator](tickets/SOAM-009-learned-scope.md) | P2 | backlog | M3 | xhigh | [SOAM-008](tickets/SOAM-008-scope-task-families.md) |
| 54 | [SOAM-010: Gate 3: evaluate functional scoping and beneficial sharing](tickets/SOAM-010-gate-3.md) | P2 | backlog | M3 | high | [SOAM-009](tickets/SOAM-009-learned-scope.md) |
| 55 | [SOAM-013: Train a learned iterative low-rank consolidator](tickets/SOAM-013-learned-consolidator.md) | P3 | backlog | M4 | xhigh | [SOAM-010](tickets/SOAM-010-gate-3.md), [SOAM-012](tickets/SOAM-012-shadow-validation.md), [SOAM-041](tickets/SOAM-041-multicircuit-acquisition-gate.md) |
| 56 | [SOAM-014: Measure consolidation error recovery, compute, and fixed-size capacity](tickets/SOAM-014-consolidation-scaling.md) | P3 | backlog | M4 | high | [SOAM-013](tickets/SOAM-013-learned-consolidator.md) |
| 57 | [SOAM-015: Gate 4: decide whether learned consolidation adds value over replay](tickets/SOAM-015-gate-4.md) | P3 | backlog | M4 | high | [SOAM-014](tickets/SOAM-014-consolidation-scaling.md) |
| 58 | [SOAM-025: Learn goal-conditioned action proposals after search is reliable](tickets/SOAM-025-action-proposals.md) | P2 | backlog | M7 | high | [SOAM-024](tickets/SOAM-024-planning-benchmark.md) |
| 59 | [SOAM-029: Conditionally investigate flow-based consolidation](tickets/SOAM-029-optional-flow.md) | P3 | backlog | MX | xhigh | [SOAM-015](tickets/SOAM-015-gate-4.md) |
| 60 | [SOAM-030: Maintain a focused theory and literature evidence map](tickets/SOAM-030-theory-literature.md) | P2 | ready | MX | high | [SOAM-000](tickets/SOAM-000-substrate-baseline.md) |
| 61 | [SOAM-045: Explore recurrent attention within shared populations](tickets/SOAM-045-recurrent-attention-memories.md) | P2 | backlog | MX | xhigh | [SOAM-033](tickets/SOAM-033-handover-protocol.md), [SOAM-047](tickets/SOAM-047-platform-contract.md), [SOAM-059](tickets/SOAM-059-research-fork-selection.md) |

| 62 | [SOAM-062: Specify and select the Study A gating protocol](tickets/SOAM-062-study-a-protocol.md) | P0 | done | M1 | xhigh | [SOAM-047](tickets/SOAM-047-platform-contract.md), [SOAM-051](tickets/SOAM-051-shared-population-study.md) |
| 63 | [SOAM-063: Implement and verify Study A recurrences and diagnostics](tickets/SOAM-063-study-a-harness.md) | P0 | done | M1 | high | [SOAM-062](tickets/SOAM-062-study-a-protocol.md) |
| 64 | [SOAM-064: Measure adaptive gating under the frozen Study A protocol](tickets/SOAM-064-study-a-experiment.md) | P0 | done | M1 | high | [SOAM-062](tickets/SOAM-062-study-a-protocol.md), [SOAM-063](tickets/SOAM-063-study-a-harness.md) |
| 65 | [SOAM-065: Review Study A mechanisms and the smallest retained core](tickets/SOAM-065-study-a-decision.md) | P0 | done | M1 | xhigh | [SOAM-064](tickets/SOAM-064-study-a-experiment.md) |
| 66 | [SOAM-066: Specify and select temporal sensory assimilation](tickets/SOAM-066-study-b-protocol.md) | P0 | done | M1 | xhigh | [SOAM-047](tickets/SOAM-047-platform-contract.md), [SOAM-064](tickets/SOAM-064-study-a-experiment.md), [SOAM-065](tickets/SOAM-065-study-a-decision.md) |
| 67 | [SOAM-067: Implement and verify temporal assimilation comparisons](tickets/SOAM-067-study-b-harness.md) | P0 | in_progress | M1 | high | [SOAM-066](tickets/SOAM-066-study-b-protocol.md) |
| 68 | [SOAM-068: Measure temporal assimilation and settling under matched evidence](tickets/SOAM-068-study-b-experiment.md) | P0 | backlog | M1 | high | [SOAM-066](tickets/SOAM-066-study-b-protocol.md), [SOAM-067](tickets/SOAM-067-study-b-harness.md) |
| 69 | [SOAM-069: Review temporal assimilation and recommend the sensory motion interface](tickets/SOAM-069-study-b-decision.md) | P0 | backlog | M1 | xhigh | [SOAM-068](tickets/SOAM-068-study-b-experiment.md) |

## Housekeeping check

Run `uv run python scripts/check_tickets.py` before finishing ticket changes.
No remote issues are created by this tracker. Documents and software tests do not
establish attraction, sharing, learning, composition, or neuroscientific validity.
