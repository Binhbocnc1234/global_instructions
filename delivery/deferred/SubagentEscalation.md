# Subagent Escalation

Summary: When should subagent delegation be reconsidered? Deferred investigation, evidence from the 2026-10-09 review, and decisions required before re-enablement.

## Why

The developer deferred subagent delegation on 2026-10-09 because the evidence does not establish a benefit for their workload. Use the single-session specialist workflow in [Leader](../../rules/Leader.md#role-routing).

The trigger for reconsideration is an observed failure of the no-subagent solution. Record the failed outcome and its evidence before proposing escalation. A role transition, an available tool, or a hypothetical benefit is not that evidence. This task remains deferred until the developer resumes it. The trigger does not authorize automatic re-enablement.

The harness task `SubagentUsagePolicy` in the one-harness project owns tool re-enablement after policy approval. This task owns the investigation that could justify that approval. Earlier delegation proposals are not accepted policy.

## Evidence from the review

[Observed] `SpawnTask` starts an independent session and returns its ID immediately, not its final report. It does not inherit the parent conversation. See [spawnSession.ts:8](../../../dev/one-harness/extension/src/tools/spawnSession.ts:8).

[Observed] The retained editor `runSubagent` implementation invokes the child with an empty history and returns its final text. These are source-code observations, not a live execution test. See [runSubagentTool.ts:358](../../../dev/vscode-src/src/vs/workbench/contrib/chat/common/tools/builtinTools/runSubagentTool.ts:358).

[Observed] The harness's plain-model loop awaits tool calls sequentially. Therefore, restoring a synchronous reporting tool alone does not establish parallel execution on that route. See [participant.ts:167](../../../dev/one-harness/extension/src/chat/participant.ts:167).

[Documented] Claude distinguishes fresh subagents from forks. Fresh subagents receive the task prompt without parent conversation history. Forks inherit the conversation. Both keep subsequent intermediate work in the child context and return a final message. See the [SDK inheritance contract](https://code.claude.com/docs/en/agent-sdk/subagents), read on 2026-10-09.

[Documented] OpenAI describes explicit subagent requests, result collection, and inherited sandbox controls. It states that subagent workflows consume more tokens than comparable single-agent runs. This describes Codex's own workflow, not the harness's implementation. See [Codex subagents](https://developers.openai.com/codex/subagents), read on 2026-10-09.

[Documented] Anthropic reports benefits for research with independent branches. It identifies shared context and dependencies between agents as limitations. Its reported research results do not measure this developer's coding workload. See [the multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), read on 2026-10-09.

No live execution of the disabled reporting tool or comparison on the developer's workload was performed. Time, quota, and correctness benefits remain unverified.

## Options to assess only after the trigger

[Inferred] The documented independent-branch results above justify investigating bounded investigations or reviews, not spawning a separate agent for every specialist responsibility.

[Inferred] The observed difference between `SpawnTask` and `runSubagent` above supports a reporting tool if coordinated delegation becomes necessary. The deferred contract would need explicit scope, completion evidence, failure and partial-result status, cancellation, remaining budget, and enforced tool permissions.

[Inferred] The documented fresh-versus-fork distinction above supports comparing two context policies. A briefed child receives shared instructions and selected task evidence. A fork receives the parent conversation. Neither policy has an established benefit for this workload.

## Step 1: Establish whether delegation addresses the failure

- [ ] #1 Record a no-subagent failure, its reproduction, required outcome, and why the existing workflow did not satisfy it.
- [ ] #2 Obtain the developer's decision to resume this investigation.
- [ ] #3 Identify a bounded delegated assignment that could address the evidenced cause, including its context and return requirements.
- [ ] #4 Compare the single-session baseline with the relevant briefed-child or forked-child option on the same task and acceptance criteria. Record correctness, elapsed time, token usage including cached usage where available, and correction work.
- [ ] #5 State the evidence limits and obtain approval or rejection of the proposed policy. Do not generalize beyond the tested workload.

## Step 2: Apply an approved escalation

- [ ] #1 Update the canonical workflow in Leader only if the developer approves a policy change.
- [ ] #2 Resume the harness task SubagentUsagePolicy for any approved tool work, without duplicating its implementation steps here.
- [ ] #3 Verify rule routing and required harness results before reporting delegation as available.
