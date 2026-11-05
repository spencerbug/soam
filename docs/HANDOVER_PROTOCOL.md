# SOAM-033: cue-driven handover protocol v1

**Date:** 2026-11-01. **Status:** preregistered design, awaiting SOAM-034 implementation.
**Scope:** controlled mechanism feasibility; no trial or positive scientific result
is reported here. Numerical choices below are engineering hypotheses, not tuned results.

The [v0.2 scope](RESEARCH_SPEC_V0_2.md) prioritizes cue-driven switching, attended /
tracking / primed roles, and sensorimotor continuity. This protocol freezes a small
implementation contract for [SOAM-034](../tickets/SOAM-034-handover-harness.md), trials
in [SOAM-035](../tickets/SOAM-035-cue-driven-handover.md), and the independent decision
in [SOAM-036](../tickets/SOAM-036-handover-gate.md). Historical Gate 1 is not this gate.
The [numerical manifest](protocols/handover_v1.json) mirrors the fixed choices. If
manifest and prose disagree, stop and amend both before running confirmation data.

## 1. Claims and deliberately supplied structure

Separate three questions:

- **K — cue recruitment:** can partial content move a recurrent key state into the
  intended basin, complete the pattern, and retain it after the cue is removed?
- **T — concurrent tracking:** can a second sensorimotor state remain calibrated
  while the first is attended, with a third pattern merely primed?
- **H — useful handover:** does attention reach the requested supported pattern
  with acceptable delay and prediction continuity? Does pre-tracking improve error
  or online latency compared with reconstruction from the same observations?

The all-other coupling tests generic associative priming, not selective learned
source-to-successor schemas. If removing L has no effect, report externally cued
retrieval with no demonstrated benefit from inter-pattern coupling.

K is measured before any output-selection rule. T is measured for each internal
state regardless of which output is selected. H includes the attention policy and
therefore cannot establish K by itself. Attraction toward a state set, exact phase
recovery, and cue-driven switching have distinct diagnostics.

The first candidate deliberately combines a modern-Hopfield-style key memory with
analytic ring dynamics. It is a modular engineered positive-control candidate, not
an assertion that one homogeneous neural population already implements all functions.
Pattern identities, local-coordinate bindings, action gains, ring geometry, and
cue couplings are supplied. Independent state banks are not evidence for the original
H1 claim that one shared recurrent population discovers multiple reusable regimes.

## 2. Small environment and observation contract

### 2.1 Two local rotating features

Use two rotating features A and B on a controllable synthetic object. They share an
executed angular command but may slip independently. This is a minimal part-to-part
handover task, not a claim of reconstructing a complete geometric object. C is a
stored distractor/primed pattern with no physical observation stream in this task.

For transitions t -> t+1, in radians:

    phi_i[t+1] = wrap(phi_i[t] + g_i * a[t] + epsilon_i[t])
    g_A = 1.0; g_B = 0.7
    phi_A[0] ~ Uniform(-pi, pi); phi_B[0] = wrap(phi_A[0] + pi/3)
    a[t] ~ Uniform(-0.12, 0.12), held for four transitions
    epsilon_i[t] ~ Normal(0, 0.02^2), independent across i and t
    y_i[t] = (cos(phi_i[t]), sin(phi_i[t])) + Normal(0, 0.03^2 I_2)
    z_i[t] = Q y_i[t]

Q is the existing 12 x 2 orthonormal FixedProjection matrix with seed 1729.
Ground truth phi, process noise, and noiseless features are evaluator-only. The
learner receives observed z, validity bits, past executed actions, and the explicit
content cue. No future observation enters a free rollout. Normalization of noisy
observations is not performed. Supplying Q and fixed forward action operators is
an analytic scaffold; the learner must not call diagnostic_inverse.

The additional **coordinate-only** condition sets g_B=1 and epsilon_B=epsilon_A.
There B is exactly A rotated by pi/3. A direct transport control should suffice;
pre-tracking superiority is not required in this condition. Independent slips in
the main condition prevent the two local states being exact coordinate copies.

### 2.2 Episode timing, overlap, and focus requests

Each episode has 192 observations indexed 0..191 and 191 executed transitions.
The initial requested focus is A. Requests change to B at 48, A at 96, B at 144.
These are content stimuli to the learner, never calls that assign the attended ID.
Cues last four observations: 0..3, 48..51, 96..99, 144..147.

Observed streams:

| Observation indices, inclusive | Available features |
| --- | --- |
| 0..15 | A |
| 16..43 | A, B |
| 44..55 | A |
| 56..91 | A, B |
| 92..103 | B |
| 104..139 | A, B |
| 140..151 | A |
| 152..191 | A, B |

