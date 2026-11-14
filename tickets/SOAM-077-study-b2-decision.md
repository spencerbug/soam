---
schema_version: 2
id: "SOAM-077"
title: "Review robust estimation and prepare the Study C baseline handoff"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-076"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-11"
updated: "2026-11-12"
github_issue: null
decision: "proceed"
---

# SOAM-077: Review robust estimation and prepare the Study C baseline handoff

## Recommended thinking

**xhigh** — Separate statistical identifiability, numerical validity and root-level evidence in a finite correction search.

## Problem / hypothesis

FILTER2 has strong ordinary prediction and a corruption failure; B2 tests the smallest robust corrector.

## Scope

Review robust estimation and prepare the Study C baseline handoff. Follow [B2 v1](../docs/STUDY_B2_PROTOCOL.md). Owner explicitly selects B2 after completed B; no other branch or Study C implementation.

## Acceptance criteria

- [x] Complete this phase with measured evidence or explicit negative/inconclusive findings.
- [x] Preserve A/B source, results and decisions; enforce no-write and causal scoring.
- [x] Record exact provenance, resource use, tests and all mandatory controls.

## Metrics / evidence

[B2 manifest](../docs/protocols/study_b2_v1.json) owns endpoints, finite allocation and fresh roots. Ordinary J, balanced corruption, genuine-change guards and real inference cost.

## Dependencies

- [SOAM-076](SOAM-076-study-b2-experiment.md) — completed evidence or proceed contract.

## Branch conditions

SOAM-074 is the fresh routing decision under the owner's explicit B2 assignment; SOAM-073 proceeds only for the interface. Historical SOAM-069 revise and SOAM-052 stop remain immutable. Protocol proceed precedes implementation; tests and fixture precede development; immutable receipt precedes confirmation. SOAM-077 completes before any fresh selection of C.

## Completion record

Decision: **proceed with the scoped conventional-reference recommendation only**.
Reviewed all frozen primary comparisons, guardrails, tails, uncertainty, costs and
identifiability limits in the [decision/C handoff](../reports/STUDY_B2_DECISION.md).
ADAPT1 is the recommended robust reference; NISEMP is the lean hard-gate control.
Both pass frozen benefit/guard criteria. Temporal/hybrid development failures remain;
Student-t and learned reliability were conditionally deferred. Coherent corruption
and measured latency prevent a general robustness/efficiency claim. No new fork or
Study C implementation is selected.

Evidence: [scientific report](../reports/STUDY_B2.md), [immutable receipt](../reports/study-b2/confirmation-receipt.json),
[integrity audit](../reports/study-b2/verification.json), [resources](../reports/study-b2/resource-final.json).
Ten fresh confirmation roots, eight models, 29 fitted executions including audit,
88 confirmation/repeat evaluations; exact repeated arrays/models and 1040 independent
reductions within 1.11e-16. Frozen source fingerprint
`28d72614c9f2d61b0e48cdd4d2ebc896cff1d37bb7324a2d5c735a29cb69e1cd`;
base commit `bdb3bdcbb47c7a2a24301e044ebaaac6b50a18cd`.
352.02 numerical CPU seconds, 352.63 execution-wall seconds, 775,749,632 peak RSS
bytes, 480,468,054 artifact bytes; all limits pass. Preserved storage-projection and
post-study checker failures are engineering records, not failed scientific fits.

Validation: `uv run pytest` 266 passed in 15.65s; targeted robust tests 28 passed;
`uv run ruff check soam tests scripts` passed; `uv run python scripts/check_tickets.py`
passed 78 tickets; `git diff --check` passed. Broader Ruff finds 16 pre-existing errors
in historical shared-population report scripts, preserved unchanged. Commands and
roots are in SOAM-076 and the receipt; `uv run python scripts/finalize_study_b2.py`
verifies final artifacts. The roadmap and README now include B2 before conditional C.
The owner was notified of the publication-worthy scoped benefit and limits; no remote
issues, blog publication, push or other branch was performed.
