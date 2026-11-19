# SOAM north star

**Long-term direction clarified by the project owner on November 19, 2026.**

SOAM aims to build sensorimotor intelligence that develops its own useful
organization of the world through experience. An agent should learn what persists,
what changes, how its actions affect its surroundings, and how earlier experiences
can help it understand unfamiliar situations. Its memory should continually acquire
and reorganize that knowledge. Language may eventually express and connect these
grounded concepts to human concepts; it need not supply their initial structure.

The ultimate capability is a robot with a world model developed through its own
sensing and action. The research question is how plastic recurrent dynamical systems
could support that development, including the discovery of reusable memory structure.
Play is a central route toward this capability: the agent should create informative
experiences through its own activity, then use them to construct and revise its model.

## Intelligence grounded in interaction

The agent learns through a continuing loop: observe, form expectations, act, encounter
the consequences, and revise its model. Actions make it possible to investigate
ambiguity and discover relationships that a single observation cannot reveal.
Objects, locations and action possibilities should increasingly become useful
structures the agent learns, rather than identities and relationships supplied by
the evaluator.

A concept earns its meaning through what it lets the agent distinguish, predict
and do. An agent might learn that different sensory encounters concern the same
object because it can move between views, track the changes and recover consistent
expectations. It might distinguish two similar objects because an interaction
reveals different behavior. Later, a word could refer to that learned distinction.
Naming it is a further capability; the grounded distinction can exist beforehand.

