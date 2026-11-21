# E0-HOLD v1: longer zero-action training with navigation/recovery guardrails

SOAM-098 owns this lightweight RFC; SOAM-099/100/101 own implementation,
execution and review. Classification: **essential next**, freshly selected by the
[owner](requests/e0_hold_2026_11_21.md) after [SOAM-097](../reports/STUDY_E0_DECISION.md).
The [manifest](protocols/study_e0_hold_v1.json) freezes the numerical contract.
Historical E0 and all earlier negative/inconclusive outcomes remain unchanged.

## Question and controlled intervention

Does extending stationary training from 24 to 128 transitions reduce NAV32's
128-step pose error by at least five degrees, bring it below five degrees, and
preserve action navigation and local recovery within declared margins?
This tests the training-horizon explanation suggested by E0's observed drift.
It does not test hierarchy, routing, translation, sparse encoders or acquisition.

Reuse E0's fixed sensory projection, model equations, inference interfaces,
training generator and evaluator without modifying their historical implementation.
Compare **SHORT24** and **LONG128** for each of NAV32, SYM32 and GRU32. Include the
fitted PCA2 conventional estimator once per root: its supplied zero-action identity
does not need a duplicate long-training arm. Its state/covariance and fitting work
remain counted. All three neural families retain the same widths and readouts.

For each root/model pair, both arms start from exactly the same parameters and
receive the same 600 batches of 32 original 24-transition training episodes. An
episode is eligible for extension if every supplied action in that prefix is zero
(about one quarter of episodes). The moving episodes and every observed cue are
identical between arms. No new cue or physical observation is added after step 24.
LONG128 continues eligible hidden states for another 104 zero-action predictions,
with gradients through the whole trajectory. The target is a repeated copy of the
already supplied stationary sensory target. This is explicitly supplied stationary
invariance supervision, not new observations or unsupervised memory discovery.

For each episode j, loss is its mean prior feature NMSE plus .5 times its mean
posterior feature NMSE, including the initialized posterior. Moving episodes use
24 priors/25 posteriors; eligible stationary episodes use 24/25 in SHORT24 and
128/129 in LONG128. Average episode losses equally across the batch. Consequently,
longer episodes do not multiply the total weight of stationary examples. The
time-average within a stationary episode changes intentionally. No geometry loss,
state normalization, new architecture or extra optimizer step is introduced.

The extra recurrence/backpropagation is a real compute mismatch. Count it rather
than calling the comparison compute-matched. Distinct original sensory snapshots,
repeated stationary targets, optimizer updates and transition evaluations are
reported separately. Longer training here means longer temporal credit assignment,
not more optimizer updates or more independent environmental observations.

## Frozen fitting, streams and inventory

Learning rate .003, 600 updates, Adam, cosine decay to 1%, clip norm 1, and all other
E0 v1 settings are fixed. This rate was selected by the earlier development study;
there is **no new tuning or checkpoint selection**. Controls receive the same
opportunity. Loss/convergence traces remain descriptive, not permission to extend
training. PCA2 fits its unchanged model to the same prefix targets with ridge 1e-6.

Use twenty independent roots 301–320, paired across conditions. Map each to an E0
generator root using derived_seed("soam-e0-hold",1,"root-map",root,0,"streams"); record both.
The existing train/confirmation/fixture split mechanisms then remain isolated.
Initialization uses the existing model-specific seed at the mapped root and is
shared between arms. No E0 confirmation stream or fitted checkpoint is reused.
All paired evaluator streams and perturbations are identical within each family.

Inventory: twenty roots × seven cells = 140 confirmation fits, plus exact repeats
of all seven cells at root 301 = **147 scientific fits**. There are seven eight-update
fixture fits at root 9301 before science. No exploratory fits, adaptive sweep,
restarts, automatic retries or new development search. A software failure stops
execution and is recorded as invalid, not as scientific falsification.

## Endpoints, uncertainty and decision

