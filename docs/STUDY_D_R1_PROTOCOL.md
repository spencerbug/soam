# Study D-R1 v1 — recurrent associative retrieval

November 18, 2026. Protocol/RFC owned by [SOAM-086](../tickets/SOAM-086-recurrent-retrieval-protocol.md).
Classification: essential next. This is the selected [D-R1 handoff](proposed-studies/STUDY_D_R1_RECURRENT_RETRIEVAL.md),
called “D1-R1” in the owner's instruction to begin. Original D1/D2 remain acquisition
and retention stages. The [manifest](protocols/study_d_r1_v1.json) owns numerical
settings. **Protocol and fresh numerical allocation accepted.**
No fixture, development fit, calibration or confirmation is authorized by the old D
allocation. The owner approved the specified fresh ceiling on November 18: see the
[allocation receipt](requests/study_d_r1_allocation_2026_11_18.json).

## Question, evidence and decision

Can a connection-based associative memory acquire independent appearance/relationship
associations, retrieve after complete transient reset, and retain them through eight
sequential objects? Does additional nonlinear settling improve final earlier-object
partial-cue accuracy over one complete update cycle using the same weights?

[Study D](../reports/STUDY_D.md) and its [decision](../reports/STUDY_D_DECISION.md)
remain unchanged: KV passed its conjunction; REG and FAST acquired isolated objects
but failed sequential-interference guards. Inspection of `soam/acquisition/models.py`
confirms FAST is a direct delta map, and REG solves a masked linear system. Neither
is a test of nonlinear Hopfield completion. D-R1 operationalizes H2; its interference
guard does not confirm H3 learned scoping. The [hypothesis ledger](HYPOTHESES.md)
owns these claims. No shared-neuron, learned-role, scaling, or integration claim follows.

**Proceed with one projection-rule Hopfield family (PH768).** The main alternative
is competent direct REG, including a control with PH768's fixed feature expansion;
KV remains the explicit-memory reference. A reliable candidate need not beat KV.
One-cycle reliability without an additional-settling benefit is also a valid outcome.
A failure of the fixed candidate is not a general falsification of associative memory.

## Primary research and mechanism choice

[Personnaz, Guyon and Dreyfus (1986)](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.34.4217)
introduce projection-rule storage; [Kanter and Sompolinsky (1987)](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.35.380)
analyze a symmetric projection memory with binary units. Their stored-pattern
stability motivates the choice for correlated codes; it does not guarantee useful
partial-cue basins, denoising or familiarity calibration here. This pilot uses the
explicit incremental orthogonal-projector construction derived below, not a claim
that the cited papers supply this entire acquisition/encoding procedure.

