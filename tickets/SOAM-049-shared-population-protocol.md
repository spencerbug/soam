---
schema_version: 2
id: "SOAM-049"
title: "Specify a minimal test of the benefit of shared recurrence"
type: "decision"
status: "done"
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
decision: "proceed"
---

# SOAM-049: Specify a minimal test of the benefit of shared recurrence

## Recommended thinking

**xhigh** — Operationalize neuronal sharing and directional dynamics with causal controls that distinguish useful overlap from interference or hidden state separation.

## Problem / hypothesis

Does sharing recurrent units for feature recall and action-conditioned relational transitions improve a prespecified behavior at a comparable resource budget, and what interference does it cause? Use fixed sensing and supplied structure. Acquisition, concurrent binding, handover, and broad composition are subsequent forks.

The adopted protocol narrows attribution: separate-role episodes admit a tied-weight,
separate-state realization with identical predictions. E1 tests a useful shared
implementation and causal unit participation, not a uniquely causal advantage of
physical neuron overlap over parameter tying. T32 makes this limit explicit.

Specification: [v0.3](../docs/RESEARCH_SPEC_V0_3.md), refined by the [conditional research paths](../docs/RESEARCH_PATHS.md).

## Scope

- Bind the adopted [platform contract](../docs/RECURRENT_PLATFORM_CONTRACT.md) to the E1 manifest, including its measurement defaults, finite study ceilings, equal-tuning rules, and fixture-only feasibility check before any fitting. Record exact inventory and endpoint/precision definitions; no fitting is authorized by the platform contract alone.
- Specify one small fixed-sensing action-conditioned transform task. Separate held-out states/actions within known transformations from later compositional generalization. Use supplied structure or declared offline fitting; freeze confirmation parameters.
- Compare one shared asymmetric candidate, its constrained disjoint form, a competent small GRU, and a cheap action-conditioned linear/local sanity reference. Separate same-width mask ablations from matched-budget comparisons; shared parameters, topology, capacity, and readout power are confounds to report.
- Include symmetric-only/action-shuffled controls, one causal overlap intervention with equal-size random/disjoint lesions, and a small perturbation/cue-removal probe. Activity overlap in an arbitrary coordinate basis is not a basis-invariant proof of semantic sharing.
- Freeze equations, state/connectivity basis, integrator, candidate counts, primary transition-error benefit, recall/interference guardrails, split/seed hierarchy, precision rules, tuning and compute caps before fitting. No concurrency or learning requirement.

## Acceptance criteria

- [x] Publish a minimal RFC/protocol and versioned manifest; adopt E1 quantitative defaults from the review or justify changes before data-dependent fitting.
- [x] Require a practical transition-error advantage over strong required references, paired uncertainty, retention guardrails, and evidence beyond decoding; report all baselines even when the development-selected comparator is weaker.
- [x] Show how causal overlap/action interventions distinguish ordinary parameter sharing, sparse connectivity, readout compensation, stored sequence replay, and useful directed recurrent computation.
- [x] Prespecify valid benefit, no-benefit, interference, directional-failure, and invalid/inconclusive outcomes, including near-zero-error floor and budget-mismatch handling.
- [x] Record proceed/revise/stop for this protocol only. Freeze the finite study and keep online learning, multi-instance binding, and broader applications deferred.

## Metrics / evidence

Adopted [E1 v1 protocol/RFC](../docs/SHARED_POPULATION_PROTOCOL.md) and
[numerical manifest](../docs/protocols/shared_population_v1.json). Primary sources
and limitations are linked in the protocol. This is a protocol decision, not H1/H5 confirmation.

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R1/R2/R3/R6/R11) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Completed 2026-11-05. Verified SOAM-047 was done with decision proceed and SOAM-049
was next primary; set in_progress before drafting. No assignee handle is known.

**Decision: proceed** for the frozen E1 v1 protocol, with implementation/feasibility
and development competence/floor screens still required before confirmation.
SOAM-048 is next; SOAM-050 remains backlog because SOAM-048 is unfinished.
SOAM-051/052/059 remain unstarted. This decision passes no empirical gate.

Manual acceptance review:

- Specified the 2D transform and fixed projection, supplied role cues, held-out
  phase/action cells, observed-target boundaries, exact symmetric/skew rate equations,
  disjoint variants, GRU and bilinear references, and inference/training schedules.
- Froze seven fitted families, two tuning configurations each, 119 maximum fit
  instances and 27,820 scoring cells including causal probes/reproduction. Preserved
  the platform's finite CPU/storage ceilings and required 2×-margin pre-fit projection.
- Adopted the review's 10% benefit, 0.005 recall guardrail, ten confirmation roots
  and 20 episodes per root/condition; operationalized references, absolute competence,
  adjusted uncertainty, precision, finite-run, floor and stopping criteria before fitting.
- Paired parameter/state controls and targeted/random/disjoint/readout-only lesions
  expose capacity and decoder confounds; direction and recovery are distinct tests.
  T32's expected intact equivalence is a substantive identifiability limit, not an
  empirical result. A positive E1 result cannot establish superiority of physical
  neuron overlap over tied parameters; future stronger claims require another test.
- Carried that limitation into SOAM-050/051/052, the hypothesis ledger and conditional
  paths; updated readiness/navigation without activating another ticket. Flagged
  the methodological concept to the owner as a potential blog/report topic; nothing
  was published and no blog was drafted.

Reviewed current platform/v0.3/review/hypothesis/path documents, the original
substrate protocol and preserved writer regressions, plus the linked Hopfield,
asymmetric sequence-memory and official GRU sources. None establishes this candidate's
performance or an energy theorem. The Qwen extraction returned unrelated H6–H8
content and ticket numbers as line references; primary review checked the H1/E1
source passages directly. No worker patch or action was applied.

Actual validation:

- `UV_CACHE_DIR=/tmp/soam-uv-cache uv run python /tmp/soam049_audit.py`: strict JSON
  parsing/unique keys, all seven parameter/state formulas, split combinatorics,
  fit/cell arithmetic, phase budgets and local links passed. All 109 protected
  source/config/report/protocol files and ten previously completed tickets match HEAD.
- `UV_CACHE_DIR=/tmp/soam-uv-cache uv run python scripts/check_tickets.py`: 61 tickets,
  ordering/dependencies/links and 2 GitHub templates validate.
- `git diff --check`: passed. These are protocol/document consistency checks, not
  executable candidate verification or measured evidence. No existing code changed;
  pytest, fitting, calibration timings and experiments were not run for this decision.

Source base: `293adc422dba9cf59bdb98321eed1c618429558d`.
Protocol SHA-256: `98846328f3ad6803a7e85d910fc2be2f8075c5d44e75d19351ad311d9eae12bf`.
Manifest SHA-256: `beda95e9aba660c4b912339dfe26f331363e8de7cbc715af132e95fd1821d83e`.
Seed/config values are frozen future inputs, not trial provenance. Historical
outcomes and Draw.io temporary files are unchanged; no remote issues were synchronized.
