---
schema_version: 2
id: "SOAM-103"
title: "Select the assembly organization and selective routing plan"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M1"
work_packages: ["WP-01"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-102"]
labels: ["type:decision", "priority:P0", "milestone:M1"]
assignees: []
created: "2026-11-22"
updated: "2026-11-22"
github_issue: null
decision: "proceed"
---

# SOAM-103: Select the assembly organization and selective routing plan

## Recommended thinking

**xhigh** — Reframe the selected question around learned connectivity while preserving the retention design, failed gates, and the distinction between a planning decision and a frozen experiment.

## Problem / hypothesis

The owner clarified that assembly organization depends on learned effective
connections, distributed sensory drive, and internal persistence. Hysteresis is one
candidate mechanism and does not name the broader study. Apply the
[common completion requirements](README.md#completion-requirements).

## Scope

Select one bounded assembly-organization design path. Update the experimental plan,
scope addendum, hypothesis ledger, priorities, and dependent tickets. Preserve
SOAM-102 and its E0-HYS numerical design as an unrun, currently unselected retention
diagnostic. This task does not implement dynamics, fit models, or publish.

## Acceptance criteria

- [x] Record the owner selection and the superseded E0-HYS execution priority without changing historical outcomes or its numerical manifest.
- [x] Define dense fixed input, learned internal roles, selective causal routing, retention/navigation guards, and explicit unresolved mathematical choices.
- [x] Sequence equations and analytical checks, bounded simulation/harness work, a frozen pilot, and evidence review; make Lean optional and theorem-specific.
- [x] Keep the next protocol ticket ready only after this decision; keep later stages backlog and preserve integrated organization gates.
- [x] Validate ticket metadata, dependency/body conditions, local links, and diff consistency.

## Metrics / evidence

Review the owner conversation, E0 and E0-HOLD reports/decisions, SOAM-102,
the current research contracts, and the scoped primary-source precedents. This is
a planning decision with no fitted results, numerical allocation, or scientific gate.

## Dependencies

- [SOAM-102](SOAM-102-state-hysteresis-protocol.md) — done/proceed for the earlier retention design only; no implementation or trials occurred.

## Completion record

**Proceed with AO-1 planning only.** The
[owner selection](../docs/requests/assembly_organization_2026_11_22.md) and
[Assembly organization and selective routing plan](../docs/proposed-studies/STUDY_ASSEMBLY_ORGANIZATION.md)
replace E0-HYS as the current design path. SOAM-104 is P0/ready, xhigh, for equations,
analytical checks and numerical protocol design. SOAM-105–107 remain backlog;
no AO-1 protocol is frozen, numerical allocation accepted, model implemented, or
fit run by this decision. Fixed thresholds remain the owner's preference if the
optional hysteresis mechanism is included.

Reviewed the v0.1/v0.2/v0.3 contracts, experiment rules, scientific review, hypothesis
ledger, SOAM-042/043 integration conditions, SOAM-101/102, and the
[E0](../reports/STUDY_E0.md) / [E0-HOLD](../reports/STUDY_E0_HOLD.md) reports and
decisions. The narrow scope amendment is recorded in v0.3 and AGENTS.md; neither
SOAM-052 stop nor integrated organization prerequisites change. SOAM-102 retains
done/proceed for its completed design. Its numerical manifest is not edited or
reused as an AO-1 allocation.

Manual review checked dense input without supplied ports/tree, explicit input
scaling, fixed optional thresholds, separate learning objective and dynamical
energy, no-write evaluation, candidate/control parity, discovery/test separation,
selective mediation versus common input, useful action/recovery guards, and the
required later freeze of all numeric criteria. A useful graph, a simpler control,
or a negative result is an allowed outcome. The 2014 paper is scoped to regulatory
precedents rather than treated as AO-1's underlying rule.

Validation: `UV_CACHE_DIR=/private/tmp/soam-uv-cache uv run --offline --no-sync
python scripts/check_tickets.py` accepts 108 tickets and two templates;
`git diff --check` and an inline local-Markdown-target audit pass. Branch readiness
was also reviewed manually because the validator cannot assess scientific body
conditions. Source baseline: `047e2b81496a41dbf96537e11c39b4d17e54c1d4`.
Changes are documentation only; no code, tests, or measured reports changed and
no full pytest or training run was performed. The future harness owes the required
pre-edit suite and scientific invariant checks.

The local Qwen extraction job `c7b79aa66d054721b5fec1772ff4ed0a` failed at its
output-token limit with incomplete findings. The primary agent used direct reads
of the contracts and checked the relevant clauses; no unverified worker output
determined this plan. The owner was notified that the scope shift merits a future
joint blog/report as a conceptual proposal, not a measured finding. No publishing,
remote issue creation, push, or commit was performed.
