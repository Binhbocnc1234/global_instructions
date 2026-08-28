---
name: learning-material
description: Create, edit, read, or review human-facing learning materials when teaching is the primary goal. Use alongside skill documentation for Markdown and repository rules.
---

# Learning Material

Design material so the intended learner can understand a concept or gain a practical skill. All learning materials will be contained within a single folder. Each folder may include a `README.md` file, a `GLOSSARY.md`, and various other `.md` files serving as learning Resources.

## Structure of Learning Folders

- `README.md` must include two core sections:
  - `Prerequisite knowledge`: Stating explicit background assumed (e.g., DSA and OOP).
  - `Contents`: A dependency-ordered navigation table with three columns: `File`, `Covers`, and `Depends on`.
- `GLOSSARY.md`: Defines terms that appear across multiple resources, serving as a unified reference index.
- **Python Pseudocode**: All pseudocode MUST be written in Python. Include explicit type annotations (`int`, `list[int]`, `Float[Tensor, "N d"]`) whenever they carry semantic meaning.
- **Trust Labels**: Classify claims as **Documented**, **Observable**, or **Inferred** when that distinction affects trust or action.
- **Self-Check Checks**: Add self-check questions, diagnosis scenarios, or executable verification steps when they expose and resolve common misconceptions.

## Example for Contents section

| File | Covers | Depends on |
|---|---|---|
| [00-overview.md](00-overview.md) | System goals, API boundaries, request lifecycle, and core terminology | — |
| [01-data-model.md](01-data-model.md) | Entities, relationships, validation rules, and database schema decisions | [00-overview.md](00-overview.md) |
| [02-api-design.md](02-api-design.md) | Resource naming, endpoints, HTTP methods, status codes, pagination, and error format | [00-overview.md](00-overview.md), [01-data-model.md](01-data-model.md) |
| [03-authentication.md](03-authentication.md) | Authentication flow, token handling, authorization rules, and protected endpoints | [02-api-design.md](02-api-design.md) |
| [04-database-access.md](04-database-access.md) | Query patterns, transactions, connection handling, and repository-layer conventions | [01-data-model.md](01-data-model.md) |
| [05-testing.md](05-testing.md) | Unit tests, integration tests, API fixtures, mocking strategy, and failure cases | [02-api-design.md](02-api-design.md), [03-authentication.md](03-authentication.md), [04-database-access.md](04-database-access.md) |
| [06-deployment.md](06-deployment.md) | Environment configuration, migrations, production startup, health checks, and rollback considerations | [03-authentication.md](03-authentication.md), [04-database-access.md](04-database-access.md), [05-testing.md](05-testing.md) |

## Pedagogical Rules for Resources

### 1. Prerequisite & No-Unintroduced-Concept Rule

- **Define Prerequisites First:** If a developer has read up to line $n$, assume they understand only lines $1$ to $n-1$ and prerequisite documents.
- **No Unintroduced Concepts:** Never require the reader to encounter, interpret, or reason about a concept that has not already been defined. This applies to explanations, examples, code snippets, syntax, formulas, diagrams, and terminology alike (e.g., in Python learning material, teaching about `Integer` while introducing a code snippet containing an `Array`/`List` that hasn't been covered yet).

### 2. Motivation Before Mechanics (Teleology Rule)

- Always explain **why** an algorithm, mechanism, or architectural choice exists before detailing **how** it calculates.
- Introduce the motivating problem, ambiguity, or failure mode of previous approaches first (e.g., polysemy of words, pronoun ambiguity, memory decay in sequential tapes) so the algorithm is understood as a necessary solution.

### 3. Pair Abstractions with Concrete Examples (Mental Unit Tests)

- Never present abstract formulas, mathematical descriptions, or complex interfaces in isolation.
- Always pair them with a concrete, traceable walkthrough (with real inputs, intermediate calculations, and expected outputs). Concrete examples act as "mental unit tests" that anchor abstract interfaces and reduce working memory load.

