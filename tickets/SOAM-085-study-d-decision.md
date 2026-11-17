---
schema_version: 2
id: "SOAM-085"
title: "Review persistent memory benefit and cheapest reliable mechanism"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-084"]
labels: ["type:decision", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-17"
updated: "2026-11-17"
github_issue: null
decision: "proceed"
---

# SOAM-085: Review persistent memory benefit and cheapest reliable mechanism

## Recommended thinking

**xhigh** — Separate persistent acquisition from transient recall, evaluate strong simpler controls, and preserve information/resource parity.

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

- [SOAM-084](SOAM-084-study-d-experiment.md) — completed prerequisite; decision requires proceed.

## Branch conditions

The November 17 owner request selects this fresh fork; the superseded SOAM-059 selection is not reused. SOAM-082 must accept the protocol before implementation; SOAM-083 must verify invariants and fixture feasibility before development/confirmation. SOAM-052 stays stop. No downstream integration or D3/D4 branch is activated by completion.

## Completion record

**Proceed with acceptance of D0–D2 and KV as the scoped reliable reference only.**
The [decision](../reports/STUDY_D_DECISION.md) reviews observability, frozen criteria,
all controls, allocation, uncertainty, failures and the SOAM-084 verification. The
tested FAST practical-benefit claim is negative; REG/FAST retention failures are
established, not hidden behind isolated-object acquisition success. KV's 100%
sampled old-object accuracy is not a universal guarantee. Actual allocation and
latency tradeoffs remain explicit. No shared-neuron, attractor, learned-scope or
whole-model reuse claim follows.

All 16 fits and 88 evaluations complete; 64 repeated arrays are exact; independent
reduction and archive checks pass. Source/config/seed/resource identities and actual
commands are in SOAM-084 and the linked report. The owner was notified that the
acquisition/retention distinction merits a joint blog/report; nothing was published.

Recommend only a fresh full-versus-partial-cue D2 diagnostic, without selecting
or executing it. D3/D4 remain deferred. Historical SOAM-052 stop, SOAM-069 revise,
and A/B/B2/C outcomes are preserved; SOAM-039 and all other forks stay unselected.

Final checks: 86 tickets and two templates validated; `uv run ruff check soam tests scripts` and `git diff --check` passed; report/protocol/ticket links resolved; all 102 frozen D source hashes still match.
