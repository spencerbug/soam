# SOAM — Self-Organizing Attractor Memory

Research repository for investigating whether a shared recurrent substrate can
acquire, preserve, reorganize, and reuse dynamical knowledge through fast associative
learning and slow consolidation. This is a hypothesis, not an established result.

The [research specification](docs/RESEARCH_SPEC.md) records the user-supplied v0.1
architecture and experimental program dated October 25, 2026. Interfaces are
provisionally frozen; learning mechanisms and connectivity are experimental.

## Current milestone

Stage 0 and the substrate sprint (WP-00/WP-01): synthetic action-conditioned 2D
regimes, a fixed sensory projection, shared bounded recurrent baselines, independent
predictors, switching without state reset, and perturbation diagnostics. Later
plasticity, consolidation, JEPA, and planning components are intentionally unimplemented.

See [experiment protocol](docs/EXPERIMENTS.md), [work packages](docs/ROADMAP.md),
[architecture boundaries](docs/ARCHITECTURE.md), and [initial report](reports/BASELINE.md), and [current controls report](reports/SUBSTRATE_CONTROLS.md).
The remaining work is organized in the [priority and milestone tracker](PRIORITIES.md)
and [issue backlog](tickets/README.md), with GitHub-ready templates and ticket conventions.

The [stronger six-model controls](reports/SUBSTRATE_CONTROLS.md) are complete:
17 of 18 trials pass the preregistered screen, with an additive seed-23 failure on
irregular switches. GRU and fully independent controls pass all three seeds. All
six seed-11 repeats match exactly. Long-horizon drift remains; these results do not
establish self-organization. [Gate 1](reports/GATE_1_REVIEW.md) proceeds with the
low-rank substrate and GRU reference. SOAM-003, the bounded local-write contract,
is next; associative writing remains unimplemented.
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
