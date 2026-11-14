# Prompt 0 — repository preflight and one retained fork

2026-11-10. **Proceed to the already-selected SOAM-039 protocol design only.**
This preflight confirms [SOAM-059](RESEARCH_FORK_SELECTION.md), not a second routing
decision or an approved E2 protocol. No scientific fit, new dataset, implementation,
ticket activation, shared-utility edit, or frozen-artifact modification occurred.

## Checkout, names, and baseline checks

Checkout: `/Users/spencerneilan/workspace/soam`, branch
`codex/soam-v0.2-attractor-dynamics`, commit
`aca071ff884696955d96172d3f6251cf4f5ae11c`. The branch name is historical, not the
current research scope. Initially no tracked changes; pre-existing untracked items
were two `docs/.$attractor cortical controller model.drawio.*` backup files and
`docs/chatgpt_convos/`. They were left untouched and are not scientific authority.
This checks the local evidence, not whether a remote publication has identical bytes.

Temporary descriptive name: **post-E1 retained-acquisition follow-up**. Registry
reconciliation permits calling this **E2 minimal grounded acquisition, SOAM-039**:
the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md),
[hypothesis ledger](../docs/HYPOTHESES.md), [routing record](../docs/RESEARCH_PATHS.md),
tickets, and versioned manifests collectively define names. There is no separate
central experiment registry file. E1 means the shared-recurrence benefit pilot;
E2 already means acquisition; E3 already means active disambiguation. Historical
`experiments/exp01_associative`, `exp02_scope`, and `exp03_consolidation` are deferred
directories, not aliases for E1/E2/E3. Existing machine protocol IDs are
`soam-e1-shared` v1 and the separate handover manifest; no E2 manifest exists yet.

SOAM-047 and SOAM-059 are done/proceed; SOAM-039 is P0/ready with named selection.
SOAM-052 remains done/stop. SOAM-044/040/041 remain backlog; E3/attention have no
selection, and shared concurrency lacks a positive sharing gate. Historical
P2-ready SOAM-004/019/030/035 are not selected. Older reports/execution documents
say SOAM-052/059 are unstarted: those dated status snapshots are superseded by the
current queue and completed decisions, not by rewriting their empirical results.
The E1 manifest's `frozen_protocol_no_trials` is its pre-execution snapshot; the
execution inventory/status records establish completion. No numerical contradiction found.

Checks, in order (working directory as above):

```sh
uv run pytest tests/test_shared_inference.py tests/test_shared_data_fitting.py tests/test_shared_models.py
uv run python scripts/check_tickets.py
UV_CACHE_DIR=/private/tmp/soam-prompt0-uv-cache uv run --offline pytest tests/test_shared_inference.py tests/test_shared_data_fitting.py tests/test_shared_models.py
UV_CACHE_DIR=/private/tmp/soam-prompt0-uv-cache uv run --offline python scripts/check_tickets.py
UV_CACHE_DIR=/private/tmp/soam-prompt0-uv-cache uv run --offline pytest
UV_CACHE_DIR=/private/tmp/soam-prompt0-uv-cache uv run --offline python reports/preflight-2026-11-10/verify.py
```

First two commands failed before checking anything because the sandbox denied uv's
default cache. The offline temporary-cache runs passed: **50 tests in 3.06s**,
**62 tickets and two templates valid**, then **190 tests in 31.75s**. The read-only
archive check passed in 71.604 CPU / 90.519 wall seconds, peak RSS 626,704,384 bytes.
It verifies every recorded source hash against disk and the execution commit,
compact checksums, both complete raw-archive digests, and saved original/repeat
outputs. It does not refit the baseline. Full fresh-refit reproducibility was
established historically, not rerun here. The engineering review is outside the
closed E1 trial allocation and does not renew it.

[Verification receipt](preflight-2026-11-10/verification.json) records exact hashes,
config, stream derivation, and environment: macOS 26.6.2 arm64, Python 3.12.13,
NumPy 2.5.4, Torch 2.14.1, CPU, one Torch thread, deterministic algorithms.
The dependency lock matches execution. Qwen was asked for bounded guidance
extraction after path selection; extraction and status calls returned no usable
result before their waits were terminated. Direct guidance review supplied the
fallback; no worker finding, patch, or trial was accepted.

## 1. What E1 established and what is frozen

The [study](SHARED_POPULATION_STUDY.md) and [gate](SHARED_POPULATION_GATE.md)
establish a complete, narrow negative result: S32 recall NMSE **0.077657** exceeds
the frozen **0.02** maximum; both relative retention guards pass. Its free-8 NMSE
is **0.086825**, versus **0.037692 G32** and **0.046443 G28**. Both GRUs have lower
free-8 error in all ten roots. This is absolute recall failure, not demonstrated
destructive interference or a rejection of all shared recurrence.

