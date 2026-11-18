---
schema_version: 2
id: "SOAM-088"
title: "Execute the frozen D-R1 acquisition and settling study"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-086", "SOAM-087"]
labels: ["type:experiment", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-18"
updated: "2026-11-18"
github_issue: null
decision: null
---

# SOAM-088: Execute the frozen D-R1 acquisition and settling study

## Recommended thinking

**high** — Preserve the finite protocol, paired observations, no-write state boundary,
independent-root inference and distinct competence/resource/scientific stop outcomes.

## Problem / hypothesis

Does PH768 acquire and retain useful associations after reset, and does additional
nonlinear settling improve partial-cue recall beyond one cycle on identical weights?
Compare the complete system with mandatory conventional and encoding-matched controls.

## Scope

Execute the [accepted v1 protocol](../docs/STUDY_D_R1_PROTOCOL.md) and
[manifest](../docs/protocols/study_d_r1_v1.json): two development roots, fixed selection,
independent familiarity calibration, ten conditional confirmation roots, one exact
repeat and report. The [fresh allocation](../docs/requests/study_d_r1_allocation_2026_11_18.json)
was explicitly accepted. All fixture use is charged to that same cumulative ceiling.

## Acceptance criteria

- [x] Enumerate and execute only the frozen inventory, stopping if competence or resources fail.
- [x] Preserve inputs, source/config/software provenance, all results/failures, no-write/core
  fingerprints and complete persistent/active/temporary storage/exposure/time accounting.
- [x] On a passed competence screen, freeze selections/calibration before confirmation and
  complete mandatory paired comparisons, uncertainty and precision rules without extensions.
- [x] Verify exact prescribed repeat and independent reduction, or document why a preconfirmation
  stop makes them inapplicable; never call incomplete confirmation a scientific falsification.
- [x] Produce a source-grounded report and evidence for a separate scoped decision; preserve
  historical gates and recommend at most one follow-up without executing it.

## Metrics / evidence

Primary: PH-FULL minus PH-1 final earlier-object partial-cue raw accuracy, .05
practical margin and .10 adjusted interval-width limit. The protocol separately owns
acquisition/retention, acceptance/coverage guards and all REG/KV/REG-LIFT contrasts.
Bounded development may stop the study before confirmation; a negative/inconclusive
or resource-stopped result can complete this ticket with explicit limitations.

## Dependencies

- [SOAM-086](SOAM-086-recurrent-retrieval-protocol.md) — done/proceed for the v1 contract.
- [SOAM-087](SOAM-087-recurrent-retrieval-harness.md) — done with verified invariants and passing fixture.

## Branch conditions

The November 18 owner instruction and explicit allocation acceptance select D-R1
only. SOAM-052 stop and all historical D/A/B/B2/C results remain unchanged. No D3/D4,
E0/F, coupling, replay, learned role allocation or capacity sweep is activated.

## Completion record

Completed November 18. All 16 core fits, 114 writer trials and 130 derived arm outputs
completed without exclusions, failed attempts, replacement roots or budget extension.
Both development roots passed competence; selections and independent calibration
were frozen before ten confirmation roots. The [report](../reports/STUDY_D_R1.md)
records a small positive settling effect, +.02143 [.00982, .03661], that is precisely
below the .05 practical margin. Earlier-object accuracy, retention and accepted-wrong
guards fail. The reliable-retrieval conjunction is false; this is a valid scoped
negative result, not invalid execution or a general memory impossibility claim.

Actual commands: `uv run python -m soam.retrieval.runner` with each phase in order:
fixture, development, calibration, freeze, confirmation, repeat, report. Reporting-only
commands: `uv run python scripts/summarize_study_d_r1.py` and
`uv run python scripts/review_study_d_r1_artifacts.py`. They audit input parity,
cost/perturbation diagnostics, plots and available saved projector checkpoints;
they introduce no new fits, writes, observations or retrieval trials. The post hoc
checkpoint diagnostic is explicitly separate from confirmatory endpoints.

Frozen source `a84736dbbd3fcdf51bd59b868e2ac5557b17d451`, aggregate fingerprint
`347e5eb9cb539374ea069de2d485f33fdb2070b06a9fbb2c670f207ffe034011`, manifest SHA-256
`7376ceb643b50820d9b2d15fa4243aaa657b03cf183dba05d1949c756f60c8bb`.
Fixture 40011; development 41001/41013; confirmation
42003/42009/42027/42029/42051/42057/42059/42063/42069/42077; repeat 42003.
Selected core ridge 1e-6, REG/REG-LIFT .01, FAST 1.0; PH768 fixed.
CPU float64, deterministic, one intra-op/inter-op thread. Source/software, data
exposure, every arm's storage, timing, seeds and settings are archived in the report.

Checks: full `uv run pytest` passed 318 tests in 17.70 s; focused retrieval tests
passed 15 in 1.06 s. Frozen code has not changed since. `uv run ruff check soam tests scripts`
passed. All 5,497 prescribed repeated arrays match exactly; 2,100 endpoints were
independently reconstructed; 16 phase/root input groups and 7,040 paired masks match;
110 frozen source files and 102 historical D source files verified. Raw artifacts
remain under ignored `runs/study-d-r1-v1/`, with compact results/hashes in
[study-d-r1](../reports/study-d-r1/verification.json).

Through the nine numerical/reporting phases, use was 650.685 CPU / 651.444 wall
seconds, 428,195,840 B RSS and 572,202,962 artifact bytes before the receipt;
[ledger](../reports/study-d-r1/resource-final.json). Final archive closeout is
separately charged by `uv run python scripts/close_study_d_r1.py` and recorded in
[closeout](../reports/study-d-r1/closeout.json). All use remains below the accepted 7200/14400 s
and 2 GiB limits. No confirmation tuning or reused confirmation-as-unseen data.

The separate [SOAM-089 review](SOAM-089-recurrent-retrieval-decision.md) interprets
the result. No later branch is activated. The owner was notified that the isolated
acquisition versus reliable retrieval distinction merits a joint blog/report;
no publication or remote issue action occurred.
