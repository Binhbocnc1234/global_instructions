# Improve Process and Adopt Emerging Practices

## Use When
- Changing engineering workflow, standards, tools, or organizational practices.
- Evaluating CMMI, SPICE, TDD, model-driven, search-based, AI-assisted, or other emerging approaches.

## Required Context
- Measured product/process problem, baseline capability, stakeholder goals, and constraints.
- Proposed practice, evidence, adoption cost, training, integration, and risks.
- Pilot scope and success/failure measures.

## Instructions
1. Define the improvement problem using product and process evidence; do not begin from a desired maturity label or tool.
2. Assess current practice and perform gap analysis against the outcome required.
3. Select a focused change that addresses the gap; use frameworks such as CMMI, SPICE, or TickIT Plus as diagnostic/reference structures, not ends.
4. Explain rationale and expected behavior change to affected people; provide education, training, and support.
5. Plan installation/migration, ownership, resources, compatibility, and rollback.
6. Pilot on a bounded representative workflow before broad adoption.
7. Measure product quality, cycle time, rework, risk, user/developer outcomes, and unintended behavior.
8. Evaluate against baseline and cost; refine, adopt, or reject.
9. Institutionalize successful practice through workflow, tooling, documentation, review, onboarding, and continued measurement.
10. Reassess periodically because context and technology change.
11. For emerging trends, identify the enduring problem, changed constraint, claimed mechanism, evidence quality, new dependencies, and failure modes.

## Decision Rules
- If no measured problem or strategic opportunity exists, do not impose a process change.
- If a framework practice does not fit local risk and goals, tailor it while preserving the intended outcome.
- If a pilot cannot define success and rollback, reduce its scope before starting.
- If a tool improves local speed but increases review, security, or maintenance cost, evaluate net system outcome.
- If evidence is vendor-controlled, anecdotal, or from unlike contexts, treat expected benefit as uncertain.
- If adoption depends on specialist knowledge, include continuity and training before scaling.
- If a trend automates judgment, retain accountable human verification for high-impact decisions.

## Constraints
- Do not use maturity levels as team-performance scores.
- Process improvement itself requires risk management.
- Preserve project-specific quality, security, and configuration obligations during migration.
- Do not institutionalize a pilot until representative evidence supports it.
- Open-source or AI-generated inputs require provenance, license, security, and quality review.

## Failure Modes
- **Process exists only in documentation** — Cause: no workflow integration or ownership. Correction: embed triggers, artifacts, checks, and training.
- **Tool adoption increases total work** — Cause: local automation shifted cost downstream. Correction: measure end-to-end rework and quality.
- **Pilot success does not scale** — Cause: unrepresentative scope or specialist dependency. Correction: expand gradually and test operating constraints.
- **Maturity chase creates bureaucracy** — Cause: assessment score replaced product outcome. Correction: return to gap and ROI evidence.

## Verification
- Improvement traces to a measured problem or opportunity.
- Gap, selected practice, risks, pilot, training, measures, and rollback are explicit.
- Evaluation compares baseline and net outcome.
- Institutionalized practices have owners and workflow triggers.
- Trend adoption records provenance, limitations, and verification obligations.

## Required Terms
- [SPI](../glossary.md#software-process-improvement-spi) — defines the complete improvement cycle rather than ad hoc optimization.
- [Open-world software](../glossary.md#open-world-software) — explains why assumptions and dependencies continue changing.

## Source Locators
- Ch 28 §§28.1–28.7, pp. 569–581.
- Ch 29 §§29.1–29.7, pp. 584–600.
