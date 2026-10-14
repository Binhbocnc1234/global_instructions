#!/usr/bin/env python3
"""Install shared rules before project context using Codex's base-instruction file.

Bootstrap with --native-instructions pointing to the unmodified base instructions
from a Desktop transcript's session_meta. Later runs reuse the installed snapshot:
python3 tools/install_codex_cache.py [--check]
Refresh the native snapshot explicitly when changing the runtime/model defaults.
Requires the one-harness cache runtime, selected by Desktop's CODEX_CLI_PATH.
This changes instruction placement and affinity; cache hits are not guaranteed.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

from compile_codex_agents import CompileError, compile_document

MARKER = "<!-- Shared global rules for prompt cache reuse. -->"


def installation_files(home: Path, source: Path, native_source: Path, runtime: Path, desktop_file: Path) -> dict[Path, str]:
    cache = home / "instruction-cache"
    output = cache / "ModelInstructions.md"
    native = native_source.read_text(encoding="utf-8").strip()
    if not native or MARKER in native or "# Global Agent Rules" in native:
        raise ValueError("Native instructions must be a nonempty, unmodified model base prompt")
    override = home / "AGENTS.override.md"
    if override.exists() and override.read_text(encoding="utf-8").strip():
        raise ValueError(f"Active global override would duplicate or replace shared rules: {override}")
    agents = home / "AGENTS.md"
    previous = agents.read_text(encoding="utf-8") if agents.exists() else ""
    if previous.strip() and previous != compile_document(source, agents):
        raise ValueError(f"Refusing to clear global instructions not generated from the selected source: {agents}")
    config_path = home / "config.toml"
    config_text = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    config = tomllib.loads(config_text)
    configured = config.get("model_instructions_file")
    if configured is not None and configured != str(output):
        raise ValueError("Another model_instructions_file is already configured")
    global_rules = compile_document(source, output)
    combined = native + "\n\n" + MARKER + "\n\n" + global_rules
    previous_prefix = config.get("global_prompt_cache_prefix")
    if previous_prefix is not None and (not output.exists() or previous_prefix != output.read_text(encoding="utf-8").strip()):
        raise ValueError("Another global_prompt_cache_prefix is already configured")
    values = {"model_instructions_file": str(output), "global_prompt_cache_prefix": combined.strip()}
    # Generated settings are single-line JSON strings, which are valid TOML.
    # Replacing only these root assignments preserves every other setting byte.
    lines = config_text.splitlines(keepends=True)
    root_end = next((i for i, line in enumerate(lines) if line.lstrip().startswith("[")), len(lines))
    root_lines = lines[:root_end]
    for key in values:
        if key in config:
            matches = [i for i, line in enumerate(root_lines) if line.strip().startswith(key + " =")]
            if len(matches) != 1:
                raise ValueError(f"Cannot safely update the existing {key} assignment")
            root_lines[matches[0]] = ""
    assignments = "".join(key + " = " + json.dumps(value) + "\n" for key, value in values.items())
    config_text = assignments + "".join(root_lines + lines[root_end:])
    expected = {**config, **values}
    if tomllib.loads(config_text) != expected:
        raise ValueError("Configuration edit changed unrelated settings")
    if not runtime.is_file() or not (runtime.parent / "codex-code-mode-host").is_file():
        raise ValueError("The cache runtime and its codex-code-mode-host dependency must be installed")
    version = subprocess.run([str(runtime), "--version"], capture_output=True, text=True, check=True).stdout
    if "one-harness-cache." not in version:
        raise ValueError("The selected runtime does not identify the required cache patch")
    launcher_source = desktop_file if desktop_file.exists() else Path("/usr/share/applications/chatgpt.desktop")
    launcher = launcher_source.read_text(encoding="utf-8")
    launcher_lines = launcher.splitlines(keepends=True)
    entry_end = next((i for i, line in enumerate(launcher_lines[1:], 1) if line.startswith("[")), len(launcher_lines))
    entries = [i for i, line in enumerate(launcher_lines[:entry_end]) if line.startswith("Exec=")]
    if len(entries) != 1:
        raise ValueError("Desktop entry must contain exactly one main Exec assignment")
    expected_exec = f'Exec=/usr/bin/env "CODEX_CLI_PATH={runtime}" /usr/bin/chatgpt %U\n'
    current_exec = launcher_lines[entries[0]]
    if current_exec.strip() not in ("Exec=chatgpt %U", expected_exec.strip()):
        raise ValueError("Refusing to replace a customized Desktop launch command")
    launcher_lines[entries[0]] = expected_exec
    return {
        cache / "NativeInstructions.md": native + "\n",
        output: combined,
        config_path: config_text,
        agents: "",
        desktop_file: "".join(launcher_lines),
    }


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
        temporary.chmod(path.stat().st_mode & 0o777 if path.exists() else 0o644)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path(os.environ.get("CODEX_HOME", "~/.codex")))
    parser.add_argument("--source", type=Path, default=Path("~/.agents/AGENTS.md"))
    parser.add_argument("--native-instructions", type=Path)
    parser.add_argument("--runtime", type=Path, default=Path("~/.local/share/one-harness/codex-cache/bin/codex"))
    data_home = Path(os.environ.get("XDG_DATA_HOME", "~/.local/share")).expanduser()
    parser.add_argument("--desktop-file", type=Path, default=data_home / "applications/chatgpt.desktop")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    source = args.source.expanduser().resolve()
    native_source = (args.native_instructions or home / "instruction-cache/NativeInstructions.md").expanduser().resolve()
    try:
        files = installation_files(home, source, native_source, args.runtime.expanduser().resolve(), args.desktop_file.expanduser().resolve())
        changed = [path for path, text in files.items() if not path.exists() or path.read_text(encoding="utf-8") != text]
        if args.check:
            for path in changed:
                print(f"Missing or stale: {path}", file=sys.stderr)
            if changed:
                return 1
            print("Up to date: stable model prefix, project discovery preserved, no duplicate home rules")
            return 0
        backup = home / "instruction-cache" / "before-install"
        for path in changed:
            saved = backup / path.name
            if path in (home / "config.toml", home / "AGENTS.md") and path.exists() and not saved.exists():
                write_atomic(saved, path.read_text(encoding="utf-8"))
        # Install the prefix before pointing config at it. Clearing the generated
        # home document comes last so a failed earlier write cannot remove rules.
        for path in changed:
            write_atomic(path, files[path])
            print(f"Installed: {path}")
        return 0
    except (CompileError, OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
