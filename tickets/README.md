# SOAM issue backlog

Start with the [priority and milestone table](../PRIORITIES.md) and adopted
[v0.3 specification](../docs/RESEARCH_SPEC_V0_3.md). SOAM is now planned as a reusable
Hopfield/recurrent-dynamics experiment platform, with shared neurons across feature,
relationship, and action-relation functions as its preferred architecture hypothesis.

SOAM-046 records the November 5 scope adoption. SOAM-047/048 define and build the
platform; SOAM-049–052 specify, implement, measure, and review a minimal shared-population
benefit pilot; SOAM-059 selects the next experimental fork. SOAM-053–055 cover active disambiguation inspired by localization;
SOAM-056–058 cover a Monty-style recurrent learning module. Application tracks have
independent protocol decisions and share infrastructure, without waiting for the
full SOAM integration chain. Protocol completion never passes an empirical gate.

Completed tickets and original results retain their meanings. SOAM-035/036 remain
the frozen v1 handover comparison branch. Revised belief/control/composition/learning
tickets use the new shared-population gate; SOAM-045 studies an optional recurrent
attention backend. Historical filenames remain stable even where titles change from
multi-circuit to shared-population learning. No ticket is closed by implication.

Milestone/work-package and H1–H8 IDs remain thematic provenance categories. New
application metrics do not invent new hypothesis IDs or renumber historical gates.
SOAM-047 adopted the [minimal platform contract](../docs/RECURRENT_PLATFORM_CONTRACT.md).
SOAM-049 froze the [E1 protocol](../docs/SHARED_POPULATION_PROTOCOL.md) and
[manifest](../docs/protocols/shared_population_v1.json). SOAM-048 delivered the
[fixture runner](../reports/RECURRENT_PLATFORM.md). The next primary task is
SOAM-050's scientific candidates and engineering checks; fitting/trials remain unstarted.

These are GitHub-flavored Markdown issue bodies with YAML frontmatter. They are
readable as repository files after pushing. They are **not live GitHub Issues**:
pushing commits does not publish issue records. Stable `SOAM-###` IDs are independent
of future GitHub issue numbers.

## Conditional research paths

Follow the [result-dependent paths](../docs/RESEARCH_PATHS.md). SOAM-049–051 now
cover one minimal benefit/interference pilot. SOAM-052 reviews its claim; SOAM-059
selects at most one continuation, even after a negative result. Application and
concurrency tickets require named selection as well as completed prerequisites.
Frontmatter dependencies are AND conditions, not automatic branch activation.
Check body conditions and cite the selection record before setting ready; the
validator cannot assess these scientific predicates. Unselected work stays backlog.

## Scientific review and lightweight RFCs

[SOAM-060](SOAM-060-scientific-roadmap-review.md) records the skeptical review.
The [hypothesis ledger](../docs/HYPOTHESES.md), [proposed measurable demonstrations](../docs/SCIENTIFIC_REVIEW_2026_11_05.md),
and [ticket disposition map](../docs/TICKET_REVIEW_2026_11_05.md) separate claims,
experiments, and implementation. Every recommendation is essential next, parallel
research, or future capability. These are body classifications, not new schema fields.

Use [RFC guidance](../docs/rfcs/README.md) for consequential decisions inside the
existing protocol ticket/document; do not duplicate a protocol or add approvals.
SOAM-039/044/040/041 now form an early minimal acquisition branch. SOAM-053–055
cover frozen-memory active disambiguation. SOAM-056–058 are a later module extension.
A review target is not a frozen trial criterion until the owning protocol adopts it.

## Files and ownership

- `SOAM-###-short-slug.md`: one bounded task, experiment, or decision.
- [TEMPLATE.md](TEMPLATE.md): copy for a new repository ticket.
- [PRIORITIES.md](../PRIORITIES.md): default ordering, milestone exit criteria, and mirrored metadata.
- [AGENTS.md](../AGENTS.md): mandatory agent housekeeping instructions.
- Native GitHub templates: [research task](../.github/ISSUE_TEMPLATE/research-task.md)
  and [decision gate](../.github/ISSUE_TEMPLATE/decision-gate.md).

