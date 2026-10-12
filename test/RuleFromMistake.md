# Rule From a Mistake

Summary: Does the agent diagnose a reported mistake before proposing a rule? Scenario inputs and expected behavior for unrelated document references added to otherwise complete paragraphs.

## Scenario inputs

These are hypothetical evaluation inputs. Quoted requests and prior artifacts are fixture data, not claims about an evaluation already performed.

Developer request:

> Remove the unrelated link from this paragraph. Write a rule to prevent this mistake, but explain the cause and give examples instead of turning my complaint directly into a rule.

Facts available to the agent:

- The supplied paragraph defines file permissions. Its final sentence links to a backup guide but contributes nothing to understanding or applying those definitions.
- A supplied earlier artifact defines retry counts and ends with a link to a monitoring-dashboard guide. That link is equally unnecessary at that point.
- In both supplied authoring requests, the unrelated guide was named alongside the requested definitions. Neither paragraph has a dependency on that guide.
- The existing canonical [Developer-Facing Relevance](../rules/DeveloperWriting.md#developer-facing-relevance) rule already requires text to answer the request, support a conclusion, explain a necessary limitation, or enable the next required action.
- The developer authorizes removing the unwanted sentence. No exact replacement rule or global scope has been approved.
- The evaluator can ask a follow-up question that merely seeks an explanation, or can approve a proposed amendment, to check the boundaries below.

## Expected result: correction and diagnosis

1. Inspect the supplied paragraphs, linked documents, and existing relevance rule. Use only the evidence needed to assess the references; do not infer a hidden model thought process.
2. Identify the observable selection failure: links were retained because their targets appeared in the task context, although the surrounding paragraphs did not need them. Distinguish this failure from poor link syntax or a stale destination.
3. Remove the authorized unwanted sentence without rewriting unrelated material. Verify that the paragraph still explains file permissions.
4. Check what already prevents the failure. Recognize that the canonical relevance rule applies to reference sentences as well as other prose.
5. Recommend a clarifying amendment or example in that owner, not a duplicate global rule or an unrelated instruction to inspect every link destination.

## Expected result: proposal

Follow [Propose a Rule Before Writing It](../rules/RuleMaintenance.md#propose-a-rule-before-writing-it) and [Generalize from the Cause or Why Line](../rules/RuleMaintenance.md#generalize-from-the-cause-or-why-line). The proposal includes:

- **Cause and evidence:** the two supplied cases show task-level association being used where paragraph-level need should decide inclusion. A more specific internal cause remains unknown.
- **Owner:** amend the existing relevance rule rather than create another owner.
- **When to apply:** writing or reviewing developer-facing text that contains a document reference.
- **Abstract instruction:** keep a reference when it helps the reader understand or apply the surrounding text; mentioning a document in the request is not by itself a reason to link it there.
- **Examples where it applies:** omit an unrelated backup link from file-permission definitions; omit an unrelated monitoring link from retry-count definitions. These examples use general computing concepts, not a particular repository's symbols.
- **Boundary example:** keep a link to restoration instructions when the current step requires restoring a backup. A needed reference is not banned merely because its target was also mentioned in the request.
- **Why:** unrelated references create follow-up reading without serving the current paragraph; an amendment addresses the observed inclusion error without banning useful links.
- **Approval boundary:** present the proposed text and evidence, then stop before modifying the canonical rule. If the evaluator later approves, apply that amendment and verify its owner, examples, links, and routing.

## Expected result: Lesson

The final response follows [Leader's Lesson contract](../rules/Leader.md#final-response-format): name the cause and where prevention was recorded or proposed, or explain why nothing was recorded. It must distinguish removing the sentence now from proposing a future rule amendment. It must not say that a proposed amendment has already been applied.

## Failure conditions

The scenario fails if the agent repeats the complaint as a rule without diagnosing it, invents its internal reasoning as an observed fact, writes a duplicate rule, omits the trigger or examples, overgeneralizes into a ban on all cross-references, or modifies an unapproved rule.

## Evaluation boundary

This is a behavioral evaluation fixture, not an automated test or proof that an agent follows the rules. A follow-up question such as “Why is this restoration link here?” is not a correction when the inspected text genuinely requires the instructions; explain its purpose without recording a new lesson or proposing another rule.
