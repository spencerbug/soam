# Codex prompt — Study D-R1: Recurrent associative retrieval

**Status:** execution handoff prompt, written November 18, 2026. The owner selected
this direction for protocol design through [SOAM-086](../../tickets/SOAM-086-recurrent-retrieval-protocol.md).
This document is not the frozen protocol, a completed protocol decision, or a new
numerical allocation. Writing it does not start the experiment.

**Numbering:** D-R1 is the first recurrent-retrieval follow-up in the persistent-memory
track. Original D1/D2 remain acquisition/retention stages; original D3/D4 remain
deferred reliability/capacity stages. Use `study-d-r1-v1` for the new experiment's
artifact namespace. Keep historical files and results unchanged.

## Mission and reason

Act as SOAM's principal research investigator. When instructed to execute this
prompt, design, implement, verify and report one bounded experiment:

**Can a recurrent associative memory acquire new associations, recover them from
partial cues after complete state reset, and retain them through sequential
learning? Does nonlinear recurrent settling contribute beyond a competent direct
read, and how does the complete system compare with REG and KV?**

The owner's motivation is a more homogeneous recurrent substrate: retrieval and
tracking might eventually acquire their roles and interactions through learning.
Here those roles are supplied. Test a component prerequisite for that future
possibility, not learned organization, superlinear scaling or biological validation.
Do not require a KV win to recognize a useful component result.

## Start from the existing evidence

Read AGENTS.md and its required research documents, PRIORITIES.md, the relevant
tickets and the [owner routing record](../requests/recurrent_retrieval_2026_11_17.md).
Then inspect the [D protocol](../STUDY_D_PROTOCOL.md), [manifest](../protocols/study_d_v1.json),
[report](../../reports/STUDY_D.md), [decision](../../reports/STUDY_D_DECISION.md),
and actual acquisition implementation. Verify checkout, provenance and dependencies.

D0–D2 found that KV, REG and FAST acquired isolated objects, while REG and FAST
failed the sequential-retention guard. FAST performs a direct linear associative
read; it did not test iterative Hopfield retrieval. REG solves a mask-aware linear
system from accumulated statistics. Neither result establishes that recurrent
associative memory generally fails or that every dynamic population needs a cache.

Use SOAM-086 for the protocol decision. Resolve consequential choices there under
the existing RFC rules. On execution, mark it in progress and complete its actual
acceptance criteria before dependent implementation. Allocate later engineering,
experiment and decision tickets only as needed; do not preactivate deferred work.

## Define one genuine recurrent memory

Select one competent nonlinear associative-memory family and one bounded sequential
write rule. A symmetric Hopfield-style memory is the preferred starting point;
justify the state representation and acquisition rule for real-valued, correlated
appearance cues and independent relationship values. Do not silently apply binary
random-pattern capacity assumptions to this task.

Freeze these details before confirmation:

- Stored tensors, state dimensions, activation law, connectivity and diagonal terms.
- Input encoding, missing-coordinate mask, cue initialization, whether observations
  remain clamped or act as a decaying bias, and the exact readout to the action core.
- Sequential write equations, learning-rate schedule, normalization, and the finite
  number of updates per grounded snapshot. Replaying old observations is outside
  this pilot; any indispensable retained sufficient statistics must be declared.
- Update order or integrator, step size, maximum settling cycles, convergence
  tolerance, cycle/nonconvergence handling and output selection without target access.
- Any energy function and the assumptions under which the implemented updates
  decrease it. Symmetry alone does not guarantee a particular discrete integrator
  converges, and convergence does not establish correct recall.

Prefer memory encoded in recurrent connections over a hidden pattern-bank lookup.
Disclose any stored patterns, lookup, fitted decoder, feature expansion or routing.
A pattern-bank/attention implementation may be a labeled control; it cannot silently
stand in for the connection-based candidate. If an encoder or readout stores new
associations, isolate its contribution before attributing recall to recurrence.
Any feature lift is fixed before confirmation and available to a corresponding
direct-read control; do not give only the recurrent candidate a useful new encoding.

