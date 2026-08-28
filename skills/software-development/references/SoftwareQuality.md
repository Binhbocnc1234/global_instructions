---
type: technical
audience: agent
status: active
language: en
description: Defines the software-quality model, one concrete example per attribute, and the evidence needed to apply it.
---

# Software Quality Model

Use this reference to select and operationalize product-quality and quality-in-use requirements. It retains the ISO/IEC 25010 model summarized in the archived `software-engineering` skill's source: *Software Engineering: A Practitioner's Approach*, 9th edition, Chapter 15, pp. 313–314. It is not a substitute for a current standard, legal requirement, or platform-specific accessibility guidance.

## How to Read the Tables

- A **characteristic** is the general property, such as reliability.
- A **subcharacteristic** is the testable facet of it, such as recoverability. A requirement attaches here, not at the characteristic level.
- The **example** shows one shape the subcharacteristic takes in a 2D game project. It illustrates the attribute; it is not the required threshold. Replace it with the target of the actual project.

Select only the attributes that are material to the request. An attribute that no stakeholder is affected by produces a score, not a decision.

## Operationalize a Quality Requirement

1. Identify the stakeholder, task, operating environment, failure consequence, and change scope.
2. Select only material characteristics; do not score every characteristic by default.
3. Write a measurable scenario: `Given <context/trigger>, when <stimulus>, <system or user> achieves <response>, measured by <metric> <=/>= <threshold>.`
4. State the evidence method and owner: automated test, static analysis, benchmark, prototype, technical review, user study, or production measurement.
5. Record meaningful trade-offs and residual risk. Re-evaluate the scenario when its architecture, platform, workload, or user context changes.

Example: `On the lowest supported device, when a player opens a saved game with 1,000 entities, the scene is interactive within 2 seconds in 95% of 30 cold-start runs.`

## Product Quality

Use these attributes to assess the static and dynamic properties of the system.

| Characteristic | Subcharacteristic | Example |
|---|---|---|
| Functional suitability | Functional completeness | The design says the shop sells weapons, armour, and potions. The shop screen sells all three, not weapons only. |
| Functional suitability | Functional correctness | A 20% buff on a 50-damage attack deals 60, not 59 from integer truncation. |
| Functional suitability | Functional appropriateness | The player equips a sword by dragging it onto the character, instead of selling it and rebuying it in another slot. |
| Performance efficiency | Timing behavior | Frame time stays below 16.6 ms while 200 bullets are active. |
| Performance efficiency | Resource utilization | The build stays below 400 MB of RAM on a 2 GB Android phone. |
| Performance efficiency | Capacity | The save format still loads when the inventory holds 5,000 items. |
| Compatibility | Coexistence | The game holds 60 FPS while the Discord overlay and OBS run on the same machine. |
| Compatibility | Interoperability | An achievement unlock reaches the Steam client through Steamworks and appears on the player profile. |
| Usability | Appropriateness recognizability | A visitor reads the store page and knows within 30 seconds that this is a turn-based roguelike, not an action game. |
| Usability | Learnability | A new player completes the tutorial and defeats the first enemy without opening a wiki. |
| Usability | Operability | Every menu is fully operable with a gamepad D-pad. No screen requires a mouse. |
| Usability | User-error protection | `Delete save slot` asks for confirmation and names the slot in the prompt. |
| Usability | Aesthetics | Every screen uses one font family and one 8-pixel spacing grid. |
| Usability | Accessibility | Subtitles scale to 150%, and no state is signalled by red-versus-green alone. |
| Reliability | Maturity | A 4-hour automated soak run produces zero unhandled exceptions. |
| Reliability | Availability | The online leaderboard answers 99% of requests, and the game still starts when it answers none. |
| Reliability | Fault tolerance | A corrupted `settings.json` falls back to defaults instead of blocking the main menu. |
| Reliability | Recoverability | A crash during a level returns the player to the last autosave, losing at most 60 seconds of play. |
| Security | Confidentiality | The Steam Web API key is read from an environment variable. It is absent from committed source and from the shipped build. |
| Security | Integrity | The save file carries an HMAC, so a hand-edited gold value is rejected on load. |
| Security | Accountability | The server log records which account granted a premium item and when, so a refund dispute can be traced. |
| Security | Authenticity | An IAP receipt is validated against the store server before the item is granted, so a forged receipt fails. |
| Maintainability | Modularity | Assembly `MvA.Bullet` compiles without referencing UI assemblies, so a HUD change cannot break bullets. |
| Maintainability | Reusability | One object-pool component serves bullets, particles, and damage numbers, with no per-type copy. |
| Maintainability | Modifiability | Changing the enemy spawn delay means editing one ScriptableObject field, not five prefabs. |
| Maintainability | Testability | Damage calculation is a pure C# method, so an EditMode test calls it without loading a scene. |
| Portability | Adaptability | The HUD stays readable at 16:9 and at 20:9 without a separate scene per aspect ratio. |
| Portability | Installability | The APK installs on Android 8 and later, and reports a clear message on earlier versions. |
| Portability | Replaceability | Replacing the analytics SDK touches one wrapper class, because gameplay code depends on `IAnalytics`. |

## Quality in Use

Evaluate these attributes with a specific user, task, and context rather than inferring them from product properties.

| Characteristic | Meaning | Example |
|---|---|---|
| Effectiveness | Accuracy and completeness with which users achieve goals | 9 of 10 playtesters finish the tutorial level without help from the developer. |
| Efficiency | Resources users expend to achieve goals accurately and completely | A player rebinds the jump key in under 30 seconds and 3 clicks. |
| Satisfaction | Usefulness, trust, pleasure, and comfort | After the session, testers rate `I want to play again` at 4 of 5 or higher, and report that deaths felt fair. |
| Freedom from risk | Mitigation of economic, health, safety, and environmental risks | The boss flash effect stays below 3 flashes per second for photosensitivity, and every IAP shows its real-currency price before purchase. |
| Context coverage | Completeness and flexibility across intended contexts | The game stays playable on a phone in sunlight and on a TV at 2 metres, because UI text respects a minimum readable size. |

## Select Evidence by Characteristic

| Characteristic | Typical evidence |
|---|---|
| Functional suitability | Requirement-to-test traceability, acceptance scenarios, negative cases |
| Performance efficiency | Representative load or device benchmark with a budget |
| Compatibility and portability | Explicit support matrix; integration, installation, upgrade, and rollback checks |
| Usability and quality in use | Representative-task observation, success rate, time, errors, recovery, and qualitative feedback |
| Reliability | Failure-rate, availability, recovery, fault-injection, and resilience evidence suited to the system |
| Security | Threat model, control review, security tests, and accepted residual risk |
| Maintainability | Cohesion and dependency review, change effort, code readability, tests, and successful scoped modification |

Do not replace representative user evidence with an internal quality score. Do not state that a quality has been achieved without evidence from the selected scenario.
