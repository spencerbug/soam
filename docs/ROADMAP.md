# Work packages and completion criteria

| Package | Status / criterion |
| --- | --- |
| WP-00 | Initial implementation: deterministic generator, config runner, provenance, tests, logs, comparisons, plots. Original four-model seed-11 reruns match exactly; current suite has 48 passing tests. |
| WP-01 | Strengthened six-model controls complete: 17/18 screen passes, additive seed-23 irregular-switch failure, six exact seed-11 repeats. [Current report](../reports/SUBSTRATE_CONTROLS.md). [Gate 1](../reports/GATE_1_REVIEW.md): bounded proceed with low-rank, GRU reference; full H1 reuse untested. |
| WP-02 | [Local-write contract complete](../reports/LOCAL_WRITE_CONTRACT.md) (SOAM-003); SOAM-004 ready. Acquisition versus no-adaptation and retention/multistep checks remain unproven. |
| WP-03 | Pending: per-context before/after interference and forgetting metrics validated on controlled changes. |
| WP-04 | Pending: fixed/random/sensitivity masks at matched adaptation and sparsity. |
| WP-05 | Pending: learned scope improves retention at matched new-task accuracy while allowing transfer. |
| WP-06 | Pending: grounded replay baseline with reported compute and retention. |
| WP-07 | Pending: validated shadow updates; learned refinement compared with replay. |
| WP-08 | Pending: withheld compositions and transfer distinguish reuse from interpolation. |
| WP-09 | Synthetic fixed encoder only; pretrained frozen encoder comparisons deferred. |
| WP-10 | Initial synthetic assimilation only; partial/ambiguous sensory grounding deferred. |
| WP-11 | Pending: candidate search with no persistent writes during imagination. |
| WP-12 | Pending: learned proposals compared with search/reactive baselines. |
| WP-13 | Pending: long sequential embodied benchmarks with acquisition, retention, transfer, capacity. |

Operational ordering, current ticket statuses, and milestone decisions are tracked in
[PRIORITIES.md](../PRIORITIES.md). The [ticket backlog](../tickets/README.md) breaks
these work packages into bounded tasks; ticket frontmatter is the status source of truth.
This high-level work-package overview is not an additional live status tracker.

Dependencies and the complete research program are in `RESEARCH_SPEC.md` §18.
Do not mark a scientific hypothesis supported solely because implementation is complete.

## Work-package ticket map

| Package | Implementation / experiments | Decision |
| --- | --- | --- |
| WP-00 | [SOAM-000](../tickets/SOAM-000-substrate-baseline.md) | Initial sprint evidence recorded |
| WP-01 | [SOAM-000](../tickets/SOAM-000-substrate-baseline.md), [SOAM-001](../tickets/SOAM-001-substrate-controls.md) | [Gate 1](../tickets/SOAM-002-gate-1.md) |
| WP-02 | [SOAM-003](../tickets/SOAM-003-plastic-write-contract.md), [SOAM-004](../tickets/SOAM-004-online-writer-baselines.md) | [Gate 2](../tickets/SOAM-006-gate-2.md) |
| WP-03 | [SOAM-005](../tickets/SOAM-005-interference-metrics.md) | [Gate 2](../tickets/SOAM-006-gate-2.md) |
| WP-04 | [SOAM-007](../tickets/SOAM-007-heuristic-scopes.md), [SOAM-008](../tickets/SOAM-008-scope-task-families.md) | Supports Gate 3 |
| WP-05 | [SOAM-008](../tickets/SOAM-008-scope-task-families.md), [SOAM-009](../tickets/SOAM-009-learned-scope.md) | [Gate 3](../tickets/SOAM-010-gate-3.md) |
| WP-06 | [SOAM-011](../tickets/SOAM-011-evidence-and-replay.md), [SOAM-012](../tickets/SOAM-012-shadow-validation.md) | Replay reference for Gate 4 |
| WP-07 | [SOAM-012](../tickets/SOAM-012-shadow-validation.md), [SOAM-013](../tickets/SOAM-013-learned-consolidator.md), [SOAM-014](../tickets/SOAM-014-consolidation-scaling.md) | [Gate 4](../tickets/SOAM-015-gate-4.md) |
| WP-08 | [SOAM-016](../tickets/SOAM-016-composition-transfer.md), [SOAM-017](../tickets/SOAM-017-identity-timescales.md) | [Gate 5](../tickets/SOAM-018-gate-5.md) |
| WP-09 | [SOAM-019](../tickets/SOAM-019-frozen-encoders.md) | Encoder branch after Gate 1 |
| WP-10 | [SOAM-020](../tickets/SOAM-020-grounded-prediction.md), [SOAM-021](../tickets/SOAM-021-partial-belief-recovery.md) | [Gate 6](../tickets/SOAM-022-gate-6.md) |
| WP-11 | [SOAM-023](../tickets/SOAM-023-action-search.md), [SOAM-024](../tickets/SOAM-024-planning-benchmark.md) | [Gate 7](../tickets/SOAM-026-gate-7.md) |
| WP-12 | [SOAM-025](../tickets/SOAM-025-action-proposals.md) | [Gate 7](../tickets/SOAM-026-gate-7.md) |
| WP-13 | [SOAM-027](../tickets/SOAM-027-continual-benchmark.md) | [H8 review](../tickets/SOAM-028-continual-review.md) |

Optional/supporting branches: [flow consolidation](../tickets/SOAM-029-optional-flow.md)
and [theory/literature map](../tickets/SOAM-030-theory-literature.md). Flow remains conditional,
not a prerequisite for the required program.
