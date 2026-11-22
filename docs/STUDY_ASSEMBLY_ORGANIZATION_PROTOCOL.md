# AO-1 assembly organization and selective routing

November 22, 2026 · [SOAM-104](../tickets/SOAM-104-assembly-organization-protocol.md)
· [Numerical manifest](protocols/study_ao1_v1.json)
· [Planning scope](proposed-studies/STUDY_ASSEMBLY_ORGANIZATION.md)

This protocol tests one proposed organizing pressure: connection cost plus activity
regulation during offline prediction learning. The candidate is an ordinary
directed leaky recurrent network with dense fixed sensory access. The question is
whether that pressure develops **one reusable, selectively mediated route** beyond
the same recurrence without the pressure and an initially random, frozen core,
while retaining useful prediction, memory, action response and perturbation recovery.

The numerical manifest owns constants, inventories and decision thresholds; the
equations and algorithms here define their meanings. The [design audit](analysis/AO1_DESIGN_AUDIT.md)
contains untrained algebra checks. Implementation and scientific fitting are
SOAM-105/106, not part of this protocol decision. No measured organization result
is available. Hysteresis is absent in v1: the selected intervention concerns learned
connections, and recurrence already supplies a candidate persistence mechanism.
The owner's fixed-threshold preference remains applicable if a later selected
version includes explicit hysteresis. E0-HYS stays unrun and unselected.

## Decision and scope

ORG96 is compared primarily with PLAIN96 and FROZEN96. The additional symmetric,
separated, GRU and polynomial controls are mandatory scientific references. This is
not a claim that a new neuron model, Hopfield dynamics, or physical overlap uniquely
causes a benefit. A tree, multiple hierarchical levels, unsupervised semantic
categories, online acquisition, and biological plausibility are outside the primary
claim. A useful graph is an allowed outcome; a positive route result cannot be
reported as a discovered tree.

The original [E0](../reports/STUDY_E0.md) remains inconclusive, and
[E0-HOLD](../reports/STUDY_E0_HOLD.md) remains negative for its declared joint fix.
AO-1 does not assume that their drift problem is solved. It changes task and model
interfaces under a fresh contract, preserving all historical source/results.

## Task and information boundary

Each episode contains one synthetic object, with attributes b0,b1,b2 in {-1,+1}
and angles theta,psi. The transition is

```text
g = 1 if b0=-1 else 1.5; o = (b1+1)/2
theta_next = wrap(theta + g*a0)
psi_next   = wrap(psi   + o*a1)
v = [cos(theta), sin(theta), cos(psi), sin(psi), b0, b1, b2,
     b2*cos(theta), b2*sin(theta)]
z = Q v
```

wrap maps to [-pi,pi). The two actions respectively rotate the object and move an
articulation only when o=1. Both initial angles are independently uniform. The six
attribute combinations other than (-1,-1,-1) and (+1,+1,+1) are available to fitting
and route discovery. Those two combinations are held out from both. Each attribute
value, action applicability and rotation gain is represented during training.
Choose training tuples uniformly and independently per episode; evaluation and
discovery instead use their explicitly balanced tuple inventories below.

Q is a fixed 12-by-9 orthonormal-column Gaussian QR map. Its seed is
derived_seed("soam-ao1",1,"fixed",0,0,"sensor-projection"). Generate in float64,
flip QR column signs so R's diagonal is nonnegative, and preserve the float64
evaluator map plus float32 observations. Q and its inverse are task/evaluator data,
not model inputs or a supplied decoder. Clean sensory energy is exactly ||z||²=6.

Models receive noisy observed z, a twelve-bit availability mask, and two actions.
Noise is independent Gaussian .01 per observed channel; unavailable channels are
zero. The initial cue is full. At later ordinary training ticks, a cue is present
with probability .5; if present, six uniformly selected channels or all twelve
are observed with equal probability. Missing cues have all-zero masks. Action
components are sampled independently from the training grid in the manifest and
held for blocks of four transitions. Angles/attributes, object IDs, Q, function
labels, route membership, and correct future features cannot enter model inference.

