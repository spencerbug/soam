# SOAM-003 — grounded local-write contract

**The engineering contract is implemented and verified.** The writer creates an
inspectable, bounded update from observed simulator/sensor evidence, changes only
`recurrent.weight`, and can restore the preceding persistent state exactly. Prediction
snapshots expose no write methods. **This does not establish H2 acquisition.**

The [Gate 1 decision](GATE_1_REVIEW.md) and [checkpoint manifest](gate-1/checkpoints.json)
remain authoritative. The implementation uses the selected width-37 low-rank model,
with all initializer/readout, action/context, modulation, bias, and timescale settings
frozen. The fixed encoder is external to memory and its declared fingerprint must
match the seed-1729 projection. Context is still an explicit input scaffold.

## Implemented interface and formulation

The [contract documentation](../soam/plasticity/README.md) defines the API, assumptions,
numerical limits, and trust boundary. Implementation: [transaction layer](../soam/plasticity/memory.py),
[local correction rule](../soam/plasticity/rules.py), and [invariant tests](../tests/test_plasticity.py).

The first rule maps observed feature error back through the frozen readout and local
leaky-tanh derivative using a damped 12×12 linear solve. It then forms a normalized
outer product with the current activity cue. This is a local linearized correction,
not a unique hidden-state target, global training, or an established associative
recurrent memory mechanism. The next benchmark must compare it with simpler rules.

The cue is reconstructed from observed history without reading the final target;
only the last transition supplies correction evidence. No simulator hidden state is
accepted by the evidence interface. Observed origins, writable splits, feature/action
shapes, finiteness, context labels, and encoder identity are checked. Provenance is
caller-attested: software cannot prove that a caller's declared observations are real.

The transaction layer validates each rule's proposal independently. It checks rank,
clips norm, prepares an isolated candidate, fingerprints the entire persistent state
and settings, and supports explicit commit/discard. Commit swaps in a prepared model
under a lock. Rollback restores one preceding model and its norm budget. Old snapshots
remain unchanged. Stale/tampered proposals, wrong checkpoint hashes, changed frozen
settings, and unsupported evidence fail closed. This is in-process atomicity, not a
crash-durable database transaction or a sandbox against malicious Python.

The example configuration caps nominal proposal rank at one, per-write Frobenius
norm at .01, and cumulative sum of applied norms at .1. The cumulative path budget
is stronger than a distance-from-origin bound; opposing updates do not refund it.
One-level rollback does refund the reverted write. A numerical rounding regression
was caught in tests: near exhaustion, float32 addition could exceed the remaining
budget. Bounded numerical halving/zero fallback now checks the actual applied norm;
it does not select updates using prediction or retention outcomes.

## Reproducible engineering demonstration

Source commit: `917eff8eebe9ffdaada8908d763bcf0a7b5a7b68`.
Source fingerprint: `cbcc1b19d4582b102acbeecd0bf2844f7ed834fb4a392db27ba484b911c1e2fa`.
Both original and repeat began with clean working trees. See [configuration](local-write-contract/config.json),
[source/software provenance](local-write-contract/provenance.json),
[repeat provenance](local-write-contract/repeat-provenance.json), and
[reproduction record](local-write-contract/reproducibility.json).

- Unmodified Gate 1 checkpoints for seeds 11, 23, 47; CPU float32 memory, float64
  regularized solve, one Torch thread and deterministic algorithms. Python 3.12.13,
  PyTorch 2.14.1, NumPy 2.5.4; no optimizer/BPTT used by the writer.
- Exactly one proposal and commit per seed, followed by rollback. No search, selection,
  repeated attempts for favorable accuracy, or changed dynamics. Three original runs
  and three repeats completed, with exact numerical metrics and before/after weights.
- One four-transition observed history is supplied per seed; the final transition is
  the single write target. The other three transitions ground the current activity.
  Source namespace 2002/train is distinct from prior substrate data. History reads are
  counted separately from targets; neither is a claim of unique new examples in a
  future replay-based experiment.
- Development-only diagnostics use six trajectories per condition (two per starting
  context), steady/irregular schedules, and horizons 48/192/384. Namespaces are
  `2003 + 10*horizon + condition_index`, with the development split. No final-test
  acquisition claim is made. No evaluation trajectory determines whether a write is kept.
- Each update records source checkpoint hash, before/after persistent fingerprints,
  evidence digest, config, norms, nominal/applied ranks, parameter/update bytes,
  elapsed times, target count, history length, and immediate fixed-cue prediction errors.