The successor is unobserved across each switch, so maintained/reconstructed history
can matter. All variants receive the identical observation packet stream and the
same action sequence. Missing streams contain zero features plus an explicit invalid
bit; zero must not be treated as an observation. The timing is disclosed scaffolding.
Models do not receive time, future masks, event indices, or future request labels.

Feature packet bindings A/B are supplied sensor-channel identities, not inferred
correspondence. The oracle-correspondence control additionally supplies an exact
requested template instead of a partial cue; it never supplies phi or noiseless z.
Learned correspondence, instance binding, and movable sensory focus are later work.

### 2.3 Content templates and cues

Construct the Sylvester Hadamard matrix H_16 recursively from H_1=[1]. P contains
columns 1, 2, 3 (zero-based) divided by 4; hence P has shape 16 x 3 and P^T P=I.
These fixed unit templates represent A/B/C. They are stored memory, not online labels.
At each cue onset choose uniformly a size-8 coordinate subset M without replacement;
keep it fixed for that four-frame pulse. Each frame presents:

    c[t] = M * p_target / sqrt(8/16) + 0.02 * M * xi[t]
    xi[t] ~ Normal(0, I_16)

Do not renormalize after adding noise. Outside pulses c=0 and cue_present=0.
During training the full requested template is allowed as an explicit supervisory
target; it is never an additional evaluation input except in the labeled oracle.
The initialization pulse is treated like any cue, not an overwrite of neural state.

## 3. Explicit attractor candidate A2

### 3.1 Key dynamics and associative priming

A live key q in R^16 starts at zero. Let w=softmax(12 P^T q). The fixed coefficient
matrix L has diagonal zero and every off-diagonal entry 1/2. Define C=P L P^T.
This dense, weak all-other association provides priming; it is not a stored
source-destination action table or an algorithm traversing discrete graph edges.
Compute C factorwise; materializing it adds storage which must be reported.

For each observation hold c fixed and take 20 Euler substeps, alpha=0.1:

    q <- q + alpha * (-q + P softmax(12 P^T q) + 1.5*c + 0.1*C*q)

There are no state resets, clamps, winner assignments, or target-index inputs.
After the substeps, set w=softmax(12 P^T q) and b=L*w. b is graded associative
priming, not a probability or independent sensory evidence. C receives no pose data.
The cue must overcome the previous basin through dynamics. Failed switches are
results, not grounds to raise cue gain after viewing confirmation outcomes.

In the autonomous key probe, remove both c and Cq. The energy is

    E(q) = 0.5 * ||q||^2 - logsumexp(12 P^T q)/12.

The update is an explicit gradient step for this chosen energy. Its continuous-time
flow has dE/dt=-||grad E||^2. The numerical update must be checked independently;
finite precision and driven dynamics do not inherit every continuous-time guarantee.
Stable endpoints must be measured; stored p_i are references, not assumed exact
fixed points. Mixture/saddle states are possible. Report convergence toward the
measured endpoint associated with each template and toward other endpoints.

### 3.2 Independent continuous sensorimotor circuits

Each feature i=A,B has r_i in R^12, initialized to 0.1 Q(1,0)^T. Parameters/operators
are shared; g_i is the supplied per-feature action gain. No state is copied between
banks. Define S=QQ^T and R(theta) as the ordinary 2D rotation matrix. The following
closed-form propagation implements an engineered ring normal form for one unit of
model time, using lambda=0.5 and lambda_perp=1:

    v = S*r; u = (I-S)*r; rho = ||v||
    F_i(r,a) = Q R(g_i*a) Q^T v /
                 sqrt(rho^2 + (1-rho^2)*exp(-2*lambda))
               + exp(-lambda_perp)*u

At rho=0 the first term is zero; its denominator remains positive. Do not normalize
the full state to unit length. This is the exact flow of radial recovery plus an
orthogonal decay and constant commanded rotation, not an invocation of the encoder's
diagnostic inverse. Operators are precomputed from the fixed supplied projection.

The zero-action/no-observation target set is {Q(cos(phi),sin(phi)): phi in S^1}.
Radial error contracts away from the zero state; phase is neutral. Thus a phase
perturbation must not be called a failure of manifold attraction, nor may radial
recovery be called recovery of the true phase. With fixed nonzero action, the target
is the corresponding moving family. Sensory feedback corrects phase:

    r_i^- [t] = F_i(r_i[t-1], a[t-1])              # t>0
    r_i[t] = (1 - 0.25*m_i[t])*r_i^-[t] + 0.25*m_i[t]*z_i[t]

At t=0 apply only the observation correction to the initial state. Each valid
observation is assimilated once. The decoded current feature is r_i and the
one-step prediction is F_i(r_i,a[t]); no learned decoder can conceal bad state.
A snapshot free rollout repeats F using executed/planned commands and no correction.

