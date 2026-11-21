# E0 v1: one learned action-navigable recurrent population

Owner: SOAM-094; implementation/trials/review: SOAM-095–097. Classification:
**essential next** under the [November 21 owner selection](requests/e0_2026_11_21.md).
This is the bounded first test of the [E0 proposal](proposed-studies/STUDY_E0_LEARNED_NAVIGABLE_ATTRACTOR_MANIFOLDS.md),
not its optional architecture sweep. The [manifest](protocols/study_e0_v1.json) owns
numerical choices. No fitting or confirmation preceded this protocol.

## Question and decision

Can a single offline-trained recurrent population maintain distinct orientations,
move them through actions, recover locally from transverse perturbations, and accept
returning evidence? Useful prediction alone does not establish attraction. A finite
sample of a circle and bounded trajectories cannot prove a continuous invariant
manifold. The operational claim is **bounded evidence for navigable, locally
recovering state geometry**, under H1/H6, not neuroscientific validation.

[Burak and Fiete (2009)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000291)
motivate testing accumulated motion error and stability separately.
[Sussillo and Barak (2013)](https://pubmed.ncbi.nlm.nih.gov/23272922/)
motivate direct analysis of recurrent state dynamics rather than inferring mechanism
from decoded behavior. Neither source establishes our proposed learned mechanism.
The original [RIM paper](https://arxiv.org/abs/1909.10893) is a later modularity reference;
input attention and communication are absent here.

## Task and information contract

One orientation evolves as theta[t+1] = theta[t] + action[t], modulo 2 pi; dt=1.
There is no radial decay. Preserve the initial sensory projection: the existing
seed-1729 orthonormal 2-to-12 projection of [cos(theta), sin(theta)]. These are fixed
overlapping sinusoidal features. The rank-two, fully identifiable sensor is deliberate
scaffolding, not a claim about natural images or learned encoders.

Only noisy masked features, masks and scalar angular increments enter inference.
The model API is initialize(z, mask), predict(h, action), correct(prior, z, mask),
readout(h). Prediction advances physical time exactly once; correction advances none.
Absent evidence is an exact no-op. Weights and buffers are frozen at evaluation.
Clean sensory targets are available to every learner offline, not at free inference.
The world angle and inverse sensory projection are evaluator-only. Distinct train,
development, confirmation and fixture streams are derived from protocol/version,
root, split, index and component. A confirmation root is an independently trained
system; episodes/timesteps are not independent inferential units.

Training episodes have 24 transitions, balanced stationary and moving examples,
four-step action blocks drawn from {-0.12,-0.06,0,0.06,0.12} radians. Half the
episodes have only an initial cue; the others receive cues every four steps.
Each cue exposes either six or twelve channels with noise SD .01. Training targets
are the complete clean feature vector at each time. Development and confirmation
use novel four-step block speeds {-0.18,-0.09,0,0.09,0.18}; report interpolation and
extrapolation separately as descriptive diagnostics. No action selection is learned.

## Fixed models and fitting

All neural states have 32 units, the same learned initializer, linear feature
readout and residual correction: h += .5 tanh(C[masked(z-D(h)),mask]), conditional
on any evidence. Initializer is tanh(E[z*mask,mask]). No object/pose labels or true
latent coordinates supervise a hidden state.

- **NAV32:** F(h,a)=.5h+.5 tanh(S h+b+(a/.12)K h), S=(W+W.T)/2,
  K=(V-V.T)/2. S starts near identity, V near zero; both are learned. Symmetric
  restoration and skew action coupling are supplied biases; a circle is not wired
  into the hidden state. This rate-network candidate is Hopfield-inspired. No
  discrete-time energy decrease or global asymmetric energy is assumed.
- **SYM32:** identical supplied architecture, initialization and training, but
  K=(V+V.T)/2. This controls the directed action-weight structure. It is not an
  equal-effective-parameter control: the full allocated matrices have redundant
  coordinates, and symmetric/skew degrees of freedom differ.
- **GRU32:** conventional GRUCell with scalar a/.12 and the same interfaces and
  losses. State counts match, parameter counts do not; GRU has more parameters.
- **PCA2:** fitted conventional estimator. PCA basis/mean come only from training
  sensory targets. Fit h[t+1]-h[t] on [a*h,a^2*h,a^3*h] with ridge 1e-6, then
  use the fitted dynamics and Kalman correction in the learned two-dimensional
  basis. Stationarity at zero action, rank two and polynomial action features
  are supplied. No true angle, projection inverse, exact rotation or radius
  normalization enters this baseline. Count its covariance and fitting costs.

Neural objective: prior sensory NMSE + .5 posterior sensory NMSE, normalized by
the known unit-circle feature power 1/12. Adam, gradient clip 1, 600 fixed updates,
batch 32; learning rate cosine-decays to 1% of its initial value. Select one initial
rate per neural family from {.001,.003} by mean development free-64 NMSE across
two independently fitted roots; deterministic first-setting tie break. No checkpoint
selection, restarts, geometry losses, online learning or confirmation tuning.
Log losses at 200/400/600 updates and last-versus-previous 100-update means; absence
of convergence limits interpretation but does not authorize extra fits.

## Endpoints and geometry probes

**Primary:** J, feature NMSE averaged over all 64 missing-input transitions, 128
fresh episodes per root. Initial cue is noisy/partial; no subsequent evidence.
Grounded one-step NMSE uses a separate observed episode stream. Correction recovery
uses another stream, 32 missing transitions then eight partial/noisy cues, scoring
the final posterior. These streams cannot enter fitting or model selection except
the explicitly named development primary.

Each root's evaluator also samples a uniformly spaced, randomly rotated 256-pose
grid. Initialize from complete clean features, then eight autonomous zero-action
updates to construct a reference family. The 128-update stationary test starts
from the initializer and scores absolute circular orientation error at the end.
The other probes start at the eight-update family and use 16 autonomous updates:

1. Estimate each local tangent by centered adjacent-state differences. Add one
   seeded random orthogonal perturbation of norm .1 times the mean centered family
   radius. Compare perturbed and unperturbed endpoints, project their separation
   perpendicular to the endpoint family's tangent, divide by the injected norm,
   and average. This is a **paired transverse contraction proxy**, not a measured
   basin volume or proof of convergence to an invariant manifold.
   For PCA2, perturb its two represented mean coordinates only; its four covariance
   entries remain counted resources, not orientation coordinates. The neural
   populations expose all 32 coordinates to the same probe.
2. Measure the induced decoded angular displacement from the paired unperturbed
   endpoint. Contraction cannot count as success if it sends the state to another pose.
3. Use valid neighboring family states four grid bins apart (about .098 radians)
   for a tangential perturbation. Report mean signed decoded angular separation
   at step 16 divided by separation at step zero. Do not require return to the
   original pose: no new information distinguishes two valid orientations.

Report initial/final reconstruction, hidden family radius, tangent degeneracy,
zero-action drift, normal and tangential traces, and simple positive/negative action
rollouts. Degenerate tangents, zero denominators, nonfinite values or unavailable
orientation cannot silently pass; mark affected geometry invalid. E0 does not
estimate a mathematically exact manifold, load capacity, basins for stored objects,
or cross-module reference-frame consistency.

## Frozen inference and outcome rules

Ten paired independent confirmation roots. Use the existing root bootstrap with
20,000 resamples, fixed seed 12203. Report 95% descriptive intervals and simultaneous
Bonferroni intervals across seven endpoints and four models (alpha=.05/28 each).
Intervals describe training/task root variation, not all possible architectures.
The small root count and extreme adjusted quantiles are explicit limitations.

| Endpoint | Passing adjusted interval | Maximum adjusted width |
| --- | --- | --- |
| Primary free-64 J | upper <= .05 NMSE | .04 |
| Grounded one-step | upper <= .05 NMSE | .04 |
| Zero-action pose error after 128 | upper <= 5 degrees | 4 degrees |
| Transverse separation ratio at 16 | upper <= .5 | .4 |
| Perturbation-induced pose error | upper <= 3 degrees | 3 degrees |
| Tangential separation retention | contained in [.8,1.2] | .4 |
| Returning-cue final posterior | upper <= .05 NMSE | .04 |

All seven adequately precise passing intervals support only the bounded operational
claim for that model. Any adequately precise interval wholly outside its acceptable
range is negative evidence for that configured model under this budget. Otherwise
classify inconclusive, retaining individual failures and wide intervals. A software
or invariant failure is invalid execution, not scientific falsification. Wide
intervals are never equivalence. Paired NAV32-minus-control prediction differences
are descriptive, not a preregistered superiority claim. A successful GRU is a valid
candidate for later module work; a conventional estimator may be the useful reference
even if it has no transverse attraction.

## Finite inventory, resources and stopping

Before scientific fits: one four-model fixture (eight neural updates), invariant
tests and a measured runtime/artifact projection. Maximum four fixture fits.
Scientific inventory: 14 development fits (3 neural families x 2 rates x 2 roots,
plus two PCA2 fits); 40 confirmation fits (4 families x 10 roots); four exact
repeats of the first confirmation root. Total 58 scientific fit attempts. Model
selection is frozen before confirmation. Save every checkpoint, loss trace, raw
metric/probe array, source/config hash, software/numerics, data exposure, resources,
timestamps and command. Exact repeat compares checkpoints and arrays, not timings.

Fresh cumulative ceiling: 3,600 CPU seconds, 7,200 execution-wall seconds, 2 GiB
peak RSS and 1 GiB numerical artifacts, including fixture/repeats. One CPU thread,
float32 models, deterministic Torch; fitting PCA/ridge and reductions use float64.
No GPU, paid service, unbounded background job, automatic retries or budget extension.
Check limits within training/evaluation; preserve partial inventory on failure.
Preflight must project <=80% of CPU/wall ceilings with a 2x margin; otherwise stop
before scientific fitting and revise transparently. Development selection cannot
change widths, model equations, thresholds or the confirmation population. Runtime
fixes before scientific fitting preserve v1; material scientific changes require a
version and fresh streams. No confirmation results are recycled as unseen evidence.

SOAM-097 accepts the scoped evidence and recommends at most one next fork. Coupling,
reference-frame translation, learned routing, hierarchy, HTM, capacity sweeps and
persistent acquisition remain unselected. Historical E1 stop, D-R1 negative and
D-R2 inconclusive outcomes remain unchanged.
