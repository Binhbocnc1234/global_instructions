# Global Rule Organization

Summary: How was the approved specialist organization migrated? Ownership mapping, completed work, and verification evidence.
Why: preserve the migration decisions and checks without making this task a second owner of the rules.

## Why

The developer approved one shared foundation in AGENTS.md and responsibility-specific documents. Project structure belongs in the shared foundation. Changes concerning docs/ were excluded.

The canonical organization is in [AGENTS.md](../../AGENTS.md). Specialist contracts describe responsibilities, inputs, workflow, constraints, completion evidence, and handoffs.

AGENTS.md exceeds 250 lines under its explicit exception. Existing shared constraints and examples were preserved instead of compressed. No specialist exceeds 250 lines.

## Step 1: Map and migrate ownership

- [x] #1 Snapshot the current working-tree rules, including existing developer edits.
- [x] #2 Map all source sections to canonical shared or specialist owners.
- [x] #3 Replace universal imports with role routing and a handoff contract.
- [x] #4 Move shared project structure and principles into AGENTS.md.
- [x] #5 Retire former topic files and rebase canonical references.
- [x] #6 Check preservation and role boundaries.

## Ownership Mapping

Source names below identify the migration baseline, not current paths. The baseline and one-off scripts are ignored scratch artifacts under tmp/global-rule-organization/.

