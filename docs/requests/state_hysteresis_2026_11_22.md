# November 22 state hysteresis experiment design

**Historical selection, superseded for current planning.** The later
[assembly organization request](assembly_organization_2026_11_22.md) and SOAM-103
select AO-1. E0-HYS remains a preserved, unrun, unselected retention diagnostic;
the record below describes the earlier selection. Fixed thresholds remain the
owner's preference if hysteresis is included in the new study.

The owner proposed that differences in neuronal responsiveness could organize
memory within a population: broadly responsive assemblies might recruit more
selective, persistent assemblies, potentially producing overlapping routing
hierarchies without a supplied tree. Discussion refined the proposed control from
excitability alone to resistance to changing an established state.

The owner then requested: “Can you write this up and design the experiment”.

When asked whether the first experiment should also learn thresholds, the owner
selected: “Keep thresholds fixed for the first mechanism test”. Thresholds are
therefore supplied; recurrent weights learn how to use the resulting units.

The owner subsequently challenged the theoretical link to a tree, emphasizing
that root-like units would receive external input and convey it through stronger
connections to subsequent assemblies. This clarifies the separate connectivity
hypothesis; it does not request starting trials or replacing fixed thresholds.
The proposal now derives local effective influence and identifies the absent
sensory-access and connectivity-learning assumptions. Hysteresis is not presented
as a sufficient tree-formation mechanism.

[SOAM-102](../../tickets/SOAM-102-state-hysteresis-protocol.md) selects **design of
E0-HYS**, a bounded test of explicit state hysteresis and navigability. The
[proposal](../proposed-studies/STUDY_E0_HYSTERESIS.md) preserves the broader assembly
idea; the [protocol](../STUDY_E0_HYSTERESIS_PROTOCOL.md) and
[manifest](../protocols/study_e0_hys_v1.json) specify the first experiment.

This is a fresh routing choice after [SOAM-101](../../reports/STUDY_E0_HOLD_DECISION.md).
Its conditional recommendation to increase optimization at the 128-step horizon
remains historical and unactivated. The owner now selects a mechanism design;
the earlier recommendation is not rewritten as if it selected hysteresis.

The current request covers documentation and experimental design. Implementation,
training, confirmation and publication have not started. E0-HYS is no longer the
default next execution path: a later return to it requires explicit fresh routing,
not silent reuse of the earlier selection. AO-1 now has its own owner selection and
will require its own protocol; it does not inherit this numerical allocation.

Classifications: the E0-HYS design is **essential next**; assembly routing,
multi-object organization, capacity, population-size/input-fan-out sweeps, HTM
encoders, coupling and neuromodulation are **future capabilities**. Historical E0's
inconclusive result, E0-HOLD's negative joint fix and E1's sharing stop are preserved.

Design source baseline: `047e2b81496a41dbf96537e11c39b4d17e54c1d4`.
No new empirical evidence is supplied by this owner selection.
