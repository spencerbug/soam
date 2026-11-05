# SOAM v0.3 — shared populations and recurrent experiment platform

**Adopted:** 2026-11-05, at the owner's request. **Status:** research direction and
ticket plan. SOAM-047 subsequently adopted the [minimal platform contract](RECURRENT_PLATFORM_CONTRACT.md);
implementations and scientific results remain open.

See the adopted [conditional research paths](RESEARCH_PATHS.md) for the November 5
refinement: one minimal benefit pilot, then one result-selected experimental fork.

The subsequent [scientific review](SCIENTIFIC_REVIEW_2026_11_05.md) sharpens this into useful dynamics,
rapid retained acquisition, and active disambiguation. It defines proposed numerical
targets and RFC conventions; protocols still freeze actual trials before execution.

## 1. Revision boundary

SOAM becomes an experimentation platform for Hopfield networks and related recurrent
dynamical systems. The preferred architecture hypothesis is that features,
relationships, and action-conditioned relationships can use overlapping neurons
and recurrent connections. They need not be separate memory networks merely because
they have different functional names. The platform must also make competing
architectures easy to compare, including unsuccessful shared-population candidates.

This amendment supersedes the default execution order and topology preference in
[v0.2](RESEARCH_SPEC_V0_2.md). It preserves the historical [v0.1](RESEARCH_SPEC.md)
claims, H1–H8/WP-00–WP-13 identifiers, evidence standards, and all completed results.
The [v1 handover protocol](HANDOVER_PROTOCOL.md), numerical manifest, implemented
harness, and fixture report remain unchanged. SOAM-035/036 become a retained P2
comparison branch; their eventual results cannot decide the new architecture alone.
No gate is passed by this revision and no unrun study is cancelled or called complete.

## 2. Shared representation, explicit responsibilities

Feature content, relational structure, and action-conditioned transitions should be
tested as patterns, overlapping assemblies, or dynamical modes within a common
population. Cues and context may change which dynamics are expressed. Separate
input/output adapters and diagnostic readouts are allowed; they must not conceal
independent recurrent memories or a graph that performs the candidate's inference.

| Function | Preferred research interpretation | Required comparison or distinction |
| --- | --- | --- |
| Features | Grounded activity in the shared population | Fixed sensory projection; quantify any fitted readout or auxiliary memory |
| Relationships | Associations or constraints among population patterns | Disjoint relation network and explicit relation-table controls |
| Action relations | Directional, action-conditioned evolution among patterns | Symmetric-only, action-shuffled/removed, ordinary recurrent, and separated-memory controls |
| Attention and binding | Selection, compatibility, and instance information carried by activity/cues | Shared weights alone do not demonstrate shared neurons; repeated-instance binding must be tested |
| Learning | Bounded grounded changes to declared persistent dynamics | No writes during prediction; interference across all affected functions |

Sharing must mean that some of the same recurrent units participate in more than
one function. Concatenating three independent networks into one tensor, tying their
weights while storing separate states, or relabeling a bank does not establish this.
Protocols must declare connectivity, recurrent state allocation, overlap, activity
timescales, and any role masks; test causal cross-function effects as well as decoding.
Shared neurons need not mean every neuron serves every role or every task uses one
undifferentiated state. Partial overlap, sparse assemblies, and multiple populations
are legitimate measured alternatives, with all capacity counted.

Functional distinctions remain mandatory even when represented in shared neurons:
estimated actual state versus desired state; observation versus internal prediction;
sensory/memory attention versus motor authority; transient activity versus persistent
parameters; instance information versus generic knowledge; learner input versus
evaluator ground truth. Evidence provenance and write permissions are software
contracts, not demands for a separate neural population per concept.

## 3. A reusable experimental core

[SOAM-047](../tickets/SOAM-047-platform-contract.md) must define concrete interfaces
before [SOAM-048](../tickets/SOAM-048-platform-runner.md) implements them. Reuse
existing code where its contracts fit, without rewriting historical experiment paths.
Keep the common core small and configuration-driven:

- A dynamics backend declares state layout, connectivity, update rule, time step or
  integrator, action/cue/sensory inputs, readouts, persistent storage, and supported
  operations. Symmetry, energy functions, convergence, and concurrency are capabilities
  to specify and test, not assumptions imposed on every backend.
- Task adapters supply permitted observations, executed actions, and declared cues;
  environment truth and future targets stay evaluator-owned. Geometry may generate
  observations or score behavior without becoming the learner's hidden memory.
- Learning policies declare offline fitting, grounded online writes, or no learning,
  with separate training/evaluation modes, snapshots, validation, and rollback.
- A common runner owns split-specific random streams, bounded sweeps, perturbations,
  cue/action/sensory ablations, metrics, artifacts, failures, and reproducibility.
- Each experiment has a versioned protocol/manifest, finite candidate matrix, fixed
  seeds, development-only tuning, reserved confirmation data, stopping conditions,
  and explicit state/weight/buffer/data/compute budgets. No autonomous open-ended sweep.

