# Priority and milestone tracker

Updated: 2026-10-25. This is an evidence-driven sequence, not a calendar commitment.
Dates and durations will be estimated when each milestone is scoped; dependencies
and research outcomes can change the order. The baseline and strengthened controls
are complete; Gate 1 proceeds to bounded low-rank local-acquisition research. A passed readiness screen does not close every H1 claim.

Ticket frontmatter is authoritative for status, priority, recommended thinking,
milestone, and dependencies.
This file owns the default execution order and milestone summaries; update both in
the same change. See [ticket conventions](tickets/README.md) and [agent instructions](AGENTS.md).

## Priority and status legend

- **P0:** next critical-path work or decision.
- **P1:** foundational learning mechanisms after prerequisites are satisfied.
- **P2:** later integration, transfer, grounding, planning, or bounded supporting research.
- **P3:** optional extension; never a hidden prerequisite of the main program.
- **ready:** prerequisites are satisfied; **backlog:** planned but not yet scheduled/eligible;
  **in_progress:** active; **blocked:** an explicit impediment requires resolution;
  **done:** acceptance/evidence complete, which can include a negative result;
  **cancelled:** retained with a reason or replacement.

SOAM-003 is in progress; SOAM-019 and SOAM-030 are ready.
[Gate 1](reports/GATE_1_REVIEW.md) proceeds with low-rank and retains GRU as a reference;
SOAM-001's additive failure and unresolved H1 claims remain recorded.
A dependency on a decision ticket requires
`done` plus `decision: "proceed"`, not merely closure. Extra conditions in ticket
bodies (such as the flow prerequisite) still apply. Revise/stop decisions retain
history and require an explicit plan/dependency update before downstream work.

## Milestones

| Milestone | Focus | Exit evidence / decision | State |
| --- | --- | --- | --- |
| M0 | Initial substrate infrastructure | Recorded baseline and exact reproduction (SOAM-000); full H1 remains open | Complete initial sprint |
| M1 | Substrate controls | Matched controls and Gate 1 decision (SOAM-002) | Complete; bounded proceed |
| M2 | Local acquisition and interference | Online-write comparisons and Gate 2 (SOAM-006) | Local-write contract in progress |
| M3 | Functional scopes | Matched acquisition/retention and shared transfer; Gate 3 (SOAM-010) | Planned |
| M4 | Replay and learned consolidation | Grounded validation, compute/capacity comparisons; Gate 4 (SOAM-015) | Planned |
| M5 | Compositional reuse | Withheld composition, identity/timescales, and transfer; Gate 5 (SOAM-018) | Planned |
| M6 | Sensory grounding | Frozen encoders, partial/ambiguous recovery; Gate 6 (SOAM-022) | Planned |
| M7 | Planning | Search/proposals, realized control gains, no imagination writes; Gate 7 (SOAM-026) | Planned |
| M8 | Continual embodied learning | Long-duration accumulation and H8 program review (SOAM-028) | Planned |
| MX | Supporting / optional research | Bounded literature map; flow only after useful learned refinement | Conditional / parallel |

M4 replay can start after M2 while M3 progresses. M6 encoder work can start after
M1; its full memory comparison waits for M4. M5 and M6 are not artificially ordered
by their numbering. Integration in M8 waits for both composition and planning.
Flow matching is optional and does not block any required milestone.

