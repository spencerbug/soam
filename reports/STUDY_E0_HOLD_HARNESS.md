# E0-HOLD harness and preflight

SOAM-099 implements the [frozen follow-up](../docs/STUDY_E0_HOLD_PROTOCOL.md).
The [receipt](study-e0-hold/preflight.json) records code commit `6733775`, complete
source/config/protocol hashes, software and resources. Historical E0 source files
remain unchanged; the source-preservation test checks all 148 prior source hashes.

The full pre-change suite passed 339 tests. The final full suite passes **348 tests
in 28.60 seconds**, including nine new E0-HOLD tests. They verify exact SHORT24
fitter equivalence, paired initializations/prefix data, stationary target eligibility,
equal per-episode weighting, absence of moving or observed tail steps, inference
purity, fresh streams, exact repetition, finite inventory and precision/noninferiority
classification. Ruff and the 102-ticket/two-template validator pass. A seed-helper
arity error was corrected during unit testing before any fixture/scientific trial;
the protocol now spells out the existing six-argument seed API.

Command (with `UV_CACHE_DIR=/private/tmp/soam-uv-cache` for the workspace sandbox):
`uv run --offline --no-sync python -m soam.hold.runner fixture --output runs/study-e0-hold-v1`.
All seven eight-update fixture cells complete. Initial parameters pair exactly
within all three neural families; all cells share identical prefix training hashes.
No scientific finding is inferred from these fixture models.

Projected complete use with 2x margin: **1,773.23 CPU seconds, 1,820.38 execution-wall
seconds, 1,191,661,882 artifact bytes**. This passes 80% of the 7,200 CPU / 14,400 wall
ceilings and the 2 GiB artifact limit; observed RSS also passes 2 GiB. The actual
runner enforces cumulative limits within training and evaluation. Seven fixtures,
140 fresh confirmation fits and seven prescribed repeats are the full inventory.

SOAM-100 may now execute confirmation using exactly the frozen .003 learning rate,
600 updates, matched prefixes and 24-versus-128 stationary horizons. There is no
new development search, adaptive change or automatic retry. Results will be owned
by reports/STUDY_E0_HOLD.md and interpreted by SOAM-101.
