# Rule Ownership

Summary: Where does a rule go? Which file owns a rule, and what a rule looks like.
Why: a rule in the wrong file is either never loaded when it is needed, or always loaded when it is not.

## Rules

- **Rule**: text stored in a file that applies across requests. Reader: agent. Including Global AGENTS.md, project-scoped AGENTS.md, skills, and project documentation hold rules. Think of rules as law of a country, everyone(developer and agent) must adhere to rules. Rules is not automatically optimal, or an immutable command. So if you think the rules is obsolete, propose a rule change instead of adhering rigidly. For example, If you believe the "250-line rule" cannot be applied to `AIManager.cs` because there is no way to split the file into smaller, meaningful topics, please inform the developer and recommend a rule change.

Rule owners:

- Global rules (`~/.agents/AGENTS.md` and the files it imports from `~/.agents/rules/`): a rule that applies across projects and meets one of two conditions. `AGENTS.md` holds the import list, the developer profile and the security rules; every other global rule lives in one topic file under `rules/`, named for the question it answers. Put a new rule in the topic file that already answers its question.
  + More than half of all tasks need it. Example: "Communicate with the developer in English" or rule about how to explain a concept to developer
  + Half or fewer of all requests need it, and it is 30 lines or shorter. Example: `Editor Tool UI Names`. A skill costs a description that is always loaded plus a trigger that can fail, which is not worth it for a rule this short.
  + A cross-project rule that half or fewer of all requests need, and that is longer than 30 lines, belongs in a skill.
- Skill (~/.agents/skills) : workflow, tool-integration or anything that you think will be used across multiple projects. For example, the `software-quality` skill is used by any project that commits to a non-functional target. Another example: a MCP skill connect to Gmail, Github or UnityEditor. Active the skill if the task matches its description(condition). Treat skill activition is mandatory, rather than activating it only when you feel the need.
- Project-scoped AGENTS.md: contain rules that should appear almost every requests from a project. You also can use project-scoped `AGENTS.md` as a temporary owner for rules whose canonical owner is not yet clear. Move the rule to canonical documentation or automation once its owner becomes clear.
  + Every project-scoped AGENTS.md MUST have a `## Project brief` section near the top. It states what the project does and who uses it..., in a few sentences.
