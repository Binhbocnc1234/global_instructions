# Reusable Techniques and Patterns

## Evolutionary Increment
**When to use**: Requirements or solution details are uncertain and partial value can be evaluated.
**Mechanism**: Deliver a coherent slice, test and evaluate it, update risks/requirements/plan, then repeat.
**Trade-offs**: Faster evidence; requires scope control, integration discipline, and architectural attention.
**Guide**: [Evolve and evaluate increments](guides/evolve-and-evaluate-increments.md).

## Prototype Decision Loop
**When to use**: Interaction, feasibility, architecture, or value needs evidence.
**Mechanism**: Define a question and criteria, build the smallest experiment, then continue, redirect, rebuild, or stop.
**Trade-offs**: Cheap learning; prototype shortcuts become debt if promoted silently.
**Guide**: [Evolve and evaluate increments](guides/evolve-and-evaluate-increments.md).

## Scenario-Based Requirements
**When to use**: Converting stakeholder goals into observable behavior.
**Mechanism**: Record actor, goal, trigger, preconditions, main flow, alternatives, failures, and postconditions.
**Trade-offs**: Strong behavioral clarity; needs complementary quality and structural models.
**Guide**: [Engineer requirements](guides/engineer-requirements.md).

## CRC Modeling
**When to use**: Responsibilities and collaborators are unclear.
**Mechanism**: Explore candidate classes using responsibility and collaborator cards before detailed design.
**Trade-offs**: Fast collaborative discovery; insufficient alone for data, timing, and deployment detail.
**Guide**: [Model requirements and behavior](guides/model-requirements-and-behavior.md).

## Functional Independence
**When to use**: Partitioning components or diagnosing change friction.
**Mechanism**: Increase cohesion, reduce coupling, hide volatile decisions, and narrow contracts.
**Trade-offs**: Improves changeability; excessive partitioning increases coordination overhead.
**Guide**: [Design software components](guides/design-software-components.md).

## Scenario-Based Architecture Review
**When to use**: Comparing consequential architecture alternatives.
**Mechanism**: Exercise quality scenarios, identify sensitivity/trade-off points and risks, then prototype uncertain paths.
**Trade-offs**: Decision-focused evidence; depends on representative scenarios and measures.
**Guide**: [Design and evaluate architecture](guides/design-and-evaluate-architecture.md).

## Formal Technical Review
**When to use**: Error propagation or impact justifies prepared, recorded review.
**Mechanism**: Bound scope, prepare individually, assign roles, record issues, decide disposition, correct, and verify closure.
**Trade-offs**: Strong early defect removal; costs preparation and follow-up time.
**Guide**: [Conduct technical reviews](guides/conduct-technical-reviews.md).

## Equivalence Partitioning plus Boundary Analysis
**When to use**: Input/output domains are too large for exhaustive testing.
**Mechanism**: Select valid/invalid behavioral classes, then test at and around each boundary.
**Trade-offs**: High yield with few cases; requires separate state, sequence, interface, and structural analysis.
**Guide**: [Plan and design tests](guides/plan-and-design-tests.md).

## Basis Path Testing
**When to use**: Internal control flow is complex or risky.
**Mechanism**: Derive independent paths using control flow/cyclomatic complexity, then add condition, data-flow, and loop cases.
**Trade-offs**: Improves structural coverage; does not validate requirements by itself.
**Guide**: [Plan and design tests](guides/plan-and-design-tests.md).

## Incremental Integration and Smoke Testing
**When to use**: Building a system from collaborating components.
**Mechanism**: Integrate one cluster/thread at a time, exercise new interfaces, and run fast show-stopper tests on each build.
**Trade-offs**: Easier failure isolation; requires scaffolding and integration planning.
**Guide**: [Integrate and specialize testing](guides/integrate-validate-and-specialize-testing.md).

## Impact-Based Regression Selection
**When to use**: After meaningful change.
**Mechanism**: Select representative critical behavior, affected behavior, changed components, and prior defect tests.
**Trade-offs**: Sustainable confidence; dependency analysis can miss indirect effects.
**Guide**: [Integrate and specialize testing](guides/integrate-validate-and-specialize-testing.md).

## RMMM
**When to use**: A material uncertainty could affect objectives.
**Mechanism**: Reduce probability/impact, monitor leading indicators, and prepare contingency action.
**Trade-offs**: Makes risk actionable; probability and impact remain estimates.
**Guide**: [Manage software risk](guides/manage-software-risk.md).

## Measurement-to-Decision Loop
**When to use**: Evaluating product, process, project, or improvement.
**Mechanism**: Define decision and questions, select operational measures, interpret indicators, act, and reevaluate.
**Trade-offs**: Supports learning; metrics can be gamed or misinterpreted as targets.
**Guide**: [Measure software work](guides/measure-and-analyze-software-work.md).

## SPI Pilot
**When to use**: Adopting a process, tool, standard, or emerging practice.
**Mechanism**: Assess gap, train, pilot bounded change, measure net outcome, refine, then institutionalize or reject.
**Trade-offs**: Limits adoption risk; pilots can be unrepresentative.
**Guide**: [Improve process and adopt trends](guides/improve-process-and-adopt-trends.md).
