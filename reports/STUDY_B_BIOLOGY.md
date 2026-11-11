# Study B: biological evidence and engineering analogies

2026-11-11. Supporting research within SOAM-066–069, not a new experimental fork.
The comparisons are specified in [Study B v1](../docs/STUDY_B_PROTOCOL.md). None
of the evidence below validates SOAM's neurons, time constants or architecture.

| Topic | Experimental evidence | Engineering connection and limit |
| --- | --- | --- |
| Theta-associated encoding/retrieval | Siegle and Wilson used closed-loop, phase-specific CA1 inhibition in mice performing a spatial task. Behavioral effects depended on theta phase and whether the task segment emphasized encoding or retrieval. | Supports phase-dependent processing in that preparation. It does not specify a universal binary sensory gate, justify a particular frequency, or show that every recurrent computation should alternate phases. Study B compares fixed-period, observation-triggered, and learned internal schedules. |
| Landmark correction and path integration | Seelig and Jayaraman recorded a localized activity pattern in the Drosophila central complex that tracked visual landmarks and continued tracking angular orientation using self-motion information without visible landmarks. | Motivates separate motion propagation and sensory correction. The insect heading representation and a trained tanh state are different systems; prediction quality or contraction in Study B does not establish a continuous attractor. |
| Corollary discharge | Sommer and Wurtz identified a midbrain–thalamus–frontal pathway conveying saccade-related signals and used thalamic inactivation to establish its influence on anticipatory frontal visual processing. | Supports a motor-related signal modulating sensory processing in that circuit. An externally supplied action vector is an engineering analogue, not a demonstrated biological corollary-discharge pathway or evidence for SOAM's motor authority. |
| Sensorimotor prediction error | Keller, Bonhoeffer and Hübener found mouse V1 responses to interruptions of visual flow linked to locomotion. | Consistent with sensorimotor mismatch processing, but such responses alone do not uniquely identify a prediction-error algorithm or infer observation reliability. |
| Alternative account of mismatch | Muzzu and Saleem elicited related perturbation responses with visual stimuli uncoupled from running; tuning to visual speed/orientation and locomotion modulation explained important response properties. | Requires conventional sensory/motor alternatives. Large residuals in Study B cannot be assumed trustworthy evidence; corruption and genuine changes must both be tested. |

Primary sources:

1. Siegle JH, Wilson MA (2014), [Enhancement of encoding and retrieval functions through theta phase-specific manipulation of hippocampus](https://elifesciences.org/articles/03061), eLife 3:e03061, DOI 10.7554/eLife.03061. The indexed publisher abstract and [author PDF](https://open-ephys.org/s/Siegle-2014-eLife.pdf) supported this narrow summary; the live article page presented an access challenge.
2. Seelig JD, Jayaraman V (2015), [Neural dynamics for landmark orientation and angular path integration](https://pubmed.ncbi.nlm.nih.gov/25971509/), Nature 521:186–191, DOI 10.1038/nature14446.
3. Sommer MA, Wurtz RH (2006), [Influence of the thalamus on spatial visual processing in frontal cortex](https://www.nature.com/articles/nature05279), Nature 444:374–377, DOI 10.1038/nature05279. Publisher indexed text and the [author institutional record](https://scholars.duke.edu/publication/742380) were available; the direct publisher fetch was restricted.
4. Keller GB, Bonhoeffer T, Hübener M (2012), [Sensorimotor mismatch signals in primary visual cortex of the behaving mouse](https://pubmed.ncbi.nlm.nih.gov/22681686/), Neuron 74:809–815, DOI 10.1016/j.neuron.2012.03.040. Summary is limited to indexed primary-source information, not an independent reanalysis.
5. Muzzu T, Saleem AB (2021), [Feature selectivity can explain mismatch signals in mouse visual cortex](https://pmc.ncbi.nlm.nih.gov/articles/PMC8655498/), Cell Reports 37:109772, DOI 10.1016/j.celrep.2021.109772. Full primary report inspected.

State estimation supplies the engineering decomposition: propagate a prior using
actions, then update it using permitted measurements and an explicit reliability
assumption. A Kalman-form update requires a model and noise assumptions; it is not
by itself a biological explanation. Study B's filter learns its observation basis
and transition from training features and carries a transient covariance. Its
ordinary fixed-noise and supplied-noise results must be labeled separately.

Predictive processing is a broader theoretical family than this decomposition.
An explicit residual is a useful computational variable; improved NMSE cannot
establish that a brain implements the same representation, objective, gain rule
or recurrent settling mechanism. Conversely, a negative settling result here
would reject only the tested engineering advantage on E1-family data, not theta
function, path integration, or predictive processing generally.

No fixed theta frequency is imported. Internal steps have zero simulated physical
time, and their cost is measured separately. The biological contribution is a
set of discriminating questions, not an architectural requirement.
