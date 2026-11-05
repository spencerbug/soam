# Lightweight research RFCs

Classification: **essential for the next experiment**, recommendation R11 in the
[scientific review](../SCIENTIFIC_REVIEW_2026_11_05.md). Use an RFC for a consequential
choice of representation, dynamics, writable memory, information flow, or evaluation
contract. Routine reversible implementation details need no RFC.

Use an existing decision ticket as the owner: SOAM-047 for the minimum experiment
contract, SOAM-049 for E1, SOAM-039 for E2 learning, SOAM-053 for E3 active perception.
An RFC can be the protocol document those tickets already require. Do not create a
second ticket, separate approval ceremony, or duplicate numerical specification.

Aim for one or two pages plus equations/manifest links. Copy [TEMPLATE.md](TEMPLATE.md)
only when useful. Include the problem, linked hypothesis and ticket IDs, primary
research, at least one strong simpler alternative, proposed state/update equations,
assumptions, resource trade-offs, falsification/evaluation, and implementation effects.
State which choices are supplied, fitted, or learned. Include what would change the
decision and what is explicitly deferred.

Workflow:

1. Draft while the owning decision ticket is in progress. Record unresolved points.
2. Review scientific identifiability, baseline competence, information parity,
   no-write/grounding invariants, cost, and the smallest decisive test.
3. Record proceed/revise/stop in the owning ticket with evidence and scope. A proceed
   accepts an experimental contract, not a scientific hypothesis. No additional
   human approval is implied beyond the user's authorization.
4. Before trials, freeze the numerical manifest/version and provenance. Changing
   inference inputs, mechanisms, primary outcomes, or confirmation rules requires
   a new protocol version, rationale, and fresh confirmation streams as applicable.
5. Retain superseded versions and negative reports. Implementation may change behind
   a stable contract after relevant regression checks; do not freeze the whole platform.

Scientific hypotheses live in [HYPOTHESES.md](../HYPOTHESES.md); measured results live
in reports; priorities select eligible work. No RFC changes ticket schema version 2.
The validator checks ticket metadata and links, not scientific adequacy or body-only
branch conditions. Record that manual review before promoting conditional work.
