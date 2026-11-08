---
schema_version: 2
id: "SOAM-051"
title: "Measure the benefit and interference of shared recurrence"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01", "WP-08"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-050", "SOAM-061"]
labels: ["type:experiment", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-05"
updated: "2026-11-07"
github_issue: null
decision: null
---

# SOAM-051: Measure the benefit and interference of shared recurrence

## Recommended thinking

**xhigh** — Distinguish shared neuronal computation from state multiplexing, overpowered decoders, and resource-dependent performance.

## Problem / hypothesis

Test whether the frozen shared-population candidates retain useful feature, relation, and action information through cue-driven transitions without destructive mixing.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

**Readiness condition satisfied:** SOAM-061 proceeded with scientific E1 v1 plus
[archive addendum A1](../docs/E1_ARCHIVE_A1.md) and a
[passing complete calibration](../reports/e1-archive-a1/preflight-cost-ledger.json).
Use the verified shared-input object store and explicit references for scientific
execution. Preserve the failed original v1 archive ledger. Commit reviewed source
before fitting and verify source/addendum fingerprints against accepted calibration.

- Follow [E1 v1](../docs/SHARED_POPULATION_PROTOCOL.md) and its [manifest](../docs/protocols/shared_population_v1.json): 119 fit instances and 27,820 scoring cells including diagnostics/reproduction, subject to the pre-fit feasibility gate and development competence/floor screens. Publish T32 equivalence alongside primary comparisons; it is an identifiability limit, not a failed superiority test to hide.
- Run only the frozen minimal recall/transition pilot and finite tuning/confirmation budget.
- Evaluate the single primary benefit endpoint, feature-retention/interference guardrails, causal overlap, and action/symmetry ablations against separated and ordinary recurrent controls.
- Classify results using the prespecified outcome rules, keeping all seeds and budget mismatches. No online acquisition or concurrent handover extension in this ticket.

## Acceptance criteria

- [x] Publish the primary effect and uncertainty, guardrail outcomes, seed-level failures, all controls, and causal-overlap evidence.
- [x] Distinguish no meaningful advantage from inadequate precision, and directional failure from recall failure or numerical invalidity.
- [x] Archive complete source/config/seeds/software/numerical settings, exposure, scaffolds, timing/storage/compute, checkpoints and confirmation reproduction.
- [x] Preserve negative outcomes without adapting the experiment to them; send complete evidence to the sharing gate and fork-selection decision. No experimental fork is automatically launched.

## Metrics / evidence

Completed report: [SHARED_POPULATION_STUDY.md](../reports/SHARED_POPULATION_STUDY.md). Use only frozen protocol seeds, splits, thresholds, and budgets. Report fixed-point/cycle recovery separately from forced tracking and ordinary prediction.

## Dependencies

- [SOAM-050](SOAM-050-shared-population-candidates.md) — required completed prerequisite; decision prerequisites require proceed for this scope.
- [SOAM-061](SOAM-061-e1-artifact-feasibility.md) — corrective protocol/storage decision and passing calibration required before fitting.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R1/R2/R3) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Implement, measure, or review E1 against the frozen protocol and review defaults. Report performance utility separately from attraction and from biological/semantic claims. Require matched random/disjoint lesions and a competent GRU; no capacity or information advantage may be relabeled a sharing effect.

## Completion record

The earlier entries below are preserved phase-boundary history. The final scientific
completion record at the end supersedes their pending-execution status.

Started 2026-11-06 after verifying SOAM-050 done and SOAM-061 done/proceed.
Committed prerequisite implementation as `a0e4e3f`. The bounded
[development procedure](../docs/E1_DEVELOPMENT_EXECUTION.md) enumerates 42 fits and
2,520 cells, with confirmation inaccessible at this stage. Full suite: 176 passed
in 15.15s; the focused entry-point tests also passed after final budget/error handling
changes. A [fresh A1 calibration](../reports/shared-population-study/calibration/cost-ledger.json)
passes all ceilings for source fingerprint
`e0585121bcd98d1bf1b49e6d21858a20279cd97f17849a91e4d1291c25f652bb`.
Development phase completed from commit `e2bf0ca9b9a6d24ff2197dee76a00590a60b8d3d`:
42/42 fits and 2,520/2,520 base cells, no numerical failures or retries, 392.372820
phase CPU seconds. The fixed baseline-competence/floor screen passes. Selected G32
is the primary reference; neural config index 1 and L12 index 0 are frozen for
confirmation. See the [development report](../reports/SHARED_POPULATION_STUDY.md)
and [screen record](../reports/shared-population-study/development/development-screen.json).

The ticket remains in progress: 70 confirmation fits, seven repeat fits and all
confirmation diagnostics/uncertainty remain unexecuted. Candidate S32's preliminary
recall weakness is reported, not used to change settings or cancel planned controls.
No confirmation or useful-sharing gate has passed. Continue from the recorded
selections and cumulative resource allocation; do not refit development to improve scores.


### Execution-readiness continuation — 2026-11-07

Completed only the requested confirmation/reproduction orchestration scope; the
scientific acceptance criteria above remain open and status remains `in_progress`.
SOAM-050 done and SOAM-061 done/proceed were rechecked, along with the body condition
requiring A1, a passing calibration, preserved selections and committed source.
Recommended thinking remains **xhigh**: this continuation must protect source,
selection timing, resource allocation and interpretation across scientific phases.

- [x] Audited preserved development artifacts, compact metrics, 42 fits, 2,520 cells,
  31,920 references, 2,220 verified objects, normalization and source provenance.
- [x] Implemented only remaining execution/summary wiring; all pre-existing scientific
  modules, protocol/manifest/A1, configurations, streams and thresholds are unchanged.
