# Select Valuable Tests

Do not create a permanent automated test merely because production code changed. Add or update one when it has unique detection value and manual verification is expensive, unreliable, or unable to cover the relevant state spaces.

Avoid tests for trivial getters, setters, constructors, passthroughs, and implementation details.

Test behaviour, not implementation.

## Representative Non-Test

Do not add a permanent test that sets a developer-only overlay's debug flag to `false` and only asserts that the overlay is hidden. This covers one trivial Boolean branch, is cheap to verify manually. Add automation only when the gate has meaningful lifecycle or state combinations, is shared by multiple tools, has regressed before, or can exercise the actual release artifact.

When a test verifies a production timing, threshold, or limit, reference the owning production constant. Keep test-only tolerances and timing margins explicitly named. A test must still pass when a production parameter changes for game balance.

## Execute Tests by Default

Agents own automated test execution by default. Run the relevant fixture first and expand only when risk or focused failures justify it.

Leave physical-device checks, performance measurement, usability review, and release approval to the developer unless explicitly delegated.

A result is evidence only when the intended fixture was discovered and a nonzero test count executed. A skipped or silently excluded test script is a failure of evidence, even if the runner exits successfully.

## Agent Tests Logic, Developer Judges Visuals

The agent MUST test every behavior that produces text it can read: return values, logs, files, process state, and messages between processes. When the product has a GUI, drive the layer under the GUI instead of asking the developer to click: call the handler, send the request, or run the code the button runs.

The agent MAY hand the developer only checks that need sight or taste: layout, readability, whether a game looks or feels good, and whether an element appears on screen when no log or file records it.

Before asking for a manual test, state what the agent already verified as text. Ask the developer only for the visual part that is left.

For example, in a VSCodium chat extension that runs Claude through the Agent SDK, the check is "Claude answers, and the Read tool runs":

- Agent: a Node script calls the SDK's `query` with the same options as the extension and a stand-in `Read` tool. The script prints the tool name Claude called, the input the handler received, and the answer text.
- Developer: opens the chat panel and confirms that the answer and the "Ran Read" entry are shown.

For example, "Stop ends the `claude` process": the agent starts a query from a script, aborts it, and runs `pgrep` itself. Asking the developer to press Stop and run `pgrep` wastes a round trip on a check with no visual part.

**Why**: the agent works through text and cannot see the screen. The developer sees the GUI directly and judges it better than an agent does.

## Verification Selection

| Defect or change | First verification method |
|---|---|
| Deterministic rule, calculation, serialization, or data error | Focused unit or integration regression when it has unique value; otherwise the smallest static or manual check |
| Lifecycle, scene/view flow, coroutine, event, physics, or input error | Runtime integration test reproducing the real hierarchy and required frames, or a focused manual scenario |
| Configuration, dependency, prefab, scene, or resource wiring | Inspect persisted configuration and runtime wiring; add a wiring test only for stable recurring contracts |
| Visual clarity, animation, audio, usability, balance, or comprehension | Focused manual review; automate only an underlying deterministic rule |
| Performance, memory, interruption, or device-specific behavior | Measure the affected scenario in the relevant environment or device |

Test the entry route named in the report. Do not bypass the defective route with a helper or alternate setup.
