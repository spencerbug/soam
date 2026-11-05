---
schema_version: 2
id: "SOAM-018"
title: "Gate 5: assess compositional reuse rather than memory maintenance"
type: "decision"
status: "backlog"
priority: "P2"
recommended_thinking: "xhigh"
milestone: "M5"
work_packages: ["WP-08"]
hypotheses: ["H5"]
depends_on: ["SOAM-017"]
labels: ["type:decision", "priority:P2", "milestone:M5"]
assignees: []
created: "2026-10-25"
updated: "2026-11-05"
github_issue: null
decision: null
---

# SOAM-018: Gate 5: assess compositional reuse rather than memory maintenance

## Recommended thinking

**xhigh** — Evaluate the strongest self-organization claim by separating composition and transfer from memory maintenance.

## Problem / hypothesis

H5 tests composition and transfer. Better retention alone cannot support reuse, and composition supplied through explicit bindings does not by itself establish self-organization.

Specification: [research plan §12, §19](../docs/RESEARCH_SPEC.md). Apply the [common completion requirements](README.md#completion-requirements).

## Scope

### v0.2 scope revision — 2026-11-01

The [v0.2 specification](../docs/RESEARCH_SPEC_V0_2.md) separates reusable computation from learned organization. A proceed may establish bounded composition with explicit scaffolding while leaving self-organization unsupported. Require causal ablations and the scaffold ledger; SOAM-043 separately reviews learned organization before integration.

### Bounded work

- Review withheld composition, new-task transfer, identity, and timescale experiments.
- Separate supported forms of generalization from failures and leakage concerns.

## Acceptance criteria

- [ ] Require reliable withheld-composition or related-task gains under the preregistered comparison plan.
- [ ] Record which baselines/ablations explain the gain and disclose unmatched budgets.
- [ ] Record proceed/revise/stop and restrict claims to the tested task families.
- [ ] If transfer fails, create a targeted objective/representation/inductive-bias revision ticket and retain the memory-maintenance result separately.

## Metrics / evidence

Gate 5 evidence for composition/transfer, with effect sizes, uncertainty, and failure analysis.

## Dependencies

- [SOAM-017](SOAM-017-identity-timescales.md) — Test identity preservation and reusable temporal structure

## Scientific review disposition — 2026-11-05

**Future capability** (R9) in the [scientific review](../docs/SCIENTIFIC_REVIEW_2026_11_05.md). Future D4 composition/identity evidence. Distinguish withheld recombination, interpolation, memorized episodes, and faster acquisition; causal recurrent motifs do not themselves prove composition. Preserve existing prerequisites and use the review quantitative targets only after a dedicated protocol decision.

## Completion record

Not started. Add implementation/report links, exact validation commands and outcomes,
configuration/seed/source identities, and limitations when work is completed.
Set frontmatter `decision` to `proceed`, `revise`, or `stop` only when the decision is documented.
