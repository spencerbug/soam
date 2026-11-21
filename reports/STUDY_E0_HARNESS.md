# E0 v1 harness and resource preflight

SOAM-095 completes the [frozen E0 contract](../docs/STUDY_E0_PROTOCOL.md).
The [machine-readable receipt](study-e0/preflight.json) records source commit
`7168e2e`, source fingerprint `4dd66fc4194336388dc8a96a742d157eab7eceac521112760f385744d5b21622`,
manifest/protocol hashes, software and resource counts. No scientific endpoint is
inferred from eight-update fixture models.

The full pre-change suite passed 328 tests. After implementation, 339 tests passed
in 18.68 seconds; the 11 E0 tests passed again in 0.98 seconds after adding raw
geometry state archival and equal-training-data checks. Ruff and ticket validation
passed. Tests cover fixed sensor and split isolation, evaluator-target exclusion,
absent-cue no-ops, immutable inference, action/update timing, symmetric/skew control,
exact fitting replay, finite inventory and precision decisions. An analytic identity
map fails transverse contraction while an analytic radial-restoration test fixture
recovers with preserved pose; those analytic controls are not experimental candidates.

Command: `uv run python -m soam.navigation.runner fixture --output runs/study-e0-v1`.
Four fixture fits completed, each neural model using eight updates. With a 2x margin,
projected numerical CPU is 372.47 seconds, execution wall 387.70 seconds and artifacts
469,379,493 bytes. These pass the predeclared 80% time ceilings (2,880 CPU / 5,760 wall
seconds) and 1 GiB archive ceiling. The live runner enforces cumulative 3,600 CPU /
7,200 wall seconds and 2 GiB RSS. The source snapshot and raw fixture records remain
in `runs/study-e0-v1`; the ledger accumulates all subsequent execution.

Scientific trials may now begin under SOAM-096: 14 development fits, 40 confirmation
fits and four exact repeats, with selection frozen between phases. No architecture,
encoder, width or geometry-loss sweep is permitted. A runtime failure stops the
branch without scientific falsification or automatic retry. Historical results and
all later module experiments remain unchanged.
