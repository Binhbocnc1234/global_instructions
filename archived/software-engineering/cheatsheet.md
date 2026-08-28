# Decision Cheatsheet

## Route the Situation

| If the dominant uncertainty is… | Start with… |
|---|---|
| What users need | Requirements elicitation and scenarios |
| Whether an idea works | Bounded prototype with a decision criterion |
| System qualities or dependencies | Architecture scenarios and risk prototype |
| Correct component behavior | Partitions, boundaries, state, paths, and errors |
| Collaboration between components | Incremental integration plus regression |
| Release confidence | Requirement validation, specialized tests, configuration audit, residual risk |
| Forecast or deadline | Bounded scope, multiple estimates, dependency network, risk |
| Recurring defects | Origin/escape analysis, earlier review, regression, process correction |
| New tool or process | Gap assessment and measured pilot |

## Cross-Cutting Rules

- If behavior is not observable, clarify the requirement before estimating or testing.
- If a decision is costly to reverse, evaluate alternatives and risks early.
- If an error can propagate, review before the next activity consumes the work.
- If values have limits, test below, at, and above them.
- If behavior depends on history, model and test states and transitions.
- If change affects shared data or dependencies, expand regression beyond direct callers.
- If a metric cannot change a decision, stop collecting it.
- If a risk lacks owner, trigger, and response, it is not managed.
- If a prototype contains shortcuts, rebuild or explicitly accept the debt.
- If a release cannot be reproduced, configuration management is incomplete.
- If user experience or playability is the question, include representative humans.
- If evidence is weak and potential harm is high, reduce exposure and escalate.

## Release Evidence

| Question | Required evidence |
|---|---|
| Built right? | Reviews, component/interface/integration tests |
| Right product? | Traceable stakeholder acceptance and user validation |
| Safe and secure enough? | Threat/risk analysis, negative tests, residual-risk decision |
| Performs in context? | Representative load, device, environment, timing, recovery |
| Reproducible and reversible? | Baseline, dependency/build audit, migration/rollback test |
| Supportable? | Documentation, monitoring, ownership, known limitations |

## Smells

- Broad flags cross interfaces → control coupling or mixed responsibility.
- One component changes for unrelated reasons → low cohesion.
- Tests pass but requirements are unlinked → validation gap.
- Late defects originate in requirements/design → strengthen earlier review.
- Regression is skipped → suite/environment is unsustainable.
- Estimates are single numbers → assumptions and uncertainty are hidden.
- Dashboard improves while users suffer → metric is incomplete or gamed.
- Process exists only in a document → not institutionalized.
