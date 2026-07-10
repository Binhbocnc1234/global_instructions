# Evolve and Evaluate Software Increments

## Use When
- Developing a product through prototypes, agile iterations, or staged releases.
- Deciding whether to continue, redirect, rebuild, release, or stop an increment.
- Managing the cost of change through frequent validation.

## Required Context
- The user or business question the increment must answer.
- Acceptance and validation criteria, including nonfunctional qualities.
- Preliminary architecture and dependencies needed for the slice.
- Resource estimate, technical risks, and time available for evaluation.
- Whether code is exploratory, production-intent, or deliberately disposable.

## Instructions
1. Define the increment in customer-valuable terms and state its evaluation question.
2. Establish preliminary architecture sufficient to constrain interfaces, data, and risky dependencies.
3. Estimate people, reusable assets, environment, effort, and schedule as ranges with assumptions.
4. Build the smallest coherent vertical slice that can be evaluated in its intended context.
5. Design tests before or during construction. Include functional, behavioral, performance, interface, and risk-driven checks.
6. Integrate continuously enough that the increment remains demonstrable.
7. Evaluate with stakeholders using agreed criteria; collect defects, usability observations, performance data, and change requests.
8. Make an explicit decision:
   - Continue when value and feasibility are supported.
   - Redirect when evidence invalidates assumptions but a viable alternative exists.
   - Rebuild when the concept is valid but exploratory implementation is unsuitable.
   - Stop when value, feasibility, risk, or resources do not justify continuation.
9. Define the next increment from new evidence, not from the original plan alone.
10. Before release, rerun functional and nonfunctional regression, audit the configuration, and prepare support.

## Decision Rules
- If the uncertainty is primarily usability, favor a thin interaction prototype with representative users.
- If the uncertainty is architectural or performance-related, exercise realistic data, load, and integration paths.
- If an increment cannot be evaluated by a stakeholder or test, reduce or reshape it until evidence is possible.
- If feedback changes requirements, update traceability, models, tests, estimates, and risks together.
- If exploratory shortcuts threaten quality attributes, rebuild rather than normalize the shortcuts.
- If release criteria are met but operational risk remains, release only with explicit mitigation, monitoring, and rollback.

## Constraints
- An increment must be coherent; disconnected component completion is not a customer-valuable increment.
- Demonstration does not replace verification of error paths, performance, security, or maintainability.
- A go decision does not freeze learning; plans and requirements remain managed artifacts.
- Do not continue solely because effort has already been spent.

## Failure Modes
- **Prototype looks convincing but fails in production** — Cause: evaluation covered appearance, not operational qualities. Correction: add realistic load, data, failure, and integration criteria.
- **Increment repeatedly expands** — Cause: no bounded question or acceptance definition. Correction: split future value from current evaluation scope.
- **Feedback cannot be reconciled** — Cause: stakeholder viewpoints and priority rules were not established. Correction: negotiate value, risk, and constraints explicitly.
- **Release cannot be reproduced** — Cause: uncontrolled code, assets, dependencies, or configuration. Correction: baseline and audit the exact release configuration.

## Verification
- The increment has a stated question, scope, and observable acceptance criteria.
- Architecture and risks are sufficient to explain why the slice is feasible.
- Evaluation includes user and technical evidence.
- The continue/redirect/rebuild/stop decision is recorded with rationale.
- The next increment reflects evaluation results and updated risk.

## Source Locators
- Ch 3 §§3.3–3.5, pp. 40–51.
- Ch 4 §§4.1–4.10, pp. 57–72.
- Ch 20 §20.2.3, pp. 400–402.
- Ch 22 §22.4, pp. 446–447.
