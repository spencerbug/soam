# Grounded local-write contract (SOAM-003)

Implemented: frozen prediction snapshots, a bounded local correction rule, inspectable
proposals, explicit commits, and one-level exact rollback. This is an engineering
interface, **not demonstrated online acquisition or support for H2**. Comparisons of
learning rules and changed dynamics belong to SOAM-004.

## Parameter boundary

Gate 1 selects the width-37 low-rank context-modulated model. `LocalMemory.from_manifest`
checks the designated checkpoint file SHA-256 and loads a private model copy without
changing the caller's Torch RNG. All tensors disable autograd; only explicit commits
can replace `recurrent.weight` (37×37). Source models/checkpoints, sensory projection,
initializer/readout, bias, action/context weights, modulation factors, and alpha/
assimilation settings remain unchanged. Context is still externally supplied.

`predictor()` returns a detached copy with a rollout interface and no writer methods.
Old snapshots retain old predictions after a commit. Obtain a fresh snapshot to use
new memory. Prediction, grounded assimilation, and imagined rollouts cannot call back
into the writer: the snapshot has no reference to it. Evaluation data does not enter
a free rollout. Internal underscore attributes are not a security sandbox against
arbitrary Python code; mutation outside the API is unsupported and integrity checked.

## Grounded inputs and transient state

`GroundedEvidence` supplies source/evidence/episode IDs, start step, origin, split,
actual encoded observations [T+1,12], executed actions [T,3], and known contexts [T].
The declared encoder fingerprint must match the frozen seed-1729 projection.
Only sensor/simulator origins and adaptation/development splits authorize proposals.
Test/evaluation and imagined origins are rejected. This is a caller-attested provenance
boundary, not a way to independently prove observations came from the physical world.
The synthetic environment's actual transitions count as grounded simulation evidence.

The writer reconstructs a detached current activity state from the observed history,
assimilating only observations up to the current time. The final outcome is used only
as the correction target. It cannot supply hidden simulator states. Reconstructing
history under current weights is an initial implementation choice, not a persistent
belief-state tracker. Its cost grows with history length and is logged. Future long
no-reset interaction belongs to SOAM-005; bounded history selection must be explicit.
Evidence payloads are cloned and hashed. Caller mutations cannot change a pending write.

## Local correction formulation

Let h be the current grounded recurrent activity, s the next preactivation, R the
frozen sensory readout matrix, and e = observed_next_feature − predicted_next_feature.
For leaky tanh recurrence, the local Jacobian from s to the predicted feature is:

    J = R diag(alpha * (1 - tanh(s)^2))
    delta_s = J.T solve(J J.T + damping I, e)
    delta_W_raw = learning_rate * delta_s h.T / (||h||² + key_epsilon)

This is a damped, minimum-norm local linearized correction and normalized outer-product
write. It uses a 12×12 float64 linear solve, then returns a float32 update. It does not
infer a unique 37-dimensional target from the 12-dimensional feature or use inverse
tanh near saturation. It is not backpropagation through time, global retraining,
Hebbian learning, or an established recurrent memory algorithm. The linearization may
be inadequate; finite changes may fail to improve even immediate prediction. That is
an experimental question for SOAM-004.

`CorrectionRule` consumes detached local signals and produces a raw matrix proposal;
future baselines can implement that interface. It never receives the live memory.
The transaction layer independently checks shape, finiteness, and nominal update rank,
then clips Frobenius norm. Default engineering settings: learning rate .1, damping
.001, key epsilon 1e-8, nominal rank at most 1, per-write norm at most .01, cumulative
**sum of applied norms** at most .1. These are untuned example limits, not preregistered
H2 success thresholds or optimized hyperparameters. SOAM-004 must freeze its own search
and evaluation protocol before measuring acquisition.

The cumulative path budget is conservative: opposing updates do not refund it; rollback
does. Float32 addition can change the numerical rank of the applied matrix difference,
so both nominal and applied numerical ranks are logged. A 0.1% clipping margin and at
most 16 numerical halvings (then a zero-update fallback) enforce the actual rounded
norm cap near an exhausted budget. This backoff uses no accuracy/retention outcomes.
Zero cues, zero residuals, and exhausted/rounding-limited budgets can yield no-ops.

## Transactions and audit records

One proposal can be pending. `propose` does not mutate persistent parameters; its
inspectable delta is the effective float32 candidate-minus-current difference. `commit`
checks the proposal digest, source-state identity, revision, candidate identity, and
frozen-state integrity, then swaps in the fully prepared candidate under a lock.
Readers use detached snapshots. Proposal mutation, stale/double commits, and external
parameter/settings changes fail closed. `discard` drops a pending proposal without
changing memory. `rollback(receipt_id)` restores the immediately preceding model and
norm budget exactly; it rejects old receipts or pending writes. Revisions increase
even on rollback to avoid accepting stale proposals after returning to identical weights.

Commit is atomic within this process/API; it is not a crash-durable database transaction.
No filesystem I/O occurs during commit. The caller persists returned audit records and
checkpoint artifacts; the demonstration runner does so in a new output directory.

Records include source checkpoint file hash, full before/after state-and-settings
fingerprints, evidence payload hash and provenance, correction config, raw/proposed/
applied norms, ranks, changed names, parameter/update bytes, timing, history exposure,
and fixed-cue one-step errors. `mse_before/after` hold the current cue fixed; they are
not held-out acquisition metrics. Proposal IDs include timing-bearing audit records;
persistent state fingerprints, weights, and predictions are deterministic, while IDs
and timing need not match across executions. Per-proposal target count is not a unique
new-observation count: repeated evidence retains its ID and must be deduplicated by
the experiment harness when reporting acquisition efficiency.

Only one previous model is kept for rollback, not an episodic replay/world-model buffer.
Model weights occupy 11,492 bytes per copy and effective update tensors 5,476 bytes;
caller-held snapshots, candidates, prior model, history, solve/SVD workspace, Python
objects, and serialization consume additional memory. Counts are not peak process RAM.
The local solve's leading arithmetic includes 5,328 MACs for J J.T, 444 for J.T times
the solution, approximately 1,440 FLOPs for dense solve, and 1,369 outer-product
multiplications; these estimates omit reconstruction, derivatives, clipping, rank SVD,
hashing/copying, and allocation. Measured timings include those proposal operations.

## Engineering verification

Run `uv run pytest tests/test_plasticity.py` and the full suite. The tests cover no-write
inference, frozen tensors/settings, grounded-only evidence, target exclusion from the
cue, proposal tampering, rank/norm budgets, atomic rejection, exact rollback, loader
identity/RNG preservation, and an analytic check of the local linearized solution.

    uv run python scripts/check_write_contract.py --output runs/local-write-contract-v1

The three-seed demonstration uses untouched Gate 1 checkpoints, namespace 2002 for
one grounded write per seed and fresh development namespaces derived from 2003 for
steady/irregular 48/192/384-step diagnostics. It saves before/after weights, evidence,
audit records, configuration and provenance, and checks exact rollback. There is no
hyperparameter search, changed-regime acquisition curve, final test set, learned scope,
or consolidation in this ticket. Poor multistep changes are recorded, not filtered.