| Seed | Observed-transition MSE before → after | Applied norm | Steady free 48 NMSE before → after | Irregular free 48 NMSE before → after | Irregular free 384 NMSE before → after |
| --- | ---: | ---: | ---: | ---: | ---: |
| 11 | .00012225 → .00010683 | .0099900 | .08380 → .08278 | .14424 → .13736 | .61668 → .55126 |
| 23 | .00006237 → .00005070 | .0061835 | .03395 → .03627 | .05049 → .06697 | .21615 → .20582 |
| 47 | .00015006 → .00012227 | .0099900 | .04550 → .04633 | .04503 → .04446 | .36290 → .35850 |

Every immediate fixed-cue error decreased, but seed 23's held-out 48-step predictions
worsened and seed 47's steady error also increased. These regressions are preserved;
a locally helpful correction need not improve a recurrent trajectory. There are too
few examples, no changed-regime acquisition curves, and no learning-rule comparisons
to infer H2 or an adaptation/retention advantage. Gate 2 remains unopened.

The proposed update ranks were all one; the numerical ranks of the applied float32
matrix differences were 1, 4, and 1. The seed-23 difference reflects rounding at weight
addition under the standard numerical-rank tolerance. The API deliberately logs both
values rather than claiming exact rank-one applied arithmetic. All non-designated
parameters remained identical. All three rollbacks restored full state identities,
parameter tensors, and every development prediction metric exactly.

## Cost and artifact accounting

Internal proposal-stage elapsed times were approximately 1.45, 1.01, and 1.18 ms;
commit validation/preparation times .27–.32 ms and rollback times .16–.18 ms on this
machine. These are tiny engineering samples, not stable latency benchmarks. Timing
fields describe internal measured stages, not process startup or caller serialization.
All timing fields and timing-bearing receipt IDs are excluded from reproduction equality.

Each model copy stores 11,492 parameter bytes; an effective update tensor is 5,476
bytes. Snapshot/candidate/undo copies, evidence history, solve/rank workspace, and
Python objects are additional; these numbers are not peak RAM. Leading correction
arithmetic estimates and excluded operations are documented in the contract. Full
before/after/free/grounded/per-context metrics and audit records are in
[compact results](local-write-contract/results.json). The [artifact index](local-write-contract/artifact-index.json)
links them by hashes to full local results and names omitted long curve fields.

Full files remain locally under `runs/local-write-contract-v1/` and
`runs/local-write-contract-v1-repeat/`: per-seed before/after checkpoints, observed
feature/action evidence, audit JSON, configuration, provenance, and status. Checkpoint
file paths/hashes are recorded in results relative to the corresponding run root.
The report archive contains metadata and compact metrics, not those binary checkpoints.

## Verification and next work

Baseline: 27 tests passed before changes. Current suite: **48 tests pass**, including
21 writer checks covering atomic rejection, no-write prediction, stale/tampered inputs,
exact rollback, frozen parameters/settings, encoder checks, norm/rank budgets, target
exclusion from cues, analytic local-solve behavior, and manifest/RNG integrity. Ruff,
ticket validation, and checkpoint/archive hash checks pass. The local worker's test
extraction contained incorrect interpretations; the relevant tests were checked
directly and primary-agent design/review was used.

Commands (writable cache environment overrides were used):

```sh
uv run pytest
uv run ruff check soam tests scripts
uv run python scripts/check_tickets.py
uv run python scripts/check_write_contract.py --output runs/local-write-contract-v1
uv run python scripts/check_write_contract.py --output runs/local-write-contract-v1-repeat
uv run python scripts/check_write_reproduction.py runs/local-write-contract-v1 runs/local-write-contract-v1-repeat --output reports/local-write-contract/reproducibility.json
```

The read-only reproduction checker was added after the demonstration runs; their
recorded implementation/source identity remains unchanged. Re-execution must choose
unused output paths. Source checkpoint hashes must match the Gate 1 manifest.

SOAM-003 is complete. **SOAM-004 is ready** to preregister observation/search budgets,
new-task/retention targets, and fresh confirmation streams, then compare no adaptation,
Hebbian/delta/local least-squares or RLS, and matched online-gradient references. The
current rule is one candidate, not a predetermined winner. No learned scopes,
consolidation, context inference, or planner was implemented in this work package.