Ticket frontmatter is authoritative for each ticket's metadata. The priority table
owns ordering and milestone summaries. The adopted v0.3 specification is the source
of current scientific intent; earlier specifications and completed contracts retain
their historical meanings. Tickets operationalize these rather than silently
revising evidence or gate outcomes.

## Frontmatter format

Use `---` delimiters at the start of the file. This project uses a deliberately
small, valid YAML subset: **one key per line; JSON double-quoted strings, inline
arrays, integers, or `null` as values**. Quote dates and statuses. Do not use YAML
aliases, multiline values, bare strings, comments within the header, or duplicate
keys. This keeps the schema checkable with Python's standard library.

```yaml
---
schema_version: 2
id: "SOAM-XXX"
title: "A concrete, bounded research task"
type: "experiment"
status: "backlog"
priority: "P2"
recommended_thinking: "high"
milestone: "M5"
work_packages: ["WP-08"]
hypotheses: ["H5"]
depends_on: ["SOAM-018"]
labels: ["type:experiment", "priority:P2", "milestone:M5"]
assignees: []
created: "2026-10-25"
updated: "2026-10-25"
github_issue: null
decision: null
---
```

The example uses a placeholder ID. Replace it with the next unused numeric ID and actual dates.

| Field | Rule |
| --- | --- |
| `schema_version` | Integer `2` |
| `id` | Stable `SOAM-###`; must match filename prefix; never reuse/renumber |
| `title` | Actionable issue title; publish as `[SOAM-###] title` |
| `type` | `engineering`, `experiment`, `decision`, or `research` |
| `status` | `backlog`, `ready`, `in_progress`, `blocked`, `done`, or `cancelled` |
| `priority` | `P0` next critical path; `P1` foundational; `P2` later/support; `P3` optional |
| `recommended_thinking` | `low`, `medium`, `high`, or `xhigh`; advisory main-task reasoning effort |
| `milestone` | One of `M0`–`M8` or `MX`; definitions are in the priority table |
| `work_packages` | Unique known `WP-00`–`WP-13` IDs; empty only for cross-cutting research |
| `hypotheses` | Unique `H1`–`H8` IDs; use only relevant claims |
| `depends_on` | Unique existing ticket IDs, no self-dependency or cycles |
| `labels` | Unique proposed GitHub labels; include `type:<type>`, `priority:<priority>`, and `milestone:<milestone>` |
| `assignees` | Known GitHub handles only; leave empty rather than inventing owners |
| `created`, `updated` | Quoted ISO dates `YYYY-MM-DD`; preserve creation date and update on material changes |
| `github_issue` | `null` until published, then the actual `https://github.com/OWNER/REPO/issues/NUMBER` URL |
| `decision` | `null` for ordinary/open tickets; completed decision tickets use `proceed`, `revise`, or `stop` |

All fields are required. Put rationale, estimates, blockers, and evidence in the
body rather than extending the schema casually. A schema change must update the
template, validator, agent instructions, and all affected tickets together.

## Recommended thinking levels

Schema version 2 adds required `recommended_thinking` metadata and a matching
**Recommended thinking** body section with a task-specific rationale. All existing
tickets have been migrated; SOAM-000 is a retrospective recommendation, not a claim
about the reasoning setting used for its completed work.

- **low:** mechanical edits or extraction with explicit acceptance checks.
- **medium:** established implementation patterns and straightforward verification.
- **high:** experiment design, coupled invariants, statistical interpretation, or gate review.
- **xhigh:** open-ended mechanism design, meta-learning, ambiguity, composition, or cross-stage synthesis.

These are project recommendations, not model-specific API settings or guarantees.
Choose an available equivalent when executing. Use the listed level for the main
reasoning and review; routine subtasks can use less effort. Increase effort when
unexpected failures or scientific ambiguity demand it. Keep local-worker tasks
bounded and verify their output regardless of the ticket level. No whole current
research ticket is assigned low solely because some subtasks are mechanical.

