# Study B: temporal gating of sensory assimilation

Confirmation complete, 2026-11-11; reproduction and independent audit are in progress.

The frozen primary test classifies learned sensory gating as a **tradeoff**, not a
supported practical benefit. GA32's paired-root gain over fixed correction PC32 is
3.44% (family-adjusted interval −0.86% to 7.86%), excluding the declared 10% benefit
at this precision. Corruption error increases by 0.03435 NMSE (adjusted interval
0.02811 to 0.03972), exceeding the 0.01 guard margin. The fitted two-state filter
has the lowest primary error but is especially vulnerable to corrupted snapshots.
No configuration or threshold changed after confirmation exposure.

## Scientific scope and prior evidence

The owner-selected study asks whether separating prediction, sensory correction and
zero-time settling improves recurrent sensorimotor inference at controlled evidence
and explicit computational cost. Study A recommended ordinary R32 as a small
competent starting core, with an accuracy tradeoff, and found its formal adaptive
update benefit inconclusive. The owner removed the copied GRU requirement. This
study searches ordinary 16/32-unit tanh recurrences and correction/control variants;
it preserves the historical GRU scores without treating them as matched Study B
measurements. Study A's learned two-dimensional model motivates stronger mask-aware
reconstruction and filtering controls.

The task is a low-dimensional, projected state-estimation benchmark with heavy
supplied structure: three action channels, known recall/motion roles, a fixed
12-feature projection and offline supervised training. It does not establish
attractors, shared-neuron superiority, compositionality, unsupervised discovery,
control benefit, online learning or biological validity. SOAM-052's negative gate
and all historical results remain unchanged.

## Frozen design

[Protocol](../docs/STUDY_B_PROTOCOL.md), [manifest](../docs/protocols/study_b_v1.json),
[implementation verification](STUDY_B_IMPLEMENTATION.md) and
[biological note](STUDY_B_BIOLOGY.md) specify assumptions and evidence boundaries.

Six schedules (every 1/2/4/8, seeded irregular, initial-only) are crossed with nine
conditions: full features, partial features, missing events, high noise, transient
corruption, contradictory snapshots, genuine state change, altered movement and a
long sensing gap. There are 20 episodes per cell and 64 physical steps. All models
receive identical information for each paired root. Half the physical intervals
use each known role; action and feature inputs have declared roles, not empirically
discovered neuron semantics. Actual sensing schedules are supplied, not learned.

Every prior is recorded before accessing the current measurement. Corrections may
change the state; internal iterations apply no action or simulator time. The
conventional mixed model recomputes its posterior from the previous state using
both action and observation, with its extra prediction branch explicitly charged.
Ground truth enters training losses and evaluator reductions only.

Sixteen candidates cover mixed-input recurrence, residual correction, cue-free
settling, repeated-input and conventional extra-compute controls, mask/residual/
state/action/metadata gains, independent motion gain, historical-form L2, mask-aware
reset and a fitted Kalman-form filter. Neural parameters are trained offline with
identical records and two learning rates, 1200 updates, batch eight, horizon sixteen
and a common decay. Linear references fit PCA/bilinear dynamics from the same
feature targets using two ridge penalties. No simulator coordinates, formulas or
projection inverse are supplied to any competitor.

The primary endpoint is pre-correction NMSE averaged equally over the four
intermittent schedules and partial/missing/noise conditions, then reduced within
root. Its variance denominator comes from 2048 independent training-distribution
samples. GA32 versus PC32 and MIX32 is the fixed primary comparison. A 10% practical
gain, positive adjusted intervals, bounded interval width, absolute competence and
four guardrails per comparator are jointly required. Ten paired roots are the
uncertainty units; 20,000 bootstrap resamples and a ten-contrast Bonferroni family
were frozen before confirmation. All other model and settling comparisons are
prespecified descriptive analyses.

## Development and execution

All 64 development fits completed using roots 11003 and 11027. Selected primary
settings: MIX32 and PC32 LR 0.01, GA32 LR 0.003. SET32 selects one extra iteration,
REP32 two, MIXC32 four. Other settings and late learning curves are retained in the
receipt. None of the three primary models crossed the >20% late-improvement flag;
this finite screen does not prove optimizer optimality.

The immutable confirmation receipt is
`ea64dceeda1dd283e8fda8af11e434e0a63159561822f762cf40a395429b701d`
(structured-content digest, excluding its own hash field).
Source commit `0e03e0dfb22f309c40f8339cd643b26d0be84f44`; aggregate source fingerprint
`ae6754ce8e177d17ad5ee4590814e5176190bb3e301907a81603c996acb06602`.
The 79-file snapshot includes the model/data/evaluator/statistics code, tests,
manifest, protocol and dependency lock. No source change separates development
from confirmation.

Confirmation roots: 12007, 12011, 12037, 12041, 12043, 12049, 12071, 12073, 12097,
12101. Root 12007 is the prescribed complete numerical repeat. Hardware is an
Apple M3 Max, Mac15,10, 36 GiB system memory. Runtime: Python 3.12.13, PyTorch
2.14.1, NumPy 2.5.4, macOS 26.6.2 arm64; local CPU, one Torch thread, deterministic
algorithms, float32 neural operations and float64 fitting/reductions.

## Interpretation constraints

Matched physical observations and state-update counts do not imply identical
MACs, parameter counts or training CPU. SET32, REP32 and MIXC32 train with four
internal iterations; testing smaller k is a controlled inference intervention on
those trained weights. The conventional/repeated-input controls are necessary to
interpret a benefit; a worse k=0 result alone cannot prove a general need for
settling. SET32's learned continuation head has additional parameters and auxiliary
supervision from training reconstruction improvements. Its gain is not a confidence
probability. Neural probabilistic confidence calibration is therefore not claimed.

The filter receives a supplied two-dimensional prior and learns its observation
basis and bilinear transition. Its covariance is transient; the ordinary comparator
assumes noise SD 0.01. The separate supplied-noise diagnostic receives actual nominal
SD, while corruption remains unflagged. Neither is an oracle. Discrete abrupt state
changes are unpredictable before their first revealing observation and impose an
irreducible component of error on every model.

Training sees full sensory targets, including unexpected-change examples, while
inference sees scheduled partial measurements. Training targets are equally
available to all competitors and separately counted. Six observed feature channels generally span the supplied two-dimensional
state; partial sensing therefore need not be fundamentally ambiguous. There is
no many-pattern associative-memory load in this task. The state-estimation task,
loss, horizon and role switching differ from Study A, so its endpoint numbers
cannot be compared as if they were new paired observations.

Recovery statistics use an explicit three-consecutive-step criterion, report
horizon-capped means and right-censoring fractions. They measure recovery relative to each trajectory's pre-event
baseline, not success in a downstream control task. Update/MAC figures exclude
universal evaluator diagnostics, matrix inverses/solves and nonlinear arithmetic;
measured evaluation CPU includes diagnostics and Python orchestration. Both must
be read together. Independent-root intervals describe this finite task and fitting
procedure, not arbitrary environments or all possible architectures.

The filter's covariance is additionally assessed by a **post hoc descriptive**
calibration audit: 90%/95% Gaussian ellipse coverage, squared Mahalanobis error and
Gaussian negative log likelihood in its learned two-dimensional sensory basis.
This uses existing frozen checkpoints and observation streams and does not affect
selection, primary tests, or decision thresholds. Neural sensory gains and the
settling continuation head are not interpreted as calibrated probabilities.