There is a limited research precedent for this direction: sensorimotor prediction
has produced aspects of egocentric spatial topology and metric regularity in bounded
simulations under particular exploration conditions. This motivates investigating
how much more structure interaction can support. [Laflaquière and Garcia Ortiz,
2019](https://proceedings.neurips.cc/paper/2019/hash/0dd1bc593a91620daecf7723d2235624-Abstract.html)

## Generating a world model through play

The owner's parser/generator distinction describes two routes to learned structure.
A language model can recover relationships already expressed in human language;
SOAM aims to construct grounded relationships through encounters with the physical
world, including encounters the agent initiates. In this sense it should be a
generator of its own world model and of the experiences that develop it. This is a
metaphor for how knowledge is acquired: language models also generate outputs, and
the existence of a universal representational geometry remains a hypothesis.

The owner's example is his four-year-old son playing with a necklace after dinner.
Holding one end in each hand, the child swung it like a small rope, changed the
distance between his hands, and watched the motion change and appear to speed up as
he pulled it taut. He repeated the movement several times, then invited his father:
"Dad, look what I can do. You try."

This illustrates the behavior SOAM should eventually support: initiate an interaction,
notice an effect, repeat it, vary it, and acquire an expectation about the relationship
between movement and outcome. The child did not need to state an equation before
exploring the phenomenon.

For a robot, play should produce reusable sensorimotor knowledge beyond a recording
of one successful performance. It should learn which variations preserve an effect,
which change it, and where its expectations fail. Selecting interesting interactions,
deciding when to repeat or vary them, and recognizing useful learning progress are
part of the open problem. Replaying a supplied motion alone would leave those
discovery capabilities unexplained.

## A proposed circuit for action and observation

One candidate play circuit couples two recurrent processes:

- **Action generation:** a process develops a sequence of projected sensorimotor
  states associated with short action chunks, such as initiating a swing, sustaining
  it and changing hand separation. Selected chunks guide an explicit motor controller
  that produces movement.
- **Observation and acquisition:** a process follows actual sensory observations
  and executed-action information, forming a provisional memory of the experienced
  trajectory. A first encounter can contribute persistent information without being
  sufficient to establish the whole physical relationship.
- **Alignment across repetitions:** subsequent encounters retrieve and refine the
  earlier trajectory. The intended correspondence is frame by frame or chunk by
  chunk where appropriate, with room for differences in timing, speed and phase.
  Alignment itself must be learned or explicitly identified as supplied scaffolding;
  identical timestep indices cannot substitute for it.
- **Reciprocal prediction:** the action process predicts sensory consequences, while
  the observation process constrains the likely action phase, compatible movement
  sequences and expected continuation. Mismatches can redirect action and, after
  grounded experience, revise persistent associations.

In the necklace example, a repeated swing-and-pull sequence would become recognizable
as an evolving interaction. Its developing action representation would anticipate
what should be observed next, and its sensory representation would help establish
where the agent is in that sequence. Observations may support several possible
actions; reciprocal prediction need not assume a unique inverse from sensation to
motor command. The aim is useful mutual constraint while retaining uncertainty.

Desired or projected states, estimated actual states, sensory evidence and motor
authority remain distinct. Imagined consequences and internal agreement between the
processes do not count as new observations or authorize persistent writes. Learning
from play must remain grounded in what was actually sensed and done, consistent with
the project's existing inference and learning boundaries.

This is an owner-proposed example of a future capability, not a claim that exactly
two separate populations are necessary or that such a circuit has been demonstrated
in SOAM. It leaves learning rules, chunk discovery, sequence alignment, coupling and
the selection of play activities open. Many other capabilities would be needed for
the eventual robot; this circuit is one way to make the broader goal concrete.

## Memory that learns its organization

Memory organization is central to the goal. The useful analogy is assembling a
puzzle while also learning what its pieces are. Experience may reveal that fragments
belong together, that a previously unified fragment contains an important distinction,
or that a relationship applies across many previously separate situations.

The intended capabilities include:

- **Integration:** connect different encounters with the same underlying structure
  while retaining distinctions such as viewpoint and context.
- **Differentiation:** separate similar experiences when their different consequences
  matter, while preserving the features they still share.
- **Reuse:** apply a learned fragment or relationship in a new combination without
  needing an independently stored example of that whole combination.
- **Reorganization:** let new evidence revise families of related expectations while
  retaining useful earlier knowledge and the ability to distinguish individual cases.

Distributed representations and shared plastic connections are candidate mechanisms
for these capabilities. One connection change can influence many associations;
overlapping populations may reuse parts of a representation across functions. The
same sharing can also cause interference. Useful organization requires learning
when to share, when to distinguish, and how to preserve information during revision.

We do not yet have a demonstrated learning process that accomplishes this for SOAM.
Recurrence supplies dynamics; plasticity changes those dynamics. The central open
problem is to identify learning signals and update rules that make those changes
produce useful organization. We may supply a learning rule without specifying the
organization it will discover. Learning to revise the learning rule itself is an
additional possibility, not a prerequisite imposed by this goal.

## A world model shaped by the agent

A robot encounters the same physical world through a different body, sensor suite
and range of actions. Our working expectation is partial representational alignment:
agents may discover corresponding physical relationships while developing different
distinctions and action possibilities. Shared laws alone do not guarantee that every
agent can observe or learn every relevant relationship.

For example, a narrow robot and a wide robot could agree about a passage's dimensions
while learning different possibilities for traversing it. A lidar-equipped robot
could develop categories of return patterns that people ordinarily encounter only
through instruments. Such categories could eventually receive names, even when they
have no familiar counterpart in unaided human perception.

An agent with a variable internal processing rate could also develop temporal
abstractions suited to its own sensing and control. This operational possibility,
sometimes called framejacking, does not establish a human-like subjective experience
of time. Human affective and homeostatic drives are not required design targets.
The robot's objectives, energy limits and other physical constraints would still
shape which distinctions are useful to it.

The intended world model is **self-developed and prelinguistic**. Its architecture,
learning rules and initial interfaces supply biases, while experience shapes the
learned organization. This distinguishes acquired structure from an innate model
already specified by the designer. Biological findings can inform the mechanisms
without making biological imitation or human representational identity a condition
of success.

## Shared geometry as a research hypothesis

The Platonic Representation Hypothesis offers a related motivation: models trained
on different data and modalities may converge toward aspects of a shared statistical
representation of reality. Its authors report representational alignment and discuss
limits arising from differences between modalities and tasks. A universal geometry
underlying all human language remains a stronger, unestablished hypothesis.
[Huh et al., 2024](https://proceedings.mlr.press/v235/huh24a.html)

If such a universal structure existed, it would suggest strong common constraints
on human meaning. Shared biology, cognitive capacities, developmental experience,
cultural transmission and physical reality could all contribute. Universality alone
would not identify which causes dominate or prove that the structure is present
before experience. Statistical regularities can themselves reflect physical and
social structure; these explanations need not be mutually exclusive.

SOAM makes this motivation concrete by asking what an agent can discover through
sensorimotor interaction before learning language. Which relationships would align
across agents with different bodies and sensors? Which would depend on their access
to the world, objectives or experience? Could a later language interface communicate
both the shared structure and distinctions specific to the robot?

Alignment should concern meaningful relationships and transformations. Different
coordinate bases can express equivalent structure. Conversely, a similar-looking
embedding is weak evidence if the agent cannot use its relationships to predict
interventions or generalize. The capability goal does not depend on discovering one
unique universal representation, and human alignment should be measured rather than
imposed as the answer.

## Why investigate recurrent memory

SOAM's preferred hypothesis is that persistent knowledge, associative retrieval and
action-conditioned prediction can use overlapping recurrent neurons and connections.
A sufficiently adaptable substrate might allow functional roles and interactions to
develop through learning. It could give memory organization a direct influence on
the agent's ongoing inference and behavior.

This leaves room for multiple populations, partial overlap, specialized dynamics and
learned interfaces. It does not require every function to occupy one undifferentiated
population or every interaction to descend a symmetric energy function. Representation,
inference dynamics and persistent learning remain separate things to specify and test.

KV, ordinary recurrent, structured-memory and hybrid systems remain serious controls
and possible components. A KV store can contain distributed learned vectors; a
recurrent network can memorize fixed supplied patterns. Neither storage format alone
establishes learned organization. Conventional retrieval success should be credited,
and a more elaborate recurrent mechanism must earn its added complexity. A useful
robot and evidence for a particular SOAM mechanism are distinct achievements.

## Evidence of progress

The following are qualitative signs of progress toward the long-term goal. Individual
protocols must turn selected questions into bounded tests with explicit criteria.

- New grounded experience changes persistent knowledge that survives transient-state
  reset, while retaining useful earlier behavior.
- The agent learns shared structure and consequential distinctions without receiving
  the corresponding identities, partitions or complete relationship graph.
- Acquired knowledge supports unfamiliar combinations, viewpoints or action sequences,
  with appropriate uncertainty when evidence is insufficient.
- The agent uses actions to resolve uncertainty and improves predictions and behavior
  as its organization changes.
- Self-directed play produces knowledge that transfers to changed conditions and new
  action sequences, beyond reproducing the interactions through which it was acquired.
- Learned relationships transfer where information is shared across settings or
  embodiments, while differences caused by sensing and action remain intelligible.

Learned organization needs evidence beyond attractive latent plots, activation
overlap or improved prediction alone. Its claimed structure must contribute to useful
behavior under suitable causal controls. Real robotics is the eventual setting;
small simulations and declared scaffolding can isolate prerequisites on the way.

## Relationship to the current research program

This direction develops the embodied world-model aim in the original
[v0.1 specification](RESEARCH_SPEC.md) alongside the adopted
[v0.3 experiment-platform scope](RESEARCH_SPEC_V0_3.md). It clarifies why learned
organization matters without prescribing a successful architecture in advance.

The completed studies establish bounded component results. [Study D](../reports/STUDY_D_DECISION.md)
retains KV as the reliable reference for its scaffolded acquisition task.
[D-R1](../reports/STUDY_D_R1_DECISION.md) records PH768's failed sequential-retrieval
guards and a settling benefit below the frozen practical margin. Its fixed
representation did not test discovery of memory fragments or their organization.
Those outcomes remain evidence that subsequent work must explain and respect.

The [hypothesis ledger](HYPOTHESES.md) owns operational claims, protocols own frozen
criteria, reports own measurements, and decision tickets interpret results.
[PRIORITIES.md](../PRIORITIES.md) and the [research paths](RESEARCH_PATHS.md) select
eligible work. This north star describes the destination; it does not select another
experimental fork, renew an allocation or revise a historical gate. Early fixed
sensory projections and other protocol commitments remain in force until explicitly
replaced by a new scoped contract.
