# Testing Workflow

Summary: Rules for automated test execution, change-based selection, the 20-second mean budget for development verification, and whether regression coverage justifies its run time.

These rules belong to [Testing](Testing.md).

## Execute Tests by Default

Agents own automated test execution by default. Use [Automate Project-Lifetime Tests](#automate-project-lifetime-tests) for tests maintained for the project. For session-only tests, run the relevant fixture first and expand only when risk or focused failures justify it.

Leave physical-device checks, performance measurement, usability review, and release approval to the developer unless explicitly delegated.

A result is evidence only when the intended fixture was discovered and a nonzero test count executed. A skipped or silently excluded test script is a failure of evidence, even if the runner exits successfully.

A script that tests or reproduces a behavior prints every error it catches and exits non-zero when anything fails. Its cleanup MUST NOT call `exit(0)` or swallow the exception: a `finally { process.exit(0) }` turns a crash into a silent pass. Exit code 0 with missing output is a failure of evidence, not a pass.

## Automate Project-Lifetime Tests

When to apply: adding or maintaining automated tests intended to remain useful beyond the current session.

Maintained tests MUST have a documented automated entry point. Adding a maintained test MUST NOT automatically add its execution to every commit.

A project-owned selection command MUST select checks from the changed files using project-owned test-selection configuration. Selection MUST include directly changed tests and tests for workflows that depend directly or indirectly on changed components. Explicitly classified non-executable changes MAY select only the applicable non-executable checks. An unmapped change MUST select the full relevant suite.

The pre-commit hook MUST NOT run tests; it runs only the staged-file checks. The agent runs the selection command once, after the last commit of the request, against the last commit, and runs exactly the checks it selects. The agent MUST NOT add, skip, or replace a selected check by its own judgement. It MAY run another check only to diagnose a failure.

For example, a request implements two features in two commits. The selection command runs once after the second commit, and its selection covers the files both commits changed.

Why: a hook runs the selected tests at every commit, so a request with two commits pays for two runs, and in one project a single run took 144 s. A command still selects from the changed files, so selection does not depend on the agent's judgement.

A workflow depends on a component when the workflow executes the component’s code or reads a value the component defines. A module the workflow loads but never calls or reads is not a dependency. Establish what a workflow executes from evidence, such as a coverage run, before mapping it.

For example, an editor workflow loads a Codex configuration module because the extension’s entry file imports it, but Codex is turned off in that workflow, so none of the module’s functions run. Selecting the workflow for a change to that module costs 30 s and checks nothing the change did.

By contrast, a Python test that imports a settings module and reads TIMEOUT_SECONDS on the path it runs depends on that module.
Changes to the test-selection configuration, shared test runner, or dependency configuration MUST select the full relevant suite unless the project defines and verifies a narrower dependency boundary.

The selector MUST print the selected checks and the reason for each selection, deduplicate checks, and execute them against the same candidate snapshot used for selection.

Workflows not selected for every commit MUST remain available through the project's test entry point. The project MUST state when those workflows are required, such as before merging or releasing.

Verification MUST test the committed files. When uncommitted changes could affect the result, run verification in an isolated checkout of the last commit. MUST NOT treat a passing test against different working-folder content as evidence that the commit passes.

A failed selected check MUST be fixed in a new commit, followed by another run of the selection command, before the final reply. When a blocker prevents the fix, the reply names the failing check. Each selected check MUST run for the same snapshot. MUST NOT repeat a passing check when its checked content, dependencies, configuration, and selection remain unchanged. Failed checks MAY be rerun to diagnose the failure; a later pass MUST NOT silently erase an earlier failure.

Tests that are only valid for the current session MUST remain in the git-ignored `tmp/` folder. MUST NOT add them to the project's permanent test workflow.

For example, a documentation-only commit runs the applicable staged-file checks without launching an editor when no executable behavior or test configuration changes.

By contrast, a change to shared session storage runs the workflows that depend on that storage. A passing run that included an unstaged storage fix does not verify a commit that omits the fix.

Why: verification must cover the committed behavior without repeating unrelated workflows or allowing uncommitted changes to hide a broken commit.

## Keep a Test Only When Its Regression Value Exceeds Its Run Time

When to apply: adding a test to the project's permanent tests, selecting a verification workflow, or reviewing verification time.

Treat development feedback time as a quality criterion alongside regression detection. Target an average end-to-end wall time of at most 20 seconds for each development verification run (lightweight verification). Measure from starting the verification entry point through selection, setup, process startup, execution and cleanup; parallel tests contribute elapsed wall time, not the sum of their durations. Report the sample count and environment with a measured mean; one run establishes only that run's duration. A project MAY set different budgets through an explicit project override with its reason.

First remove avoidable work, reuse supporting processes where test isolation permits, and select checks by affected workflow under [Automate Project-Lifetime Tests](#automate-project-lifetime-tests). When retaining every check would exceed the budget, development speed MAY take priority over additional regression coverage: remove checks whose regression value does not justify their cost, or move them to a documented event such as merge, release or dependency upgrade. Record the omitted coverage and the failure that could then go undetected; MUST NOT silently skip a selected check or describe unverified behavior as passing. Report an unresolved overrun with measured times rather than weakening assertions or test isolation merely to meet the clock.

For example, reuse one loaded test process across 40 cases while giving each case fresh storage; there is no reason to reload the same libraries 40 times unless a case verifies startup. By contrast, a test of crash recovery must exercise the crash and restart, so keeping its process alive would remove the behavior under test.

A permanent test costs its run time on every commit that selects it, for the life of the project. It pays back only when a later change breaks the behavior it checks. Verify a new behavior in `tmp/` first. Promote the test to the permanent tests only when at least one of these holds:

- Code that other tasks change often runs the behavior, so an unrelated change can break it.
- The behavior has regressed before.
- A break would stay unnoticed in daily use, or would damage data, such as a lost chat or a file written by the wrong owner.

Assume a later agent edits only the code its task names. A test of behavior that only that code runs, and whose break the developer sees on first use, stays in `tmp/`.

A permanent test whose behavior breaks only at a known event, such as an editor upgrade, runs at that event and not on every commit, under [Automate Project-Lifetime Tests](#automate-project-lifetime-tests).

For example, a new label shows the session id in the chat header. The agent checks it once through the editor, from a script in `tmp/`. Only the label's own code shows it, and a missing label is visible at once, so the script stays in `tmp/`.

For example, a change to how turn logs are written gets a permanent test, because every chat writes through that code, and a bad write loses history without any visible error.

For example, a test to check if prompt caching work properly, it should be pernament test, because the bad situation fail silently

Why: every permanent test was kept because it verified something once, so the suite only grew. In one project a typical commit ran 9 editor workflows and took 50–90 s, and the project is the developer's working tool, so a slow fix delays their main work.
