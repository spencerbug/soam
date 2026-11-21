# SOAM — Self-Organizing Attractor Memory

**November 21 E0-HOLD complete:** [SOAM-098–101](tickets/SOAM-101-e0-hold-decision.md) complete the paired follow-up. NAV32 stationary error improves 12.33° → 5.70°, but remains precisely above 5°; transverse-recovery noninferiority is unresolved. Formal result: **negative for the declared joint fix** (11/13 criteria pass). All 147 scientific fits complete, with 189 arrays/54 tensors reproduced exactly. [Report](reports/STUDY_E0_HOLD.md); [decision](reports/STUDY_E0_HOLD_DECISION.md). No successor is selected.

**November 21 E0 complete:** [SOAM-094–097](tickets/SOAM-097-e0-decision.md) complete the bounded single-population pilot. NAV32 passes six of seven criteria, but 128-step stationary pose error is 13.86° [12.12,16.28], above the 5° target; width 4.16° exceeds the frozen 4° cap, so the joint result is **inconclusive**. All 58 scientific fits complete; 108 arrays and 29 tensors repeat exactly. [Report](reports/STUDY_E0.md); [scoped decision](reports/STUDY_E0_DECISION.md). No successor is selected; coupling/hierarchy and historical gates remain unchanged.

**November 19 D-R2 complete:** Exact acquired-code decoding scored 100% in the sample; ordinary PH768 recall scored 77.63%. The +22.37-point gap has adjusted interval [15.36,29.02], wider than the frozen ten-point precision cap: formal diagnosis **inconclusive**. All 12 fits and exact repeat complete. [Report](reports/STUDY_D_R2.md); [scoped decision](reports/STUDY_D_R2_DECISION.md). SOAM-090–093 are complete; no successor is selected.

**November 18 completion:** D-R1 is complete: PH768 adds 2.14 percentage points of recall through settling (adjusted interval 0.98–3.66), precisely below the five-point practical margin, and fails sequential-recall, retention and accepted-wrong guards. All 16 fits and ten confirmation roots complete; 5,497 repeated arrays match exactly. KV remains the scoped conventional reference; no next experiment is selected. See the [report](reports/STUDY_D_R1.md) and [decision](reports/STUDY_D_R1_DECISION.md).

Research repository and planned experiment platform for Hopfield networks and
related recurrent dynamical systems. The preferred hypothesis uses overlapping
neurons for features, relationships, and action relations, with separated networks
as controls. Useful sharing, attraction, and learned organization remain unproven.

The [north star](docs/NORTH_STAR.md), clarified on November 19, 2026, centers the
long-term goal on self-developed sensorimotor world models, learning through play,
and continually learned memory organization. Language may follow grounded understanding;
alignment with human representations is an empirical question.

The adopted [v0.3 research specification](docs/RESEARCH_SPEC_V0_3.md), dated November 5,
2026, broadens the program to reusable experiments, including NeuroSLAM-inspired
localization and Monty-style sensorimotor learning modules with recurrent memory.
The [v0.2 scope](docs/RESEARCH_SPEC_V0_2.md), [v0.1 specification](docs/RESEARCH_SPEC.md),
and completed contracts/results retain their historical meanings. The v1 handover
harness, platform fixture runner and E1 engineering harness are implemented.
The initial E1 storage check failed; the A1 correction passed. The completed E1 study
records absolute recall failure for S32, with both relative retention guardrails passing.

The [conditional research paths](docs/RESEARCH_PATHS.md) govern follow-ups: first
measure one benefit of sharing, then select one experimental fork from the results.
Concurrency/handover and the two application studies are conditional extensions.

The [scientific assessment](docs/SCIENTIFIC_REVIEW_2026_11_05.md) treats SOAM as a
plausible mechanism research programme. Sensorimotor intelligence remains a long-term
goal rather than a supported claim. The three questions identified in that review are
useful shared dynamics, rapid retained acquisition, and active disambiguation.
See the [hypothesis ledger](docs/HYPOTHESES.md) and [ticket change map](docs/TICKET_REVIEW_2026_11_05.md).