- [x] Verified 230-cell continuation fixtures and exact archived-input repeat
  (1,576 arrays, 259 references, 512 records); tested frozen root/config routing,
  selection-before-confirmation, failure/no retry and cumulative budget stops.
- [x] Completed a full fresh A1 calibration, committed reviewed source, recorded a
  cumulative readiness receipt and [concrete execution procedure](../docs/E1_CONFIRMATION_EXECUTION.md).
- [x] Left scientific confirmation and reproduction unstarted; no downstream fork
  or empirical gate is activated.

Baseline `uv run pytest`: 176 passed in 6.53s before edits. Final suite: 190 passed
in 14.03s. Targeted Ruff check/format, `git diff --check` and
`uv run python scripts/check_tickets.py` pass (62 tickets, two GitHub templates).
The [report continuation](../reports/SHARED_POPULATION_STUDY.md#confirmation-execution-readiness--2026-11-07)
and [checksummed evidence](../reports/shared-population-study/continuation/sha256.json)
record exact commands, calibration, fixture/config/software/source and ledger data.
Reviewed source commit: `fe9925f796af0a835a509cbef3bded4be3783fa3`;
SHA-256: `b52329efaa0a4927337691e60a5b610ed08984b884aef8dd5b7b12801f2408c9`.
The new full projection passes all ceilings, including 5.27 GiB artifacts with 2×
margin. The carried allocation is 454.075947 CPU seconds and 129,092,588 artifact
bytes; earlier failed/complete engineering attempts remain preserved and charged.
No numerical equation or scientific budget was changed to achieve readiness.

Next eligible action is the 70 confirmation fits, seven archived-input repeat fits
and remaining 25,300 cells under that procedure, when execution is requested.
Development-only GRU advantage/S32 recall weakness and the T32 identifiability limit
remain publication-worthy context for a joint blog post and report after confirmation;
no publication is authorized or performed. Fixture success is not scientific evidence
for useful sharing, attraction or biological validation.

### Scientific execution complete — 2026-11-07

All acceptance items are satisfied by the [complete report](../reports/SHARED_POPULATION_STUDY.md)
and [checksummed confirmation evidence](../reports/shared-population-study/confirmation/sha256.json).
Status is `done`; `decision` remains null because this is an experiment, not SOAM-052's
gate review. Recommended thinking remains **xhigh** for the consequential distinctions
between absolute recall failure, passing relative retention guards and unresolved
causal precision. SOAM-050 done, SOAM-061 done/proceed and all ticket-body conditions
were checked before the once-only execution.

- `uv run pytest` before execution: **190 passed in 14.45s**.
- Executed `uv run python -m soam.shared.continuation --mode execute --readiness runs/e1-confirmation-readiness-v1 --output runs/e1-confirmation-v1-a1` once; exit 0.
- Completed 70/70 confirmation fits, 7/7 archived-input reproduction fits and
  25,300/25,300 new cells. Preserved 42 development fits/2,520 cells yield the exact
  frozen total **119 fits / 27,820 cells**. No scientific failures, exclusions,
  replacements, retries, retuning or allocation extensions.
- Frozen outcome: **`recall_interference_or_failure`**, specifically absolute recall
  failure (S32 0.077657 >0.02). Both relative recall guards pass; free-8 absolute
  threshold passes (0.086825 ≤0.10), but required comparative utility does not.
  Both GRUs have lower primary error; all six causal width criteria remain unresolved.
  Recovery is `diagnostic_criteria_not_met`. All required comparisons, ordinary and
  adjusted intervals, controls, failures and root-level results are reported.
- Scientific repeat is exact: **11,764 arrays, 7,280 input references, 9,603 records**.
  T32 intact identity and T32/D16 opposite-bank isolation each pass 440 episode-pair /
  660 prediction-array checks at exactly zero difference. No extra independent root.
- Read-only audit verified 7,440 A1 objects, 80,080 references, 129,404 finite arrays,
  stream derivation/separation, selection ordering, metric reductions and bootstrap
  bounds. Two incomplete reporting attempts are preserved and conservatively charged;
  the regrouped-mean tolerance correction affects only extraction, not scientific
  source, results, inference thresholds or exact reproduction.
- Development selections remain neural config 1 / L12 config 0, primary reference
  G32. Confirmation roots 11,23,47,71,101,131,173,211,257,307; repeat root 11.
  Reviewed source `fe9925f796af0a835a509cbef3bded4be3783fa3`, execution HEAD
  `7b3dea667cd65626af259a6ccbf0e17e0d8e96f6`, source digest
  `b52329efaa0a4927337691e60a5b610ed08984b884aef8dd5b7b12801f2408c9`.
  Software/numerics/config and exposure details, including the capture-wrapper hash
  distinction and L12 ridge accounting, are archived and explained in the report.
- Confirmation CPU 1,736.235285s, repeat 316.280692s; maximum fit 36.121810s <90s.
  [Final cumulative ledger](../reports/shared-population-study/confirmation/final-ledger.json)
  retains the original carry, reporting attempts and audit. Scientific runtime
  ceilings pass; reporting-attempt RSS telemetry limitations are disclosed.
- Final `uv run python scripts/check_tickets.py`, targeted source Ruff check/format,
  `git diff --check`, unchanged-source/calibration verification and preserved
  development/evidence checksums pass; exact outputs are in
  [verification.json](../reports/shared-population-study/confirmation/verification.json).

The consumed receipt and all scientific/engineering artifacts are retained. Nothing
was published or pushed. The confirmed baseline/retention/identifiability/recovery
findings merit a joint blog post and report after review; that flag is not publication
authorization. **Next eligible action: SOAM-052 evidence review**, unstarted. SOAM-059
remains a separate unstarted routing decision; no gate outcome or new experiment is
included in this completion.
