# Gate 1 — proceed to bounded local-acquisition research

**Decision: proceed.** Recorded 2026-10-25 for SOAM-002 after review of the original
substrate experiment and SOAM-001 controls. The user selected “Proceed with low-rank;
retain GRU as a reference” during the interactive review.

Use the **width-37, rank-4 low-rank context-modulated recurrent model** as the primary
substrate. Retain the width-24 GRU as a conventional predictive reference. This is an
engineering choice for investigating H2; the stronger H1 claim of reusable dynamical
structure remains open. No associative writer is implemented by this decision.

## Evidence reviewed

- [Original baseline](BASELINE.md) and [original protocol](../docs/EXPERIMENTS.md).
- [Stronger controls report](SUBSTRATE_CONTROLS.md), [preregistered protocol](../docs/SUBSTRATE_CONTROLS.md),
  [configuration](substrate-controls/config.json), [results](substrate-controls/results.json),
  [readiness checks](substrate-controls/readiness.json), and [reproduction](substrate-controls/reproducibility.json).
- Controls source commit: `7238e6ce69ce5a4e561960b290a2222e5e16aeb5`.
  Source SHA-256: `6c0ae5c4344472957ab472298751be9348de55863012ae9f8ce2045df20af269`.
  Runtime/software/numerical settings are recorded in the linked
  [provenance](substrate-controls/provenance.json).

All 18 planned trials completed; 17 passed the frozen engineering screen. Low-rank
and GRU each passed all three seeds, with no unperturbed invalid/bound violations
through 384 steps. All six seed-11 models reproduced exactly. The experiment's
27-test suite passed; this review does not reinterpret tests as scientific evidence.

| Evidence, mean across three seeds | Low-rank | GRU | Implication |
| --- | ---: | ---: | --- |
| Trainable parameters | 2,873 | 2,916 | Both within 1% of the 2,892 reference |
| Grounded one-step NMSE, steady sequence | .0076 | .0017 | GRU predicts corrected states more accurately on average |
| Steady free 48-step NMSE | .0448 | .0438 | Similar means; no established superiority |
| Irregular free 48-step NMSE | .1065 | .0825 | GRU has lower mean; substantial seed variation remains |
| Irregular plus held-action 48-step NMSE | .1506 | .1033 | Retain GRU as a strong control |
| Irregular free 384-step NMSE | .3289 | .3225 | Both accumulate substantial long-horizon error |
| Final paired hidden-gap ratio, irregular 48 | .1640 | .2669 | Lower low-rank gap in this perturbation protocol |
| Perturbation excess feature MSE, irregular 48 | +.001113 | +.004562 | GRU is more sensitive under the tested perturbation |
| Mean training seconds | 4.74 | 4.03 | Parameter matching does not imply equal cost |

Both received 691,200 training transitions per seed. Low-rank uses 11,492 weight
bytes and an estimated 2,220 linear MACs per recurrent/readout step; GRU uses 11,664
bytes and 2,448 MACs. Nonlinearities, backward work, assimilation, and dispatch are
excluded from these estimates. Full seed variation, storage, timing, and assumptions
are in the controls report; three seeds support descriptive comparisons only.

## Why this choice

Low-rank combines a passing three-seed screen with a directly identifiable shared
recurrent matrix whose local modification can be studied without modifying GRU
gates. Its observed perturbation sensitivity is lower, although equal per-unit
noise does not imply equal functional perturbations across models. This makes it a
tractable first experimental substrate, not a proven better memory architecture.

The name `low_rank` refers to the existing rank-4 context modulation. It does not
mean the complete recurrent matrix or future accumulated updates must have rank 4.
No claim of learned reusable transformations follows from the model name.

The alternatives remain available:

- Additive remains a simplicity control, but seed 23 failed irregular accuracy
  (.2527 > .25). Do not erase that failure or automatically retain it as the primary.
- Gated also passes, but provides no compelling engineering reason to prefer it
  for the first writer over the selected matrix formulation.
- Independent predictors have the lowest mean irregular error (.0722), but they
  use separate parameter sets and predicted-feature handoffs at switches. Their
  success is a useful counterexample to treating good prediction as evidence of
  shared organization. They do not instantiate the shared substrate under study.
- GRU remains a predictive reference. Any online-gradient comparison intended to
  isolate the writer must also use the **same low-rank substrate and allowed plastic
  parameters**; a GRU comparison cannot substitute for that matched control.

## Reference checkpoint contract

The [checkpoint manifest](gate-1/checkpoints.json) records exact paths and SHA-256
hashes for low-rank and GRU seeds 11, 23, and 47 from `runs/substrate-controls-v1/`.
All six checkpoint files were loaded and their variant, seed, tensor dimensions,
and file hashes checked during this review.

