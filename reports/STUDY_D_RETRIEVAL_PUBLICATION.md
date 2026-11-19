# D-R1 and D-R2 publication — November 19, 2026

Published the authorized joint article and companion report covering D-R1 and its
D-R2 follow-up:

- [A Stored Memory Still Has to Be Retrieved](https://spencerbug.github.io/blog/soam-retrieval-and-decoding/)
- [Recurrent Retrieval and Exact-Code Decoding](https://spencerbug.github.io/research/soam-retrieval-and-decoding/)

Site repository: `spencerbug/spencerbug.github.io`. Publication commit:
`3c0b27253804bdd065bbd637d0cc5ada26df1395`.

The article separates preserving a stored code, reaching it from a partial cue,
and decoding it into a useful prediction. It explains PH768's 512 appearance and
256 relationship units and distinguishes ordinary recall from the privileged,
evaluation-only exact-code diagnostic. The report records the protocols,
mandatory controls, uncertainty, resources, source fingerprints and limitations.

D-R1's additional-settling benefit remains 2.14 percentage points, adjusted
interval [0.98, 3.66], precisely below its five-point practical margin. Its
sequential-recall, retention and accepted-wrong guards remain failed. D-R2's
22.37-point exact-code versus ordinary-recall gap has adjusted interval
[15.36, 29.02]; its width exceeds the frozen ten-point precision cap, so the
formal diagnosis remains **inconclusive**. The publication does not present the
different evaluation inventories as evidence of improvement between studies.
KV remains the scoped conventional reference; no successor experiment is selected.

The nine published files comprise the two new pages, shared study navigation,
two research indexes, dated follow-up notes on the earlier Study D article and
report, and unchanged copies of the D-R1 settling and D-R2 decoding figures.
No downloadable source or raw-data bundles were published. No new scientific
trials, fits, bootstrap estimates or gate decisions were introduced.

## Verification

- `bundle exec jekyll build` with the site's locked dependencies: passes.
- `python3 scripts/check_inline_mathjax.py`: passes.
- `node scripts/check_review_annotations.cjs`: all 12 DOM scenarios pass.
- Real Chrome checks of both local and live pages at 390 and 1280 pixels,
  light and dark: all eight cases in each environment return HTTP 200, load
  the figures, preserve annotations, and show no JavaScript errors or
  page-level horizontal overflow. Screenshots were visually reviewed.
- Both live research indexes link to the new article and report.
- [GitHub Pages deployment](https://github.com/spencerbug/spencerbug.github.io/actions/runs/44556443045)
  and [MathJax validation](https://github.com/spencerbug/spencerbug.github.io/actions/runs/44556444220)
  completed successfully.
- All nine published file hashes match the local site checkout, which was
  fast-forwarded to the publication commit without overwriting existing work.
- All 110 D-R1 and 116 D-R2 frozen source hashes still match. Original protocols,
  measured reports, archived artifacts and historical decisions remain unchanged.
- `uv run python scripts/check_tickets.py`: validates 94 tickets and two GitHub
  templates. `git diff --check` passes.

Exact file hashes, deployment identifiers, browser evidence and the publication
receipt are retained locally under `runs/publications/retrieval-2026-11-19/`.
A bounded Qwen extraction was checked against the owning protocol and measured
evidence; incorrect citations and missing guardrail coverage were corrected
during primary review. No SOAM executable code changed.

## Evidence

- [D-R1 report](STUDY_D_R1.md) and [decision](STUDY_D_R1_DECISION.md).
- [D-R2 report](STUDY_D_R2.md) and [decision](STUDY_D_R2_DECISION.md).
- [Earlier Study D publication](STUDY_D_PUBLICATION.md).
