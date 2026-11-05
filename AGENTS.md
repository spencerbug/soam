# SOAM research instructions

Read README.md, docs/RESEARCH_SPEC.md, docs/EXPERIMENTS.md, and the reports relevant
to the selected ticket first; README.md indexes the reports. A newer engineering
report does not replace an earlier empirical result or gate decision.
For planned work, also read PRIORITIES.md, tickets/README.md, and the relevant ticket/dependencies.
Run `uv run pytest` before modifying existing code. An empty bootstrap suite is not a pass.

The user supplied SOAM v0.1 on 2026-10-25 and adopted the switching-first v0.2 scope
on 2026-11-01. On 2026-11-05 the owner adopted the shared-population experiment
platform scope. Read docs/RESEARCH_SPEC_V0_3.md for current intent alongside
historical v0.1/v0.2 and preserve their experimental contracts.
The old global interface freeze is superseded; concrete new interfaces must be
defined in the relevant protocol before implementation. Preserve existing experiment
contracts and negative results; do not claim
attractors, compositionality, self-organization, or neuroscientific validation from
bounded trajectories or ordinary RNN prediction alone.

## Current scope

The initial WP-00/WP-01 substrate sprint and v1 handover harness are delivered;
full H1 and measured handover claims remain open. The primary path now defines a
reusable Hopfield/recurrent-dynamics experiment platform and tests overlapping
neurons for feature, relationship, and action-relation functions. Shared weights,
cloned states, or concatenated disjoint networks do not establish shared neurons.
Keep separated populations, symmetric-only dynamics, and ordinary recurrence as
controls; test overlap, binding, interference, and asymmetric transition behavior.
Functional evidence/goal/motor/write boundaries do not mandate separate neural stores.
SOAM-035/036 retain the frozen v1 handover study as a P2 comparison branch. The new
shared-population gate controls later integrated SOAM work. NeuroSLAM-inspired
localization and Monty-style recurrent learning-module tracks have independent
protocols on common infrastructure, not dependencies on the full integration chain.
Heavy declared scaffolding is permitted. Keep graph/point-cloud memory as labeled
controls for recurrent-memory candidates; simulator geometry remains task/evaluator
data. No universal one-population concurrency or symmetric-energy guarantee is assumed.
The historical writer remains a separate comparison branch. Learned organization
and unsupervised memory discovery remain later work. Completed Gate 1 and engineering
fixtures do not pass the new shared-population or historical handover gates.
Read docs/SCIENTIFIC_REVIEW_2026_11_05.md and docs/HYPOTHESES.md for current
operational claims and proposed quantitative criteria. Minimal acquisition now
precedes skills/concurrency; active disambiguation uses a small supplied policy.
Use lightweight RFCs within existing decision tickets, not a new approval layer.
Classify review recommendations as essential next, parallel research, or future
capability and preserve ticket-ID traceability.
Follow docs/RESEARCH_PATHS.md for result-dependent forks. The first shared pilot
tests one declared benefit with interference guardrails; concurrency and applications
are later selected branches. Dependencies alone do not activate a conditional ticket.
Preserve failed gates and create fresh corrective protocols/reviews rather than
changing a negative outcome or running all branches.
The remaining timeline is tracked in PRIORITIES.md and tickets/. Start from the next
eligible ticket rather than treating the full backlog as authorization to implement
every stage. Prerequisite decision tickets must be complete with `decision: "proceed"`
before dependent implementation starts; also honor conditions in the ticket body.
Planning tickets do not by themselves pass a research gate. Empty future module
directories are boundaries, not implementations.

## Research decision discipline

- Treat shared recurrence as a candidate mechanism, not a required conclusion.
  Simpler separated, conventional recurrent, structured-memory, or hybrid models
  are valid outcomes. Identify the smallest experiment that could change the next
  architectural decision; do not build a general framework or a future mechanism
  merely because it appears in the roadmap.
- Keep ownership clear: docs/HYPOTHESES.md owns operational claims; the selected
  protocol/manifest owns frozen experimental criteria; reports own measured evidence;
  decision tickets interpret that evidence; PRIORITIES.md selects eligible work.
  Follow docs/rfcs/README.md for consequential choices. Routine reversible details
  need no RFC, duplicate protocol, additional ticket, or approval ceremony.
- Review thresholds are proposals until the owning protocol adopts or justifies
  changes to them. Before fitting/confirmation, freeze the primary endpoint,
  guardrails, mandatory baselines, splits/seeds, uncertainty and precision rules,
  tuning/compute limits, and stopping rule. Fixture timings may inform the budget.
  Do not tune on confirmation results, silently extend a budget, or present reused
  confirmation data as unseen. Material changes require a versioned protocol and
  fresh confirmation streams as applicable; preserve the earlier outcome.
- Distinguish supported benefit, adequately precise negative evidence, inconclusive
  evidence, and invalid execution. A wide interval is not equivalence; a software
  failure is not a scientific falsification. Scope conclusions to the tested task,
  mechanism, and resources. Passing a protocol review accepts a test, not its hypothesis.
- Select at most one next experimental fork using information gained relative to
  implementation effort. Cite the named branch decision and check body conditions
  before activating conditional work; the ticket validator cannot check them.
  Supporting research does not activate additional experiments. A later fork needs
  a fresh routing decision, not silent reuse of a completed selection.
- When a finding (including an informative negative result), research direction or
  scope change, or concept appears significant enough for the owner's blog,
  proactively inform the owner. Briefly explain why it merits publication and link
  the relevant evidence, report, or decision tickets; distinguish measured findings
  from hypotheses and conceptual proposals. Flag substantive developments rather
  than routine engineering progress. We will prepare a blog post and an accompanying
  report for publication together; this notification does not itself authorize
  publishing. Continue the authorized research work while awaiting the owner's response.

## Experimental rules

- Use Python/PyTorch. Keep the initial sensory projection fixed.
- Keep transient hidden state, persistent parameters, and environment ground truth separate.
- Prediction/imagined rollouts must not modify persistent parameters.
- Evaluation cannot pass hidden world states or correct future observations into free rollouts.
- Give every result its configuration, seed, source commit, source fingerprint, software versions,
  numerical settings, data exposure, parameter/storage counts, timing, and compute estimates.
- Separate train, development, and test random streams. Tune on development only.
- Use competent mandatory baselines with comparable observations, tuning opportunity,
  and declared total resources. Report all required comparisons, including stronger
  simpler alternatives. Count readouts, external memory, replay, supplied patterns,
  active states, and offline fitting; state mismatches rather than claiming perfect matching.
- Use multiple fixed seeds. Match uncertainty estimates to independent experimental
  units; correlated timesteps are not independent replicates. Report guardrail
  uncertainty as well as the primary endpoint, including failed runs and exclusions.
- Compare grounded one-step error with free multistep error, switching, and perturbation responses.
- A tanh bound is not evidence of recovery toward a trajectory or useful attractors.
- A scripted bank swap or state copy is not evidence of cue-driven attraction.
  Record the supplied/learned status of cues, basins, correspondence, role labels,
  schedules, and controllers. Count every active state, cloned weight, and coupling.
- Support sharing claims with the protocol's causal controls, not activation overlap
  alone. Separate persistent acquisition from transient adaptation by testing after
  a declared state reset; count distinct grounded observations separately from replay
  and updates. Better prediction alone does not establish control or compositionality.
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
