---
schema_version: 2
id: "SOAM-086"
title: "Specify a bounded recurrent associative retrieval pilot"
type: "decision"
status: "done"
priority: "P0"
recommended_thinking: "xhigh"
milestone: "M2"
work_packages: ["WP-02", "WP-03"]
hypotheses: ["H2", "H3"]
depends_on: ["SOAM-047", "SOAM-085"]
labels: ["type:decision", "priority:P0", "milestone:M2"]
assignees: []
created: "2026-11-17"
updated: "2026-11-18"
github_issue: null
decision: "proceed"
---

# SOAM-086: Specify a bounded recurrent associative retrieval pilot

## Recommended thinking

**xhigh** — Isolate actual iterative associative retrieval from direct-map readout,
choose a competent memory and acquisition rule, and separate the common-substrate
motivation from claims of learned specialization, attraction, and self-organization.

## Problem / hypothesis

The [owner's fresh routing decision](../docs/requests/recurrent_retrieval_2026_11_17.md)
selects this next direction after [Study D](../reports/STUDY_D.md). D's FAST candidate
was a direct linear read; its failure does not test nonlinear recurrent completion.
Can an iterative memory acquire associations that survive reset and sequential
learning, and does recurrent settling causally improve useful retrieval?

Retrieval using a substrate compatible with tracking could later permit learned
functional specialization and adaptive interaction. This pilot can establish a
component capability, not that future organizational hypothesis.

## Scope

The November 18 [Study D-R1 handoff prompt](../docs/proposed-studies/STUDY_D_R1_RECURRENT_RETRIEVAL.md)
names this first recurrent-retrieval follow-up and specifies the proposed execution
assignment. Its candidate constraints, primary contrast, margins and budget are
inputs to this protocol review, not frozen criteria or an allocation. The owner instructed execution on November 18 ("Begin study D1-R1", interpreted
as D-R1). The protocol is accepted for implementation; this does not renew the numerical allocation.

- Design one bounded recurrent-retrieval comparison with a fixed action core.
- Define the persistent write rule, transient settling law, cue treatment, stopping
  rule, and exact interface from retrieved association to action prediction.
- Keep KV and a competent direct-map reference; define an intervention on settling
  that isolates recurrence rather than changed exposure or extra storage.
- Use full/partial cue conditions as a diagnostic within this selected question.
- Count supplied patterns, encoders/projections, memory, gates, active states and
  inner updates; avoid choosing an incompetent capacity regime for the candidate.
- Preserve D0–D2 outcomes. D3/D4, E0, mutual coupling, learned role allocation,
  autonomous organization and broad scaling searches remain outside this ticket.

## Acceptance criteria

- [x] Define a competent recurrent associative candidate and acquisition mechanism,
  with observability, reset/no-write and data-separation contracts.
- [x] Freeze primary endpoint, acquisition/retention and false-recall guards,
  causal settling comparison, mandatory controls, uncertainty/precision and stop rules.
- [x] Declare finite tuning inventory, independent train/development/confirmation
  streams and total numerical CPU/wall/RSS/artifact ceilings before trials.
- [x] Distinguish reliable component retrieval, a causal settling contribution,
  competitive resource cost and unsupported outcomes without requiring a KV win.
- [x] Record proceed/revise/stop with rationale and proposed implementation scope;
  passing protocol review does not establish the scientific hypothesis.

## Metrics / evidence

Review the D protocol/report/source and relevant primary associative-memory work.
Candidate measurements include post-reset completion, free prediction from recall,
sequential retention, false acceptance and resource cost. Freeze the exact primary
quantity and margins in the protocol. Existing D results cannot become unseen
confirmation data; its old numerical ceiling is not a renewed allocation.

## Dependencies

- [SOAM-047](SOAM-047-platform-contract.md) — done/proceed for the common platform contract.
- [SOAM-085](SOAM-085-study-d-decision.md) — done/proceed for acceptance of scoped D evidence.

## Branch conditions

The November 17 owner request is the new selection. It replaces the unselected
standalone full-versus-partial D2 diagnostic as the next proposed experiment while
retaining that diagnostic distinction within protocol design. SOAM-052 remains
stop; no useful-sharing or self-organization gate is passed. No implementation or
confirmation is activated until this protocol decision is done with proceed.

## Completion record

**November 18: proceed with the [D-R1 v1 contract](../docs/STUDY_D_R1_PROTOCOL.md)
and [manifest](../docs/protocols/study_d_r1_v1.json), for implementation only.**
The owner's “Begin study D1-R1” starts the selected D-R1 follow-up. SOAM-047 and
SOAM-085 are done/proceed, and their scoped outcomes and SOAM-052 stop remain intact.

Reviewed D's protocol, report, decision, manifest and actual acquisition source:
FAST is a direct delta read; REG is a masked linear solve. Chose one symmetric
projection-rule memory, with an explicit incremental projector derivation and a
fixed real-valued threshold encoding. The accessible
Personnaz et al. author paper (section 2, equation 3) verifies the projector form;
the incremental residual update is explicitly derived, not confused with its
orthogonal-pattern approximation. Publisher PRA full text was restricted.
Implementation must independently verify the stated algebra/energy invariants. This is a competence-motivated design, not a
claim of demonstrated competence. The frozen development screen can stop the study.

The seven arms include a same-weights one-cycle intervention and REG-LIFT to expose
encoding confounds. The protocol freezes acquisition/retention and independent
false-recall/coverage guards, one primary contrast, all REG/KV comparisons, a
12-quantity adjusted root-bootstrap family, finite settings/seeds, 16 core-fit
attempts, stopping rules and an 8 MiB per-arm persistent ceiling. Ten-root precision
and degenerate empirical intervals are explicit limitations. The fresh proposed
7200 CPU / 14400 wall seconds and 2 GiB RSS/artifact allocation awaits owner acceptance;
no numerical run is authorized by the old D ceiling.

Baseline checkout `f325d26` was clean before documentation changes. `uv run pytest`
passed **303 tests in 21.14s**; no existing source code was modified. Qwen's bounded
bulk-document extraction timed out after 360 seconds; no worker findings or patches
were accepted, and relevant evidence was checked directly. No fit, development,
calibration or confirmation stream was generated. `uv run python scripts/check_tickets.py` validated **88 tickets and two templates**.
`git diff --check` passed. A static manifest audit checked dimensions, independent
roots, the 16-fit/12-writer inventory and persistent sizing; all **465** local links
in changed/new Markdown resolved. Historical source and evidence are unchanged.
Manifest SHA-256: `7376ceb643b50820d9b2d15fa4243aaa657b03cf183dba05d1949c756f60c8bb`.

[SOAM-087](SOAM-087-recurrent-retrieval-harness.md) is the next eligible engineering
package; its numerical fixture remains contingent on explicit allocation acceptance.
No later branch or empirical gate is activated and no remote publication occurred.