### 3.3 Roles, output selection, and source retention

The two possible live banks A/B are preallocated scaffolding. Before a bank has
received a valid observation it is unlocalized, even though its numerical prior
exists. Both banks propagate each frame; they assimilate their own valid observations.
Their cost is counted even while unlocalized. C has a template and priming score,
but no pose bank. No state for C is silently running elsewhere.

Primed means b_i>=0.1 and not currently attended; tracking additionally requires
a live bank with at least one past valid observation. Attended means the output
policy below has committed that bank. These thresholds define reported roles;
they do not write q, copy states, or count as learned attention. Between frames
20 and 43 the intended diagnostic is A attended, B tracking, C merely primed.
Report actual role occupancy and violations rather than forcing that outcome.

The same output policy applies to every model. A candidate must have w_i>=0.9
for three consecutive observation frames, a live/localized bank, latest valid
observation age <=16, and decoded state norm in [0.5,1.5]. It may then replace the
attended output. Keep the previous valid output otherwise; if none exists, abstain.
Age is zero on the current observation. At initialization no bank is attended.
There is no extra target-ID test in this policy. Unsupported C can win key retrieval
but cannot obtain motor/output authority; record both events separately.

The attended bank returns its own local feature prediction and decoded identity.
Do not use evaluator truth to choose a bank or repair its output. Preserve source
state after every handover and continue calibration. Attention does not control an
actuator here: actions are a fixed exogenous experiment stream. Motor authority and
an actual policy are deferred to the later control tickets.

## 4. Layout and ordinary-recurrence controls

Run five frozen model/layout variants; do not add topologies after seeing results.

| ID | Key memory | Sensorimotor memory | Purpose |
| --- | --- | --- | --- |
| A2 | q attractor above | Two shared-parameter, independent 12D ring states | Main engineered candidate |
| A1 | Same q and fixed operators | One 12D ring state | Explicit one-state bottleneck control |
| G2 | 16D trained GRU selector | Two 12D GRU states with tied parameters | Ordinary recurrence with separated live state |
| GS24 | Same trained selector | One 24D dense GRU, two 12D readouts | Shared population with equal total pose-state width |
| GS9 | Same trained selector | One 9D dense GRU, two 12D readouts | Approximately parameter-matched shared control |

A1 uses d=argmax over w_A,w_B (A wins exact ties) as its sole routing scaffold.
It propagates F_d and assimilates only z_d when valid. It has no source bank,
backup state, or implicit chart conversion when d changes. It returns the one r
for either requested local output. Evaluate both its selected output and explicitly
mark the missing independent source state. A1 failure cannot prove a shared
population is incapable of concurrency: GS24/GS9 test less restrictive alternatives.

GRU selector: input [c (16), P*b_previous (16), cue_present (1)], hidden width 16,
linear logits 16->3 plus softmax. Start hidden=0, previous w=(1/3,1/3,1/3).
Use L to compute b for every family. One selector step per observation, versus 20
Euler steps for A; report that compute difference. The trained selector is shared
unchanged across G2/GS24/GS9 within a seed. It has no prescribed attraction property.

G2 pose cell: input [m_i*z_i (12), m_i (1), a_previous (1), g_i (1)], hidden 12,
linear readout 12->12. One cell, weights shared across two live states.
GS pose cell: input [m_A*z_A (12), m_B*z_B (12), m_A,m_B,a_previous,g_A,g_B], hidden 24 or 9,
linear readout to 24, split into A/B predictions. All hidden states start at zero.
The supplied gains are identical across layouts, including the deliberately wrong
gain in the mismatch condition; the shared controls do not lose calibration inputs.
At t=0 a_previous=0. Feed no time index, focus target, or hidden ground truth.
Current estimates are readout(h[t]); one-step/free predictions use a cloned state,
the requested action, and missing observations. Snapshot calls must not mutate live
states, key memory, evidence history, or parameters.

Train with observed current-feature reconstruction and next-observed prediction,
not evaluator phases. Selector training targets the most recently presented full
cue template (including a deliberately wrong cue), holding that target through
cue-free frames. It must not train on an unobserved requested switch in the no-cue
condition. This is declared cue supervision, not the evaluator-only ideal task focus. For
missing-current targets, no reconstruction loss is applied; missing-next targets
also contribute no prediction loss. Normalize losses by valid feature scalars.
Use loss = current MSE + next MSE for pose training, CE for selector training;
train selector and each pose architecture separately. No gradients couple selection
and pose, and no BPTT or optimizer step occurs at evaluation.

