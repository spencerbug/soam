# SOAM-001 substrate controls — protocol v1

Frozen before measured comparison runs on 2026-10-25. This extends, rather than
replaces, [the original protocol](EXPERIMENTS.md) and [baseline](../reports/BASELINE.md).
It addresses H1 predictive representation and switching; it cannot establish reusable
primitives, attractors, composition, or self-organization. Gate 1 remains a separate decision.

## Fixed question and trial grid

Can budget-matched shared predictors represent and switch among the three regimes
under unfamiliar schedules and action paths, compared with GRU and fully independent
predictors? Six variants × seeds 11, 23, 47 = **18 measured training trials**:
additive, gated, low_rank, separate (the historical shared-interface control), gru,
and independent. Exactly six seed-11 repeats test reproducibility. No sweep, tuning,
checkpoint selection, retries for poor metrics, or adaptive stopping is planned.

Use `configs/substrate-controls.json`: the original 600 Adam steps, batch 48,
24-step training horizon, learning rate .003, loss and clipping, fixed projection,
CPU float32 and one thread. Train alternates steady and regular eight-step switches,
with IID uniform actions. Each model sees 691,200 transitions. Model initialization
uses the same three seeds; the new data namespace is 1. Original namespace 0 and
its artifacts remain unchanged. No conclusions are selected using the old test set.

Expected local budget: 24 training runs plus evaluations, under 20 minutes of CPU
wall time and 1 GB of stored output. Check elapsed time between trials and stop the
remaining grid if 20 minutes is exceeded; report partial coverage. No GPU, network,
or paid API computation. Debug smoke runs are software checks, not research trials.

## Models, budgets, and switching semantics

The additive width-40 predictor fixes the target **2,892 trainable parameters**.
Choose each alternative's integer width in [2,40] solely by nearest analytic total
parameter count; ties choose the smaller width. Reject a configuration exceeding
5% difference. Include all sensory initializer, readout, transition, context, and
modulation parameters; report actual counts, width, and mismatch. This is approximate
capacity matching, not equivalent expressivity or equal compute.

- Additive/gated/low-rank/separate retain the existing leaky recurrence, assimilation,
  and hidden-state carry at switches. Separate still shares sensory/readout layers.
- GRU uses an ordinary GRUCell with action plus one-hot context input, its own learned
  initializer/readout, and the same observation assimilation gain. Its gates determine
  timescale; it does not use the leaky baseline's alpha.
- Independent has disjoint initializer, transition, and readout weights for every
  context, with no shared trainable parameters. At a context switch it initializes
  the new active model from the **previous predicted observation**. This is a sensory
  coordinate handoff and hidden reinitialization, not continuous hidden-state carry.
  It adds no actual observation to a free rollout. Grounded evaluation then assimilates
  the actual current observation as it does for other models. Training differentiates
  through the handoff, so disjoint parameters do not imply isolated training objectives.

The fixed sensory encoder is common to all models and has no trainable parameters.
Independent hidden-gap diagnostics cross model coordinate changes; feature gaps and
error against reality must accompany them. A contracting handoff is not attractor recovery.

## Reserved evaluation streams

Train/dev/test/stability use distinct split IDs. New ordinary runner evaluations use
namespace 1. Extended evaluations use namespace `10000 + 10*horizon + condition_index`,
with split ID distinguishing development and test, for each of horizons 48, 192, 384.
Conditions in fixed order:

0. steady, IID actions;
1. regular switches every 8 transitions, IID actions;
2. irregular switches, IID actions;
3. irregular switches, actions held constant for blocks of 4 transitions.

Initial context is balanced (32 sequences per context); initial states and action
values retain the original distributions. Irregular dwell times are uniform over
{3,4,5,6,7,9,10,11,12,13}, sampled independently per sequence, with the next context
uniformly chosen from the other two. Final dwell intervals may be truncated.
These dwell times, context orders, and correlated-action paths are unseen in training.
They are controlled distribution shifts, not withheld contexts or composition tests.
Different horizons use different streams; report this rather than treating them as
prefixes of identical trajectories. Within a condition, all models receive identical
trajectories, and perturbed/unperturbed comparisons use the same trajectory.

