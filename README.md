# SOAM — Self-Organizing Attractor Memory

Research repository for investigating cue-driven attractor dynamics: concurrent
predictive circuits, sensorimotor calibration, attentional handover, and eventually
reusable embodied skills and continual memory. This is a hypothesis, not an
established result.

The adopted [v0.2 research specification](docs/RESEARCH_SPEC_V0_2.md), dated November 1,
2026, revises the architecture and execution order. The [v0.1 specification](docs/RESEARCH_SPEC.md)
and its reports remain preserved. No new attractor mechanism has been implemented
or empirically validated by the scope revision.

## Current milestone

**Next: [SOAM-033](tickets/SOAM-033-handover-protocol.md), the cue-driven handover
protocol and bounded circuit-layout comparison.** Switching among attended,
tracking, and primed roles takes priority over sophisticated prediction. Use an
explicit attractor candidate, recurrent controls, fixed sensing, and declared
scaffolding. Shared populations, separate circuits, clones, alternating banks, and
columns/stacks are experimental alternatives. An explicit discrete world graph is
not required. Unsupervised organization and associative writing follow later.

The delivered Stage 0/substrate work (WP-00/WP-01) covers synthetic action-conditioned 2D
regimes, a fixed sensory projection, shared bounded recurrent baselines, independent
predictors, shared-state switching, independent-model handoffs, and perturbation diagnostics.
The bounded local-write contract is implemented; acquisition comparisons, learned
scopes, consolidation, JEPA, and planning remain future work.

See [experiment protocol](docs/EXPERIMENTS.md), [work packages](docs/ROADMAP.md),
[architecture boundaries](docs/ARCHITECTURE.md), [initial report](reports/BASELINE.md),
[controls report](reports/SUBSTRATE_CONTROLS.md), and [current writer report](reports/LOCAL_WRITE_CONTRACT.md).
The remaining work is organized in the [priority and milestone tracker](PRIORITIES.md)
and [issue backlog](tickets/README.md), with GitHub-ready templates and ticket conventions.

The [stronger six-model controls](reports/SUBSTRATE_CONTROLS.md) are complete:
17 of 18 trials pass the preregistered screen, with an additive seed-23 failure on
irregular switches. GRU and fully independent controls pass all three seeds. All
six seed-11 repeats match exactly. Long-horizon drift remains; these results do not
establish self-organization. [Gate 1](reports/GATE_1_REVIEW.md) proceeds with the
low-rank substrate and GRU reference. SOAM-003 now provides bounded grounded writes,
read-only prediction snapshots, and exact rollback. All 48 tests pass. A three-seed
contract demonstration reproduces exactly but includes multistep regressions; it does
not establish H2. SOAM-004 remains ready on a separate writer comparison branch;
it is no longer the next primary task. The reported 48-test result belongs to that
implementation; documentation changes do not constitute a new experiment.
The original four-model benchmark remains preserved as historical evidence.

## Run

```sh
uv sync --extra dev --locked
uv run pytest
uv run soam-run --config configs/smoke.json --output runs/smoke
uv run soam-run --config configs/substrate.json --output runs/substrate
uv run soam-compare runs/substrate --output reports/substrate-comparison.md
```

CPU and one Torch thread are the reproducible reference. Run directories refuse
overwrite and contain resolved config, source/version provenance, checkpoints,
per-seed metrics, training traces, and diagnostic PNGs. Numerical results should
repeat on the same software/hardware; wall times are expected to vary. `uv.lock`
pins dependencies. The smoke configuration exercises the pipeline; it is not
evidence for H1. Tracked compact results are in `reports/`; larger artifacts are in `runs/`.

To check a full-length repeat of seed 11 (choose unused output paths):

```sh
uv run soam-run --config configs/substrate.json --seeds 11 --output runs/my-repeat
uv run python scripts/check_reproduction.py runs/substrate runs/my-repeat
```

## Research discipline

Ordinary RNNs here are baselines. Bounded activity does not establish attractor
recovery; shared weights do not establish reusable primitives. H1 remains
provisional until prediction, switching, stability, and budget comparisons are
examined. Transfer/composition belong to H5. Ground truth is used by the simulator
and diagnostics, never supplied to the recurrent transition during evaluation.

This local repository is independent of `geometric-recurrent-memory`. No remote
hosting or publication is required for these experiments.