PyTorch GRUCell with both biases and Linear with bias gives these trainable counts:
selector 2,499; tied G2 pose 1,200; GS24 pose 4,560; GS9 pose 1,320. Totals are
3,699 / 7,059 / 3,819. GS9 is within 3.3% of G2's total; GS24 matches active-state
width instead. A models have zero trained parameters but substantial supplied
structure: count all stored templates/operators/constants, not just learned tensors.
Do not claim fair parameter/compute superiority for analytic A versus trained G.

Separate untied clones, larger banks, dynamic slot allocation, flip-flop bank reuse
across more than two identities, columns/stacks, learned cue weights, and neuronal
ring fields are deferred. A2 already alternates attended/tracking roles across fixed
banks; this does not evaluate dynamic cloning or a general stack organization.

## 5. History and source-transport controls

For A2 and G2, evaluate three additional modes using unchanged fitted/fixed weights.
They use exactly the same input packets as their pre-tracking counterpart:

- **Cold:** only the attended bank updates before a handover. On an actual policy
  commit to another bank, reset that destination to its original prior and permit
  current/future observation correction. Log the reset as a control, not attraction.
  The commit readiness check uses localization/age from observation history and
  ignores the dormant pose norm; then measure resulting continuity without hiding
  its bad output. All other output-policy conditions are unchanged.
- **Equal-history replay:** store packets from episode start. At the same commit,
  reconstruct the destination from its original prior by replaying every packet
  through the exact same per-bank operations up through the current observation.
  Do not apply the current packet again. Count buffer storage, replay observations,
  operations, and blocking handover latency. Exact equality with pre-tracking is
  expected for deterministic independent G2/A2 banks; this is an integrity check.
- **Source transport (A2 only):** at commit overwrite the destination with the
  source transformed by the supplied initial offset and accumulated executed action
  difference. A->B uses angle pi/3+(g_B-g_A)*sum(a[0:t]); reverse uses its negative.
  No slip state is supplied. Continue ordinary propagation/correction afterwards.
  This is an explicit handover map/copy control; every copy is logged and costed.

Cold/replay/transport key dynamics continue normally and receive the same cues.
Their role accounting must not pretend dormant/reconstructed banks tracked online.
The cold/replay scheduling change is a deliberate control, never proof of neural
attraction. Compare reconstruction compute as well as statistical error. End-to-end
latency includes reconstruction; key crossing time is reported separately.

## 6. Bounded training and evaluation plan

### 6.1 Streams, fitting, and numerical settings

Use seeds [11,23,47,71,101] and NumPy SeedSequence([3300,seed,split,condition,
episode,component]). Split IDs: train=0, development=1, confirmation=2, fixture=3.
Component IDs: initial_phase=0, actions=1, process_noise=2, observation_noise=3,
cue_masks=4, cue_noise=5, perturbations=6, training_order=7, initialization=8.
Use probe condition IDs 100+2*target+corruption for key probes and
200+2*perturbation+action_mode for ring probes (all indices zero-based); probe
episode IDs are 0..15. Key masks use component 4 and ring perturbations component 6.
Training-order draws use condition=0, episode=0, component=7 and the same index
sequence across architectures. Initialization uses component=8 with episode IDs
0/1/2/3 for selector/G2/GS24/GS9. Derive the Torch seed as the first uint64 from
that SeedSequence modulo (2^63-1), and record it.
For the eight main conditions, packet generation uses condition=0 and the same
base episode index: pre-sample all standardized innovations, per-frame cue masks,
and noise for the entire episode before applying condition-specific transformations.
The condition ID in an output record is not an RNG change for paired packets.
History/ablation cells reuse those same base packets. This makes removed or added
cues unable to shift subsequent RNG consumption. Probe conditions use their separate
IDs above. Do not draw a fresh trajectory for each variant. Reproduction reuses
the original packet files/seeds; it is not a new statistical sample. Torch model
initialization uses a separately logged seed derived from the initialization stream.

Per seed generate 512 base training innovation streams and all eight condition
variants of each, yielding 4,096 derived episodes. Retain the paired-base identity
when reporting unique versus repeated exposure. Sample with replacement for 500 Adam steps, batch 8 full episodes,
learning rate 0.001, no weight decay, gradient norm cap 1.0. This is 4,000 episode
presentations / 764,000 executed transitions for each fit. Train one selector and
three pose variants per seed: 20 fits total, final checkpoint only. No hyperparameter
sweep, early-stopping selection, or best-seed selection is authorized. Report unique
and repeated observation exposure separately; analytic models see no training data.

Evaluate development with 8 episodes per condition/seed, confirmation with 32.
Development may detect bugs or motivate a new protocol version, but this version
has zero tuning budget. A material change requires a dated amendment and fresh,
unopened confirmation namespace; do not reinterpret failures by moving thresholds.
Use CPU, float32, one Torch thread, deterministic algorithms. Compute energy,
aggregate metrics, and circular statistics in float64. Pin actual installed versions
from uv.lock and record them at run time rather than asserting future versions here.

