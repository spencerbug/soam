# Study D v1 — post-reset association acquisition and retention

November 17, 2026. Protocol/RFC owned by SOAM-082. The [owner selection](requests/study_d_2026_11_17.md)
and [manifest](protocols/study_d_v1.json) select D0–D2 only. This is a new experiment,
not evidence that Study C learned persistent memory. E1 stop and A/B/B2/C decisions
remain unchanged. Initial scope is D-H1 and a bounded D-H4 comparison; D-H2 independent
whole-model refitting, D-H3 write selection, D3 faults, and D4 capacity scaling are
untested. A conventional winner is a valid outcome.

## Decision and alternatives

Question: can a few grounded snapshots create object-specific relationships that
survive complete transient reset, generalize through an offline-learned action
operator, and survive learning seven other similar objects? Does a rank-one fast
associative operator outperform bounded episodic storage or online regression?

Use a small learned linear recurrent action core rather than importing TWO16's
supplied competing-regime semantics. The candidate updates a key-to-value block of
a recurrent state operator. This block is algebraically an online delta regression;
an exact direct-map equivalence check is mandatory. A win cannot establish a uniquely
recurrent mechanism, a Hopfield attractor, shared neurons, or learned organization.
[Schlag, Irie and Schmidhuber (2021)](https://arxiv.org/abs/2102.11174) motivate
outer-product/delta fast associative writes, not a claim that this experiment
replicates their learned programmer or proves a biological theory.

## Task, observability and supplied structure

Each family has a random appearance prototype in 16 observed feature coordinates.
Each object has `k = prototype + 0.5 * independent_normal`, normalized to norm 4,
and an independently sampled two-dimensional landmark relationship `v` (each
coordinate uniform [-1,1]). A fixed seed-1729 orthonormal 8-by-2 projection P gives
relationship features `y(q) = P R(q) v`. Appearance and relationship are independent;
neither labels nor keys encode the target. Family/object IDs remain evaluator-only.
The learner receives feature arrays, measured cumulative action angle q, masks,
and executed incremental angles. P, v, R, and simulator objects are not learner inputs.

Training uses eight families, eight objects each, and 32 clean action pairs per
object: 2048 transition records / 4096 feature snapshots. Fit the feature operator
`M(a)y = cos(a) A y + sin(a) B y` by ridge regression. The trigonometric action basis
and reversible rotation family are **supplied scaffolding**; A/B are fitted only
from observed features. Train actions and orientations are uniform [-pi,pi].
Distinct namespace/family streams isolate training, development-selection,
development-calibration, confirmation, old-core probes, and unknown objects.

Acquisition supplies 0/1/2/4/8 distinct noisy snapshots of a new object at known q
uniform [-0.4,0.4]. A snapshot contains full stable appearance k and all eight
relationship channels with independent SD .02 noise. One snapshot permits one
write after canonicalizing with the fitted M(-q); no replay or optimization repeats.
Each snapshot is one distinct grounded observation, not a transition pair. Cumulative
angle is a supplied proprioceptive reference, not hidden landmark geometry. This is
easy correspondence through stable observed content, not correspondence discovery.

After acquisition, discard all transient activity and nonpersistent caches. Query
with eight randomly selected appearance coordinates plus SD .02 noise, **no**
relationship observation. Predict canonical relationship and an eight-action free
sequence (actions uniform [-0.6,0.6]); no future observation enters prediction.
Query sequences and views are independent of acquisition. They test transfer of a
supplied transformation family to a new association, not discovery of compositions.

Analytic identifiability: one noiseless snapshot at known q identifies canonical
relationship since R(q) is invertible on P's two-dimensional image. Before any
snapshot, v is independent of k, so the conditional mean relationship is zero.
Distinct continuous partial appearances distinguish a finite object set almost
surely without noise, but finite noisy cues can overlap. Include exact equal-cue,
different-target fixtures and retain all noisy errors; no unconditional recognition
guarantee follows. Shuffle query order and change evaluator IDs without changing
predictions. A known-cue confidence threshold cannot resolve identical evidence.

## Persistent and transient contracts

All models share one fitted A/B core (128 float64 values, 1024 bytes). Fixed P is
task infrastructure, counted separately (128 supplied bytes). Writable memory has
an identical **8192-byte cap**, including counters, key reconstruction, covariance,
and retained samples; actual allocations differ and must be reported. Total numerical
persistent cap is 9216 bytes per model including the common core, plus disclosed
scalar settings. No matching claim follows merely from the common ceiling.

The common recurrent state is initialized from the permitted partial key; memory
recall creates y, then `y <- M(action)y` advances once per physical step. Calling
reset replaces all transient arrays and caches with zeros/empty values, preserving
only declared persistent tensors. Evaluation and repeated queries are byte-identical
for all persistent tensors/settings. Acquisition rejects nonfinite inputs, invalid
shapes, or a wrong mode before mutation. No labels, IDs or filenames enter the API.
Explicit snapshot/restore supports exact rollback for verification, not performance
selection. Every snapshot/undo copy is temporary and its bytes are reported.

## Fixed inventory and finite tuning

All writers use always-write on the same snapshots. No novelty/reliability gate.

* **NOWRITE:** same core and observations; transient pre-reset state may assimilate
  a canonicalized snapshot, but post-reset y is zero and persistent memory is empty.
* **KV:** preallocated 32 rows of full appearance, running mean canonical relationship,
  and count (6400 bytes plus occupancy scalar). Match acquisition by observed key
  equality (stable appearance); query by masked nearest mean squared distance.
  No oracle object index. Capacity is never grown; exhaustion fails explicitly.
* **REG:** online sufficient statistics Sxx (16x16), Syx (8x16), and count. For observed
  cue coordinates O, predict `Syx[:,O] solve(Sxx[O,O]+lambda I, cue[O])`.
  This is a competent mask-aware local linear map, not a zero-filled full-cue shortcut.
  Reconstruct the full key with Sxx for a declared familiarity score.
* **FAST:** W (24x16), initially zero, maps a recurrent key state to reconstructed
  key and canonical relationship. Each grounded record t=[k, M(-q)y] makes exactly
  `W += eta (t-Wk) k^T / (k^T k)`; clip the Frobenius norm to 16 after each write.
  Each proposal has rank at most one before clipping. Query uses zero-filled cue
  scaled by `16 / max(sum(cue[O]^2), 1e-12)` before applying W once. This normalization
  gives exact single-pattern noiseless completion when eta=1. Use the identical
  direct map as an algebraic control, not an independent fit or extra replicate.

FAST is a structured cross-block recurrent memory; directional dynamics stay fixed.
Its unclipped write also equals one normalized squared-loss gradient step on W;
verify this algebraically against autograd, without counting it as another fit.
It does not test dense recurrent-core plasticity or require settling. No slow-weight
fine-tuning arm: estimating the known generic transformation anew would confound
association storage and general dynamics in this first test; independent-model reuse
and richer learned gates remain untested rather than claimed defeated.

Development roots 31001/31013 evaluate all pairs of core ridge [1e-6,1e-3] and
FAST eta [.25,.5,1], REG ridge [.01,.1,1]; KV/NOWRITE have no writer tuning. Select
the core by old-core free-8 error, then each writer by equal-weight mean of D1 J
and D2 final old-object free-8 error. Break ties by manifest order. No new settings.
Select the strongest conventional reference (KV or REG) by that same composite.
Report FAST against **both** regardless of selection. All roots/candidates get equal
observations; offline exposure and unequal tuning compute are disclosed.

Separately calibrate familiarity thresholds on two independent development-calibration
streams: 95th percentile known-object score after D2, pooled within model. KV uses
nearest squared key distance; REG/FAST use observed-coordinate reconstruction MSE.
Empty memory always rejects. Thresholds do not gate raw predictions or writes.
These scores are not probabilities, and “accepted wrong recall” is not calibrated
posterior overconfidence. Unknown-object rejection is diagnostic, not D3 reliability.

## D0, D1, D2 and endpoints

D0 tests exact analytic acquisition, complete reset, no-write inference, snapshot
restore, identity/future independence, split separation, direct FAST equivalence,
finite storage and a known ambiguous pair. Reproduce existing scientific-invariant
fixtures through the full repository suite. A timing fixture runs the full D1/D2
inventory at one fresh fixture root before development, with twice the projected
remaining time/storage and RSS below the ceilings. No confirmation is inspected.

D1: 24 independent objects (one per new family) per fitted root; eight partial-cue
queries per object and each budget. Primary J is free-8 NMSE equally averaged over
budgets 1/2/4/8. NMSE denominator is training snapshot mean squared feature amplitude,
frozen per root, with floor 1e-8. Report canonical, free-1/free-4/free-8 and every
budget, including zero. Association accuracy is fraction of queries with canonical
NMSE <=.1, independent of acceptance; accepted-wrong is accepted and NMSE >.1.

D2: four independent sequences of eight similar objects from one new family each;
eight observations per object. After every acquisition, reset and query every seen
object with the same held-out queries, without writing. Retention is final free-8
error minus error immediately after that object's acquisition, averaged over the
first seven objects. Also report the full lower-triangular retention matrix, final
old-object accuracy and errors. Test eight unacquired same-family objects per sequence
after the final acquisition for false familiarity. No capacity/size sweep.

Old-core probe: 64 separate held-out trajectories/root initialized from observed
full relationship features; compare core free-8 before/after writes. Core tensor
identity is mandatory; each root's probe NMSE must be <=.02 for valid general dynamics.
This protects the shared motion function only; the D2 guard protects object recall.

## Frozen inference and outcome rules

Ten independently fitted roots are the independent units. Objects/sequences and
timesteps are averaged within roots. Paired bootstrap uses 20000 resamples and a
fixed seed, family-adjusted alpha .05/20 for the following 20 quantities: for each
of KV/REG/FAST, D1 gain over NOWRITE, retention difference, final-old accuracy, D1
budget-eight accuracy, budget-eight free-8 error (15); FAST gain over KV and REG (2);
the three writers' one-shot gain over NOWRITE (3). Descriptive metrics use ordinary
95% root intervals, labelled separately. No timestep-level independence claim.

Persistent acquisition supported for a writer only if D1 gain point >=20%, adjusted
lower >0, width <=.4, D1 budget-eight accuracy lower >=.8, budget-eight error upper
<=.15, retention upper <=.02, and final-old accuracy lower >=.8. One-shot support
additionally requires its separate one-shot gain >=20% and lower >0. A claim refers
to this scaffolded family, not arbitrary one-shot structure learning.

FAST practical advantage requires all acquisition guards, paired relative J gain
>=10% against **both** conventional controls, lower >0 and width <=.4. Gain is
`(reference-candidate)/max(reference,1e-6)`. An upper bound <.10 with width <=.4
is precise negative practical-benefit evidence for that contrast. Otherwise it is
inconclusive; failed guards are separately reported, with a positive lower bound
on excess retention >.02 an established interference failure. If floor denominators
dominate a conventional comparison (reference J<1e-6), report absolute differences
and classify relative benefit uninformative rather than pass. All validity/invariant
failures are invalid execution, not scientific negatives. A memory can fail these
strict criteria while showing a smaller genuine learning effect.

The older review's proposed 20% acquisition gain is retained for acquisition versus
no-write. This first mechanism test uses 10% relative advantage over strong adaptive
controls; .02 retention allows modest noise/generalization cost, but absolute .8
accuracy prevents an easy non-regression pass by uniformly bad memories. These are
engineering margins chosen before fitting, not biologically established constants.

## Execution, resources, provenance and stopping

CPU/PyTorch, one thread, deterministic float64 calculations. Fixed sensor never fits.
Phases: fixture, development, freeze, confirmation, repeat, report. Enumerate every
configuration/root; save inputs, predictions, errors, checkpoints, selected settings,
failed records, timestamps and a phase ledger. At most 40 offline fits, including
fixture/development/confirmation/repeat. No adaptive extensions or replacement seeds.
Two core settings x two development roots = four development core fits; one fixture
fit, ten confirmation fits, one prescribed repeated fit; the cap leaves room for
documented engineering repair but never authorizes extra scientific configurations.

Freeze selected settings, thresholds, source/config hashes and immutable source
snapshot before generating confirmation. Repeat the first complete root, checking
all numerical inputs, memories and predictions exactly (timings excluded). Independently
reduce saved errors and verify no historical C source hash changed. Commit scientific
source before research runs and disclose non-source working-tree changes.

Ceilings: 7200 numerical CPU seconds, 14400 execution-wall seconds, 2 GiB RSS,
2 GiB all D artifacts. Charge fixture, tuning, calibration, failures, confirmation,
repeat, profiling, plotting and audits. Phase import/startup and engineering overhead
are explicitly separate. Stop before 90% CPU/wall to reserve reporting. Software
failures preserve records; any source repair gets a new identity and compatible
fresh streams if scientific meaning changes. No silent extension after imprecision.

Required report: paired acquisition/retention curves, failures, actual parameter,
persistent/active/temporary-memory counts, measured read/write latency, exposure,
resource Pareto table, uncertainty, source/environment and repeat records. Recommend
at most one bounded next experiment without executing it. D3/D4 remain deferred.