Each batch has four explicitly stationary episodes, randomly assigned among sixteen.
Other episodes use the action sampler; if both action sequences are entirely zero,
set a0 throughout the first four-transition block to .06. Stationary episodes have the same 32-step
observation schedule, then extend to 64 with no further observations and a repeated
final stationary target. This is extra processing of existing evidence. Generator
labels identifying stationary examples only select the loss duration.

Training targets are clean observed features; all families may use that same
finite corpus, including earlier targets as system-identification data. No hidden
factor loss is supplied. POLY12 uses clean current/successor training pairs; neural
models fit through noisy partial-input trajectories. This is a disclosed fitting
method/prior difference, not extra ground-truth information or equal computation.

## State, dense input, and prediction

All neural models have one transient state h and a learned linear sensory readout
D h+d. Their fixed input P has N rows and 24 orthonormal columns. Generate it as
for Q using fixed components neural-input-96 or neural-input-168; all same-width
families/roots share P. It is never fitted, masked by neuron identity, or assigned
root/leaf roles. Input width does not scale with N: the candidate has N/d=96/24=4,
counting masks. Define

```text
s(z,m) = tanh(P [m*z, m])
initialize(z,m) = s(z,m)
correct(h,z,m) = h                         if no channel is observed
                 .5*h + .5*s(z,m)          otherwise
```

These fixed interfaces expose every neural unit to sensory drive. They are simpler
than E0's learned initialization/correction maps and constitute declared scaffolding.
There is no learned sensory gate hiding entry masks. P preserves total input norm
before tanh; SEP168 therefore has lower average per-neuron input power at the same
total drive. No population-size scaling claim is made from this control.

For ORG96, PLAIN96, SYM96, SEP168 and FROZEN96, with u=a/.12:

```text
A(a) = R + u0*K0 + u1*K1
predict(h,a) = .5*h + .5*tanh(A(a)*h+b)
```

R and both K matrices are independently directed except in SYM96, where all three
are symmetric. SEP168 has three uncoupled 56-unit blocks in those matrices, with
one dense readout and dense input access; its groups are supplied control structure.
The candidate contains no supplied groups. Diagonal connections are permitted;
their dominance is an interpretable non-routing outcome.

The order is initialize -> readout -> predict once per executed action -> score
the prior against the next sensory target -> correct using that tick's available
evidence -> readout/score posterior. Internal analysis must never repeat a physical
action or use the next cue before prior scoring. All parameters and fixed buffers
are frozen during evaluation and counterfactual interventions.

## Learning rule and constraints

Let E_t be ||z_hat-z||²/6. Each episode's task loss is its time-mean prior E plus
.5 times its time-mean posterior E, including initialization. Each episode receives
equal total weight irrespective of its 32/64-step length. Use the final checkpoint
after 800 Adam updates, batch sixteen, gradient norm clip one, the four declared
rates, and cosine decay to .01 of the initial rate at update 799. No checkpoint
selection, restart, extra observations, or adaptive optimizer extension is allowed.

Only ORG96 adds

```text
L_conn = (sum_ij |R_ij| + |K0_ij| + |K1_ij|)/(3*N)
p_i = mean_over_episodes(mean_over_posterior_times(h_i²))
L_act = mean_i (p_i - .1)²
L = L_task + .005*L_conn + .1*L_act
```

This is a bundled intervention. It tests whether economical connections and a soft
activity-power target help organize useful pathways. It does not isolate the two
penalties' individual contributions. The target is a soft power constraint, not
equal instantaneous firing, a tree label, or a biological homeostasis claim. The
cost coefficients are fixed engineering choices: connection cost is bounded by
about .0067 under the caps below, and activity cost by .081 for bounded states.
They can compete with small prediction errors without replacing the task loss.
No theorem states that their minima are hierarchical, sparse, or semantically useful.

