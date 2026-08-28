# Plan, Estimate, and Schedule Software Work

## Use When
- Creating or revising project scope, effort estimates, staffing, tasks, dependencies, or schedule.
- Evaluating feasibility or communicating forecast confidence.

## Required Context
- Product scope, constraints, acceptance, architecture, risks, and quality obligations.
- Available people, reusable assets, environment, historical data, and delivery constraints.
- Dependencies, uncertainty, and required milestones.

## Instructions
1. Use the management spectrum: clarify people, product, process, and project.
2. Apply W5HH: why is the system built, what is done, when, who owns it, where responsibilities reside, how work is performed, and how much resource is needed.
3. Bound software scope by functions, data, interfaces, performance, constraints, and acceptance; assess technical, economic, operational, and schedule feasibility.
4. Identify human, reusable software, and environmental resources; account for availability and onboarding.
5. Estimate using at least two defensible perspectives where risk justifies it:
   - Size-based estimates such as LOC or function points when local productivity data exists.
   - Use-case points when actor/use-case complexity and local calibration are available.
   - Process/task decomposition using estimated effort per activity.
   - Relative agile estimates and observed local throughput for short-horizon forecasting.
6. State assumptions, range, confidence, exclusions, and drivers; reconcile materially different estimates by investigating causes.
7. Define a project task set from the selected process, product decomposition, quality work, and risk responses.
8. Build a task network showing dependencies, parallel work, milestones, slack, and critical path.
9. Allocate people with communication, expertise, and dependency effects; do not assume effort and duration are interchangeable.
10. Establish a baseline schedule and track actual completion, remaining work, risks, and changed assumptions.
11. Reestimate when scope, staffing, productivity, architecture, or risk evidence changes.

## Decision Rules
- If scope is not bounded, do not present a precise estimate.
- If independent methods disagree substantially, inspect size assumptions, omitted tasks, productivity data, and risk before reconciling.
- If a deadline is fixed, negotiate scope, quality-neutral sequencing, resources, or staged delivery; do not silently remove essential quality work.
- If adding people requires significant onboarding and communication, expect near-term delay before any capacity gain.
- If historical data is not comparable, use it cautiously and widen uncertainty.
- If a task is large enough to hide progress or risk, decompose it until completion evidence is observable.

## Constraints
- Estimates are forecasts, not guarantees.
- Do not derive individual performance judgments from estimate variance.
- Include reviews, testing, configuration, documentation, integration, support preparation, and risk work.
- Schedule dependencies and resource contention must be represented.
- Replanning is required when assumptions change; preserving an obsolete baseline is not control.

## Failure Modes
- **Single-date certainty** — Cause: assumptions and variance hidden. Correction: provide ranges, confidence, and drivers.
- **Schedule slips despite task completion** — Cause: integration and quality tasks omitted. Correction: include full process work and dependency milestones.
- **Late project worsens after hiring** — Cause: onboarding and communication ignored. Correction: assign bounded work and protect experienced staff.
- **Velocity forecast fails** — Cause: cross-team comparison or changing scope/team. Correction: calibrate locally and use recent stable observations.

## Verification
- Scope, feasibility, resources, assumptions, and exclusions are explicit.
- Estimates use traceable local data or clearly labeled judgment.
- Task network includes quality and risk work.
- Critical path and milestone evidence are visible.
- Forecast updates reflect actual evidence and changed assumptions.

## Required Terms
- [W5HH principle](../glossary.md#w5hh-principle) — ensures planning questions are not omitted.
- [Function point](../glossary.md#function-point) — matters when selecting size-based estimation.

## Source Locators
- Ch 24 §§24.1–24.8, pp. 491–502.
- Ch 25 §§25.1–25.11, pp. 505–530.
