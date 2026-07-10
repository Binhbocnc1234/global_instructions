# Select and Tailor a Software Process

## Use When
- Starting or restructuring a software effort.
- Choosing between sequential, prototyping, evolutionary, agile, or hybrid work.
- Deciding how much process, documentation, review, and control a project needs.

## Required Context
- Product goals, stakeholders, constraints, expected lifetime, and release expectations.
- Requirement stability and the cost of obtaining feedback.
- Technical, business, safety, security, and schedule risks.
- Team size, experience, distribution, and organizational constraints.
- Required standards, audits, work products, and approval gates.

## Instructions
1. Establish the generic framework: communication, planning, modeling, construction, and deployment.
2. Identify umbrella activities needed across the entire effort: tracking and control, risk management, SQA, technical reviews, measurement, configuration management, reuse management, and work-product preparation.
3. Characterize the project before selecting a flow:
   - Use a more sequential flow when requirements are stable, handoffs must be auditable, and late change is unlikely.
   - Use prototyping when requirements, interaction, feasibility, or stakeholder expectations are unclear.
   - Use evolutionary or agile increments when change is expected and useful feedback can be obtained from partial capability.
   - Use parallel flows when independent components can progress concurrently without hiding integration risk.
4. Define a task set for each framework activity: actions, tasks, work products, quality checks, and milestones.
5. Tailor task depth to project size, complexity, criticality, team capability, and stakeholder need. Preserve required outcomes even when reducing artifacts.
6. Define how progress will be demonstrated. Prefer reviewed work products, executable increments, tests, and stakeholder evaluation over activity counts.
7. Reassess the process after early increments and whenever assumptions, risks, staffing, or constraints change.

## Decision Rules
- If requirements are stable and change control dominates, use a plan-driven sequence with explicit baselines.
- If stakeholders cannot evaluate abstract requirements, build the smallest prototype that exposes the uncertain behavior.
- If a prototype uses expedient architecture or weak quality controls, discard or deliberately reengineer it before production use.
- If usable functionality can be delivered in coherent slices, prefer evolutionary delivery because evidence arrives earlier.
- If the team adopts agile practices, retain planning, architecture, testing, configuration control, and quality assurance; agility changes cadence, not engineering obligations.
- If work-in-progress queues grow, limit concurrent work and finish/integrate existing increments before starting more.
- If a prescribed practice has no project-relevant purpose, tailor it; if removing it would hide risk or eliminate required evidence, keep it.

## Constraints
- Do not treat any process model as universally applicable.
- Do not interpret agility as absence of documentation, design, or discipline.
- Do not let a prototype become the operational product by accident.
- Do not optimize local task utilization at the expense of integrated, validated progress.
- Testing, review, measurement, risk management, and configuration control must begin before final construction is complete.

## Failure Modes
- **Late discovery of misunderstood needs** — Cause: sequential commitment under uncertainty. Correction: introduce elicitation, scenarios, and early prototypes.
- **Endless prototyping** — Cause: no evaluation criteria or go/no-go decision. Correction: attach a decision and bounded question to every prototype.
- **Ceremony without evidence** — Cause: process compliance measured instead of product outcomes. Correction: require executable or reviewable evidence at milestones.
- **Constant reprioritization without completion** — Cause: uncontrolled intake and excessive WIP. Correction: stabilize a short increment and limit active work.
- **Process rejection by the team** — Cause: imposed activities with unclear value. Correction: connect every activity to risk, quality, coordination, or stakeholder evidence.

## Verification
- The selected flow explicitly matches requirement uncertainty and feedback cadence.
- Each framework activity has an adapted task set and observable completion evidence.
- Umbrella activities have owners or explicit execution mechanisms.
- Prototype continuation criteria and production-code policy are documented.
- The process includes a feedback point at which it can be adjusted.

## Required Terms
- [Task set](../glossary.md#task-set) — determines the concrete rigor applied inside a framework activity.
- [Umbrella activity](../glossary.md#umbrella-activity) — prevents cross-cutting quality work from being deferred.

## Source Locators
- Software Engineering: A Practitioner's Approach, 9th ed., Ch 1 §§1.3–1.4, pp. 9–15.
- Ch 2 §§2.1–2.6, pp. 21–35.
- Ch 3 §§3.1–3.5, pp. 38–51.
- Ch 4 §§4.1–4.10, pp. 57–72.
- Ch 6 §§6.1–6.2, pp. 85–100.
