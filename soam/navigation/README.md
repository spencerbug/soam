# E0 evaluation terminology

**Blindfolded action prediction** supplies the action sequence but no new sensory
observations after the initial cue. Actions can be nonzero: “blindfolded” refers
to missing sensory feedback. The reported endpoint averages sensory prediction
NMSE across 64 steps.

**Zero-action drift** supplies zero action and no new observations. Its reported
endpoint is absolute pose error after 128 steps, in degrees, including any error
at initialization. Displacement from the initialized pose is a separate diagnostic.

The frozen numerical code and saved-result identifiers retain their original names:

| Identifier | Meaning |
| --- | --- |
| `condition="free"`, `free_nmse` | Blindfolded action prediction and its NMSE |
| `free_horizon` | Rollout length; also used by other prediction conditions |
| `stationary_deg` | Zero-action absolute pose error |
| `stationary_drift_deg` | Zero-action displacement from the initialized pose |

`free` also participates in stream seeding; changing it would change the data.
The E0 and E0-HOLD reporting scripts use the clearer display labels while the
numerical source, archived keys, thresholds and outcomes remain unchanged.
