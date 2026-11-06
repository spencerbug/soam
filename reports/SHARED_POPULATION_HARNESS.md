# Shared-population harness — SOAM-050

2026-11-05. The engineering harness is delivered. **The v1 storage feasibility
projection failed**, so this delivery does not authorize scientific fitting.
[SOAM-061](../tickets/SOAM-061-e1-artifact-feasibility.md) is the next corrective
protocol decision; SOAM-051 remains backlog. No scientific E1 comparison,
confirmation exposure, architecture benefit or empirical gate is claimed.

## Delivered implementation

- [Models](../soam/shared/models.py): packed symmetric/skew rate weights, the seven
  frozen candidate families, and T32 with physically shared S32 parameters and
  independent role states. Correction and GRU/rate preactivations are checked for
  finiteness so bounded outputs cannot hide overflow.
- [Data](../soam/shared/data.py): fixed seed-1729 projection, float64 simulation using
  executed float32 commands, held-out phase/action cells, independent archived
  component streams, masked noisy initial observations, clean training records,
  and evaluator-only world states. The model never receives the simulator or P.
- [Fitting](../soam/shared/fitting.py): the frozen two-stage Adam and normalized
  float64 ridge mechanics, recall/final checkpoints, loss/exposure accounting,
  mandatory archive and budget hooks, and explicit per-fit stopping without retries.
  Full scientific schedules are implemented but were not executed.
- [Evaluation](../soam/shared/evaluation.py): isolated predictions, causal singleton
  selection on separate diagnostic streams, full/readout/random lesions, independent
  bank controls, shifted actions, zero-A/zero-S, missing cues and matched RMS-0.1
  perturbations that exclude the supplied role flags. The selection function requires
  an archive callback and budget checks for every cell.
- [Inference](../soam/shared/inference.py): two-config development selection,
  competence/floor screens, ten-root paired bootstrap with frozen adjusted and ordinary
  intervals, and outcome precedence. These rules were checked on synthetic values;
  they have not classified any scientific results.
- [Runner](../soam/shared/runner.py): bounded fixture and preflight modes, separate
  observed/clean/evaluator archives, source/protocol hashes, explicit failure records,
  no-overwrite output paths and replay from archived records. There is no scientific
  study CLI that bypasses the failed feasibility gate.

## Verification and fixture evidence

Baseline before the first backend changes: 110 tests passed in 14.55 seconds.
Baseline before this continuation: 144 passed in 14.67 seconds. Final full suite:
**171 passed in 16.24 seconds**. The 61 E1 tests cover numerical equations and signs,
packed gradients, counts, RNG isolation, split partitioning, projection consistency,
actual executed commands, clean-record ownership, target exclusion, loss timing,
checkpoint separation, exact fit repeats, no-write inference, lesion timing,
T32/disjoint isolation, preactivation failures, paired-root inference and budget stops.
Targeted Ruff check/format and ticket/link validation also pass.

The final fixture invocation used one CPU Torch thread, deterministic algorithms,
float32 models and float64 simulation/metrics. There were **181 cells per execution**,
plus an expected nonfinite-weight failure. The original and replay restored exactly
**1,560 arrays**, including inputs, checkpoints, optimizer tensors and trajectories.
Replay restores archived records rather than asking the simulator to recreate them.

Fourteen tiny fixture fit instances cover seven families twice. Each uses batch two,
one recall-only update and one joint update (ridge uses sufficient-statistic updates,
not Adam). This is an engineering check, not a shortened scientific pilot. Data use
isolated fixture/train and fixture/evaluation splits, root 9001; diagnostic selection
uses fixture/evaluation root 401. Normalization uses the prescribed 2,048 records
under train/root 1801/normalization components; these are not fitting examples.
There is no development-config search or confirmation data exposure.

The implementation assigns component keys as role/radius, role/phase, role/action,
role/mask and role/noise; normalization and lesion-selection use explicit distinct
prefixes. Initialization includes family/configuration, while task streams omit both.
All complete keys and derived seeds are archived. Action rounding is kept inside
its selected half-open bin with a one-ULP endpoint correction if float32 rounding
would cross the upper edge. Later observations are available only after prediction.

T32 intact outputs equal S32 exactly on both roles; an opposite-bank lesion leaves
that role unchanged. These are algebraic/implementation controls, not evidence that
shared neurons cause a prediction advantage. Two allocated banks do not establish an
unavoidable memory penalty compared with lazy allocation.

| Family | Trainable scalars | Allocated neural state + role flags | Active neural state |
| --- | ---: | ---: | ---: |
| S32 | 3868 | 32+2 | 32 |
| D25 | 3849 | 50+2 | 25 |
| D16 | 2040 | 32+2 | 16 |
| G28 | 3988 | 28+2 | 28 |
| G32 | 4940 | 32+2 | 32 |
| SYM32 | 1884 | 32+2 | 32 |
| L12 | 924 | 12+2 | 12 |
| T32 | 3868, aliased to S32 | 64+2 | 32 |

