# Shared-population study — development phase

2026-11-06. SOAM-051 is **in progress**. All 42 prescribed development fits and
2,520 base evaluation cells completed without numerical failures or retries.
The frozen development screen **passes**; confirmation is permitted but has not
started. This is a partial phase of the 119-fit/27,820-cell study, not a completed
scientific comparison or a positive shared-population gate.

## Prespecified screen and selections

Selected GRU G32 has development free-8 NMSE 0.031548 (limit 0.15) and recall
NMSE 0.015432 (limit 0.03). No required reference reaches the 1e-6 error floor.
G32 is therefore the preselected primary reference, with all five required
references still mandatory in confirmation. Config index 1 is selected for every
neural family (learning rate 0.003); L12 selects index 0 (ridge lambda 0.0001).
Selection used mean development free-8 NMSE only, as frozen; recall did not choose
or rescue a configuration.

Results below are means and sample standard deviations across the three independent
fit roots 401, 409 and 419, each scored on 20 development episodes per role.
These are descriptive development statistics, not confirmation confidence intervals.
Config 0/1 means learning rate 0.001/0.003 for neural models and lambda 0.0001/0.01
for L12. Lower NMSE is better; the same fixed normalization variance applies to all.

| Family | Config | Free-8 NMSE, mean ± SD | Recall NMSE, mean ± SD | Selected |
| --- | ---: | ---: | ---: | --- |
| S32 | 0 | 0.087671 ± 0.024196 | 0.087678 ± 0.008768 | No |
| S32 | 1 | 0.069605 ± 0.019474 | 0.063337 ± 0.013631 | Yes |
| D25 | 0 | 0.108620 ± 0.016765 | 0.086075 ± 0.005181 | No |
| D25 | 1 | 0.089745 ± 0.018857 | 0.076476 ± 0.006890 | Yes |
| D16 | 0 | 0.113326 ± 0.014940 | 0.083242 ± 0.008261 | No |
| D16 | 1 | 0.078360 ± 0.017748 | 0.078076 ± 0.006430 | Yes |
| G28 | 0 | 0.158020 ± 0.012479 | 0.069406 ± 0.004038 | No |
| G28 | 1 | 0.036545 ± 0.002515 | 0.018497 ± 0.005317 | Yes |
| G32 | 0 | 0.146721 ± 0.020197 | 0.064063 ± 0.012958 | No |
| G32 | 1 | 0.031548 ± 0.009656 | 0.015432 ± 0.002712 | Yes |
| L12 | 0 | 0.075852 ± 0.019501 | 0.073676 ± 0.009670 | Yes |
| L12 | 1 | 0.196939 ± 0.032233 | 0.132349 ± 0.017212 | No |
| SYM32 | 0 | 0.177285 ± 0.008836 | 0.093241 ± 0.010155 | No |
| SYM32 | 1 | 0.174653 ± 0.033979 | 0.072618 ± 0.027369 | Yes |

Development favours the conventional GRUs. Selected S32's transition mean is below
0.10, but its recall mean 0.063337 exceeds the eventual confirmation target 0.02.
That does not trigger an unregistered candidate-specific stop or authorize tuning:
the prespecified development gate checks baseline competence and floor effects.
Its passage is permission to perform the reserved test, not evidence for useful
sharing. Confirmation must retain S32's selected configuration despite this concern.
No hypothesis outcome is assigned from these selected development results.

This first measured comparison is a potential blog/report topic after confirmation:
strong conventional baselines materially change how a plausible shared-dynamics
mechanism should be assessed. Any publication must clearly label these preliminary
results and avoid treating a development win or loss as held-out confirmation.

## Execution and coverage

The [committed procedure](../docs/E1_DEVELOPMENT_EXECUTION.md) enumerated seven
families × two configurations × three roots in advance. Each fit used the complete
100-recall/300-joint schedule, batch 16; ridge used its corresponding observed-data
schedule. No shorter fixture schedule was substituted. Each fit archived 700 input
batch references and 60 evaluation cells (pre-recall, final-recall, transition).
Transition cells include free32/grounded32 and their free8 prefix; recall is scored
at update ten. Data split train supplies fitting and development supplies scoring.
Confirmation data have not been generated or inspected.

Verification counted 29,400 per-fit batch references and 2,520 cell-array archives,
with 2,220 unique A1 input objects. Shared objects preserve identical data across
families/configurations rather than erasing any fit's exposure. Each fit uses 6,400
recall source records and 4,800 transition episodes / 38,400 executed transitions.
Across the three unique training roots these are 19,200 recall records and 14,400
transition episodes, reused across model/config fits. Normalization's 2,048 records
are separate, not additional fitting examples.

