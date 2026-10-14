# Global Instructions Development

Summary: This repository is the source project for developing global agent instructions used in `~/.agents/`.

## Project brief

This project holds the source instructions and is used to develop new rules. The effective instructions used by agents are in `/home/binhbocnc/.agents/` (`~/.agents/`).

[AGENTS.development.md](AGENTS.development.md) holds the global instruction document being developed in this repository. This `AGENTS.md` describes the purpose of the project rather than duplicating that document.

## Repository folders

- `scripts/` contains executable support for the global instructions: Git checks, request-budget hooks, and keyring access, together with automated tests for those scripts.
- `test/` contains behavioral evaluation scenarios for the agent rules, written as Markdown rather than executable test code. Like unit and integration tests, they specify scenario inputs, expected behavior, and failure conditions to check individual rules or interactions between rules. These scenarios are evaluation criteria, not evidence that the rules have passed.

## Install instructions

Run `python3 tools/install_agents.py` to install the development document as `~/.agents/AGENTS.md` and copy `rules/` into `~/.agents/rules/`. The installer preserves `@` imports and leaves other destination files untouched.

Run `python3 tools/install_agents.py --check` to compare without writing. Use `--destination /path/to/directory` for an isolated installation.

Verify the installer with `python3 -m unittest discover -s tools/tests -p 'test_install_agents.py'`.

## Global Git hooks

Run `python3 tools/install_global_hooks.py` to install the shared checkers in `~/.agents/scripts/` and the pre-commit hook in `~/.agents/hooks/`, then enable Git's global `core.hooksPath`. Rerun this command after changing the checkers or hook; the instruction installer does not update them.

The hook runs an existing repository-local `.git/hooks/pre-commit` first, then checks the resulting index for source/Markdown line counts, local Markdown links, and folder-child violations. Repository-specific `core.hooksPath` settings override the global hook. Git's `--no-verify` can bypass it.

Projects may commit `.agent-checks.json` with `source_extensions` (replaces the default source extension list), `exclude` (repository-relative third-party/generated directories), and `line_exceptions` (repository-relative file paths mapped to nonempty reasons). Markdown remains in the line-count check regardless of `source_extensions`. The schema and defaults belong to `scripts/check_staged_files.py`.

Folder-check settings remain in `.folder-child-limit.json`, documented by `scripts/folder_child_limit.py`. Both configurations are read from the index during pre-commit checks.

Verify real commit workflows with `python3 -m unittest discover -s tools/tests -p 'test_global_hooks.py'`; those tests use isolated global Git configuration.
