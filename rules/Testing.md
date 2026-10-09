# Testing

Summary: What does the Testing specialist do? Its responsibility, inputs, workflow, constraints, completion evidence, and responsibility transitions.
Why: one role owns this responsibility without copying shared principles.

Use the shared foundation in [AGENTS.md](../AGENTS.md).

## Responsibility

Select, construct, execute, and assess verification.

## Inputs Required

The changed behavior, actual entry route, candidate fixtures, environment, and relevant contracts.

## Workflow

Select verification with detection value. Use owned inputs. Execute the intended fixture. Assess evidence and state what remains unverified.

## Role-Specific Constraints

## Select Valuable Tests

Do not create a permanent automated test merely because production code changed. Add or update one when it has unique detection value and manual verification is expensive, unreliable, or unable to cover the relevant state spaces.

Avoid tests for trivial getters, setters, constructors, passthroughs, and implementation details.

Test behaviour, not implementation.

## Test Only What the Branch Changes

When to apply: writing a test, and dropping or reverting a change that has tests.

A test stays only when it covers behaviour this branch changes. When a change is dropped or reverted, its tests go with it. A rule owned by another component, such as a shared system another developer maintains, is asserted by that component's tests, not again by a test of the code that relies on it. A test may still trigger that rule as a setup step, as long as it asserts only the branch's own behaviour.

For example, a branch changes how one game piece removes its own buff at a phase change. Its tests assert that removal. They do not assert that the effect system rejects a duplicate trait or promotes the next instance, because the effect system owns those rules and its tests cover them.

For example, a change to a passive is reverted after a policy merge makes it unnecessary, and the agent keeps the passive's regression tests as a separate commit. The commit adds tests for code the branch no longer changes, so it is dropped with the change.

Why: a leftover test from a dropped change pins behaviour nobody on the branch changed, and a test that re-asserts another component's rule fails when that owner changes the rule on purpose. Both cost review time and history without guarding anything the branch did.

## Representative Non-Test

Do not add a permanent test that sets a developer-only overlay's debug flag to `false` and only asserts that the overlay is hidden. This covers one trivial Boolean branch, is cheap to verify manually. Add automation only when the gate has meaningful lifecycle or state combinations, is shared by multiple tools, has regressed before, or can exercise the actual release artifact.

## Do Not Copy Tuned Numbers Into Tests

When to apply: a test asserts or uses a number that someone tunes for balance, feel, or performance, such as a unit's health, a price, a cooldown, an effect's strength or duration, a spawn interval, a timeout, or a retry count.

A tuned number has one owner: a named constant in production code, or an authored data file such as a Godot `.tres`, a Unity ScriptableObject, or a JSON config. It changes on every tuning pass. By contrast, the behaviour built on it stays the same: the unit attacks, the effect ends, the spawns keep their order. So a test pins the behaviour.

- Assert behaviour: who survives, whether a target is hit, that an effect expires, that a retry loop stops.
- When an assertion needs a tuned number, read it from its owner: write `assert_eq(armor, ARMOR_BONUS)`, not `assert_eq(armor, 40.0)`. Derive a value that depends on tuned numbers in the test, from the same owners: write `start_x + config.move_speed * seconds`, not a `3.0` worked out by hand.
- When the owner is a literal inside production code, such as `damage *= 2.0`, extract a named constant first, because a test cannot reference a literal.
- MUST NOT assert that an authored data file holds a particular value, such as `assert_eq(archer.max_health, 120.0)`. The file already is that value, so the test only repeats it.
- MUST NOT rely on a tuned value being zero or absent without reading it. For example, a test adds 40 armor and asserts `armor == 40`, which holds only while the unit's authored armor is 0. Read the starting value first, or use a fixture the test builds.
- A test MAY write its own numbers for inputs it owns: a fixture config it builds, the damage it deals, the grid size it creates. Keep test-only tolerances and timing margins explicitly named.

Why: a test that copies a tuned number fails on a balance change while no behaviour broke. The reader learns to update the number without reading the failure, and then the test stops catching real regressions. In a game project, raising one unit's health from 120 to 200 failed a test that only repeated the data file.

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

