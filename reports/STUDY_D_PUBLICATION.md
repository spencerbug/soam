# Study D publication — November 17, 2026

Published the authorized D0–D2 article and companion report:

- [Learning Quickly Is Not the Same as Remembering](https://spencerbug.github.io/blog/soam-study-d-acquisition-and-retention/)
- [Persistent Acquisition and Sequential Retention](https://spencerbug.github.io/research/soam-study-d/)

Site repository: `spencerbug/spencerbug.github.io`. Publication commit:
`5e8faf22fb8dc26e89fab22691baccd60a20db13`. Mobile table formatting follow-up:
`ed749bdaf9628912514a76e301dd77523be8f3ad`.

The article distinguishes isolated acquisition from sequential retention, includes
the stronger KV result and unequal actual storage, and states that FAST is a direct
linear read rather than iterative Hopfield retrieval. The new old-object accuracy
figure renders archived root results and adjusted intervals; no new scientific
trial, fit, bootstrap estimate, or outcome was introduced. Original D reports,
protocol, source snapshot and gate decisions remain unchanged.

The later owner-selected recurrent-retrieval direction is explicitly a new protocol
question. Its homogeneous-substrate motivation and possible future learned roles
are captured in the [routing record](../docs/requests/recurrent_retrieval_2026_11_17.md),
[hypothesis ledger](../docs/HYPOTHESES.md#population-cooperation-and-retrieval-scaling),
and ready [SOAM-086](../tickets/SOAM-086-recurrent-retrieval-protocol.md). D3/D4 and
broader coupling/scaling work remain deferred.

## Publication boundary

Automatic approval review rejected a larger public upload containing the frozen
source ZIP and numerical evidence bundle because that disclosure exceeded explicit
article authorization. A separate user question remains pending. The accepted
publication includes the article, companion report, three figures, styling and
navigation updates. It excludes downloadable source/data archives and does not
claim that those downloads are available.

The prepared full package and publication QA are retained locally under
`runs/publications/study-d-2026-11-17/`. The source ZIP was checked against all 102
frozen source hashes before being prepared. This preparation does not authorize its
public release.

## Verification

- `python3 scripts/check_inline_mathjax.py`: passes.
- `bundle exec jekyll build` using the site's locked dependencies: passes.
- `node scripts/check_review_annotations.cjs`: 12 DOM scenarios pass.
- Real Chrome checks of both live pages at 390 and 1280 pixels, light and dark:
  all eight cases return HTTP 200, load the figures, preserve annotations, and
  show no JavaScript errors or page-level horizontal overflow.
- Visual review identified and corrected mobile table word/number splitting;
  tables scroll within their containers while prose hashes remain wrappable.
- GitHub Pages deployment and MathJax validation succeeded for the publication.
- The local blog checkout was fast-forwarded without overwriting existing work.
- SOAM ticket validation passes 87 tickets and two templates. No SOAM executable
  code changed; the historical 303-test result remains the study's pre-run record.

Exact site file hashes, deployment identifiers and browser evidence are retained
in the local publication receipt and QA directory. A Qwen extraction with incorrect
thresholds and missing citations was rejected; claims were checked against the
owning protocol, source and archived results directly.
