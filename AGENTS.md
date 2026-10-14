# Global Instructions Development

Summary: This repository is the source project for developing global agent instructions used in `~/.agents/`.

## Project brief

This project holds the source instructions and is used to develop new rules. The effective instructions used by agents are in `/home/binhbocnc/.agents/` (`~/.agents/`).

[AGENTS.development.md](AGENTS.development.md) holds the global instruction document being developed in this repository. This `AGENTS.md` describes the purpose of the project rather than duplicating that document.

## Install instructions

Run `python3 tools/install_agents.py` to install the development document as `~/.agents/AGENTS.md` and copy `rules/` into `~/.agents/rules/`. The installer preserves `@` imports and leaves other destination files untouched.

Run `python3 tools/install_agents.py --check` to compare without writing. Use `--destination /path/to/directory` for an isolated installation.

Verify the installer with `python3 -m unittest discover -s tools/tests -p 'test_install_agents.py'`.
