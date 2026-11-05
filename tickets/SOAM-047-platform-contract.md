---
schema_version: 2
id: "SOAM-047"
title: "Define the shared-population experiment platform contract"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M0"
work_packages: ["WP-00", "WP-01"]
hypotheses: ["H1", "H6"]
depends_on: ["SOAM-046"]
labels: ["type:decision", "priority:P0", "milestone:M0"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: "proceed"
---

# SOAM-047: Define the shared-population experiment platform contract

## Recommended thinking

**xhigh** — Choose a small reusable abstraction without building topology assumptions or unsupported energy claims into every experiment.

## Problem / hypothesis

The current harness implements one frozen handover protocol. A broader platform needs explicit contracts for interchangeable dynamics and tasks, including shared neurons across feature, relation, and action-relation functions.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md). Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

- Define only the state/parameter/observation/action, intervention, metric, and artifact contracts needed for E1; preserve historical entry points. Use an existing protocol document as the short RFC rather than creating another design layer.
- Specify the shared candidate, constrained disjoint control, GRU, and cheap linear sanity reference contract; extension points may describe later backends without implementing them.
- Define parameter/state/external-memory/exposure accounting and a finite tuning/time budget based on fixture timings. No general framework or new environment stack.
- Keep evaluator truth, future targets, live state, persistent parameters, and no-write rollout permissions explicit; no universal energy assumption.

## Acceptance criteria

- [x] Publish concrete minimal signatures, one worked E1 flow, and one small example showing task-specific code does not leak into recurrence.
- [x] Document the ownership/resource ledger, numerical reproducibility, invalid-run behavior, and preservation checks.
- [x] Adopt the review measurement defaults or justify changes before fitting; specify the time/storage cap and equal-tuning rules.
- [x] Record proceed/revise/stop in this decision ticket using the lightweight RFC convention; explicitly defer unneeded backend and application infrastructure.

## Metrics / evidence

Adopted [platform contract v1](../docs/RECURRENT_PLATFORM_CONTRACT.md), including
interface/flow examples, resource ledger, measurement defaults, finite ceilings,
failure behavior and implementation verification requirements. Architecture evidence
only; no scientific gate is passed.

## Dependencies

- [SOAM-046](SOAM-046-shared-platform-scope.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Branch conditions

The first delivery serves only the minimal SOAM-049 recall/transition pilot. Specify extension boundaries but implement no general backend catalogue. A second tiny task fixture checks reuse only; it is not a localization or learning-module study. Expand infrastructure only when a selected fork identifies a concrete missing capability.

## Scientific review disposition — 2026-11-05

**Essential for the next experiment** (R3/R6/R7/R11) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Use the operational hypothesis ledger and the proposed quantitative criteria; protocol decisions must adopt or justify them before fitting/confirmation. No new empirical result is implied.

## Completion record

Completed 2026-11-05. Verified SOAM-046 was done and SOAM-047 was the selected
primary task, then set in_progress before drafting. No assignee handle is known.

**Decision: proceed** for the explicit-state platform contract and engineering
fixtures only. Appendix A fixes observation/action timing, snapshot ownership,
backend signatures and bounded interventions; B supplies the worked E1 flow and
two-task fixture; C adopts review defaults with finite resource ceilings and a
mandatory pre-fit feasibility check; D specifies artifacts, failures and verification.
Task-specific scientific equations, statistics and trial inventory remain SOAM-049.
Online write infrastructure and application/backend catalogues are explicitly deferred.

Reviewed the historical [handover interface](../docs/HANDOVER_HARNESS.md),
[fixture report](../reports/HANDOVER_HARNESS.md) and stored status timings; the
[writer contract](../soam/plasticity/README.md) and
[writer results](../reports/LOCAL_WRITE_CONTRACT.md); current v0.3/review/hypothesis
and conditional-path documents; and the linked primary sequence-memory/PyTorch
sources in the contract. The leaky recurrence is illustrative, not selection of
the scientific mechanism. No general asymmetric-energy guarantee is assumed.

Manual acceptance review checked all four items above. The 60-second fixture
ceiling has explicit historical timing support; the four-CPU-hour study ceiling
is labeled a resource allocation, not a measured training forecast. Preflight must
demonstrate feasibility before fitting; a negative/infeasible outcome cannot silently
expand budgets or remove controls. SOAM-048 and SOAM-049 are now ready with their
body conditions checked; SOAM-049 is next primary. Neither has been started.

Validation:

- `UV_CACHE_DIR=/tmp/soam-uv-cache uv run python scripts/check_tickets.py`: 61 tickets,
  ordering/dependencies/links and 2 GitHub templates validate.
- `git diff --check`: passed.
- Inline Python audit via `uv run python`: all 105 tracked code/config/report/protocol
  files and all nine previously completed tickets match HEAD byte-for-byte; changed
  documentation links resolve and both Python interface/flow sketches parse with AST.
  Sketch syntax is not an implementation or behavioral test.
- The Qwen extraction returned an unusable synthesis without the requested source
  references. Primary review checked the selected ownership/accounting passages
  directly; no worker patch or action was used.

Source base: `22f85020a81684db6a2eb189915e84ae29f23e9c`.
Contract SHA-256: `4a30165d4399198cc42ca5d2cc82a295718109d511fb77e86bf5ede6116e9f61`.
This task changes documentation only. No code, fitting, fixture execution, or
measured trial was performed; pytest was not rerun for this decision. Proposed
seed/configuration values in the contract are future inputs, not result provenance.
Updated priorities, navigation and child-ticket scope/readiness together; preserved
historical outcomes and temporary Draw.io files. No remote issues were synchronized.