The design should accommodate classical symmetric Hopfield recall, asymmetric
sequence/transition dynamics, continuous attractor/path-integration models, recurrent
modern-Hopfield/attention candidates, and ordinary RNN/GRU controls. These are a
catalogue of extension points, not an instruction to implement all families at once.
The first platform delivery uses a small synthetic fixture and a second distinct
task fixture to demonstrate reuse before expensive studies. Capability-specific
metrics may be absent with an explicit reason; do not invent a common energy score.

Asymmetric sequence memory has primary-source precedents, but their results are not
proof for this proposed architecture: [Chaudhry et al., Long Sequence Hopfield Memory](https://arxiv.org/abs/2306.04532).
For each selected rule, derive or cite its actual assumptions. In particular, do not
transfer a symmetric-network energy argument to an arbitrary asymmetric update.
Measure fixed-point recovery, cycle/trajectory recovery, and behavior under persistent
forcing separately. Boundedness, routing success, and prediction alone remain insufficient.

## 4. Independent experiment tracks

| Track | Bounded initial question | Tickets |
| --- | --- | --- |
| Shared-population mechanism | Does sharing improve held-out action-conditioned transitions at a declared budget while retaining feature recall? | SOAM-049 protocol → SOAM-050 candidates → SOAM-051 pilot → SOAM-052 claim review and SOAM-059 fork selection |
| Active sensorimotor disambiguation | Can a recurrent belief and informative action resolve aliasing and reach a simple goal with fewer observations? | SOAM-053 protocol decision → SOAM-054 adapter/controls → SOAM-055 study |
| Minimal grounded acquisition | Can one or a few observations improve held-out transitions while preserving earlier behavior after state reset? | SOAM-039 protocol → SOAM-044 candidates → SOAM-040 study → SOAM-041 review |
| Future Monty-style learning module | Can grounded recurrent memory acquire and recognize sensorimotor feature/location structure without a point-cloud/graph as its core learned memory? | SOAM-056 protocol decision → SOAM-057 adapter/controls → SOAM-058 study |
| Historical handover | What does the frozen v1 shared/separated-state comparison support? | SOAM-035 → SOAM-036, retained unchanged experimentally |

Application protocols require the platform contract and explicit selection by
SOAM-059. They do not require a positive shared-population gate or the full SOAM
control/learning chain. Only one experimental continuation is selected at a time. Minimal acquisition is
the preferred first follow-up; the larger Monty module also requires SOAM-041 proceed.
Each selected application still requires its own protocol proceed and the runner
before implementation. Negative sharing results can motivate a conventional or
separated control here, with claim limits recorded. No application success passes
H1–H8 or authorizes continual integration automatically.

The active-disambiguation track begins with a tiny aliased 2D task and a supplied
probe-action policy, not full mapping or 3D reproduction. Freeze memory initially
and cross model choice with active/fixed policies to isolate inference and action.
NeuroSLAM combines attractor-based pose processing with an experience map; it is not
evidence that graphs have already been eliminated. Review the [authors' repository](https://github.com/cognav/NeuroSLAM)
and [paper](https://doi.org/10.1007/s00422-019-00806-9) when freezing the protocol.
Compare a recurrent-memory candidate with odometry, recurrent, and explicit-map
references under equal observations. Report localization, map/loop consistency, and
failure separately; localization alone is not a full SLAM claim.

The learning-module track takes inspiration from Monty's sensorimotor module
responsibilities and reference frames, described in its [official learning-module documentation](https://docs.thousandbrains.org/docs/learning-modules).
It is a proposed alternative memory mechanism, not a claim that Monty uses Hopfield
dynamics or that SOAM is already a compatible replacement. Specify one small
feature/location/action task, observed-data learning, object/pose hypotheses,
uncertainty, and re-identification. Keep point-cloud/graph memory as an explicit
comparison and simulator geometry as evaluator/task infrastructure. A full Monty
integration, multi-module voting, and physical robotics are later scoped work.

## 5. Later SOAM integration and claims

SOAM-052 replaces SOAM-036 as the prerequisite decision for revised shared-population
beliefs, control, and composition planning. Minimal acquisition is now independent
of a positive sharing gate, with alternative learners labeled explicitly. Its proceed identifies useful sharing and interference limits in the minimal pilot.
Explicit fork selection in SOAM-059 is also required before SOAM-037 first tests
concurrent instance binding and handover. Skills remain later work in SOAM-038. SOAM-039/044 select
and implement minimal grounded writes before skills/concurrency; SOAM-040/041 test
acquisition and retention. Replay/shadow infrastructure and SOAM-042/043 organization
are later conditional work; organization still requires the sharing gate. Their historical filenames retain stable links.

These integrated tickets remain distinct from the small application branches, whose
own protocols must define any task-specific learning and no-write invariants. Shared
hardware, shared code, overlapping activity, successful recall, useful reuse, and
learned organization are separate claims. Require causal ablations, held-out tasks,
multi-seed results, and resource accounting appropriate to each. Negative results
may complete an experiment and produce revise/stop at its gate.

Current ordering and metadata live in [PRIORITIES.md](../PRIORITIES.md).
[SOAM-046](../tickets/SOAM-046-shared-platform-scope.md) records this documentation
change only. SOAM-047 now records the platform contract decision; SOAM-049 is next
and SOAM-048's engineering fixtures are ready. This does not activate the entire
catalogue or all application studies.
