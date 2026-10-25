# Interface boundaries

The implementation begins with conventional recurrent baselines. All functions have
explicit state inputs and outputs; model modules hold parameters, never the active
belief state.

| Boundary | v0.1 contract | Initial implementation |
| --- | --- | --- |
| Encoder | `encode(observation) -> z` | Fixed orthonormal projection of synthetic observation |
| Observation assimilation | `assimilate(h_pred, z, context) -> h_obs` | Convex blend with learned sensory-state projection |
| Recurrent memory | `step(h, action, context) -> h_next` | Leaky tanh, additive/gated/low-rank context |
| Readout | `decode(h) -> z_pred` | Trained linear map |
| Fast writer | evidence → proposed parameter delta | [Grounded bounded proposals, explicit commit, one-level rollback](../soam/plasticity/README.md); H2 unproven |
| Scope translator | local statistics + proposed delta → constrained delta | Deferred |
| Consolidator | weights + grounded evidence → validated provisional weights | Deferred |
| Planner | state + candidate actions + goal → selected action | Deferred |

`rollout` starts from one observation, then uses only hidden state, supplied actions,
and supplied context. It never sees future observations or ground-truth world state.
Grounded one-step evaluation assimilates each real observation between predictions.
The fixed projection has an inverse only for diagnostic plots; predictors cannot
call that inverse. Full observability and known context are deliberate first-stage
simplifications. There is no context inference or uncertainty representation yet.

The separate-core baseline has disjoint per-context transition matrices and shared
sensory initialization/readout. It carries a single active hidden state across switches
without resetting it. This is partial independence, not a fully independent ensemble;
the limitation is explicit in the protocol. No explicit object graph is used in inference.
