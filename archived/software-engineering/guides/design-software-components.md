# Design Software and Components

## Use When
- Translating requirements and architecture into maintainable components.
- Refactoring code with poor cohesion, excessive coupling, or unstable interfaces.
- Selecting or applying design patterns.

## Required Context
- Requirements and quality attributes.
- Architectural boundaries and dependency rules.
- Expected variation, reuse, performance, data, and lifecycle constraints.
- Existing components, contracts, and test protection.

## Instructions
1. Trace design elements to requirements and architectural responsibilities.
2. Apply abstraction and separation of concerns so each design element can be understood with limited context.
3. Partition responsibilities into modules/components that exhibit high cohesion and low coupling.
4. Hide likely-to-change data representations, algorithms, devices, external services, and policy decisions behind stable interfaces.
5. Refine from architecture to interfaces, class responsibilities, operations, data, algorithms, and error behavior.
6. Design class-based components:
   - Elaborate inherited and local responsibilities.
   - Define provided and required interfaces.
   - Specify preconditions, postconditions, invariants, exceptions, and state effects where needed.
   - Evaluate cohesion and every dependency introduced.
7. Prefer data coupling and narrow type-use dependencies over control, common, content, or broad stamp coupling.
8. Apply patterns only after identifying context, problem, forces, alternatives, and consequences.
9. Refactor when behavior is protected: simplify responsibilities, remove duplication, clarify names, reduce interfaces, and restore dependency direction.
10. Review design against quality attributes, error handling, testability, and anticipated change.

## Decision Rules
- If a component changes for unrelated reasons, split responsibilities along those change axes.
- If callers pass flags that dictate another component's internal path, replace control coupling with separate operations or polymorphic policy.
- If many callers know a representation detail, hide it before it becomes a widespread dependency.
- If pattern consequences exceed the problem's needs, use the simpler design.
- If reuse requires speculative generality, postpone it until a second concrete use clarifies the abstraction.
- If refactoring cannot be verified by existing tests, add characterization or public-behavior tests first.

## Constraints
- Keep interfaces at one level of abstraction.
- Do not expose mutable internal data without an explicit ownership contract.
- Do not add indirection solely to match a pattern name.
- Preserve observable behavior during refactoring.
- Specialized components for web/mobile still require clear contracts, cohesion, coupling control, and quality validation.

## Failure Modes
- **God component** — Cause: responsibilities accumulated around convenience. Correction: separate policy, data, coordination, and presentation concerns.
- **Ripple changes** — Cause: information hiding failed. Correction: place volatile knowledge behind a stable boundary.
- **Pattern-heavy design** — Cause: patterns selected before forces. Correction: restate the problem and compare simpler alternatives.
- **Unmockable or untestable component** — Cause: hidden dependencies and mixed lifecycle concerns. Correction: expose explicit collaborators and separate pure logic.
- **Refactoring changes behavior** — Cause: weak regression protection or mixed feature work. Correction: isolate the refactor and verify public behavior continuously.

## Verification
- Each component has a coherent responsibility and explicit contract.
- Dependencies follow architecture and are justified by required collaboration.
- Volatile decisions are hidden.
- Error behavior and lifecycle effects are explicit.
- Tests can exercise component behavior and interfaces.
- Pattern use records consequences and alternatives.

## Required Terms
- [Functional independence](../glossary.md#functional-independence) — operational goal of high cohesion and low coupling.
- [Information hiding](../glossary.md#information-hiding) — determines what must remain behind the component boundary.

## Source Locators
- Ch 9 §§9.1–9.5, pp. 157–178.
- Ch 11 §§11.1–11.6, pp. 207–231.
- Ch 14 §§14.1–14.7, pp. 290–306.
