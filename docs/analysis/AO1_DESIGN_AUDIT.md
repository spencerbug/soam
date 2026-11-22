# AO-1 mathematical design audit

SOAM-104 · November 22, 2026 · source baseline `c121d69`.
These are finite, untrained algebra checks, not a scientific pilot or a timing
calibration. No optimizer, learned assembly discovery, development selection, or
confirmation evaluation is permitted in this audit.

## Frozen check inventory before execution

Use NumPy float64 and PCG64 seed 20261122. Run the following inventory once, with
a 60-second CPU / 120-second wall ceiling, 1 GiB RSS and 10 MiB output allowance.
Code defects may be corrected and rerun with both failure and correction recorded;
no parameter search or trained examples may be added.

1. Construct a dense 96 by 24 Gaussian thin-QR projection with positive QR diagonal.
   Check full column rank, nonzero rows, orthonormal columns (tolerance 1e-12), and
   preservation of input norm for one declared random 24-vector.
2. For an eight-unit candidate with alpha .5, bounded R/K matrices, two actions,
   random h in [-.8,.8], and bias in [-.2,.2], compare the analytic Jacobian with
   central differences at epsilon 1e-6; maximum error must be below 1e-8.
3. For 512 randomly generated states in [-1,1]^8, verify one prediction and one
   convex sensory correction stay in [-1,1] to 1e-12. This checks the implementation
   of a convexity argument, not attraction or a universal numerical proof.
4. Iterate the scalar diagonal system R=1.5, alpha=.5 from h=.7 for 256 steps.
   Check the nonzero fixed-point residual below 1e-12 and local derivative below
   one. With zero cross-connections this supplies a stable-memory counterexample
   to the inference that stable states imply routing.
5. For R=[[0,2],[-2,0]], alpha=.5 and h=[.01,0], calculate the one-step increase of
   the symmetric-part Hopfield energy (S=0). Check positive energy change and a
   local origin multiplier magnitude above one. This exposes the absence of an
   automatic energy/stability guarantee for the permitted directed discrete update.
6. In a three-unit leaky tanh chain with R[1,0]=R[2,1]=.8 and all other entries
   zero, give every unit the same direct cue. Replace only source-to-receiver
   recurrent message changes by the zero-cue reference. At the second step the
   downstream output must differ from the uncut trajectory; with R=0 it must not.
   Initial direct sensory drive remains identical in cut and uncut trajectories.
7. Audit the manifest's finite fit counts, disjoint root sets, sixteen primary
   intervals, model resource formulas, fixed sensor energy, and six/two object split.

## Result

All seven checks passed in the single declared run. The
[audit script](../../scripts/check_ao1_design.py) and
[raw output](ao1_design_checks.json) preserve the exact inputs, versions, results
and hashes. This is analytical design evidence only; no model was trained.

| Check | Observed result |
| --- | --- |
| Dense expansion | Rank 24, minimum row norm .303889; orthonormality error 8.88e-16; norm error zero |
| Candidate Jacobian | Maximum central-difference discrepancy 3.25e-11, below 1e-8 |
| Sampled bounded updates | Maximum absolute state .895275 over the 512 samples |
| Stable memory without routes | Nonzero fixed point .858560; residual 1.11e-16; local multiplier .697157; no cross-connections |
| Directed energy counterexample | Energy increases by 1.24867e-5; origin multiplier magnitude 1.11803 |
| Dense-input chain intervention | Downstream difference .0158624; uncoupled common-input difference exactly zero |
| Manifest formulas/inventory | All checks passed, including 231 scientific fits, sixteen primary intervals and disjoint roots |

The two counterexamples are successful checks of claim limits, not implementation
failures. Stable memory alone does not establish routing, and directed bounded
updates do not inherit a monotone symmetric energy. The chain shows that a
message intervention can detect a supplied route despite common direct input;
it does not establish learned organization or validate the full future evaluator.

Command: `UV_CACHE_DIR=/private/tmp/soam-uv-cache uv run --offline --no-sync python
scripts/check_ao1_design.py --output docs/analysis/ao1_design_checks.json`.
Python 3.12.13 / NumPy 2.5.4, float64, PCG64 seed 20261122. Measured CPU .010866 s,
wall .012809 s, peak RSS 36,732,928 bytes: all within the predeclared allowance.
No failures, retries or excluded checks. This small audit does not calibrate
training or intervention-evaluation runtime.

The raw output retains the pre-review manifest hash. After this run, only its
status and blindfolded-action names changed; no numeric input, criterion, seed or
budget changed. Reconstructing the earlier names/status reproduces its recorded
SHA-256 exactly, and the script hash still matches. Accepted manifest SHA-256:
`d49332cfeee73d9a85a4b249c605c117b78cd1075c0333a4af6cc939e81e2091`.
The protocol's final review also clarifies per-case selective-error aggregation,
block-preserving action fallback, diagnostic reporting and repeat requirements;
these procedures have not been implemented or tested by this algebra audit.
