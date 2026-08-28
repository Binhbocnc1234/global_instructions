# Plan and Design Component Tests

## Use When
- Creating a test strategy, designing component/class tests, or defining completion criteria.
- Selecting tests under limited time and resources.
- Converting requirements, code structure, or defect risk into test cases.

## Required Context
- Traceable functional/nonfunctional requirements and validation criteria.
- Component design, interfaces, states, data structures, control flow, and error behavior.
- Risk, complexity, defect history, dependencies, and available test environment.
- Expected results or another reliable test oracle.

## Instructions
1. State the primary objective: execute software with the intent of finding previously undiscovered errors.
2. Plan testing before construction is complete; review the strategy and test cases themselves.
3. Define the progression from component verification through integration, validation, and system testing.
4. Record each test's requirement/risk link, setup, input/action, expected result, pass/fail, date, and diagnostic notes. Keep recordkeeping lightweight but auditable.
5. Prioritize crucial, complex, frequently changed, highly connected, and historically defect-prone components.
6. Design component tests for:
   - Interfaces and data flow in both directions.
   - Local data structures and effects on shared/global state.
   - Independent control paths and both outcomes of decisions.
   - Loops at zero, one, two, typical, maximum-minus-one, maximum, and maximum-plus-one where valid.
   - Boundary values for input, output, counts, and data structures.
   - Every error, exception, cleanup, initialization, and termination path.
7. Apply black-box techniques:
   - Partition inputs into valid and invalid equivalence classes.
   - Select representatives that cover distinct error classes without redundant cases.
   - Test at and immediately around boundaries.
   - Exercise missing/incorrect functions, interface errors, data errors, behavior/performance, and lifecycle errors.
8. Apply white-box techniques where internal logic risk justifies them: independent paths, conditions, data flow, and loops.
9. For object-oriented classes, test operations in class/subclass context, valid and invalid operation sequences, states, transitions, and collaborations.
10. Build simple drivers/stubs only where isolation adds value; defer collaboration behavior to integration tests rather than creating unrealistic scaffolding.
11. Define completion using agreed coverage of requirements, risks, states, paths, defects, reliability evidence, residual risk, time, and budget—not a claim that all defects are absent.

## Decision Rules
- If two inputs exercise the same equivalence class and behavior, keep the one with higher defect-finding value.
- If values have limits, test just below, at, and just above each boundary.
- If code has complex control flow, derive a basis set of independent paths and add condition/data/loop tests; statement execution alone is insufficient.
- If behavior depends on subclass data or collaborators, test inherited operations in each materially different context.
- If exhaustive testing is impossible, prioritize by failure impact, defect likelihood, complexity, and usage.
- If a component cannot be tested without heavy scaffolding, reconsider its interface and coupling before accepting the overhead.
- If a test passes alone but fails in the suite, inspect shared state, order dependence, resource cleanup, time, and environment.

## Constraints
- Testing can reveal defects; it cannot prove their absence.
- Developer component testing remains required even when independent testing exists.
- Testing and debugging are separate: testing exposes failure; debugging locates and corrects cause.
- Expected results must be specified before interpreting output.
- Do not use line coverage as the sole completion criterion.
- Never omit invalid, error, and recovery behavior because the happy path passes.

## Failure Modes
- **Many tests, few defects found** — Cause: redundant center-value happy paths. Correction: use partitions, boundaries, state, interface, and error analysis.
- **Test results cannot be audited** — Cause: missing traceability or expected outcome. Correction: add minimal structured records.
- **Coverage high, behavior wrong** — Cause: structural execution without requirement validation. Correction: add scenario-derived black-box tests.
- **Tests brittle under refactoring** — Cause: assertions target implementation details. Correction: assert public behavior and contracts unless internal structure is the explicit risk.
- **Error handler fails during incident** — Cause: error paths were never executed. Correction: force every material error and cleanup path.

## Verification
- Test strategy identifies levels, responsibilities, milestones, records, and completion criteria.
- Functional tests trace to requirements; structural tests trace to logic or risk.
- Interfaces, partitions, boundaries, states, paths, loops, and error behavior are represented where applicable.
- Test cases have explicit expected results and independent cleanup.
- Prioritization is defensible from risk and defect likelihood.

## Required Terms
- [Basis path testing](../glossary.md#basis-path-testing) — defines the structural path-selection method.
- [Equivalence partitioning](../glossary.md#equivalence-partitioning) — prevents redundant input selection.
- [Boundary-value analysis](../glossary.md#boundary-value-analysis) — identifies high-yield edge cases.
- [Scaffolding](../glossary.md#scaffolding) — distinguishes test drivers/stubs from production components.

## Source Locators
- Ch 6 §6.2.4, pp. 95–98.
- Ch 19 §§19.1–19.7, pp. 373–393.
- Ch 23 §23.4, pp. 474–476.
