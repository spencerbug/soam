---
schema_version: 2
id: "SOAM-084"
title: "Measure post-reset acquisition and sequential retention"
type: "experiment"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-082", "SOAM-083"]
labels: ["type:experiment", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-17"
updated: "2026-11-17"
github_issue: null
decision: null
---

# SOAM-084: Measure post-reset acquisition and sequential retention

## Recommended thinking

**high** — Separate persistent acquisition from transient recall, evaluate strong simpler controls, and preserve information/resource parity.

## Problem / hypothesis

Does bounded grounded experience yield post-reset object knowledge and retention, and does one rank-one fast operator improve on explicit memory and online regression?

## Scope

Follow the [owner selection](../docs/requests/study_d_2026_11_17.md) and [D v1 protocol](../docs/STUDY_D_PROTOCOL.md). D0–D2 only; D3/D4, learned write gates, replay and integration are deferred.

## Acceptance criteria

- [x] Complete this bounded phase with evidence or documented negative/inconclusive/invalid outcome.
- [x] Verify reset, no-write inference, evidence parity, source identity and resource limits.
- [x] Preserve every mandatory comparator, independent-root uncertainty and historical outcome.
- [x] Record actual checks, artifacts and implications for the next ticket.

## Metrics / evidence

Post-reset canonical/free prediction, one/few-shot curves, sequential retention, unknown rejection, resource costs and exact repeat. The versioned protocol/manifest owns frozen criteria.

## Dependencies

- [SOAM-082](SOAM-082-study-d-protocol.md) — completed prerequisite; decision requires proceed.
- [SOAM-083](SOAM-083-study-d-harness.md) — completed prerequisite; decision requires proceed.

## Branch conditions

The November 17 owner request selects this fresh fork; the superseded SOAM-059 selection is not reused. SOAM-082 must accept the protocol before implementation; SOAM-083 must verify invariants and fixture feasibility before development/confirmation. SOAM-052 stays stop. No downstream integration or D3/D4 branch is activated by completion.

## Completion record

Completed the [report](../reports/STUDY_D.md) and paired artifacts under the unchanged
[D v1 protocol](../docs/STUDY_D_PROTOCOL.md). All 16 offline fits / 88 model evaluations
completed: one fixture fit, four development fits, ten confirmation fits and one
repeat. No failed fit, excluded root, extra setting or budget extension. KV passes
the full persistent-acquisition/retention conjunction. REG and FAST learn isolated
objects but fail the .02 retention bound; FAST's practical-advantage comparisons
are precise negatives. Negative results are retained.

Actual commands: `UV_CACHE_DIR=/private/tmp/soam-uv-cache uv run pytest` (303 passed
in 26.83s before numerical work), `uv run ruff check soam tests scripts`, ticket
validator, and `uv run python -m soam.acquisition.runner` with fixture, development,
freeze, confirmation, repeat, report in order (writable UV cache and MPLCONFIGDIR
under /private/tmp). `uv run python scripts/verify_study_d.py` completed the archive
audit without new fits/streams. Plots visually inspected.

Scientific source commit `2270743`, aggregate
`e3b352a3cc4257203baced7a5be720b0884309efa9f31680cd5b50b0146241d2`;
receipt `99a16a77f86e2f2626dc873fe300e7fe5b9d727ea709f3a09418cdf3720a7277`.
Confirmation roots 32003,32009,32027,32029,32051,32057,32059,32063,32069,32077;
root 32003 repeats all 64 saved numerical arrays exactly, plus inputs/core/memory
fingerprints. Independent reconstruction verifies 280 endpoint values to 2.22e-16.
The archive audit checks 40 input/checkpoint records, 102 frozen files, and 1135
indexed artifacts; all 95 historical C files are unchanged. Separate post-freeze
audit source hash and environment are recorded in the artifacts.

[Final resources](../reports/study-d/resource-final.json): 51.13 CPU seconds, 61.60
execution-wall seconds, 344047616 bytes peak RSS and about 165 MB artifacts, inside
7200/14400 seconds and 2 GiB caps. Engineering/test overhead is separate. Full
checkpoints, inputs, predictions, scores and statuses remain in `runs/study-d-v1/`;
[compact records](../reports/study-d/tables.md) and [development](../reports/STUDY_D_DEVELOPMENT.md)
are preserved. SOAM-085 may interpret this evidence; no other study is activated.
