# Diataxis Writing Guidelines & Templates

This reference provides detailed rules for writing documentation, defining YAML frontmatter fields, and utilizing checklists and templates for the 4 Diataxis document types.

## YAML Frontmatter Rules

Every documentation Markdown file starts with a YAML frontmatter block that describes the document.

```yaml
---
type: gameplay | technical | product | process | user-guide
audience: [developer, agent]
status: draft | active | deprecated
language: en | vi
description: Explains the current AI system flow, simulator contract, scoring model, and tests.
prerequisite_docs:
  - ../../explanation/gameplay/DesignPrinciples.md
related_docs:
  - ../../explanation/gameplay/ExecutionPaths.md
related_code:
  - Assets/Scripts/Battlefield/AI
related_tests:
  - Assets/Scripts/Tests/Editor/AI
requirements:
  - MVP-FUN-002
  - TEST-SEL-001
---
```

### Frontmatter Field Specifications

| Field | Description & Rules |
|-------|---------------------|
| `type` | The category of content. Use categories matching your project. For game projects, `gameplay` means player-facing game rules and `technical` means implementation/developer workflows. |
| `audience` | Targeted reader role (e.g., `player`, `developer`, `operator`, `agent`, `user`). Can be a single value or YAML list. |
| `status` | Document lifecycle state (`draft`, `active`, or `deprecated`). |
| `language` | Standard language code (`en`, `vi`). |
| `description` | One concise sentence covering the entire document's purpose. |
| `prerequisite_docs` | Documentation that the reader **must** read first to understand or apply this document. |
| `related_docs` | Other documents providing neighboring context, deeper explanations, or downstream workflow. |
| `related_code` | Relative project paths to source files/folders directly described by the document. |
| `related_tests` | Relative project paths to tests or suites verifying the behavior. |
| `related_assets` | Relative project paths to configuration files, assets, or scenes affecting documented behavior. |
| `requirements` | Stable requirement IDs (e.g., `MVP-FUN-002`, `RULE-COMBAT-004`) for impact and validation tracking. |

### Reference/Link Formatting Rules
*   **Document References (`prerequisite_docs`, `related_docs`):** Always use explicit relative Markdown paths with file extensions (e.g., `../explanation/Architecture.md` or `../../reference/ApiDetails.md`). This ensures robust link rendering and direct navigation on code platforms (such as VS Code or GitHub) and tools.
*   **Path References (`related_code`, `related_tests`, `related_assets`):** Always specify paths relative to the project root directory (e.g., `Assets/Scripts/Combat` or `src/components/Button.tsx`).

---

## Writing Style & Tone

*   **Imperative Mood:** Use imperative mood for instructional steps.
*   **Sentence Length:** Keep sentences short, concise, and direct.
*   **Terminology:** Define prerequisite concepts before dependent concepts. Do not explain concept B using concept A before concept A has been defined.
*   **Tone examples:**
    *   *Avoid:* "First you need to open Unity Editor", "Then you should click Run All", "If everything is fine, you'll see the tests pass".
    *   *Prefer:* "Open Unity Editor", "Click Run All", "Result: all tests pass".

---

## Diataxis Document Guidelines

### 1. Tutorials (Learning-Oriented)

*   **Scope:** A guided lesson for newcomers. Focus on a practical, learning-oriented path. Show the user how to do something, step-by-step, explaining *what* is happening at each stage but avoiding deep technical specs.
*   **Completeness Checklist:**
    *   **Learning Objectives:** What the user will achieve and learn.
    *   **Setup / Prerequisites:** Initial state, tools, or dependencies.
    *   **Guided Progression:** Ordered, simple instructions showing the task from start to finish.
    *   **Verification:** A checkpoint step showing the user how to confirm their progress.
*   **Template & Structure:**
    ```markdown
    # Tutorial: Creating a Custom Combat Unit (Game Project Example)
    
    Learn how to add and configure a new combat unit prefab.
    
    ## Learning Objectives
    - Configure unit attributes in a prefab.
    - Add the unit prefab to the unit spawn pool.
    
    ## Setup
    - Open the Unity project.
    - Locate `Assets/Prefabs/UnitTemplate.prefab`.
    
    ## Step-by-Step Instructions
    1. Duplicate `UnitTemplate.prefab` and name it `CustomUnit.prefab`.
    2. Open the prefab in the Inspector.
    3. Modify the health parameter to `150`.
    4. Drag `CustomUnit.prefab` into `Assets/Resources/SpawnPool.asset`.
    
    ## Verification
    - Click Play in Unity, select "Spawn Custom Unit" from the test menu, and confirm that the unit spawns with 150 health.
    ```

