---
schema_version: 2
id: "SOAM-049"
title: "Specify a minimal test of the benefit of shared recurrence"
type: "decision"
status: "backlog"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01", "WP-08"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-047"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-049: Specify a minimal test of the benefit of shared recurrence

## Recommended thinking

**xhigh** — Operationalize neuronal sharing and directional dynamics with causal controls that distinguish useful overlap from interference or hidden state separation.

## Problem / hypothesis

Does sharing recurrent units for feature recall and action-conditioned relational transitions improve a prespecified behavior at a comparable resource budget, and what interference does it cause? Use fixed sensing and supplied structure. Acquisition, concurrent binding, handover, and broad composition are subsequent forks.

Specification: [v0.3](../docs/RESEARCH_SPEC_V0_3.md), refined by the [conditional research paths](../docs/RESEARCH_PATHS.md).

## Scope

- Specify one small fixed-sensing action-conditioned transform task. Separate held-out states/actions within known transformations from later compositional generalization. Use supplied structure or declared offline fitting; freeze confirmation parameters.
- Compare one shared asymmetric candidate, its constrained disjoint form, a competent small GRU, and a cheap action-conditioned linear/local sanity reference. Separate same-width mask ablations from matched-budget comparisons; shared parameters, topology, capacity, and readout power are confounds to report.
- Include symmetric-only/action-shuffled controls, one causal overlap intervention with equal-size random/disjoint lesions, and a small perturbation/cue-removal probe. Activity overlap in an arbitrary coordinate basis is not a basis-invariant proof of semantic sharing.
- Freeze equations, state/connectivity basis, integrator, candidate counts, primary transition-error benefit, recall/interference guardrails, split/seed hierarchy, precision rules, tuning and compute caps before fitting. No concurrency or learning requirement.

## Acceptance criteria

- [ ] Publish a minimal RFC/protocol and versioned manifest; adopt E1 quantitative defaults from the review or justify changes before data-dependent fitting.
- [ ] Require a practical transition-error advantage over strong required references, paired uncertainty, retention guardrails, and evidence beyond decoding; report all baselines even when the development-selected comparator is weaker.
- [ ] Show how causal overlap/action interventions distinguish ordinary parameter sharing, sparse connectivity, readout compensation, stored sequence replay, and useful directed recurrent computation.
- [ ] Prespecify valid benefit, no-benefit, interference, directional-failure, and invalid/inconclusive outcomes, including near-zero-error floor and budget-mismatch handling.
- [ ] Record proceed/revise/stop for this protocol only. Freeze the finite study and keep online learning, multi-instance binding, and broader applications deferred.

## Metrics / evidence

Planned protocol: docs/SHARED_POPULATION_PROTOCOL.md and versioned manifest. Start from the v0.3 reference list; SOAM-030/045 can inform design but are not prerequisites. This is a protocol decision, not H1/H5 confirmation.

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R1/R2/R3/R6/R11) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Not started. Record actual sources, tests/commands, artifacts, limitations, and
source/configuration/seed provenance appropriate to the work. Set decision to proceed,
revise, or stop only after completing the review.
