---
schema_version: 2
id: "SOAM-032"
title: "Adopt the switching-first embodied attractor scope"
type: "research"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "MX"
work_packages: []
hypotheses: ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8"]
depends_on: []
labels: ["type:research", "priority:P0", "milestone:MX"]
assignees: []
created: "2026-11-01"
updated: "2026-11-01"
github_issue: null
decision: null
---

# SOAM-032: Adopt the switching-first embodied attractor scope

## Recommended thinking

**xhigh** — Reconcile the owner's expanded architecture with historical evidence, distinguish scaffolding from learned dynamics, and revise dependencies without passing scientific gates by planning.

## Problem / hypothesis

The October 31 architecture conversation and November 1 owner decisions prioritize
cue-driven concurrent attractor handover, sensorimotor calibration, and eventual
embodied skill reuse. The v0.1 writer-first queue no longer expresses that priority.
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

- Adopt a dated v0.2 specification and architecture boundaries; preserve v0.1 evidence.
- Record attended/tracking/primed roles, heavy initial scaffolding, and an early comparison of circuit separation alternatives.
- Reconcile the roadmap, instructions, and bounded tickets; do not implement experiments or claim new results.

## Acceptance criteria

- [x] Record the accepted owner decisions and distinguish them from unresolved mechanisms.
- [x] Preserve historical reports, completed gates, ticket IDs, and current code.
- [x] Define a switching-first path with explicit attractor and recurrent controls, sensing, and concurrency alternatives.
- [x] Reconcile later belief/control/learning work and document each changed dependency.
- [x] Validate ticket metadata, dependencies, links, and mirrored priorities.

## Metrics / evidence

Documentation evidence: supplied architecture conversation, November 1 owner
clarifications, v0.1 specification, current writer report, and Gate 1 limitations.
No measured attractor, learning, or control claim is made by this scope adoption.

## Dependencies

None. This is the owner's authorized scope revision, not a research gate.

## Completion record

Completed 2026-11-01 as a documentation-only scope adoption. Baseline source commit:
`83acbab6372c71dac2200ecf23c9355b374210b5`; changes remain in the working tree.
The working tree already contained the architecture conversation, diagrams, and
SOAM-031 with its priority/index entries. Those contributions are preserved; the
SOAM-031 scope/dependency is explicitly revised without claiming its completion.

Delivered [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md),
[architecture boundaries](../docs/ARCHITECTURE.md), [roadmap](../docs/ROADMAP.md),
and [execution/dependency migration](../PRIORITIES.md), with README, instructions,
and ticket-index updates. New tickets SOAM-033–044 bound the later work; SOAM-033
is ready and all other new follow-ups remain backlog. No existing unfinished
research ticket is closed, and no empirical gate outcome changes.

Reviewed evidence: historical [v0.1 specification](../docs/RESEARCH_SPEC.md),
[experiment protocol](../docs/EXPERIMENTS.md), [Gate 1](../reports/GATE_1_REVIEW.md),
and [current writer report](../reports/LOCAL_WRITE_CONTRACT.md), plus the supplied
October 31 conversation and November 1 owner decisions recorded in v0.2 §1.
Conversation path: `docs/ChatGPT-SOAM Architecture Baseline-20261031-2347.md`;
SHA-256: `7fdddaff7bffa87ee8f5c6a7ffa9118e1de943d06707169a1557975619b9cce9`.

Validation:

- `UV_CACHE_DIR=/tmp/soam-uv-cache uv run python scripts/check_tickets.py`:
  45 tickets and 2 native GitHub templates validated, including links, mirrored
  metadata, dependency cycles, and readiness. The cache override avoids a sandbox
  denial on the default uv cache; no permission escalation was needed.
- Additional read-only calls to the validator's `check_links` verified the new
  specification, architecture, experiment/spec notices, and AGENTS.md links.
- `git diff --check`: passed. Read-only diff inspection confirms no changes to
  runtime code, tests, configs, reports, dependency lock, or completed SOAM-000–003.
- The local worker's four-ticket extraction omitted three inputs; direct source
  review supplied the dependency audit. Its output was not accepted as evidence.

No pytest run or new trials were needed for these documentation changes; the
historical 48-test result is not represented as a new validation run. Configuration,
trial seeds, and runtime timings are not applicable to scope adoption. Numerical
thresholds, chosen circuit topology, and mechanism equations remain SOAM-033 work.