SOAM-034 uses fixture data only for implementation/smoke checks (at most 2 episodes
per condition, seed 11, plus deterministic analytic unit checks). SOAM-035 performs
fitting and measured development/confirmation runs. Do not run confirmation during
harness development. Maximum 600 seconds per fit and 4 CPU-hours for the full
study, including all evaluation/reproduction, with an 8 GiB process-RSS cap. On
budget exhaustion preserve partial results and stop; do not silently shrink the
trial matrix or drop a weak model. Runtime costs are unknown until measured.

### 6.2 Main condition matrix

Every model/layout runs all eight conditions, with 192 observations per episode.
Condition-specific input mutations occur before any model receives the packet.

| ID | Condition | Exact intervention |
| --- | --- | --- |
| 0 | Main independent-slip overlap | As specified in §2 |
| 1 | Coordinate-only | g_B=1 and epsilon_B=epsilon_A |
| 2 | No transition cue | Keep initial A cue; remove pulses at 48,96,144 |
| 3 | Shuffled transition cue | Swap A/B cue templates at 48,96,144; expected request remains the original external task request for scoring |
| 4 | Misleading unsupported cue | Main inputs plus C pulse at 120..123; external task remains A until 144 |
| 5 | Missing overlap evidence | Additionally mask both feature streams at 32..43,80..91,128..139 |
| 6 | Observation noise | Observation standard deviation 0.10 instead of 0.03 |
| 7 | Motor calibration mismatch | True g_B=0.9, supplied model g_B=0.7; all else main |

Condition 2 and 3 intentionally withhold/corrupt informative requests. Failure to
follow the unobserved true request is expected and is not grounds to fail the
main feasibility gate. Their purpose is to expose a hidden scripted switching path.
Condition 7 is a declared stress test, not a reason to retune the gains.

### 6.3 Additional comparisons and isolated probes

Do not take a full Cartesian product of all manipulations.

- History modes: A2 cold/replay/transport and G2 cold/replay on conditions 0 and 1.
- Main-condition ablations, A2 and G2 only: no associative priming (L=0), shuffled
  priming (replace L with L[[2,0,1],:], a fixed cyclic output permutation), and no sensory correction
  after observation 15. These change runtime inputs/operations, not fitted weights.
  For G2 the latter means m=0 and z=0 after 15; for A2 set m=0. Preserve packets for
  scoring and exposure accounting. Priming removal still leaves external cues;
  an unchanged outcome limits the claimed contribution of associations.
- Oracle cue: A2 and G2 on condition 0 with c=p_target, no cue noise, the same pulse
  timing and gains; never supply true phase. Report separately from partial cues.
- Autonomous key probes: 3 targets x 2 corruptions (erase 8 coordinates; flip the
  sign of 2 coordinates) x 16 instances per seed. Initialize q from the corrupted
  p_target, disable c and Cq, run 80 substeps. Probe the GRU selector using a one-frame
  corrupted cue followed by 80 zero-input frames; different state/time units prohibit
  numerical recovery-rate equivalence claims. Fit weights remain unchanged.
- Ring probes (A2): 3 perturbations (radius x0.5; radius x1.5 plus an orthogonal
  perturbation of norm 0.2; phase rotation 0.3 rad) x 2 input modes (a=0; a=0.08)
  x 16 instances per seed. Start on a ring phase drawn from the probe stream, remove
  sensing and key/coupling inputs, and propagate 16 frames. These analytic initial
  conditions are labeled diagnostic interventions, not learner access to world truth.
- Live source/candidate perturbation: A2/G2 condition 0 at observation 40, after
  correction and before prediction, perturb either A or B (two cells). For A2 multiply
  its r by 0.5; for G2 add seeded Gaussian hidden noise normalized to 0.5 times that
  hidden norm (floor 0.1). Keep a paired unperturbed run. These are different state
  spaces; report effects without claiming functionally matched perturbation sizes.

Main, history, ablation, oracle, and live-perturbation cells total 62 episode cells
per seed: 40+10+6+2+4. Confirmation thus contains 9,920 episodes / 1,894,720 executed
transitions across five seeds, excluding isolated probes. Development contains
2,480 episodes / 473,680 transitions. Isolated probes use 192 unique initial-condition
cases per seed (288 primary model evaluations, because both selectors use the key cases).
Run one exact seed-11 confirmation repeat for all 62 cells and probes using archived
packets and checkpoints. Repeats are excluded from inferential sample counts.

## 7. Measurements and preregistered decision rules

