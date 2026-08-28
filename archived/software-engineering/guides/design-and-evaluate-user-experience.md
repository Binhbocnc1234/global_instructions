# Design and Evaluate User Experience

## Use When
- Designing interfaces, interaction flows, information architecture, or accessibility.
- Evaluating usability or adapting an experience for mobile/web contexts.

## Required Context
- User groups, goals, capabilities, frequency of use, environment, and devices.
- Tasks, content, data, error risks, accessibility needs, and business constraints.
- Existing interaction conventions and platform guidance.

## Instructions
1. Research representative users and work/play context rather than relying on developer assumptions.
2. Model user classes by goals, experience, capabilities, frequency, and relevant differences; avoid decorative personas.
3. Analyze tasks into goals, actions, information needs, errors, frequency, sequence, and environmental constraints.
4. Establish information architecture and navigation before visual polish.
5. Apply the three golden rules:
   - Place users in control through direct, interruptible, reversible interaction.
   - Reduce memory load through recognition, meaningful defaults, visible state, and progressive disclosure.
   - Maintain consistency in language, layout, commands, feedback, and expected behavior.
6. Design feedback for action, progress, success, failure, disabled state, and recovery.
7. Prototype interaction at the lowest fidelity that can answer the current question.
8. Conduct expert review against usability/accessibility guidance and user tests with representative tasks.
9. Measure task success, time, errors, recovery, assistance, satisfaction, and qualitative confusion; investigate causes, not only scores.
10. Iterate the design and retest affected tasks.

## Decision Rules
- If users must remember information across views, make it visible or remove the dependency.
- If an operation is destructive or costly, provide prevention, confirmation where appropriate, and recovery/undo.
- If expert review and user behavior disagree, prioritize observed task evidence while investigating sampling and context.
- If accessibility conflicts with visual convention, preserve perceivability, operability, understanding, and robustness.
- If a prototype question concerns flow, use low fidelity; if it concerns visual hierarchy or touch targets, use realistic fidelity.
- If different user classes have genuinely different goals, adapt workflow rather than merely relabeling one design.

## Constraints
- Do not make color the only carrier of meaning.
- Keyboard, assistive technology, text scaling, focus, contrast, and error identification must be considered where applicable.
- Consistency does not require preserving a harmful convention.
- User tests evaluate the design, not participant competence.

## Failure Modes
- **Users require explanation** — Cause: designer knowledge substituted for visible cues. Correction: simplify flow and improve feedback.
- **Prototype validates only aesthetics** — Cause: no representative tasks. Correction: test goal completion and recovery.
- **Accessibility added late** — Cause: structural interaction decisions already exclude users. Correction: include accessibility constraints during analysis.
- **Inconsistent controls** — Cause: local screen optimization. Correction: define shared interaction vocabulary and patterns.

## Verification
- User classes and tasks are evidence-based.
- Main, alternative, error, cancellation, and recovery flows are evaluable.
- Golden-rule and accessibility checks are documented.
- Representative users complete critical tasks with measured outcomes.
- Revisions are linked to observed issues and retested.

## Source Locators
- Ch 12 §§12.1–12.10, pp. 234–261.
- Ch 13 §§13.1–13.5, pp. 265–282.
- Ch 21 §§21.3, 21.11, pp. 415–417, 430–434.
