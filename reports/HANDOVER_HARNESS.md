# SOAM-034: bounded handover harness engineering report

Completed 2026-11-01. The [implementation guide and artifact schema](../docs/HANDOVER_HARNESS.md)
describe the delivered harness for [protocol v1](../docs/HANDOVER_PROTOCOL.md).
This is engineering verification using fixture data. No measured training,
development, or confirmation study was run, and no handover gate is passed.

## Delivered behavior

The isolated `soam.handover` package implements the five prescribed layouts:
explicit A2/A1 key/ring dynamics, tied separate-state G2 recurrence, and shared-state
GS24/GS9 controls. Observed packets, caller-owned transient state, persistent
parameters/buffers, runner-owned replay history, and evaluator truth are separate.
Free prediction accepts only a snapshot and future commands; it cannot consume
future cues/observations or update live state/weights.

All 62 episode cells are runnable, including cold, equal-history replay, source
transport, cue/priming/sensing interventions, full-cue oracle, and live perturbations.
Autonomous key/ring probes include restoring-term ablations. The output policy logs
commits separately from key capture, and every reset/copy/reconstruction is labeled.
The one-state A1 control cannot claim concurrent tracking or an independent source
readout. GS source readouts are distinguished from physically separate state banks.

Observed-data-only training losses and bounded component fitting are implemented
for SOAM-035. Selector checkpoints can be reused across G layouts while learned
pose parameters load without overwriting condition-specific fixed gains. Numeric
counts are checked: G2 3,699, GS24 7,059, GS9 3,819 trained parameters; A2/A1 have
zero trained parameters and explicitly counted supplied buffers. Supplied geometry,
templates, cues, gains, bindings, and controllers remain scaffolding.

## Verification and fixture coverage

Baseline before code edits: **48 tests passed in 14.68 s**. Final suite:
**86 tests passed in 14.37 s**, including 38 new handover cases. The tests cover
packet/target separation, action indexing, paired random streams, cue masks,
state isolation, no-write prediction, energy-gradient/ring invariants, three-frame
selection, unsupported-key authority, repeated switches, actual replay commits,
source preservation, observed-only losses, component gradient isolation, checkpoint
validation, artifact reproduction, protocol pinning, and failure records.

Four two-update optimizer unit tests use a mocked five-frame fixture batch to
check fitting dispatch and component isolation. A deliberately nonfinite-loss test
checks exposure reporting on failure. These create no measured checkpoints and
generate no training/development/confirmation episodes.

The final smoke run used `runs/handover-fixture-v3` and its exact repeat used
`runs/handover-fixture-v3-repeat`. The v3 suffix denotes an engineering run revision;
the scientific protocol remains v1 with unchanged stimuli, thresholds and matrix.

- **62/62 episode cells completed**, each with 192 observations and 191 transitions.
- **30 probe evaluations completed**: one case per target/corruption or ring
  perturbation/action group, including passive-leak and radial-restoring ablations.
- **One unique base episode index**, fixture seed 11; paired conditions plus oracle
  produce nine archived packet variants. Repeated exposure is not independent data.
- **Exact reproduction of 1,239 arrays across 72 NPZ files**, plus deterministic
  metrics, events, operation counts, and fixed-state fingerprints.
- First run: **9.052 s wall / 9.021 s CPU**, peak RSS **295,010,304 bytes**.
  Repeat: **8.582 s wall / 8.557 s CPU**, peak RSS **298,958,848 bytes**.
  These are whole engineering-run costs, not preregistered latency-benchmark results.

See [coverage and operation records](handover-harness/coverage.json),
[probe records](handover-harness/probes.json), [first status](handover-harness/status.json),
[repeat status](handover-harness/repeat-status.json), and
[reproducibility result](handover-harness/reproducibility.json).
The [artifact index](handover-harness/artifact-index.json) fingerprints the complete
local run; compact evidence is retained here while full trajectories/checkpoints
remain under the run directories.

