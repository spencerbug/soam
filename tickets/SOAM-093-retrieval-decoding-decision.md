---
schema_version: 2
id: "SOAM-093"
title: "Review the retrieval-versus-decoding diagnosis"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-092"]
labels: ["type:decision", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-19"
updated: "2026-11-19"
github_issue: null
decision: "proceed"
---

# SOAM-093: Review the retrieval-versus-decoding diagnosis

## Recommended thinking

**xhigh** — Distinguish sufficient exact-code decoding from useful cue-driven completion and avoid attributing a mixed failure to one mechanism.

## Problem / hypothesis

[D-R1](../reports/STUDY_D_R1_DECISION.md) preserved stored codes in audited checkpoints while ordinary recall failed. Can the fixed decoder use those codes when completion is removed? The [owner selected this diagnostic](../docs/requests/retrieval_diagnostic_2026_11_19.md).

## Scope

Review validity, frozen criteria, uncertainty and resources; preserve earlier gates and select no automatic successor.

Use [D-R2 v1](../docs/STUDY_D_R2_PROTOCOL.md) and its [manifest](../docs/protocols/study_d_r2_v1.json). Classification: **essential next**.

## Acceptance criteria

- [x] Classify the bounded result as supported, practically small, inadequate decoding, inconclusive or invalid.
- [x] Verify privileged scoring was isolated and earlier evidence remains intact.
- [x] Record proceed/revise/stop for evidence acceptance and at most one next recommendation.

## Metrics / evidence

Exact acquired-code minus cue-only canonical accuracy, adjusted exact-code adequacy, minimum free-coordinate code discrepancy, decoded NMSE, free-rollout errors, KV/REG-LIFT references, ten independent roots and one prescribed repeat. Fresh 900 CPU / 1,800 execution-wall seconds, 2 GiB RSS, 1 GiB artifacts, 12 fit attempts. Numerical findings belong in reports/STUDY_D_R2.md.

## Dependencies

- [SOAM-092](SOAM-092-retrieval-decoding-study.md) — required done; decision prerequisites require proceed.

## Branch conditions

The November 19 request selects only this diagnostic. SOAM-089 proceed accepts scoped negative evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. No E0, D3/D4, learned organization, coupling or later branch is activated.

## Completion record

Started after SOAM-092 completed. Reviewing the frozen gap/adequacy rules, independent audit, complete raw archive and scoped interpretation in reports/STUDY_D_R2_DECISION.md.

**Proceed with acceptance of valid, precision-qualified inconclusive evidence only.** The [decision](../reports/STUDY_D_R2_DECISION.md) preserves the frozen width rule: exact-code accuracy 1.0, ordinary PH768 .776339, gap .223661 [.153571,.290179], width .136607 > .10. The directional gap does not override inadequate precision. Boundary intervals remain finite-sample empirical results. KV stays the scoped reference; no positive retrieval/sharing/integration gate is inferred from this metadata.

Reviewed privileged-code isolation, equal snapshot weighting, same-data controls, source/fit inventory, 40 projector audits, adjusted primary/adequacy intervals, descriptive code/rollout metrics and resources. Independent reduction verified 210 root metrics; 87 arrays and 42 checkpoint tensors repeat exactly; all 110 historical D-R1 source hashes match. Every acquired-code reference is evaluator-only and cannot update or select ordinary outputs.

The [closeout](../reports/study-d-r2/closeout.json) verifies 116 frozen files against both the working source and archived copies and hashes 397 payload files. `uv run python scripts/close_study_d_r2.py` completed without new fitting/inference. Cumulative use before its final receipt: 26.880253 CPU / 27.089411 execution-wall seconds, 366,903,296 B peak RSS and 348,556,036 bytes; all limits pass. Source commit/fingerprint, complete roots and command history are recorded in SOAM-092 and the report. The final plot was visually checked.

At most one follow-up is recommended conditionally: a fresh fixed-design precision replication if the next architecture decision requires a formal diagnosis. It requires fresh routing/streams and its own frozen count/ceiling; no successor is selected and no unused allocation is silently spent. Owner notified of the blog-worthy stored-code/usable-recall distinction, with inconclusive classification prominent; no publication, push or remote issue action. Historical negative gates remain intact.

Validation: 328 tests passed before trials, Ruff and whitespace checks passed, and the ticket validator checked 94 tickets/two templates. All 526 local links in the changed Markdown set resolved before archive closure. Final metadata/archive checks are recorded in the closing commit.
