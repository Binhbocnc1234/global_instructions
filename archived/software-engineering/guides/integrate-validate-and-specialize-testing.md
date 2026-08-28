# Integrate, Validate, and Specialize Testing

## Use When
- Combining components, building regression suites, validating releases, or testing specialized environments.
- Testing mobile/web, performance, real-time, AI, virtual environments, usability, accessibility, or playability.

## Required Context
- Tested components, architecture, dependencies, interfaces, build process, and integration order.
- Requirement-derived validation criteria and representative user scenarios.
- Change impact, previous tests/defects, target platforms, workloads, and operational risks.

## Instructions
1. Choose an incremental integration strategy:
   - Top-down to verify major control and decision behavior early, replacing stubs progressively.
   - Bottom-up to combine low-level clusters first, using drivers and reducing stub complexity.
   - For object-oriented systems, integrate by event/use thread or from independent classes toward dependent collaborators.
2. Integrate one controlled component or cluster at a time and test newly established data, control, and interface paths.
3. Build frequently and run smoke tests aimed at show-stopping failures that prevent the build's intended function.
4. After every major change or integration, run regression containing:
   - Representative tests across major functions.
   - Tests for behavior likely affected by the change.
   - Tests for changed components.
   - Tests for previously escaped defects.
5. Keep regression economical by retaining cases that address distinct error classes and critical functions; remove obsolete redundancy with evidence.
6. Maintain an integration test specification covering phases/builds, interfaces, test cases, expected results, schedule, environment, and records.
7. Conduct validation from stakeholder requirements and use scenarios; include functional, behavioral, performance, usability, compatibility, security, and acceptance evidence as applicable.
8. Add specialized testing from context:
   - Mobile: devices, orientation, gestures, virtual keyboard, voice, alerts, interruption, network, resources.
   - Web: content, interface, navigation, compatibility, internationalization, security, load, stress, and performance.
   - Real time: event timing, deadlines, interrupt handling, load, recovery, and resource contention.
   - AI: data/model inspection, dynamic behavior, metamorphic/model-based checks, robustness, bias, drift, and uncertain oracles.
   - Virtual/game environments: usability, accessibility, comfort, consistency, feedback, challenge, balance, and playability with humans.
   - Documentation/help: correctness, consistency, navigation, and task success.
9. Test installation, configuration, upgrade, rollback, and representative production-like environments before release.
10. Record residual limitations and monitor field behavior after deployment.

## Decision Rules
- If major control risk dominates, begin top-down; if reliable utilities/data services dominate, begin bottom-up; combine approaches when architecture warrants.
- If a new component changes shared data or indirect dependencies, expand regression beyond direct collaborators.
- If regression duration causes skipping, tier it by speed/risk and optimize environment or redundant cases before reducing critical coverage.
- If expected AI output is not exact, use invariants, metamorphic relations, statistical bounds, reference models, and human evaluation.
- If user experience, accessibility, or playability is the question, automated functional tests are necessary but insufficient.
- If performance requirements specify load or timing, reproduce representative and worst credible conditions rather than extrapolating from trivial tests.

## Constraints
- Avoid big-bang integration.
- Smoke tests are not substitutes for full regression or validation.
- Specialized test matrices must be prioritized and explicit; “works everywhere” is not evidence.
- Test data and environments must be controlled enough to reproduce failures.
- Human-subject evaluation must use representative users and ethical handling of collected data.

## Failure Modes
- **Failure cannot be isolated** — Cause: too many components integrated at once. Correction: restore incremental builds and interface checkpoints.
- **Old behavior breaks unnoticed** — Cause: regression covers only the new feature. Correction: add representative and impact-based cases.
- **Mobile/web defect appears only in field** — Cause: narrow environment matrix. Correction: select devices/browsers by usage and risk.
- **AI test always passes** — Cause: vague oracle. Correction: define properties, bounds, adversarial cases, and human acceptance.
- **Game is correct but not playable** — Cause: only deterministic rules were tested. Correction: run structured playability sessions and analyze player behavior.

## Verification
- Integration order and rationale are documented.
- Every build has smoke evidence and major changes have regression evidence.
- Validation traces to stakeholder requirements and scenarios.
- Specialized test scope matches platform and operational risk.
- Installation, recovery, configuration, and documentation are verified where relevant.

## Required Terms
- [Regression testing](../glossary.md#regression-testing) — defines protection against unintended change effects.
- [Smoke testing](../glossary.md#smoke-testing) — distinguishes fast build viability checks from complete testing.
- [Test oracle](../glossary.md#test-oracle) — matters where correctness is not directly observable.

## Source Locators
- Ch 20 §§20.1–20.7, pp. 396–409.
- Ch 21 §§21.1–21.13, pp. 413–435.
- Ch 22 §22.4, pp. 446–447.
