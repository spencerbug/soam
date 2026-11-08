# E1 confirmation and reproduction procedure — SOAM-051

Revision 1, 2026-11-07. This completes execution support for scientific E1 v1 plus
[A1](E1_ARCHIVE_A1.md). It changes no scientific mechanism, stream, configuration,
comparison, endpoint, threshold, inventory or resource ceiling. Confirmation data
remain unopened. The [readiness evidence](../reports/SHARED_POPULATION_STUDY.md#confirmation-execution-readiness--2026-11-07)
is an engineering result, not a scientific gate.

## Reviewed starting state

SOAM-050 is done; SOAM-061 is done/proceed. SOAM-051 remains in progress. Its body
conditions are satisfied by the passing development competence/floor screen and
current complete A1 calibration. SOAM-052/059 remain backlog; no fork is selected.

Preserve `runs/e1-development-v1-a1` and its compact report unchanged. It contains
42 fits, 2,520 cells, 31,920 references, 2,220 verified objects and 48,382 files.
The reviewed archive digest is
`3780bbb310ee7bc7d9b9ebf70afe58d0b39e0565a7234c704ea361f288d7c4fd`.
The digest covers the sorted relative-file SHA-256 mapping. The original execution
commit is `e2bf0ca9b9a6d24ff2197dee76a00590a60b8d3d`. G32 remains the primary reference;
all neural families use config 1 and L12 uses config 0. All five references remain
mandatory. Do not repeat development or use its recall weaknesses to retune.

Reviewed continuation source is committed at
`fe9925f796af0a835a509cbef3bded4be3783fa3`, with aggregate source digest
`b52329efaa0a4927337691e60a5b610ed08984b884aef8dd5b7b12801f2408c9`.
Calibration and the final fixture have that exact digest. Preparation verified
every calibrated source file against both disk and HEAD, including added files,
and pinned the runtime versions, scientific protocol and A1 contract. Later
report-only commits may change HEAD without changing this source digest.

## Completed preparation

These commands have already run; they are provenance, not instructions to repeat
fits or discard earlier artifacts:

```sh
uv run pytest
uv run python -m soam.shared.continuation --mode fixture --output runs/e1-continuation-fixture-v1
uv run python -m soam.shared.continuation --mode fixture --output runs/e1-continuation-fixture-v2
uv run python -m soam.shared.runner --archive-revision a1 --mode preflight --output runs/e1-continuation-calibration-v1
uv run python -m soam.shared.continuation --mode prepare --calibration runs/e1-continuation-calibration-v1 --fixture runs/e1-continuation-fixture-v1 --fixture runs/e1-continuation-fixture-v2 --output runs/e1-confirmation-readiness-v1
```

The first fixture passed before final failure-accounting and normalization checks;
the second verifies the frozen source. Both remain charged. Preparation does not
fit models or generate confirmation observations. It verifies the sealed development
archive, selections, source, dependencies, full calibration and fixture, then records
the carried resources and remaining projections. Full archives remain in `runs/`;
[compact evidence and checksums](../reports/shared-population-study/continuation/sha256.json)
are tracked. Retain both: compact metadata cannot reproduce input trajectories.

## Next scientific execution — not run in this continuation

When SOAM-051 confirmation execution is requested, use the reviewed receipt once:

```sh
uv run python -m soam.shared.continuation --mode execute --readiness runs/e1-confirmation-readiness-v1 --output runs/e1-confirmation-v1-a1
```

The command refuses an existing output directory, stale source/calibration/runtime,
changed prior artifacts or a consumed receipt. It creates an exclusive
`execution-claim.json` in the readiness directory before scientific work. Never
remove that claim, rename a failed output to bypass it, or prepare another receipt
to retry science. There is no automatic resume. A setup or execution failure needs
an explicit recorded diagnosis under the frozen protocol; a source repair needs
review, fresh calibration and an accounted continuation, not a silent rescue fit.

1. Carry the development ledger once, including its three historical preflight
   allocations. Separately charge four retained historical engineering fixtures,
   both continuation fixtures, the new calibration and measured preparation overhead.
   Use one owner for all new input objects, outputs, temporary checkpoints and
   failure metadata. Physical storage, wall/CPU and RSS are distinct quantities.
2. Enumerate ten confirmation roots, in order 11, 23, 47, 71, 101, 131, 173, 211, 257,
   307. For each, fit S32, D25, D16, G28, G32, L12, SYM32 on its new **train** stream
   using the saved configuration. Each uses the unchanged full schedule: 100 recall
   plus 300 joint updates, batch 16, or the corresponding ridge procedure.
3. After all seven fits, run S32's 1,320 selection cells on the separate root-401
   development-diagnostic set. Persist targeted/random masks and selection evidence
   **before requesting any confirmation observation**, including intact base cells.
   Selection neither changes parameters nor chooses checkpoints/configurations.
4. Run all 420 base cells and the remaining 560 diagnostic cells for that root.
   Archive pre/final weights, optimizer tensors, losses/exposure, inputs, outputs,
   metrics, resources and failures. Reuse intact paths. Check T32 exact equivalence
   and D16/T32 opposite-bank isolation on free **and grounded** predictions.
5. After ten roots, refit the seven seed-11 models from archived training inputs,
   restore evaluation and selection inputs through verified A1 references, recompute
   selections, and compare all numerical arrays, traces, seeds, exposure, optimizer
   groups and metric records exactly. Timing and ZIP container bytes are excluded.
   No simulator regeneration or additional independent confirmation root is allowed.
   An incomplete original seed cannot be rescued by the repeat; its repeat is
   explicitly unexecuted and the incomplete evidence retained.
6. Aggregate episodes within each root and pass the ten paired root contrasts to
   the existing seven-contrast utility and six-contrast causal bootstrap/classifier.
   Publish every baseline, SYM32, random/disjoint controls, T32 equivalence, absolute
   errors and guardrail intervals. Recovery is a separate finite-horizon diagnostic;
   variance ratios are computed within root over episode endpoints, with ordinary
   root intervals. It does not establish a global attractor.
7. Enforce 90 CPU seconds per fit; confirmation 8,000, repeat 1,200 and cumulative
   overhead 1,200 CPU seconds; whole study 14,400 CPU / 28,800 wall seconds, 2 GiB RSS
   and 8 GiB artifacts. Check between bounded operations, preserve overshoot and stop
   subsequent work. The 2 MiB failure-metadata reservation is **inside** the artifact
   ceiling. A numerical failure keeps its failed/unavailable rows and does not retry;
   an implementation exception or exhausted budget stops later work with explicit
   unexecuted counts. Preserve every failed attempt.

At full completion, the preserved development plus this continuation totals exactly
119 fits and 27,820 cells. Audit `inventory.json`, per-root results, `reproduction.json`,
`result.json`, status/resource ledgers and provenance before interpreting evidence.
Finish SOAM-051's scientific report and acceptance criteria only from actual results.
Then SOAM-052 reviews the claim and SOAM-059 selects at most one subsequent fork;
neither is activated by this readiness assessment.
