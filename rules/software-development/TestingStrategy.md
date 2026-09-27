# Select Valuable Tests

Do not create a permanent automated test merely because production code changed. Add or update one when it has unique detection value and manual verification is expensive, unreliable, or unable to cover the relevant state spaces.

Avoid tests for trivial getters, setters, constructors, passthroughs, and implementation details.

Test behaviour, not implementation.

## Representative Non-Test

Do not add a permanent test that sets a developer-only overlay's debug flag to `false` and only asserts that the overlay is hidden. This covers one trivial Boolean branch, is cheap to verify manually. Add automation only when the gate has meaningful lifecycle or state combinations, is shared by multiple tools, has regressed before, or can exercise the actual release artifact.

When a test verifies a production timing, threshold, or limit, reference the owning production constant. Keep test-only tolerances and timing margins explicitly named. A test must still pass when a production parameter changes for game balance.

## Tests Own Their Inputs

When to apply: whenever you create or modify a test that reads a file, folder, setting, or other input that exists for another purpose, such as developer config, skills, rules, save files, or editor settings.

The test must use a test-owned fixture instead of live project state. Put the fixture inside the test repository and point the code under test at it. A test may read live state only when verifying that live state itself, and the test name must explicitly identify that purpose.

For example, a Godot test for key rebinding must read a fixture such as `test/fixtures/settings.cfg`, not the developer's `user://settings.cfg`. If the developer changes their key bindings while playing, the test must remain unchanged.

For example, a test for an agent harness that verifies skill loading must load a test-owned skill fixture rather than a skill from the developer's skills folder. If the test is specifically intended to verify the developer's real skill configuration, it may read that live skill, and its name must state that it is a live-configuration check.

Why: a test should fail because the behavior under test changed, not because unrelated live state changed.

## Execute Tests by Default

Agents own automated test execution by default. Run the relevant fixture first and expand only when risk or focused failures justify it.

Leave physical-device checks, performance measurement, usability review, and release approval to the developer unless explicitly delegated.

A result is evidence only when the intended fixture was discovered and a nonzero test count executed. A skipped or silently excluded test script is a failure of evidence, even if the runner exits successfully.

A script that tests or reproduces a behavior prints every error it catches and exits non-zero when anything fails. Its cleanup MUST NOT call `exit(0)` or swallow the exception: a `finally { process.exit(0) }` turns a crash into a silent pass. Exit code 0 with missing output is a failure of evidence, not a pass.

## Agent Tests Logic, Developer Judges Visuals

The agent MUST test every behavior that produces text it can read: return values, logs, files, process state, and messages between processes. When the product has a GUI, drive the layer under the GUI instead of asking the developer to click: call the handler, send the request, or run the code the button runs.

The agent MAY hand the developer only checks that need sight or taste: layout, readability, and whether a game looks or feels good. Whether an element is on screen is not one of them: [Query the GUI Before Asking the Developer to Look](#query-the-gui-before-asking-the-developer-to-look) owns that case.

Before asking for a manual test, state what the agent already verified as text. Ask the developer only for the visual part that is left.

For example, in a VSCodium chat extension that runs Claude through the Agent SDK, the check is "Claude answers, and the Read tool runs":

- Agent: a Node script calls the SDK's `query` with the same options as the extension and a stand-in `Read` tool. The script prints the tool name Claude called, the input the handler received, and the answer text.
- Developer: opens the chat panel and confirms that the answer and the "Ran Read" entry are shown.

For example, "Stop ends the `claude` process": the agent starts a query from a script, aborts it, and runs `pgrep` itself. Asking the developer to press Stop and run `pgrep` wastes a round trip on a check with no visual part.

**Why**: the agent works through text and cannot see the screen. The developer sees the GUI directly and judges it better than an agent does.

## Query the GUI Before Asking the Developer to Look

When to apply: a check concerns what a running GUI shows, and you are about to ask the developer to look at the screen.

A GUI framework exposes its widget tree to a debugger, and a widget tree is text. Find that channel and query it first. A screenshot says which of several states you are in; a query names the element, its class list, its computed style and its contents, which is what the fix needs.

Spend at most 10 minutes finding the channel. When none exists, name the channels you tried, then hand the check over.

| Runtime | Channel |
|---|---|
| Electron, VS Code, VSCodium | Launch with `--remote-debugging-port=<port>`, then the Chrome DevTools Protocol at `http://127.0.0.1:<port>/json/list`. `Runtime.evaluate` reads the DOM, `Input.dispatchKeyEvent` and `Input.dispatchMouseEvent` drive it. |
| A web page | The same protocol, or the session's browser tools. |
| Godot | The remote scene tree in the editor debugger, and `print` from `_process` into the log the agent reads. |
| Unity | The editor API through the `unityMCP` skill. |

Presence in the tree is not proof that the developer sees it. Read the computed style and the box: a node can carry text while its computed `display` is `none` and its box is 0 by 0. Report what is drawn, not what exists.

When two states differ only in what is drawn, change one input and query again. The pair is the evidence; a single reading of a broken state names no cause.

Hand over only what needs sight or taste: whether a layout reads well, whether a game feels good, whether a colour is right.

Why: the agent cannot see a screen, so it treated every visual question as the developer's. Most of them are not visual; they are queries against a tree the agent can read directly, and each hand-over costs a round trip and arrives as a picture the agent cannot act on.

## Verification Selection

| Defect or change | First verification method |
|---|---|
| Deterministic rule, calculation, serialization, or data error | Focused unit or integration regression when it has unique value; otherwise the smallest static or manual check |
| Lifecycle, scene/view flow, coroutine, event, physics, or input error | Runtime integration test reproducing the real hierarchy and required frames, or a focused manual scenario |
| Configuration, dependency, prefab, scene, or resource wiring | Inspect persisted configuration and runtime wiring; add a wiring test only for stable recurring contracts |
| Visual clarity, animation, audio, usability, balance, or comprehension | Focused manual review; automate only an underlying deterministic rule |
| Performance, memory, interruption, or device-specific behavior | Measure the affected scenario in the relevant environment or device |

Test the entry route named in the report. Do not bypass the defective route with a helper or alternate setup.
