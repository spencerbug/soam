---
schema_version: 2
id: "SOAM-046"
title: "Adopt shared-population recurrent experimentation scope"
type: "engineering"
status: "done"
priority: "P0"
recommended_thinking: "high"
milestone: "MX"
work_packages: ["WP-00", "WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: []
labels: ["type:engineering", "priority:P0", "milestone:MX"]
assignees: []
created: "2026-11-05"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-046: Adopt shared-population recurrent experimentation scope

## Recommended thinking

**high** — Reconcile shared neuronal representations, independent experiment tracks, and existing contracts without turning a planning preference into scientific evidence.

## Problem / hypothesis

The owner's 2026-11-05 request makes shared neurons across feature, relationship,
and action-relation functions the preferred architecture hypothesis. SOAM should
also support many Hopfield/recurrent-dynamics experiments, including NeuroSLAM-style
localization and a Monty-style learning module using recurrent memory in place of
point-cloud/graph storage. This ticket records that request and updates planning only.

## Scope

- Adopt a dated scope amendment; preserve completed evidence and the frozen v1 handover contract.
- Revise affected future tickets, dependencies, priorities, and project navigation together.
- Allocate bounded platform, shared-population, localization, and learning-module work; keep implementation and trials unstarted.

## Acceptance criteria

- [x] Shared neurons are an explicit preferred candidate, with overlap/interference tests and separated-population controls.
- [x] Reusable infrastructure and independent application tracks have bounded tickets, prerequisites, and negative-result acceptance.
- [x] Existing reports, code, configurations, frozen protocols, and completed gate outcomes remain intact.
- [x] Ticket metadata, dependency DAG, links, and priority mirrors validate; documentation agrees on the next task.

## Metrics / evidence

Documentation and dependency consistency only. No experiment, seed, model, or performance result is produced by scope adoption.

## Dependencies

None. This is the owner's explicit planning revision, not a research gate.

## Completion record

Completed 2026-11-05 as documentation/ticket work at the owner's request.
Adopted [v0.3](../docs/RESEARCH_SPEC_V0_3.md), revised 25 existing future/comparison
tickets, and added this adoption record plus 12 bounded future tickets. Updated
[priorities](../PRIORITIES.md), [roadmap](../docs/ROADMAP.md), architecture, README,
ticket conventions, and agent scope together. SOAM-047 is the next ready task;
SOAM-035 remains a ready P2 comparison with its original experimental contract.
No future implementation or research decision was marked complete.

Actual validation:

- `UV_CACHE_DIR=/tmp/soam-uv-cache uv run python scripts/check_tickets.py` passed
  before edits (46 tickets) and after the revision (59 tickets, dependency/order/link
  checks and 2 GitHub templates).
- `git diff --check` passed.
- A documentation snapshot/link/hash audit verified all local links in changed
  Markdown, 99 unchanged code/test/config/protocol/report/package files, and the
  seven previously completed tickets unchanged. Existing dirty work was preserved.
- Qwen bulk extraction reached its output limit and returned partial findings with
  unreliable line references. Primary review checked the affected ticket text
  directly; no worker patch or action was applied.

Source base: `6ed54ae4fa28eea52b858bef2a9f916ec7c04b6a`, with pre-existing uncommitted
harness/documentation work. Adopted scope SHA-256: `186e8739d38cd10aece199b837d28d10c281d4d346fc315a92441260bda3a282`.
No executable code changed in this task, so pytest was not rerun. Experimental
configurations, seeds, training, and measured trials are not applicable to this
planning revision. All historical negative results and gate decisions remain intact;
new protocols, implementations, and experiments remain unfinished. No remote issues
were created or synchronized.
