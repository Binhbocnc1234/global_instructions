# Operational Glossary

## Architectural driver
**Meaning**: A functional requirement, quality-attribute scenario, or constraint that materially shapes architecture.
**Operational significance**: Architecture alternatives must be evaluated against drivers, not fashion.
**Source**: Ch 10 §§10.1–10.5, pp. 182–196.

## Attack surface
**Meaning**: The exposed entry points, data, interfaces, privileges, dependencies, and paths available to an attacker.
**Operational significance**: Security design should reduce exposure before relying on detection.
**Source**: Ch 18 §18.8, pp. 366–367.

## Baseline
**Meaning**: A reviewed and accepted configuration that can be changed only through defined control.
**Operational significance**: Crossing a baseline triggers impact analysis, authorization, and status tracking.
**Source**: Ch 22 §22.1.3, p. 441.

## Basis path testing
**Meaning**: White-box technique that uses control-flow complexity to select a basis set of independent execution paths.
**Operational significance**: Guides structural path coverage but does not replace condition, data-flow, boundary, or behavioral tests.
**Source**: Ch 19 §19.4.1, pp. 384–386.

## Boundary-value analysis
**Meaning**: Black-box technique selecting values at and immediately around input, output, count, and structural limits.
**Operational significance**: Targets edges where software failures occur disproportionately.
**Source**: Ch 19 §19.5.3, pp. 389–390.

## Cost of quality
**Meaning**: Prevention and appraisal costs plus internal and external failure costs.
**Operational significance**: Supports deliberate investment in early quality activities instead of treating them as pure overhead.
**Source**: Ch 15 §15.3.2, pp. 317–319.

## CRC model
**Meaning**: Class-Responsibility-Collaborator cards used to explore analysis classes and their relationships.
**Operational significance**: Helps allocate behavior before detailed class/interface design.
**Source**: Ch 8 §8.3.4, pp. 144–146.

## Cyclomatic complexity
**Meaning**: Quantitative measure of control-flow complexity that indicates the number of independent paths.
**Operational significance**: Supports path-test planning and flags complex logic; it is not a universal quality score.
**Source**: Ch 19 §19.4.1, pp. 384–386.

## Defect amplification
**Meaning**: Multiplication of an undetected early error into downstream design, code, test, and operational defects.
**Operational significance**: Justifies reviewing work before the next activity consumes it.
**Source**: Ch 16 §§16.1–16.2, pp. 326–327.

## Equivalence partitioning
**Meaning**: Black-box technique dividing an input domain into valid and invalid classes expected to behave similarly.
**Operational significance**: Selects high-value representatives while avoiding redundant cases.
**Source**: Ch 19 §19.5.2, p. 389.

## Formal technical review
**Meaning**: Prepared, role-based review of a bounded work product with recorded findings, disposition, correction, and follow-up.
**Operational significance**: Specifies rigor when error propagation or impact justifies more than informal peer checking.
**Source**: Ch 16 §16.6, pp. 332–335.

## Forward engineering
**Meaning**: Construction or reconstruction of software from recovered and improved abstractions and models.
**Operational significance**: Distinguishes deliberate rebuilding from reverse engineering, which only recovers understanding.
**Source**: Ch 27 §27.5.6, p. 565.

## Function point
**Meaning**: Implementation-independent sizing measure based on user-visible inputs, outputs, inquiries, files, and interfaces adjusted for complexity.
**Operational significance**: Supports estimation only when counting rules and local productivity calibration are credible.
**Source**: Ch 25 §§25.6.2–25.6.4, pp. 511–515.

## Functional independence
**Meaning**: Design objective combining high cohesion within a component and low coupling between components.
**Operational significance**: Guides responsibility partitioning and dependency evaluation.
**Source**: Ch 9 §9.3.7, p. 167.

## Indicator
**Meaning**: A metric or combination of metrics interpreted to provide insight into product, process, or project state.
**Operational significance**: Separates raw measurement from decision-oriented interpretation.
**Source**: Ch 23 §23.1.1, pp. 461–462.

## Information hiding
**Meaning**: Concealing design decisions likely to change behind stable interfaces.
**Operational significance**: Prevents volatile knowledge from becoming widespread dependency.
**Source**: Ch 9 §9.3.6, pp. 166–167.

## Open-world software
**Meaning**: Software operating in an evolving environment of independently changing systems, users, assumptions, and requirements.
**Operational significance**: Requires ongoing monitoring, adaptation, and dependency/risk review.
**Source**: Ch 29 §29.4.2, pp. 589–590.

