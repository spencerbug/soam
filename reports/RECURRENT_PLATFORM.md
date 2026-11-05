# SOAM-048 recurrent platform engineering report

Completed 2026-11-05. The [fixture runner](../docs/RECURRENT_PLATFORM_RUNNER.md)
implements the [minimal contract](../docs/RECURRENT_PLATFORM_CONTRACT.md), with
separate tasks, supplied dynamics, isolated prediction and bounded artifacts.
This report verifies engineering invariants only. No E1 model was fitted, no
development/confirmation study ran and no scientific gate passed.

## Verification

- Baseline before code changes: **86 tests passed in 16.21 seconds**.
- Final full suite: **110 tests passed in 14.92 seconds**, including 24 platform cases.
- Targeted Ruff checks and format checks pass for the new package/tests.
- Two distinct tasks × two backend configurations × two episode indices: **8/8 cells**
  per pass, plus one deliberately invalid nonfinite-output case per pass.
- Original and repeat match **137 numerical arrays in 33 NPZ files**, as well as
  deterministic configuration/metric/resource records. The injected NaN artifact is
  explicitly compared as a known failure, not accepted as a valid prediction.
- Tests cover target/observation separation, action indexing, correction exactly once,
  snapshot/result isolation, persistent/input mutation detection, exception isolation,
  random streams, mask/shape/capability rejection, clamp/perturbation behavior,
  registry extension, archive tamper detection, budgets and overwrite rejection.

The original/repeat suite used root seed **9001**, fixture split, episode indices
0 and 1, projection seed **1729**, supplied width-eight buffers and three transitions.
Four unique task episodes provide 16 distinct observations and 12 transitions;
they are reused across backends and repeat. Sixteen model/episode executions are
not sixteen independent datasets. There were zero fitting updates and no trained
parameters. Bad fixture accuracy cannot establish or reject H1.

| Combined original + repeat cost | Measured | Ceiling |
| --- | ---: | ---: |
| CPU seconds | 0.532955 | 60 |
| Wall seconds | 0.639720 | 120 |
| Whole-process peak RSS bytes | 282,181,632 | 1,073,741,824 |
| Artifact bytes, including final status | 249,062 | 268,435,456 |

These are measured engineering-run costs, not E1 training forecasts or latency
benchmark results. Import/startup is outside the runtime clock; RSS includes process
overhead. Tensor/copy ledgers distinguish storage from estimates of arithmetic work.
Per model, rotation uses 288 supplied floats (1,152 bytes), translation 208 (832 bytes);
live recurrent state uses eight floats (32 bytes). The task encoders use 96/64 bytes
respectively. Source, snapshot and private prediction model copies coexist. Additional
state, observation, target, output and temporary storage is disclosed in the records.

## Reproducible artifacts

Executed:

```sh
UV_CACHE_DIR=/tmp/soam-uv-cache uv run pytest
UV_CACHE_DIR=/tmp/soam-uv-cache uv sync --extra dev --locked
UV_CACHE_DIR=/tmp/soam-uv-cache uv run ruff check soam/platform tests/test_platform.py
UV_CACHE_DIR=/tmp/soam-uv-cache uv run soam-platform-fixture --output runs/platform-fixture-v1
```

The pytest command was run before edits and after implementation. An intermediate
targeted run passed 21 cases; the final suite includes three added failure/accounting
checks. Installing the new entry point needed an editable-package refresh; a restricted
network attempt failed, then the authorized `uv sync` succeeded without changing the
lockfile. An early module invocation exposed an incorrect repository-root calculation,
fixed before the successful archived run. No failed invocation is counted as evidence.

Source commit: `ce29de0deb59a1804d4f9c883bb79029792c65cd`, with the new implementation
in a dirty working tree. Source fingerprint:
`d0ce56276aaa715aa217106cec320519660b154a4e5e1680d1076bdf44e213b9`.
CPU float32 models/float64 metrics, one Torch thread, deterministic algorithms;
Python 3.12.13, Torch 2.14.1, NumPy 2.5.4, macOS arm64.

Compact evidence:
[configuration](recurrent-platform/config.json), [manifest](recurrent-platform/manifest.json),
[original provenance](recurrent-platform/provenance.json),
[repeat provenance](recurrent-platform/repeat-provenance.json),
[deterministic metrics/work/storage/failure records](recurrent-platform/deterministic.json),
[suite status](recurrent-platform/status.json),
[reproduction](recurrent-platform/reproduction.json), and
[artifact index](recurrent-platform/artifact-index.json).
Full checkpoints, inputs, targets and traces remain in `runs/platform-fixture-v1/`;
the index paths are relative to that directory. An independent audit verified every
indexed artifact, every source-file fingerprint and the exact on-disk byte total.

## Limits and next work

The dynamics have supplied random weights; the linear fixture has nonlinear sensory
correction and is not the scientific L12 control. The tasks have no binding,
acquisition or fitted associative memory. Tests show controlled implementation
properties, not attraction, useful sharing or improved prediction. Only initial
state perturbation and full-rollout clamping are supported here; unsupported
interventions fail rather than silently approximate scientific controls.

The local Qwen worker was busy with another job, so bounded test drafting fell back
to direct implementation/review. No worker changes or approval actions were applied.
Historical source, frozen protocols and reports remain unchanged. SOAM-050 can now
implement the frozen scientific candidates and their feasibility checks; SOAM-051
still owns fitting and measured trials. No application fork was selected or launched.
