# E1 archive A1 decision — SOAM-061

2026-11-06. **Proceed** with scientific protocol v1 plus the versioned
[A1 archive addendum](../docs/E1_ARCHIVE_A1.md). The replacement calibration passes
all ceilings; the [original failed v1 ledger](shared-population-harness/preflight-cost-ledger.json)
is unchanged. No scientific fits or confirmation data were used in this decision.

## Correction and rationale

The original formula charged 400 recall and 300 transition input batches for each
of 119 fits. Data streams deliberately omit family/configuration, so only 13 training
roots have distinct inputs: three development and ten confirmation. Repeat restores
seed 11's existing records. The old cell allowance also includes a 16-episode input
batch even though a cell scores one episode; A1 conservatively retains that allowance.
These were storage/accounting choices, not requirements for independent evidence.

[InputStore](../soam/shared/archive.py) stores each input batch once with a digest
covering tensor names, dtypes, shapes, values and stream keys. Fit/cell paths retain
explicit references and manifest hashes. Readers verify manifests, every file and
the reconstructed identity before replay. Corruption, incomplete objects, symlinks
and invalid reference digests stop execution without overwrite. A single run-owned
Budget counts physical writes; failed attempts remain preserved. Observation,
clean learning record and evaluator truth files remain separate.

The addendum was written and hash-pinned before the replacement calibration.
It changes archive ownership only: all 119 fit instances, 27,820 cells, roots,
hyperparameters, endpoints, thresholds, stream version and budgets remain intact.
Scientific measurements must still enforce runtime budgets; a projected pass is
not a promise that every model will finish successfully.

## Evidence

- Baseline: `uv run pytest`, 171 passed in 16.03 s before code edits.
- Final: `uv run pytest`, **173 passed in 16.71 s**. Targeted Ruff checks pass.
- New tests verify physical deduplication, exact input restoration, corruption and
  path rejection. Existing budget/failure tests remain passing.
- The A1 original/replay fixture covers **181 cells per execution**, compares
  **1,344 output/checkpoint arrays exactly**, and verifies nine shared input objects
  during replay. The smaller array count reflects removed duplicate input files;
  no model condition or data exposure was removed. Two expected nonfinite probes
  retain failure records.
- The first A1 fixture failed because one fit replay call still expected the old
  per-fit files. Its status/provenance are preserved. Correcting that call produced
  the passing replay; this engineering bug was not a scientific failure or a
  retry of a scientific fit.
- Calibration timed ten operations after one warm-up at all original shapes, with
  no optimizer updates. A1 archive timings use a fresh store each time, charging
  hashing and physical writes rather than timing only reuse.

## Full-inventory projection

All values include the original 2× margin. Artifact formula:

`2 * [13 * (400*51,385 + 300*45,698 + 700*4,096)
      + 119 * (checkpoint_allowance + 400*1,024 + 700*1,024)
      + 27,820*76,212 + 64 MiB]`.

Input estimates use uncompressed serialization sizes, independent of the compressibility
of unfitted weights. Per-object manifest overhead is 4,096 bytes; references are
bounded by 1,024 bytes. All checkpoint/optimizer/trace outputs remain per-fit.
The miscellaneous reserve covers normalization, aggregation metadata and the small
retained engineering failures; the 1,200 CPU-second overhead allocation also remains.

| Check | Projected value | Ceiling | Result |
| --- | ---: | ---: | --- |
| Artifacts | **5,661,352,816 B (5.27 GiB)** | 8 GiB | Pass |
| Slowest per-fit CPU | 23.102 s | 90 s | Pass |
| Development CPU | 986.552 s | 4,000 s | Pass |
| Confirmation CPU | 2,885.880 s | 8,000 s | Pass |
| Repeat CPU | 288.588 s | 1,200 s | Pass |
| Total CPU | 5,361.020 s | 14,400 s | Pass |
| Total wall | 5,375.480 s | 28,800 s | Pass |
| Peak RSS ×2 | 597,000,192 B | 2 GiB | Pass |

This is a new passing ledger, not a rewrite of the original 11.81 GiB failure.
The correction demonstrates efficient evidence storage, not useful shared recurrence.

## Reproduction and readiness

Commands use `UV_CACHE_DIR=/tmp/soam-uv-cache`:

```sh
uv run python -m soam.shared.runner --archive-revision a1 --output runs/shared-a1-fixture-fixed
uv run python -m soam.shared.runner --archive-revision a1 --mode preflight --output runs/shared-a1-preflight
uv run pytest
uv run python scripts/check_tickets.py
```

Full archives remain in those local directories; outputs refuse overwrite.
[Compact evidence and checksums](e1-archive-a1/sha256.json) include the
[full cost ledger](e1-archive-a1/preflight-cost-ledger.json), configurations,
source/config/software hashes, timings, statuses and the earlier fixture failure.
Both passing runs use exactly the same source fingerprint, as verified against the
current source. They disclose uncommitted work atop ec6035554458835cc5e92cc12d6662fac5ef9dbf,
CPU float32 models, float64 simulator/metrics, one Torch thread and deterministic
algorithms. Fixture roots 9001/401 and normalization root 1801 are unchanged.
Python/Torch/NumPy versions and constituent hashes are in each provenance file.

SOAM-051 is ready under **v1 + A1**, not under the failed standalone v1 archive
layout. Commit the reviewed implementation before scientific execution; verify its
source and addendum hashes, use A1 references for shared inputs, retain all planned
cells or explicit screen/budget stop rows, and enforce the original runtime ceilings.
No additional research fork or scientific execution was started by this decision.
