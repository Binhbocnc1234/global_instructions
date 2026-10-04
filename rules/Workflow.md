# Request Workflow

Summary: In what order do I handle a request? The steps from classifying the request to the final response, which rules each task type follows, and the shape of the final response.
Why: the other global rule files are grouped by topic, not by order. Without one ordered list, an agent applies the rules it happens to recall and skips a step, most often the reusable-knowledge step at the end.

## Steps

1. **Classify.** Name the type of every task in the request, from the table below. A request often carries two or more tasks; classify each one.
2. **Route.** In a project, read its documentation index under [Route Through the Documentation Index](WorkStyle.md#route-through-the-documentation-index), and look up unknown project concepts under [Identify unknown concepts](SoftwareDevelopment.md#identify-unknown-concepts).
3. **Work.** Run the workflow of each task type. During every type, [Blocker Detection and Stop Policy](WorkStyle.md#blocker-detection-and-stop-policy) and [The Agent Does What It Does Better](DivisionOfLabor.md#the-agent-does-what-it-does-better) apply.
4. **Record.** Assess whether [Reusable Knowledge](ReusableKnowledge.md#reusable-knowledge) applies. A correction in this request always gets this step, under [A Correction Is a Trigger](ReusableKnowledge.md#a-correction-is-a-trigger).
5. **Respond** in the [Final Response Format](#final-response-format).

| Task type | Example request | Workflow |
|---|---|---|
| Explanation | "Explain how ext4 finds a file" | [Explaining a Technique](Communication.md#explaining-a-technique) and [Evidence Labels](Communication.md#evidence-labels). The `ask` skill when the answer depends on context the agent lacks. Do not change the project. |
| Design | "Design the UI for the Collection scene" | How a requirement should work and be structured before it is built. [Requirement elicitation](WorkStyle.md#requirement-elicitation). Do not change the project. |
| Implementation, migration | "Add a card that summons an Exploder" | [Software Development](SoftwareDevelopment.md): construction, tests, commit. [Task Management](TaskManagement.md#request-budget) when the work exceeds one request budget. |
| Bug fixing | "Fix the crash when the player dies during a pause" | [Debugging](software-development/Debugging.md), then the tests and commit of [Software Development](SoftwareDevelopment.md). |
| Review or audit | "Review this PR description" | [Do not fill the response with noise](WorkStyle.md#do-not-fill-the-response-with-noise) and [Report a Risk Only With Its Failure](WorkStyle.md#report-a-risk-only-with-its-failure). [Documentation Audit](Authoring.md#documentation-audit) for a document. |
| Rule change | "Add a rule that ..." | [Rule Ownership](RuleOwnership.md). |

## Final Response Format

- **Vocabulary**: first, only when [Teach the Standard Term](Communication.md#teach-the-standard-term) applies.
- **Task type**: name the type of each task in the request, from step 1.
- **Answer**: only an explanation task needs this. For an implementation, do not list the changes: the git diff already shows them.
- **Lesson**: only when step 4 handled a correction. Name the cause and where it was recorded or proposed, or why nothing was recorded.
- **Remaining work**: only work that an unmade decision or an unavailable dependency actually blocks.
- **Questions**: last, and only when an unmade decision blocks the requested work. State the recommended option, and what it costs or protects. An offer of work the request did not name is noise under [Do not fill the response with noise](WorkStyle.md#do-not-fill-the-response-with-noise). For example, the request asks why the chat shows an image under a command's output, and the cause is a feature of the editor that works as designed. Do not end with "Do you want these images removed?", because the developer did not say the images were unwanted.

[Response Relevance](Communication.md#response-relevance) decides what goes inside each part.

Why: a fixed order lets the developer find the answer, the lesson, and the open questions in the same place in every response. The Task type line also shows the developer how the agent read the request, so a wrong reading is caught before the work is checked.
