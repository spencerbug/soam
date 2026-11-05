# Conditional research paths

Adopted refinement: 2026-11-05, following the owner's request to replace an apparent
linear implementation programme with result-dependent experimental forks. This
refines [v0.3](RESEARCH_SPEC_V0_3.md); no experimental result or branch is selected yet.

The [scientific review](SCIENTIFIC_REVIEW_2026_11_05.md) adds proposed quantitative
criteria and changes the default information-gain order to E1 useful dynamics,
E2 rapid retained acquisition, then E3 active disambiguation. These are conditional
experiments, not three automatically authorized implementation stages.

## Small common starting point

SOAM-047 defines the minimum contract; SOAM-049 freezes one recall/transition pilot;
SOAM-048 implements only the runner support needed for that pilot and a tiny second
fixture demonstrating reuse. SOAM-050 implements the selected candidates and
SOAM-051 measures them. Implementing an extensible interface does not require
implementing the full backend catalogue or either application.

The first question is whether shared recurrent units yield a practically meaningful
benefit at a declared resource budget. Default primary endpoint: held-out
action-conditioned transition error. Feature recall retention and interference are
guardrails. SOAM-049 freezes numerical margins, uncertainty/precision rules, seed
counts, tuning limits, and budget comparisons before fitting. Shared activity alone
is insufficient. Fixed sensing and supplied structure isolate this question;
online learning, concurrency, and handover follow only on a selected branch.

## Results determine the next experiment

SOAM-052 judges the scientific claim. SOAM-059 selects the next experiment from the
complete pilot evidence. Both depend on SOAM-051; SOAM-059 deliberately does not
depend on a positive SOAM-052 decision. A negative finding can motivate further
research without becoming a successful gate.

| Observed result under frozen criteria | Sharing-gate interpretation | Candidate next fork | What stays deferred |
| --- | --- | --- | --- |
| Meaningful primary benefit, retention guardrails, and causal shared-unit evidence | Proceed for useful sharing in this task only | Prefer minimal acquisition SOAM-039; alternatively active disambiguation SOAM-053 or a specifically justified concurrency fork | All unselected experiments; acquisition and integration claims |
| Stable recurrence and an adequately precise absence of meaningful benefit | Stop the tested benefit claim, or revise only with a specific confound | Simpler separated/ordinary reference for an application, or stop; recurrent attention only with a concrete explanatory hypothesis | Shared-architecture superiority and automatic topology sweeps |
| Recall/transition benefit accompanied by destructive cross-function interference | Revise or stop according to frozen guardrails | One bounded partial-overlap/sparsity or coupling diagnostic with fixed total capacity | Concurrency, learning, and control until the issue is resolved |
| Recall works but directional transitions fail | Revise directional mechanism | One asymmetric-update/action-conditioning diagnostic; optional SOAM-045 if its retrieval mechanism addresses the failure | Extra encoders, skill libraries, and broad application implementation |
| Invalid numerics, leakage, unmatched information, or insufficient precision | Inconclusive; no claim passes | Repair the identified defect or run only prespecified additional evidence collection with fresh confirmation data | Architecture selection from unreliable scores |
| All credible candidates fail at the allocated budget | Stop the tested scope | Archive failure and choose a genuinely different bounded question in a fresh decision, or end this line | Repeated unbudgeted tuning and hidden capacity growth |

These outcomes are classifications, not predictions. Protocol design must turn them
into non-overlapping or explicitly prioritized numerical rules. Validity checks come
first, then guardrails, then benefit/precision. Mixed outcomes must be reported;
uncertain estimates must not be called equivalence or evidence of no benefit.

## Selecting and activating a fork

The SOAM-059 record must name one exact next protocol or experiment, its motivating
evidence, candidate subset, budget, stopping rule, and deferred alternatives. At most
one experimental continuation is selected at a time. Small read-only literature or
protocol work can support that selection; it does not activate implementations.

- **Concurrency:** SOAM-037 requires both useful-sharing proceed (SOAM-052) and
  explicit selection (SOAM-059). It is now the first concurrent binding/handover
  extension. SOAM-023 proceeds only if its measured states and handover conditions
  are usable; a failed concurrency study does not invalidate the narrower pilot.