Report each seed and condition separately, then paired differences on the same
packets. Do not pool thousands of events as independent model seeds. Provide mean,
median, minimum/maximum across five seeds and 95% percentile bootstrap intervals
from 10,000 resamples of seed-level means (analysis RNG seed 330033). These intervals
are descriptive with five seeds, not broad statistical or neuroscience validation.
Stress/ablation endpoints are exploratory and cannot replace a failed primary test.

### 7.1 Metrics

- **Key capture:** first frame at/after request onset where requested-template w>=0.9
  for three frames, before the policy's localization/norm checks. Record q distances,
  winner margins, mixture states, and capture after cue removal separately.
- **Handover delay:** frame of policy commit minus request onset; censor at 16 frames
  and record a failure rather than deleting events. Record blocking replay time too.
- **Event success:** correct source attended at onset-1, requested supported target
  committed within 8 frames, then retained for 8 frames. Successful key capture alone
  is not event success. Count all three scheduled requests per episode.
- **Continuity:** for the requested target bank over onset..onset+7, NMSE is sum of
  squared feature-vector errors divided by sum of squared noiseless target-vector
  norms. Evaluator truth is used only here. Also report angular RMSE from diagnostic
  inverse and circular wrap; if decoded planar norm <1e-6, angle error is pi, not NaN.
  Report errors even on failed events and abstentions using the bank's raw predicted
  state, alongside the failure/abstention count; never silently score a different bank.
- **Source retention:** source-bank NMSE and angular error at onset+8 and onset+16
  regardless of current attention. A1 has no separate source state: report unavailable
  capacity and its one-state error, not a fabricated preserved source.
- **False commits:** unsupported C commits and commits inconsistent with the current
  external task outside the 16-frame event windows; initialization 0..15 is excluded.
  Report occupancy, abstention duration, and spontaneous key transitions separately.
- **Tracking/priming:** actual A-attended/B-tracking/C-primed occupancy at 20..43,
  evidence age, dormant steps, and every state reset/copy/replay.
- **Prediction:** grounded one-step and free 8/32-step feature NMSE at anchors
  40,88,136, scored for A and B independently using future executed actions only.
  Future observations, process noise, and future cues are unavailable to snapshots;
  keep the cloned key input cue-free. Report feature motion energy/collapse.
- **Recovery:** radial distance |rho-1|, orthogonal norm, key endpoint error, and
  perturbation excess feature error relative to paired unperturbed dynamics.
  A phase-shifted ring can recover to the manifold while remaining phase-shifted.

### 7.2 Thresholds for the narrow handover gate

These are fixed engineering screens chosen before data, not promised performance.
A SOAM-036 proceed for the specified A2 mechanism requires all integrity checks and:

1. **Autonomous key attraction:** >=95% of each corruption/target probe group per seed
   reaches requested-template w>=0.99 by substep 80; norm of the last update <=1e-4.
   Energy has no increase >2e-6 per step (float64 diagnostics). Retain endpoints from
   all starts; do not discard mixed/incorrect attractors to define a favorable basin.
2. **Continuous-state attraction:** all radial/orthogonal probes end with radial
   error <=0.01 and orthogonal norm <=0.01 at frame 16. Zero-action phase must remain
   within 0.01 rad of its own perturbed phase. In the phase-perturbed test do not demand
   recovery of the original phase without sensing. Driven tests preserve the commanded
   rotation to within 0.01 rad. No nonfinite state or state norm >10 is allowed.
3. **Main-condition cutover:** event success >=90% per seed, median commit delay <=8,
   mean continuity NMSE <=0.08 and angular RMSE <=0.25 rad per seed. Mean source
   retention NMSE at +8/+16 must each be <=0.10. Unsupported C commits are zero;
   false committed occupancy outside event windows <=1% in condition 0.
4. **Role concurrency:** A-attended/B-tracking/C-primed occupancy covers >=80% of
   frames 20..43 per seed in condition 0, with no undeclared C state or source copy.
5. **Cue attribution:** condition-0 key capture success exceeds each of the no-cue
   and shuffled-cue conditions by >=30 percentage points for every seed. Score
   capture after each requested change, not merely the number of scheduler commits.
   Report mismatch cases where policy retains a source while q captures C.
6. **Useful pre-tracking:** A2 improves mean condition-0 continuity NMSE over cold by
   >=20% in the median seed, with a positive paired difference in at least four of
   five seeds. If cold error is <1e-8, relative benefit is undefined and this criterion
   fails rather than reporting an infinite gain. Equal-history replay must reproduce
   A2/G2 per-bank states within absolute/relative 1e-6 at each reconstruction point.
   Report online model-call and latency differences; no total-compute advantage is
   required or implied. If reconstruction already meets the latency needs, record
   that pre-tracking may not be worth its continuous state cost.

