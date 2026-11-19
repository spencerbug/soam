---
schema_version: 2
id: "SOAM-093"
title: "Review the retrieval-versus-decoding diagnosis"
type: "decision"
status: "in_progress"
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
decision: null
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

- [ ] Classify the bounded result as supported, practically small, inadequate decoding, inconclusive or invalid.
- [ ] Verify privileged scoring was isolated and earlier evidence remains intact.
- [ ] Record proceed/revise/stop for evidence acceptance and at most one next recommendation.

## Metrics / evidence

Exact acquired-code minus cue-only canonical accuracy, adjusted exact-code adequacy, minimum free-coordinate code discrepancy, decoded NMSE, free-rollout errors, KV/REG-LIFT references, ten independent roots and one prescribed repeat. Fresh 900 CPU / 1,800 execution-wall seconds, 2 GiB RSS, 1 GiB artifacts, 12 fit attempts. Numerical findings belong in reports/STUDY_D_R2.md.

## Dependencies

- [SOAM-092](SOAM-092-retrieval-decoding-study.md) — required done; decision prerequisites require proceed.

## Branch conditions

The November 19 request selects only this diagnostic. SOAM-089 proceed accepts scoped negative evidence, not a positive retrieval gate. Historical SOAM-052 stop and SOAM-069 revise remain intact. No E0, D3/D4, learned organization, coupling or later branch is activated.

## Completion record

Started after SOAM-092 completed. Reviewing the frozen gap/adequacy rules, independent audit, complete raw archive and scoped interpretation in reports/STUDY_D_R2_DECISION.md.
