# SOAM post-C research proposals (2026-11-16)

**November 18 completion:** D-R1 is complete: PH768 adds 2.14 percentage points of recall through settling (adjusted interval 0.98–3.66), precisely below the five-point practical margin, and fails sequential-recall, retention and accepted-wrong guards. All 16 fits and ten confirmation roots complete; 5,497 repeated arrays match exactly. KV remains the scoped conventional reference; no next experiment is selected. See the [report](../../reports/STUDY_D_R1.md) and [decision](../../reports/STUDY_D_R1_DECISION.md).

**Status: proposed Codex prompts, not approved protocols or completed experiments.** This directory captures the next research directions after completed Studies A, B, B2, and C. Execute only the next explicitly selected bounded study. Do not edit or reinterpret historical gate decisions.

## November 17 execution update

The owner selected D0–D2 through SOAM-082–085; the [completed report](../../reports/STUDY_D.md) and [decision](../../reports/STUDY_D_DECISION.md) support explicit memory for the bounded task and preserve the tested fast-weight interference failure. D3/D4 remain deferred. The original proposed prompts below retain their historical scope and do not activate later work.

The later [November 17 owner routing decision](../requests/recurrent_retrieval_2026_11_17.md) selects a narrow recurrent-retrieval pilot for [SOAM-086 protocol design](../../tickets/SOAM-086-recurrent-retrieval-protocol.md). Its common-substrate motivation is distinct from the original D3 reliability and D4 capacity tests. E0/F and learned organization remain future questions.

**Historical November 18 prompt:** [Study D-R1 — Recurrent associative retrieval](STUDY_D_R1_RECURRENT_RETRIEVAL.md) is the copy-ready handoff for that selected direction. D-R1 avoids reusing D2 (the completed retention stage) or D3 (deferred reliability). SOAM-086 was then ready; that prompt alone did not approve its protocol or numerical budget.

**Historical November 18 protocol acceptance:** The owner instructed D-R1 to begin. [SOAM-086](../../tickets/SOAM-086-recurrent-retrieval-protocol.md) accepted the [v1 protocol](../STUDY_D_R1_PROTOCOL.md) for implementation; [SOAM-087](../../tickets/SOAM-087-recurrent-retrieval-harness.md) was ready. The proposed numerical ceiling was then pending; it was subsequently accepted and the study completed.

## Evidence ledger

Original result publications and frozen evidence:

