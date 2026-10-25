# Exp00: context-conditioned recurrent substrate

Protocol: [EXPERIMENTS.md](../../docs/EXPERIMENTS.md).

```sh
uv run soam-run --config configs/substrate.json --output runs/substrate
uv run soam-compare runs/substrate --output reports/substrate-comparison.md
```

Compare additive, gated, low-rank, and separate-core baselines on seeds 11, 23, 47.
Use `configs/smoke.json` for a fast pipeline check. No associative writes,
consolidation, JEPA, or learned action proposals are in scope.