After each optimizer step, symmetrize SYM matrices, then apply

```text
cap(B,c) = B * min(1, c / max_i sum_j |B_ij|)
```

using the identity factor when B=0. Cap R at two, each K at one, each readout row
at sixteen, and clip recurrent/readout biases to [-1,1]. Apply the same constraints
to all leaky neural controls. For SEP, apply the recurrent cap to each stored block.
The global scale preserves symmetry; per-row scaling would not. Adam moments are
not projected. PLAIN/SYM/SEP omit both organizing penalties but retain these norm
constraints; differences are not attributed to a hidden hard sparsity mask.

Initialize R=I+Gaussian(.1/sqrt(n)) and K=Gaussian(.01/sqrt(n)), where n is the full
width or SEP block width. Initialize D=Gaussian(1/sqrt(N)); all biases zero. Apply
caps before fitting. ORG/PLAIN/FROZEN start with identical core/readout draws for
each root/rate; SYM symmetrizes the same underlying draws. Different rates within
a family share initialization and data. FROZEN never fits R,K,b; it fits only D,d.

GRU96 uses the standard PyTorch GRUCell with two normalized action inputs, the same
fixed initialization/correction interface and readout. Use its default seeded
initialization; only its readout receives the row/bias caps. Its gates are ordinary
GRU gates, not hidden AO-1 organization penalties. It has no persistent state besides
its fixed weights and one 96-unit transient state.

POLY12 maintains estimated sensory state z. Predict z plus a ridge-fitted polynomial
residual and clip nonzero-action predictions to [-sqrt(6),sqrt(6)] per channel. Zero
action returns the exact unchanged state. Its basis is the constant, twelve linear,
and 78 unique quadratic observation terms, crossed with the nine nonconstant
action monomials of total degree one through three in (a0/.12,a1/.12), ordered by
degree then decreasing a0 exponent. Observation terms are constant, ascending
linear index, then pairs (i,j) with i<=j in lexicographic order. The constant
observation term stays one; center
and scale the other ninety terms using training current-snapshot means and
population standard deviations with floor 1e-6. Do not center the full action
product, which would break zero-action identity. Solve the averaged float64 normal
equations with the declared ridge value on every coefficient and Cholesky; no
adaptive jitter/fallback fit. Use streaming statistics, not a full feature matrix
in memory. Initialize from the full first cue; correct only observed coordinates
by .5*(observation-current). Its exact stationarity is a supplied favorable prior,
not learned attraction. It has no neural routing endpoint.

This is a competent structured reference by construction: a third-order Taylor
approximation of the task's rotation increments lies in its observation/action
basis. The true latent features are linear in z; powers of the binary-dependent
gains reduce to affine functions of their attributes. Multiplying those gains by
the cosine/sine features requires at most quadratic observation terms, crossed
with action powers through degree three. This establishes representational capacity,
not accurate fitting or multistep stability; Q is still unavailable to the learner.

## Mathematical claims and checked counterexamples

For ordinary unperturbed neural states, initialization, prediction and correction
map [-1,1]^N into itself by convexity and tanh bounds. GRU's bounded candidate and
convex update give the same state bound. This proves bounded state, not recovery.
P's rank is at most 24; nonlinear processing and recurrence can still distribute
input influence across the population. No protected individual neurons follow.

Away from any external intervention, the leaky candidate Jacobian is

```text
J = .5*I + .5*diag(1-tanh(A*h+b)^2)*A
d predict / d a_k = (.5/.12)*diag(1-tanh(A*h+b)^2)*K_k*h
```

On a specified invariant region where ||J|| is uniformly below one, ordinary local
contraction reasoning applies. The matrix caps do not enforce that condition;
global contraction would also exclude multiple fixed points under its usual
assumptions. Multiple stable states and selective routes must be examined separately.
The action derivative can vanish when K_k*h vanishes or units saturate, even when
stationary retention improves. Conversely, a nonzero derivative need not point
toward the correct successor. Small-action, reversal and release tests therefore
measure task-correct movement rather than treating state change as navigation.

