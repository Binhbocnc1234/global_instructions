# Maintain, Support, and Evolve Software

## Use When
- Correcting defects, adapting to environments, improving a product, or preventing future failure.
- Deciding between patching, refactoring, reengineering, or replacement.
- Organizing user support and maintenance evidence.

## Required Context
- Deployed versions, configuration, architecture, code/data quality, documentation, and tests.
- User reports, telemetry, defects, business value, support cost, and change demand.
- Available expertise, operational constraints, and migration risk.

## Instructions
1. Classify maintenance intent:
   - Corrective: repair faults.
   - Adaptive: respond to environment/platform change.
   - Perfective: improve capability, performance, or usability.
   - Preventive: reduce future failure or maintenance cost.
2. Reproduce and understand the request or failure; identify affected versions, users, data, and conditions.
3. Perform impact and risk analysis across requirements, architecture, interfaces, data, tests, documentation, deployment, and support.
4. Add regression protection for defects before or with correction when feasible.
5. Implement the smallest coherent change that solves the cause, not only the symptom.
6. Review, integrate, regression-test, update documentation, audit configuration, release, and monitor.
7. Use proactive support data—defect trends, telemetry, user channels, maintenance effort, and environment change—to identify emerging work.
8. Refactor code, data, or architecture when structural friction repeatedly blocks valuable change; protect behavior and migrate incrementally.
9. For poorly understood systems, recover knowledge through inventory analysis, document restructuring, reverse engineering, and dependency/data analysis.
10. Use forward engineering or replacement only after evaluating business value, recovered knowledge, migration, coexistence, verification, and rollback.

## Decision Rules
- If a defect can recur, add a regression test or other automated verification.
- If repeated changes touch the same broad area, investigate cohesion, coupling, architecture, and data design rather than continuing patches.
- If code is ugly but stable and unrelated to current value, do not refactor it speculatively.
- If documentation cannot support safe change, reconstruct the minimal current architecture, interfaces, data, and operational procedures needed.
- If replacement risk exceeds incremental evolution, modernize behind stable boundaries.
- If a release changes persistent data or protocol, plan migration, compatibility, verification, and rollback explicitly.

## Constraints
- Maintenance changes use the same engineering, review, testing, configuration, and quality disciplines as new development.
- Preserve user data and operational continuity.
- Do not rewrite solely from frustration; quantify value, cost, risk, and lost knowledge.
- Do not log sensitive user reports or production data indiscriminately.

## Failure Modes
- **Patch causes secondary defects** — Cause: weak impact analysis and regression. Correction: map dependencies and execute affected tests.
- **Same incident repeats** — Cause: symptom correction without root/process action. Correction: add regression and analyze origin.
- **Rewrite stalls** — Cause: hidden requirements and migration complexity. Correction: recover behavior and deliver incremental replacement slices.
- **Support backlog grows indefinitely** — Cause: no classification or value/risk prioritization. Correction: triage by impact, frequency, strategic value, and effort.

## Verification
- Request/failure, affected versions, and expected outcome are reproducible.
- Impact analysis, change, tests, documentation, and configuration are traceable.
- Migration and rollback pass where applicable.
- Monitoring confirms the deployed result and detects recurrence.
- Refactoring/reengineering decisions include economic and risk rationale.

## Required Terms
- [Reverse engineering](../glossary.md#reverse-engineering) — distinguishes recovering understanding from changing behavior.
- [Forward engineering](../glossary.md#forward-engineering) — defines rebuilding from recovered and improved models.

## Source Locators
- Ch 27 §§27.1–27.6, pp. 550–565.
- Ch 22 §22.5, pp. 447–453.
- Ch 23 §23.5, pp. 476–477.
