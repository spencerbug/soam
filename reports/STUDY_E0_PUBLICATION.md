# E0 and E0-HOLD publication — November 21, 2026

Published the owner-authorized joint article and companion scientific report:

- [A Memory That Moves Must Also Hold Still](https://spencerbug.github.io/blog/soam-stationary-memory-and-navigation/)
- [Stationary Retention, Action Navigation and Local Recovery](https://spencerbug.github.io/research/soam-stationary-memory-and-navigation/)

Site repository: `spencerbug/spencerbug.github.io`. Publication commit:
`b89fa0a2a8c622f1d5d3f6e594f0bdb0514389f6`, following `3c0b272`.
The scientific closeout was already committed as `d105b4f`.

The article explains why holding a pose, predicting action-driven motion and
recovering after a disturbance require independent checks. The report includes
the supplied task structure, model equations, information boundaries, frozen
criteria, all E0 comparisons, all thirteen E0-HOLD confirmatory intervals, complete
descriptive control tables, resources, source identities and limitations.

E0 retains its **inconclusive** NAV32 result: six of seven criteria pass, but the
stationary interval exceeds the frozen precision cap. E0-HOLD retains the
**negative declared joint fix**: the paired stationary gain is 6.635° [5.017,8.805],
while residual error 5.698° [5.259,6.183] precisely exceeds five degrees.
Transverse-ratio degradation [.007312,.062184] crosses the .05 practical margin,
leaving noninferiority unresolved. The article uses the fresh paired baseline
12.332° → 5.698°, not the historical pilot's 13.861° as the causal comparison.

The publication includes GRU32's stationary improvement alongside markedly worse
action prediction, SYM32's poor navigation, and PCA2's strong estimation without
transverse restoration. Passing NAV32's mixed-action degradation guard is not
presented as unchanged performance on every action stream. About 3.32× fitting
CPU and repeated stationary targets are disclosed. The optimization-budget
recommendation remains conditional; hierarchy and coupling are not activated.

Nine files were published through the GitHub connector in one commit: the two
pages, two unchanged archived figures, shared series navigation, two research
indexes, and dated updates on the earlier D-R1/R2 article and report. No source
or raw-data bundles were uploaded. No new scientific fits, bootstrap estimates,
gate decisions or production code changes were introduced.

## Verification

- Jekyll build and `python3 scripts/check_inline_mathjax.py` pass with the site's
  installed dependency versions. Bundler's incidental local platform addition
  was removed; `Gemfile.lock` is unchanged in the publication.
- `node scripts/check_review_annotations.cjs`: all twelve DOM scenarios pass.
- Local Chrome checks cover both pages at 390 and 1280 pixels, light and dark:
  HTTP 200, loaded figures, working annotation controls, no JavaScript errors
  or page-level horizontal overflow. Wide tables retain horizontal scrolling.
  An initial mobile check sampled before MathJax loaded; the check now explicitly
  waits for typesetting. All eight corrected cases pass. The equation was split
  across two lines and both final mobile themes were checked again successfully.
  Screenshots of prose, figures, tables and the equation were visually reviewed.
- Both live research indexes link the article and report. Both deployed figure
  SHA-256 hashes exactly match the original study archives.
- All eight live Chrome cases also pass, including equation typesetting,
  annotations, image loading and page-width checks. Live desktop and mobile
  screenshots were visually reviewed.
- [Pages deployment](https://github.com/spencerbug/spencerbug.github.io/actions/runs/44960598297)
  and [MathJax validation](https://github.com/spencerbug/spencerbug.github.io/actions/runs/44960598731)
  succeeded for the publication commit.
- All nine files in the fetched public commit match the reviewed publication
  hashes. The clean local site checkout was fast-forwarded to that commit.
- All 148 E0 and 153 E0-HOLD frozen source hashes remain unchanged.
- Ticket validation passes for 102 tickets and two GitHub templates;
  `git diff --check` passes. No SOAM executable code changed.

The exact file manifest, hashes, browser checks and publication receipt are local
under `runs/publications/e0-2026-11-21/`. A bounded Qwen extraction did not return
before cancellation; no worker findings were used. Claims were checked directly
against the owning reports, protocols and archived tables. Historical scientific
outcomes and the conditional next-step decision remain unchanged.

## Evidence

- [E0 report](STUDY_E0.md), [protocol](../docs/STUDY_E0_PROTOCOL.md) and
  [decision](STUDY_E0_DECISION.md).
- [E0-HOLD report](STUDY_E0_HOLD.md), [full tables](study-e0-hold/tables.md),
  [protocol](../docs/STUDY_E0_HOLD_PROTOCOL.md) and
  [decision](STUDY_E0_HOLD_DECISION.md).

## November 22 terminology clarification

At the owner's request, “free action” is now **blindfolded action prediction**:
actions are supplied, but sensory observations stop after the initial cue.
**Zero-action drift** supplies zero action and no further observations. The
reports explicitly retain the endpoint definitions: mean sensory NMSE over
64 steps versus absolute pose error after 128 steps, including initialization
error, in degrees. Displacement from the initial pose remains a separate metric.

Site update: `29d7830b8d1bd9267ebabe563b21fce1ef4a6cc0`. It changes the post and
joint report and adds two figures with revised labels. Original figure URLs and
archived PNG/SVG files remain available. Local E0/HOLD reports, decision wording,
plotting labels and table-generation code use the same terminology.
[Module documentation](../soam/navigation/README.md) maps the clearer terms to
the retained `free_nmse`, `free_horizon` and `stationary_deg` identifiers.
The `free` stream identifier also seeds data, so it is unchanged.

Only reporting labels and documentation changed. Eighty archived NPZ inputs
were hash-verified; rendering the original and revised plot blocks produces
exactly identical numerical line coordinates. All table data values are
unchanged. No fitting, inference, bootstrap estimation or gate decision was
performed. The earlier publication commit preserves the original reporting
source versions; the numerical receipts and raw archives are untouched.

Validation: all 348 tests passed before changes; all twenty navigation/HOLD
tests pass after the final changes. An intermediate docstring edit triggered
the historical-source hash guard and was reverted; that guard remains intact.
All 148 E0 and 153 E0-HOLD scientific source hashes still match. Ruff, ticket
validation (102 tickets/two templates), report links and `git diff --check`
pass. Jekyll, MathJax lint, all twelve annotation DOM scenarios and all eight
local desktop/mobile light/dark browser cases pass. The revised figures and
rendered pages were visually checked.

[Pages deployment](https://github.com/spencerbug/spencerbug.github.io/actions/runs/44993407815)
and [MathJax validation](https://github.com/spencerbug/spencerbug.github.io/actions/runs/44993408346)
succeeded. All eight live browser cases pass. Live wording and both revised
figure hashes match the reviewed files; the four published file hashes match
the synchronized local site checkout.

The label-rendering script, exact curve checks, file hashes and browser evidence
are retained locally in `runs/publications/e0-terminology-2026-11-22/`. A bounded
local-worker read timed out; direct source review was used. No worker output
was accepted without verification.