---

### 2. How-To Guides (Problem-Oriented)

*   **Scope:** Problem-oriented recipes to complete a specific task. Focus on completing a real-world task.
*   **Completeness Checklist:**
    *   **Preconditions:** Required environment, tools, and initial state.
    *   **Steps:** Numbered list with one concrete action per step.
    *   **Expected Results:** Observable outcomes after steps.
    *   **Edge Cases:** Recovery actions for errors or unexpected situations.
    *   **Verification:** How to confirm the task completed successfully.
*   **Template & Structure:**
    ```markdown
    # How to Run EditMode Tests (Game Project Example)
    
    Run EditMode tests using the Unity Test Runner.
    
    ## Preconditions
    - Unity Editor is open.
    - Test Runner window is open (`Window > General > Test Runner`).
    
    ## Steps
    1. Select the **EditMode** tab in the Test Runner window.
    2. Click **Run All**.
    3. Wait for progress bar to complete.
    
    ## Expected Results
    - Tests complete within 15 seconds.
    - The test list icons turn green.
    
    ## Edge Cases
    - **Test fails:** Check the Console log, resolve the compilation or runtime exception, and run tests again.
    - **Test Runner does not load:** Close Unity, delete the `Library` folder, and restart the project.
    
    ## Verification
    - Locate the summary bar at the top; verify the message "All tests passed" is visible.
    ```

---

### 3. References (Information-Oriented)

*   **Scope:** Detailed catalogs, API specs, schemas, database tables, configuration lists, and exact technical facts. Keep descriptions brief, structured, and factual.
*   **Completeness Checklist:**
    *   **Fact Sheets / Quick References:** Structural table of attributes, syntax, or parameters.
    *   **Field/Option Specifications:** Direct description of allowed ranges, types, and defaults.
    *   **Configuration / Implementation Code Snippets:** Short examples showing usage.
*   **Template & Structure:**
    ```markdown
    # Unit Attributes Configuration Reference (Game Project Example)
    
    Configuration schemas and boundaries for unit attributes.
    
    ## Attribute Configuration Table
    
    | Field | Type | Range | Description | Default |
    |-------|------|-------|-------------|---------|
    | `maxHp` | Integer | `[1, 999]` | Starting health points of the unit. | `100` |
    | `speed` | Float | `[0.1, 5.0]` | Speed multiplier on the grid. | `1.0` |
    | `defense` | Integer | `[0, 50]` | Damage reduction constant. | `0` |
    
    ## Configuration Example
    
    Specify properties in the unit configuration JSON (`Assets/Config/Units.json`):
    ```json
    {
      "unitId": "warrior_01",
      "maxHp": 120,
      "speed": 1.2,
      "defense": 5
    }
    ```
    ```

---

### 4. Explanations (Understanding-Oriented)

*   **Scope:** High-level discussions focusing on architecture, design choices, rationale, background context, and design trade-offs. Use diagrams (like PlantUML) to represent flows.
*   **Completeness Checklist:**
    *   **Architectural Overview:** The big picture of the system.
    *   **Core Concepts:** Terms, concepts, or algorithms involved.
    *   **Design Choices & Trade-offs:** Rationale behind decisions (why a certain solution was picked, trade-offs made).
    *   **Flowcharts / Sequence Diagrams:** Visual representation of logic or state changes.
*   **Template & Structure:**
    ```markdown
    # Unit Death Flow Explanation (Game Project Example)
    
    This document explains the architecture and state synchronization of unit death in combat.
    
    ## Architectural Overview
    
    Unit death is handled asynchronously to separate visual feedback (animations) from the gameplay state (grid registry).
    
    ```plantuml
    @startuml
    participant UnitHealth
    participant DeathController
    participant GridSystem
    
    UnitHealth -> DeathController : Health reaches 0 (trigger death)
    activate DeathController
    DeathController -> GridSystem : Remove unit from registry
    DeathController -> Visuals : Play death animations & FX
    deactivate DeathController
    @enduml
    ```
    
    ## Design Decisions & Trade-offs
    
    - **Instant Grid Deregistration:** The unit is immediately removed from the grid registry before the death animation finishes. 
      * *Rationale:* Prevents other units from selecting a dying unit as a target, avoiding synchronization bugs.
      * *Trade-off:* Requires holding a visual dummy object in the scene during the death animation, which slightly increases active object overhead.
    ```