The [audit](analysis/AO1_DESIGN_AUDIT.md) verifies this Jacobian numerically and
exhibits a diagonal system with stable nonzero states but no inter-neuron routes.
It also exhibits an allowed skew R whose discrete update increases the classical
symmetric-part energy near the origin. Therefore no monotone energy, global
convergence, continuous attractor, or hierarchy guarantee is adopted. The training
loss changes weights; it is not a Lyapunov function for prediction. Lean is deferred
unless a later specific theorem warrants formal verification.

For the audit's zero-bias example the tested energy is
E(h)=-h^T*S*h/2 + sum_i[h_i*atanh(h_i)+log(1-h_i^2)/2], with S=(R+R^T)/2=0.
This is the classical symmetric-part candidate, not a proposed directed-network
energy. Its increase is a counterexample to inheriting that guarantee; it does
not prove that no other Lyapunov function can exist for a restricted system.

## Route discovery and intervention

Assemblies here are evaluator-selected candidate neuron sets, not training labels.
Their discovery algorithm, group count and size are supplied measurement choices.
Clustering alone supplies no organization evidence. Use only the independent
training-side discovery stream of the fitted root; no evaluation episode or
held-out attribute combination may choose a route, group, control, or function.

For each neural fit, let M=abs(R); for GRU, use the average absolute recurrent
weight across its reset/update/candidate gate matrices. Remove its diagonal and
form affinity (M+M^T)/2. Partition into eight equal-size sets by the following
deterministic greedy procedure: among unused neurons seed a set with the strongest
affinity pair; add the neuron with largest mean affinity to that set until full;
remove the set and repeat. Break all ties by ascending indices. Sort completed
groups by their minimum index. Zero affinities produce deterministic arbitrary sets,
not discovered assemblies. This algorithm supplies candidate sets, not a tree.
Its disjoint groups and weight ranking can miss distributed or overlapping routes.
A negative result concerns this detector, mechanism, task and budget, not the
absence of all possible organization. Results are specific to the implemented
neuron basis; no basis-independent hierarchy claim is made.

Rank the 56 ordered distinct group pairs (source S, receiver T) by mean M[T,S],
descending, then by group indices. Keep four. Discover which of the three feature
functions, if any, each route selectively mediates using the same 48 paired episodes
per function. The functions are rotation, articulation and attributes, as listed
in the manifest. Function names and experimental factor manipulations are
evaluator-only labels used to define this test, never a training target or neuron
assignment. This is not unsupervised discovery of semantic categories.

Each pair shares one eight-transition, full-cue, zero-action warmup. At tick zero,
one world keeps the old object state; the other changes theta or psi by alternating
sign pi/4, or flips b0. All other variables remain identical. Supply four full cues
at ticks 0–3, then no cues. Use zero actions throughout. Counterfactual changes are
sensory correction probes, not claims that an action caused a teleport or attribute
change. Warmup initial phases are independently uniform. Discovery uses all six
training objects for angle changes, balanced eight times each. For b0 flips, use
the four eligible target tuples with b1 and b2 opposite, balanced twelve times
each, so both old and new objects are training combinations. Use paired noise draws
for old/new observations; their difference comes from the controlled change.

Reference, full-response and cut-response states share frozen parameters. For a
leaky model, at each prediction tick 1–16 replace only the designated message:

```text
u_cut = R*h_cut+b
u_cut[T] += R[T,S] * (h_reference[S] - h_cut[S])
h_cut_next = .5*h_cut + .5*tanh(u_cut)
```

