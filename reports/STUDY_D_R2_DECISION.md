# Study D-R2 decision: useful exact codes, imprecise completion-gap estimate

November 19, 2026. Owned by [SOAM-093](../tickets/SOAM-093-retrieval-decoding-decision.md).

**Proceed with acceptance of valid, precision-qualified inconclusive evidence.
Retain KV as the existing scoped conventional reference.** This completes the
selected diagnostic; it does not pass a retrieval, sharing or integration gate.

## Frozen decision and measured evidence

The [report](STUDY_D_R2.md) follows the [frozen protocol](../docs/STUDY_D_R2_PROTOCOL.md)
without tuning, extra roots, exclusions, retries or mechanism changes. All 12 fits
(fixture, ten independent confirmation roots, one prescribed repeat) complete.
87 repeated numerical arrays and 42 checkpoint tensors match exactly; independent
reduction checks 210 root metrics and all archived acquired codes. All 110 frozen
D-R1 source hashes remain unchanged. The suite passed 328 tests before numerical
execution; source is commit `924acd8c3f32af9abfbd77ff69f8bab3030b01cb`, fingerprint
`0df3abe0ec7906dea1d1978280709f99f3111b2c06fff066d759559ad3fba577`.

| Question | Result | Interpretation |
| --- | --- | --- |
| Can the unchanged decoder use exact acquired codes? | 100% sampled canonical accuracy; mean NMSE .01012; adjusted empirical interval [1,1] | Meets the frozen exact-code adequacy guard in this finite sample; no universal reliability guarantee |
| How does ordinary partial-cue PH768 recall perform? | 77.634% accuracy; canonical NMSE .08339; free-eight NMSE .05813 | Substantial errors remain despite usable acquired-code decoding |
| Is the diagnostic gap sufficiently precise? | +22.366 percentage points; adjusted interval [15.357,29.018]; width 13.661 points | Interval is above the five-point practical margin, but width exceeds the frozen ten-point cap: **inconclusive**, not a passed diagnosis |
| Are acquired codes preserved? | All 40 final sequence projectors audited; maximum residual 3.94e-14 | Preserved in their stored spans at the declared tolerance; not evidence of correct cue completion |
| How do ordinary references perform? | KV 100%; REG-LIFT 96.071% sampled accuracy | Descriptive same-data references, not newly tested superiority/reliability conjunctions |

The formal classification is governed by both the effect and precision rules.
Reporting the clearly positive direction is appropriate; dropping the width rule
or calling this a confirmed diagnosis would revise the protocol after seeing data.
All-success intervals are degenerate empirical root-bootstrap intervals, not proof
that population risk is zero. No additional roots are added from the unused budget.

## What the diagnostic resolves and leaves open

The fixed encoder and decoder can preserve task-relevant relationships in the
actual noisy acquired codes. The privileged branch knows which object's codes to
decode, and equally weights all eight acquired snapshots. It never selects the
best target-scored snapshot, changes a prediction, or writes to a learner.
This supports a descriptive distinction between available code content and its
use through the present cue-to-output path. It does not establish a deployable
retrieval advantage or determine the unique cause of the errors.

PH converged in every query, averaging 2.300 cycles. Every queried relationship
state has at least one upward step in one of its eight thermometer-coded value
coordinates. The mean discrepancy on free coordinates is .00911 to the correct
object's acquired codes versus .05538 to other objects' codes; another object's
code is strictly closer on only .446% of queries. These are descriptive measures.
Being near a correct code need not give the correct decoded output, and an invalid
thermometer pattern need not give an incorrect output. These observations alone
cannot separate clamping, noisy cues, encoding geometry, mixed states, or readout
behavior away from the acquired-code set. No correction or causal intervention ran.

The common action core remains a supplied-family scaffold with grounded one-step
NMSE about 8.75e-18. Its good dynamics do not rescue an incorrect retrieved value.
This study does not retest unknown rejection, isolated acquisition, prefix retention,
capacity, additional settling, learned organization or general attractors.
The D-R1 practical-settling negative and reliability failures, SOAM-052 stop,
SOAM-069 revise, and every earlier empirical outcome remain unchanged.

## Resources, next recommendation and communication

The four numerical phases used 26.704 CPU / 26.829 execution-wall seconds, peak
RSS 366,903,296 B and 348,491,815 artifact bytes before the final resource receipt;
all are below the fresh 900 / 1,800 seconds, 2 GiB RSS and 1 GiB artifact limits.
Archive-closeout overhead is recorded separately and charged to the same allocation.
PH uses 4,720,160 persistent bytes, REG-LIFT 2,131,480, and KV 7,448; memory and
timing mismatches remain explicit. The three arms coexist during evaluation with
a shared core; RSS includes evaluator arrays and transient dense workspaces.

At most one next recommendation: **if a formal precision-qualified diagnosis is
needed for the next architecture decision, select a fresh, fixed-design precision
replication**. Plan its independent-root count from this pilot's dispersion, freeze
its finite maximum and criteria before execution, and use entirely fresh streams.
Do not expand the completed study, change the width cap, or infer that an encoding,
clamp or population sweep has been selected. No successor is activated here.

The owner was notified that usable acquired codes versus failed ordinary recall
merits a joint blog/report, with the frozen inconclusive classification prominent.
This is a communication recommendation only; nothing was published or pushed.