## Quality assurance
**Meaning**: Planned infrastructure, oversight, audit, records, analysis, and reporting that ensure quality-control activities are complete and effective.
**Operational significance**: Prevents QA from being reduced to test execution.
**Source**: Ch 15 §15.4.5, p. 323; Ch 17.

## Quality control
**Meaning**: Direct reviews, inspections, tests, measurements, feedback, and corrections applied to work products.
**Operational significance**: Distinguishes product checking/correction from assurance oversight.
**Source**: Ch 15 §15.4.4, pp. 322–323.

## Regression testing
**Meaning**: Reexecution of selected existing tests to detect unintended effects of change.
**Operational significance**: Requires representative, impact-focused, changed-component, and prior-defect coverage.
**Source**: Ch 20 §20.3, pp. 402–404.

## Requirement traceability
**Meaning**: Bidirectional links among stakeholder needs, requirements, design, implementation/configuration, and verification evidence.
**Operational significance**: Enables impact analysis and proof that required behavior was validated.
**Source**: Ch 7 §7.2.6, pp. 109–110; Ch 19 §19.3.2, p. 383.

## Risk exposure
**Meaning**: Probability of a risk multiplied by its projected loss or impact.
**Operational significance**: Supports prioritization while requiring qualitative judgment where estimates are uncertain.
**Source**: Ch 26 §26.4, pp. 538–542.

## RMMM
**Meaning**: Risk Mitigation, Monitoring, and Management plan.
**Operational significance**: Separates preventive action, observable triggers, and contingency response.
**Source**: Ch 26 §§26.6–26.7, pp. 543–547.

## Scaffolding
**Meaning**: Test drivers and stubs that provide missing callers or collaborators for component testing.
**Operational significance**: Enables isolation but adds non-production overhead and can become unrealistic.
**Source**: Ch 19 §19.2.1, p. 379.

## Sensitivity point
**Meaning**: Architectural decision or property where a small change strongly affects a quality attribute.
**Operational significance**: Focuses architecture analysis and prototyping on consequential choices.
**Source**: Ch 10 §10.7, pp. 201–204.

## Smoke testing
**Meaning**: Frequent build-level tests designed to reveal severe errors that prevent the build's intended function.
**Operational significance**: Provides rapid integration feedback but does not replace regression or validation.
**Source**: Ch 20 §20.2.3, pp. 400–402.

## Software configuration item
**Meaning**: A named software work product or environmental element placed under configuration control.
**Operational significance**: Determines what must be versioned, baselined, audited, and reproducible.
**Source**: Ch 22 §22.1.4, pp. 441–442.

## Software process improvement (SPI)
**Meaning**: Assessed, planned, installed, evaluated, and sustained change to software-process capability and outcomes.
**Operational significance**: Prevents ad hoc process changes from being mistaken for durable improvement.
**Source**: Ch 28 §§28.1–28.2, pp. 569–576.

## SQUARE
**Meaning**: Security Quality Requirements Engineering, a structured security-requirements process.
**Operational significance**: Guides agreement on terms/goals, risk assessment, elicitation, categorization, prioritization, and inspection.
**Source**: Ch 18 §18.4, pp. 360–363.

## Task set
**Meaning**: Adapted collection of actions, tasks, work products, quality checks, and milestones for a framework activity.
**Operational significance**: Is the mechanism for tailoring process rigor without losing required outcomes.
**Source**: Ch 2 §2.3, pp. 23–24.

## Test oracle
**Meaning**: Mechanism or evidence used to decide whether observed test behavior is correct.
**Operational significance**: Becomes critical for AI, simulation, probabilistic, and experience-oriented systems where exact output may be unavailable.
**Source**: Ch 21 §§21.10–21.11, pp. 428–434.

## Umbrella activity
**Meaning**: Cross-cutting activity applied throughout the process, including tracking, risk, SQA, reviews, measurement, SCM, reuse, and work-product preparation.
**Operational significance**: Prevents these activities from being deferred to the end.
**Source**: Ch 1 §1.3.2, p. 11.

## Validation
**Meaning**: Activities establishing that the software satisfies stakeholder needs—the right product was built.
**Operational significance**: Requires requirement and user evidence beyond implementation correctness.
**Source**: Ch 19 §19.1.1, pp. 373–374.

## Verification
**Meaning**: Activities establishing that software correctly implements specified functions—the product was built right.
**Operational significance**: Keeps conformance evidence distinct from product fitness.
**Source**: Ch 19 §19.1.1, pp. 373–374.

## W5HH principle
**Meaning**: Planning questions: why, what, when, who, where, how, and how much.
**Operational significance**: Exposes missing purpose, scope, ownership, coordination, method, schedule, and resources.
**Source**: Ch 24 §24.6, pp. 501–502.