Study B2 artifacts: [protocol](docs/STUDY_B2_PROTOCOL.md), [FILTER2 audit](reports/STUDY_B2_FILTER_AUDIT.md), [development](reports/STUDY_B2_DEVELOPMENT.md), [full tables](reports/study-b2/tables.md), [Pareto plot](reports/study-b2/pareto.png), [decision and C handoff](reports/STUDY_B2_DECISION.md).

## Current milestone

**E0-HOLD (SOAM-098–101) is complete:** longer stationary training reduces NAV32 drift substantially, but the declared joint fix fails on residual error and leaves recovery noninferiority unresolved. The [report](reports/STUDY_E0_HOLD.md) and [decision](reports/STUDY_E0_HOLD_DECISION.md) preserve the result; no successor is selected.

**2026-11-18 D-R1 complete:** [SOAM-086](tickets/SOAM-086-recurrent-retrieval-protocol.md) accepted the [frozen protocol](docs/STUDY_D_R1_PROTOCOL.md); [SOAM-087](tickets/SOAM-087-recurrent-retrieval-harness.md) verified the harness; [SOAM-088](tickets/SOAM-088-recurrent-retrieval-study.md) completed the study. [SOAM-089](tickets/SOAM-089-recurrent-retrieval-decision.md) accepts its scoped negative practical-settling result and reliability failures. Stored-code preservation is distinct from correct cue-driven completion. The single next recommendation is a fresh retrieval/decoding diagnostic, not an activated fork. Historical gates remain unchanged.

**Historical 2026-11-18 handoff:** [Study D-R1: Recurrent associative retrieval](docs/proposed-studies/STUDY_D_R1_RECURRENT_RETRIEVAL.md) is the execution prompt for the selected follow-up under SOAM-086. It reuses D1/D2-style questions while testing actual nonlinear settling; protocol acceptance and a fresh numerical allocation were then pending.

**Historical November 17 owner routing:** [SOAM-086](tickets/SOAM-086-recurrent-retrieval-protocol.md) was P0/ready, xhigh, for a fresh recurrent associative retrieval protocol. The motivation is a common recurrent substrate that could later support learned specialization and adaptive organization; neither is demonstrated. D0–D2 remain complete, D3/D4 and E0/F remain deferred, and no new numerical study was then running. This owner selection follows the completed D decision rather than revising it.

**2026-11-17: Study D D0–D2 complete (SOAM-082–085).** Explicit key-value memory passes the post-reset acquisition and retention criteria. All writers learn isolated objects, but regression and the tested rank-one FAST memory exceed the sequential-interference guard; FAST has a precise negative practical-benefit result against both conventional controls. All 16 fits and 88 model evaluations complete, 64 repeat arrays match exactly, and 303 tests pass. The decision retains KV for this scaffolded task only. D3/D4 remain deferred; no next experiment or historical gate change is selected.

Study D: [report](reports/STUDY_D.md), [decision](reports/STUDY_D_DECISION.md), [protocol](docs/STUDY_D_PROTOCOL.md), [paired results and resources](reports/study-d/tables.md).

