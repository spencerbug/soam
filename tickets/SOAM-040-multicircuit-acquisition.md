---
schema_version: 2
id: "SOAM-040"
title: "Measure one-shot and few-observation acquisition with retention"
type: "experiment"
status: "backlog"
priority: "P1"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-039", "SOAM-044"]
labels: ["type:experiment", "priority:P1", "milestone:M2"]
assignees: []
created: "2026-11-01"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-040: Measure one-shot and few-observation acquisition with retention

## Recommended thinking

**xhigh** — Distinguish retained grounded generalization from immediate error correction, transient adaptation, and hidden repeated exposure.

## Problem / hypothesis

Grounded updates must improve held-out behavior while preserving unrelated feature, relation, action, and instance knowledge.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Run only the selected E2 protocol across 0/1/2/4/8/16 distinct new transitions, preserving candidate topology and all frozen criteria.
- Evaluate unseen states/actions and old tasks after each budget with no writes; reset transient state to check persistent recall.
- Compare selected associative, delta/RLS, online-gradient, no-write and bounded retrieval behavior; report sample and compute efficiency separately. No full replay/shadow-consolidation prerequisite.

## Acceptance criteria

- [ ] Publish normalized acquisition-area effects and paired uncertainty against every required adaptive reference, plus old-task and multistep guardrails.
- [ ] Report the one-distinct-observation endpoint separately; no one-shot claim from repeated target optimization or memorizing the tested point.
- [ ] Count every new target, history read, replay, optimizer step, stored record and offline fitting exposure; evaluate reset persistence and held-out generalization.
- [ ] Archive all configurations/source/seeds/versions/numerical settings, timing/storage/compute and confirmation reproduction, including harmful writes and failed seeds.
- [ ] A negative result may complete the experiment; do not add capacity, new controllers, or extra observations to rescue the frozen criterion.

## Metrics / evidence

Expected report: reports/SHARED_POPULATION_ACQUISITION.md (stable planned path). Use E2 review defaults once adopted by the protocol: area over the fixed linear observation-count axis, one-exposure held-out error, retention, multistep error, reset persistence and measured compute. Integration and generic instance binding remain later claims.

## Dependencies

- [SOAM-039](SOAM-039-grounded-memory-design.md) — required completed prerequisite; decision prerequisites require proceed and applicable body conditions.
- [SOAM-044](SOAM-044-multicircuit-write-contract.md) — required completed prerequisite; decision prerequisites require proceed and applicable body conditions.

## Scientific review disposition — 2026-11-05

**Future capability** (R4) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Not started. Record actual commands/results, report/artifact links, source/configuration/seed
provenance, supplied scaffolding, negative results, and the effect on downstream readiness.