Readouts are included in parameter counts. Per-cell records include physical tensor
storage, returned arrays, state flags, copies and dense linear forward MAC estimates.
MACs explicitly exclude nonlinearities, matrix packing, backward, hashing and copies;
process CPU/wall/RSS measurements cover those costs. Expanded symmetric/skew matrices
are temporary workspace, not fictitious additional trainable parameters. Other
resident models and allocator workspace are covered by process peak RSS rather than
by the per-cell model-copy count.

Final original-plus-repeat fixture: 6.149916 CPU seconds, 6.187392 wall seconds,
304,955,392-byte peak RSS; 4,876,687 bytes on disk including final status metadata.
The status ledger's 4,876,562-byte count was sampled immediately before its final
status rewrite. Numerical equality excludes wall time, process metadata and ZIP
container bytes. Source was dirty and is explicitly recorded; no clean-source
scientific run is claimed.

## Negative preflight result

The [immutable captured ledger](shared-population-harness/preflight-cost-ledger.json)
measured ten operations after one warm-up per relevant shape, using unfitted models,
forward/backward checks and ridge solves with **zero optimizer updates**. It included
all 119 fits, 27,820 scoring cells, selection diagnostics, repeat, serialization,
normalization/aggregation overhead, explicit optimizer/bookkeeping allowances and a
2× projection margin. Calibration took 4.386504 CPU / 4.433091 wall seconds and
126,204 bytes on disk. Its ledger preserves the original failure and timing samples.

| Projected check, including margin | Value | Ceiling | Result |
| --- | ---: | ---: | --- |
| Slowest per-fit CPU | 22.106 s | 90 s | Pass |
| Development CPU | 974.640 s | 4,000 s | Pass |
| Confirmation CPU | 3,010.938 s | 8,000 s | Pass |
| Repeat CPU | 301.094 s | 1,200 s | Pass |
| Total CPU, including reserved overhead | 5,486.672 s | 14,400 s | Pass |
| Total wall | 5,489.961 s | 28,800 s | Pass |
| Peak RSS ×2 | 595,984,384 B | 2,147,483,648 B | Pass |
| Artifacts ×2 | **12,680,048,016 B (11.81 GiB)** | **8,589,934,592 B (8 GiB)** | **Fail** |

This is a conservative **projection**, not an observed 11.81 GiB archive. The current
formula archives paired training inputs per fit and charges a maximum-width transition
payload plus input allowance to every scoring cell. That may be unnecessarily costly;
it does not show that the experiment is intrinsically infeasible. Content-addressed
input reuse or a more precise, tested per-condition archive contract is a plausible
correction. SOAM-061 must justify and version it, preserve v1's failure, and run a
fresh complete calibration. No baselines, seeds or cells were dropped and no caps or
thresholds were changed to obtain a pass.

The calibration and final fixture have different source fingerprints because archive
replay and failure-path tests were completed after calibration. This does not upgrade
the failed ledger to a current passing gate. A corrected passing calibration must
cover the exact final source intended for scientific execution.

## Reproduction and provenance

Commands, each with UV_CACHE_DIR=/tmp/soam-uv-cache:

```sh
uv run pytest
uv run ruff check soam/shared tests/test_shared*.py
uv run ruff format --check soam/shared tests/test_shared*.py
uv run python scripts/check_tickets.py
uv run python -m soam.shared.runner --output runs/shared-harness-v1-final
uv run python -m soam.shared.runner --mode preflight --output runs/shared-preflight-v1
```

Use fresh output paths to reproduce engineering runs. The commands above record
completed work; they do not instruct restarting a failed gate or starting SOAM-051.
Full local artifacts remain under those runs/ directories. Compact committed evidence
is indexed by [SHA-256 manifest](shared-population-harness/sha256.json):
[fixture result](shared-population-harness/fixture-result.json),
[fixture provenance](shared-population-harness/fixture-provenance.json),
[preflight provenance](shared-population-harness/preflight-provenance.json),
[expected failure](shared-population-harness/expected-failure.json), and the cost ledger.

Source base: ec6035554458835cc5e92cc12d6662fac5ef9dbf plus disclosed uncommitted work.
Preflight aggregate source SHA-256:
ce02d0fd1155b6658a6c3f04ce1591bbf90e6a93bc0405982b94a493df57514d.
Final fixture aggregate source SHA-256:
dd3590b2cd354493074ef80f5a44fa739a10948042a78bddd22eaf71fe54e327.
The provenance files contain all constituent source hashes, Python 3.12.13,
PyTorch 2.14.1, NumPy 2.5.4, machine, numerical settings and resolved configuration.

Frozen protocol SHA-256:
98846328f3ad6803a7e85d910fc2be2f8075c5d44e75d19351ad311d9eae12bf.
Frozen manifest SHA-256:
beda95e9aba660c4b912339dfe26f331363e8de7cbc715af132e95fd1821d83e.
Fixed float32 projection bytes SHA-256:
c0ad772cb34d7a2ee8971c9108772f70478b79a818970759c9526ad64e05805c.
Historical handover and substrate implementations, frozen protocols and empirical
negative results are unchanged. Scientific outcomes and any later experimental fork
remain untested and unselected.