For GRU apply that replacement to the recurrent affine input for recipient rows
of each gate, before nonlinearities and before the reset multiplier in its
candidate calculation. The existing reset/update arithmetic remains unchanged.
For SEP cross-block weights are zero. Sensor correction and direct sensory access
are identical in full/cut responses; neither source activity nor source-to-readout
connections are clamped. The old-world reference receives only its own prescribed
cues and actions. These are paired counterfactual diagnostic rollouts with up to
three live state instances, not ordinary model performance or free hidden evidence.
Reference/full paths can be cached; each additional cut is still counted.

Matched controls address generic disruption and large-weight/readout effects.
For each candidate route, draw 256 unique random ordered disjoint subsets of the
same sizes, excluding the route and its reverse. Match five descriptors: forward
and reverse mean absolute recurrent strength, mean source and receiver activity
power, and receiver readout-column power. Powers use common warmup states from
the 144 discovery pairs; readout-column power is mean squared D over all output
rows and receiver columns. Choose sixteen pairs minimizing squared Euclidean
distance between log descriptors, with the manifest floor and lexicographic ties.
No matching or route reselection occurs on confirmation episodes. Also evaluate
the reverse route descriptively; no directionality theorem follows from the ranking.

Decode diagnostic features by Q^T z_hat. For function f, let E_f be squared feature
error summed within its group and divided by the group's constant energy. Score
at ticks 4,8,16. At each scored time within each paired episode, define

```text
Delta_f = E_f(cut) - E_f(full)
selectivity = Delta_selected - mean_other_functions(abs(Delta_other))
route_score = selectivity(route) - mean(selectivity(matched controls))
```

Apply the absolute values before averaging: first compute these quantities per
time and episode, then average the three times within each episode and finally
across episodes. Opposite collateral effects must not cancel before penalization.

Choose the route/function with maximum discovery route_score, with route indices
then manifest function order breaking ties. Preserve all candidate scores. If every
score is nonpositive, retain the best with that value; do not suppress negative
results or invent a successful route. Zero cross-connections yield exactly zero
effect. An untrained dense-input chain fixture must produce a mediated downstream
effect, whereas an uncoupled common-input fixture must produce zero effect.

Confirmation tests the frozen selected route on 192 new pairs in each of the seen
and held-out target-object folds, with the same cue/change schedule. For b0 flips,
seen targets use the four eligible training tuples; held-out targets use the two
reserved tuples and their opposite-b0 references. Balance targets exactly and
alternate angle-change signs within each target. The primary per-root C is the
minimum of the two fold route scores. This requires held-out reuse of the measured
path, but does not establish a multilevel hierarchy or a general semantic concept.

Report descriptive organization diagnostics from the same discovery data: per-unit
activity power, squared sensory-correction increments, squared prediction increments,
and within/between-group absolute recurrent strengths, including forward/reverse
comparisons. Average squared increments over ticks within episodes, then episodes;
zero-cue correction increments are zero. Report input covariance eigenvalues from
the original training inputs (excluding repeated stationary tails), and the known
projection rank. These are influence/activity diagnostics, not information in bits,
router/leaf labels, or additional pass criteria.

## Functional evaluation

Every evaluation episode begins with eight full noisy zero-action warmup transitions,
including a full initial cue. Use 192 episodes per seen/held-out fold, balanced over
its six/two tuples, with fresh independent phases and stream components per test.
Never select episodes using model performance. All below are frozen-parameter tests.
Mixed-action evaluations use independent uniform component draws on the evaluation
grid in four-step blocks, without the training batch's forced-stationary quota.

The three group errors use the fixed group energies. Add the off-sensor-subspace
quantity ||(I-QQ^T) z_hat||²/6, so output error cannot hide outside the diagnostic
features. For functional NMSE guards, average episodes/times first, then take the
maximum across groups and folds. Also report total sensory NMSE ||z_hat-z||²/6.

