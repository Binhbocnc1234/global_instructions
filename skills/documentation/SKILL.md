---
name: documentation
description: Technical writing and project documentation management. Use when creating, reviewing, validating, or reading project documents under Documentation/ using Diataxis guidelines and custom search tools.
---

# Technical Documentation Management

You are an expert technical writer specializing in high-quality software documentation.
Your work is guided by the Diataxis framework.

## Guiding Principles

1. **Clarity:** Write in simple, clear, and unambiguous language.
2. **Accuracy:** Ensure all details, code snippets, and configuration examples are correct.
3. **User-Centricity:** Every document must serve a specific reader role (player, developer, agent).
4. **Consistency:** Maintain consistent tone, structure, and style.
5. **Single Source of Truth:** Each concept or rule must have one canonical location. Other docs link to it instead of restating it.

## Document Types

Choose one primary Diataxis document type before writing or editing. Do not mix types in one file.

| Document type | Purpose | Reader goal |
|---------------|---------|-------------|
| **Tutorial** | Learning-oriented lesson. | Learn a workflow through a guided path. |
| **How-to guide** | Problem-oriented recipe. | Complete one specific task. |
| **Reference** | Information-oriented description. | Look up exact facts, contracts, or rules. |
| **Explanation** | Understanding-oriented discussion. | Understand why a concept or decision works. |

## Consistency & Naming Rules

### Avoid Duplication
Two documents must not describe the same logic or workflow. When cross-referencing, use an explicit relative Markdown link: `See [EntitySystem](../../explanation/gameplay/EntitySystem.md)`.

### Negative Rules
*   **Avoid Placing Files in the Wrong Section:** Never place an explanation file under a reference folder, or a how-to guide under a tutorial folder. Choose the folder path and file location based strictly on its Diataxis classification.
*   **Avoid Multi-Purpose Files:** A single file must not attempt to serve multiple Diataxis purposes (e.g., combining high-level architecture explanations with dense reference API tables). Split them into separate files (e.g. `Architecture.md` for explanation, `ApiReference.md` for reference) and link them.

### File Naming
Follow the project's naming convention. If the project has no convention, use PascalCase for Markdown file names (e.g., `HowToDocumentation.md`, `Architecture.md`, `DesignPrinciples.md`). Do not use kebab-case or snake_case unless requested.

## Frontmatter Rules

Every documentation Markdown file starts with a YAML frontmatter block.

```yaml
---
type: gameplay | technical | product | process | user-guide
audience: [developer, agent]
status: draft | active | deprecated
language: en | vi
description: Explains the current AI system flow and scoring model.
prerequisite_docs:
  - ../../explanation/gameplay/DesignPrinciples.md
related_code:
  - Assets/Scripts/Battlefield/AI
related_tests:
  - Assets/Scripts/Tests/Editor/AI
requirements:
  - MVP-FUN-002
---
```

*   **Link Formatting:** Always use explicit relative Markdown paths with file extensions (e.g., `../explanation/Architecture.md`) for references in `prerequisite_docs` and `related_docs` to ensure robust rendering on code platforms (such as VS Code or GitHub).
*   **Traceability Paths:** Paths in `related_code`, `related_tests`, and `related_assets` must be relative to the project root directory.

## Diataxis Document Guidelines

### How-To Guides
*   **Scope:** Include preconditions, ordered steps with one action per step, expected results, edge cases, and verification. Exclude broad background or reference tables.
*   **Template:**
    ```markdown
    # How to Run EditMode Tests (Game Project Example)
    ## Preconditions
    - Unity Editor is open
    - Test Runner is open (Window > General > Test Runner)
    ## Steps
    1. Select the EditMode tab
    2. Click Run All
    ## Expected Results
    - All tests pass (green)
    ## Edge Cases
    - **Test fails:** Check the Console log, fix the issue, and run again.
    ## Verification
    - The message "All tests passed" appears
    ```

### Tutorials
*   **Scope:** A guided lesson for newcomers. Focus on a practical, learning-oriented path. Do not skip setup steps.
*   **Template:**
    ```markdown
    # Tutorial: Creating a New Combat Unit (Game Project Example)
    ## Learning Objectives
    - Understand how to configure unit attributes
    - Bind a prefab to the unit controller
    ## Step 1: Clone the Template Prefab
    1. Locate `Assets/Prefabs/UnitTemplate.prefab`
    2. Duplicate it and rename it to `CustomUnit.prefab`
    ## Verification
    - Click Play and verify that the custom unit spawns in the test scene.
    ```

### Reference Docs
*   **Scope:** Information-oriented facts, API contracts, schema structures, and configuration values.
*   **Template:**
    ```markdown
    # Unit Attributes Configuration Reference (Game Project Example)
    ## Attribute Configuration Table
    | Field | Type | Range | Description |
    |-------|------|-------|-------------|
    | `maxHp` | Integer | [1, 999] | Starting health points |
    | `speed` | Float | [0.1, 5.0] | Movement speed multiplier |
    ```

### Explanations
*   **Scope:** Understanding-oriented discussions. Discusses architecture, design choices, trade-offs, and reasons behind decisions. Use Mermaid diagrams.
*   **Template:**
    ```markdown
    # Unit Death Flow Explanation (Game Project Example)
    ## Architecture Overview
    When unit health reaches 0, the `UnitHealth` component triggers the death flow.
    ```mermaid
    graph TD
        A[Health reaches 0] --> B[Trigger Death Event]
        B --> C[Play Death Animation]
        B --> D[Remove Unit from Board]
    ```
    ## Design Decisions & Trade-offs
    - **Separate Animation and State:** We process removal independently of animation playback to prevent gameplay state desynchronization.
    ```

## Reading & Validating Documentation

Use the bundled Python scripts to search, inspect, and validate documentation before making changes.

### 1. Query Documents by Frontmatter
Use `query_docs_frontmatter.py` to find documents matching specific metadata:
```powershell
python .\.agents\skills\documentation\scripts\query_docs_frontmatter.py --audience agent --status active --language en
```

### 2. Inspect Headings & Line Ranges
Use `get_markdown_headers.py` to list headings and discover the exact line ranges:
```powershell
python .\.agents\skills\documentation\scripts\get_markdown_headers.py .\Documentation\en\how-to\style\HowToDocumentation.md
```

### 3. Read a Section Range
Use `read_markdown_section.py` to read only a specific range of lines:
```powershell
python .\.agents\skills\documentation\scripts\read_markdown_section.py .\Documentation\en\how-to\style\HowToDocumentation.md "[81,126]"
```

### 4. Find Related Documents
Use `find_related_docs.py` to discover inbound and outbound links for a document ID:
```powershell
python .\.agents\skills\documentation\scripts\find_related_docs.py --id testing --root .\Documentation\en
```

### 5. Validate Frontmatter
Use `validate_docs_frontmatter.py` after creating or editing documentation to check formatting, allowed enum values, and link validity:
```powershell
python .\.agents\skills\documentation\scripts\validate_docs_frontmatter.py --root .\Documentation\en
```