Remaining, explicitly unexecuted: 70 confirmation fits and seven seed-11 repeat fits;
4,620 later base cells and 20,680 diagnostic cells. Causal lesions, T32 confirmation
identity, action ablations, finite-horizon recovery, paired ten-root uncertainty,
confirmation guards and exact scientific repeat remain outstanding. The next stage
must preserve selections and cumulative budgets and verify its execution source.
No scientific superiority, compositionality, attraction or neuroscience claim is made.

## Resources and provenance

- Development phase CPU: 392.372820 seconds, below its 4,000-second ceiling.
- Total allocated CPU so far: 406.208421 seconds; wall: 407.710123 seconds, including
  current and historical calibration charges. Future phases inherit these costs.
- Sum of fitting CPU: 355.569260 seconds; maximum individual fit: 9.749874 seconds,
  below the 90-second fit ceiling. Per-fit orchestration rows additionally count scoring.
- Process peak RSS: 320,487,424 bytes, below 2 GiB.
- Run directory: 95,228,443 bytes on disk. Budget ledger: 97,048,731 bytes including
  prior calibration allocations and reserved metadata; whole-study ceiling is 8 GiB.

Prerequisite implementation commit: a0e4e3f. Scientific execution commit:
`e2bf0ca9b9a6d24ff2197dee76a00590a60b8d3d`.
Source SHA-256: `e0585121bcd98d1bf1b49e6d21858a20279cd97f17849a91e4d1291c25f652bb`.
All calibrated source files matched both HEAD and disk before fitting and remained
unchanged afterward. The unrelated Draw.io temporary files were neither staged nor
used as inputs. One CPU Torch thread and deterministic algorithms were enforced;
models use float32, simulator/metrics use float64. Python/Torch/NumPy versions and
all constituent hashes are in the archived provenance.

The study setup had 176 passing tests, including fixed-inventory, calibration-gate
and atomic-checkpoint tests. The numerical and archive implementation remained
unchanged; a fresh A1 calibration including the orchestration source passed all
original limits before fitting. Qwen extracted the bounded execution checklist;
the primary agent invoked deterministic trial code and audited the output. No worker
selected parameters, ran autonomous trials or changed a stopping rule.

Commands (with UV_CACHE_DIR=/tmp/soam-uv-cache):

```sh
uv run pytest
uv run python -m soam.shared.runner --archive-revision a1 --mode preflight --output runs/e1-development-calibration
uv run python -m soam.shared.study --calibration runs/e1-development-calibration --output runs/e1-development-v1-a1
```

These record completed execution; do not rerun scientific fits to improve scores.
Output directories reject overwrites and this entry point does not automatically
resume or start confirmation. The full local run contains every input, checkpoint,
optimizer tensor, trace, target and output array.
[Compact evidence checksums](shared-population-study/development/sha256.json) index
[fit and per-episode metrics](shared-population-study/development/fit-results.json),
[inventory](shared-population-study/development/inventory.json),
[screen decision](shared-population-study/development/development-screen.json),
[provenance](shared-population-study/development/provenance.json), and
[resource status](shared-population-study/development/status.json).
The [accepted calibration](shared-population-study/calibration/cost-ledger.json)
retains its complete shape-equivalent timing and storage projection.

## Confirmation execution readiness — 2026-11-07

**Ready for a later explicitly requested execution; confirmation remains unopened.**
This continuation completes and verifies orchestration only. It performs no new
scientific fits, assigns no confirmation outcome and leaves SOAM-051 in progress.
The [concrete procedure](../docs/E1_CONFIRMATION_EXECUTION.md) records the next command,
ordering, failure handling and review requirements.

The initial audit verified the existing 42 fits/2,520 cells, all 31,920 A1 input
references and 2,220 unique objects, per-cell/compact metric agreement, checkpoint
finiteness, fitting exposure and 400-step traces. Recomputed development selections
match exactly. Normalization restores 2,048 samples and variance 0.03096017249093924;
its hash and statistics agree. All 48,382 raw files remain unchanged (95,228,443 bytes).
Development source matches both its recorded commit and current scientific files.
See the [audit](shared-population-study/continuation/development-audit.json).
The frozen protocol, manifest, A1 addendum, equations, data generator, fitting,
evaluation, inference rules and earlier development entry point were not edited.

New [root orchestration](../soam/shared/execution.py) orders fitting, development-only
lesion freeze, confirmation cells and archived-input repetition. The
[continuation entry point](../soam/shared/continuation.py) checks source/dependencies,
seals the prior evidence, carries cumulative budgets and prevents receipt reuse.
[Summary wiring](../soam/shared/study_summary.py) feeds complete paired root metrics
to the existing inference rules and retains all controls and separate recovery
summaries. The remaining inventory is 70 confirmation fits, seven repeat fits and
25,300 cells. Confirmation data cannot be opened by `prepare` or fixture mode.