| Frozen item | Verified contract/evidence |
| --- | --- |
| Source | Scientific freeze `fe9925f796af0a835a509cbef3bded4be3783fa3`; execution `7b3dea667cd65626af259a6ccbf0e17e0d8e96f6`; source SHA-256 `b52329efaa0a4927337691e60a5b610ed08984b884aef8dd5b7b12801f2408c9` still matches current checkout |
| Configuration | E1 v1 + archive A1; all neural models config 1, Adam 0.003, 100 recall + 300 joint updates, batch 16; L12 config 0, ridge 0.0001; G32 development-selected reference; final checkpoints, no test selection |
| Generator/splits | `soam-e1-shared` v1, fixed 12×2 projection seed 1729; train even initial sectors/action-bin parity, development/confirmation odd; distinct split/component RNG keys. Subsequent state support can overlap; not unseen compositions |
| Seeds | Development 401/409/419; confirmation 11/23/47/71/101/131/173/211/257/307; normalization train root 1801, 2,048 records; diagnostic selection root 401 in its own split; inference root 8675309; repeat root 11 adds no independent unit |
| Models | S32; mandatory D25, D16, G28, G32, L12; fitted SYM32; no-fit tied-weight/two-state T32 and all specified intervention/recovery controls |
| Metrics | Free-8 primary; recall, grounded-32/free-32, causal and recovery diagnostics; ten-root paired bootstrap, 10,000 draws; seven utility/guardrail and six causal contrasts with frozen multiplicity and precision rules |
| Checkpoints and data | 119 fits / 27,820 cells. Raw development: 48,382 files, 95,228,443 bytes; confirmation/repeat: 168,426 files, 538,869,653 bytes. Complete tree hashes match the gate, covering pre/final weights, optimizers, losses, input objects, selections, predictions and targets |
| Plots/reproduction | PNG/SVG primary-and-guardrails plots and rendering inputs match checksums. Saved repeat rechecked exactly: 11,764 arrays, 7,280 input references, 9,603 records; timing/container bytes excluded |

**All E1 holdout evidence is exposed and historical.** Reuse architecture/settings
as declared prior knowledge only; use fresh base fits and a new stream namespace
for any follow-up. Do not execute the consumed E1 receipt again.

## 2. What E1 did not establish

No isolated gating advantage, uniquely beneficial physical neuron overlap,
useful attractor recovery, persistent acquisition, learned organization,
compositionality, ambiguous multi-hypothesis tracking, navigation, or neuroscience
validation. All six causal contrasts miss frozen precision caps. S32 and T32 are
exactly equivalent on the tested sequential-role episodes. Hidden-distance
contraction occurs even with the S=0 control; recovery accuracy criteria fail.
Wide intervals are not equivalence. G32's greater capacity and different equations
prevent attributing its predictive advantage specifically to gates.

## 3. Descriptive claims and computational alternatives

Lower prediction error, contraction, lesion sensitivity in the supplied unit basis,
and overlapping activity are descriptive evidence at their measured scope. None
identifies semantic assemblies or an attractor mechanism by itself. Operationalize
the analogies relevant to these candidate forks as follows; none activates a trial:

| Analogy | Testable computational hypothesis | Competing explanation/control |
| --- | --- | --- |
| Shared neural assemblies | Same-unit recurrence adds useful cross-function performance | Tied parameters/separate state, active width and capacity; E1's T32 limit remains |
| Attractor/content completion | Perturbations recover useful target behavior after cue removal | Generic contraction or collapse; restoring-term ablation plus accuracy/variance guards |
| Gating/attention and predictive correction | Gating or correction improves held-out prediction at equal information/resources | Capacity, optimization, supplied role cues or extra observations; matched ablations required |
| Persistent competing beliefs | Multiple states reduce false commitment under irreducible aliasing | Replay/filter or extra state capacity; ambiguity and state-budget controls required |
| Fast synaptic acquisition | Few grounded writes generalize and survive transient-state reset | State calibration, point retrieval, or simple residual fitting; selected E2 controls |
| Sensorimotor/navigation maps | Action-conditioned memory improves realized goal efficiency | Supplied policy/map/geometry or ordinary prediction; closed-loop controls needed later |

## 4. Exactly one selected fork

Retain **E2: bounded recurrent-core acquisition versus a stable core with simpler
adaptive memory**. This has the highest decision value per implementation effort:
G32 is an existing predictive starting point, while the [historical writer](LOCAL_WRITE_CONTRACT.md)
already shows immediate improvement can accompany held-out rollout regression.
A single scalar change makes persistent generalization identifiable and could
change where future memory is stored. This is an ordinal research judgment.

Gating isolation remains worthwhile but would explain an offline ranking before
resolving acquisition risk. Sparse/unreliable correction and multiple hypotheses
need new sensing/aliasing controls; navigation adds policy and closed-loop confounds.
They are unselected. Literal object/sensor fast associations with **all slow weights
unchanged** are also unselected: existing E2 changes one recurrent block and does
not establish that stronger fast-memory/core separation claim. No substitute
architecture is silently introduced under SOAM-059.

## 5. Smallest distinguishing design

