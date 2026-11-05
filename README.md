# SOAM — Self-Organizing Attractor Memory

Research repository and planned experiment platform for Hopfield networks and
related recurrent dynamical systems. The preferred hypothesis uses overlapping
neurons for features, relationships, and action relations, with separated networks
as controls. Useful sharing, attraction, and learned organization remain unproven.

The adopted [v0.3 research specification](docs/RESEARCH_SPEC_V0_3.md), dated November 5,
2026, broadens the program to reusable experiments, including NeuroSLAM-inspired
localization and Monty-style sensorimotor learning modules with recurrent memory.
The [v0.2 scope](docs/RESEARCH_SPEC_V0_2.md), [v0.1 specification](docs/RESEARCH_SPEC.md),
and completed contracts/results retain their historical meanings. The v1 handover
harness is implemented; the general platform and new studies are planned work.

The [conditional research paths](docs/RESEARCH_PATHS.md) govern follow-ups: first
measure one benefit of sharing, then select one experimental fork from the results.
Concurrency/handover and the two application studies are conditional extensions.

The [scientific assessment](docs/SCIENTIFIC_REVIEW_2026_11_05.md) treats SOAM as a
plausible mechanism research programme, with human-like sensorimotor intelligence
as a long-term goal rather than a supported claim. The next three questions are
useful shared dynamics, rapid retained acquisition, and active disambiguation.
See the [hypothesis ledger](docs/HYPOTHESES.md) and [ticket change map](docs/TICKET_REVIEW_2026_11_05.md).

## Current milestone

**Next: [SOAM-049](tickets/SOAM-049-shared-population-protocol.md), the minimal
shared-recurrence experiment protocol.** SOAM-047 adopted the
[platform contract](docs/RECURRENT_PLATFORM_CONTRACT.md); SOAM-048 is also ready
to implement its small engineering runner and fixtures. Scientific candidates
follow both deliveries. SOAM-039/044/040/041 plan minimal acquisition without waiting for skills or
concurrency. SOAM-053–055 test active disambiguation with frozen memory. The larger
Monty-style module (SOAM-056–058) follows supported acquisition and explicit selection.

Sharing refers to recurrent neurons and connections, not just tied parameters or
three independent networks stored in one tensor. Test overlap, binding, interference,
and directional dynamics while keeping evidence, goals, motor authority, transient
state, and persistent memory distinguishable. Preserve separated-state controls and
accept negative results. See the [ordered ticket queue](PRIORITIES.md).

SOAM-033/034 delivered the frozen [handover protocol](docs/HANDOVER_PROTOCOL.md),
[numerical manifest](docs/protocols/handover_v1.json), and [harness](docs/HANDOVER_HARNESS.md).
The [engineering report](reports/HANDOVER_HARNESS.md) records fixture-only verification.
SOAM-035 remains ready as a P2 comparison branch; no measured v0.2 study or new
shared-population study has run, and no handover/shared-population gate has passed.

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
uv run soam-handover-smoke --output runs/my-handover-fixture
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
