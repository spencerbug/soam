# Codex prompt — Study D: Persistent associative acquisition after C

**Status:** proposal only. Select via a fresh SOAM routing decision before execution.

## Mission

Act as the principal research investigator for SOAM. Design, implement, test and report one bounded Study D on this question:

**Can an agent acquire unfamiliar object-specific sensorimotor relationships from a limited number of grounded observations, retrieve them after transient-state reset, and preserve earlier learned relationships without unacceptable interference?**

Investigate whether persistent associative storage or fast recurrent plasticity earns a practical advantage over conventional learned maps/online regression. Do **not** assume a Hopfield, a learned write gate, or multiple neural populations is mandatory.

Read the current checkout AGENTS.md, protocol/ticket rules, frozen Study A/B/B2/C reports and decisions, and current source provenance. Public evidence: https://spencerbug.github.io/research/soam-study-c/ and links in README.md of this directory. The checked-in GitHub code may lag the local study source; verify before editing. Never modify historical decisions or treat C as a write-memory result.

## Interpretation of Study C

Study C's TWO16 shares one fitted ordinary recurrent transition/correction function across two **separate transient state instances**. It improves Brier over PC16 and PC32 under supplied two-regime ambiguity, but does not demonstrate storing new object knowledge, plastic recurrent attractors, shared neurons, or a practical probability advantage over ADAPT1-M. ADAPT1-C remains a strong compact conventional comparator. Use a minimal tested inference reference rather than requiring the TWO16 mechanism for acquisition. Multi-hypothesis inference may be a secondary condition after the basic memory question is answered.

A/B/B2 retain predict -> score prior -> correct; default extra settling zero; no persistent parameter changes during free prediction. B2's ADAPT1 channel-disagreement rule depends on redundant linear observations and is not a general learned reliability mechanism.

## Scientific hypotheses

- D-H1 (persistent acquisition): memory-enabled models acquire previously unavailable object-specific associations and use them following a complete reset of transient recurrent state and nonpersistent caches.
- D-H2 (reuse): a shared slowly trained dynamics core plus instance memory reuses action-conditioned transformations better than re-fitting an entire independent model for each object under declared memory/training budgets.
- D-H3 (write selection): reliability/novelty-aware writing reduces false association and interference compared with a well-tuned simple always-write policy.
- D-H4 (mechanism): gated/low-rank recurrent fast weights add measurable value over an explicit key-value store, local regression, or compact explicit map.
- D-H0 (simplicity): the structured conventional memory provides equal or better useful acquisition at lower overall cost.

## Minimal learnable task

Use an object family sharing general action-conditioned observation dynamics but with held-out instance-specific landmark/feature relationships. Freeze the feature encoder initially. Train general dynamics on disjoint object families; supply each new test object only a finite schedule of grounded action/observation records.

A successful model cannot solve the retrieval test using a hidden state that persists through the training-to-query boundary. Reset all transient activity and nonpersistent caches, then issue incomplete cues and withhold a subset of object views/action compositions. Verify that instance-specific information was not encoded in object labels, simulator states, training IDs, implicit provided correspondence, evaluation filenames, or other leakage.

Analytically verify acquisition identifiability: a one-observation task must reveal enough information to distinguish the intended association. Distinguish one-shot, few-shot, cumulative and changed-object cases. Held-out objects and acquisition sequences are independent confirmation units where appropriate.

## Controlled candidate inventory

Start with the smallest meaningful inventory. Include:
1. No-write recurrent inference control, with identical sensory experience and reset.
2. Explicit associative key-value / nearest-neighbor reference with bounded storage and a competent retrieval rule.
3. Online regression/local learned map correction using permitted data; include a structured fitted predictor (FILTER2/ADAPT1-inspired where valid).
4. Fast-weight recurrent correction (e.g. bounded rank-k update to the transition/associative operator), **only** if it can be evaluated against the same acquisition information and fixed total memory.
5. Limited ordinary slow-weight fine-tuning as a disclosed comparison if feasible.

Start with the same simple writing policy for storage mechanisms, then compare always-write, fixed reliability threshold, novelty threshold and one combined policy on a proven competent mechanism. A learned policy requires a diagnosed gap; do not add a trained gate automatically. A history of large residuals may mean model mismatch, new object information, or unreliable observation; large error alone is not proof of valid novelty.

Where reference models differ in representational shape, compare separate parameter, active-state, persistent-memory and inference-compute budgets. All learned projections and controllers count. A bigger or overtrained recurrent memory is not a fair proof against a tiny baseline. A/C source models may need retraining on the new task; no transferred numeric performance guarantee.

## Experimental sequence

**D0 — scientific fixture:** one known general transformation and one learnable novel association. Test exact reset/no-write rules, valid cue recovery, improper simulator access, and parameter integrity.

**D1 — single unfamiliar object:** give a fixed evidence budget, write, reset, retrieve from a partial cue, predict withheld action-conditioned features.

**D2 — sequential accumulation:** acquire several similar objects. After each acquisition, reset and query all earlier objects; measure forgetting and false familiarity.

**D3 — reliability:** inject erroneous grounded measurements or wrong correspondence; test false writes and ability to revise, quarantine or roll back corrupted associations. Distinguish a genuinely changed relationship from a transient fault.

**D4 — fixed-capacity stress:** vary number of associations at equal total persistent bytes, report retrieval cost, collisions and degradation.

Stop after the smallest stage needed to decide the main question; each extension needs an explicit finite budget and frozen criteria. Do not launch consolidation/replay, autonomous organization, multi-object attention, or unlimited architecture search as automatic remedies.

## Outcome metrics and guardrails

Primary: newly acquired, post-reset association accuracy and held-out action-conditioned prediction under a finite grounded-observation budget. Co-primary or guarded old-object retention after sequential acquisition; define practical effects before confirmation. Include strong explicit-memory control.

Report false recall, overconfident wrong retrieval, unknown-object rejection, one/few-shot acquisition curves, retention, interference, storage growth, write/read latency, compute, root/object uncertainty and failures. Include old-model prediction tasks as a non-regression guard.

A model may form a transient correct posterior without modifying persistent memory. A correct output before reset is not persistent acquisition. A no-write imagined rollout must leave persistent tensors/entries byte-identical, verified by tests. Repeated evaluation queries must not become hidden training evidence.

## Scientific procedure

Before training: perform a protocol/observability review, reproduce reference fixtures, pre-register candidate set, independent train/development/confirmation streams, fit roots, selection/uncertainty procedure, practically meaningful gain, retention/robustness guards, memory and compute caps, and stop conditions. Calibrate on development only; freeze before confirmation. Preserve all failed and negative experiments. Record parameter counts, active and retained state, memory, runtime including matrix solves, artifacts, source/config hashes and exact repeat checks. Do not compare correlated timesteps as independent roots.

## Biological/theoretical note

Discuss fast associative plasticity, hippocampal acquisition, three-factor learning, complementary learning systems and consolidation as inspirations, not achieved properties. Any fast-weight update requires a demonstrated memory benefit beyond conventional storage; mere changed recurrent weights do not demonstrate self-organization.

## Required artifacts and decision

Produce a versioned protocol, minimal implementation/tests, provenance, reproducible paired results, retention/interference curves, representative failures, resource Pareto table, scientific report and decision record. Identify which capabilities are supported, unsupported, or untested. Recommend **one** bounded next experiment, if any, without executing it.

**Final question:** Does persistent recurrent plasticity provide an advantage beyond a small structured episodic/associative memory, and what is the cheapest reliable mechanism for learning new object-specific sensorimotor structure after offline training?