Prediction at 32 steps, noise/mismatch stress, and cross-family superiority are not
pass requirements. The 8-frame continuity screen prevents calling meaningless
switching useful. If G controls fail their supervised development loss or empirical
screen, report a weak control; do not use that failure as evidence of A's superiority.
If GS24 or GS9 succeeds, separate populations are not necessary in that tested
ordinary-RNN implementation. If both fail, that does not prove a universal constraint.
If source transport meets the main screen, report that concurrent tracking was not
necessary for that measured task even if it beat the deliberately cold control.

Add paired restoring-term ablations to the isolated probes only: for key dynamics
remove P softmax(12 P^T q), leaving passive leak; for the ring set lambda=0 while
retaining the same action/orthogonal decay. Their failure/success distinguishes the
specified restoring mechanism from forcing or decoder effects. These add 192 model
probe evaluations per seed, for 480 total (288 primary plus 192 ablations).
The 192 unique probe initial conditions are not 480 independent samples.

If any integrity check fails, the affected run is invalid and must be repaired and
repeated with the repair disclosed. If a scientific threshold fails, preserve the
negative result and choose revise/stop or a narrower separately documented claim.
The chosen design does not have to win. No criterion licenses unsupervised learning,
compositionality, a shared-population H1 claim, or biological equivalence.

## 8. Scaffolding ledger and interface freeze

| Item | Initial status | Claim restriction |
| --- | --- | --- |
| P templates and pattern inventory | Supplied, frozen | No learned memory discovery or capacity claim |
| Ring geometry, g values, Q/action operators | Supplied; g stress is deliberately mismatched | No learned world dynamics |
| L coupling and priming thresholds | Supplied, frozen | No learned associations; ablate their contribution |
| Sensor-channel A/B bindings and initial relative phase | Supplied | No inferred object/role correspondence |
| Two available state banks, latent C | Supplied allocation | No learned slot management or simultaneous identity retrieval in one key population |
| Focus requests and visibility windows | Exogenous observations | No autonomous attention policy or active sensing |
| Three-frame policy and evidence/norm checks | Explicit controller | Output routing is not itself attractor evidence |
| GRU training supervision | Observed features and supplied full cue labels | Conventional supervised baseline, not self-organization |
| Cold/replay/transport resets or copies | Labeled controls only | Never counted as neural recruitment |
| Ground-truth phases and perturbation labels | Evaluator/diagnostic only | Must not enter ordinary learner packets |

Concrete proposed Python boundaries for SOAM-034 (names may be translated to the
repository style without changing the data contract):

    ObservationPacket(z[2,12], valid[2], cue[16], cue_present, executed_action_previous)
    ModelState(key_state, pose_state, previous_weights, role_counters, evidence_age)
    Model.step(state, packet) -> (new_state, estimates[2,12], diagnostics)
    Model.predict(snapshot, actions[H]) -> estimates[H,2,12]
    Evaluator.score(outputs, hidden_truth) -> metrics

Time indices, target labels, phi, future packets, and process noise are absent from
ObservationPacket. Action is scalar; a[0] is the first executed transition after
observation 0. In predict, no new cues/corrections are received; action gains and
frozen model parameters are the only dynamics information. State is passed explicitly
and model modules own parameters only. A1 returns two references to its sole estimate
for evaluator comparison and declares the one-state limitation; it may not secretly
hold two histories. Stored episode packets are runner-owned, with replay receiving
only the prefix through the current observation. Model predictions cannot write to
history, persistent parameters, any other candidate, or the active interaction state.

SOAM-034 must test shape/finite contracts; observation-before-action indexing; alias
and snapshot isolation; no-write inference; target-label/future-packet exclusion;
exact equal-history reconstruction; role source retention; seed separation; expected
parameter counts; known-action propagation; autonomous energy/norm behavior; and
failure logging. Test the inverse restriction with a diagnostic_inverse stub that
raises if invoked by learner/prediction code. Reuse FixedProjection.forward and its
frozen matrix; retain the historical v0.1 contracts unchanged.

## 9. Resource and provenance accounting

In addition to trained and fixed tensor counts, record transient state, readout
outputs, role metadata, evidence history, optimizer state, cached operators, and
peak RSS. A2 has 40 recurrent floats (16+2*12); A1 28; G2/GS24 40; GS9 25. Previous
weights, priming scores, output estimates, and policy counters are additional,
not included in those recurrent counts. Tied weights are stored once; clones are
counted whenever materialized. Report logical batch and scalar per-episode costs.

