# Measure and Analyze Software Work

## Use When
- Selecting product, quality, test, maintenance, process, or project metrics.
- Investigating defects, forecasting, or deciding whether an engineering practice works.

## Required Context
- The decision or improvement goal the measurement must support.
- Definitions, collection sources, population, normalization basis, and data quality.
- Stakeholder behavior risks created by the metric.

## Instructions
1. Begin with a goal and decision; derive questions whose answers could change action.
2. Select direct measures, calculate metrics, and interpret indicators only with context.
3. Define each measure operationally: unit, scope, source, frequency, owner, exclusions, and uncertainty.
4. Prefer automatically collected data when it is semantically correct; audit automation against reality.
5. Use product metrics selectively for requirements, design, architecture, components, interfaces, code, tests, and maintenance.
6. For quality, combine defect severity, origin, detection/escape stage, density, correction effort, recurrence, reliability, and stakeholder outcomes.
7. For testing, examine requirement/risk coverage, failures by class, defect yield, regression duration, flakiness, and escaped defects; do not rely on execution coverage alone.
8. For reviews, track preparation, assessment, rework effort, size, issue severity, density, and downstream escapes where the data will improve reviews.
9. Analyze trends, distributions, cohorts, and normalized comparisons rather than isolated totals.
10. Communicate uncertainty and avoid causal claims from correlation alone.
11. Act on findings, then evaluate whether the action improved the intended outcome.
12. Retire metrics that are gamed, costly, invalid, or no longer influence decisions.

## Decision Rules
- If no decision changes for any possible metric result, do not collect it.
- If size or opportunity differs, normalize before comparison.
- If a metric becomes a target, inspect gaming and unintended behavior before trusting improvement.
- If defect counts fall while user failures rise, the measure is incomplete or detection weakened.
- If a prediction lacks sufficient local data, present a range and assumptions rather than false precision.
- If an individual-level metric ignores task context and collaboration, do not use it for performance evaluation.

## Constraints
- Measures, metrics, and indicators are distinct; do not report interpretation as raw fact.
- Preserve privacy and minimize personal data.
- Do not compare teams or products without accounting for domain, size, complexity, lifecycle, and process differences.
- Cyclomatic complexity, coverage, LOC, velocity, and defect counts are diagnostic inputs, never universal quality scores.

## Failure Modes
- **Dashboard grows, decisions do not improve** — Cause: data-first measurement. Correction: remove metrics not tied to questions/actions.
- **Metric improves through gaming** — Cause: target pressure. Correction: use balanced evidence and inspect behavior.
- **False causal conclusion** — Cause: uncontrolled confounding. Correction: seek comparative evidence, experiment, or label inference.
- **Data collection is inconsistent** — Cause: ambiguous definitions. Correction: operationalize and audit collection.

## Verification
- Every metric maps to a goal, question, interpretation, and potential action.
- Definitions and collection procedures are reproducible.
- Comparisons are normalized and uncertainty is visible.
- Findings produce an assigned decision or are explicitly classified as exploratory.
- Metric side effects and continued value are reviewed.

## Required Terms
- [Indicator](../glossary.md#indicator) — distinguishes interpreted decision evidence from a raw measure.
- [Cyclomatic complexity](../glossary.md#cyclomatic-complexity) — constrains its use to control-flow risk and path planning.

## Source Locators
- Ch 16 §16.3, pp. 327–330.
- Ch 17 §§17.4–17.7, pp. 343–353.
- Ch 23 §§23.1–23.10, pp. 461–487.
