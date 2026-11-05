# Recurrent platform fixture runner

[SOAM-048](../tickets/SOAM-048-platform-runner.md) implements the small
[platform contract](RECURRENT_PLATFORM_CONTRACT.md). This is engineering verification
with supplied weights. Scientific candidate fitting and E1 interventions remain
SOAM-050; measured comparisons remain SOAM-051.

## Run and reproduce

```sh
uv sync --extra dev --locked
uv run soam-platform-fixture --output runs/my-platform-fixture
uv run pytest tests/test_platform.py
```

The command runs the original eight-cell matrix, a deliberate invalid-output case,
and an exact repeat under one combined budget. Output directories must be new.
The repeat restores archived observations, evaluator targets and supplied weights;
it also verifies seeded initialization. It is not another independent sample.
Configuration: [platform-fixture.json](../configs/platform-fixture.json). Only
fixture split, seed 9001, supplied models, two registered tasks/backends, episode
indices 0/1, three transitions and one CPU thread are accepted. Fitting, online
writing, study splits, unknown capabilities, overwrite and partial resume are rejected.

The numerical reference is CPU float32 dynamics, float64 metrics and deterministic
operations. Thread/dtype/determinism settings are restored after success or failure.
Random streams are explicit local generators derived by the contract's SHA-256
scheme. The frozen platform contract is hash-pinned; historical scientific protocols
are neither imported into this runner nor changed by it.

## Responsibilities

| Module | Boundary |
| --- | --- |
| [core.py](../soam/platform/core.py) | Numeric observation/command types, fixed-buffer dynamics, state validation, private prediction snapshots, bounded clamp/perturbation capabilities, storage counts |
| [tasks.py](../soam/platform/tasks.py) | Rotation and translation simulation, fixed projection, separate observed packets and evaluator targets, task scoring |
| [evaluation.py](../soam/platform/evaluation.py) | Correct once, free prediction from a snapshot, grounded predict-then-correct sequence, metrics and work/resource ledger |
| [runner.py](../soam/platform/runner.py) | Factory selection, bounded matrix, archival/restoration, failures, exact repeat and provenance |

Rotation has 12 sensory features and three action coordinates; translation has
eight features and one action. Both use a fixed seed-1729 projection of 2D simulator
state. The supplied eight-unit backends receive no simulator, inverse geometry,
task label or target object. Their sensory and readout matrices are fixed random
buffers too. Correction is `0.5*h + 0.5*tanh(E@z)`. Leaky transition is
`0.5*h + 0.5*tanh(W@h + U@a + b)`; linear transition is `W@h + U@a + b`.
The linear fixture has a nonlinear correction adapter; it is not E1's bilinear L12
reference. Readout is `D@h`. These arbitrary supplied models have no accuracy gate.

`freeze(model,state)` detaches and copies all model buffers and activity. Prediction
uses another private model/state copy so even an exception cannot modify its source
snapshot or live state. Persistent fingerprints and input checks detect violations;
this trusted Python API is not a malicious-extension security sandbox. The caller
still controls declared observation provenance. No future observation/cue enters
`predict(snapshot,commands)`. Returned arrays do not alias live or snapshot state.

The two implemented prediction interventions are an initial state perturbation with
declared per-row RMS and a full-rollout unit clamp. Both preserve model parameters
and source state. Unsupported kinds fail explicitly. E1-specific timing, role masks,
rule variants and causal diagnostics are not silently approximated by these fixtures.

## Extending a fixture without changing orchestration

Register a Task factory with `features`, `actions`, `episode(split,seed,index)` and
`score(predictions,targets)`; register a backend factory taking `(ModelSpec,seed)`.
Keep the selected matrix at two tasks/two backends for this engineering command.
For example, the extension test adds a named translation adapter and a backend alias:

```python
from dataclasses import replace
from soam.platform.core import BACKENDS, SuppliedDynamics
from soam.platform.tasks import TASKS, TranslationTask

TASKS["alternate_translation"] = TranslationTask
BACKENDS["linear_alias"] = lambda spec, seed: SuppliedDynamics(
    replace(spec, kind="linear"), seed
)
```

The standard matrix itself exercises distinct transition equations and feature/action
dimensions without runner branches. The alias test separately verifies registration
plumbing. It does not constitute another sensorimotor study or authorize plugins,
arbitrary executable config strings or a general backend catalogue.

## Artifacts and resource meaning

The output root has status, reproduction and an immutable artifact index. Each of
`original/` and `repeat/` has configuration, manifest, provenance and a timing-free
deterministic record. Each cell stores `observations.npz`, separate `targets.npz`,
`checkpoint.npz`, `trajectories.npz`, record and timing JSON. Arrays load without
pickle. Expected-invalid data and its failure classification have a separate directory.
Unexpected cell failures retain identity, seeds and, when serialization completed,
the actual input/checkpoint archives. JSON never contains NaN; the explicitly
injected nonfinite fixture is preserved in its raw array.

Provenance reuses the existing capture utility and adds the pinned platform contract.
It records source/config hashes, dirty state, versions, architecture and numerical
settings. Exact reproduction checks source/environment, deterministic metrics and
all arrays; timings, PID, RSS and NPZ container bytes are excluded. All matching NaNs
are confined to the known injected-failure artifact. Artifact SHA-256 values validate
stored bytes separately from numerical equality.

Budget ceilings cover original plus repeat: 60 CPU seconds, 120 wall seconds,
1 GiB RSS and 256 MiB artifacts. Serialization reserves space before writing,
including 64 KiB for failure/status records. CPU/memory checks are cooperative at
bounded operation/cell boundaries, not OS-enforced interruption or crash durability.
Whole-process RSS includes Torch/interpreter overhead; measured run timing excludes
interpreter import/startup. Per-cell timers include evaluation and artifact writing.
Simulator/model construction and provenance overhead remain in whole-suite timing.

Records distinguish supplied buffers, fixed encoder, live state, snapshots, private
prediction model/state, observations, evaluator truth and outputs. Unique tensor
storage and logical bytes are separate; three model copies coexist during prediction.
Copy/call counts and leading dense MAC estimates do not claim complete hardware
FLOPs. Stack/hash/serialization temporaries and allocator overhead are reflected in
RSS; tensor inventories are not an exact simultaneous-workspace peak estimate.
This fixture runner uses batch one; counts refer to that bounded matrix.

Evidence and limitations: [engineering report](../reports/RECURRENT_PLATFORM.md).