| Test | Procedure and root endpoint |
| --- | --- |
| Blindfolded action prediction | 64 steps, no new cues, novel action grid and four-step blocks; maximum group/fold time-mean NMSE |
| Grounded prediction | Same horizon/action generator with the ordinary partial-cue schedule; score each prior before evidence |
| Blindfolded stationary retention | 128 zero-action steps without cues; maximum fold/coordinate mean absolute angular error at 128, and maximum fold attribute NMSE; include initialization error |
| Stationary with sensory cues | 128 zero-action steps with a new partial/full noisy cue each step, sizes equally likely; score time-mean prior errors |
| Returning cue | 32 blindfolded mixed-action steps, followed by eight zero-action full noisy cues; score final posterior group/fold errors |
| Perturbation recovery | At calibrated warmup state, inject a normal perturbation, then 16 blindfolded zero-action steps; compare with an unperturbed clone |
| Small actions, reversal and release | Isolate one action axis at a time, preserving other factors; compare with the corresponding zero-command trajectory and score legitimate movement and inactive-coordinate disturbance |

For recovery, estimate two local tangent vectors of the calibrated hidden state
by centered angle differences of .001 with fixed attributes and identical noise
draws. Project a root-seeded random unit vector off their span using SVD (relative
singular-value cutoff 1e-8), renormalize, and inject .1*r, where r is the RMS hidden
radius about the mean over discovery warmup-final states. A projected vector norm
below 1e-8 uses the first standard basis vector with a nonzero projection, with no
random retry. Compare ||h_perturbed16-h_reference16||/||delta||, averaged over episodes
then maximized across folds. The additional accuracy guard is the maximum across
groups/folds of mean positive excess error max(0,E_perturbed-E_reference) at step16.
Do not clip the perturbed state. This is local trajectory separation recovery, not
a proof of attraction to a correct manifold. POLY uses the analogous sensory-state
tangents and radius; its exact zero-action identity gives ratio one.

For action probes, use magnitudes/signs and timepoints in the manifest. Small actions
run for 32 steps and score step32. Reversal runs 32 steps outward then 32 with the
opposite action. Release runs 128 zero-action steps then 32 action steps. For each
scored segment, branch a matched zero-action reference from the same estimated state
at the segment start. Decode angles using atan2 of the first cosine/sine pair for
theta and the second for psi. Unwrap consecutive increments by the principal angle.
R is commanded angular displacement minus matched-zero displacement, divided by
the known true displacement (g*a*t for theta; a*t for enabled psi). Compute mean
abs(R-1) per condition then the maximum over folds, directions, active axes and
listed times. Report stalled abs(R)<.1 and wrong-direction R<0 fractions separately.

For each probe also measure the inactive coordinate's absolute difference from its
zero-command reference: psi during rotation; theta during articulation; both when
articulation is disabled. Average episodes, then take the maximum condition/fold.
Preserve absolute target errors alongside displacement ratios, since subtracting
zero-command drift can conceal an inaccurate trajectory. Radius or decoded angle
norm below the declared floor is a finite model collapse, not a removable episode.

## Selection, uncertainty and scientific decisions

All seven families have four declared configurations and the same training corpus
per root. Three development roots select independently within each family. Compute
the ten absolute functional guard endpoints (criteria 4–13 in manifest order),
normalize positive violations by their thresholds, and minimize lexicographically:
maximum violation, sum violation, negative C, blindfolded action NMSE, numeric hyperparameter.
Use root means of already aggregated endpoints. POLY omits C. Undefined selection
metrics make a configuration ineligible; if a family has no eligible configuration,
retain its failures, stop before confirmation and record design/execution limitations
rather than change the selection rule. A finite failed guard is not ineligibility.

Freeze selected configurations and discovery algorithm before twenty new
confirmation roots. Each new fit discovers its own route using only its separate
training-side discovery stream; confirmation episodes and held-out tuples cannot
influence that discovery. This is an explicitly supplied diagnostic selection
procedure, not an additional learned inference module. Pair streams and compatible
initializations; record unavoidable architecture differences.

