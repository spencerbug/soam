# E1 development execution procedure — SOAM-051, revision 1

Execute scientific v1 plus archive A1 without modifying either. This operational
entry point ends at the development phase boundary; it cannot open confirmation
streams. This is a partial stage of the 119-fit study, not an alternative smaller
experiment. No extra model, seed, learning rate, ridge setting or retry is allowed.

1. Check SOAM-050 done and SOAM-061 done/proceed. Run regression tests. Generate a
   new shape-equivalent A1 calibration including the entry point's source and tests.
   Freeze committed source before scientific fitting. Entry point checks every
   calibrated source hash against both working files and HEAD, plus the pinned A1
   contract. Changing implementation requires a new run identity/calibration.
2. Run `uv run python -m soam.shared.study --calibration runs/e1-development-calibration
   --output runs/e1-development-v1-a1`. Output must not exist. Reference CPU numerics
   are one Torch thread, deterministic algorithms, float32 models, float64 metrics.
3. Enumerate exactly 42 fits before execution: family order S32, D25, D16, G28, G32,
   L12, SYM32; configuration index 0 then 1; roots 401, 409, 419. Training data use
   split train, not development. FitPlan is exactly 100 recall plus 300 joint updates,
   batch 16; ridge uses the same observed records and its two frozen regularizers.
4. Record every input batch via verified A1 objects, pre/final weights and optimizer
   tensors, final training traces, data exposure and per-fit CPU. Checkpoints use a
   temporary file followed by rename; incomplete attempts remain in the run directory.
   No automatic resume or rescue retry is supported by this first entry point.
5. Score 20 development episodes per condition: pre-recall, final-recall, final
   transition (free32, grounded32 and free8 prefix). Preserve arrays, metrics and
   input references: 2,520 base cells total. No causal confirmation diagnostics run.
6. Enforce 90 CPU seconds per fit, 4,000 development CPU seconds, and whole-study
   14,400 CPU / 28,800 wall seconds, 2 GiB RSS and 8 GiB artifacts. Include old and
   selected calibration costs. Check between bounded operations; retain overshoot.
7. A numerical failure gets no successful replacement score. Continue independent
   development fits only for explicitly recognized nonfinite tensor failures.
   Unexpected implementation exceptions or any budget exhaustion stop subsequent
   execution, preserve artifacts and mark remaining inventory unexecuted. Escalate
   to the primary agent; do not edit code or rerun affected trials to obtain a pass.
8. On complete finite development results, apply the frozen two-config selection,
   GRU competence and floor screens. Record all families/configurations, including
   failures. Screen failure stops this scientific version as inconclusive. Screen
   success leaves confirmation pending at the explicit execution boundary. Neither
   outcome establishes superiority from development-selected results.

Qwen may extract/review this procedure and summarize emitted statuses or logs. It
may not choose parameters, edit source during execution, launch autonomous trials,
approve actions or change stopping rules. The primary agent invokes deterministic
code, validates evidence and owns interpretation. Confirmation/repeat orchestration
is subsequent work under the same frozen science and cumulative budget, conditional
on the development screen; it is not silently included in this entry point.
