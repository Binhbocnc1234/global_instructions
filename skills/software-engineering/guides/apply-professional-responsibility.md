# Apply Professional Responsibility

## Use When
- Engineering decisions affect safety, privacy, security, accessibility, fairness, finances, autonomy, or public welfare.
- Product pressure conflicts with evidence, standards, or user interests.
- Communicating uncertainty, limitations, risk, or readiness.

## Required Context
- Affected stakeholders, potential harms/benefits, system context, and power asymmetries.
- Evidence quality, uncertainty, legal/professional obligations, and decision authority.
- Available safer alternatives, mitigations, monitoring, and escalation paths.

## Instructions
1. Identify who may benefit, be excluded, bear risk, or lack meaningful choice.
2. Evaluate technical correctness together with privacy, security, safety, accessibility, fairness, maintainability, and social consequence.
3. State evidence, assumptions, uncertainty, known limitations, and residual risk honestly.
4. Protect confidential information and minimize collection/exposure of personal data.
5. Seek review from appropriate domain, security, safety, legal, accessibility, or ethics expertise when impact exceeds competence.
6. Propose safer designs, reduced scope, staged release, monitoring, rollback, or refusal when requested behavior creates unacceptable harm.
7. Preserve traceable decisions and dissent for consequential choices.
8. Escalate unresolved material concerns through organizational channels; do not silently implement foreseeable harm.
9. Monitor deployed effects and correct harmful outcomes as evidence emerges.
10. Maintain competence and update practices as technology, threats, and societal context change.

## Decision Rules
- If impact is high and evidence is weak, reduce exposure and obtain evidence before broad release.
- If a user cannot reasonably understand or control data use, redesign consent and defaults.
- If schedule conflicts with critical safety/security validation, reduce scope or delay; do not misrepresent readiness.
- If instructed to conceal material risk, document and escalate.
- If the system affects vulnerable groups, include them or qualified representatives in requirements and validation.
- If consequences exceed the team's competence, obtain expert review rather than extrapolating general knowledge.

## Constraints
- Compliance is a minimum, not proof of ethical or safe behavior.
- Do not fabricate evidence, hide defects, or present estimates as certainties.
- Do not expose secrets, private raw data, or user information in logs, tests, prompts, or repositories.
- Technical neutrality does not remove responsibility for foreseeable system use and harm.

## Failure Modes
- **Technically correct but harmful outcome** — Cause: narrow functional success criteria. Correction: include affected stakeholders and harm scenarios.
- **Risk hidden by optimistic language** — Cause: delivery pressure. Correction: report uncertainty, severity, and missing evidence explicitly.
- **Consent without understanding** — Cause: formal notice replaces user control. Correction: minimize collection and make choices clear and reversible.
- **No one owns deployed harm** — Cause: responsibility ended at release. Correction: assign monitoring, response, and correction ownership.

## Verification
- Consequential decisions identify affected stakeholders and harms.
- Claims are supported by evidence with uncertainty stated.
- Required expert review and validation occurred.
- Safer alternatives and residual risks are recorded.
- Monitoring, response, and escalation mechanisms exist.

## Source Locators
- Ch 15 §§15.3.3–15.3.6, pp. 319–321.
- Ch 18 §§18.1–18.12, pp. 357–370.
- Ch 30 §§30.1–30.6, pp. 603–609.
