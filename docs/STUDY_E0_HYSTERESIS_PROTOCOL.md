# E0-HYS v1 state hysteresis and navigability

**Current status — superseded as the next execution path, not run.**
[SOAM-103](../tickets/SOAM-103-assembly-organization-plan.md) now selects
[Assembly organization and selective routing](proposed-studies/STUDY_ASSEMBLY_ORGANIZATION.md)
for mathematical/protocol design. E0-HYS remains a preserved retention diagnostic
and is not an AO-1 prerequisite. Its numerical contract and manifest are unchanged;
the historical design acceptance below is not current execution selection.

November 22, 2026 · [SOAM-102](../tickets/SOAM-102-state-hysteresis-protocol.md)
owns this protocol and lightweight RFC. The [owner selection](requests/state_hysteresis_2026_11_22.md)
covers design. The [manifest](protocols/study_e0_hys_v1.json) fixes the proposed
numerical contract; implementation and execution have not started. Classification:
**essential next at SOAM-102 adoption; currently unselected**. The [concept proposal](proposed-studies/STUDY_E0_HYSTERESIS.md)
records the broader, conditional assembly-routing hypothesis.

## Decision and claim

Test whether heterogeneous local state hysteresis reduces 128-step zero-action
orientation error beyond competent ordinary NAV-family updates, while preserving
action navigation, sensory correction and local perturbation recovery. Test the
additional contribution of heterogeneity separately against uniform hysteresis.

E0-HOLD reduced NAV32 stationary error to 5.698°, but failed its declared joint fix;
recovery noninferiority remained unresolved. Its [decision](../reports/STUDY_E0_HOLD_DECISION.md)
recommended a conditional optimization-budget comparison, which was not activated.
The new owner request selects this mechanism design instead. No historical result
or criterion changes, and the proposed numerical allocation is fresh.

The first test has one continuous orientation and cannot establish learned
assemblies, hierarchical routing, storage capacity, useful shared-neuron functions,
or neuroscience. More stable state is not automatically more accurate state.

