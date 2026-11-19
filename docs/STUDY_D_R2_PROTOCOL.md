# Study D-R2 v1: fixed retrieval-versus-decoding diagnostic

November 19, 2026. Owner: SOAM-090. Classification: **essential next**, following
the [owner selection](requests/retrieval_diagnostic_2026_11_19.md) and
[D-R1 decision](../reports/STUDY_D_R1_DECISION.md). Numerical source of truth:
[manifest](protocols/study_d_r2_v1.json). This protocol is the lightweight RFC.

## Question and interpretation

D-R1 preserved acquired codes in the audited projector spans but often returned
incorrect relationships. At the same fixed load, can the unchanged decoder recover
useful relationships from the exact acquired codes, while ordinary cue-only
completion fails? This separates insufficient acquired-code/readout fidelity from
the cue-to-output path. A positive result does not isolate a basin defect from
cue ambiguity, mixed states, encoding geometry or clamping effects.

The privileged branch is an evaluator-only diagnostic ceiling, not deployable
recall. It uses every actual acquired code of the correct object equally; it never
selects the code with the best target error. Because noisy acquisitions are used,
this reference is not a mathematical upper bound on every possible estimate.
No pattern is retrieved, corrected, trained or selected using evaluator truth.

## Fixed mechanism, information and design

Reuse the committed D-R1 `RetrievalMemory`, encoder/decoder, `Core`, and update
rules without modification. PH768 is the `PH-FULL` arm in the manifest and code. It uses the 512 appearance / 256 relationship
thermometer bits, incremental projector writes, fixed observed-key clamps,
ascending asynchronous updates and 32-cycle cap already specified in
[D-R1](STUDY_D_R1_PROTOCOL.md). KV and REG-LIFT are mandatory references.
Carry forward D-R1 development-selected core ridge 1e-6 and REG-LIFT ridge .01;
all other settings are 1. No hyperparameter selection or familiarity calibration.
Scores are archived; accuracy is raw and unconditional. No unknown/rejection,
isolated-acquisition, new retention-gate or comparative-superiority claim is tested.

Fresh task-root namespace `soam-study-d-r2-v1:{root}` inside the existing D-R1
SHA-256 random-stream generator, using the unchanged D-R1 generating
distribution and fixed sensory projection. One fit per independent root uses
2,048 clean training transitions; normalization is that root's training-input
mean squared feature value, floored at 1e-8. Fit and normalization see no
confirmation objects. Four independently generated sequences per root each have
eight correlated-appearance objects, eight noisy grounded snapshots per object,
and eight partial-cue queries per object. Evaluate only after all eight objects
have been acquired; the primary population is the first seven objects. No prefix
testing or capacity sweep. Learners receive the same snapshots and masked cues.
Evaluator geometry, correct object index and clean future features stay private.

Ordinary inference is completed and saved before privileged scoring. Reset all
transient state before queries. The prediction helper takes only memory, masked
cue and actions; the diagnostic helper takes only copied evaluator arrays and has
no model reference. Hash persistent tensors before and after inference and verify
the common core is unchanged. Free eight-step rollouts use retrieved values and
actions only. Separately record grounded one-step core error on fresh probes.

Evaluator-only acquired codes are reconstructed from the same observed record
and fitted core that entered each write: concatenate encode(key,4) with
encode(core.advance(observed_features,-observed_angle),1.5). Preserve all 64 codes
and each final projector for auditing. Decode each of the eight correct-object
codes using the unchanged mean-bit decoder. Score all eight against the clean
canonical relationship; average scores/accuracy across codes, never predictions
before scoring. This explicitly includes acquisition noise and quantization.

## Endpoints and frozen decision

Canonical NMSE <= .1 defines a correct output, as in D-R1. Per root, average
equally across the four sequences and seven earlier objects (and eight query
cues for ordinary recall; eight acquired snapshots for privileged decoding).
The **primary endpoint** is exact-code raw accuracy minus PH-FULL cue-only raw
accuracy. The practical gap is .05; maximum interpretable gap interval width .10.
The diagnostic adequacy guard is exact-code accuracy >= .95. These are scoped
engineering criteria, not a claim about unbounded memory capacity.

Use ten independent confirmation roots. Paired-root percentile bootstrap with
200,000 resamples and fixed seed 54013; Bonferroni family of two quantities
(primary gap and exact-code accuracy), family alpha .05. Root means are the
independent units; snapshots, objects and query repetitions are nested, not extra
replicates. Report ordinary 95% root intervals for every descriptive endpoint.
All-identical root outcomes give degenerate empirical intervals; explicitly state
their finite-sample limit and make no universal reliability claim.