Use E0's complete evaluation battery unchanged: 128 zero-action steps, 64-step
free action rollouts, grounded one-step prediction, returning-cue correction,
16-step transverse/tangential probes on a 256-pose reference family, and the
descriptive interpolation/extrapolation/constant-direction streams. Preserve the
paired-transverse-proxy and finite sampled geometry limitations. This is not proof
of a continuous invariant manifold or preservation of every pose.

**Primary contrast:** SHORT24 minus LONG128 mean stationary pose error in degrees.
Its adjusted lower confidence bound must be at least 5 degrees (a practical gain),
and LONG128's absolute adjusted upper bound must be at most 5 degrees (a fix).
Both intervals must be no wider than 4 degrees. Twenty roots are chosen before
fitting to improve precision over E0's ten-root stationary result, not after viewing
new confirmation. The original E0 precision rule and outcome are not changed.

The primary inferential family is NAV32 only, with **13 simultaneous intervals**:
the seven absolute LONG128 E0 endpoints, the primary stationary gain, and five
paired LONG128-minus-SHORT24 degradation checks below. Bootstrap independent roots
with 20,000 resamples, seed 32203, alpha=.05/13. Never resample timesteps as roots.
Also report unadjusted 95% intervals and root values. SYM32/GRU32 paired results and
PCA2 endpoint intervals are mandatory descriptive controls at 95%; they cannot be
substituted for the preregistered NAV32 claim or called confirmatory discoveries.

| Paired degradation metric (LONG minus SHORT) | Maximum adjusted upper bound | Maximum interval width |
| --- | --- | --- |
| Free-64 NMSE | .01 | .02 |
| Grounded one-step NMSE | .01 | .02 |
| Returning-cue NMSE | .01 | .02 |
| Transverse separation ratio | .05 | .10 |
| Perturbation-induced pose error | .5 degrees | 1 degree |

The seven absolute LONG128 requirements retain E0's thresholds and widths:
free/grounded/return NMSE upper <= .05, width <= .04; stationary error upper <=5°,
width <=4°; transverse ratio upper <=.5, width <=.4; induced pose error upper <=3°,
width <=3°; tangent-retention interval inside [.8,1.2], width <=.4. These absolute
requirements prevent a noninferior but still inadequate model from counting as fixed.

Support the declared fix only if all 13 adequately precise intervals pass. A
precisely established paired degradation beyond a margin is a **tradeoff**. Otherwise
an adequately precise primary gain below five degrees, persistent absolute failure,
or another precise absolute failure is **negative for the declared joint fix**.
Other cases are **inconclusive**. Apply precision before directional classification
to each interval, preserving unfavorable but wide evidence. Missing/degenerate
geometry cannot pass. Invalid execution is distinguished from scientific outcomes.
"Without hurting" means noninferiority within these margins, not exact equality.

## Resource and execution contract

Fresh cumulative ceiling: **7,200 CPU seconds, 14,400 execution-wall seconds,
2 GiB RSS and 2 GiB numerical artifacts**, including fixtures, repeats and numerical
postprocessing. One CPU thread, deterministic Torch, float32 recurrent models and
float64 fitted/statistical reductions. No GPU or paid service. Preflight must project
all fits/evaluations with a 2x margin below 80% of both time ceilings and below the
artifact ceiling; otherwise stop before science. Check limits during training and
evaluation, checkpoint atomically and preserve failed/partial inventory.

Freeze source/config/protocol identity before fitting, with a committed clean source
for confirmation. Save checkpoints, raw geometry/error arrays, learning traces,
training-data hashes, model/stream seeds, data exposure, software/numerics, resource
counts, timestamps and commands. Exact repetition checks arrays/parameters, not
timings. Repeated trials must match identity and completed payload hashes; never
silently overwrite an earlier result. Historical E0 files remain unchanged.

Required invariants include exact prefix/initialization pairing, SHORT24 equivalence
to the historical objective, stationary-tail eligibility/target constancy, no extra
observations or moving-tail gradients, correct episode weighting, no-write inference,
fresh streams, deterministic repetition and confidence/precision classification.
SOAM-101 interprets measured evidence and recommends at most one later fork; no later
experiment is automatically activated by this protocol.
