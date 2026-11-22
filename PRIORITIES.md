# Priority and milestone tracker

**Current selection — November 22:** [Assembly organization and selective routing (AO-1)](docs/STUDY_ASSEMBLY_ORGANIZATION_PROTOCOL.md) is the sole selected path. SOAM-103/104 are done/proceed for planning/protocol; SOAM-105 is ready for implementation and resource preflight. SOAM-106/107 remain backlog. No AO-1 model fits have run. Earlier dated records below retain their historical meaning.

**November 21 E0-HOLD complete:** [SOAM-098–101](tickets/SOAM-101-e0-hold-decision.md) complete the paired follow-up. NAV32 stationary error improves 12.33° → 5.70°, but remains precisely above 5°; transverse-recovery noninferiority is unresolved. Formal result: **negative for the declared joint fix** (11/13 criteria pass). All 147 scientific fits complete, with 189 arrays/54 tensors reproduced exactly. [Report](reports/STUDY_E0_HOLD.md); [decision](reports/STUDY_E0_HOLD_DECISION.md). No successor is selected.

**November 21 E0 complete:** [SOAM-094–097](tickets/SOAM-097-e0-decision.md) complete the bounded single-population pilot. NAV32 passes six of seven criteria, but 128-step stationary pose error is 13.86° [12.12,16.28], above the 5° target; width 4.16° exceeds the frozen 4° cap, so the joint result is **inconclusive**. All 58 scientific fits complete; 108 arrays and 29 tensors repeat exactly. [Report](reports/STUDY_E0.md); [scoped decision](reports/STUDY_E0_DECISION.md). No successor is selected; coupling/hierarchy and historical gates remain unchanged.