For A key evaluation, a factorwise P/L implementation uses 2*16*3 + 3*3 + 2*16*3
=201 leading MACs per substep including coupling, or 4,020 per observation, excluding
softmax/nonlinear/vector arithmetic. An implementation reusing products may use fewer;
report the actual operation formula. Fixed-operator pose propagation, observation
correction, diagnostics, snapshot clones, and inference overhead are separate. GRU
costs include each gate projection and every readout; do not equate parameter count
with runtime. Estimate backward work separately from forward-only model calls.

Time model initialization, fitting, live inference, key recruitment, pose updates,
policy commit, replay, prediction snapshots, diagnostics, and artifact I/O separately.
For handover timing use archived seed-11 condition-0 episode IDs 0..3, A2/G2 only,
20 warm-up passes and 200 measured replay/pre-tracking passes in alternating order, identical CPU settings;
report median/p95 and total benchmark overhead, not independent accuracy samples.
Fixed budgets include these timing passes. No real-time robotics claim follows.

Each run must archive resolved manifest, protocol SHA-256, source commit and all
source hashes (including this protocol and manifest), dirty status, uv.lock, software/
hardware, dtype/thread/determinism settings, seeds/RNG derivations, packet/checkpoint
hashes, data exposure, losses, scalar metrics, trajectory diagnostics, resource counts,
timings, and complete/running/failed state. Refuse overwrite. The existing provenance
helper omits this protocol and hardcodes some runtime metadata; adapt or extend it
in SOAM-034 and report actual values. Do not silently reuse it as a complete audit.

Before measured SOAM-035 runs commit the implementation/protocol or explicitly
record a dirty source fingerprint. No remote push is required. Keep development,
confirmation, and repeat artifacts separate. Suggested roots are runs/handover-v1/
and runs/handover-v1-repeat/; archive compact evidence under reports/handover-v1/ and
summarize in reports/ATTRACTOR_HANDOVER.md. These paths are planned, not existing
results. Wall time/PIDs are excluded from exact numerical reproduction equality.

## 10. Focused primary-source review and limits

The reviewed sources motivate the controlled ingredients; none validates their
combination in SOAM. No quotations or biological equivalence claims are adopted.

| Primary source / reviewed portion | Supported design consideration | Limit and resulting protocol choice |
| --- | --- | --- |
| [Hopfield, 1984, PNAS, pp. 3088–3092](https://www.rctn.org/bruno/public/papers/hopfield84.pdf), especially continuous model and energy discussion pp. 3089–3090 | Associative retrieval can be studied through recurrent convergence and an energy function | Theorems depend on the stated system/weights; driven coupling and discretization require separate checks. Use autonomous probes, not a boundedness claim. |
| [Ramsauer et al., 2021, Hopfield Networks Is All You Need](https://arxiv.org/abs/2008.02217), abstract and [authors' model description](https://ml-jku.github.io/research/hopfield_networks/) | Continuous memory can exhibit single-pattern and mixed retrieval states | The protocol's damped gradient step with external/coupled forcing is a specified adaptation, not a claimed verbatim reproduction or inherited convergence theorem. Measure mixed states and endpoint recovery. |
| [Zhang, 1996, Journal of Neuroscience 16:2112–2126](https://pages.jh.edu/kechen/jns-hd.pdf), abstract and introductory discussion | Continuous state, motion-driven updating, and sensory calibration can be distinguished | The analytic radial ring here is not Zhang's neural-field model. Its supplied geometry supports only an engineered manifold test; phase truth still requires evidence. |
| [Davis et al., 2021, Neural Networks 138:78–97](https://www.cs.umd.edu/~grpdavis/papers/compositionality.pdf), manuscript §2.1 and Fig. 3 | Recovery connections, transition connections, and control/gating can play distinct roles | Their structured-memory experiments use explicit control and learned graph associations. Retain the distinction between those roles without adopting a graph traversal requirement or claiming their composition result for SOAM. |

Accessed 2026-11-01. The Ramsauer full PDF was inaccessible through the available web
fetch (OpenReview challenge; arXiv PDF size limit); only the abstract and authors'
public description were used. The displayed energy/update above is fully defined
and its gradient relation can be checked directly; do not attribute unreviewed
proof details to that paper. Broader source review remains SOAM-030/031 work.

## 11. Versioning and next step

v1 freezes these choices before any measured results. Implementation feasibility
failures may justify a v2 protocol, but preserve v1, explain each change, record
which data were viewed, and allocate a fresh confirmation namespace. Bug fixes must
also record affected runs. Numeric thresholds cannot be relaxed retroactively.

This document completes a research design deliverable only. SOAM-034 becomes ready
after its acceptance review; SOAM-035/036 remain backlog. No experiment, convergence
claim for the combined driven system, or empirical gate is completed by writing it.
