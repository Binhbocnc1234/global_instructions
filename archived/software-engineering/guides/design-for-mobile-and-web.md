# Design for Mobile and Web Contexts

## Use When
- Building software for variable devices, browsers, connectivity, orientation, or context.
- Designing touch, gesture, voice, responsive, or context-aware interaction.

## Required Context
- Target devices, operating systems, browsers, screen classes, inputs, sensors, and accessibility services.
- Network variability, offline requirements, power/memory limits, privacy, and security constraints.
- Content, navigation, architecture, and deployment channels.

## Instructions
1. Inventory platform variability and define the supported matrix by user value and risk.
2. Design for interruption, pause/resume, backgrounding, orientation, loss of connectivity, and resource pressure as normal behavior.
3. Keep critical actions reachable, visible, and suitable for touch target and one-handed constraints where relevant.
4. Separate platform-independent domain behavior from device, browser, presentation, and service adapters.
5. For context-aware behavior, define sensed data, confidence, privacy purpose, retention, fallback, and user control.
6. Coordinate the web/mobile design pyramid: interface, aesthetic, content, architecture, navigation, and components must support the same user goals.
7. Make navigation predictable; provide orientation, return paths, meaningful labels, and protection from dead ends.
8. Budget performance, memory, battery, data, and startup behavior; validate budgets on representative low-end conditions.
9. Design offline and synchronization semantics explicitly, including conflict and recovery behavior.
10. Validate on real devices/environments, not emulator or desktop behavior alone.

## Decision Rules
- If the device or context signal is uncertain, degrade safely and let the user correct the assumption.
- If content density requires desktop-style precision, redesign the task rather than shrinking controls.
- If connectivity is optional for a task, queue or cache safely and communicate synchronization state.
- If a platform-specific capability creates domain coupling, isolate it behind an adapter.
- If the support matrix is too large to test credibly, narrow official support by evidence rather than claiming universal compatibility.

## Constraints
- Do not collect context data without explicit purpose, protection, and user expectation.
- Do not assume constant bandwidth, stable latency, or uninterrupted execution.
- Do not let responsive layout hide essential functions or make focus/navigation order incoherent.
- Security and privacy controls must survive platform variation and offline behavior.

## Failure Modes
- **Works only on developer device** — Cause: unsupported environmental assumptions. Correction: define and execute a representative matrix.
- **State lost after interruption** — Cause: lifecycle treated as exceptional. Correction: persist recoverable state and test transitions.
- **Context-aware surprise** — Cause: invisible inference and no override. Correction: expose state, explain action, and provide control.
- **Synchronization corruption** — Cause: conflict policy unspecified. Correction: define ownership, versioning, merge/retry, and user recovery.

## Verification
- Supported environments and degraded modes are explicit.
- Interruption, orientation, resource pressure, connectivity, and synchronization have tests.
- Context behavior has privacy and fallback evidence.
- Performance budgets pass on representative constrained devices.
- Navigation and accessibility remain coherent across layouts.

## Source Locators
- Ch 13 §§13.1–13.9, pp. 265–287.
- Ch 21 §§21.1–21.8, pp. 413–425.