The sixteen simultaneous primary intervals cover C_ORG, its gains over PLAIN and
FROZEN, ten ORG functional guards, and three ORG-minus-PLAIN noninferiority guards.
Their exact bounds and maximum widths are in the manifest. C_ORG must reach .02
normalized-error units, and both paired route gains .01; these are engineering
practical-effect choices, not biological constants. Five-degree stationary retention
continues the intended accuracy target on a new task, not a retroactive E0 criterion.
Other controls' complete results and descriptive intervals remain mandatory; no
unmeasured architecture-wide superiority is implied.

Use 50,000 paired independent-root bootstrap resamples, common across all quantities,
two-sided percentile intervals at alpha/16 with linear quantiles, and the fixed
bootstrap seed. Resample roots, never timesteps, episodes, routes or matched controls
as independent fits. Apply the width cap before directional pass/fail. An interval
entirely satisfying a bound passes; one entirely on its failing side is a precise
negative; an interval crossing a boundary or exceeding its width cap is unresolved.
Lower-bound tests use >= the threshold; upper-bound tests use <=. No rounded
value may change the classification.

Validity is checked first. A valid, adequately precise failure of any joint criterion
is a negative configured joint result; all pass supports only the scoped conjunction;
otherwise it is inconclusive. If routing passes but function guards fail, describe
the observed trade-off while preserving the negative joint result. Finite ORG
collapse on any required confirmation case fails the joint usability condition;
report any undefined intervals rather than imputing them. Nonfinite numerics,
leakage, missing required runs or broken interventions are invalid execution or
incomplete evidence, not a falsification of the scientific hypothesis. No exclusions,
restarts, best-seed selection, repeated confirmation tuning, or budget extensions.

## Finite inventory, resources and implementation handoff

The manifest fixes 84 development fits, 140 confirmation fits and seven exact-repeat
fits (root701), totaling 231 scientific fits, plus seven eight-update engineering
fixtures at root9601. Every neural family has four learning rates; POLY has four
ridge values. Fixtures use the largest neural rate or smallest ridge, full batch and
32/64 horizons, complete discovery/evaluation, and synthetic known-pass/known-fail
intervention checks. Use them only for correctness/timing, not scientific selection.
The POLY fixture fits the first eight batches of the same corpus; it has no Adam
updates. The exact repeat must reproduce every model tensor, selected route/control
and root-level evaluation array bitwise, excluding nondeterministic resource/timing
metadata. Any mismatch blocks a reproducible result and must be reported.

The cumulative ceiling is 28,800 CPU seconds / 57,600 execution wall seconds,
3 GiB RSS and 8 GiB artifacts, including fixtures, fits, discovery, all evaluations,
repeat and independent analysis. Historical E0-HOLD NAV fits took about 9.6 CPU
seconds at width32; that is context only, not an AO-1 timing measurement. SOAM-105
must project its full inventory from per-family fixture timings, with 2x margin,
below 80% of each time/artifact cap and within RSS before any scientific fit.
Stop on infeasibility. No unused E0-HYS budget transfers to this study.

Use CPU, one Torch thread, deterministic operations, float32 learned dynamics and
float64 statistics/intervals. Record Python/Torch/NumPy versions, numerical flags,
commit/source fingerprint, resolved configs, every derived seed, data/target hashes,
parameter and active-state counts, timing, MAC estimates, peak RSS and artifacts.
Stream seeds use the existing derived_seed function with namespace soam-ao1, version1,
split development/confirmation/fixture, the declared root, and an explicit index and
component. Use separate components for train-world, train-action, train-mask,
train-noise, neural-init, gru-init, sep-init, route-discovery-world/noise/controls,
and each evaluation condition/fold. Same-dimension leaky initialization uses the
same neural-init seed across families; data seeds never include model or rate.