Published November 19: [Joint D-R1/D-R2 article](https://spencerbug.github.io/blog/soam-retrieval-and-decoding/) and [companion report](https://spencerbug.github.io/research/soam-retrieval-and-decoding/), site commit `3c0b272`. They distinguish code preservation, cue-driven retrieval and decoding, preserving D-R1's negative practical-settling result and D-R2's inconclusive diagnosis. See the [publication record](reports/STUDY_D_RETRIEVAL_PUBLICATION.md).

Published November 17: [Study D article](https://spencerbug.github.io/blog/soam-study-d-acquisition-and-retention/) and [companion report](https://spencerbug.github.io/research/soam-study-d/), site commits `5e8faf2` / `ed749bd`. They explain the measured retention failure and the separately selected recurrent-retrieval direction. Source/data downloads await separate publication authorization; the frozen study and historical decisions remain unchanged. See the [publication record](reports/STUDY_D_PUBLICATION.md).

**2026-11-14: Study C C-H1 complete (SOAM-078–081).** The [report](reports/STUDY_C.md) supports two recurrent candidate states over PC16 and the larger single-state PC32 control. Conventional retained multiplicity has a small benefit precisely below the declared practical margin. The [decision](reports/STUDY_C_DECISION.md) retains ADAPT1-C as the compact conventional reference and TWO16 as the faster recurrent alternative. All 67 fits and ten confirmation roots completed; 1,530 repeated arrays match exactly; 285 tests pass. Coherent-fault/genuine-change cause ambiguity remains overconfident. Scheduling, complementary objects and learned allocation remain conditional; no next experiment is selected and historical gates are preserved.

Published November 14: [Study C visual article](https://spencerbug.github.io/blog/soam-study-c-hypothesis-preservation/) and [companion report with evidence downloads](https://spencerbug.github.io/research/soam-study-c/). The site publication is commit `fd5e0a7`; the frozen study snapshot and historical gate decisions remain unchanged.

**2026-11-12: Study B2 complete (SOAM-074–077).** [Robust Kalman correction](reports/STUDY_B2.md) supports bounded channel-disagreement covariance adaptation and empirical NIS gating. ADAPT1 improves balanced corruption by 52.69% with all frozen accuracy guards passing, while coherent plausible corruption remains unresolved and measured Torch latency is slower than PC16. The [decision/C handoff](reports/STUDY_B2_DECISION.md) recommends conventional references only. Study C/D/E stay conditional; F stays a future planning track. Historical A/B and E1 decisions remain unchanged.



**2026-11-11: Studies A and B complete (SOAM-062–073).** [Study A](reports/STUDY_A.md) retains its inconclusive practical adaptive-update result and [R32 recommendation](reports/STUDY_A_DECISION.md). [Study B](reports/STUDY_B.md) completes 368 fits and 108 exact repeat checks; 238 tests pass. V1 shows a gating tradeoff; the fresh magnitude supplement precisely excludes the declared 10% practical gain. The [final decision](reports/STUDY_B_DECISION.md) recommends separate correction with PC16 as the small robust neural reference and a fitted filter as the accuracy/resource reference with a corruption failure. Optional settling and independent gain channels are retained without requiring learned gates. The subsequent owner request selected [Study B2](docs/STUDY_B2_PROTOCOL.md) through SOAM-074–077 before conditional Study C. SOAM-039 remains backlog; historical E1 evidence and SOAM-052 stop remain unchanged.


Historical [SOAM-052](tickets/SOAM-052-shared-population-gate.md)
is complete with **stop** for E1 v1 S32's tested useful-sharing claim. The
[gate review](reports/SHARED_POPULATION_GATE.md) audits validity, information parity,
resources and uncertainty before applying absolute recall failure. Both relative
retention guards pass; GRUs have lower primary error, causal precision is unresolved,
and T32 prevents a uniquely physical-overlap performance claim. Recovery usefulness
criteria also fail, separately. This does not reject shared recurrence generally.
The [full study](reports/SHARED_POPULATION_STUDY.md) preserves 119 fits/27,820 cells,
exact reproduction and all source/selections/resources. All 190 tests pass.
Sharing-dependent integration remains unready. [SOAM-059](reports/RESEARCH_FORK_SELECTION.md)
historically selected E2 protocol design with G32 and a bounded writer. The owner
superseded that current selection with Study A, preserving SOAM-059's decision
and allocation history. SOAM-039/044/040/041 remain backlog; no E2 protocol or
implementation has been approved. Any later branch needs fresh routing.

Study A adds [tested recurrence variants and execution history](reports/STUDY_A_IMPLEMENTATION.md),
a [versioned frozen protocol](docs/STUDY_A_PROTOCOL_V2.md), [root tables and intervals](reports/study-a/tables.md),
gate/state/recovery plots and historical phase-drift analysis. All 120 new
confirmation fits and the 12-model prescribed repeat completed, within the owner
ceiling; its completed suite had 215 passing tests. Its inconclusive mechanism
claim does not alter the historical negative sharing gate.

Sharing refers to recurrent neurons and connections, not just tied parameters or
three independent networks stored in one tensor. Test overlap, binding, interference,
and directional dynamics while keeping evidence, goals, motor authority, transient
state, and persistent memory distinguishable. Preserve separated-state controls and
accept negative results. See the [ordered ticket queue](PRIORITIES.md).

SOAM-033/034 delivered the frozen [handover protocol](docs/HANDOVER_PROTOCOL.md),
[numerical manifest](docs/protocols/handover_v1.json), and [harness](docs/HANDOVER_HARNESS.md).
The [engineering report](reports/HANDOVER_HARNESS.md) records fixture-only verification.
SOAM-035 remains ready as a P2 comparison branch; no measured v0.2 study has run.
E1 confirmation is complete, but no handover/shared-population gate has passed.

The delivered Stage 0/substrate work (WP-00/WP-01) covers synthetic action-conditioned 2D
regimes, a fixed sensory projection, shared bounded recurrent baselines, independent
predictors, shared-state switching, independent-model handoffs, and perturbation diagnostics.
The bounded local-write contract is implemented; acquisition comparisons, learned
scopes, consolidation, JEPA, and planning remain future work.

See [experiment protocol](docs/EXPERIMENTS.md), [work packages](docs/ROADMAP.md),
[architecture boundaries](docs/ARCHITECTURE.md), [initial report](reports/BASELINE.md),
[controls report](reports/SUBSTRATE_CONTROLS.md), and [current writer report](reports/LOCAL_WRITE_CONTRACT.md).
The remaining work is organized in the [priority and milestone tracker](PRIORITIES.md)
and [issue backlog](tickets/README.md), with GitHub-ready templates and ticket conventions.

The [stronger six-model controls](reports/SUBSTRATE_CONTROLS.md) are complete:
17 of 18 trials pass the preregistered screen, with an additive seed-23 failure on
irregular switches. GRU and fully independent controls pass all three seeds. All
six seed-11 repeats match exactly. Long-horizon drift remains; these results do not
establish self-organization. [Gate 1](reports/GATE_1_REVIEW.md) proceeds with the
low-rank substrate and GRU reference. SOAM-003 now provides bounded grounded writes,
read-only prediction snapshots, and exact rollback. All 48 tests pass. A three-seed
contract demonstration reproduces exactly but includes multistep regressions; it does
not establish H2. SOAM-004 remains ready on a separate writer comparison branch;
it is no longer the next primary task. The reported 48-test result belongs to that
implementation; documentation changes do not constitute a new experiment.
The original four-model benchmark remains preserved as historical evidence.

## Run

```sh
uv sync --extra dev --locked
uv run pytest
uv run soam-run --config configs/smoke.json --output runs/smoke
uv run soam-run --config configs/substrate.json --output runs/substrate
uv run soam-compare runs/substrate --output reports/substrate-comparison.md
uv run soam-handover-smoke --output runs/my-handover-fixture
uv run soam-platform-fixture --output runs/my-platform-fixture
uv run python -m soam.shared.runner --output runs/my-shared-fixture
```

CPU and one Torch thread are the reproducible reference. Run directories refuse
overwrite and contain resolved config, source/version provenance, checkpoints,
per-seed metrics, training traces, and diagnostic PNGs. Numerical results should
repeat on the same software/hardware; wall times are expected to vary. `uv.lock`
pins dependencies. The smoke configuration exercises the pipeline; it is not
evidence for H1. Tracked compact results are in `reports/`; larger artifacts are in `runs/`.

To check a full-length repeat of seed 11 (choose unused output paths):

```sh
uv run soam-run --config configs/substrate.json --seeds 11 --output runs/my-repeat
uv run python scripts/check_reproduction.py runs/substrate runs/my-repeat
```

## Research discipline

Ordinary RNNs here are baselines. Bounded activity does not establish attractor
recovery; shared weights do not establish reusable primitives. H1 remains
provisional until prediction, switching, stability, and budget comparisons are
examined. Transfer/composition belong to H5. Ground truth is used by the simulator
and diagnostics, never supplied to the recurrent transition during evaluation.

This local repository is independent of `geometric-recurrent-memory`. No remote
hosting or publication is required for these experiments.
