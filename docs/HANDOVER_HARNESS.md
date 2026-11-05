# SOAM-034 handover harness

This implements [protocol v1](HANDOVER_PROTOCOL.md) and its
[numerical manifest](protocols/handover_v1.json). It provides mechanisms, controls,
training primitives, scoring, fixture coverage, and reproducible artifacts. The
fixture CLI does not run SOAM-035's measured study or pass SOAM-036's gate.

## Running fixtures

From the repository root, choose unused output directories:

```sh
uv sync --extra dev --locked
uv run pytest
uv run soam-handover-smoke --output runs/my-handover-fixture
uv run soam-handover-smoke --output runs/my-handover-repeat --repeat-from runs/my-handover-fixture
```

The default [smoke config](../configs/handover-smoke.json) allows only fixture seed
11, one or two episode indices, one Torch thread, and all 62 prescribed cells.
Default coverage uses one paired base episode index across eight conditions and
one full-cue oracle variant. Thirty probe evaluations cover all target/corruption,
ring perturbation/action, and restoring-ablation groups using one initial case per
group. These are engineering fixtures, not the five-seed scientific sample.

GRU fixture checkpoints contain seeded, **unfitted** weights. Failing to commit or
predict well with these checkpoints is expected; no comparison against trained
controls is implied. The report records this limitation explicitly.

The runner refuses overwrites, non-fixture splits, extra fixture seeds, and excess
episode counts. It checks CPU and peak-RSS budgets between cells and after probes,
preserves partial artifacts on failure, and records the active cell. These are
cooperative checks rather than OS-enforced resource limits. Model updates reject
nonfinite state and state norms above the protocol limit.

Both protocol files are fingerprint-pinned by the implementation. An amendment must
be reviewed and versioned before changing those pins; editing thresholds in place
cannot silently change a run. The existing v1 files are preserved.

## Boundaries and mechanisms

| Module | Responsibility |
| --- | --- |
| `soam/handover/protocol.py` | Frozen manifest, independent stream derivation, templates, fingerprints |
| `soam/handover/data.py` | Paired synthetic streams, observed-only packets, evaluator truth, archive restoration |
| `soam/handover/models.py` | A2/A1 key/ring models, G2/GS24/GS9 GRUs, explicit state, selection, no-write prediction |
| `soam/handover/evaluation.py` | Runner-owned history controls, interventions, trajectories, evaluator-only scoring |
| `soam/handover/training.py` | Separate observed-data selector/pose losses, fixed-budget fits, learned-parameter checkpoint transfer |
| `soam/handover/probes.py` | Autonomous key/ring probes and restoring-term ablations |
| `soam/handover/runner.py` | Fixture-only CLI, provenance, resource limits, artifact writing, exact repeat checking |

The model receives only `ObservationPacket(z, valid, cue, cue_present,
executed_action_previous)`. It never receives an Episode, focus label, phase truth,
future mask, or future observation. Its `ModelState` holds key/pose activity,
previous retrieval weights, role counters, evidence age/localization, attended ID,
and an initialization flag. State belongs to the caller; modules own parameters and
fixed buffers. The flag distinguishes first-observation correction from later
past-action propagation; it does not encode a switching schedule.

`step(state, packet)` returns a fresh state, current feature estimates, and
diagnostics. `predict(snapshot, actions)` copies the state, propagates the supplied
commands with no future sensing or cues, and leaves the interaction and weights
unchanged. `diagnostic_inverse` is restricted to diagnostics; analytic pose
propagation uses the declared fixed forward operators.

| Variant | Trained parameter count | Recurrent floats | Pose organization |
| --- | --- | --- | --- |
| A2 | 0 | 40 | Two independent ring states, shared fixed operators |
| A1 | 0 | 28 | One ring state, explicitly missing separate source capacity |
| G2 | 3,699 | 40 | Two 12D states with tied GRU weights |
| GS24 | 7,059 | 40 | One 24D state with two feature readouts |
| GS9 | 3,819 | 25 | One 9D state with two feature readouts |

Previous weights, counters, age/localization, output tensors, snapshots, and history
are additional storage. Fixed buffers include templates, coupling, projection,
gains, and analytic operators where applicable. The artifact records their actual
sizes. Shared readouts do not imply physically independent state banks.

## Control scheduling details

- Before the first commitment, history controls warm the leading live candidate
  selected from previous key weights (A on an exact tie). This is initial
  acquisition, not a destination reset. After acquisition, only the attended bank
  updates online in cold/replay/transport modes.
- Cold switching checks cue persistence and available evidence history, uses the
  protocol's dormant-norm exception, resets the destination, and applies current
  correction once. The resulting poor output remains in continuity scoring.
