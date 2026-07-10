# Engineer and Manage Requirements

## Use When
- Discovering product needs, clarifying a vague feature, or validating scope.
- Reconciling conflicting stakeholder expectations.
- Defining acceptance criteria and managing requirement change.

## Required Context
- Stakeholders, business goals, users, operating environment, constraints, and existing system.
- Known functional behavior, quality attributes, external interfaces, data, and compliance needs.
- Decision authority, priorities, feasibility limits, and expected change rate.

## Instructions
1. Perform inception: identify stakeholders, goals, problem boundaries, existing solutions, and why the work matters.
2. Elicit requirements through collaborative discussion, observation, scenarios, artifacts, prototypes, and context-free questions.
3. Capture multiple viewpoints explicitly; separate needs from proposed solutions.
4. Include nonfunctional requirements such as performance, reliability, usability, security, safety, maintainability, compatibility, and legal constraints.
5. Elaborate requirements into scenarios, domain concepts, data, functions, states, interfaces, constraints, and validation criteria.
6. Negotiate conflicts by ranking stakeholder value, risk, cost, feasibility, and dependencies. Record rejected or deferred scope.
7. Specify requirements at the least formal level that remains clear, consistent, testable, and maintainable.
8. Validate the requirement set for correctness, completeness, consistency, feasibility, necessity, priority, unambiguity, and testability.
9. Establish bidirectional traceability from stakeholder need to requirement, design, code/configuration, and verification evidence.
10. Manage changes: submit, analyze impact, decide, update affected artifacts, communicate, and verify implementation.

## Decision Rules
- If stakeholders describe a solution, ask what goal and constraint make that solution desirable.
- If a requirement uses terms such as fast, intuitive, robust, many, or user-friendly, replace them with observable criteria.
- If viewpoints conflict, do not average them; identify authority, priority, consequences, and viable alternatives.
- If a requirement cannot be tested or reviewed, elaborate it before commitment.
- If uncertainty remains high, prototype the uncertain interaction or technical quality.
- If a change is accepted, update all trace links and regression scope in the same change process.
- If a requested quality cannot be measured directly, define operational scenarios and acceptable bounds.

## Constraints
- Do not assume the first stakeholder represents all users or constraints.
- Do not omit negative, abuse, error, recovery, and boundary scenarios.
- Do not freeze requirements informally; baseline them and manage subsequent change.
- Traceability must be useful for impact and verification, not maintained as disconnected identifiers.

## Failure Modes
- **Correct implementation rejected by users** — Cause: solution matched specification but not stakeholder goal. Correction: strengthen inception, scenarios, and validation.
- **Scope grows without decision** — Cause: requests enter without negotiation or change control. Correction: prioritize and baseline; route additions through impact analysis.
- **Nonfunctional failure discovered late** — Cause: qualities treated as implicit. Correction: define measurable quality scenarios early.
- **Tests do not prove requirements** — Cause: missing traceability or acceptance criteria. Correction: link each requirement to explicit evidence.
- **Specification contradicts itself** — Cause: multiple viewpoints merged without consistency review. Correction: perform structured validation and resolve conflicts.

## Verification
- Stakeholder classes and viewpoints are represented.
- Every requirement has rationale, priority, and observable validation evidence.
- Functional, nonfunctional, interface, data, constraint, error, and recovery needs are addressed.
- Traceability supports both forward verification and backward impact analysis.
- Changes update requirements and dependent work products consistently.

## Required Terms
- [Requirement traceability](../glossary.md#requirement-traceability) — enables impact analysis and auditable validation.
- [Validation](../glossary.md#validation) — distinguishes stakeholder fitness from implementation correctness.

## Source Locators
- Ch 7 §§7.1–7.8, pp. 103–124.
- Ch 8 §8.1, pp. 127–130.
- Ch 18 §18.4, pp. 360–363, for security requirements.
- Ch 19 §§19.3.1–19.3.2, pp. 382–383, for test traceability.