- **Minimal acquisition:** SOAM-039 requires the platform contract and explicit
  selection; SOAM-044 implements its bounded rules, SOAM-040 measures acquisition
  and retention, and SOAM-041 reviews the evidence. Skills, concurrent handover, and
  the full SOAM-011/012 replay/shadow stack are not prerequisites. A negative sharing
  result may select a labeled alternative learner.
- **Active disambiguation:** SOAM-053 requires the platform contract and explicit selection.
  A negative sharing result may motivate testing conventional/separated dynamics
  here. Its own protocol decision precedes SOAM-054/055. Its first test crosses frozen-memory models and supplied
  active/fixed sensing policies. Failure calls for a bounded belief/policy diagnostic,
  not automatic full SLAM construction.
- **Learning module:** SOAM-056 is a later extension requiring selection and narrow
  SOAM-041 acquisition evidence, then its own protocol before SOAM-057/058.
  Failed acquisition does not automatically justify consolidation or extra capacity.
- **Alternative dynamics:** SOAM-045 is selected only for a specific retrieval/cue
  or transition limitation. Partial-overlap, coupling, and other corrective studies
  receive new IDs and versioned protocols when selected; they are not all prebuilt.

Application paths remain independent of a *positive* sharing gate and the full SOAM
integration chain. They are conditional alternatives, not automatic next stages.
Successful application scores do not pass unrelated sharing, composition, or
continual-learning gates.

## Branches after later results

| Evidence point | Positive or narrower useful result | Negative or inconclusive result |
| --- | --- | --- |
| SOAM-037 concurrency/handover | Test control only under the demonstrated binding and sensing limits | Preserve single-state result; select one binding/coupling diagnostic or another application |
| SOAM-024 control | Reliable search may motivate SOAM-025 efficiency study | Separate model failure from search/controller failure before another experiment |
| SOAM-038 skills | Test reuse within demonstrated applicability limits | SOAM-026 may retain search-only control with an explicit negative skill-transfer finding |
| SOAM-040/041 acquisition | Retained grounded improvement permits selecting active behavior or a module extension; organization separately requires useful sharing | One scoped write/credit diagnostic, or read-only use with the learning claim stopped; SOAM-042 remains unready |
| SOAM-042/043 organization | Select learned organization if supported; fixed organization/replay may also support a limited integration control | If neither retains useful behavior, stop/revise and keep integration unready |
| SOAM-055 or SOAM-058 application | Propose one generalization study or a separately scoped integration review | Diagnose the specific failure once, prefer the simpler control, or stop; no automatic second application |

## Dependency and stopping rules

SOAM-059 selects only the next fork, not an entire multi-experiment programme. After
E2 or E3, allocate a fresh routing decision and explicitly update the chosen next
ticket edge; do not silently amend a completed selection or treat an old selection
as blanket authorization. Full integration keeps its original empirical gates.

Frontmatter `depends_on` retains AND semantics. Named fork selection and evidence
conditions live in ticket bodies and are mandatory in addition to dependencies.
The validator checks the DAG and metadata, but cannot verify scientific conditions;
reviewers must cite the branch record before promoting a conditional ticket to ready.
Unselected forks remain backlog, not blocked. No new ticket-schema fields are needed.

A completed revise/stop decision never unblocks its children. For a corrective
experiment, allocate a fresh protocol decision depending on the completed evidence
experiment, with the failed gate cited in its body. On successful correction, create
a fresh empirical review and explicitly revise only the selected downstream edges.
Retain old decisions and reports; never change a negative outcome to proceed merely
to make the graph runnable. Routine gate review needs no extra human permission.

Allow at most one diagnostic follow-up per pilot failure mode in the initial
allocation. Its finite compute/data budget must be set before starting; further
iterations require a fresh evidence-based decision. Never reuse confirmation data
as unseen evaluation, expand capacity silently, or run every proposed branch.

This revision changes planning only. Existing frozen protocols, code, configurations,
reports, negative findings, and completed tickets retain their original meanings.
