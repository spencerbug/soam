---
schema_version: 2
id: "SOAM-031"
title: "Plan research on compositional dynamical motifs and learned pattern detectors"
type: "research"
status: "backlog"
priority: "P2"
recommended_thinking: "xhigh"
milestone: "M5"
work_packages: ["WP-08"]
hypotheses: ["H5"]
depends_on: ["SOAM-052"]
labels: ["type:research", "priority:P2", "milestone:M5"]
assignees: []
created: "2026-10-25"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-031: Plan research on compositional dynamical motifs and learned pattern detectors

## Recommended thinking

**xhigh** — Distinguish learned internal reuse from supplied structure, and design causal tests of composition without presuming attractors or explicit references are necessary.

## Problem / hypothesis

H5 already covers behavioral composition and transfer. The proposed extension asks
whether reusable internal dynamical patterns explain those abilities, including
attractor structures where attraction is independently demonstrated. Pattern
similarity alone does not establish functional reuse or compositionality.

Originally parked on 2026-10-25 and moved after handover in v0.2, this discussion
is now scheduled after the v0.3 shared-population decision. The shared low-rank model remains a historical control, not a
mandatory final substrate. This ticket plans composition mechanisms without
implementing them or treating scope adoption as a scientific result.

Specification: [§12 and §20](../docs/RESEARCH_SPEC.md). Related work:
[composition benchmark](SOAM-016-composition-transfer.md),
[identity/timescales](SOAM-017-identity-timescales.md),
[Gate 5](SOAM-018-gate-5.md), and [literature map](SOAM-030-theory-literature.md).
Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.3 shared-population revision — 2026-11-05

The shared-population empirical gate now precedes this later composition study. Prefer motifs/assemblies that share neurons across features, relationships, and action relations. Detector/readout modules do not imply dedicated memory populations; compare any explicit binding or separated detector architecture as an alternative.

The [v0.3 scope](../docs/RESEARCH_SPEC_V0_3.md) governs current topology and
platform use; earlier scope notes below retain dependency history only.

### Historical v0.2 scope revision — 2026-11-01

The [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md) adopts the broader embodied scope separately in SOAM-032. This ticket remains unfinished, bounded composition research. Revisit detector/feedback and reference alternatives after the handover gate identifies a usable population organization; do not let this task block the first cutover experiment.

### Bounded work

- Plan a dated research-spec amendment and corresponding documentation/ticket updates; preserve the original v0.1 provenance and distinguish proposals from adopted mechanisms.
- Compare implicit reuse in a shared recurrent substrate with context-gated attractor linking and explicit reference/binding mechanisms. Review Davis's shared memory, separate recovery/transition connections, and programmed control rather than treating it as independent Hopfield networks per context.
- Include the owner's proposed pattern detectors: small, potentially overlapping populations that learn to recognize activity patterns or temporal motifs in the larger recurrent population, then feed activity back into it. Investigate recognition, reactivation, hierarchical combination, and whether these provide useful implicit references.
- Separate slow learning of detector/feedback weights from their activity timescale. Consider temporal evidence for motion patterns, sparse/competitive selection, bounded feedback, and representation drift. Begin from a fixed total capacity; growth is not assumed.
- Distinguish detectors that merely label existing dynamics from mechanisms that causally support reusable computation. Compare passive detectors, active feedback, and a matched-capacity ordinary recurrent baseline; distinguish supplied context labels from inferred selection.
- Planning only: do not implement detectors, references, new attractor substrates, or experiments in this ticket. Do not assume biological equivalence or declare explicit references necessary.

## Acceptance criteria

- [ ] Plan causal overlap/connectivity interventions and held-out cross-function recombination, distinguishing shared units from shared weights and supplied pattern/role labels.

- [ ] Define separate claims and falsification conditions for pattern similarity, functional reuse, held-out composition/transfer, and attractor-level composition under specified input conditions.
- [ ] Propose a bounded protocol combining internal diagnostics with causal perturbation/ablation and held-out recombination; distinguish zero-shot composition from faster acquisition and control for common inputs, collapse, and leakage.
- [ ] Specify how a detector learns useful structure without primitive labels, how feedback is grounded, and how self-excitation, duplication, drift, and loss of object/role information would be detected.
- [ ] Review primary sources, identifying supplied control/binding versus learned organization; record open questions and allow a recommendation to defer or reject the extension.
- [ ] Produce a dated planning note, an explicit proposed spec/docs amendment, and bounded follow-up tickets or documented deferral; reconcile with existing H5 work without silently changing gate outcomes or dependencies.

## Metrics / evidence

Planning evidence, not new measured results. Propose motif-selectivity and causal
reuse measures alongside withheld-composition error, transfer, retention, stability,
and resource cost. Define seed/split, uncertainty, and parameter/data/compute matching
requirements before future trials. Suggested eventual note: `docs/COMPOSITION_RESEARCH_PLAN.md`.

Starting sources for focused review:
[Davis et al. (2021)](https://www.cs.umd.edu/~grpdavis/papers/compositionality.pdf),
[Driscoll et al. (2024)](https://www.nature.com/articles/s41593-024-01668-6), and
[Brain computation by assemblies of neurons (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7322080/).
These motivate comparisons, not evidence that SOAM already supports these mechanisms.

## Dependencies

- [SOAM-052](SOAM-052-shared-population-gate.md) — required completed prerequisite; decision prerequisites require proceed for this scope.

## Scientific review disposition — 2026-11-05

**Future capability** (R9) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Future D4 composition/identity evidence. Distinguish withheld recombination, interpolation, memorized episodes, and faster acquisition; causal recurrent motifs do not themselves prove composition. Preserve existing prerequisites and use the review quantitative targets only after a dedicated protocol decision.

## Completion record

Not started. Discussion captured on 2026-10-25. The broader v0.2 scope amendment
is recorded in SOAM-032; this ticket’s source review, detector/composition protocol,
and acceptance criteria remain unfinished.