Updated: 2026-11-22. The owner adopted the [v0.3 shared-population experiment
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
and the subsequent owner-selected Study B are complete. The owner-selected B2 is complete. The first bounded Study C experiment selected by the owner on November 14 is complete through SOAM-078–081.

## Current work and readiness

**November 22 protocol accepted:** [SOAM-104](tickets/SOAM-104-assembly-organization-protocol.md), P0/done, xhigh, accepts the [AO-1 protocol](docs/STUDY_ASSEMBLY_ORGANIZATION_PROTOCOL.md), [manifest](docs/protocols/study_ao1_v1.json) and [untrained design audit](docs/analysis/AO1_DESIGN_AUDIT.md). [SOAM-105](tickets/SOAM-105-assembly-organization-harness.md), P0/ready, high, is next for exact implementation, invariants and resource preflight. SOAM-106/107 remain backlog. The candidate learns with connection cost/activity regulation and dense fixed input; v1 has no hysteresis, prescribed entry neurons or tree. No scientific fits have run.

**Earlier November 22 retention design:** SOAM-102 remains done/proceed for E0-HYS design only. Its fixed-threshold contract is preserved, unrun and currently unselected; it is not a prerequisite for AO-1. Hysteresis is an optional mechanism in the new plan. E0-HOLD and all historical outcomes remain intact.

**2026-11-19 D-R2 complete:** SOAM-090/093 are done/proceed for the protocol and scoped inconclusive-evidence decision; SOAM-091/092 are done. Exact acquired-code accuracy 100%, PH768 cue-only accuracy 77.63%; gap +22.37 points [15.36,29.02], width 13.66 points exceeds the frozen ten-point cap: **inconclusive**. All 12 fits, 87 repeated arrays and 42 repeated tensors complete; KV remains the scoped reference. See the [report](reports/STUDY_D_R2.md), [decision](reports/STUDY_D_R2_DECISION.md), and [owner selection](docs/requests/retrieval_diagnostic_2026_11_19.md). No successor is selected; all historical gates remain unchanged.

**2026-11-18 D-R1 complete:** SOAM-086/089 are done/proceed for the frozen protocol and scoped evidence/reference decision; SOAM-087/088 are done. D-R1 is complete: PH768 adds 2.14 percentage points of recall through settling (adjusted interval 0.98–3.66), precisely below the five-point practical margin, and fails sequential-recall, retention and accepted-wrong guards. All 16 fits and ten confirmation roots complete; 5,497 repeated arrays match exactly. KV remains the scoped conventional reference; no next experiment is selected. [SOAM-089](tickets/SOAM-089-recurrent-retrieval-decision.md) recommends only a fresh retrieval/decoding diagnostic, without activating it. See the [report](reports/STUDY_D_R1.md) and [decision](reports/STUDY_D_R1_DECISION.md).

**Historical November 17 owner routing:** [SOAM-086](tickets/SOAM-086-recurrent-retrieval-protocol.md) was P0/ready, xhigh, for a fresh recurrent associative retrieval protocol. The motivation is a common recurrent substrate that could later support learned specialization and adaptive organization; neither is demonstrated. D0–D2 remain complete, D3/D4 and E0/F remain deferred, and no new numerical study was then running. This owner selection follows the completed D decision rather than revising it.

**2026-11-17: Study D D0–D2 complete (SOAM-082–085).** Explicit key-value memory passes the post-reset acquisition and retention criteria. All writers learn isolated objects, but regression and the tested rank-one FAST memory exceed the sequential-interference guard; FAST has a precise negative practical-benefit result against both conventional controls. All 16 fits and 88 model evaluations complete, 64 repeat arrays match exactly, and 303 tests pass. The decision retains KV for this scaffolded task only. D3/D4 remain deferred; no next experiment or historical gate change is selected. See the [report](reports/STUDY_D.md) and [decision](reports/STUDY_D_DECISION.md).

**Study C complete, November 14.** SOAM-078 and SOAM-081 are done/proceed for the [C-H1 protocol](docs/STUDY_C_PROTOCOL.md) and [scoped result/reference decision](reports/STUDY_C_DECISION.md); SOAM-079/080 are done. The [report](reports/STUDY_C.md) supports TWO16 over both neural single-state controls, while conventional retained multiplicity falls precisely below the declared practical benefit. ADAPT1-C is the compact conventional reference; TWO16 is the faster recurrent alternative. All 67 fits, ten confirmation roots and 1,530 exact repeated arrays complete; 285 tests pass. Coherent-cause overconfidence remains unresolved. Scheduling, complementary objects and learned allocation stay conditional. No next experiment is selected; historical gates remain unchanged.

**Study B2 complete, November 12.** SOAM-074–077 deliver [robust Kalman correction](reports/STUDY_B2.md). ADAPT1 and empirical NIS pass the frozen benefit/guard criteria; coherent corruption and measured inference latency remain limitations. [SOAM-077](reports/STUDY_B2_DECISION.md) recommends ADAPT1/NISEMP conventional references and hands off baselines only. C/D/E remain future conditional studies; F remains a future planning track. No new fork is selected.


**Study B complete, November 11.** SOAM-066–068 deliver v1's measured gating tradeoff; SOAM-069 preserves revise for the missing magnitude-input comparison. SOAM-070–072 complete the fresh magnitude supplement: negative practical advantage, with the adjusted intervals excluding the declared 10% gain. SOAM-073 is done/proceed for the [separate-correction interface recommendation](reports/STUDY_B_DECISION.md) only. All 368 fits and 108 repeat checks complete; 238 tests pass. Numerical use is 1422.60 CPU / 1422.72 execution wall seconds, 0.822 GiB RSS and 0.517 GiB artifacts, below the accepted 7200/14400 seconds and 2 GiB limits. Acquisition and all other forks remain unselected.

**November 11: Study A complete.** SOAM-062 done/proceed, SOAM-063/064 done, and SOAM-065 done/proceed for the [R32 core recommendation](reports/STUDY_A_DECISION.md) only. The [scientific result](reports/STUDY_A.md) is inconclusive for the frozen practical adaptive-update claim. All 120 confirmation fits and 12 prescribed repeats completed within the cumulative ceiling; 215 tests pass. Study B is separately completed below; SOAM-039 remains backlog pending fresh routing. Historical E1 evidence and SOAM-052 stop remain unchanged.


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
| M1 | Shared populations and recurrent dynamics | SOAM-049–052 test one sharing benefit with interference guardrails and explicit T32 claim limits; SOAM-059 selects the next fork | E1 harness delivered; v1 storage failure preserved; SOAM-061 A1 proceed; 119 fits/27,820 cells complete; absolute recall failure, exact repeat; SOAM-052 done/stop for tested useful sharing; dependent integration unready; Study A complete/inconclusive practical update benefit; SOAM-065 proceeds with R32 reference recommendation only; Study B complete: v1 tradeoff, magnitude negative practical advantage; SOAM-073 accepts separate-correction interface only; B2 complete with bounded robust-correction benefit and coherent/runtime limits; SOAM-077 recommends references only; Study C complete: supported neural factorization benefit, conventional practical multiplicity negative, unresolved coherent-cause overconfidence; SOAM-081 accepts scoped references only; E0 SOAM-094–097 complete: NAV32 six criteria pass, stationary drift imprecise and unfavorable; joint inconclusive; E0-HOLD SOAM-098–101 complete: substantial drift improvement, precise residual-drift failure and unresolved recovery margin; SOAM-102 E0-HYS retained unrun/unselected; SOAM-103/104 done/proceed for AO-1 scope/protocol; untrained algebra checks pass; SOAM-105 ready, SOAM-106/107 backlog; no model implementation or scientific fits |
| M2 | Grounded acquisition | Early E2 through SOAM-039/044/040/041: few-observation learning with retained generalization; no skill/concurrency/replay-stack prerequisite | Study D SOAM-082–085 complete: KV passes bounded acquisition/retention; REG/FAST interference, FAST precise negative practical advantage; historical writer/E2 preserved; D3/D4 deferred; D-R1 SOAM-086–089 complete: PH768 precise negative practical-settling benefit and three established reliability failures; scoped KV reference retained; D-R2 SOAM-090–093 complete, precision-qualified inconclusive diagnosis accepted; no successor selected |
| M3 | Conditional functional scopes | SOAM-007–010; limited interference with beneficial sharing | Deferred comparison branch |
| M4 | Replay and overlapping organization | SOAM-011/012, SOAM-042/043 at fixed capacity; optional SOAM-013–015 | Planned; learned refinement conditional |
| M5 | Compositional reuse | SOAM-031, SOAM-016–018; held-out feature/relation/action reuse and identity | Planned after shared-population evidence |
| M6 | Grounding and independent applications | E3 active disambiguation SOAM-053–055; later SOAM-037/019–022 and module SOAM-056–058 after acquisition | Conditional alternatives awaiting named fork selection, contract/runner, and own decisions |
| M7 | Control and shared action relations | SOAM-023/024/038/026; optional SOAM-025 | Planned after supported shared beliefs/handover |
| M8 | Continual embodied integration | SOAM-027/028 require composition, grounding, control, acquisition, organization outcomes | Planned; application success alone does not pass integration gates |
| MX | Scope and supporting research | SOAM-046 adoption and SOAM-060 review; SOAM-030 evidence map; SOAM-045 optional recurrent attention; SOAM-029 optional flow | SOAM-059 routing preserved; Study A delivered under owner override; Study B/B2/C complete under SOAM-066–081; Study D complete through SOAM-082–085; D-R1 SOAM-086–089 complete with scoped negative evidence and KV reference; D-R2 diagnostic complete/inconclusive; E0 complete/inconclusive; E0-HOLD complete/negative joint fix; SOAM-102 E0-HYS retained unrun/unselected; SOAM-103/104 done/proceed for AO-1 scope/protocol; untrained algebra checks pass; SOAM-105 ready, SOAM-106/107 backlog; no model implementation or scientific fits |

## Execution paths and dependency changes

Current selected path: **SOAM-103 → SOAM-104 → SOAM-105 → SOAM-106 → SOAM-107**. Scope and protocol decisions are complete. SOAM-105 is the sole next eligible task: implement the accepted contract and verify the full-inventory resource projection before scientific fitting. Lean is optional; E0-HYS is unselected. This narrow offline pilot leaves SOAM-042/043 integration gates unchanged.

Primary path: SOAM-047 minimum contract → SOAM-049 minimal benefit protocol;
SOAM-048 runner + SOAM-049 → SOAM-050 → SOAM-061 corrective feasibility decision → SOAM-051. The pilot measures one primary
benefit of sharing with recall/interference guardrails and is now complete with a
negative gate. The subsequent Study A diagnostic is complete; acquisition, concurrent
handover and broad backend work remain deferred.

SOAM-052 completed the scientific review with stop; its failed gate remains intact.
SOAM-059 is historically done/proceed for **E2 via SOAM-039** using ordinary G32
under the [bounded branch record](reports/RESEARCH_FORK_SELECTION.md). The owner
selected Study A instead; its completed SOAM-065 decision recommends R32 without
itself activating another experiment. The later owner request and SOAM-066 selected Study B alone; its completed SOAM-073 decision selects no subsequent experiment. SOAM-039/044/040/041 remain backlog pending fresh
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
| 67 | [SOAM-067: Implement and verify temporal assimilation comparisons](tickets/SOAM-067-study-b-harness.md) | P0 | done | M1 | high | [SOAM-066](tickets/SOAM-066-study-b-protocol.md) |
| 68 | [SOAM-068: Measure temporal assimilation and settling under matched evidence](tickets/SOAM-068-study-b-experiment.md) | P0 | done | M1 | high | [SOAM-066](tickets/SOAM-066-study-b-protocol.md), [SOAM-067](tickets/SOAM-067-study-b-harness.md) |
| 69 | [SOAM-069: Review temporal assimilation and recommend the sensory motion interface](tickets/SOAM-069-study-b-decision.md) | P0 | done | M1 | xhigh | [SOAM-068](tickets/SOAM-068-study-b-experiment.md) |
| 70 | [SOAM-070: Specify the magnitude-sensitive sensory gain supplement](tickets/SOAM-070-study-b-magnitude-protocol.md) | P0 | done | M1 | xhigh | [SOAM-068](tickets/SOAM-068-study-b-experiment.md) |
| 71 | [SOAM-071: Implement magnitude inputs for sensory and motion gain](tickets/SOAM-071-study-b-magnitude-harness.md) | P0 | done | M1 | high | [SOAM-070](tickets/SOAM-070-study-b-magnitude-protocol.md) |
| 72 | [SOAM-072: Measure magnitude-sensitive correction on fresh streams](tickets/SOAM-072-study-b-magnitude-experiment.md) | P0 | done | M1 | high | [SOAM-070](tickets/SOAM-070-study-b-magnitude-protocol.md), [SOAM-071](tickets/SOAM-071-study-b-magnitude-harness.md) |
| 73 | [SOAM-073: Review both Study B versions and select the inference interface](tickets/SOAM-073-study-b-interface-decision.md) | P0 | done | M1 | xhigh | [SOAM-068](tickets/SOAM-068-study-b-experiment.md), [SOAM-072](tickets/SOAM-072-study-b-magnitude-experiment.md) |

| 74 | [SOAM-074: Specify and select robust Kalman correction](tickets/SOAM-074-study-b2-protocol.md) | P0 | done | M1 | xhigh | [SOAM-073](tickets/SOAM-073-study-b-interface-decision.md) |

| 75 | [SOAM-075: Implement and verify robust correction and corruption controls](tickets/SOAM-075-study-b2-harness.md) | P0 | done | M1 | high | [SOAM-074](tickets/SOAM-074-study-b2-protocol.md) |

| 76 | [SOAM-076: Screen and confirm bounded robust Kalman correctors](tickets/SOAM-076-study-b2-experiment.md) | P0 | done | M1 | high | [SOAM-074](tickets/SOAM-074-study-b2-protocol.md), [SOAM-075](tickets/SOAM-075-study-b2-harness.md) |

| 77 | [SOAM-077: Review robust estimation and prepare the Study C baseline handoff](tickets/SOAM-077-study-b2-decision.md) | P0 | done | M1 | xhigh | [SOAM-076](tickets/SOAM-076-study-b2-experiment.md) |

| 78 | [SOAM-078: Specify hypothesis preservation under genuine ambiguity](tickets/SOAM-078-study-c-protocol.md) | P0 | done | M1 | xhigh | [SOAM-077](tickets/SOAM-077-study-b2-decision.md) |
| 79 | [SOAM-079: Implement and verify the two-candidate inference comparison](tickets/SOAM-079-study-c-harness.md) | P0 | done | M1 | high | [SOAM-078](tickets/SOAM-078-study-c-protocol.md) |
| 80 | [SOAM-080: Measure explicit candidate states on fresh ambiguity streams](tickets/SOAM-080-study-c-experiment.md) | P0 | done | M1 | high | [SOAM-078](tickets/SOAM-078-study-c-protocol.md), [SOAM-079](tickets/SOAM-079-study-c-harness.md) |
| 81 | [SOAM-081: Review candidate-state benefit and conditional scheduling](tickets/SOAM-081-study-c-decision.md) | P0 | done | M1 | xhigh | [SOAM-080](tickets/SOAM-080-study-c-experiment.md) |

| 82 | [SOAM-082: Specify and select post-reset persistent acquisition](tickets/SOAM-082-study-d-protocol.md) | P0 | done | M2 | xhigh | [SOAM-047](tickets/SOAM-047-platform-contract.md), [SOAM-081](tickets/SOAM-081-study-c-decision.md) |

| 83 | [SOAM-083: Implement and verify bounded persistent memory controls](tickets/SOAM-083-study-d-harness.md) | P0 | done | M2 | high | [SOAM-082](tickets/SOAM-082-study-d-protocol.md) |

| 84 | [SOAM-084: Measure post-reset acquisition and sequential retention](tickets/SOAM-084-study-d-experiment.md) | P0 | done | M2 | high | [SOAM-082](tickets/SOAM-082-study-d-protocol.md), [SOAM-083](tickets/SOAM-083-study-d-harness.md) |

| 85 | [SOAM-085: Review persistent memory benefit and cheapest reliable mechanism](tickets/SOAM-085-study-d-decision.md) | P0 | done | M2 | xhigh | [SOAM-084](tickets/SOAM-084-study-d-experiment.md) |

| 86 | [SOAM-086: Specify a bounded recurrent associative retrieval pilot](tickets/SOAM-086-recurrent-retrieval-protocol.md) | P0 | done | M2 | xhigh | [SOAM-047](tickets/SOAM-047-platform-contract.md), [SOAM-085](tickets/SOAM-085-study-d-decision.md) |
| 87 | [SOAM-087: Implement and verify the bounded D-R1 retrieval harness](tickets/SOAM-087-recurrent-retrieval-harness.md) | P0 | done | M2 | high | [SOAM-086](tickets/SOAM-086-recurrent-retrieval-protocol.md) |
| 88 | [SOAM-088: Execute the frozen D-R1 acquisition and settling study](tickets/SOAM-088-recurrent-retrieval-study.md) | P0 | done | M2 | high | [SOAM-086](tickets/SOAM-086-recurrent-retrieval-protocol.md), [SOAM-087](tickets/SOAM-087-recurrent-retrieval-harness.md) |

| 89 | [SOAM-089: Review recurrent retrieval reliability and added settling benefit](tickets/SOAM-089-recurrent-retrieval-decision.md) | P0 | done | M2 | xhigh | [SOAM-088](tickets/SOAM-088-recurrent-retrieval-study.md) |

| 90 | [SOAM-090: Specify and select the fixed retrieval-versus-decoding diagnostic](tickets/SOAM-090-retrieval-decoding-protocol.md) | P0 | done | M2 | xhigh | [SOAM-089](tickets/SOAM-089-recurrent-retrieval-decision.md) |
| 91 | [SOAM-091: Implement and verify the evaluator-only decoding diagnostic](tickets/SOAM-091-retrieval-decoding-harness.md) | P0 | done | M2 | high | [SOAM-090](tickets/SOAM-090-retrieval-decoding-protocol.md) |
| 92 | [SOAM-092: Execute the fixed retrieval-versus-decoding diagnostic](tickets/SOAM-092-retrieval-decoding-study.md) | P0 | done | M2 | high | [SOAM-090](tickets/SOAM-090-retrieval-decoding-protocol.md), [SOAM-091](tickets/SOAM-091-retrieval-decoding-harness.md) |
| 93 | [SOAM-093: Review the retrieval-versus-decoding diagnosis](tickets/SOAM-093-retrieval-decoding-decision.md) | P0 | done | M2 | xhigh | [SOAM-092](tickets/SOAM-092-retrieval-decoding-study.md) |
| 94 | [SOAM-094: Select and freeze the single-population E0 pilot](tickets/SOAM-094-e0-protocol.md) | P0 | done | M1 | xhigh | [SOAM-093](tickets/SOAM-093-retrieval-decoding-decision.md) |
| 95 | [SOAM-095: Implement and verify the E0 navigation harness](tickets/SOAM-095-e0-harness.md) | P0 | done | M1 | high | [SOAM-094](tickets/SOAM-094-e0-protocol.md) |
| 96 | [SOAM-096: Execute the bounded E0 navigation pilot](tickets/SOAM-096-e0-study.md) | P0 | done | M1 | high | [SOAM-094](tickets/SOAM-094-e0-protocol.md), [SOAM-095](tickets/SOAM-095-e0-harness.md) |
| 97 | [SOAM-097: Review E0 navigation and local recovery evidence](tickets/SOAM-097-e0-decision.md) | P0 | done | M1 | xhigh | [SOAM-096](tickets/SOAM-096-e0-study.md) |
| 98 | [SOAM-098: Freeze the longer zero-action E0 follow-up](tickets/SOAM-098-e0-hold-protocol.md) | P0 | done | M1 | xhigh | [SOAM-097](tickets/SOAM-097-e0-decision.md) |
| 99 | [SOAM-099: Implement the paired stationary-horizon comparison](tickets/SOAM-099-e0-hold-harness.md) | P0 | done | M1 | high | [SOAM-098](tickets/SOAM-098-e0-hold-protocol.md) |
| 100 | [SOAM-100: Execute the frozen longer stationary-training study](tickets/SOAM-100-e0-hold-study.md) | P0 | done | M1 | high | [SOAM-098](tickets/SOAM-098-e0-hold-protocol.md), [SOAM-099](tickets/SOAM-099-e0-hold-harness.md) |
| 101 | [SOAM-101: Review stationary drift improvement and navigation guardrails](tickets/SOAM-101-e0-hold-decision.md) | P0 | done | M1 | xhigh | [SOAM-100](tickets/SOAM-100-e0-hold-study.md) |

| 102 | [SOAM-102: Design the state hysteresis and navigability experiment](tickets/SOAM-102-state-hysteresis-protocol.md) | P0 | done | M1 | xhigh | [SOAM-101](tickets/SOAM-101-e0-hold-decision.md) |
| 103 | [SOAM-103: Select the assembly organization and selective routing plan](tickets/SOAM-103-assembly-organization-plan.md) | P0 | done | M1 | xhigh | [SOAM-102](tickets/SOAM-102-state-hysteresis-protocol.md) |

| 104 | [SOAM-104: Specify assembly organization dynamics and freeze the bounded pilot](tickets/SOAM-104-assembly-organization-protocol.md) | P0 | done | M1 | xhigh | [SOAM-103](tickets/SOAM-103-assembly-organization-plan.md) |
| 105 | [SOAM-105: Implement and verify the assembly organization pilot harness](tickets/SOAM-105-assembly-organization-harness.md) | P0 | ready | M1 | high | [SOAM-104](tickets/SOAM-104-assembly-organization-protocol.md) |
| 106 | [SOAM-106: Execute the bounded assembly organization and routing pilot](tickets/SOAM-106-assembly-organization-study.md) | P0 | backlog | M1 | high | [SOAM-104](tickets/SOAM-104-assembly-organization-protocol.md), [SOAM-105](tickets/SOAM-105-assembly-organization-harness.md) |
| 107 | [SOAM-107: Review selective routing evidence and memory stability trade-offs](tickets/SOAM-107-assembly-organization-decision.md) | P0 | backlog | M1 | xhigh | [SOAM-106](tickets/SOAM-106-assembly-organization-study.md) |

## Housekeeping check

Run `uv run python scripts/check_tickets.py` before finishing ticket changes.
No remote issues are created by this tracker. Documents and software tests do not
establish attraction, sharing, learning, composition, or neuroscientific validity.
