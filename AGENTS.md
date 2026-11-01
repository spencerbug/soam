# SOAM research instructions

Read README.md, docs/RESEARCH_SPEC.md, docs/EXPERIMENTS.md, and the current report first.
For planned work, also read PRIORITIES.md, tickets/README.md, and the relevant ticket/dependencies.
Run `uv run pytest` before modifying existing code. An empty bootstrap suite is not a pass.

The user supplied SOAM v0.1 on 2026-10-25 and adopted the switching-first v0.2 scope
on 2026-11-01. Read docs/RESEARCH_SPEC_V0_2.md alongside the historical v0.1 spec.
The old global interface freeze is superseded; concrete new interfaces must be
defined in the relevant protocol before implementation. Preserve existing experiment
contracts and negative results; do not claim
attractors, compositionality, self-organization, or neuroscientific validation from
bounded trajectories or ordinary RNN prediction alone.

## Current scope

The initial WP-00/WP-01 substrate sprint is delivered; its full H1 claims remain open.
The primary path now tests cue-driven concurrent attractor handover with attended,
tracking, and primed roles and sensorimotor feedback. Switching has priority over
rich prediction; an explicit attractor candidate and recurrent controls are required.
Heavy declared scaffolding is permitted. Investigate shared populations, separate
parallel circuits, shared-weight/separate-state clones, alternating banks, and
columns/stacks as alternatives; no single-population concurrency assumption or
mandatory discrete world graph is adopted. Choose a bounded subset per protocol.
The historical writer remains a separate comparison branch. Learned organization
and unsupervised memory discovery are later work, not prerequisites for the first
handover study. Completed Gate 1 does not pass the new handover gate.
The remaining timeline is tracked in PRIORITIES.md and tickets/. Start from the next
eligible ticket rather than treating the full backlog as authorization to implement
every stage. Prerequisite decision tickets must be complete with `decision: "proceed"`
before dependent implementation starts; also honor conditions in the ticket body.
Planning tickets do not by themselves pass a research gate. Empty future module
directories are boundaries, not implementations.

## Experimental rules

- Use Python/PyTorch. Keep the initial sensory projection fixed.
- Keep transient hidden state, persistent parameters, and environment ground truth separate.
- Prediction/imagined rollouts must not modify persistent parameters.
- Evaluation cannot pass hidden world states or correct future observations into free rollouts.
- Give every result its configuration, seed, source commit, source fingerprint, software versions,
  numerical settings, data exposure, parameter/storage counts, timing, and compute estimates.
- Separate train, development, and test random streams. Tune on development only.
- Use multiple fixed seeds and equivalent total parameter budgets where practical;
  state differences and report compute rather than claiming perfect matching.
- Compare grounded one-step error with free multistep error, switching, and perturbation responses.
- A tanh bound is not evidence of recovery toward a trajectory or useful attractors.
- A scripted bank swap or state copy is not evidence of cue-driven attraction.
  Record the supplied/learned status of cues, basins, correspondence, role labels,
  schedules, and controllers. Count every active state, cloned weight, and coupling.
- Keep estimated actual state, desired successor state, sensory/memory attention,
  and motor execution authority distinct. Shared parameters do not imply shared
  instance state; sensory evidence must not be double-counted through associative cues.
- Keep baseline results and failure analysis. Advance one work package at a time.
- Tests must cover scientific invariants, data separation, no-write inference, and reproducibility.
- Review and verify local-worker output. Never let a worker control its own approval or trials.

## Ticket format and housekeeping

- Keep one bounded task/experiment/decision in `tickets/SOAM-###-short-slug.md`.
  Copy `tickets/TEMPLATE.md`; allocate the next unused ID. Never reuse or renumber IDs,
  and do not confuse them with GitHub issue numbers.
- Frontmatter must begin/end with `---` and follow schema version 2 in
  `tickets/README.md`: required fields are `schema_version`, `id`, `title`, `type`,
  `status`, `priority`, `recommended_thinking`, `milestone`, `work_packages`, `hypotheses`, `depends_on`,
  `labels`, `assignees`, `created`, `updated`, `github_issue`, and `decision`.
  Use one key per line with JSON-compatible YAML values: double-quoted strings/dates,
  inline arrays, integers, or `null`. No aliases, bare strings, duplicate keys, or multiline values.
- Valid types: `engineering`, `experiment`, `decision`, `research`. Valid statuses:
  `backlog`, `ready`, `in_progress`, `blocked`, `done`, `cancelled`. Priorities are
  `P0`–`P3`; milestones are `M0`–`M8`/`MX`. Keep work-package and hypothesis IDs valid.
- Set `recommended_thinking` to `low`, `medium`, `high`, or `xhigh` using the rubric
  in tickets/README.md. Include a matching Recommended thinking body section with
  a task-specific rationale and mirror the level in PRIORITIES.md. It is advisory
  for main-task reasoning/review, not authorization or a model setting; keep worker
  subtasks bounded and review the recommendation when scope changes.
- Use the required issue-body sections from the template. Acceptance criteria must
  be checkable and must allow documented negative scientific results.
- Ticket frontmatter owns metadata; PRIORITIES.md owns execution ordering/milestone
  summaries and mirrors that metadata. Change both together. Keep README/ROADMAP
  links and milestone summaries current when the project phase changes.
- Before starting, verify dependencies and gate outcomes, set `in_progress`, and
  set an assignee only if a real handle is known. Do not mark future implementation
  active just because its planning ticket was written.
- Unsatisfied ordinary dependencies remain `backlog`. For an exceptional impediment,
  set `blocked` and explain the reason/resolution in `## Blockers`.
- Before setting `done`, check acceptance items and fill the completion record with
  actual tests/commands, results, report/artifact links, and source/config/seed provenance
  appropriate to the work. Never invent evidence. Document negative or inconclusive findings.
- For completed decision tickets, set `decision` to `proceed`, `revise`, or `stop`
  and explain the result. Other tickets keep it `null`. A completed revise/stop
  decision does not unblock children; retain history and explicitly revise the plan.
  Reviewing a gate does not itself require a new human permission prompt beyond
  the user's existing authorization.
- Preserve `created`; update `updated` on material changes. Retain cancelled or
  superseded tickets with a reason and replacement link. Maintain an acyclic dependency graph.
- Leave `github_issue: null` until actually published, then store the returned URL.
  Native GitHub templates in `.github/ISSUE_TEMPLATE/` use GitHub's own smaller schema.
  Pushing Markdown does not create Issues. Publish/synchronize remote issues only
  when requested; check for duplicate stable IDs and do not guess URLs or owners.
- Run `uv run python scripts/check_tickets.py` before finishing ticket changes.
  For code changes also run relevant tests and required checks. Schema changes must
  update the template, validator, instructions, and affected tickets together.