The A2 history fixtures exercised three cold resets, three replay reconstructions
(298 prefix packets total), and three source copies per history cell. G2's unfitted
selector made no commitments in these smoke cells, so those runtime switches were
not exercised by its natural fixture trajectories. Separate controller unit tests
use an explicitly labeled cue-based test selector to exercise repeated G2 cold/replay
dispatch. Direct reconstruction tests verify exact-history equality for real A2/G2
pose dynamics. The test selector is never used in the smoke runner or scientific models.

## Provenance and actual commands

Base commit: `6ed54ae4fa28eea52b858bef2a9f916ec7c04b6a`; implementation was an explicitly
dirty working tree. Both runs recorded source fingerprint
`194e9b5478fcfada2e66dc6ded1b2f62f463b1a2eea110871ee8ad1a5f7738e0`.
Full file hashes, dirty status, resolved numerical settings and derived initialization
seeds are in [provenance](handover-harness/provenance.json) and
[repeat provenance](handover-harness/repeat-provenance.json).

Protocol SHA-256: `b0deaca9e98601bb7ba7252f677b1cae5416b5315f6778c8ecf9d6a51dbeb6c9`.
Manifest SHA-256: `79875fee3b53bb00c385d6572dfa309e7f359371b449c2266d59261076b79611`.
Runtime: Python 3.12.13, PyTorch 2.14.1, NumPy 2.5.4, macOS 26.6.2 arm64, CPU,
float32 model state, float64 diagnostics, one Torch thread, deterministic algorithms.

Commands used (the cache override avoids the sandbox's default-cache restrictions):

```sh
UV_CACHE_DIR=/tmp/soam-uv-cache uv run pytest
UV_CACHE_DIR=/tmp/soam-uv-cache uv sync --extra dev --locked
UV_CACHE_DIR=/tmp/soam-uv-cache uv run ruff check soam tests scripts
UV_CACHE_DIR=/tmp/soam-uv-cache uv run soam-handover-smoke --output runs/handover-fixture-v3
UV_CACHE_DIR=/tmp/soam-uv-cache uv run soam-handover-smoke --output runs/handover-fixture-v3-repeat --repeat-from runs/handover-fixture-v3
UV_CACHE_DIR=/tmp/soam-uv-cache uv run python scripts/check_tickets.py
git diff --check
```

Earlier same-fixture runs `handover-fixture-v1` and `handover-fixture-v2` are retained
locally. Review subsequently corrected A1 role labeling, completed cost/timing and
artifact metadata, and strengthened fitter failure/exposure records. No threshold,
cue strength, scientific sample size, or mechanism parameter was tuned from them.

## Limitations and issues encountered

- All GRU smoke checkpoints are unfitted. Their failures cannot support an analytic
  candidate's superiority. No empirical effect size, five-seed screen, or learned
  attractor/composition claim is made here.
- Initial acquisition and history-control scheduling are made explicit in the
  implementation guide. Replay checks the reconstructed norm; cold uses the declared
  dormant-norm exception. These controllers remain supplied mechanisms.
- Linear MAC counts exclude nonlinear/vector operations and Python overhead;
  backward estimates are labeled approximations. Fixed tensor storage excludes
  Python configuration objects, whose constants are archived in the manifest and
  whose overhead is included in process RSS. Nested timers must not be summed.
- Repeats restore main episode packets/checkpoints. Isolated fixture probe inputs
  are regenerated from their dedicated streams and compared exactly. SOAM-035 must
  archive/reuse confirmation probe inputs as required by its full repeat contract.
- A bounded Qwen read-only review timed out after 90 seconds with no findings or
  pending actions. Primary review and invariant tests supplied the fallback; no
  worker patch or unreviewed action was applied.
- Adding the CLI triggered an editable-package rebuild; restricted DNS initially
  prevented fetching Hatchling. The authorized locked dependency sync succeeded,
  and the installed CLI was then verified. The lockfile was unchanged.

SOAM-034 is complete. SOAM-035 is ready to execute the measured study, including
whole-study orchestration, trained checkpoints, development/confirmation streams,
seed-level aggregation, the latency schedule, and confirmation reproduction.
SOAM-036 remains backlog. Historical v0.1 code/configuration/results and the v1
handover protocol remain unchanged; SOAM-045's exploration was not implemented.
