# Engineer Software Security

## Use When
- Software handles valuable assets, untrusted input, identity, payments, network access, or private data.
- Defining security requirements, reviewing attack surface, or testing mitigations.

## Required Context
- Assets, users, trust boundaries, data flows, deployment, dependencies, and attacker capabilities.
- Business impact, safety/privacy obligations, compliance constraints, and acceptable residual risk.
- Existing security controls, incidents, and operational response capabilities.

## Instructions
1. Integrate security across requirements, design, coding, testing, deployment, operation, and improvement.
2. Identify assets and protection goals: confidentiality, integrity, availability, authenticity, accountability, and privacy as applicable.
3. Elicit security requirements using a structured process such as SQUARE: agree definitions, identify goals/artifacts, assess risk, select elicitation, elicit, categorize, prioritize, and inspect requirements.
4. Create misuse/abuse cases and attack patterns describing adversary goals, preconditions, paths, and expected defenses.
5. Model threats at trust boundaries, data stores, processes, interfaces, and dependencies.
6. Estimate likelihood and impact; prioritize mitigations by risk and feasibility.
7. Reduce attack surface: minimize entry points, privileges, exposed data, enabled features, dependency footprint, and secret access.
8. Apply secure coding: validate untrusted data, encode output, enforce authorization, handle errors safely, protect secrets, use safe defaults, and avoid sensitive logging.
9. Verify through review, static/dynamic analysis, interface and abuse tests, dependency checks, penetration activities where justified, and operational monitoring.
10. Measure incidents, vulnerabilities, remediation time, recurring causes, coverage of critical controls, and process maturity; feed results into improvement.

## Decision Rules
- If a threat can be eliminated through design or reduced privilege, prefer that over detection-only controls.
- If a control depends on secrecy of implementation, treat it as insufficient by itself.
- If likelihood is uncertain but impact is catastrophic, prototype and test the risky path rather than assigning low probability casually.
- If security conflicts with usability, redesign the workflow; do not silently remove either requirement.
- If a dependency is unmaintained or vulnerable, replace, isolate, patch, or explicitly accept and monitor the risk.
- If logs aid attackers or expose private data, reduce and sanitize them while preserving necessary audit evidence.

## Constraints
- Never hardcode or expose secrets.
- Authenticate identity and authorize each protected operation; authentication alone is not authorization.
- Treat all external input and persisted data as potentially malformed or hostile.
- Fail safely without revealing sensitive internal detail.
- Security requirements and accepted residual risks require stakeholder authorization and traceability.

## Failure Modes
- **Security added before release** — Cause: threats were absent from requirements/architecture. Correction: add lifecycle security gates and threat modeling.
- **Checklist says secure, exploit succeeds** — Cause: generic controls ignored product-specific data flows. Correction: model assets, trust boundaries, and misuse scenarios.
- **Secret appears in source/log** — Cause: weak secret lifecycle. Correction: revoke, remove, use managed storage, and prevent recurrence.
- **Mitigation breaks under change** — Cause: no regression or configuration audit. Correction: trace controls to tests and release checks.

## Verification
- Assets, trust boundaries, threats, abuse cases, and risk priorities are documented.
- Security requirements trace to design controls and verification.
- Attack surface and privilege are minimized and reviewed.
- Critical controls have negative and abuse-path tests.
- Residual risks, monitoring, and response ownership are explicit.

## Required Terms
- [Attack surface](../glossary.md#attack-surface) — determines what exposure must be minimized and monitored.
- [SQUARE](../glossary.md#square) — names the source's structured security-requirements process.

## Source Locators
- Ch 18 §§18.1–18.12, pp. 357–370.
- Ch 21 §21.7, pp. 423–424.
- Ch 26 §§26.2–26.7, pp. 534–547.