- [Studies A/B](https://spencerbug.github.io/research/soam-studies-a-b/): adaptive-update practical benefit inconclusive; ordinary fixed-leak recurrence competent; predict -> score -> correct is retained; fixed sensory correction is an adequate neural default.
- [Study B2](https://spencerbug.github.io/research/soam-study-b2/): ADAPT1 reduced balanced corruption by 52.69% versus FILTER2 while passing guards; coherent and sustained plausible faults remain hard.
- [Study C](https://spencerbug.github.io/research/soam-study-c/): TWO16 (two recurrent states, shared fitted core) improved Brier by 0.02048 versus PC16 and by 0.01819 versus capacity-controlled PC32; both exceed the frozen 0.01 practical margin. Conventional retained multiplicity ADAPT1-M over collapsed ADAPT1-C improved Brier by only 0.00157, below that margin. TWO16 over ADAPT1-M improved Brier by just 0.00029; the conventional model has cheaper fitting and better feature prediction, while TWO16 is faster in that measured implementation. In coherent-fault versus genuine-change evidence-identical worlds, confident predictions remained badly miscalibrated (~0.445-0.450 Brier versus 0.25 uncertainty optimum). Study C did NOT test selective updates, learned operating modes, coupled neural populations, persistent writes, or attractors.
- [Study C decision](https://spencerbug.github.io/assets/research/soam-study-c/STUDY_C_DECISION.txt): accepted the bounded C-H1 result only; no downstream study automatically selected. Historical E1 sharing stop remains unchanged.

**Repository synchronization caveat (checked 2026-11-16):** The public SOAM main branch and the visible historical codex branch do not contain the later A/B/B2/C implementation snapshots and completed local ticket series. The public study reports contain archival evidence. These proposals deliberately add no claims that the current GitHub checkout already implements those studies. Codex must first inspect the actual local working branch and provenance; do not recreate, overwrite, or silently mark missing research records complete.

## Proposed studies and recommended sequence

| Track | Prompt | Question | Default status |
| --- | --- | --- | --- |
| D | [Persistent associative acquisition](STUDY_D_PERSISTENT_MEMORY.md) | Can new object-specific information survive recurrent-state reset without interference? | D0–D2 complete; D3/D4 deferred |
| D-R1 | [Recurrent associative retrieval](STUDY_D_R1_RECURRENT_RETRIEVAL.md) | Can connection-based associative memory retain new associations, and does nonlinear settling improve partial-cue recall? | SOAM-086–089 complete; small settling effect below practical margin, reliability guards failed; no successor selected |
| E | [Object-centered sensorimotor navigation](STUDY_E_OBJECT_NAVIGATION.md) | Can a model reuse learned object-relative structure across viewpoints and actions, beyond sequence memorization? | Conditional independent capability study |
| C2 optional | [Selective updating and modes](OPTIONAL_C2_SELECTIVE_PROCESSING.md) | Are primed/tracking/attended scheduling policies useful when two valid components coexist? | Deferred until a diagnosed compute/continuity bottleneck |
| F planning | [Population topology search](STUDY_F_POPULATION_TOPOLOGY.md) | What favors monolithic, hierarchical, horizontal, or dynamically coupled organizations? | Planning only; no architecture sweep yet |
| F-coupling pilot | [Gated population intermingling](STUDY_F_GATED_INTERMINGLING.md) | Can two independently meaningful populations temporarily couple, mutually settle, and gain compositional capability without overwriting private states? | Future narrow experimental fork after suitable task and controls |

D and E need not require positive C2 results or each other. F's coupled-population pilot can be evaluated after an appropriate complementary-component task exists; do not treat C's *competing* regime hypotheses as *complementary* parts that should be merged. Stage F first as narrow mechanism ablations within family, later a multi-resource tournament.

## Scientific interpretation and architecture principles

- TWO16 demonstrated useful **factorized recurrent hypothesis state**, not simultaneous shared neurons and not a proven attractor. Shared parameters across separate state instances do not establish physical neuron overlap.
- A two-state recurrent predictor and two-state conventional filter are roughly competitive on C's declared probability endpoint; decide among them using feature quality, runtime, fitting and retained-state cost, not only Brier.
- Beliefs may be **competing** (one causal explanation) or **complementary** (several simultaneously valid objects/components). Use different probability/evidence semantics; do not normalize complementary existence probabilities to sum to one.
- The coherent-cause failure is **missing modeled causes or information**, not evidence that two states are too few, that attention is needed, or that recurrent settling will resolve indistinguishable worlds.
- Keep sensory correction, action prediction, internal settling, and persistent writing distinct. A physical action advances once per physical interval; settling never replays a physical action or invents observations.
- Test direct gating, routed messages, temporary joint coupling, and full recurrent intermingling separately. Do not confuse concatenating vectors or independently running populations with demonstrated mutual settling.
- Preserve private component state and identity when composing; test independent component changes, held-out combinations, interference, reversibility, and spurious convergence.
- Report parameters, active and retained state, temporary branches, memory, projections, routing, recurrent iterations, throughput and **measured** latency; FLOP/MAC counts alone are not enough.
- Obtain protocol, manifests, data splits, independent fit roots, controls, effect thresholds, uncertainty rules and finite compute ceilings *before* confirmation. Negative/invalid/inconclusive results remain first-class evidence.

## Codex use

Each linked document is a copy-ready bounded Codex assignment. Read the repository's current AGENTS.md and gate/ticket conventions before use. Write a versioned protocol and finite decision gate before any full run. Do not auto-execute later prompts, create remote issues, or publish a blog. These proposal documents are not amendments to PRIORITIES.md or proof of approval of any later branch.
