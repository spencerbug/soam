# Substrate experiment protocol v0.1

Historical protocol for the existing baseline, preserved without changing its
experimental contract. The adopted [v0.2 scope](RESEARCH_SPEC_V0_2.md) prioritizes
cue-driven concurrent attractor handover. [SOAM-033](../tickets/SOAM-033-handover-protocol.md)
has specified the [new handover protocol](HANDOVER_PROTOCOL.md). SOAM-034 implemented
the [fixture-verified harness](HANDOVER_HARNESS.md); measured trials remain future
work. This v0.1 protocol does not specify them.

The adopted [v0.3 scope](RESEARCH_SPEC_V0_3.md) now prioritizes a shared-population
experiment platform. New shared-dynamics, localization, and learning-module studies
require their own versioned protocols and manifests; neither this historical protocol
nor handover v1 is silently extended to cover them. See the [current queue](../PRIORITIES.md).

This protocol was written before the first measured benchmark. It implements
Stage 0 / the immediate substrate sprint, not fast plasticity or self-organization.

## Hypothesis and scope

Operational question: can a bounded action/context-conditioned recurrent model
predict three simple regimes, switch without resetting activity, and tolerate
hidden-state perturbations sufficiently to justify testing online writes?

The initial synthetic observation is fully observable 2D state encoded into 12
features by a frozen orthonormal random projection. This isolates dynamics from
perceptual learning. Known context is provided, not inferred. A learned tanh
projection initializes hidden state; a trained linear readout predicts features.
Grounded prediction blends predicted hidden state with sensory-projected state
(gain 0.5). This is a simple assimilation baseline, not a probabilistic belief update.

## Environment

For state x, context center b, and action a=(angular, dx, dy):

`x_next = b + 0.995 * R(theta_context + 0.08*a[0]) @ (x-b) + 0.015*a[1:]`

Contexts: clockwise -0.18 rad, counterclockwise +0.18 rad, and +0.14 rad around
center (0.2, -0.15). The third adds context-dependent translation relative to the
origin. Starting radius is uniform [0.25, 0.8], phase [-pi, pi], actions [-1,1]^3.
There is weak contraction but no hard clipping of the environment state. Long
switching rollouts can leave the training-state distribution; this is reported.

Projection seed 1729 is fixed for all data and model seeds. Independent random
streams derive from `(seed, split_id)` for train/dev/test/stability. Training sees
fresh generated sequences; test trajectories are never optimized. State and action
distributions intentionally overlap; this is held-out-trajectory generalization,
not held-out context/composition or proof of transfer.

## Models and budget

All models use leaky tanh recurrence (alpha=0.7), learned sensory initialization,
readout, and the same assimilation rule:

- **additive:** recurrent state + action projection + context embedding.
- **gated:** context modulates recurrent input multiplicatively, with additive context.
- **low_rank:** shared recurrence plus context-modulated rank-4 correction.
- **separate:** disjoint per-context transition matrices with shared sensory initializer
  and readout. The active state is carried without reset at switches.

Separate cores use a width chosen to be closest to additive's total parameter count
(within 5% for the default). This is a partial independence baseline; it is **not**
a full ensemble of independent encoders/readouts. Gated and low-rank have additional
parameters at the same width. Both differences are recorded; no matched-capacity
advantage or reusable structure may be inferred from this initial comparison.
A fully independent predictor comparison and budget-matched gated/low-rank variants
remain work for a later H1 study.

Persistence repeats the initial observation in free rollouts and the most recent
observed feature in grounded one-step evaluation. It requires no fitted parameters.
Wrong-context and reversed-action evaluations are diagnostic interventions, not
separately trained ablations.

## Training and test schedule

Default seeds: 11, 23, 47. Fixed 600 Adam steps, batch 48, 24 transitions per sequence;
no checkpoint selection. Alternate steady and switching batches, switching every
8 transitions. Loss = free-rollout MSE + 0.3 grounded one-step MSE + 0.1 initial
reconstruction MSE. Clip gradient norm at 1.0. Identical data exposure and order for
all model variants. This is ordinary offline BPTT, not the proposed fast writer.

Test: 32 independent sequences per starting context for each condition, 48 steps
(twice training horizon), and a separate 192-step switching stability stream.
Steady and switching conditions use separate generated trajectories. Seeds are
paired across model variants. Development results are also saved; future tuning
must use development, then a newly reserved confirmation set. Do not silently tune
against these test results.

## Metrics and diagnostics

- MSE and energy-normalized MSE = mean squared prediction error / mean squared target.
  This is not R². Includes one-step grounded, free rollout, each horizon prefix,
  per starting context, final-step, and long-horizon errors.
- Grounded evaluation observes each actual current feature before predicting its
  successor; free evaluation only receives the first observation. No state resets
  at context switches. Report error by transitions since each switch.
- Perturb hidden state at step 8 with zero-mean Gaussian noise, standard deviation 0.15 per unit;
  compare to the same unperturbed model trajectory. Record gap decay, sustained
  halving over the last four steps, excess error against reality, and bound violations.
  The injected state is not clipped; bound metrics cover returned predicted states.
- Hidden bounds: any |h| > 1.5; separately record nonfinite trajectories. Leaky tanh
  ensures unperturbed bounds structurally. These statistics cannot prove attractors.
- Predicted/true temporal motion energy helps expose collapse into nearly fixed states.
- Parameters, weight bytes, optimizer tensor bytes, retained evaluation tensor bytes,
  linear multiply-accumulates per transition, training and inference time, data exposure.
  Tensor bytes are **not peak process memory**; MACs omit nonlinearities/backward pass.
- Plots: loss, ordinary optimizer update norm, prefix error, truth/predicted trajectories,
  context switches, and paired perturbation response. Ground truth inverse projection
  is used only in diagnostics.

## Initial decision criteria

Chosen before observing benchmark results; provisional engineering thresholds:

1. Every tested seed has steady free NMSE <= 0.15 and switching free NMSE <= 0.25.
2. Every steady context has NMSE <= 0.25.
3. Steady free NMSE is <= 25% of the zero-fit persistence reference.
4. No invalid/bound-violating unperturbed 192-step trajectories.
5. Mean final hidden gap / injected gap <= 1.0 in steady and switching perturbation
   trials, with grounded excess error reported. Halving is diagnostic, not mandatory:
   physical rotational dynamics can retain phase differences.

Passing these is a **substrate readiness screen**, not full Gate 1 or H1 confirmation.
Reuse, truly matched alternative budgets, and stronger independent baselines remain
necessary. Failing is a documented negative result; revise the substrate/protocol
explicitly before investigating associative writes. Three seeds give descriptive
spread, not a claim of statistical significance.

## Provenance and reproduction

Each output directory refuses overwrite. `config.json` is fully resolved;
`provenance.json` records commit, dirty status, per-source and aggregate SHA-256,
configuration hash, Python/Torch/NumPy, device/dtype, thread and deterministic settings.
Checkpoints and compressed trajectory artifacts accompany JSON metrics and PNGs.
`status.json` distinguishes running/complete/failed runs. Commit source before research
runs; a dirty working tree is detectable and must be disclosed. Wall-clock values
are not expected to repeat. Unit tests repeat a tiny end-to-end run exactly excluding
wall times. Benchmark numerical repeatability is checked on one full model/seed.