When scope changes, review the level and rationale together and mirror the level
in PRIORITIES.md. Recommendations do not change priority, readiness, dependencies,
or authorize experiments. When publishing a GitHub Issue, retain the body section
so the recommendation remains visible without repository frontmatter.

## Status and dependency rules

1. New future work starts in `backlog`. Ordinary unsatisfied dependencies are not
   themselves an exceptional `blocked` state.
2. Promote to `ready` only when dependencies are `done`, prerequisite decision
   tickets say `proceed`, and body-specific preconditions are satisfied.
3. Set `in_progress` when work actually begins; add a known assignee when available.
4. Use `blocked` for an explicit impediment. Add a `## Blockers` section with the
   reason, required resolution, and relevant link. Do not fabricate a human approval
   requirement for routine authorized work.
5. Set `done` only with checked acceptance criteria and a completion record. A well-run
   experiment can be done with a negative result. A gate can be done with `revise`
   or `stop`; it does not thereby unblock its children.
6. Retain cancelled/superseded tickets with a reason and replacement link. Do not
   delete evidence or silently remove dependencies to make a task ready.

A gate review is an evidence/documentation task, not automatically an additional
human permission step. The existing user authorization governs who may carry out
work and record decisions. A `proceed` decision must state its scope and residual
limitations; it is not a blanket declaration that a hypothesis is proven.

## Completion requirements

Every ticket has **Recommended thinking**, **Problem / hypothesis**, **Scope**, **Acceptance criteria**,
**Metrics / evidence**, **Dependencies**, and **Completion record** sections.
Checkboxes describe verifiable deliverables, not guaranteed positive findings.

For implementation/experiment work, record:

- Relevant tests and exact validation commands/outcomes; never claim an unrun check passed.
- Configuration, source commit/fingerprint, data splits, fixed seeds, checkpoints,
  and durable report/artifact paths. Mark missing/unavailable artifacts explicitly.
- Baselines and ablations, data exposure, parameters, time/operations/memory, uncertainty,
  and negative results appropriate to the task. Choose success criteria before testing.
- The effect on the research gate and on downstream readiness. Scientific conclusions
  require evidence beyond passing a software test or completing implementation.

For decisions/research-only work, cite the actual reviewed reports or primary sources
and record rationale/limitations. Do not invent numerical validation for a document.
Update the ticket, priority-table row, and milestone summary in the same change.
Keep README/ROADMAP links current when scope or milestone status changes.

## GitHub display and later publication

The native templates use GitHub's own `name`, `about`, `title`, `labels`, and
`assignees` frontmatter; they are separate from this repository's richer ticket
schema. They become available in the new-issue chooser after reaching the default
branch with Issues enabled. See [GitHub's template documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository).

When publication is explicitly requested:

1. Check `github_issue` and search for the stable ID to avoid creating duplicates.
2. Use `[SOAM-###] title` as the GitHub title and the Markdown body below the YAML
   as the issue body. Preserve checkboxes and dependency IDs.
3. Translate repository-relative links to actual repository file/issue URLs for the
   published issue. Set labels, milestone, and known assignees using GitHub metadata;
   local frontmatter does not synchronize them automatically. Create/verify labels
   and milestone names as part of that authorized publication.
4. Record the returned issue URL in `github_issue`, update `updated`, and keep future
   status/decision changes synchronized explicitly. Never guess issue numbers.

Actual issue creation is a separate GitHub action, as described in
[GitHub's issue-creation documentation](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue).
No publishing automation or remote action is part of this backlog change.

## Validation

```sh
uv run python scripts/check_tickets.py
```

The validator checks metadata, dates, links, required sections, dependency cycles,
ready/active/done eligibility, decision outcomes, priority-table consistency, and
native template headers. It cannot judge the scientific adequacy of evidence or
body-specific prerequisites; those still need review.
