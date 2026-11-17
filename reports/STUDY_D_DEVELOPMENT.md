# Study D development and preconfirmation review

November 17, 2026. Source commit `2270743`; protocol v1 unchanged. The full
repository suite passed 303 tests before numerical work; lint and ticket checks
passed. One full-inventory fixture fit / four model evaluations completed. Its
2x resource projection was 106.44 CPU seconds and 385234896 artifact bytes.

All four core fits and 32 model/setting development evaluations completed, followed
by eight independent-object calibration evaluations. The two core ridge settings,
three FAST rates and three REG penalties were exhausted exactly as declared.
Paired model inputs and source identities were checked. No candidate, root or
failed endpoint was dropped; no extra setting, replay, or learned gate was added.

Selection: core ridge 1e-6, FAST eta 1, REG ridge .01, KV as the strongest
conventional reference. Both conventional controls remain in confirmation. FAST
composite development score was .87252 versus .0003596 KV and .02604 REG. FAST
learns a single object but shows large sequential interference. That is a valid
measured developmental failure, not a reason to discard its mandatory confirmation
comparison or change its update budget. No optimizer convergence claim is made for
closed-form core fitting or prescribed single-update online methods.

Known-object familiarity 95th-percentile thresholds from independent calibration
objects: KV .0007452845502214262, REG .000033517236573334454, FAST .6328776779396241.
No unknown-object or confirmation labels selected thresholds. These scores are not
probabilities. Calibration has no effect on raw predictions or writes.

Proceed to the ten frozen confirmation roots and prescribed repeat. The primary
agent reviewed information parity, source identity, controls, resources and fixed
stopping criteria. No confirmation stream had been generated at this review.
Exact candidates, selections, thresholds, inputs, fit records and arrays are in
`runs/study-d-v1/development/`; failed/out-of-scope hypotheses remain preserved.
