---
name: software-engineering
description: "Use when choosing or improving a software process; engineering requirements, architecture, components, UX, quality, security, or tests; managing configuration, metrics, projects, risk, maintenance, or professional responsibility."
---

# Software Engineering: A Practitioner's Approach, 9th Edition

## How to Use This Skill

- Route the task through the Capability Index and read every relevant guide before answering or acting.
- Read linked glossary entries when exact source terminology changes execution.
- Use [source-map.md](source-map.md) and targeted searches in retained raw extracts to verify ambiguous or precise claims.
- State when retained guidance is insufficient. Do not fill source-specific gaps from general knowledge without labeling that distinction.
- Combine this guidance with project-specific instructions, current authoritative standards, and observed project evidence.

## Core Decision Rules

- Quantify every verification: define a pass/fail threshold, scope, and measurement method; replace qualitative checks such as "keep files short" with verifiable limits such as "keep each source file at or below 250 lines."
- Automate repeatable checks with a runnable script and execute it before reporting completion; use [verify-file-lengths.ps1](scripts/verify-file-lengths.ps1) for the 250-line source-file limit.
- Define stakeholder value, observable behavior, constraints, and quality before committing to implementation.
- Adapt process rigor to uncertainty and risk while preserving required evidence and cross-cutting quality work.
- Use prototypes and increments as decision instruments; every experiment needs criteria and a continue, redirect, rebuild, or stop decision.
- Hide volatile decisions behind cohesive components and evaluate architecture against measurable quality scenarios.
- Review work before errors propagate; test to discover defects from components outward to user validation.
- Select regression from critical behavior, change impact, changed components, and prior defects.
- Control every artifact that affects reproducibility; analyze impact before changing a baseline.
- Start measurement from a decision, not available data; retire metrics that do not produce action.
- Express estimates and risks with assumptions, uncertainty, owners, triggers, and response.
- Treat security, privacy, safety, accessibility, fairness, and truthful reporting as engineering responsibilities.

## Capability Index

| Capability | Use when | Guide |
|---|---|---|
| Select and tailor process | Starting or adapting project workflow | [Guide](guides/select-and-tailor-process.md) |
| Evolve increments | Prototyping, iterative delivery, go/no-go decisions | [Guide](guides/evolve-and-evaluate-increments.md) |
| Lead teams | Structuring coordination, ownership, or distributed work | [Guide](guides/collaborate-and-lead-teams.md) |
| Engineer requirements | Discovering, negotiating, validating, or changing needs | [Guide](guides/engineer-requirements.md) |
| Model requirements | Modeling scenarios, classes, workflows, interactions, or state | [Guide](guides/model-requirements-and-behavior.md) |
| Design components | Partitioning responsibilities, contracts, patterns, or refactoring | [Guide](guides/design-software-components.md) |
| Design architecture | Selecting structure and evaluating quality trade-offs | [Guide](guides/design-and-evaluate-architecture.md) |
| Design UX | Researching users, interaction, usability, accessibility | [Guide](guides/design-and-evaluate-user-experience.md) |
| Design mobile/web | Handling device, browser, context, network, and resource variability | [Guide](guides/design-for-mobile-and-web.md) |
| Define and assure quality | Establishing quality goals, controls, SQA, and release evidence | [Guide](guides/define-and-assure-quality.md) |
| Conduct reviews | Reviewing requirements, design, code, tests, or releases | [Guide](guides/conduct-technical-reviews.md) |
| Engineer security | Defining security requirements, threats, controls, and tests | [Guide](guides/engineer-software-security.md) |
| Plan component tests | Designing traceable black-box/white-box tests and done criteria | [Guide](guides/plan-and-design-tests.md) |
| Integrate and validate | Integration, regression, acceptance, or specialized testing | [Guide](guides/integrate-validate-and-specialize-testing.md) |
| Manage configuration | Versioning, baselines, change control, builds, and audits | [Guide](guides/manage-configuration-and-change.md) |
| Measure and analyze | Selecting metrics or evaluating product/process evidence | [Guide](guides/measure-and-analyze-software-work.md) |
| Plan and estimate | Scope, feasibility, resources, estimation, tasks, schedule | [Guide](guides/plan-estimate-and-schedule.md) |
| Manage risk | Identifying, prioritizing, mitigating, monitoring uncertainty | [Guide](guides/manage-software-risk.md) |
| Maintain and evolve | Support, defects, refactoring, reengineering, migration | [Guide](guides/maintain-support-and-evolve-software.md) |
| Improve process | Adopting process, tools, standards, or emerging practices | [Guide](guides/improve-process-and-adopt-trends.md) |
| Apply responsibility | High-impact decisions, harm, evidence, and escalation | [Guide](guides/apply-professional-responsibility.md) |

## Topic Index

- **Accessibility, playability, usability** → [UX](guides/design-and-evaluate-user-experience.md), [specialized testing](guides/integrate-validate-and-specialize-testing.md)
- **Agile, Scrum, XP, Kanban, DevOps** → [process](guides/select-and-tailor-process.md), [increments](guides/evolve-and-evaluate-increments.md)
- **Architecture, dependencies, patterns** → [architecture](guides/design-and-evaluate-architecture.md), [components](guides/design-software-components.md)
- **CI, baselines, releases, version control** → [configuration](guides/manage-configuration-and-change.md), [integration](guides/integrate-validate-and-specialize-testing.md)
- **Code and component design, refactoring** → [components](guides/design-software-components.md), [maintenance](guides/maintain-support-and-evolve-software.md)
- **Estimation, scheduling, staffing** → [planning](guides/plan-estimate-and-schedule.md), [teams](guides/collaborate-and-lead-teams.md)
- **Metrics, coverage, defect analytics** → [measurement](guides/measure-and-analyze-software-work.md), [quality](guides/define-and-assure-quality.md)
- **Mobile, web, device compatibility** → [mobile/web](guides/design-for-mobile-and-web.md), [specialized testing](guides/integrate-validate-and-specialize-testing.md)
- **Process models and improvement** → [process](guides/select-and-tailor-process.md), [improvement](guides/improve-process-and-adopt-trends.md)
- **QA, quality, reviews** → [quality](guides/define-and-assure-quality.md), [reviews](guides/conduct-technical-reviews.md)
- **Requirements, use cases, modeling** → [requirements](guides/engineer-requirements.md), [modeling](guides/model-requirements-and-behavior.md)
- **Risk, security, safety, privacy** → [risk](guides/manage-software-risk.md), [security](guides/engineer-software-security.md), [responsibility](guides/apply-professional-responsibility.md)
- **Testing, regression, validation** → [component tests](guides/plan-and-design-tests.md), [integration/specialized tests](guides/integrate-validate-and-specialize-testing.md)

## Supporting Files

- [glossary.md](glossary.md) — uncommon, ambiguous, or operationally significant terms
- [patterns.md](patterns.md) — reusable techniques and trade-offs
- [cheatsheet.md](cheatsheet.md) — compact decision aids
- [source-map.md](source-map.md) — guidance-to-source traceability and chapter coverage audit
- `raw-source-extract/manifest.json` — local retained-source inventory

## Scope and Limits

This skill contains source-grounded operational guidance, not a complete reproduction of the book. It omits narrative and repetition while preserving materially behavior-changing instructions. Verify ambiguity against retained extracts and identify unsupported gaps. Current laws, standards, APIs, threats, and tools require current authoritative sources in addition to this book.