- Replay checks cue/history eligibility, reconstructs the candidate from the actual
  observed prefix, then checks the reconstructed norm before commitment. Failed
  reconstruction attempts are logged and costed too. The current packet is not
  assimilated a second time. Reconstruction is not labeled continuous tracking.
- Transport rotates the current source using the supplied initial offset and
  accumulated executed commands, then applies current destination evidence once.
  Each deliberate copy is logged. No process-noise or true-phase correction is supplied.
- A1 never receives credit for concurrent tracking. Its two output references share
  one estimate; source scores are explicitly labeled with unavailable independent
  source readout capacity. GS models have two readouts but one shared pose state.
- The policy retains its previously committed identity when no eligible replacement
  exists. This does not certify fresh evidence or a valid new commitment; evidence
  age, abstention, raw estimates, and failure metrics remain visible.

These details resolve controller initialization/ordering without changing v1's
numerical stimuli, dynamics, thresholds, or trial matrix. The controller is supplied
scaffolding; key recruitment is measured before output eligibility checks.

## Artifact schema version 1

| Artifact | Contents |
| --- | --- |
| `config.json`, `manifest.json` | Resolved fixture settings and frozen scientific design |
| `provenance.json` | Commit, dirty state, per-file hashes, combined source fingerprint, protocol/manifest hashes, actual software/platform/dtype/thread settings, derived initialization seeds, exposure boundary |
| `packets/*.npz` | Observed `z[192,2,12]`, validity, cues/presence, executed actions; separately named evaluator phases/noiseless features, ideal task focus, and presented-cue training labels |
| `cells/cellNN-eN/checkpoint.pt` | Exact supplied/unfitted model state for that cell; safe tensor-only loading |
| `cells/cellNN-eN/trajectories.npz` | Estimates, key/pose state, retrieval/priming weights, roles, evidence ages/localization, updated-bank flags, one-step predictions, anchor 8/32-step predictions, analytic key energies |
| `cells/cellNN-eN/record.json` | Cell/packet identity, supplied/unfitted status, per-event metrics, control operations, exposure, state/parameter storage, operation counts, timings |
| `cells.json`, `deterministic.json` | Completed-cell inventory/timings and timing-free numerical records |
| `probes.json`, `probes.npz` | Probe definitions/endpoints, operation counts, trajectories and analytic energies |
| `artifact-index.json` | SHA-256 of immutable completed artifacts; status is excluded because it is finalized afterwards |
| `status.json` | Running/complete/failed status, active cell on failure, timestamps, CPU/wall time, peak RSS and engineering-only outcome |
| `reproduction.json` | Exact numerical comparison when `--repeat-from` is used |

Role codes are inactive=0, primed=1, tracking=2, attended=3. Attended ID -1 means
abstention; A/B/C IDs are 0/1/2. C cannot receive output authority. Empty GRU energy
arrays mean no Hopfield energy claim, not missing numerical values. An absent
handover delay is JSON null, with a separately recorded censored delay and failure.
Failed events and abstentions keep their raw-bank continuity errors in the report.

Leading linear MAC estimates exclude nonlinear/vector arithmetic and Python
overhead. Key/ring/GRU calls, corrections, resets, control copies, history packet
copies, transition-state clones, snapshot clones, and replay calls are counted.
Live and prediction work are separate. Key/pose/readout timings are nested within
core, selection, replay, and prediction timings; do not add overlapping timers.
Trajectory/history byte counts are logical storage; RSS includes allocator/Python
overhead and temporary allocations.

Repeat runs restore archived episode packets and per-cell checkpoints. Isolated
fixture probes regenerate their initial cases from the same separate streams.
All NPZ arrays and deterministic records must match exactly under the same source
fingerprint. Timestamps, PID, runtime/RSS, and ZIP container bytes are excluded from
numerical equality. No repeat is an independent statistical sample.

## Fitting and measured-study boundary

`observed_batch` drops evaluator truth. `selector_loss` uses only presented-cue
labels; `pose_loss` uses masked current and next observed features, with prediction
receiving only the action and missing observations. Component losses have no
cross-component gradients. `fit_component` implements the fixed optimizer/stream
schedule, timeout/RSS checks, progress/exposure callbacks, and partial-failure
checkpoint delivery. Its callback receives `(learned_tensors, progress, status)`.
Learned-parameter transfer leaves condition-specific fixed gains and interventions
untouched. No measured fit was executed for SOAM-034.

SOAM-035 must orchestrate one selector and three pose fits per seed, reuse the
selector across layouts, persist callbacks/checkpoints, enforce the whole-study
four-CPU-hour budget, and run the declared development/confirmation/repeat and
latency schedules. Seed-level aggregation/bootstrap and empirical interpretation
belong to that experiment and SOAM-036. The fixture CLI deliberately cannot be
used as a confirmation runner. SOAM-045's recurrent-attention exploration remains
a separate design backlog item.