Before asking for a manual test, state what the agent already verified as text. Ask the developer only for the visual part that is left, delivered as a capture under [Capture Visual Evidence for the Developer](#capture-visual-evidence-for-the-developer) when the project has a route.

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

## Capture Visual Evidence for the Developer

When to apply: a change has a visual part that the developer would otherwise check by launching the product and reaching the state by hand, such as a new character, an animation, an effect, a layout, or a UI flow.

Test the logic as text first, under [Agent Tests Logic, Developer Judges Visuals](#agent-tests-logic-developer-judges-visuals). Then capture the visual part and link it in the response as a Markdown link to its path relative to the project root, such as `[clip.mp4](tmp/video/out/clip.mp4)`, so the developer opens it with one click without launching the product. MUST NOT send it with the harness's file-sending tool: a link sits next to the caption that says where to look, and it opens in the developer's own player. The capture replaces the developer's manual session, not the logic test. Whether an element is drawn at all is a query under [Query the GUI Before Asking the Developer to Look](#query-the-gui-before-asking-the-developer-to-look), not a capture.

- **Image or video.** An image shows a state: a layout, a colour, a label. A video shows change over time: an animation, a transition, a sequence of steps. Send an image when nothing in the check moves.
- **Drive it through the production path.** A driver (a script, a scene, a test entry point) reaches each state through the code path the product uses. It also stages states that are slow or impossible to reach by hand, such as a skill with a long cooldown or a failed network call.
- **Off the developer's screen.** Render into a virtual display or an off-screen renderer. A headless mode that draws no frames captures nothing, so prove the renderer draws before relying on it. When no off-screen route exists, [Ask Before Taking the Developer's Machine](Execution.md#ask-before-taking-the-developers-machine) applies.
- **Own state only.** The driver runs on its own profile, save file, and settings, under [Tests Own Their Inputs](#tests-own-their-inputs), because the product may write on exit and overwrite the developer's data. Its outputs go under [Scratch Files Go in `tmp/`](Execution.md#scratch-files-go-in-tmp).
- **Mark each behavior.** The driver prints one line per behavior it shows, with its time in the video. Build the caption from those lines, so the developer knows where to look.
- **Short.** One video is at most 30 seconds. Split a longer showcase into one video per behavior group.
- **Check before linking.** The file has the expected size and duration, it is a format any player opens (PNG, H.264 MP4), and a frame taken at one marked time is not blank. A broken capture costs the round trip it was meant to save.

The project owns the route, reached from its `AGENTS.md`: the capture mode, the virtual display, the driver's entry point, and the encoder command. A project with a GUI and no route gets one proposed.

For example, a new game character: the driver spawns it beside an enemy, then shows its walk, an attack, its skill, a hit, and its death in one 15-second video.

For example, a new button in an editor's side panel: the driver opens the panel, and one screenshot of it answers whether the button looks right. A video adds nothing, because nothing moves.

Why: checking a visual by hand costs the developer a launch, a route through menus, and a staged state, and some states cannot be staged by hand at all. A capture costs seconds of looking, and the driver reaches every state the same way each time.

## Verification Selection

| Defect or change | First verification method |
|---|---|
| Deterministic rule, calculation, serialization, or data error | Focused unit or integration regression when it has unique value; otherwise the smallest static or manual check |
| Lifecycle, scene/view flow, coroutine, event, physics, or input error | Runtime integration test reproducing the real hierarchy and required frames, or a focused manual scenario |
| Configuration, dependency, prefab, scene, or resource wiring | Inspect persisted configuration and runtime wiring; add a wiring test only for stable recurring contracts |
| Visual clarity, animation, audio, usability, balance, or comprehension | A capture under [Capture Visual Evidence for the Developer](#capture-visual-evidence-for-the-developer) for what an image or video shows; focused manual review for feel and usability; automate only an underlying deterministic rule |
| Performance, memory, interruption, or device-specific behavior | Measure the affected scenario in the relevant environment or device |

Test the entry route named in the report. Do not bypass the defective route with a helper or alternate setup.

## Completion Evidence

Commands or fixtures, discovered test counts, outcomes, and explicit evidence limits.

## Responsibility Transitions

Return results and evidence limits to Leader. Identify production defects for Implementation and unknown causes for Debugging. Supply verified captures for developer-only visual judgments.
