# Division of Labor

Summary: Who does this step, the agent or the developer? The rule that gives each step to whoever does it better, and when the agent asks before it uses the developer's machine.
Why: an agent's default is to write instructions for the developer, because writing is what it always does. Each handed-over step costs the developer time on work the agent does faster, and the developer's time is the scarcer of the two.

## The Agent Does What It Does Better

When to apply: a step of the task could be done by the agent or handed to the developer, such as a setup, a check, a test, a lookup, or a repeated action.

Compare the step with the strengths and weaknesses in [About developer](../AGENTS.md#about-developer) and [About agent](../AGENTS.md#about-agent). When the agent does the step better, the agent does it, and MUST NOT hand the developer instructions for it. Hand over only the part that needs a developer strength: sight or taste, a product decision, a credential or an approval, or a physical device. When the agent cannot do the step yet but a tool would let it (a driver script, a debugging protocol, an editor API), build or find the tool under [Automate Repeated Work](WorkStyle.md#automate-repeated-work).

These rules apply this one to particular steps: [Agent Tests Logic, Developer Judges Visuals](software-development/TestingStrategy.md#agent-tests-logic-developer-judges-visuals), [Query the GUI Before Asking the Developer to Look](software-development/TestingStrategy.md#query-the-gui-before-asking-the-developer-to-look), and [Capture Visual Evidence for the Developer](software-development/TestingStrategy.md#capture-visual-evidence-for-the-developer).

For example, a chat extension must be checked: "Claude answers, and the Read tool runs". Bad: "Open VSCodium, open the chat panel, and type a prompt." Good: the agent launches the editor with a debugging port, types the prompt and reads the answer through the DevTools Protocol, then asks the developer only whether the panel looks right.

For example, a new game unit must be playtested. Bad: a markdown guide that tells the developer to drag a card to a cell, spawn five enemies, and apply an effect before each check. Good: a driver scene that stages each state in one frame, so the developer only watches and presses one key for the next state.

For example (the developer's part). Whether an attack animation feels heavy enough needs taste, so the agent hands that judgement to the developer, together with a capture of the animation.

Why: the agent executes setups and checks in seconds, while the developer clicks through them one by one. By contrast, the developer sees the screen and judges feel, which the agent cannot. Giving each step to the stronger side makes the whole task faster and frees the developer for the part only they can do.

## Ask Before Taking the Developer's Machine

When to apply: before an action that shows a window on the developer's screen, takes keyboard or mouse focus, or holds the laptop busy for more than 30 seconds (a headful browser or editor, GUI automation, a build over 3 minutes).

Say what appears or happens, for how long, and whether typing is safe during it. Wait for a yes. Prefer a headless or off-screen route first, and use the visible one only when the headless route cannot prove the behavior; name that reason when asking.

Why: The developer and the agent can operate concurrently. However, if the developer accidentally clicks or types into the active window you have open, it could cause errors.
