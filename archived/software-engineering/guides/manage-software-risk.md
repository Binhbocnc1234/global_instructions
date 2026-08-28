# Manage Software Risk

## Use When
- Planning projects, architecture, security, releases, migrations, or process changes under uncertainty.
- Prioritizing prevention and contingency effort.

## Required Context
- Objectives, scope, assumptions, constraints, stakeholders, and failure consequences.
- Product size/complexity, technology, people, process, environment, dependencies, schedule, and business conditions.
- Existing controls, evidence, and decision authority.

## Instructions
1. Adopt a proactive strategy: identify uncertain conditions before they become problems.
2. Identify generic and product-specific risks across product, business, project, technical, people, process, environment, security, safety, and external dependencies.
3. Phrase each risk as a condition and consequence rather than a vague concern.
4. Estimate probability and impact; consider performance, support, cost, schedule, business, safety, and reputation consequences.
5. Build and rank a risk table using exposure and qualitative judgment; avoid false numeric precision.
6. Refine high-priority risks into drivers, subconditions, and failure paths that can be acted on.
7. Assign an owner and define RMMM:
   - Mitigation reduces probability or impact before occurrence.
   - Monitoring defines observable indicators, thresholds, and review cadence.
   - Management defines contingency actions if the risk materializes.
8. Integrate mitigation and monitoring tasks into the plan, budget, architecture, tests, and release criteria.
9. Review risks regularly and whenever scope, technology, staffing, dependencies, or evidence changes.
10. Close risks only when no longer relevant, realized and managed, or explicitly accepted by authorized stakeholders.

## Decision Rules
- If impact is catastrophic, do not dismiss a risk solely because probability is uncertain or estimated low.
- If exposure is high and mitigation is cheap, mitigate early.
- If mitigation cost exceeds exposure, monitor or accept only with explicit rationale and authority.
- If a risk cannot be observed before failure, seek leading indicators, prototypes, tests, or architectural containment.
- If multiple risks share a driver, address the driver rather than funding duplicate responses.
- If a contingency cannot be executed under incident conditions, rehearse or simplify it.

## Constraints
- A risk is uncertain; an existing issue belongs in issue/defect management, though it can create secondary risks.
- Every material risk requires an owner.
- Risk acceptance must identify residual consequence and decision authority.
- Do not hide schedule or quality risk inside optimistic estimates.
- Maintain security/safety confidentiality without preventing accountable review.

## Failure Modes
- **Risk register never changes work** — Cause: risks detached from plan and ownership. Correction: schedule mitigation/monitoring and review triggers.
- **Everything is high risk** — Cause: no prioritization criteria. Correction: compare probability, impact, exposure, and urgency.
- **Known issue called risk** — Cause: avoidance of action. Correction: manage the issue now and identify only uncertain consequences as risks.
- **Contingency fails during crisis** — Cause: untested assumptions. Correction: simulate, rehearse, and maintain resources.

## Verification
- Risks are specific condition/consequence statements.
- Probability, impact, priority, owner, mitigation, indicators, and contingency are recorded for material risks.
- Risk work appears in project tasks and tests.
- Review cadence and triggers are active.
- Accepted residual risks have authorized rationale.

## Required Terms
- [Risk exposure](../glossary.md#risk-exposure) — guides prioritization while retaining qualitative judgment.
- [RMMM](../glossary.md#rmmm) — distinguishes mitigation, monitoring, and contingency management.

## Source Locators
- Ch 26 §§26.1–26.8, pp. 533–547.
- Ch 17 §17.2, pp. 341–343.
- Ch 18 §18.6–18.7, pp. 364–366.
