# Conduct Technical Reviews

## Use When
- Reviewing requirements, models, architecture, code, tests, documentation, or release work products.
- Choosing review formality based on risk.
- Improving review effectiveness and follow-up.

## Required Context
- Review objective, bounded work product, applicable requirements and standards.
- Risk, expected defect types, product size, and readiness.
- Reviewers with relevant perspectives and available preparation time.

## Instructions
1. Choose review formality based on error impact, propagation risk, complexity, novelty, and available resources.
2. For informal review, use a work-product-specific checklist, record findings, and assign correction.
3. For a formal technical review:
   - Limit scope to a small, self-contained work product.
   - Assign producer, review leader, reviewers, and recorder.
   - Distribute material and criteria in advance.
   - Require individual preparation; keep preparation and meeting bounded.
   - Use an agenda and walk through the product while reviewers raise prepared issues.
   - Record problems; defer detailed solution work unless essential to classify the issue.
   - Decide: accept, provisionally accept with corrections, or reject for re-review.
   - Track every issue through correction and verification.
4. Review the product, not the producer; maintain constructive, evidence-based language.
5. Collect useful review measures: preparation, meeting, rework effort, size, defect count/severity, density, and downstream escapes.
6. Use trends to improve checklists, scope, preparation, reviewer mix, and timing.
7. Conduct postmortems or retrospectives to capture process improvements after increments or releases.

## Decision Rules
- If error propagation or failure impact is high, use formal preparation, records, and follow-up.
- If scope cannot be reviewed in roughly two hours, partition it into coherent review units.
- If an issue triggers prolonged debate, record alternatives and resolve offline with the needed decision-makers.
- If reviewers are unprepared, postpone or narrow the review rather than perform ineffective live reading.
- If review yield is unexpectedly low, investigate product quality and review effectiveness before concluding success.
- If the same defects escape reviews, revise checklists, reviewer expertise, or review timing.

## Constraints
- Typical FTR participation is three to five people; more participants do not automatically improve detection.
- Do not use review findings for personal blame or performance ranking.
- Do not close an issue merely because it was discussed.
- Schedule correction and verification effort, not only the meeting.
- Review test strategy and test cases as work products, not just production code.

## Failure Modes
- **Review becomes design meeting** — Cause: discovery and solution work mixed. Correction: record issue and assign focused follow-up.
- **Findings disappear** — Cause: no recorder, owner, or closure verification. Correction: maintain an issue list and follow-up owner.
- **Defensive producer** — Cause: personal language or status threat. Correction: enforce product-focused, question-based review.
- **Low-value checklist ritual** — Cause: generic questions disconnected from defect history. Correction: tailor from risks and escaped defects.

## Verification
- Scope, roles, criteria, preparation, and disposition are documented.
- Findings include owner and closure status.
- Required re-review or verification occurred.
- Review measures are used only where they improve decisions.
- Retrospective actions are assigned and checked.

## Required Terms
- [Formal technical review](../glossary.md#formal-technical-review) — defines the roles, preparation, disposition, and follow-up expected.
- [Defect amplification](../glossary.md#defect-amplification) — explains why review timing matters.

## Source Locators
- Ch 16 §§16.1–16.9, pp. 326–337.
- Ch 17 §17.2, pp. 341–343.
- Ch 19 §19.2, pp. 378–381.
