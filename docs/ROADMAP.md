# Work packages and completion criteria

| Package | Status / criterion |
| --- | --- |
| WP-00 | Initial implementation: deterministic generator, config runner, provenance, tests, logs, comparisons, plots. Confirm numerical repeatability. |
| WP-01 | Initial implementation: additive/gated/low-rank/shared and independent baselines, switching and perturbations. Scientific gate remains evidence-dependent; see report. |
| WP-02 | Pending: local writes outperform no-adaptation on held-out changes with retention and multistep checks. |
| WP-03 | Pending: per-context before/after interference and forgetting metrics validated on controlled changes. |
| WP-04 | Pending: fixed/random/sensitivity masks at matched adaptation and sparsity. |
| WP-05 | Pending: learned scope improves retention at matched new-task accuracy while allowing transfer. |
| WP-06 | Pending: grounded replay baseline with reported compute and retention. |
| WP-07 | Pending: validated shadow updates; learned refinement compared with replay. |
| WP-08 | Pending: withheld compositions and transfer distinguish reuse from interpolation. |
| WP-09 | Synthetic fixed encoder only; pretrained frozen encoder comparisons deferred. |
| WP-10 | Initial synthetic assimilation only; partial/ambiguous sensory grounding deferred. |
| WP-11 | Pending: candidate search with no persistent writes during imagination. |
| WP-12 | Pending: learned proposals compared with search/reactive baselines. |
| WP-13 | Pending: long sequential embodied benchmarks with acquisition, retention, transfer, capacity. |

Dependencies and the complete research program are in `RESEARCH_SPEC.md` §18.
Do not mark a scientific hypothesis supported solely because implementation is complete.
