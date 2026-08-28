# Design and Evaluate Software Architecture

## Use When
- Establishing or changing system structure and dependency boundaries.
- Comparing architectural styles or patterns.
- Validating implementation conformance to intended architecture.

## Required Context
- Functional requirements and prioritized quality-attribute scenarios.
- System context, external actors/systems, deployment environment, and constraints.
- Existing architecture, reusable assets, risks, and irreversible decisions.

## Instructions
1. Describe the system context and external interfaces before internal decomposition.
2. Identify architectural drivers: essential functions, performance, reliability, security, modifiability, usability, deployment, and business constraints.
3. Define archetypes—the small set of core abstractions recurring throughout the design.
4. Compare candidate styles and patterns against drivers; consider data-centered, data-flow, call-and-return, object-oriented, layered, and domain-specific structures as alternatives, not defaults.
5. Refine archetypes into components, interfaces, data/control flow, and deployment responsibilities.
6. Record consequential decisions with context, alternatives, rationale, trade-offs, assumptions, and consequences.
7. Describe representative instantiations or scenarios showing how components collaborate at runtime.
8. Evaluate alternatives through scenario-based review:
   - Exercise normal and stress scenarios.
   - Identify sensitivity points and trade-off points.
   - Expose risks and non-risks.
   - Prototype uncertain quality attributes when analysis is insufficient.
9. Define dependency and layering constraints that can be inspected or tested.
10. Check conformance as implementation evolves; update the architecture or correct deviations deliberately.

## Decision Rules
- If a quality attribute is architecturally significant, express it as a measurable scenario before selecting structure.
- If an architectural decision is reversible and low-risk, delay detail; if irreversible or high-risk, evaluate it early.
- If two qualities conflict, expose the trade-off rather than claiming both are maximized.
- If a pattern fits the name but not the forces, reject it.
- If implementation repeatedly violates a boundary, determine whether the architecture is wrong, unclear, or unenforced before adding exceptions.
- If a review cannot discriminate alternatives, improve the scenarios and measures.

## Constraints
- Architecture is more than component diagrams; include behavior, data, deployment, interfaces, and rationale needed for decisions.
- Do not optimize architecture for hypothetical scale without current drivers.
- Do not allow presentation or infrastructure dependencies to leak inward without an explicit architectural decision.
- Exceptions to architecture rules require scope, rationale, owner, and removal or review condition.

## Failure Modes
- **Architecture by fashion** — Cause: style selected before drivers. Correction: compare candidates against quality scenarios.
- **Big design with no evidence** — Cause: review relies on opinion. Correction: prototype risky paths and measure.
- **Architecture drift** — Cause: constraints are not checked. Correction: automate dependency checks and review exceptions.
- **Decision knowledge lost** — Cause: only final diagrams remain. Correction: record alternatives and rationale.
- **Layering adds pass-through code** — Cause: layers have no independent responsibility. Correction: collapse or redefine boundaries.

## Verification
- Context, drivers, archetypes, components, interfaces, and deployment are coherent.
- Major decisions include rationale and consequences.
- Quality scenarios have evidence from review, prototype, test, or measurement.
- Dependency constraints are checkable.
- Implementation conforms or documented exceptions exist.

## Required Terms
- [Architectural driver](../glossary.md#architectural-driver) — determines which requirements materially shape structure.
- [Sensitivity point](../glossary.md#sensitivity-point) — identifies decisions where small changes strongly affect a quality attribute.

## Source Locators
- Ch 9 §§9.3–9.4, pp. 163–178.
- Ch 10 §§10.1–10.8, pp. 182–204.
- Ch 14 §§14.3–14.4, pp. 299–302.