Review primary sources for the chosen equations and write rule. Starting points
include [Hopfield's graded-response model](https://authors.library.caltech.edu/records/rhj8z-8dj90)
and [Storkey's incremental storage rule](https://homepages.inf.ed.ac.uk/amos/publications/Storkey1997IncreasingtheCapacityoftheHopfieldNetworkwithoutSacrificingFunctionality.pdf).
These are candidates to assess, not an instruction to combine incompatible rules
or assume they solve this task. Choose one family, not an architecture tournament.

## Preserve the D task and isolate retrieval

Keep D's supplied feature/action task as the default: stable 16-coordinate appearance,
eight relationship-feature channels, fixed sensory projection, measured reference
angle and a common fitted action core. Appearance does not determine the novel
relationship. Fit the common core only on disjoint offline data, then freeze it
during acquisition and evaluation for every memory variant within a root.

At acquisition, supply identical grounded snapshots and masks to all candidates.
Use the permitted inverse action operator for canonicalization. At query, clear
all transient state and nonpersistent caches, expose the cue, retrieve a canonical
relationship and predict eight actions without future observations. No object IDs,
hidden simulator variables, correct relationship targets or evaluator-selected
memory addresses enter retrieval. Each physical action advances the predictor once;
settling cycles do not replay actions or create observations.

Use D's 0/1/2/4/8 snapshot budgets for isolated acquisition and eight similar objects
with eight snapshots each for sequential retention. Retain its task distributions
unless a change is justified and frozen as a new condition. Use fresh streams and
rerun all comparators; published D confirmation results are historical context.
Start from D's 24 isolated objects and four acquisition sequences per root, with
eight queries per object/condition. Keep its training-derived error normalization;
do not renormalize by each candidate's output or use query targets to fit it.

## Required controls

| Control | Purpose |
| --- | --- |
| NOWRITE | Same observations and reset, no acquired persistent associations |
| KV | Strong explicit nearest-neighbor memory with declared storage |
| REG | Competent mask-aware ridge-regression memory with development-only tuning |
| FAST | Historical direct delta-map reference, rerun on the new paired streams |
| Recurrent candidate, full settling | Proposed connection-based associative retrieval |
| Same candidate, truncated retrieval | Same acquired weights, encoding, initial state and decoder; one complete update cycle versus the frozen full settling budget |

Define a complete update cycle so the truncated condition is meaningful for the
chosen state layout. Trace intermediate retrievals and report latency versus useful
accuracy. Additional iterations can be useless or harmful; do not assume a monotonic
improvement. If feature expansion changes the direct-read hypothesis class, include
the corresponding REG/direct-read comparator in the finite inventory.

As a fixture, show that an iterative linear solver converges to the direct REG
answer within declared numerical tolerance. It need not become another full trial
arm. This distinguishes implementing a linear solve with recurrent activity from
testing nonlinear associative completion. Similar energy language is not sufficient
evidence that these mechanisms are equivalent or different in useful behavior.

## Bounded stages

**D-R1.0 — scientific and competence fixtures.** Test reset, no-write inference,
reproducibility, legal information access and preservation of the action core.
Demonstrate acquisition and retrieval of a few development-only associations at a
plausible load. Include a known failure and verify correct scoring. Test the actual
energy/update assumptions where claimed. If the finite development inventory cannot
produce a competent candidate, report that limitation and stop; do not launch an
unbounded search or call a software error scientific falsification.

**D-R1.1 — isolated acquisition.** Observe, write, reset, retrieve and predict at each
snapshot budget. Pair full appearance cues with D-style partial cues (eight visible
appearance coordinates); relationship channels remain hidden in both. Match cue
noise on shared coordinates. This measures learning before sequential interference.

**D-R1.2 — sequential retention.** Acquire eight similar objects in order. After each
acquisition, reset and query every acquired object without writing. Pair full/partial
cues across models and acquisition stages. Record immediate post-acquisition and
later performance on identical evaluator-owned probes. Include unacquired same-family
cues for false-recall assessment. Probe earlier memories after new writes, and test
a small preregistered perturbation of retrieval activity with weights fixed.

A full-cue success with partial-cue failure points toward completion/ambiguity limits.
Failure on both can reflect storage, decoding or retrieval dynamics; it does not
prove the memory was erased. Use permitted-observation development diagnostics and
the frozen interventions to distinguish these explanations. Evaluator targets may
score trajectories but never initialize or steer the main retrieval condition.

## Endpoints and interpretation

Choose and freeze one primary endpoint and contrast. **Recommended primary:** paired
gain in final D-R1.2 earlier-object raw retrieval accuracy from full settling over
the truncated condition, on partial cues. A proposed practical margin is five
percentage points, with a positive adjusted lower bound and interval width at most
ten percentage points. Adopt or justify those margins before confirmation; also
report absolute performance so improvement over a poor ablation is not enough.

Keep D's canonical NMSE <=0.1 definition of accurate recall unless explicitly revised.
Proposed absolute guards carry forward D's budget-eight accuracy lower bound >=0.8,
free-eight prediction-error upper bound <=0.15, final old-object accuracy lower bound
>=0.8, and old-object prediction-error-increase upper bound <=0.02. The protocol
must specify the full acquisition criterion, independent units, comparison family
and uncertainty procedure rather than silently inherit the old decision gate.
Prespecify secondary REG/KV contrasts and any practical margins used to claim an
advantage; do not select a favorable comparator or endpoint after confirmation.

Freeze separate false-acceptance and known-cue coverage guards using development
calibration only. Report raw accuracy over all queries, accepted-query accuracy,
coverage, accepted-but-wrong rate and unknown-cue acceptance with explicit denominators.
Rejecting every query cannot pass. A low energy or stable state is not automatically
a calibrated familiarity score.

Also report acquisition curves, canonical recall error, grounded one-step and free
multistep prediction, forgetting by object age, full/partial-cue gaps, perturbation
recovery toward correct outputs, settling trajectories and failures, and all REG/KV
comparisons. Use paired independent roots with uncertainty for primary and guardrail
quantities; nested objects, queries and timesteps are not independent fit replicates.

Keep conclusions separate:

1. Does the candidate provide reliable persistent acquisition and retention?
2. Does additional recurrent settling make a practically useful causal contribution?
3. Does the complete system improve on REG, or offer a useful tradeoff against KV?

A one-pass candidate may be reliable without establishing a need for additional
settling. A recurrent candidate may be reliable without beating KV. Conversely,
convergence, bounded activity or a win over FAST alone does not establish useful
attractors. Classify evidence as supported, adequately precise negative,
inconclusive or invalid under the frozen rules.

## Resources and execution discipline

Before numerical work, freeze the candidate inventory, tuning opportunities, fresh
train/development/confirmation streams, independent roots, selection rule, repeat
check and stopping rule. Ten independent confirmation roots is a starting proposal;
justify precision and feasibility before freezing. Never tune on confirmation or
extend a run because an interval is disappointing.

Propose a fresh ceiling of **2 CPU-hours, 4 execution wall-hours, 2 GiB peak process
memory and 2 GiB artifacts**, inclusive of numerical development, confirmation,
fixtures, calibration, failures, diagnostics, repeats, profiling and reporting;
engineering/tests are separate. Obtain owner acceptance
if a new allocation has not already been explicitly authorized. The earlier D0–D2
allocation is not renewed by this prompt. Reserve time and storage for reporting.

Separately freeze a model-storage ceiling after development-free sizing/analytic
checks and bounded timing fixtures. Do not force a Hopfield candidate into an
obviously overloaded regime just to reuse D's old byte limit. Count recurrent
weights, encodings, readouts, statistics, patterns, caches, active/retained states,
write updates and settling work. Report actual allocations and all mismatches;
equal ceilings are not equal usage. Separate a capability result from an advantage
at matched resources. Measure write/recall latency, throughput and total fitting cost.

Use Python/PyTorch and the repository's reproducibility conventions. Run
`uv run pytest` before changing existing code, then appropriate invariant and
regression checks. Keep frozen D code/evidence intact or preserve it with explicit
versioned interfaces. Use the experimental-trials skill when numerical execution
begins; local workers cannot select their own trials or approve their own actions.

## Deliverables and stop boundary

Produce `docs/STUDY_D_R1_PROTOCOL.md`, a versioned manifest, minimal implementation
and invariant tests, source/config/software provenance, paired root results with
uncertainty, acquisition/retention and settling plots, failure examples, resource
accounting, `reports/STUDY_D_R1.md` and a separate decision report. Preserve all
prespecified failures and exclusions. Update the owning tickets, indexes and
PRIORITIES.md, and run the ticket validator.

Finish with one result-dependent next recommendation. Do not execute D3/D4, E0/F,
bidirectional coupling, learned role allocation, replay/consolidation, a capacity
sweep or a larger population framework. No remote issue or blog publication is
authorized by executing this experiment prompt.

**Final question:** Can a population acquire and retain useful associative memories
through its declared recurrent mechanism, and what did nonlinear settling add
beyond strong direct retrieval at the measured cost?