Thinking levels are advisory defaults for the main task; see the
[ticket rubric](tickets/README.md#recommended-thinking-levels).

## Ordered ticket queue

Lower order is the default preference among eligible tickets, not permission to
skip dependencies. Independent supporting work may proceed when the primary path
is waiting. Reordering this table never changes stable ticket IDs.

| Order | Ticket | Priority | Status | Milestone | Thinking | Depends on |
| --- | --- | --- | --- | --- | --- | --- |
| 00 | [SOAM-000: Record the reproducible substrate baseline](tickets/SOAM-000-substrate-baseline.md) | P0 | done | M0 | medium | — |
| 01 | [SOAM-001: Strengthen substrate controls and budget comparisons](tickets/SOAM-001-substrate-controls.md) | P0 | done | M1 | high | [SOAM-000](tickets/SOAM-000-substrate-baseline.md) |
| 02 | [SOAM-002: Gate 1: review the substrate before online writing](tickets/SOAM-002-gate-1.md) | P0 | done | M1 | high | [SOAM-001](tickets/SOAM-001-substrate-controls.md) |
| 03 | [SOAM-003: Define the grounded local-write contract and plastic parameters](tickets/SOAM-003-plastic-write-contract.md) | P1 | in_progress | M2 | high | [SOAM-002](tickets/SOAM-002-gate-1.md) |
| 04 | [SOAM-004: Benchmark online transition correction and changed dynamics](tickets/SOAM-004-online-writer-baselines.md) | P1 | backlog | M2 | high | [SOAM-003](tickets/SOAM-003-plastic-write-contract.md) |
| 05 | [SOAM-005: Measure interference and learning without resets](tickets/SOAM-005-interference-metrics.md) | P1 | backlog | M2 | high | [SOAM-004](tickets/SOAM-004-online-writer-baselines.md) |
| 06 | [SOAM-006: Gate 2: decide whether local acquisition is viable](tickets/SOAM-006-gate-2.md) | P1 | backlog | M2 | high | [SOAM-004](tickets/SOAM-004-online-writer-baselines.md), [SOAM-005](tickets/SOAM-005-interference-metrics.md) |
| 07 | [SOAM-007: Compare unfiltered, sparse, random, and sensitivity-based scopes](tickets/SOAM-007-heuristic-scopes.md) | P1 | backlog | M3 | high | [SOAM-006](tickets/SOAM-006-gate-2.md) |
| 08 | [SOAM-008: Build shared-scope and noisy-evidence task families](tickets/SOAM-008-scope-task-families.md) | P1 | backlog | M3 | high | [SOAM-007](tickets/SOAM-007-heuristic-scopes.md) |
| 09 | [SOAM-009: Meta-train a constrained functional scope translator](tickets/SOAM-009-learned-scope.md) | P1 | backlog | M3 | xhigh | [SOAM-008](tickets/SOAM-008-scope-task-families.md) |
| 10 | [SOAM-010: Gate 3: evaluate functional scoping and beneficial sharing](tickets/SOAM-010-gate-3.md) | P1 | backlog | M3 | high | [SOAM-009](tickets/SOAM-009-learned-scope.md) |
| 11 | [SOAM-011: Implement a bounded grounded evidence buffer and replay baseline](tickets/SOAM-011-evidence-and-replay.md) | P1 | backlog | M4 | medium | [SOAM-006](tickets/SOAM-006-gate-2.md) |
| 12 | [SOAM-012: Validate consolidation candidates with shadow weights and rollback](tickets/SOAM-012-shadow-validation.md) | P1 | backlog | M4 | high | [SOAM-011](tickets/SOAM-011-evidence-and-replay.md) |
| 13 | [SOAM-013: Train a learned iterative low-rank consolidator](tickets/SOAM-013-learned-consolidator.md) | P1 | backlog | M4 | xhigh | [SOAM-010](tickets/SOAM-010-gate-3.md), [SOAM-012](tickets/SOAM-012-shadow-validation.md) |
| 14 | [SOAM-014: Measure consolidation error recovery, compute, and fixed-size capacity](tickets/SOAM-014-consolidation-scaling.md) | P1 | backlog | M4 | high | [SOAM-013](tickets/SOAM-013-learned-consolidator.md) |
| 15 | [SOAM-015: Gate 4: decide whether learned consolidation adds value over replay](tickets/SOAM-015-gate-4.md) | P1 | backlog | M4 | high | [SOAM-014](tickets/SOAM-014-consolidation-scaling.md) |
| 16 | [SOAM-016: Benchmark withheld compositions and transfer to related tasks](tickets/SOAM-016-composition-transfer.md) | P2 | backlog | M5 | xhigh | [SOAM-015](tickets/SOAM-015-gate-4.md) |
| 17 | [SOAM-017: Test identity preservation and reusable temporal structure](tickets/SOAM-017-identity-timescales.md) | P2 | backlog | M5 | high | [SOAM-016](tickets/SOAM-016-composition-transfer.md) |
| 18 | [SOAM-018: Gate 5: assess compositional reuse rather than memory maintenance](tickets/SOAM-018-gate-5.md) | P2 | backlog | M5 | xhigh | [SOAM-017](tickets/SOAM-017-identity-timescales.md) |
| 19 | [SOAM-019: Build rendered observations and frozen encoder comparisons](tickets/SOAM-019-frozen-encoders.md) | P2 | ready | M6 | medium | [SOAM-002](tickets/SOAM-002-gate-1.md) |
| 20 | [SOAM-020: Train recurrent prediction and assimilation on rendered observations](tickets/SOAM-020-grounded-prediction.md) | P2 | backlog | M6 | high | [SOAM-019](tickets/SOAM-019-frozen-encoders.md) |
| 21 | [SOAM-021: Evaluate partial observations, ambiguity, and context recovery](tickets/SOAM-021-partial-belief-recovery.md) | P2 | backlog | M6 | xhigh | [SOAM-020](tickets/SOAM-020-grounded-prediction.md), [SOAM-015](tickets/SOAM-015-gate-4.md) |
| 22 | [SOAM-022: Gate 6: review sensory grounding and belief recovery](tickets/SOAM-022-gate-6.md) | P2 | backlog | M6 | high | [SOAM-021](tickets/SOAM-021-partial-belief-recovery.md) |
| 23 | [SOAM-023: Implement candidate action search and known goal costs](tickets/SOAM-023-action-search.md) | P2 | backlog | M7 | medium | [SOAM-022](tickets/SOAM-022-gate-6.md) |
| 24 | [SOAM-024: Benchmark navigation, changed dynamics, and planning horizons](tickets/SOAM-024-planning-benchmark.md) | P2 | backlog | M7 | high | [SOAM-023](tickets/SOAM-023-action-search.md) |
| 25 | [SOAM-025: Learn goal-conditioned action proposals after search is reliable](tickets/SOAM-025-action-proposals.md) | P2 | backlog | M7 | high | [SOAM-024](tickets/SOAM-024-planning-benchmark.md) |
| 26 | [SOAM-026: Gate 7: assess planning benefit and safe memory separation](tickets/SOAM-026-gate-7.md) | P2 | backlog | M7 | high | [SOAM-024](tickets/SOAM-024-planning-benchmark.md), [SOAM-025](tickets/SOAM-025-action-proposals.md) |
| 27 | [SOAM-027: Integrate an extended continual embodied-learning benchmark](tickets/SOAM-027-continual-benchmark.md) | P2 | backlog | M8 | xhigh | [SOAM-018](tickets/SOAM-018-gate-5.md), [SOAM-026](tickets/SOAM-026-gate-7.md) |
| 28 | [SOAM-028: Review cumulative learning evidence and the next research cycle](tickets/SOAM-028-continual-review.md) | P2 | backlog | M8 | xhigh | [SOAM-027](tickets/SOAM-027-continual-benchmark.md) |
| 29 | [SOAM-029: Conditionally investigate flow-based consolidation](tickets/SOAM-029-optional-flow.md) | P3 | backlog | MX | xhigh | [SOAM-015](tickets/SOAM-015-gate-4.md) |
| 30 | [SOAM-030: Maintain a focused theory and literature evidence map](tickets/SOAM-030-theory-literature.md) | P2 | ready | MX | high | [SOAM-000](tickets/SOAM-000-substrate-baseline.md) |

## Housekeeping check

```sh
uv run python scripts/check_tickets.py
```

Do not infer successful hypotheses from a completed ticket. Keep negative outcomes
and revision decisions linked; update this table, ticket metadata, and affected
milestone summaries together. No GitHub issue numbers or URLs have been assigned.