Baseline before edits: **176 passed in 6.53s**. Final `uv run pytest`: **190 passed
in 14.03s**. Targeted Ruff check/format and the 62-ticket/two-template validator pass.
The tests verify selection-before-observation ordering, all prescribed root/config
routing using stubs, archive-only replay with simulator calls prohibited, corruption
and missing-file rejection, grounded-output isolation, normalization restoration,
source additions, consumed receipts, numerical failure/no retry, phase/overhead
limits and complete 2,300-cell failure records under storage exhaustion.

Both continuation fixtures passed with isolated root 9001 streams, two episodes
per condition and one update per fitting stage at batch two. Each performed 14
fixture fits, 230 cells per execution and exact comparison of **1,576 numerical
arrays, 259 input references and 512 records**. The repeat created no new input
objects. These are engineering fixtures, not the required full seed-11 scientific
repeat. The final fixture used 8.373325 CPU / 8.491413 wall seconds and 307,249,152
bytes peak RSS. Earlier fixture evidence is retained and charged.

The complete fresh A1 calibration used ten measurements after one warm-up, zero
optimizer updates and no confirmation data. All checks pass, with the unchanged
119-fit/27,820-cell projection and 2× margin:

| Check | Projection including margin | Frozen ceiling |
| --- | ---: | ---: |
| Slowest fit CPU | 21.7414 s | 90 s |
| Development CPU | 964.15056 s | 4,000 s |
| Confirmation CPU | 2,827.564 s | 8,000 s |
| Repeat CPU | 282.7564 s | 1,200 s |
| Total CPU | 5,274.47096 s | 14,400 s |
| Total wall | 5,284.81089 s | 28,800 s |
| Peak RSS ×2 | 595,492,864 B | 2 GiB |
| Artifacts ×2 | 5,661,352,816 B (5.27 GiB) | 8 GiB |

The historical failed v1 projection and earlier passing A1 ledgers are unchanged.
The [new calibration](shared-population-study/continuation/calibration/cost-ledger.json)
and final fixture share source fingerprint
`b52329efaa0a4927337691e60a5b610ed08984b884aef8dd5b7b12801f2408c9`.
Reviewed source was then committed as `fe9925f796af0a835a509cbef3bded4be3783fa3`;
readiness verified every calibrated source hash against disk and HEAD. Calibration
provenance honestly records its earlier base commit plus then-uncommitted additions.
Runtime remains Python 3.12.13, Torch 2.14.1, NumPy 2.5.4, CPU/one thread,
deterministic algorithms, float32 models and float64 simulation/metrics.

The [cumulative receipt](shared-population-study/continuation/readiness/readiness.json)
retains the original 406.208421 CPU-second development allocation, which already
includes three preflights. It adds four preserved historical fixture attempts
(including the failed A1 replay), both continuation fixtures, this calibration and
measured readiness preparation. Carried allocation is **454.075947 CPU seconds,
460.089971 wall seconds and 129,092,588 artifact bytes**, with 320,487,424-byte
historical peak RSS. Component entries distinguish measured physical bytes from
conservative metadata reservations. Ordinary regression tests and code review are
engineering verification, separate from the measured run ledger. Preparation and
future execution audits are charged to overhead. The remaining projection, including
that prefix and the full overhead allowance, is 4,764.396347 CPU / 4,777.155039 wall
seconds and 5,790,445,404 bytes; all remain inside the original ceilings. Projections
do not guarantee actual completion, so runtime enforcement remains mandatory.

Qwen's extraction omitted the requested orchestration gaps. Its later bounded
review harness aborted after a path error and proposed an unnecessary search;
the primary agent rejected that action and completed review directly. No worker
ran or controlled trials. [Verification and checksums](shared-population-study/continuation/sha256.json)
include fixture/config/source records, audit, calibration, readiness and commands.
The unrelated Draw.io temporary files and prior development artifacts were preserved.

The evidence supports engineering readiness and preserves the development screen.
It does not resolve S32's preliminary recall weakness, comparative utility, causal
sharing, recovery, ten-root uncertainty or full scientific reproduction. Those
remain SOAM-051's next eligible action under the recorded procedure. SOAM-052/059
remain backlog. The development-only GRU advantage and T32 identifiability limitation
remain worth a joint methods blog post and report once paired with confirmation;
this is a publication flag, not a new scientific finding or authorization to publish.