Each neural fit processes 12,800 episodes / 422,400 original clean snapshot records
and 102,400 extra stationary target replays. Repeated stationary values are not new
independent information. POLY uses the original 409,600 transitions only; the zero
residual tail would duplicate training evidence and is omitted with its exact
stationarity prior disclosed. Count additional discovery observation records,
target reuses, causal rollout calls, and offline passes separately. Streaming ridge
statistics may be cached across its four rates within one root, with actual shared
processing and memory reported rather than charged as fictitious repeated work.

| Family | Fitted coefficients | Total model scalars excluding fixed P | Fixed P | Live state |
| --- | ---: | ---: | ---: | ---: |
| ORG96 / PLAIN96 | 28,908 | 28,908 | 2,304 | 96 |
| SYM96 | 28,908 stored parameters; 15,228 effective degrees | 28,908 | 2,304 | 96 |
| SEP168 | 30,420 | 30,420 | 4,032 | 168 |
| GRU96 | 29,964 | 29,964 | 2,304 | 96 |
| FROZEN96 | 1,164 | 28,908 | 2,304 | 96 |
| POLY12 | 9,828 coefficients | 10,008 including fitted statistics | 0 | 12 |

SEP has about 5.2% more fitted coefficients and 75% more live state than ORG; report
that favorable state allowance. Count float64 POLY storage, fixed matrices, optimizer
moments, supplied task/evaluator geometry, intervention metadata and up to three
diagnostic state instances separately. Preserve all selected and unselected dev
scores, root-level raw evaluation arrays sufficient for independent reduction,
checkpoints, discovery choices, matched controls, full inventories and failures.

SOAM-105 must verify the implemented equations/Jacobians, dense fixed input and
exact no-cue behavior, no-write inference, no target leakage, action timing, split
separation, constant-energy normalization, selector locking, supplied/common-input
fixtures, collapse handling and reproducibility. The algebra audit is not a substitute
for these tests. Reuse infrastructure without modifying archived E0/E0-HOLD sources.
SOAM-107 reviews the result and may recommend one later fork. The joint blog/report
follows the first experiment and review, including negative or inconclusive evidence.

## SOAM-104 design review

**Proceed to SOAM-105 implementation and verification.** The protocol has an explicit
learned intervention and finite test; it does not require a theorem of emergence.
Fixed dense sensory access, unregularized and frozen-core comparisons, matched
message interventions, untouched direct sensory paths and held-out reuse make the
scoped routing question testable. The mandatory stronger/simple references and
functional guards prevent retention or lesion sensitivity alone from being a success.

The principal mechanism risk is that connection cost favors independent diagonal
memory or suppresses useful action pathways rather than producing routes. The
activity target does not remove that possibility. A precise failure is an allowed
result, not grounds to silently add a topology prior. Disjoint detector groups may
miss another useful organization; no negative result rules out all such mechanisms.

Information/resource differences are explicit: POLY has a stationarity prior and
clean-pair fitting, SEP has additional state, and all interventions use evaluator
labels and diagnostic clones. Functional performance uses no such diagnostic state.
The 231-fit inventory is a ceiling, not a timing claim. Its feasibility remains
conditional on SOAM-105's complete fixture projection with the prescribed margin;
if that fails, stop before scientific fitting and record the impediment. SOAM-104
accepts this test design only, not a research gate, measured benefit, or permission
to activate another experimental fork.

## Primary-source context

[Litwin-Kumar and Doiron (2014)](https://www.nature.com/articles/ncomms6319) supply
precedent for plasticity with regulation and synaptic competition; AO-1 uses different
learning equations and adopts no theorem from that model.
[Hopfield (1984)](https://redwood.berkeley.edu/wp-content/uploads/2018/08/hopfield84.pdf)
provides the classical symmetric graded-response energy context; arbitrary directed
discrete updates do not inherit that result.
[Mengistu et al. (2016)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004829)
motivate connection cost as a possible organizing pressure in their already layered
evolved-network experiments. None of these sources proves AO-1 routing or hierarchy.