- **Completion-path limitation supported:** code preservation/inference checks
  pass, exact-code adjusted lower bound >= .95, gap lower bound > .05, width <= .10.
- **Practically small gap:** adequate exact decoding, gap upper bound < .05 and
  width <= .10. Do not infer general equivalence.
- **Exact decoding inadequate:** its adjusted upper bound < .95; representation,
  acquisition noise and readout remain candidate limitations. A completion gap
  can coexist and must still be reported.
- Otherwise **inconclusive**. A software/invariant failure is **invalid execution**.

Also save canonical and free-rollout errors/accuracy for KV and REG-LIFT; these
are descriptive references, without a new comparative gate. Report PH cycles,
convergence, monotonic-code violations, and minimum free-coordinate code
discrepancy to the correct object's acquired codes and to other objects' codes.
Discrepancy is mean squared bit/activity difference divided by four, over all
unclamped coordinates (zero activity contributes .25 against a bipolar bit).
The nearest-code calculation is evaluator-only and never changes a prediction.
Check every sequence's stored span (max absolute Px-x <= 1e-8), projector symmetry
and idempotence. Preserve per-query predictions, states, codes, masks and targets
so an independent reduction can reconstruct both endpoint families.

## Schedule, resources and stopping

Fixture root 50011; confirmation roots 53003, 53009, 53027, 53029, 53051, 53057,
53059, 53063, 53069, 53077; repeat root 53003. All use new namespace and separated
train/probe/evaluation streams. The fixture runs one complete four-sequence root,
for timing/invariants only; no setting may be selected from its accuracy.
Ten confirmation fits plus one exact repeated fit plus one fixture = 12 maximum
fit attempts and 36 ordinary model-by-root evaluations. A root contains 256 new
acquisition snapshots shared by the three arms, 224 earlier-object query cues and
no replay. The repeat reproduces a root and is excluded from scientific inference.

The [selection record](requests/retrieval_diagnostic_2026_11_19.md) sets a fresh
900 CPU / 1,800 execution-wall seconds, 2 GiB RSS, 1 GiB artifact ceiling. Before
confirmation, require two times the fixture's 12-root projected time/storage plus
60 seconds / 16 MiB reporting reserve to fit, and measured RSS to fit with 2x headroom.
No retries, replacement roots, extra fits or automatic budget extension. Completed
matching roots may be resumed only without rerunning them. Record running/failed/
complete status and cumulative use even on exception. Use a wall watchdog and
per-object resource checks; stop new numerical work at 90% CPU/wall allocation.

CPU float64, deterministic PyTorch, one intra-op and inter-op thread. Freeze and
archive source hashes, commit, manifest, software/hardware, seeds and fitting inputs
before the fixture; recheck scientific hashes before every later phase. Record all
persistent parameters/storage, live/temporary/evaluator state, measured fit/write/
recall time, cumulative CPU/wall/RSS/artifacts and arithmetic estimates. Per-query
timings are batch-derived, not deployment serial benchmarks.

Required engineering checks include a hand-constructed incorrect-completion/correct-
decode case, exact/noisy-code decoding, evaluator-target poisoning that leaves
ordinary predictions unchanged, hidden-cue poisoning, reset/no-write invariants,
fresh streams, independent metric reduction and exact repeated numerical arrays.
No scientific outcome may relax any criterion. Freeze any material correction as
a new protocol/source identity with fresh streams if confirmation was exposed.

## Decision and exclusions

SOAM-093 will accept supported, negative or inconclusive evidence and recommend at
most one next step without activating it. Retain KV as the existing scoped reference
unless a separate protocol tests changing that recommendation. D-R1's negative
practical-settling result and reliability failures remain unchanged. This study
tests no learned organization, overlap benefit, capacity scaling, active perception,
population coupling, play or general attractor hypothesis. Publication needs a
separate owner instruction.

## Execution procedure

Run, in order, `uv run python -m soam.decoding.runner fixture`, then `confirmation`,
`repeat`, and `report` with the same module prefix. The CLI accepts only these fixed
phases; it does not accept new roots, settings or budgets. A failed phase requires
primary review and cannot be silently retried. Preserve its status and artifacts.
The primary agent controls phase execution; a local worker may only inspect the
prescribed logs or propose the exact next command. No worker controls trials or
its own approval. No external API, GPU service or paid computation is used.
