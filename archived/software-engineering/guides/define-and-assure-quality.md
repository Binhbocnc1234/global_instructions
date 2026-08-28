# Define, Control, and Assure Software Quality

## Use When
- Defining product quality goals or a project quality plan.
- Deciding which prevention, review, testing, audit, and measurement activities are required.
- Investigating recurring defects or weak quality evidence.

## Required Context
- Stakeholder value, product risks, failure consequences, and operating environment.
- Functional and nonfunctional requirements.
- Applicable standards, organizational practices, release criteria, and available resources.
- Current defect, review, test, and process data.

## Instructions
1. Define quality for the product through observable factors and stakeholder value; avoid a single universal score.
2. Establish quality goals for requirements, design, code, testing, support, security, and safety where applicable.
3. Analyze cost of quality:
   - Prevention: planning, training, complete requirements/design, and test planning.
   - Appraisal: reviews, audits, measurement, testing, and debugging.
   - Internal failure: rework and downstream correction before release.
   - External failure: support, reputation, liability, harm, and correction after release.
4. Select engineering methods and management practices that prevent predictable errors.
5. Define quality-control actions for each work product: review, inspection, analysis, test, measurement, and feedback.
6. Define quality-assurance oversight: standards, planned evaluations, audits, records, deviation handling, reporting, and corrective follow-up.
7. Create an SQA plan covering scope, controlled work products, standards, reviews/audits, testing oversight, configuration management, records, roles, and feedback.
8. Collect defect origin, detection stage, severity, correction effort, and recurrence data.
9. Analyze concentrations and escapes; change prevention or detection where evidence shows weakness.
10. Report quality truthfully and make release decisions using requirements, risk, open defects, reliability, and stakeholder criteria.

## Decision Rules
- If external failure consequences are high, increase prevention, independent review, and validation rigor.
- If defects cluster in one origin activity, improve that activity and its immediate review rather than only adding downstream tests.
- If a standard adds evidence required by stakeholders or risk, enforce it; otherwise tailor without pretending compliance.
- If quality data identify a problem, assign corrective action and resources; reporting alone is not assurance.
- If a product is labeled “good enough,” document which quality goals, risks, and stakeholder trade-offs justify that judgment.
- If schedule pressure requires trade-offs, reduce scope before silently removing critical quality controls.

## Constraints
- Quality assurance is broader than testing.
- Testing cannot compensate for poor requirements, design, or uncontrolled change.
- Metrics must not be used to punish individuals or conceal uncertainty.
- Deviations and noncompliance remain open until corrected or explicitly accepted by authorized stakeholders.

## Failure Modes
- **High test effort, low release confidence** — Cause: quality goals and traceability are unclear. Correction: define measurable goals and evidence paths.
- **Same defect class recurs** — Cause: correction without process learning. Correction: analyze origin and add prevention/checklist/test action.
- **Quality plan is unused** — Cause: generic plan detached from workflow. Correction: assign activities to actual milestones, roles, and artifacts.
- **Green metrics, unhappy users** — Cause: measures do not represent stakeholder quality. Correction: revisit goals and operational indicators.

## Verification
- Quality goals are measurable or operationally assessable.
- Prevention, appraisal, review, testing, audit, and configuration activities are assigned.
- SQA records support traceability from deviation to resolution.
- Defect analysis produces process or product action.
- Release criteria include product value and risk, not only test pass count.

## Required Terms
- [Cost of quality](../glossary.md#cost-of-quality) — changes how prevention and failure trade-offs are evaluated.
- [Quality assurance](../glossary.md#quality-assurance) — distinguishes process oversight from product-control activities.
- [Quality control](../glossary.md#quality-control) — identifies direct checks and corrections on work products.

## Source Locators
- Ch 15 §§15.1–15.5, pp. 311–323.
- Ch 17 §§17.1–17.10, pp. 341–355.
- Ch 23 §§23.8–23.9, pp. 482–487.
