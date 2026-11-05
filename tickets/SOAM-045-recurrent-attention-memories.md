---
schema_version: 2
id: "SOAM-045"
title: "Explore recurrent attention within shared populations"
type: "research"
status: "backlog"
priority: "P2"
recommended_thinking: "xhigh"
milestone: "MX"
work_packages: ["WP-01", "WP-08", "WP-10"]
hypotheses: ["H1", "H5", "H6"]
depends_on: ["SOAM-033", "SOAM-047", "SOAM-059"]
labels: ["type:research", "priority:P2", "milestone:MX"]
assignees: []
created: "2026-11-01"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-045: Explore recurrent attention within shared populations

## Recommended thinking

**xhigh** — Determine where attention/Hopfield equivalence supports recurrent
mechanisms, and separate retrieval, grounded state correction, composition, and
routing without inheriting unsupported stability claims.

## Problem / hypothesis

The owner's 2026-11-01 proposal is to explore attention-based associative memories
as an implementation of SOAM's attractor dynamics: outputs cue other memories,
parallel instances remain calibrated before handover, and predictive routing selects
which instance becomes attended. Several instances might share memory matrices
while retaining independent queries and evolving state.

The question is whether this formulation supplies a useful, testable architecture
beyond relabeling the existing Hopfield-style retrieval term. Attention-update
equivalence alone does not establish stability of a full transformer, sensorimotor
tracking, or compositional reuse.

Specification: [SOAM v0.3](../docs/RESEARCH_SPEC_V0_3.md).
Starting contract: [handover protocol](../docs/HANDOVER_PROTOCOL.md).
Related work: [composition planning](SOAM-031-compositional-dynamics-planning.md),
[concurrent instance beliefs](SOAM-037-attention-belief-instances.md), and
[literature map](SOAM-030-theory-literature.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.3 shared-population revision — 2026-11-05

Reframe the candidate as an optional platform backend with overlapping feature/relation/action representations. Serial or parallel independent memory instances remain controls; shared matrices alone are not shared neurons. Use the platform contract for ownership and keep the v1 handover protocol unchanged.

The [v0.3 scope](../docs/RESEARCH_SPEC_V0_3.md) governs current topology and
platform use; earlier scope notes below retain dependency history only.

- Review Ramsauer's update/attention equivalence and recurrence assumptions using
  the primary paper. Distinguish associative-space updates from projected value
  readouts, residual/normalization operations, changing memories, and external drive.
- Specify one bounded recurrent-attention candidate. Compare serial output-to-query
  chaining with parallel persistent instances, shared matrices versus copied weights,
  and separate live state versus a shared-state control. Identify which alternatives
  are algebraically equivalent and which change the dynamics or available information.
- Define cues carrying content, role, and relation information, including any map
  between one module's output and another's query. Distinguish associative chaining
  from composition that preserves instance identity and supports held-out combinations.
- Define pre-calibration through executed actions and sensory prediction-error
  correction of transient state. Keep persistent matrices frozen during evaluation;
  count every live query, state, cache, coupling, and supplied binding. Prevent
  internal predictions from being counted again as independent sensory evidence.
- Separate candidate relevance, evidence-based calibration, computation allocation,
  attended readout, and motor authority. Preserve attended/tracking/primed roles;
  specify how predictive routing avoids starving tracking instances or repeatedly
  reinforcing unsupported candidates.
- Produce a design and evaluation proposal only. Keep SOAM-033's v1 protocol and
  SOAM-034/035 implementation/trial scope intact. Any prototype, new trial, or protocol
  amendment needs a separately bounded follow-up honoring applicable gate outcomes.
  This task does not replace SOAM-031/037 or become their prerequisite.

## Acceptance criteria

- [ ] Specify how the proposed recurrent attention update uses the same units across functions, compare disjoint/cloned-state variants, and avoid extending an attention-update equivalence into an unsupported asymmetric stability claim.

- [ ] Publish a dated design note with verified primary-source references, equations,
  and an explicit boundary between proven equivalence and SOAM-specific hypotheses.
- [ ] Document candidate interfaces and a state/parameter/evidence ownership diagram,
  including output-to-query mappings, sensory correction, independent instances,
  routing decisions, and all declared scaffolding.
- [ ] Propose a bounded comparison against the existing attractor and recurrent
  controls, including serial versus parallel operation, pre-tracking versus cold
  start/equal-history replay, and cue, feedback, and routing ablations. Identify
  redundant comparisons rather than treating equivalent formulas as new evidence.
- [ ] Define falsification criteria for recovery, grounded handover, false confidence,
  identity retention, and held-out composition; specify future seed/split, threshold,
  storage, data-exposure, and compute-budget requirements before any trials.
- [ ] Record a supported recommendation to pursue, revise, or defer the candidate,
  including negative findings and unresolved assumptions. Identify one bounded next
  implementation/experiment if warranted, or document why none is justified.

## Metrics / evidence

Planned artifact: `docs/RECURRENT_ATTENTION_RESEARCH_PLAN.md` (not yet created).
This ticket reviews theory and proposes tests; it makes no new measured claim.
Candidate endpoints include cue recruitment before explicit routing, perturbation
recovery, handover delay/continuity, source retention, grounded versus free prediction,
identity errors, repeated-evidence sensitivity, and active-state/compute cost.
Composition requires held-out role/instance combinations, not retrieval accuracy alone.

Starting primary source: [Ramsauer et al., Hopfield Networks Is All You Need,
v3 (2021), §2 and Appendices A.1/A.4](https://arxiv.org/html/2008.02217v3).
The HTML source became accessible in the follow-up discussion; targeted equation
review does not constitute completion of this ticket or a full proof audit.
Limit additional literature to sources needed to resolve the candidate's concrete
recurrence, feedback, or routing assumptions; reuse SOAM-030's evidence map where available.

## Dependencies

- [SOAM-033](SOAM-033-handover-protocol.md) — required completed prerequisite; decision prerequisites require proceed and the branch conditions below.
- [SOAM-047](SOAM-047-platform-contract.md) — required completed prerequisite; decision prerequisites require proceed and the branch conditions below.
- [SOAM-059](SOAM-059-research-fork-selection.md) — required completed prerequisite; decision prerequisites require proceed and the branch conditions below.

## Branch conditions

Start only if SOAM-059 names recurrent attention as a specific alternative for an observed retrieval/cue or transition limitation. Identify the failed assumption it changes and a finite comparison. This is optional research, not an obligatory platform backend.

## Scientific review disposition — 2026-11-05

**Parallel research investigation** (R8) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Keep as a bounded mechanism investigation conditional on a relevant diagnosed limitation. Review attention/fast-weight equivalence before claiming novelty; do not add this backend to the minimum runner.

## Completion record

Not started. Proposal captured on 2026-11-01. Record the actual reviewed sources,
design-note link, validation commands, limitations, and follow-up recommendation
when the research is performed. No implementation or trial is authorized by adding
this ticket to the backlog.
