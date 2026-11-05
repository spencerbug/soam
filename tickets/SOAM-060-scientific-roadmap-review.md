---
schema_version: 2
id: "SOAM-060"
title: "Review scientific direction and refine evidence-driven milestones"
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
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-060: Review scientific direction and refine evidence-driven milestones

## Recommended thinking

**xhigh** — Challenge the architecture against primary research, distinguish independent scientific claims, and make bounded roadmap changes with preserved provenance.

## Problem / hypothesis

The owner requests a skeptical scientific and robotics architecture review, with
recommendations classified as essential next, parallel research, or future capability
and traceable to existing ticket IDs. Ambition alone cannot validate the mechanism.

## Scope

- Assess foundations, speculative assumptions, alternatives, missing capabilities, and implementation cost.
- Operationalize H1–H8 without changing historical meanings; define the next three experiments and progressively capable demonstrations.
- Refine existing tickets and dependencies; introduce a lightweight RFC convention without a new ticket schema or extensive new backlog.

## Acceptance criteria

- [x] Deliver a primary-source-grounded assessment and prioritized, classified recommendations.
- [x] Map hypotheses to predictions, experiments, strong baselines, measurable decisions, and negative-result interpretations.
- [x] Define quantitative proposed milestones and next-three-experiment protocols, with reproducibility and claim limits.
- [x] Record dispositions for every existing ticket ID, revise affected acceptance criteria/dependencies, and distinguish proposed protocols from frozen experiments.
- [x] Document a minimal RFC workflow, validate tickets/links, and preserve completed reports, code, protocols, and gate outcomes.

## Metrics / evidence

Research/planning evidence only. No measured trials or source-code changes are
part of this review. Record source limitations and actual validation commands.

## Dependencies

None. Explicit owner-requested scientific review; no experimental gate is passed.

## Completion record

Completed 2026-11-05. Delivered the [scientific assessment](../docs/SCIENTIFIC_REVIEW_2026_11_05.md),
[operational hypothesis ledger](../docs/HYPOTHESES.md), [complete ticket dispositions](../docs/TICKET_REVIEW_2026_11_05.md),
and [lightweight RFC guide/template](../docs/rfcs/README.md). Updated the affected
tickets, priority mirrors, roadmap, architecture, scope, and research paths together.

The review challenges unconditional sharing/graph-free assumptions, strengthens
E1 controls, moves minimal E2 acquisition before skills/concurrency/replay stacks,
and refocuses E3 on active ambiguity resolution. Larger Monty-style module work
now requires narrow acquisition evidence. Only this review ticket was added;
future implementation and empirical gates remain unfinished. Proposed numerical
defaults still require adoption or justified revision before trial fitting.

Actual checks:

- `UV_CACHE_DIR=/tmp/soam-uv-cache uv run python scripts/check_tickets.py`: passed
  on the 60-ticket starting backlog and the revised 61-ticket backlog, including
  ordering, dependencies, links, and 2 GitHub templates.
- `git diff --check`: passed.
- A snapshot/link/hash audit verified 61 unique ticket dispositions, valid local
  links in changed Markdown, 104 unchanged code/test/script/config/protocol/report/
  package files, and every previously completed ticket unchanged.

Primary-source references and access limitations are recorded in the review.
The bounded Qwen extraction was interrupted by the user turn interruption and its
exec result was unavailable on continuation; the affected acquisition/application
ticket text was checked directly. No worker patch or unverified action was used.

Source base: `6ed54ae4fa28eea52b858bef2a9f916ec7c04b6a`, with existing uncommitted
harness and documentation work preserved. This review changed documentation only;
pytest was not rerun and no new model, training, simulation or measured experiment
was performed. Experimental configurations/seeds are not applicable to completion
of this planning task; seed lists and thresholds in the review are proposals.
No remote issues were published or synchronized.
