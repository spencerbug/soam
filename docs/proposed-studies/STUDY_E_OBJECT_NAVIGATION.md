# Codex prompt — Study E: Navigable object-centered recurrent memory

**Status:** conditional proposal, not selected. This is a minimal *capability* experiment, not proof that recurrent attractors exist.

## Mission

Design one bounded scientific experiment asking:

**Can a recurrent estimate represent a learned object's local structure so that it can be initialized from partial features, evolved under action, corrected by observations, and reused across unseen viewpoints/routes more effectively than a conventional learned map or state-space predictor?**

Read current AGENTS.md and the checked-out branch's research state. Verify source provenance; current public SOAM branches may not contain the completed A/B/B2/C local implementation. Study C evidence: https://spencerbug.github.io/research/soam-study-c/ . Preserve its results and historical E1 failed sharing gate.

## Evidence-based starting assumptions

Study B/B2 support separating predict -> score prior -> correct, with zero extra settling by default. B2's ADAPT1 is only validated for redundant linearly projected 2D features; do not blindly import its channel-disagreement rule to new sensors. Study C showed TWO16 (two separate recurrent states with shared learned parameters) improves Brier over single-state PC16 and capacity-controlled PC32 under an explicitly supplied two-regime task. It did not show shared-neuron dynamics, online object learning, attractors or general open-world belief robustness. ADAPT1-C was an effective compact conventional alternative, and both neural/structured candidates were overconfident for omitted coherent-fault causes. Carry conventional state-space and neural baselines; don't assume multiple hypotheses must always run.

Study D is an independent acquisition question. If D has demonstrated persistent learning, use its proven mechanism as an optional extension; otherwise start with objects learned offline and do not call their recall online acquisition.

## Minimal simulator and observability

Construct one stationary 2D object with learned local landmarks, an observer with relative pose (translation and orientation if possible), action commands and intermittent partial feature observations. Use a frozen encoder or generated features; sensor/perception training is not this study. Generate distinctive and aliased landmarks, occlusion and withheld action trajectories. Keep object geometry, exact pose, correspondence, hidden state, simulator transforms and future observations evaluator-only. A strong explicit map must learn geometry from the same permitted experience, not read simulator ground truth.

Establish symmetries and conditions under which pose is identifiable; score modulo unobservable symmetries. Distinguish motion-source ambiguity from sensor corruption. Do not expect a single partial view to identify a symmetric pose or distinguish identical objects.

## Controlled architecture inventory

At minimum:
1. Conventional GRU sequence/predictor with the same observations/actions and reasonable training.
2. Small recurrent predict/correct reference (PC16-like, scaled only if task difficulty requires).
3. Structured learned object map + localization filter with learned observation/action model, or another competent explicit-memory estimator.
4. A minimal object-relative recurrent state candidate, optionally split into identity and pose readouts/variables, with no oracle pose. A split is a hypothesis to test, not evidence of disentanglement.
5. If Study C's ambiguity is present, a conventional candidate-mixture and a shared-parameter separate-state neural reference. Compare to strong collapsed single-Gaussian or single-state variants.
6. If Study D passes, an optional instance-associative memory adapter with a complete transient reset test.

No thalamic routing, multi-population coupling or learned attention in the first pilot. Preserve parameter-matched, active-state-matched and measured-time comparisons separately. Model inference may be slower than linear filters despite fewer MACs.

## Stage E1 — one familiar object's sensorimotor navigation

1. Cue from an unfamiliar partial viewpoint and initialize posterior.
2. Predict forward once per physical action, score before new observation.
3. Correct when permitted observations arrive; otherwise coast with action-conditioned dynamics.
4. Return to a known viewpoint by a held-out alternative route and test loop closure.
5. Run reverse actions, reordered action compositions, long gaps, partial masks, aliased landmarks and corrupted snapshots.
6. Compare same-object novel routes against entirely novel objects; do not conflate trajectory generalization with persistent learning.

Frozen primary endpoints should include action-conditioned feature prediction and at least one object-centered reuse measurement (e.g. pose/loop-closure quality on withheld routes). Add reconstruction, drift, correction recovery, identity stability, false familiarity and calibrated uncertainty guards. Evaluate the representation against a simple explicit learned map.

## Conditional Stage E2 — identity and pose

Only if E1 demonstrates a meaningful gap, introduce multiple known objects with overlapping local features. Test object identification across changed world poses and unseen viewpoints, withholding particular route/pose combinations. If object hypotheses compete, use proper probability scoring and compare against structured hypothesis filters. A learned identity/pose separation needs causal interventions and retention tests, not vector-label assertions.

## Conditional Stage E3 — persistence and novel objects

If Study D supplies supported acquisition, expose novel object-specific features, permit bounded grounded writing, reset transient activity, and require later viewpoint recognition and prediction. Count learned map or associative storage equally. Do not call offline object memorization self-organizing acquisition.

## Conditional Stage E4 — moving objects

Only after stationary navigation works, distinguish observer motion from object motion with known self-actions; show an observability argument. Test stationary/moving observer crossed with stationary/moving object and withheld combinations. Accurate optical/feature prediction alone does not prove motion-source identification.

## Attractor/geometry diagnostics

Plot hidden trajectories, pose probe accuracy, action reversal, closed-loop consistency and perturbation response. A smooth manifold or contraction does not prove a useful continuous attractor; test whether states recover toward correct task-relevant states. Do not assume a symmetric recurrent matrix yields convergence while driven by asymmetric motion or gated feedback. Keep probe ground truth out of learner updates.

## Scientific process, boundaries and artifacts

Freeze a versioned protocol, simple and strong baselines, independent train/development/confirmation objects and roots, primary endpoint, practical margins, calibration/recovery guards, uncertainty, compute/storage budget, stopping rule and source fingerprints before confirmation. Run finite early fixtures and stop when irreducible ambiguity or leaked map geometry invalidates the task. Compare models under matched information, learning exposure, params, retained state, external maps and actual latency. Report resource Pareto and failure cases.

Deliver code/tests, observability analysis, paired results, trajectories, report, decision and a conditional one-step follow-up. Do not auto-build complex compositional object graphs or a robotic agent.

**Final question:** Has the recurrent representation learned *navigable, reusable object-relative structure* beyond ordinary autoregressive sequence prediction, and is that benefit worth its resources versus a conventional map and estimator?