[Hopfield (1984)](https://authors.library.caltech.edu/records/rhj8z-8dj90) supplies a
graded-response alternative. We choose discrete coordinate minimization to make the
implemented energy argument exact rather than assume a synchronous tanh integrator
converges. [Storkey (1997)](https://homepages.inf.ed.ac.uk/amos/publications/Storkey1997IncreasingtheCapacityoftheHopfieldNetworkwithoutSacrificingFunctionality.pdf)
is an incremental local-storage alternative, not combined with the projection rule.
This candidate deliberately accepts a nonlocal, quadratic-cost write to address
correlation before testing cheaper local writes. No random-binary-pattern capacity
law is applied to the strongly correlated codes or noisy snapshots in this study.
The accessible author copy of [Personnaz et al. (1986), section 2, equation 3](https://www.neurones.espci.fr/Articles_PS/J.STAT.PHYS.1986.pdf)
explicitly gives the projector `X X^+` as the zero-initial-matrix case. Its later
orthogonal-pattern local approximation is **not** our write rule. Our residual
rank-one update below is an independently derived incremental construction of that
projector for correlated patterns. Publisher full-text retrieval for the PRA papers
was restricted; the accessible primary equation, publisher abstracts and the explicit
derivation support this contract. Implementation must still verify the invariants.

## Task and information boundary

Retain D's distributions: 16-dimensional appearance `k = normalize(prototype +
0.5 normal) * 4`, independent latent relationship with two uniform [-1,1] coordinates,
fixed seed-1729 orthonormal 8-by-2 sensory projection, and eight observed relationship
channels. Simulator geometry, object/family labels and projection inverse remain
**evaluator-only**. The learned core receives observed features and action angles.

For each root, fit `M(a)y = cos(a) A y + sin(a) B y` from 2048 clean transition pairs
(8 families x 8 objects x 32 pairs; 4096 feature snapshots). The trigonometric basis
is supplied. Fit A/B by ridge using the two manifest settings on development only;
select one ridge by mean held-out old-core free-eight NMSE. Each confirmation root
fits that chosen ridge on its own fresh train stream. Freeze the resulting A/B and
the training-feature mean-square normalization (floor 1e-8) before any writes.
The same A/B tensors and denominator serve every arm within that root.

Acquisition supplies full, stable appearance and eight noisy relationship features
(SD .02) at a measured reference angle uniform [-.4,.4]. Canonicalize with the
fitted `M(-q)`. One distinct grounded snapshot allows one write; no old-observation
replay, global refitting, hidden identity, or evaluator-selected address. The stable
appearance matching used by KV is declared supplied correspondence through content.

Query exposes either all 16 appearance coordinates or eight selected without
replacement, with no relationship channels. Generate one 16-coordinate noise vector
(SD .02) and one partial mask, then derive both views: shared visible coordinates
are bit-identical. Hidden values, including NaNs/sentinels, must not affect retrieval.
Full/partial views share actions and evaluator targets. Clear all transient states
and caches before every query. Recall once, then advance M by each of eight actions
(uniform [-.6,.6]) exactly once, without future observations. Settling neither advances
physical time nor creates data. Grounded one-step diagnostics receive only the actual
current observed relationship, in a separate evaluation path; they cannot feed free
rollouts. Evaluation and all retrieval interventions leave persistent bytes unchanged.
The learner API accepts only a grounded record (key, observed features, reference
angle), a masked cue, and incremental actions. Reject wrong shapes, nonfinite visible
values and ungrounded write requests before mutation. Reset clears activity and all
nonpersistent caches. Snapshot/restore is for verification, never result selection.

Use new namespace `soam-study-d-r1-v1` and artifact directory `runs/study-d-r1-v1`.
Preserve D's code and artifacts; use new modules/interfaces rather than modifying its
random generator or memory class. No existing confirmation array becomes unseen data.

## PH768 representation and sequential writing

There is one fixed representation, no width/encoding search. Encode each appearance
coordinate with 32 evenly spaced midpoint thresholds on [-4,4], and each canonical
relationship coordinate with 32 midpoint thresholds on [-1.5,1.5]. For bound b,
`theta_j = -b + (j + .5) * 2b/32`, `j=0..31`; code is +1 if `x >= theta_j`, else -1.
Concatenate appearance first (512 units), relationship second (256): n=768. Missing
appearance coordinates mean all their 32 bits are unobserved, not negative bits.
The fixed decoder is `b * mean(bits)` per coordinate; for nonmonotone states this
same decoder applies without sorting or target-based correction. Encoding clips by
saturation only; record acquisition/query saturation rates. Range choices are supplied
scaffolding, not learned features. Relationship quantization spacing is .09375, with
at most .046875 scalar reconstruction error inside range; this is not an NMSE guarantee.

Persistent tensors are a float64 768x768 projector P, initialized to zero, and int64
snapshot/rank counters. No pattern bank, object index, learned decoder, raw-record
cache, replay buffer or optimizer state is retained. For one encoded grounded
snapshot x, compute from the old P:

```
r = x - P @ x
r = r - P @ r                 # one fixed numerical reorthogonalization
s = r.T @ r
if s > 1e-10 * (x.T @ x):
    P_new = P + outer(r, r) / s
    P_new = (P_new + P_new.T) / 2
else:
    P_new = P
```

Increment snapshot count even for a dependent code; rank count increments only on
an update. This is one bounded write with no learning-rate search or decay. In exact
arithmetic, r is orthogonal to the old span; adding its normalized outer product
extends the orthogonal projector and preserves all old span vectors. A repeated
or linearly dependent code needs no additional direction. The second residual
projection is solely a fixed floating-point safeguard. Check symmetry, idempotence,
finite entries and stored-vector residuals in fixtures (max absolute tolerance 1e-8); abort on violated tolerance,
never silently refit from retained patterns. Noisy snapshots can add directions and
spurious completions. Algebraic storage preservation does not prove retained recall.

Effective recurrent weights are `W = P - diag(diag(P))`, symmetric with zero diagonal.
Keep the full P diagonal for future writes; do not zero it in persistent storage.
W can be formed transiently or applied by excluding self-terms. Any materialized W
and scratch/copy count toward peak/temporary bytes. No candidate-only hidden lookup.

## Initialization, settling, scoring and energy

Initialize state s to zeros; fill and permanently clamp observed appearance bits.
All relationship and missing-appearance bits start at zero. A **complete cycle**
visits every free coordinate exactly once, in increasing global coordinate index,
using the current state (asynchronous updates). For field `h_i = sum_j W_ij s_j`,
set the coordinate to +1 if h_i > 1e-12, -1 if h_i < -1e-12, otherwise keep it.
Thus unseen zero ties may remain zero; zero is an explicit abstaining activity,
not a second observation or a randomized target-dependent initialization.

PH-1 returns after one complete cycle. PH-FULL uses the same weights, initialization,
ordering, decoder and clamp, stopping after a cycle with no changed coordinates or
32 cycles, whichever comes first. Save every cycle's decoded values, energy, number
of changes and convergence status; do not select the best target-scored iterate.
At the cap return the last state and flag nonconvergence, retaining its raw score.
Detect a repeated nonstationary state as a numerical/invariant failure; record it
and stop. No random restart, extra cycle or alternate memory fallback is permitted.

For fixed cue clamps, `E(s) = -.5 s.T W s`. Every changed free coordinate strictly
reduces E because W_ii=0 and the chosen endpoint minimizes `-s_i h_i`. The finite
{-1,0,+1} free-state space and tie retention exclude cycles in exact arithmetic;
this does not assert convergence within 32 cycles or correct output. Record per-update
energy in invariant fixtures, per-cycle energy in trials; tolerated upward drift is
`1e-10 * max(1, abs(E_before))`. Symmetry/energy failures are invalid execution.

Familiarity score for PH is `mean((s - P @ s)^2)` after its own retrieval budget.
It is a residual, **not a probability**; stable/low-energy activity alone does not
pass familiarity. Calibrate separate full/partial and PH-1/PH-FULL thresholds from
development only. Thresholds annotate acceptance, never alter raw output or writes.
Empty memory returns zero relationship and rejects regardless of score.

## Mandatory controls and finite tuning

| Arm | Persistent association mechanism | Development inventory |
| --- | --- | --- |
| NOWRITE | No persistent associations; post-reset zero relationship | One |
| KV | D's 32 preallocated content-matched rows; running mean values; masked nearest neighbor | One |
| REG | D's Sxx/Syx mask-aware ridge solve in raw appearance coordinates | Ridge .01, .1, 1 |
| FAST | D's normalized delta update and direct read; Frobenius cap 16 | Rate .25, .5, 1 |
| REG-LIFT | Same 512-bit appearance encoding as PH; masked ridge; raw canonical value targets | Ridge .01, .1, 1 |
| PH-FULL | Projection memory and nonlinear settling | One fixed setting |
| PH-1 | Same acquired PH checkpoint, one complete cycle | No additional fit/write |

REG-LIFT stores Szz (512x512), Syz (8x512) and count. A cue exposes all bits belonging
to visible coordinates; solve only their principal submatrix. Use unscaled bipolar
bits and the displayed ridge values, and reconstruct observed bits with Szz for the
familiarity residual. Count the fixed encoder and learned cross-map. This prevents a
feature-expansion benefit alone from establishing a recurrence advantage. REG/FAST/KV
use their historical equations, not their historical selected settings or results.

Select the core first. Then evaluate all 12 writer configurations (including NOWRITE
and KV, excluding duplicate PH-1 storage) on each of two development roots. Select
REG, FAST and REG-LIFT independently by equal-weight mean of D1 J and final D2
old-object free-eight error, each averaged equally across cue conditions. Tie within
1e-12 goes to manifest order. PH has no selectable hyperparameter. Report all development
failures. No architecture tournament, additional learning rate, clamp choice or seed.

On independent calibration streams at the two development roots, run selected arms
on four eight-object sequences each, plus eight unknown same-family objects per
sequence. For each arm and cue condition choose the smallest threshold among sorted
known scores giving pooled known coverage >=.95 (empirical quantile, method `higher`).
Unknown outcomes are recorded but cannot choose thresholds. PH-1 calibrates its own
threshold. Failure of false-recall guards is a result, not permission to retune.

Fixture requirement: conjugate gradients from zero on a raw REG masked SPD system
must agree with the direct solve (relative solution residual <=1e-8; canonical output
absolute tolerance 1e-8, relative 1e-7), at most 64 iterations. It is a numerical
identity check, not another full arm or evidence for nonlinear completion.

## Stages and finite inventory

**D-R1.0:** hand-constructed invariant fixtures first, then one budgeted timing root
and two development roots. Include reset, no-write inference, forbidden-input poisoning,
query-order/ID invariance, deterministic exact replay, clamping, correct decoder,
projector algebra, duplicate writes, action-core fingerprints, energy descent, and
an equal-cue/different-target failure with correct raw/accepted scoring. Verify that
one-cycle outputs equal the first cycle of the full trace. Three-association noiseless
fixtures (hand-specified observations, identity core and denominator 1) must recover
within canonical NMSE .1 on full cues; the budgeted development
screen additionally requires PH's isolated budget-eight full accuracy >=.9 and partial
accuracy >=.8 on **each** development root. This checks basic competence without
requiring the eight-object retention hypothesis to succeed. If the fixed candidate
fails, report a bounded competence failure and stop before confirmation; do not call
an invariant/software failure scientific falsification. No automatic corrective search.

**D-R1.1:** 24 isolated objects from distinct fresh families per root, each at budgets
0/1/2/4/8. Use prefixes of eight snapshots and the same eight paired full/partial
query/action probes at all budgets. Reset memory between objects and initialize each
budget from the declared snapshot prefix, never from a future budget. Define J as the
equal-budget mean free-eight NMSE for budgets 1/2/4/8, partial cues only for decisions.
Report both cue conditions and every budget, including zero and one-shot descriptives.

**D-R1.2:** four sequences per root, eight similar objects per sequence, eight snapshots
per object. After each acquisition query every acquired object on its fixed eight
paired probes after reset, without writing. Save the triangular acquisition-age
matrix. Final earlier-object metrics average the first seven objects, then sequences,
then roots. Retention is final free-eight error minus immediately post-acquisition
error on those identical probes. Query eight never-acquired same-family objects per
sequence after the last write. No unknown object is written.

Perturbation: after cycle one, flip a fixed RNG-selected 5% (ceil) of nonzero free
coordinates, using a distinct stream; never perturb clamped bits. At final D2 only,
run one additional PH trajectory to the same total cap of 32 cycles, with fixed
weights. Record excess canonical error relative to unperturbed recall, final accuracy,
energy and convergence. If no eligible coordinate exists, record a zero-size intervention.
The injection may increase energy; subsequent coordinate updates must still decrease
it under the stated tolerance. This is descriptive recovery toward useful output; do not equate return to any fixed
point with correct recovery. Traces and timings at cycles 1/2/4/8/16/32 use the same
path, padding stopped trajectories for accuracy plots but recording actual cycles/time.

Old-core check: 64 held-out trajectories/root from observed current relationship
features, with free-eight NMSE <=.02 for every root and byte-identical A/B before/after
writes. Switching between queried objects must produce identical results under order
permutation after reset. These checks protect implementation validity, not retention.

## Endpoints, uncertainty and classification

Canonical accuracy is `canonical NMSE <= .1`, with D's **training-derived denominator**.
Free-eight averages future steps 1..8; canonical step zero is reported separately.
Raw accuracy includes every query, even rejected/nonconverged ones. Primary root value
is PH-FULL minus PH-1 final earlier-object raw accuracy on partial cues. Adopt the
handoff's .05 absolute practical margin and <=.10 interval-width precision criterion.

Ten paired, independently fitted roots are the independent units. Average nested
queries, objects and sequences within root first. Use 200,000 paired root bootstrap
resamples with fixed seed and percentile intervals; the same sampled root indices
apply across all arms. Use two-sided alpha .05/12 for these **12 frozen decision
quantities**, always reporting all of them:

1. PH-FULL minus PH-1 final earlier-object partial-cue raw accuracy.
2. PH-FULL D1 J relative gain over NOWRITE: `(J_N - J_PH)/max(J_N,1e-6)` per root.
3. PH-FULL D1 budget-eight partial-cue raw accuracy.
4. PH-FULL D1 budget-eight partial-cue free-eight NMSE.
5. PH-FULL final earlier-object partial-cue raw accuracy.
6. PH-FULL earlier-object partial-cue free-eight retention difference.
7. PH-FULL final earlier-object partial-cue known coverage.
8. PH-FULL final earlier-object partial-cue accepted-but-wrong rate over **all known queries**.
9. PH-FULL partial-cue unknown acceptance over **all unknown queries**.
10. PH-FULL minus REG final earlier-object partial-cue raw accuracy.
11. PH-FULL minus KV final earlier-object partial-cue raw accuracy.
12. PH-FULL minus REG-LIFT final earlier-object partial-cue raw accuracy.

Reliable persistent retrieval requires J gain point >=.20, lower >0, width <=.40;
budget-eight accuracy lower >=.80; budget-eight free error upper <=.15; final old
accuracy lower >=.80; retention increase upper <=.02; known coverage lower >=.90;
accepted-but-wrong upper <=.05; unknown acceptance upper <=.10. These last three
are separate guards; rejecting everything cannot pass. Report accepted accuracy as
correct-and-accepted / accepted, coverage as accepted / known, and accepted-wrong
also / accepted as a descriptive conditional risk. If accepted count is zero,
conditional rates are undefined, not zero. Report metrics per root with denominators.

Useful additional settling requires reliable retrieval plus primary point >=.05,
adjusted lower >0 and width <=.10. Primary upper <.05 with width <=.10 is adequately
precise negative practical-settling evidence even if some smaller improvement exists.
Otherwise the primary is inconclusive; reliability is reported separately. A failed
guard is a demonstrated adverse result only if its adjusted interval lies wholly on
the failing side; a straddling interval is inconclusive reliability. Invalid execution
supersedes scientific classifications and never counts as a negative hypothesis test.

Each secondary REG/KV/REG-LIFT advantage uses the same .05 point, positive lower and
.10 width rules on final old accuracy, conditional on candidate reliability; upper
<.05 with sufficient precision is a precise practical negative for that comparison.
Never choose whichever comparator happens to lose. Report all errors and storage/
latency tradeoffs; no accuracy-cost advantage or global cheapest claim is preregistered.
A capability result may stand without any comparator advantage. FAST comparisons,
full cues, one-shot, accepted-only accuracy and perturbations use descriptive ordinary
95% root intervals, not additional confirmatory claims.

Ten roots are a bounded pilot, not a guaranteed-power design. A normal approximation
for the adjusted contrast width is `2*z_(1-.05/24)*SD(root differences)/sqrt(10)`;
roughly .055 root SD is needed for width .10. No D confirmation result estimates
D-R1 variance. If NOWRITE J < 1e-6 in any root, report absolute acquisition error
differences and classify the relative acquisition criterion uninformative, never supported. Report observed width and leave imprecision inconclusive; never add
roots because of an interval. Root bootstrap can degenerate at all-zero/all-one
outcomes: label such intervals as empirical finite-root intervals, report the number
of independent roots and raw counts, and do not claim a population-wide zero risk or
universal reliability. The criteria support only this task/distribution and budget.

## Resources, phases and stopping boundary

Accepted fresh allocation: **7200 CPU seconds, 14400 execution wall seconds, 2 GiB
peak process RSS and 2 GiB artifacts**, inclusive of numerical fixtures, development,
calibration, failed attempts, confirmation, repeat, diagnostic/profiling work, plots
and audit/reporting. Engineering and hand-constructed unit tests are separate; a
scientific timing/competence fixture is numerical work and cannot bypass allocation.
Record owner acceptance separately; do not infer it from the old D allocation.

Development-free sizing fixes an **8 MiB per-arm numerical persistent ceiling**:
PH P uses 4,718,592 bytes plus counters; A/B uses 1024 bytes; fixed threshold tables,
settings and permutations are charged. REG-LIFT's 512x512 + 8x512 float64 statistics
use 2,129,920 bytes before counters/core/encoder; KV/REG/FAST keep their smaller actual
allocations. This is not matched usage. PH has 768 transient state values plus fields
per query, and temporary projector/write/snapshot tensors must be counted. All peaks
include batch workspaces, materialized W, copies and evaluator artifacts. No pattern
bank is hidden outside the cap. At most 64 grounded encoded snapshots enter any
sequential PH memory; raw load/rank is descriptive, not a capacity guarantee.

Run CPU PyTorch, deterministic float64, one intra-op and one inter-op thread. Finite
core inventory: one fixture fit, four development fits (2 roots x 2 ridges), ten
confirmation fits and one exact repeated first-root fit = **16 attempts maximum**.
Calibration reuses the frozen development cores; no new fits. No spare attempts or
replacement roots are silently authorized. The fixture runs the complete selected
configuration inventory and all evaluation/diagnostic paths at its single root.
Before development, project remaining phase CPU/wall/artifacts with a 2x timing/size
margin, including each raw/lifted ridge solve, calibration, repeat and report reserve.
If projections exceed 90% of CPU/wall or artifact caps, stop with a feasibility report.
Do not reduce mandatory controls or change size/precision to squeeze through.

Freeze manifest hash, immutable source snapshot/commit, dependency versions, selected
settings, familiarity thresholds, fixture receipt and allocation acceptance before
confirmation data generation. Commit scientific source before numerical work, disclose
other dirty files, and preserve historical D fingerprints. Phases refuse overwrite:
fixture -> development -> calibration -> freeze -> confirmation -> repeat -> report.
The primary agent controls the finite run list using the experimental-trials skill;
local workers cannot choose trials or approve actions. Sample CPU/wall/RSS/disk through
every phase including failed ones; stop new trials before 90% CPU/wall to reserve
reporting. Limits never silently renew after failures. Preserve incomplete outputs
and distinguish resource-stopped/inconclusive from invalid or scientific failure.

Repeat confirmation root 42003 exactly, including fresh core fitting, encoded inputs,
memories, all raw outputs, decisions and diagnostics; timings excluded. Independently
reduce saved arrays, verify source/input hashes, enumerate all failed/excluded records
(no planned exclusions), and stop on mismatches. An implementation repair needs a new
source identity and explicit review; changes of mechanism/endpoint/data require a new
protocol version and fresh confirmation streams. Do not reuse a failed confirmation
attempt as unseen data or silently consume a seventeenth fit.

## Implementation, deliverables and review

Implement a new `soam/retrieval/` package and scientific-invariant tests; import only
unchanged pure D interfaces/equations as appropriate. Source roots must not expose
simulator objects to learner APIs. Keep fit/selection/calibration/confirmation receipts
and raw arrays under the new namespace. Save source/config/environment, train/data
hashes, observation/update/settling counts, all persistent/active/temporary storage,
CPU/RSS/artifact telemetry, latency distributions and serial query throughput.

Required outputs after numerical authorization: `reports/STUDY_D_R1.md`, a separate
`reports/STUDY_D_R1_DECISION.md`, acquisition/retention/settling plots, all root tables,
unknown/known acceptance tables, failure examples, repeat verification and resource
ledger. Reports must distinguish storage preservation, successful completion, added
settling benefit and complete-system tradeoffs. Choose at most one next recommendation;
do not execute D3/D4, E0/F, replay, learned role allocation, coupling or capacity sweeps.
No issue/blog publication is authorized. The owner has already selected the conceptual
recurrent-substrate direction; a new substantive finding should trigger a blog notice.

SOAM-086 accepts this contract only. Its acceptance does not establish candidate
competence, feasibility or a research gate. The next engineering ticket must verify
all invariants and, after allocation acceptance, the bounded timing fixture. Only then
allocate the experiment ticket for development and its competence screen, followed
by conditional confirmation. If a screen fails, preserve the result and require a
fresh corrective decision.