## Metrics and preregistered screen

For every seed, condition, horizon, and development/test split report:

- Grounded one-step and free energy-normalized MSE, final-step error, per-start-context
  and per-active-context error, instantaneous and cumulative horizon curves.
- Error at each lag 0–7 since the **most recent** switch, with sample counts. Censor
  older-switch windows when another switch occurs; do not mix overlapping events.
- Nonfinite/bound-violating trajectory rates, maximum hidden magnitude, motion-energy
  ratio, and a diagnostic collapse flag for ratio < .25.
- Gaussian hidden perturbation at transition 8, standard deviation .15 per unit:
  paired hidden-gap ratios, feature gaps, excess error against actual observations,
  sustained halving, and invalid/bound rates at every horizon.
- Total parameters, parameter bytes, optimizer tensor bytes, retained trajectory
  tensor bytes, exposure, wall times, and linear MAC estimates. Tensor storage is not
  peak process memory. MACs exclude nonlinearities, assimilation, backward pass,
  Python dispatch, and independent switch handoffs; separately report switch counts
  and extra handoff MACs (readout is already counted, extra initializer costs d*h).

For each model/seed, the engineering screen requires at horizon 48 on held-out test:
steady free NMSE <= .15, irregular IID free NMSE <= .25, each steady start context
NMSE <= .25, steady error <= 25% of persistence, motion-energy ratio in [.25,4] in
steady and irregular IID, and final paired hidden-gap ratio <= 1 in both. All four
conditions at all horizons must have zero invalid or bound-violating unperturbed
trajectories. The 192/384-step errors, held-action condition accuracy, switch-lag
curves and perturbation excess errors remain diagnostics with no post-hoc thresholds.

A shared variant passing every seed supports a bounded Gate 1 review. Failing
controls, mixed results, or all failures still complete this experiment when reported.
Do not turn a failed screen into a passed one by changing thresholds or choosing seeds.
Three paired seeds support descriptive means/sample SD, not claims of significance.
No model ranking alone proves structural reuse. Gate 1 must interpret comparisons,
handoff confounds, and drift before authorizing local acquisition.

## Execution, failures, and artifacts

Primary agent owns protocol, code, trials, and conclusions. The local worker may
extract bounded logs or check a small result table; it may not choose parameters or
control trials. Worker output must be verified against saved artifacts.

Before measured runs: validate invariants, smoke the six variants, commit source and
this protocol, and save the resolved config/source hashes/software/numerical settings.
Use immutable output directories with per-trial checkpoint, training history, metrics,
trajectories, plots, and status records. A numerical failure stops the grid, preserves
completed results, and requires a documented correction/new output identity. Never
silently rerun a failed seed until it passes. No retry is planned except a documented
transient execution interruption with unchanged source/config/data.

```sh
uv run pytest
uv run python scripts/check_tickets.py
uv run python -m soam.evaluation.runner --config configs/substrate-controls.json --output runs/substrate-controls-v1
uv run python -m soam.evaluation.runner --config configs/substrate-controls.json --seeds 11 --output runs/substrate-controls-v1-repeat
uv run python scripts/check_reproduction.py runs/substrate-controls-v1 runs/substrate-controls-v1-repeat --output reports/substrate-controls/reproducibility.json
```

The runner saves both ordinary metrics/plots and extended diagnostics/trajectories.
Publish `reports/SUBSTRATE_CONTROLS.md`, compact measured records and representative
seed-11 plots in `reports/substrate-controls/`. Record grid coverage, failed trials,
source/config identities, limitations, and exact reproduction outcomes. Do not mark
Gate 1 complete in this ticket.