Use fresh G32 base fits at E1-selected settings; vary only one translation-action
gain with fixed sensing and disclosed transform-family prior. Equal observed
before/action/after pairs go to five conditions: bounded local-error writer,
no-write, RLS action residual on fixed G32, same-block one-step online gradient,
and at most 16-record retrieval with fixed-G32 fallback. Candidate writes only the
32×32 candidate-state block of `gru.weight_hh`; all other parameters stay fixed
during acquisition. The sound derivative/update rule still needs SOAM-039 review.

With nonzero affected command and other commands zero, the supplied family gives
`z_next - 0.98*z = a1*b_g`; observable coefficient estimation is possible without
passing simulator state, actual gain or projection inverse to learners. This is
not identification of an arbitrary unknown function from one example.

At 0/1/2/4/8/16 distinct transitions, reset transient state, preserve acquired
memory, and test new states/actions with writes disabled. Reset to the same base
checkpoint between adaptation episodes. Primary endpoint: normalized held-out
free-8 error area on the linear observation-count axis; protect recall and
unaffected-command transitions. Grounded one-step/free-32 and harmful-write rates
remain guardrails. These protected tasks do not test retention of contradictory
old/new gains under the same cue. Pair methods within independent roots and count
all readouts, stores, copies, updates, history reads and offline exposure.

## 6. Compute and storage budget

Carry SOAM-059's whole-branch ceilings: **3,600 CPU / 7,200 wall seconds**, one CPU
worker, **2 GiB peak RSS / 2 GiB cumulative artifacts**, failures included.
At most 16 base fits: 2 fixture/calibration, 3 development, 10 confirmation, 1 repeat;
reuse each fit across all five arms. At most two fixed configurations per adaptive
arm, 20 adaptation episodes/root, 16 distinct transitions/episode and 20 query
trajectories per budget/task slice, horizon at most 32. No architecture search.

E1's observed maximum fit cost ×16 is approximately **578 CPU seconds** for base
fitting only. This is a rough planning anchor, not an E2 runtime forecast. Full
adaptation/scoring/archive time and storage are uncalibrated; no precise expected
total is defensible yet. Whole-inventory projection with safety margin must fit
the ceiling before execution. Unused E1 resources cannot extend it.

## 7. Preregistration requirements and outcomes

**No E2 preregistration is frozen yet.** Do not mislabel these proposed outcome
rules as an approved protocol. SOAM-039 owns their exact adoption before fitting:

- **Supported benefit:** at least 20% smaller reset-held-out free-8 acquisition
  area than every mandatory adaptive reference, positive multiplicity-adjusted
  paired-root lower bounds, and a declared precision cap; protected-task increase
  upper bounds at most 0.005 NMSE. Absolute competence, one-step/free-32 and
  reset/no-write checks must also pass. Report no-write and every adaptive comparison.
- **Adequately precise negative:** an adjusted upper bound below the 20% practical
  margin with adequate precision against a required adaptive reference, or a
  precise protected-task breach, stops the tested retained-write advantage.
  A simple learner winning is an informative valid result, not a software failure.
- **Inconclusive:** intervals straddle the required benefit/guardrail boundaries,
  miss precision limits, or the valid finite inventory cannot resolve the question.
  No seed additions, retries, threshold changes or confirmation tuning.
- **Invalid/incomplete:** leakage, corrupted source/data, nonfinite/unauthorized
  writes, reset/rollback failure or budget exhaustion stops execution with failed
  and unexecuted rows retained; it is not scientific falsification.

One-shot is a separate claim: one distinct observation and one update, at least
20% improvement versus no-write plus positive advantage over adaptive controls
under frozen uncertainty rules. Immediate training-error reduction is insufficient.
Numerical precision caps, family construction, absolute competence thresholds,
gain range, masks, normalization, exact new roots and stream derivation are still
open protocol items. Their absence blocks implementation/trials, not this preflight.

## 8. Artifacts and stop boundary before the next prompt

Prompt 0 delivers this record, the [read-only verifier](preflight-2026-11-10/verify.py),
and its [verification receipt](preflight-2026-11-10/verification.json). E1 evidence,
code, utilities, ticket metadata and ordering remain unchanged. Baseline integrity
and archived reproducibility have no unresolved failure. Retain known E1 caveats:
the wrapper config hash differs from the separately verified resolved scientific
config hash; L12 generic exposure counters are not gradient steps; two historical
reporting failures lack separate RSS telemetry. Full end-to-end telemetry cannot
be retroactively certified.

The next authorized design stage is SOAM-039's existing planned
`docs/SHARED_POPULATION_LEARNING_PROTOCOL.md` and a versioned E2 manifest, containing
equations, competent-control rules, fresh streams, exact endpoints/uncertainty,
finite inventory, and proceed/revise/stop review. Later engineering must produce
invariant/rollback/replay evidence and a calibrated resource receipt/source freeze
before confirmation. None is falsely reported complete here. If a sound design
cannot fit the selected envelope, stop/revise instead of extending the programme.

Publication relevance remains the previously flagged E1 negative gate and the
decision to test simpler adaptive memories. This preflight adds integrity checks,
not a new scientific finding or permission to publish.
