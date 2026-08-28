# Model Requirements and Behavior

## Use When
- Requirements remain ambiguous after prose discussion.
- Designing object responsibilities, interactions, workflows, or stateful behavior.
- Deriving tests or architecture from scenarios.

## Required Context
- Validated stakeholder goals, actors, system boundary, and prioritized requirements.
- Main, alternative, error, and abuse scenarios.
- Domain vocabulary and known external systems.

## Instructions
1. Select only models that answer an unresolved question; avoid modeling for inventory.
2. Build scenario models:
   - Identify primary and secondary actors and their goals.
   - State preconditions, trigger, main flow, alternatives, exceptions, and postconditions.
   - Keep actor intent separate from interface detail unless interaction design is the subject.
3. Identify analysis classes from external entities, things, events, roles, organizational units, places, and structures in the problem domain.
4. Assign responsibilities, attributes, operations, and collaborators. Use CRC modeling when collaborative exploration will expose missing responsibilities.
5. Model functional flow when transformation, input/output, or processing sequence needs clarification.
6. Use sequence diagrams to allocate scenario messages to participants and expose interfaces.
7. Derive events from scenarios; model states, transitions, guards, and actions for objects whose behavior depends on lifecycle.
8. Use activity models for concurrent or branching workflows when sequence alone is insufficient.
9. Cross-check models:
   - Every scenario action has a responsible class/component.
   - Every message maps to an operation or interface responsibility.
   - State transitions cover valid and invalid events.
   - Data and constraints remain consistent across views.
10. Review models with stakeholders and designers; update requirements and tests when contradictions are found.

## Decision Rules
- If order and collaboration matter, use a sequence model.
- If response depends on history or lifecycle, use a state model.
- If responsibilities are unclear, use CRC cards before detailed class diagrams.
- If workflow branches or proceeds concurrently, use an activity model.
- If a model does not change a decision, reveal a defect, or support verification, do not maintain it.
- If the model introduces implementation-specific mechanisms prematurely, return to problem-domain abstractions.

## Constraints
- Analysis models describe what and why before committing to how.
- Preserve requirement and scenario identifiers in model elements where traceability is needed.
- Include alternative, invalid, timeout, cancellation, and recovery transitions when material.
- Do not assume one diagram is authoritative; reconcile complementary views.

## Failure Modes
- **Diagram is accurate but useless** — Cause: no question or consumer. Correction: define the decision the model must support.
- **Class model mirrors database or UI prematurely** — Cause: solution detail replaced domain analysis. Correction: rediscover domain responsibilities and behavior.
- **State defects appear in testing** — Cause: only happy transitions were modeled. Correction: add invalid events, guards, terminal states, and recovery.
- **Models drift from implementation** — Cause: no traceability or review trigger. Correction: update or retire models as part of change control.

## Verification
- Each model has a stated purpose and linked requirements.
- Scenario, class, sequence, state, activity, and data views are mutually consistent where they overlap.
- Alternative and error behavior is represented.
- Models provide direct inputs to design or test-case derivation.

## Required Terms
- [CRC model](../glossary.md#crc-model) — defines the responsibility/collaboration technique used before detailed design.

## Source Locators
- Ch 7 §§7.3–7.5, pp. 110–122.
- Ch 8 §§8.1–8.6, pp. 127–154.
- Ch 19 §19.6.2, pp. 392–393, for state-based test derivation.
