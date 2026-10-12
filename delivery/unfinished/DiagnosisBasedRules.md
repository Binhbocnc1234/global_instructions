## Why

The original request reviewed an external debugging skill, cause-to-solution reasoning in rule maintenance, the Lesson contract, and two behavioral evaluation scenarios under `test/`.

The developer subsequently decided to delete `Debugging.md` and its dedicated role. The proposed external-skill adaptation is withdrawn, not deferred. No debugging workflow is awaiting implementation. The condition for any future reconsideration belongs in [Reintroducing Debugging Rules](../../rules/RuleMaintenance.md#reintroducing-debugging-rules), not in this task.

The two scenarios remain evaluation fixtures, not global rules or completed runtime evaluations. Existing developer edits outside the authorized removal remain untouched.

## Remaining proposal

Only the earlier rule-maintenance proposals remain awaiting approval. They do not restore a debugging workflow or role.

The diagnosis principle already exists in [A Correction Is a Trigger](../../rules/RuleMaintenance.md#a-correction-is-a-trigger): name the cause, decide whether it recurs, then route prevention. The proposed clarification distinguishes the observed failure, evidence for its cause, proposed prevention, and a scenario demonstrating the prevention. A complaint establishes a symptom, not automatically the correct rule. Assess whether a fact, routing repair, tool repair, or clarification of an existing rule addresses the cause.

Example: a check reports success after discovering zero tests. Inspect the invocation and discovery output before proposing prevention. If a wrong fixture path caused the empty run, repair that invocation and clarify the existing nonzero-count requirement rather than add an unrelated instruction to run every test suite. By contrast, a question about a correctly executed test does not itself establish an error.

Proposed rule-shape text for RuleMaintenance:

`When to apply: drafting or revising a rule proposal.`

`State an observable trigger under When to apply, then the abstract instruction, examples that demonstrate its application and boundary, and a Why that identifies the cause or need it addresses.`

`Why: an instruction without its trigger can fire in unrelated situations; without causal reasoning and examples, the reader cannot check whether it addresses the reported failure.`

Example: when a correction reveals that several commands overwrite a developer's log, identify the observable trigger, state the general log-preservation action, show its application, and explain the overwritten evidence it prevents. A file containing only facts is not a rule proposal and does not need this shape.

Preserve the existing ownership of cause diagnosis, example selection, scope evidence, and approval rather than duplicate those constraints. This proposal concerns rule authoring, not the format of every final response.

The unrelated-reference example belongs in [Developer-Facing Relevance](../../rules/DeveloperWriting.md#developer-facing-relevance). The observed selection failure was treating a document's relevance to the request as a reason to reference it in a paragraph that did not need it. The proposed example and boundary are exercised by [RuleFromMistake](../../test/RuleFromMistake.md).

No change to [Leader's Lesson contract](../../rules/Leader.md#final-response-format) is proposed: it already requires naming the cause and where it was recorded or proposed, or why nothing was recorded. It does not require examples on the Lesson line.

## Step 1: Review and prepare evaluation fixtures

- [x] #1 Retrieve and critically review the external skill; its adaptation was subsequently withdrawn
- [x] #2 Inspect the former Debugging rules, RuleMaintenance, and the Lesson requirement
- [x] #3 Create the game-debugging scenario under `test/`
- [x] #4 Create the rule-from-mistake scenario under `test/`
- [x] #5 Verify file paths, links, line counts, and scenario structure; this was static review, not an actual agent evaluation

## Step 2: Approve and apply the remaining rule-maintenance proposal

- [ ] #1 Obtain approval for the correction clarification, rule-shape guidance, and reference example only
- [ ] #2 Apply approved changes only in their canonical owners, preserving unrelated developer edits
- [ ] #3 Check triggers, abstract instructions, examples, causal reasons, unique ownership, links, and routing against the scenario fixtures
- [ ] #4 Report verification limits and submit the rule diff for required review before committing

## Step 3: Remove the dedicated Debugging role

- [x] #1 Remove the rule file, global import, Leader workflow dependency, and role-routing entry without relocating the deleted workflow
- [x] #2 Record the developer-authorized condition for reconsidering debugging-specific rules in RuleMaintenance
- [x] #3 Withdraw the external-skill adaptation and remove the scenario's dependency on the deleted report contract
- [x] #4 Verify active references, links, imports, and preservation of unrelated edits
