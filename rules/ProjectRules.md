# Project Instructions

Summary: Requirements for project-scoped AGENTS.md.

## When to Apply

Apply when creating, reviewing, or changing a project-scoped AGENTS.md.

## Project-Scoped AGENTS.md

Project-scoped AGENTS.md MUST contain:

1. A Project brief section near the top stating the project's purpose and
   identifying what the project produces or maintains.
2. A Project Index section routing readers to the project resources needed
   for their requests.
3. Project-wide instructions and explicit exceptions to global rules.
   Each exception MUST use [Override] and state its reason.

MUST NOT copy global instructions into project-scoped AGENTS.md.
State project-specific requirements or link to their canonical owner.

Why: one writing contract lets an agent check project instructions without
collecting requirements from several specialist rule files.

## Project Index

The Project Index is the canonical starting point for finding project
resources. The Documentation Index is one part of this navigation.

The Project Index MUST identify, where applicable:

- Source, asset, and authored-data locations, with their purposes.
- Engine and language conventions.
- Setup, run, build, and developer-tool entry points.
- Automated verification entry points and when each is required.
- Project contracts and responsibility boundaries.
- The Documentation Index and its maintenance entry point.
- The visual-capture route.

Each entry MUST state the task or question the resource serves and provide
its path, command, or an inline link to its canonical instructions.

Index responsibility areas and workflow entry points, not every file.
MUST NOT copy a resource's contents into its index entry.

Keep the Project Index in project-scoped AGENTS.md. A category MAY link
to a dedicated index or instruction document instead of expanding its
contents in AGENTS.md.

Update affected entries in the same change that moves, removes, renames,
or changes the purpose of an indexed resource.

For example, a capture entry links to a workflow that provides the capture
mode, virtual display, driver entry point, and encoder command.

By contrast, a source folder entry identifies the system the folder owns;
it does not list every class inside the folder.

Why: readers need routes to code, tools, contracts, and verification,
not only routes to documents.