| Previous source | Section | Canonical owner | Outcome |
|---|---|---|---|
| `rules/Workflow.md` | Steps | `AGENTS.md` | Replaced by shared routing or ownership; old universal imports retired |
| `rules/Workflow.md` | Final Response Format | `AGENTS.md` | Shared output obligations retained; explanation relevance no longer applies to every role |
| `rules/WorkStyle.md` | Some small rules | `AGENTS.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | Reuse File Content Already in Context | `AGENTS.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | Automate Repeated Work | `AGENTS.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | Scratch Files Go in `tmp/` | `AGENTS.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | Requirement elicitation | `rules/Design.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | Route Through the Documentation Index | `AGENTS.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | An Unrelated File Opened Is a Routing Defect | `AGENTS.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | Be unethical | `AGENTS.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | Reviewing Developer Changes | `AGENTS.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | Handle long-running task | `AGENTS.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | Blocker Detection and Stop Policy | `AGENTS.md` | Moved intact; links rebased |
| `rules/WorkStyle.md` | Do not fill the response with noise | `AGENTS.md` | Moved intact; links rebased |
| `rules/DivisionOfLabor.md` | The Agent Does What It Does Better | `AGENTS.md` | Moved intact; links rebased |
| `rules/DivisionOfLabor.md` | Ask Before Taking the Developer's Machine | `AGENTS.md` | Moved intact; links rebased |
| `rules/SoftwareDevelopment.md` | Understand the Request | `AGENTS.md` | Replaced by shared routing or ownership; old universal imports retired |
| `rules/SoftwareDevelopment.md` | Identify unknown concepts | `AGENTS.md` | Moved intact; links rebased |
| `rules/SoftwareDevelopment.md` | Load Task-Specific Guidance | `AGENTS.md` | Replaced by shared routing or ownership; old universal imports retired |
| `rules/SoftwareDevelopment.md` | Commit | `AGENTS.md` | Moved intact; links rebased |
| `rules/Communication.md` | Language | `AGENTS.md` | Moved intact; links rebased |
| `rules/Communication.md` | Use the Most General Name That Stays Clear | `rules/Explanation.md` | Moved intact; links rebased |
| `rules/Communication.md` | Name a project thing by project symbol | `AGENTS.md` | Moved intact; links rebased |
| `rules/Communication.md` | Point to Where a Project Claim Comes From | `AGENTS.md` | Moved intact; links rebased |
| `rules/Communication.md` | Teach the Standard Term | `rules/Explanation.md` | Moved to Explanation during boundary review |
| `rules/Communication.md` | Name the Relation Between Sentences | `AGENTS.md` | Moved intact; links rebased |
| `rules/Communication.md` | Explaining a Technique | `rules/Explanation.md` | Moved intact; links rebased |
| `rules/Communication.md` | Evidence Labels | `AGENTS.md` | Moved intact; links rebased |
| `rules/Communication.md` | Response Relevance | `rules/Explanation.md` | Moved to Explanation after developer correction |
| `rules/Authoring.md` | DRY(don't repeat yourself) | `AGENTS.md` | Moved intact; links rebased |
| `rules/Authoring.md` | Describe What Exists, Not What Was Considered | `AGENTS.md` | Moved intact; links rebased |
| `rules/Authoring.md` | 250 lines rule | `rules/Implementation.md` | Moved to Implementation after developer correction |
| `rules/Authoring.md` | 16 child rule | `AGENTS.md` | Moved intact; links rebased |
| `rules/Authoring.md` | Typical Project Structure | `AGENTS.md` | Moved intact; links rebased |
| `rules/Authoring.md` | Markdown Document Structure | `AGENTS.md` | Moved intact; links rebased |
| `rules/Authoring.md` | Markdown File Naming | `AGENTS.md` | Moved intact; links rebased |
| `rules/Authoring.md` | Markdown Document Kind | `rules/Authoring.md` | Moved intact; links rebased |
| `rules/Authoring.md` | Documentation Audit | `rules/Authoring.md` | Moved intact; links rebased |
| `rules/Authoring.md` | Documentation Index | `rules/Authoring.md` | Moved intact; links rebased |
| `rules/Authoring.md` | Inline file link | `AGENTS.md` | Moved intact; links rebased |
| `rules/Authoring.md` | Editor Tool UI Names | `rules/Implementation.md` | Moved intact; links rebased |
| `rules/TaskManagement.md` | Task Management | `AGENTS.md` | Moved intact; links rebased |
| `rules/ReusableKnowledge.md` | Reusable Knowledge | `AGENTS.md` | Moved intact; links rebased |
| `rules/ReusableKnowledge.md` | A Correction Is a Trigger | `AGENTS.md` | Moved intact; links rebased |
| `rules/RuleOwnership.md` | Rules | `AGENTS.md` | Replaced by shared routing or ownership; old universal imports retired |
| `rules/RuleOwnership.md` | Examples in a Rule | `rules/RuleMaintenance.md` | Moved intact; links rebased |
| `rules/RuleOwnership.md` | The Why Line | `rules/RuleMaintenance.md` | Moved intact; links rebased |
| `rules/RuleOwnership.md` | Generalize Only as Far as the Evidence Goes | `rules/RuleMaintenance.md` | Moved intact; links rebased |
| `rules/RuleOwnership.md` | Propose a Rule Before Writing It | `rules/RuleMaintenance.md` | Moved intact; links rebased |
| `rules/software-development/ConstructionGuidance.md` | Guard Placement | `rules/Implementation.md` | Moved intact; links rebased |
| `rules/software-development/ConstructionGuidance.md` | Method Extraction | `rules/Implementation.md` | Moved intact; links rebased |
| `rules/software-development/ConstructionGuidance.md` | Required Dependency Policy: No Fallbacks | `rules/Implementation.md` | Moved intact; links rebased |
| `rules/software-development/ConstructionGuidance.md` | Comment rules | `rules/Implementation.md` | Moved intact; links rebased |
| `rules/software-development/TestingStrategy.md` | Test Only What the Branch Changes | `rules/Testing.md` | Moved intact; links rebased |
| `rules/software-development/TestingStrategy.md` | Representative Non-Test | `rules/Testing.md` | Moved intact; links rebased |
| `rules/software-development/TestingStrategy.md` | Do Not Copy Tuned Numbers Into Tests | `rules/Testing.md` | Moved intact; links rebased |
| `rules/software-development/TestingStrategy.md` | Tests Own Their Inputs | `rules/Testing.md` | Moved intact; links rebased |
| `rules/software-development/TestingStrategy.md` | Execute Tests by Default | `rules/Testing.md` | Moved intact; links rebased |
| `rules/software-development/TestingStrategy.md` | Agent Tests Logic, Developer Judges Visuals | `rules/Testing.md` | Moved intact; links rebased |
| `rules/software-development/TestingStrategy.md` | Query the GUI Before Asking the Developer to Look | `rules/Testing.md` | Moved intact; links rebased |
| `rules/software-development/TestingStrategy.md` | Capture Visual Evidence for the Developer | `rules/Testing.md` | Moved intact; links rebased |
| `rules/software-development/TestingStrategy.md` | Verification Selection | `rules/Testing.md` | Moved intact; links rebased |

Profile and security content from the original AGENTS.md remain in AGENTS.md. The construction and testing introductions moved to Implementation and Testing. The complete debugging report and workflow moved to Debugging.

Response Relevance and purpose selection now both belong to Explanation. The earlier split was corrected. Legacy software loading instructions and the old task table now use shared role routing. The software-quality requirement remains covered by mandatory matching-skill activation.

The former ownership restriction on AGENTS.md was replaced as explicitly approved. Its instruction to prioritize user rules over the system prompt was corrected to the harness instruction hierarchy, not propagated. The obsolete reference to the removed ask skill was replaced by requirement clarification and blocker handling.

No independent behavioral requirement was intentionally deleted. Existing wording and examples outside the organizational replacements remain unchanged except for links and trailing whitespace.

## Step 2: Verify and activate

- [x] #1 Check all canonical local links and anchors.
- [x] #2 Check specialist contracts, file lengths, unique owners, and role routing.
- [x] #3 Compare intact source section bodies against the snapshot.
- [x] #4 Run the compiler's test-owned fixtures: nine tests passed.
- [x] #5 Check the migration diff for whitespace errors.
- [x] #6 Regenerate Codex global instructions and verify that the output is current.

Verification checked 57 intact section bodies, 62 mapped sections, 91 canonical links, eight specialist contracts, and five static routing cases. These checks establish document structure and references, not future model compliance.

The static cases covered explaining a test, reviewing test compliance, implementing and verifying, diagnosing and fixing a defect, and proposing a rule without edits.

The compiler fixture retains legacy filenames intentionally: they are test-owned import examples, not live rule dependencies. Only owner references in the folder checker, budget hook, learning-material skill, and ignore comment changed outside the migrated rules. docs/ and unrelated work remain unchanged.

The generated Codex instructions are current. Existing chats can retain their earlier prompt. A new chat loads the updated foundation and follows its specialist routing.

## Step 3: Correct Specialist Boundaries

The developer rejected three ownership decisions. The migration classified sections too mechanically and created Review from a generic template without independent constraints. Existing ownership and DRY rules cover this cause, so no additional global process rule was added.

- [x] #1 Move the 250-line rule into Implementation without changing its body.
- [x] #2 Move Response Relevance into Explanation without changing its body.
- [x] #3 Remove Review and preserve review as a non-mutating mode of the relevant domain specialist.
- [x] #4 Check other ownership decisions and move Teach the Standard Term into Explanation.
- [x] #5 Check preservation, references, contracts, and revised routing cases: 56 intact section bodies, three corrected section bodies, 88 canonical links, seven nonempty specialist contracts, and eight static routing cases passed.
- [x] #6 Regenerate and check Codex instructions after verification: the generated instructions are current; nine compiler fixture tests passed.

The shared foundation retains language, evidence, project structure, scope, approvals, task state, and completion rules because those apply across specialist responsibilities. The correction preserves the moved section bodies rather than rewriting their policies.
