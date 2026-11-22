# E0-HOLD decision: accept the improvement and preserve the failed joint fix

2026-11-21 · SOAM-101 · **proceed with evidence acceptance only**.
The [owner-selected follow-up](../docs/requests/e0_hold_2026_11_21.md) is complete.
The [report](STUDY_E0_HOLD.md) records a valid **negative result for the declared
joint fix**, not a failed execution or a general falsification of recurrent memory.

The horizon intervention substantially reduces NAV32's stationary drift at fixed
optimizer count and fixed sensory evidence: 12.332° → 5.698°. Its paired gain of
6.635° [5.017,8.805] passes the frozen five-degree practical-gain criterion and
four-degree width cap. But the remaining pose-error interval [5.259,6.183] is
adequately precise and wholly above the five-degree absolute target. We do not
round 5.70 down to a fix, change the threshold or reuse the earlier E0 classification.

The mixed-action prediction degradation interval [−.001027,.006732] passes the
.01 NMSE margin. Grounded prediction, cue return and induced-pose-error guards
also pass. This does not mean every diagnostic is unchanged: constant-direction
action errors worsen, and small correction/pose degradations are measured.
Transverse-ratio degradation [.007312,.062184] crosses its .05 margin. It establishes
a weaker contraction proxy in this paired sample, but does not establish either
noninferiority within the margin or a degradation definitively beyond it. The
absolute recovery criterion still passes. Eleven of thirteen joint criteria pass;
the unresolved recovery guard does not erase the precise stationary failure.

The control results reinforce why the joint criteria matter. GRU32's long arm has
better stationary accuracy (2.631°) but markedly poorer blindfolded action prediction
(.07717 → .26582 NMSE). Those are mandatory descriptive control results, not a
replacement confirmatory claim. SYM32 retains poor action prediction. PCA2 remains
the compact accuracy reference for this supplied rank-two task, with no autonomous
transverse restoration. The evidence does not support proceeding to hierarchy on
the assumption that the navigable-state problem is solved.

Validity review accepts all 147 scientific fits, twenty paired roots, seven repeats,
189 exact arrays, 54 exact tensors, 980 independently checked root metrics and all
13 adjusted intervals. Initial states/prefix data pair correctly; no extra cues or
moving-tail updates enter LONG128. All 148 historical E0 source hashes remain
unchanged. The [receipt](study-e0-hold/receipt.json) and
[621-file archive inventory](study-e0-hold/archive_sha256.json) preserve complete
source/resource identity. No failed/excluded run, confirmation tuning or allocation
extension occurred. Additional recurrence costs about 3.32× per NAV32 fit and is
disclosed; it is not an equal-compute result. Raw payloads remain local.

**Essential next, conditional recommendation under SOAM-101:** a single fixed
optimization-budget comparison at the 128-step stationary horizon, replaying the
same prefix corpus rather than acquiring more observations. Freeze one larger
update count, fresh roots, resource controls and the existing navigation/recovery
guardrails in a new protocol before execution. The long-arm training loss still
decreases near the end (.04204 in the preceding hundred updates versus .03861 in
the final hundred, averaged across roots), making incomplete optimization a
reasonable hypothesis to test. That diagnostic is not proof of underfitting, and
more optimization is not assumed to fix either residual drift or recovery.
Do not extend this completed run or select an architecture based on an unrun remedy.

No successor experiment is selected or activated. Coupling, reference-frame
translation, RIM-like routing, hierarchy, sparse encoders and capacity remain
**future capabilities**; no parallel numerical branch is opened. Historical E0's
inconclusive outcome, E1 stop, D-R1 negative evidence, D-R2 inconclusive diagnosis
and the scoped storage references remain unchanged.

This merits a joint blog/report discussion: longer stationary training improves
retention substantially while other dynamics require independent checks. The owner
is notified with the measured findings and the failed joint criterion prominent.
This decision authorizes no publication, remote push or issue synchronization.