For implementation/debugging, use `low_rank-seed11/checkpoint.pt`: seed 11 is the
predetermined fixture, not the best-performing seed. Measured local-acquisition
comparisons must start from **all three** low-rank checkpoints, preserving each
original and applying each learning rule to a fresh copy. Do not select the best
seed or continue ordinary pretraining. GRU checkpoints remain unchanged references
unless a later explicitly scoped comparison defines their adaptation contract.

Checkpoint files are currently local/Git-ignored. Verify manifest hashes before
use; archive or reproducibly regenerate missing artifacts before starting a measured
study. The manifest is not a claim that pushing the repository uploads these weights.

## Allowed plasticity and frozen interfaces

For the first local-write contract (SOAM-003), the only mutable persistent parameter
is **`recurrent.weight`, shape 37 × 37, 1,369 scalar weights**. This is the dense
shared recurrent matrix, not the context-specific rank-4 modulation factors.

Freeze the sensory projection, `sensory.*`, `readout.*`, `recurrent.bias`,
`action.weight`, `context.weight`, `down.weight`, `up.weight`, `modulation.weight`,
and the alpha/assimilation settings. Transient activity may evolve and assimilate
observations without changing any of those persistent values. Evaluation and
imagined trajectories must not commit updates.

SOAM-003 must define a grounded cue/target construction, bounded update proposal,
atomic apply/rollback, and provenance. An outer-product correction to this matrix is
an admissible starting family; cumulative updates need not remain rank one. This
review does not assert that the delta rule is already a valid recurrent learner.
A 12-dimensional observation embedding is not a unique 37-dimensional hidden target:
the target-lifting/correction procedure must be justified and cannot use evaluator
hidden world state. If this family is unsuitable, document a revision before adding
plastic tensors, extra capacity, or an adapter. Do not silently unfreeze the readout.

## Scope and failure conditions for the next study

Proceed to the local-write contract first, followed by the existing writer/interference
benchmarks and Gate 2. No learned scopes, consolidation, JEPA, or planning is started
by this review. SOAM-019's prerequisite is also satisfied under the existing roadmap,
but it remains an optional parallel branch; SOAM-003 is the next primary task.

Before measured writer runs, freeze a protocol defining changed regimes, observation
budgets, update norm/rank caps, development-only hyperparameter choices, and numerical
acquisition/retention tolerances. Use fresh train/development/confirmation namespaces;
SOAM-001's observed tests now inform model selection and must not be reused as an
unseen confirmation set for writer tuning. Keep the original checkpoint comparisons.

The following outcomes require explicit failure/revision handling:

1. **Integrity failure:** any imagined/evaluation write, changed frozen tensor, access
   to hidden ground truth by the learner, nonfinite proposal, or failed rollback
   invalidates the affected run. Stop and correct it before interpreting accuracy.
2. **Acquisition failure:** a rule that fails to improve changed-regime prediction
   against no adaptation at the preregistered observation budgets has not established
   H2. Improvement only on the just-written transition or only in grounded one-step
   error is insufficient; report held-out free-rollout effects through 48 steps.
3. **Retention/stability failure:** compare every unchanged context to its own prewrite
   behavior. Exceeding preregistered forgetting tolerances, introducing invalid
   trajectories, or producing unacceptable 48-step degradation prevents calling the
   update useful merely because changed-task error falls. Preserve such failures for
   SOAM-005/Gate 2; do not use final-test retention data to choose which writes to keep.
4. **Target/formulation failure:** if grounded observations cannot produce a defensible
   correction in the designated matrix, revisit the update representation. Do not
   substitute global end-to-end retraining and label it local acquisition.

At 192/384 steps, report postwrite drift relative to the frozen baseline even if
48-step acquisition succeeds. Gate 1 accepts existing long-horizon drift only for
this bounded local-writing investigation, not for reliable long-horizon planning.
The numerical success tolerances for H2 belong in the next preregistered protocol;
this review does not fabricate measured improvements or pass Gate 2 in advance.

## Claim boundaries and validation

The evidence supports multiple known regimes, sensory-grounded prediction, and
switching within one shared model sufficiently to investigate local writes. It does
not establish compositional reuse, inferred context, partial-observation recovery,
attractor structure, fixed-capacity continual learning, or embodied competence.
The stronger H1/shared-structure question remains open for the transfer/composition
program; a passing engineering screen is not a claim that every Stage 1 exit criterion
has been scientifically established.

This was an interactive decision review with no new training, code changes, or
weight updates. The local worker extracted a bounded comparison table; its reported
entries were checked against source rows, and omitted GRU fields were read directly.
Checkpoint identity verification and `uv run python scripts/check_tickets.py` passed;
relative report/manifest links were checked. Existing experimental test results are
cited above, not claimed as newly executed tests in this documentation-only review.
