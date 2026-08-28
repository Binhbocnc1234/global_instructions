---
type: technical
audience: agent
status: active
language: en
description: Defines the software-quality model and the evidence needed to apply it.
---

# Software Quality Model

Use this reference to select and operationalize product-quality and quality-in-use requirements. It retains the ISO/IEC 25010 model summarized in the archived `software-engineering` skill's source: *Software Engineering: A Practitioner's Approach*, 9th edition, Chapter 15, pp. 313–314. It is not a substitute for a current standard, legal requirement, or platform-specific accessibility guidance.

## Operationalize a Quality Requirement

1. Identify the stakeholder, task, operating environment, failure consequence, and change scope.
2. Select only material characteristics; do not score every characteristic by default.
3. Write a measurable scenario: `Given <context/trigger>, when <stimulus>, <system or user> achieves <response>, measured by <metric> <=/>= <threshold>.`
4. State the evidence method and owner: automated test, static analysis, benchmark, prototype, technical review, user study, or production measurement.
5. Record meaningful trade-offs and residual risk. Re-evaluate the scenario when its architecture, platform, workload, or user context changes.

Example: `On the lowest supported device, when a player opens a saved game with 1,000 entities, the scene is interactive within 2 seconds in 95% of 30 cold-start runs.`

## Product Quality

Use these characteristics to assess the static and dynamic properties of the system.

| Characteristic | Subcharacteristics to consider |
|---|---|
| Functional suitability | Functional completeness, correctness, appropriateness |
| Performance efficiency | Timing behavior, resource utilization, capacity |
| Compatibility | Coexistence, interoperability |
| Usability | Appropriateness, learnability, operability, user-error protection, aesthetics, accessibility |
| Reliability | Maturity, availability, fault tolerance, recoverability |
| Security | Confidentiality, integrity, accountability, authenticity |
| Maintainability | Modularity, reusability, modifiability, testability |
| Portability | Adaptability, installability, replaceability |

## Quality in Use

Evaluate these characteristics with a specific user, task, and context rather than inferring them only from product properties.

| Characteristic | Meaning |
|---|---|
| Effectiveness | Accuracy and completeness with which users achieve goals |
| Efficiency | Resources users expend to achieve goals accurately and completely |
| Satisfaction | Usefulness, trust, pleasure, and comfort |
| Freedom from risk | Mitigation of economic, health, safety, and environmental risks |
| Context coverage | Completeness and flexibility across intended contexts |

## Select Evidence by Characteristic

| Characteristic | Typical evidence |
|---|---|
| Functional suitability | Requirement-to-test traceability, acceptance scenarios, negative cases |
| Performance efficiency | Representative load or device benchmark with a budget |
| Compatibility and portability | Explicit support matrix; integration, installation, upgrade, and rollback checks |
| Usability and quality in use | Representative-task observation, success rate, time, errors, recovery, and qualitative feedback |
| Reliability | Failure-rate, availability, recovery, fault-injection, and resilience evidence suited to the system |
| Security | Threat model, control review, security tests, and accepted residual risk |
| Maintainability | Cohesion and dependency review, change effort, code readability, tests, and successful scoped modification |

Do not replace representative user evidence with an internal quality score. Do not state that a quality has been achieved without evidence from the selected scenario.
