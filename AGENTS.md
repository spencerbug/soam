# SOAM research instructions

Read README.md, docs/RESEARCH_SPEC.md, docs/EXPERIMENTS.md, and the current report first.
Run `uv run pytest` before modifying existing code. An empty bootstrap suite is not a pass.

The user supplied SOAM v0.1 on 2026-10-25. The architecture is frozen at the interface
level; mechanisms remain experimental. Preserve negative results and do not claim
attractors, compositionality, self-organization, or neuroscientific validation from
bounded trajectories or ordinary RNN prediction alone.

## Current scope

WP-00/WP-01: deterministic synthetic dynamics, bounded action/context-conditioned
recurrent baselines, context switches without reset, perturbation diagnostics,
reproducible metrics and reports. Do not implement associative writing, learned
scope translation, consolidation, JEPA, or an action expert before the relevant
decision gate is reviewed. Empty future module directories are boundaries, not implementations.

## Experimental rules

- Use Python/PyTorch. Keep the initial sensory projection fixed.
- Keep transient hidden state, persistent parameters, and environment ground truth separate.
- Prediction/imagined rollouts must not modify persistent parameters.
- Evaluation cannot pass hidden world states or correct future observations into free rollouts.
- Give every result its configuration, seed, source commit, source fingerprint, software versions,
  numerical settings, data exposure, parameter/storage counts, timing, and compute estimates.
- Separate train, development, and test random streams. Tune on development only.
- Use multiple fixed seeds and equivalent total parameter budgets where practical;
  state differences and report compute rather than claiming perfect matching.
- Compare grounded one-step error with free multistep error, switching, and perturbation responses.
- A tanh bound is not evidence of recovery toward a trajectory or useful attractors.
- Keep baseline results and failure analysis. Advance one work package at a time.
- Tests must cover scientific invariants, data separation, no-write inference, and reproducibility.
- Review and verify local-worker output. Never let a worker control its own approval or trials.