The owner's connectivity clarification is recorded in the
[proposal](proposed-studies/STUDY_E0_HYSTERESIS.md#connectivity-and-the-missing-hierarchy-mechanism).
The present symmetric zero-action core and dense sensory interfaces do not specify
a root-to-leaf routing mechanism. Hysteresis alone provides no theoretical reason
to expect such organization. This clarification changes no numerical contract;
an experiment on learned routing would first need a different, explicitly reviewed
connectivity/learning hypothesis.

## State and update equations

Use one state vector h in R^32, the existing learned initializer E, readout D and
sensory correction C. Preserve the fixed 12-by-2 sensory projection, twelve mask
indicators, one scalar action and prediction-before-correction ordering.

Define S=(W+W^T)/2, K=(V-V^T)/2 and

`q(h,a; alpha) = (1-alpha) * h + alpha * tanh(S h + b + (a/0.12) K h)`.

Multiplication by alpha is elementwise; scalar alpha broadcasts. This is the
column-vector form of the existing NAV32 implementation. Action is applied once
per physical interval. Neither S nor the added operator implies an energy descent
guarantee for the full asymmetric discrete system.

For hysteresis models, first compute q with alpha=.5, then apply

`P_delta(q,h)_i = max(q_i-delta_i, min(q_i+delta_i, h_i))`.

Equivalently, return q_i-delta_i when q_i-h_i>delta_i, q_i+delta_i when
q_i-h_i<-delta_i, and h_i otherwise. This is a discrete play operator whose
retained output is h. It has no additional dynamic state or hidden input
accumulator. For positive delta, repeated identical q does not make an interior
output approach q, unlike a leaky update. Under driven upward/downward sweeps its
branches differ. This local property does not prove useful network attractors.
See [Esbrook, Tan and Khalil](https://doi.org/10.1109/TAC.2013.2281859) for the
standard play element; this network coupling is the proposed intervention.

Use the exact piecewise rule in training and evaluation. Autodifferentiate the
selected branch; at equality choose the retained-h branch. No straight-through
estimator, smoothing, threshold annealing or learned thresholds. A delta=0
implementation fast path returns q exactly, including its gradients, to recover
NAV32. Fixed threshold buffers are never optimized. The hard deadband can limit
gradient flow; failures are scoped to this rule and fitting budget.

Initialization remains `tanh(E([z*mask,mask]))`. Correction remains

`h_post = h_prior + .5*tanh(C([(z-D(h_prior))*mask,mask]))`,

with exact identity when all mask entries are absent. Apply hysteresis only to
autonomous/action prediction, not to correction or initialization. Correction
changes h itself, so the next prediction begins from the corrected play state;
there is no stale second latch. This isolates retention dynamics and permits
grounded correction. It does not test rejecting distracting sensory evidence.

## Fitted families and supplied structure

| Family | Update and finite configuration grid | Purpose |
| --- | --- | --- |
| NAV32 | q, alpha=.5 | Current recurrent reference |
| LEAK32 | q, uniform alpha in {.1,.25,.5} | Ordinary slow-update control |
| HLEAK32 | q, alpha_i=lambda*u_i; lambda in {.1,.25,.5}; sixteen u=.5 and sixteen u=1.5 | Heterogeneous ordinary timescales |
| HYS32 | P(q,h), all delta_i=rho; rho in {.0005,.002,.008} | Uniform hysteresis |
| HHYS32 | P(q,h), delta_i=rho*v_i; same rho grid; sixteen v=.25 and sixteen v=1.75 | Primary candidate |
| HSYM32 | Same as HHYS32 with K=(V+V^T)/2 | Symmetric action-connection control |
| GRU32 | Existing GRUCell and observation interfaces | Conventional recurrent reference |
| PCA2 | Existing fitted rank-two estimator, ridge=1e-6 | Strong accuracy/storage reference |

For each independent root, generate one random permutation of 32 unit indices,
independent of observations and initialization. The first sixteen receive the
lower coefficient in HLEAK/HHYS/HSYM; the other sixteen receive the higher one.
The same assignment is used for every configuration within that root. Both
coefficient distributions have mean one; their functional roles are not supplied.
This fixes heterogeneity before learning. No tree, sparse connectivity, assembly
labels or interpopulation attention is imposed. Same mean coefficients do not
imply matched activity, effective timescales or exact functional capacity.

The owner explicitly selected fixed thresholds for this first test. Backpropagation
updates E/D/C/W/V/b through the declared dynamics; it does not optimize delta or
assign semantic roles. Representational specialization may arise through those
weights, but unused units and absence of specialization remain valid outcomes.
Learned threshold allocation is outside this inventory.

All seven neural families use learning rates {.001,.003}. NAV/GRU have two
configurations each; the five other neural families have six each; PCA has one.
Total: **35 configurations per development root**. NAV32 and LEAK32 at alpha=.5
deliberately overlap and must reproduce exactly at the same rate/root; their
declared fit slots count even if an implementation later shares an immutable
result with explicit provenance. No released slot funds an extra fit.

NAV-derived families share identical E/D/C/W/V/b initial tensors at a root, including
HSYM before applying the different K constraint. GRU uses its own initializer
stream. All families/configurations receive identical training data within a root.
Parameters, optimizer updates and observation exposure are matched within the NAV
family; tuning counts and runtime differ and must be reported.

Expected accounting from existing code: NAV-derived models have 4,044 fitted
scalars, 32 active floats and a 32-float prior workspace; GRU has 5,324 fitted
scalars and 32 active floats; PCA has 52 persistent scalars and six active floats
including covariance. LEAK/HLEAK/HYS/HHYS/HSYM additionally serialize a 32-float
fixed coefficient buffer (128 bytes). Count any actual extra workspace, temporary
branches, readouts, masks, common projection, optimizer state and artifacts in the
implementation ledger. Dense prediction retains O(32^2) work; sparse activity does
not establish sparse computation or logarithmic retrieval.

## Training and independent streams

Use the E0-HOLD LONG128 objective unchanged in meaning: 600 Adam updates, batches
of 32 original 24-step episodes, gradient-norm clip 1, cosine learning-rate decay
to 1% of the initial rate. Extend only all-zero-action episodes to 128 steps,
repeating the already supplied stationary sensory target with no additional cues.
Average prior NMSE plus .5 posterior NMSE within each episode, then weight episodes
equally. No geometry loss, action-reversal loss or pose labels enter training.
PCA fits the same original prefix corpus with its existing two passes.

The original action alphabet is {-.12,-.06,0,.06,.12} rad/step in blocks of four;
one quarter of episodes are explicitly made stationary. Initial phases are uniform.
Visible observations contain either six or twelve channels with equal probability,
noise SD .01, and the original intermittent cue schedule. Each neural fit sees
19,200 episodes and 480,000 original sensory snapshots. Repeated stationary targets
and PCA's second pass are processing, not new observations. Ground truth angle and
the inverse projection belong only to task construction/evaluation.

Use namespace `soam-e0-hys`, version 1. Development roots are 401,402,403;
confirmation roots are 501–520; fixture root is 9501. For each split/root compute
`mapped = derived_seed(namespace,1,split,root,0,"base-stream")` and use mapped
as the root of the unchanged E0 split generators. Training remains in E0's train
split; development/confirmation evaluation remains in its respective split.
Record both root values. New probe streams, initialization and permutations use
separate named components under the new namespace, all at index 0: `probe-grid`,
`stationary-cued/phase`, `stationary-cued/mask`, `stationary-cued/noise`, `nav-init`,
`gru-init` and `permutation`. Use `derived_seed(namespace,1,split,root,0,component)`.
The common probe grid is `2*pi*arange(256)/256 + uniform(-pi,pi)` from its own stream.
No historical checkpoint, confirmation stream or selected hyperparameter is reused
as unseen evidence.

Use final-update checkpoints only. Select configurations once on development data
using the rule below; commit the selection and complete development results before
opening confirmation. Evaluation never writes weights, coefficients or fitted
statistics. Cloned states used for paired probes are evaluator resources, not a
second memory available to the candidate during normal inference.

## Evaluation battery

Retain E0's seven endpoints and definitions: blindfolded action NMSE at 64 steps,
grounded one-step NMSE, zero-action absolute pose error at 128 steps, 16-step normal
separation ratio, perturbation-induced pose error, tangent retention, and final
returning-cue NMSE. Use evaluation batch 128, geometry grid 256, burn-in eight,
normal perturbation .1 times mean family radius and tangent separation four bins.
All ordinary E0 interpolation/extrapolation/direction diagnostics remain reported.

The original geometry uses a clean full initial cue, then no cues. Its recovery
measure compares two trajectories normal to a sampled evolving family; both can
drift. It is not basin volume or proof of an invariant manifold. Report absolute
pose error and displacement from the model's initial decoded pose separately.
For retention curves continue the stationary trajectory to 512 steps, saving
readouts at 0,1,4,16,24,64,128,256,512; only step 128 is confirmatory.

The following new probes use the fixed projection and a fresh 256-pose grid with
a root-specific uniform angular offset, shared across model families. Start from
a clean full cue unless specified. No observations arrive during blindfolded
probes. Phase decoding uses the existing evaluator-only inverse projection.

**Small actions.** For each magnitude {.001,.003,.01,.03} rad/step and each sign,
roll out 64 constant-action steps and a zero-action companion from the identical
initialized state. At t=16 and 64 compute unwrapped decoded displacement as the
sum of successive principal wrapped angle differences. Let
`R=(displacement_action-displacement_zero)/(t*a)`.
Define `small_action_error` as the maximum, across magnitude/sign/time cells, of
the mean over poses of `abs(R-1)`. Thus stalling yields error approximately one.
Also report absolute true-pose error, per-cell signed response, quantiles and
fractions of stalled (abs(R)<.1) and wrong-direction (R<0) poses, with
5th/50th/95th percentiles. Companion subtraction isolates action
response but cannot erase the separate absolute retention/navigation requirements.

**Reversal.** For magnitudes {.003,.03,.09}, each sign, drive 32 steps in one
direction. From that same reached state fork a reversed-action and zero-action
companion. Compute R relative to the reversed command at 4,16,32 subsequent steps.
`reversal_error` takes the same maximum-of-pose-mean absolute response-error reduction.
Archive the complete outward/return readouts and true-pose closure errors.

**Release after holding.** Hold the initialized state for 128 zero-action steps,
then fork action and zero-action paths for magnitudes {.003,.03,.09}, both signs.
Compute R at 4,16,64 steps. `release_error` is the same worst-cell mean error.
This prevents a long hold from silently destroying the ability to move again.

**Small perturbations.** Repeat E0's normal-direction probe at .01 times the
same reference-family radius, using the same normalized perturbation directions
as the .1 probe. `small_normal_ratio` is the mean final normal separation divided
by the injected norm after 16 zero-action steps. Report pose effects too. Together
the two amplitudes expose a deadband that preserves small errors while apparently
recovering larger ones. Neither amplitude tests recovery of arbitrary tangential
errors to an unobserved true pose, which is generally unidentifiable.

**Stationary with observations.** Use 128 episodes, uniform fixed physical phase,
128 zero-action steps and a cue at every time including initialization. At each
cue choose six or twelve channels equiprobably and add independent SD .01 noise
on visible channels. Score prior predictions before each current cue.
`stationary_cued_nmse` is 12 times mean squared prior feature error over all
episodes/steps/channels. Record posterior error and decoded drift separately.
This complements the blindfolded stationary condition rather than replacing it.

Every new cell is first reduced within a trained root. Timesteps, signs, magnitudes
and poses do not add independent experimental replicates. A decoded feature vector
with inverse-projected norm below 1e-6 cannot provide a valid angle. Record all
degenerate cases; never silently drop, impute or replace roots.

## Development selection

Evaluate the whole battery for every declared development configuration. Average
each root-level endpoint across the three roots. Use the nonstationary absolute
requirements in the inferential table as development guards, including the small
action/reversal/release, small-perturbation and repeated-cue requirements. Exclude
stationary error, comparative gains and paired degradation criteria from this
selection-guard set.

For a guarded endpoint with allowed range [L,U] and declared scale s, define
`v=max(0,(L-x)/s,(x-U)/s)`, omitting missing bounds. Scales are .05 for NMSE,
.5 for normal ratio, 3 for induced degrees, .2 for tangent ratio, .2 for each
action-response error, and .8 for small normal ratio. Degenerate geometry gives
infinite violation. Select within each family lexicographically by
`(max(v), sum(v), mean_stationary_deg, mean_free_nmse, canonical_config_id)`.
Canonical IDs sort family name, then rate, then alpha or rho in numeric ascending
order; ties never depend on confirmation results.
Undefined selection quantities sort as positive infinity; do not omit their roots.
All configurations and violations are reported, including unsuccessful controls.

Select comparator C among the selected NAV32, LEAK32 and HLEAK32 configurations
using the same ordering, with the named family as final tie-break. C is fixed
before confirmation. If none satisfies every development guard, label the
reference unqualified: absolute candidate capability can still be assessed, but
the practical comparative claim is inconclusive. GRU/PCA/HSYM remain mandatory
reported references; C's selection cannot imply superiority over them.

## Confirmatory family and decision rules

Let H=selected HHYS32, U=selected HYS32 and C=the development-selected ordinary
NAV-family reference. The primary gain is `stationary_deg(C)-stationary_deg(H)`.
All contrasts are computed within paired independent confirmation roots.

| Quantity | Required confidence interval | Maximum width | Count |
| --- | --- | --- | ---: |
| H stationary absolute error at 128 | upper <=5° | 4° | 1 |
| C minus H stationary error | lower >=1° | 2° | 1 |
| H blindfolded, grounded, returning-cue NMSE | each upper <=.05 | .04 each | 3 |
| H normal ratio at amplitude .1 | upper <=.5 | .4 | 1 |
| H induced pose error at amplitude .1 | upper <=3° | 3° | 1 |
| H tangent retention | interval within [.8,1.2] | .4 | 1 |
| H minus C blindfolded, grounded, returning-cue NMSE | each upper <=.01 | .02 each | 3 |
| H minus C normal ratio at amplitude .1 | upper <=.05 | .10 | 1 |
| H minus C induced pose error at amplitude .1 | upper <=.5° | 1° | 1 |
| H small-action, reversal, release errors | each upper <=.2 | .2 each | 3 |
| H small normal ratio at amplitude .01 | upper <=.8 | .4 | 1 |
| H stationary-cued NMSE | upper <=.05 | .04 | 1 |
| U minus H stationary error, secondary heterogeneity claim | lower >=.5° | 2° | 1 |

There are **19 simultaneous intervals**: eighteen quantities for the primary joint
claim and one secondary contrast. Bootstrap the twenty independent paired roots
with 50,000 resamples, seed 52203, two-sided alpha=.05/19, percentile quantiles using
NumPy's linear interpolation. Use one shared root-index resample matrix across
quantities. Report unadjusted 95% intervals and all root values as well. Control
family summaries and unlisted contrasts are descriptive, with 95% root intervals.

The five-degree target and original absolute/paired guards carry forward E0-HOLD.
One degree is a new practical gain threshold for the smaller remaining error;
half a degree asks whether heterogeneity adds a meaningful increment beyond
uniform hysteresis. A response error of .2 allows at most 20% mean relative
transport error in the worst declared cell. The .8 small-normal bound requires
measurable recovery even for small perturbations. These are engineering choices
for this task, not physiological constants or promised power. Fixed twenty-root
sampling may still be inconclusive; do not add roots in response to its intervals.

Apply the following rules in order:

1. Leakage, corrupted provenance, implementation error, failed exact repeat,
   nonfinite execution or an incomplete budget-limited inventory is **invalid or
   incomplete execution**, with the cause recorded. It is not scientific falsification.
2. Finite representational collapse/undefined geometry in any required H confirmatory
   evaluation at any root fails the all-root usability requirement. Report
   **negative for this configured joint capability** and the degenerate-root count; no bootstrap claim is made for
   an undefined metric. Descriptive holds beyond 128 steps and derived diagnostic
   interventions do not enter this usability gate. Do not exclude a failed root
   to obtain a passing interval.
3. Apply each interval's precision cap before classifying its direction. An
   adequately precise paired degradation wholly above a margin is a **tradeoff**.
   Any adequately precise absolute guard wholly outside its allowed range, or a
   primary-gain interval wholly below one degree, is **negative for the primary
   joint claim**. Preserve other inconclusive quantities in the report.
4. Otherwise support the primary claim only if all eighteen intervals pass and C
   was qualified on development. Remaining cases are **inconclusive**. A wide
   interval is not equivalence; no margin crossing is rounded into a pass.
5. Support the secondary heterogeneity claim only when the primary claim passes,
   U satisfies the development qualification guards, and its nineteenth interval
   passes. A precise gain below .5° rejects that practical increment; unresolved
   evidence stays inconclusive. If the primary claim fails, report the secondary contrast without promoting it to a success.

If C has undefined required metrics, its associated comparative intervals are
unavailable and cannot pass; retain all roots and classify the comparison as
inconclusive unless a valid absolute H failure already determines a negative
result. Undefined U metrics similarly prevent the secondary claim. Failures in
other controls are reported with their root counts, not hidden by exclusions or
substituted models. Absolute H capability remains separately interpretable.

A supported retention result licenses a scoped mechanism conclusion only. It does
not pass a hierarchy, sharing, acquisition, control or biological-validation gate.

## Fixed diagnostic interventions

On each confirmation root and the prescribed repeat, evaluate three additional
conditions without fitting or selecting settings:

- **FREEZE0:** from fitted NAV32, replace prediction by identity when the supplied
  action is exactly zero; retain normal prediction otherwise and normal correction.
  This is a supplied hold rule, not learned recovery. Its normal ratio should expose
  why exact stationary retention alone is insufficient.
- **HHYS remove:** evaluate the fitted HHYS32 checkpoint with every delta=0.
- **HHYS swap:** exchange the low/high coefficient assignments in that checkpoint,
  preserving their histogram and mean.

Run the full battery for these three conditions. They add 63 evaluations across
twenty roots plus the repeat, zero fits. Fitting histories remain unchanged.
Intervention effects show dependence on the chosen coefficients and their alignment
with fitted weights, not proof of selective routing or semantic assemblies.

Record per-unit state variance, fraction of predictions held exactly, distribution
of proposed/realized increments and norms of S/K/D. These are descriptive diagnostics
in the chosen neuron basis; do not cluster them on confirmation data and label the
result a discovered hierarchy. No post hoc selection feeds back into fitting.

## Inventory and resource ceiling

Development: 3 roots × 35 configurations = **105 fits**. Confirmation: 20 roots ×
8 selected families = **160 fits**. Exact full-fit/full-evaluation repeat of all
eight selected families at root 501 = **8 fits**. Maximum scientific inventory:
**273 fits**, plus the 63 derived diagnostic evaluations. Repeat arrays, coefficients
and parameters exactly; exclude timings from equality checks.

Before science, perform at most eight engineering fixture fits, one per family,
at root 9501, eight optimizer updates and batch 32. Use rate .003, alpha=.25 for
LEAK/HLEAK and rho=.008 for hysteresis families; retain actual 24/128 horizons and
the full evaluation battery for runtime/artifact projection. Fixtures are not
tuning data. Operator/invariant checks use deterministic synthetic tensors and no
additional fits. There are no exploratory fits, seed replacements, adaptive grid
extensions, checkpoint searches or automatic retries.

Cumulative ceilings, including fixtures, development, confirmation, repeats,
diagnostics and numerical postprocessing: **14,400 CPU seconds, 28,800 execution
wall seconds, 2 GiB RSS and 4 GiB numerical artifacts**. Single CPU thread,
deterministic Torch, float32 recurrent operations and float64 fitted/statistical
reductions; no GPU or paid compute. These are maximum design allocations, not
measured runtimes. Prior LONG128 NAV32 fitting cost about 9.63 CPU seconds per fit;
this only motivates feasibility and does not time the new hard operator.

Preflight projects the entire fixed inventory with a 2x margin below 80% of each
time and artifact ceiling and below the RSS ceiling. Stop before scientific fits
if infeasible. A versioned, reviewed redesign may reduce work; do not spend an
undefined budget or silently extend a ceiling. Check resources during fitting and
evaluation, preserve partial artifacts and the stopped inventory, and do not restart
failed science without a fresh recorded decision.

## Implementation and audit requirements

Use a new module and protocol path; preserve historical navigation/hold numerical
files and archived hashes. Reuse their functions only when contracts agree. A
future implementation must run the existing full suite before modifying code and
complete these checks before scientific fitting:

- delta=0 equivalence to NAV32, LEAK alpha=.5 equivalence, all-zero-mask identity,
  exact common initialization/data streams, no-write inference and deterministic repeats;
- scalar play history loops, retained interiors under constant input, coefficient
  histogram/mean, and gradients on either side of boundaries with the declared
  equality convention; correct h ownership after sensory correction;
- a frozen-state synthetic control fails normal recovery and action-response guards;
  an analytic rotation evaluator fixture has unit response, including reversal and
  release; these fixtures are not eligible trained competitors;
- probe denominators/signs/unwrapping, separate initial-pose displacement and absolute
  error, correct E0 geometry reuse, no future observation/angle access by models;
- independent split namespaces, development-only selection, exactly nineteen
  interval quantities and independent-root resampling; validate decision edge cases;
- full resource inventory, finite execution ledger, immutable source/selection,
  atomic checkpoints and a raw-array independent reducer.

Before development freeze the implementation commit, protocol/manifest hashes,
software versions, device/numerics and data-generation identity. Before confirmation
commit all selected configurations and C; a dirty source cannot start confirmation.
Every result stores source fingerprint, root/mapped seeds, coefficient assignment,
training-data hashes, exposure/update counts, timings, parameter/state/storage
counts, checkpoints and raw readouts/geometry sufficient for independent reduction.
Save learning traces and per-root failures rather than only successful averages.

Expected future deliverables are a development-selection record, harness/preflight
report, empirical report, raw-root table, paired retention/navigation/recovery plots
and a scoped decision. These are future outputs, not existing result links.
SOAM-102 accepts design only; no fit, hierarchy study or publication is completed
by this document.
