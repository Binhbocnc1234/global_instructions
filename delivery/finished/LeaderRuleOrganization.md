# Leader Rule Organization

Summary: How does the specialist organization gain request coordination? Approved ownership changes, migration progress, and verification evidence.
Why: the previous migration treated rules used across tasks as rules that every specialist must load.

## Why

The developer approved a Leader that coordinates an outcome-based request. Design approval is the only routine human checkpoint. Blockers, credentials, machine control, and other explicit permission requirements remain exceptional stops. Explanation runs only when the developer requests explanation.

The correction concerns responsibility boundaries, not text compression. The approved owners will be [Leader](../../rules/Leader.md), [Implementation](../../rules/Implementation.md), and [Design](../../rules/Design.md). Shared principles and the standard project structure remain in [AGENTS.md](../../AGENTS.md).

The developer removed the prohibition on work not explicitly mentioned in a request. Preserve that deletion. Required supporting work serves the requested outcome. Discovered risks must be reported under the existing evidence and consequence criteria.

## Step 1: Migrate ownership

- [x] #1 Snapshot the current worktree and preserve unrelated edits.
- [x] #2 Move request routing, handoffs, task management, commits, and final reporting into Leader.
- [x] #3 Move the 16-child rule and repeated-work automation into Implementation.
- [x] #4 Move unknown-concept resolution into Design and distinguish new concepts from missing existing contracts.
- [x] #5 Connect specialist outputs to Leader and update canonical references.
- [x] #6 Check section preservation, links, role boundaries, and representative request routes.
- [x] #7 Run compiler fixtures and regenerate installed Codex instructions.
- [x] #8 Include the approved prerequisite rule migration in the scoped commit.

## Verification

[Observed] The shared foundation changed from 878 to 668 lines. Leader contains 227 lines. All eight specialist documents remain below 250 lines.

[Observed] Static checks confirmed eight moved sections with unique owners, 103 resolved Markdown references, and three unchanged illustrative references. Five moved section bodies remain intact apart from rebased links. Shared section bodies remain intact except the approved ownership and supporting-work changes.

[Observed] Ten routing-clause checks passed. They cover outcome-based requests, Design approval, existing approvals, automatic transitions, failed verification, requested explanation, non-mutating reviews, changed scope, exceptional stops, and specialist boundaries.

[Observed] Nine compiler fixture tests and four folder-checker fixture tests passed. The scoped folder checks and diff whitespace check passed. Codex instructions were regenerated and the compiler check confirmed the output is current.

## Commit Scope

The developer approved committing all pending changes. The rule migration includes its prerequisite specialist files, retired owners, updated references, and task records. Independent skill imports, archive moves, and developer notes use separate commits.

[Observed] Before committing, the nine compiler tests, four folder-checker tests, migration checks, and generated-instruction check passed again. A secret-pattern scan found no candidate matches in the 249 pending files. The scan checks defined patterns, not every possible credential format.

## Correction Record

The prior organization confused shared use with shared ownership. [Rule Ownership](../../AGENTS.md#rule-ownership) now distinguishes specialist outputs from internal workflows. [Leader](../../rules/Leader.md) owns coordination instead of making each specialist load it.

## Evidence Limits

Static document checks cannot prove that a future model follows these rules. Runtime evidence applies only to the tools that execute during verification.
