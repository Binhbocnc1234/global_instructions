"""Exercise installed hooks through real commits with isolated global config."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

INSTALLER = Path(__file__).resolve().parents[1] / "install_global_hooks.py"


class GlobalHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.base = Path(self.directory.name)
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        self.env.update(HOME=str(self.base), GIT_CONFIG_GLOBAL=str(self.base / ".gitconfig"), GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="Test", GIT_AUTHOR_EMAIL="test@example.invalid", GIT_COMMITTER_NAME="Test", GIT_COMMITTER_EMAIL="test@example.invalid")
        self.root = self.repository("existing")
        self.destination = self.base / ".agents"
        result = self.command(self.base, sys.executable, str(INSTALLER), "--destination", str(self.destination))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def tearDown(self) -> None:
        self.directory.cleanup()

    def command(self, cwd: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(arguments, cwd=cwd, env=self.env, capture_output=True, text=True)

    def git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return self.command(self.root, "git", *arguments)

    def repository(self, name: str) -> Path:
        path = self.base / name
        path.mkdir()
        result = self.command(path, "git", "init", "-q")
        self.assertEqual(result.returncode, 0, result.stderr)
        return path

    def write(self, name: str, text: str) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def stage(self, *paths: str) -> None:
        result = self.git("add", "--", *paths)
        self.assertEqual(result.returncode, 0, result.stderr)

    def commit(self, succeeds: bool) -> subprocess.CompletedProcess[str]:
        result = self.git("commit", "-q", "-m", "test: verify hooks")
        if succeeds:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def test_existing_and_new_repositories(self) -> None:
        for name in ("existing", "new"):
            self.root = self.base / name if name == "existing" else self.repository(name)
            for path, boundary in (("Source.py", "pass\n" * 4800), ("Notes.md", "é🙂\r\n" * 6000)):
                self.write(path, boundary + "x")
                self.stage(path)
                self.write(path, "unstaged text\n")
                result = self.commit(False)
                self.assertIn("24001 characters, limit 24000", result.stdout + result.stderr)
                self.write(path, boundary)
                self.stage(path)
                self.write(path, boundary + "x")
                self.commit(True)

    def test_index_links_not_worktree_links(self) -> None:
        trace = self.base / "git-trace"
        self.env["GIT_TRACE"] = str(trace)
        (self.root / "Unrelated.bin").write_bytes(b"\xff\x00\xfe")
        self.stage("Unrelated.bin")
        self.write("Source.md", "[link](Target.md#staged)\n")
        self.write("Target.md", "# Staged\n")
        self.stage("Source.md", "Target.md")
        self.write("Source.md", "[broken](Missing.md)\n")
        self.write("Target.md", "# Unstaged\n")
        self.commit(True)
        self.stage("Source.md")
        result = self.commit(False)
        self.assertIn("Missing.md: target does not exist", result.stdout + result.stderr)
        self.write("Source.md", "[link](Target.md#unstaged)\n")
        self.stage("Source.md")
        result = self.commit(False)
        self.assertIn("heading anchor does not exist", result.stdout + result.stderr)
        self.write("Source.md", "[link](Target.md#staged)\n[asset](assets/item.bin)\n[directory](assets)\n")
        self.write("assets/item.bin", "asset\n")
        self.stage("Source.md", "assets")
        self.commit(True)
        # Only the target changes; the unchanged source must still be checked.
        self.stage("Target.md")
        result = self.commit(False)
        self.assertIn("heading anchor does not exist", result.stdout + result.stderr)
        self.write("Target.md", "# Staged\n")
        self.stage("Target.md")
        self.git("mv", "Target.md", "Renamed.md")
        result = self.commit(False)
        self.assertIn("Target.md#staged: target does not exist", result.stdout + result.stderr)
        self.git("mv", "Renamed.md", "Target.md")
        self.git("rm", "assets/item.bin")
        result = self.commit(False)
        self.assertIn("assets/item.bin: target does not exist", result.stdout + result.stderr)
        self.assertIn("assets: target does not exist", result.stdout + result.stderr)
        self.assertNotIn("checkout-index", trace.read_text())

    def test_file_already_over_limit_warns_while_new_overflow_fails(self) -> None:
        self.write("Old.md", "x" * 24001)
        self.write("Near.md", "x" * 23999)
        self.stage(".")
        self.assertEqual(self.git("commit", "-q", "--no-verify", "-m", "test: existing oversize file").returncode, 0)
        # Editing and moving a file that HEAD already holds over the limit only warns.
        self.write("Old.md", "x" * 24010)
        self.stage("Old.md")
        result = self.commit(True)
        self.assertIn("warning: Old.md: 24010 characters, already over", result.stdout + result.stderr)
        (self.root / "docs").mkdir()
        self.assertEqual(self.git("mv", "Old.md", "docs/Old.md").returncode, 0)
        result = self.commit(True)
        self.assertIn("warning: docs/Old.md", result.stdout + result.stderr)
        # A commit that puts a file over the limit still fails, whether the file is new or grew past it.
        self.write("Near.md", "x" * 24002)
        self.write("New.md", "x" * 24001)
        self.stage(".")
        failed = self.commit(False)
        self.assertIn("Near.md: 24002 characters, limit 24000", failed.stdout + failed.stderr)
        self.assertIn("New.md: 24001 characters, limit 24000", failed.stdout + failed.stderr)

    def test_staged_exceptions_exclusions_and_custom_extensions(self) -> None:
        self.write("Main.custom", "x" * 24001)
        self.write("Long.md", "é" * 24001)
        self.write("vendor/Example.md", "[bad](Missing.md)\n" + "x" * 24001)
        config = {"source_extensions": [".custom"], "exclude": ["vendor"], "line_exceptions": {"Main.custom": "One generated protocol table", "Long.md": "One cohesive reference table"}}
        self.write(".agent-checks.json", json.dumps(config))
        self.stage(".")
        self.write(".agent-checks.json", "invalid json")
        self.commit(True)
        config["line_exceptions"]["Long.md"] = ""
        self.write(".agent-checks.json", json.dumps(config))
        self.stage(".agent-checks.json")
        self.assertIn("nonempty reasons", self.commit(False).stderr)
        config["line_exceptions"].pop("Long.md")
        self.write(".agent-checks.json", json.dumps(config))
        self.stage(".agent-checks.json")
        # A full audit includes unchanged files; normal commits remain selective.
        self.commit(True)
        result = self.command(self.root, sys.executable, str(self.destination / "scripts/check_staged_files.py"), "--all")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Long.md: 24001 characters", result.stdout + result.stderr)

    def test_folder_limit_uses_staged_config(self) -> None:
        for index in range(17):
            self.write(f"vendor/lib/file{index}.txt", "")
        self.stage("vendor")
        result = self.commit(False)
        self.assertIn("17 children", result.stdout + result.stderr)
        self.write(".folder-child-limit.json", json.dumps({"third_party": ["vendor/lib"]}))
        self.stage(".folder-child-limit.json")
        self.write(".folder-child-limit.json", "{}")
        self.commit(True)
        self.write("new/file.txt", "")
        self.stage("new")
        self.commit(True)
        self.write("new/file.txt", "content only\n")
        self.stage("new/file.txt")
        result = self.commit(True)
        self.assertIn("Skipped folder counts", result.stdout + result.stderr)
        # Configuration-only changes cannot take the content-only shortcut.
        self.write(".folder-child-limit.json", json.dumps({"third_party": ["vendor"]}))
        self.stage(".folder-child-limit.json")
        result = self.commit(True)
        self.assertNotIn("Skipped folder counts", result.stdout + result.stderr)
        self.write(".folder-child-limit.json", "{}")
        self.stage(".folder-child-limit.json")
        result = self.command(self.root, sys.executable, str(self.destination / "scripts/folder_child_limit.py"), "--staged", "--all")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("17 children", result.stdout + result.stderr)
        self.write(".folder-child-limit.json", json.dumps({"third_party": ["vendor"]}))
        self.stage(".folder-child-limit.json")
        for index in range(17):
            self.write(f"new/file{index}.txt", "")
        self.stage("new")
        result = self.commit(False)
        self.assertIn("18 children", result.stdout + result.stderr)

    def test_local_hook_preserved_and_mutations_checked(self) -> None:
        local = self.root / ".git/hooks/pre-commit"
        local.write_text("#!/bin/sh\necho ran > local-marker\nexit 7\n", encoding="utf-8")
        local.chmod(0o755)
        self.write("Source.py", "pass\n")
        self.stage("Source.py")
        self.commit(False)
        self.assertTrue((self.root / "local-marker").exists())
        local.write_text("#!/bin/sh\nyes pass | head -n 4801 > Source.py\ngit add Source.py\n", encoding="utf-8")
        result = self.commit(False)
        self.assertIn("24005 characters", result.stdout + result.stderr)
        local.write_text("#!/bin/sh\necho ran > local-marker\n", encoding="utf-8")
        self.write("Source.py", "pass\n")
        self.stage("Source.py")
        self.commit(True)

    def test_session_attribution_through_real_commits(self) -> None:
        self.env.pop("AGENT_SESSION_ID", None)
        self.write("Source.py", "pass\n")
        self.stage("Source.py")
        self.commit(True)
        self.assertNotIn("Agent-Session:", self.git("log", "-1", "--format=%B").stdout)
        session = "11111111-1111-4111-8111-111111111111"
        self.env["AGENT_SESSION_ID"] = session
        local = self.root / ".git/hooks/prepare-commit-msg"
        local.write_text('#!/bin/sh\nprintf "\\nLocal body\\n" >> "$1"\n', encoding="utf-8")
        local.chmod(0o755)
        for message in ("fix: attribution", f"fix: attribution\n\nAgent-Session: {session}",
                        "fix: attribution\n\nAgent-Session: 22222222-2222-4222-8222-222222222222\nAgent-Session: stale"):
            result = self.git("commit", "--allow-empty", "-m", message)
            self.assertEqual(result.returncode, 0, result.stderr)
            body = self.git("log", "-1", "--format=%B").stdout
            self.assertTrue(body.startswith("fix: attribution\n"), body)
            self.assertIn("Local body", body)
            self.assertEqual(body.count(f"Agent-Session: {session}"), 1, body)
        self.env["AGENT_SESSION_ID"] = "not-a-session"
        result = self.git("commit", "--allow-empty", "-m", "fix: invalid")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Malformed AGENT_SESSION_ID", result.stderr)

    def test_concurrent_session_commits(self) -> None:
        processes = []
        for index in (1, 2):
            root = self.repository(f"session-{index}")
            session = f"{index:08d}-1111-4111-8111-111111111111"
            env = {**self.env, "AGENT_SESSION_ID": session}
            process = subprocess.Popen(["git", "commit", "--allow-empty", "-m", "fix: concurrent"],
                                       cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            processes.append((root, session, process))
        for root, session, process in processes:
            stdout, stderr = process.communicate(timeout=20)
            self.assertEqual(process.returncode, 0, stdout + stderr)
            result = self.command(root, "git", "log", "-1", "--format=%B")
            self.assertEqual(result.stdout.count("Agent-Session:"), 1, result.stdout)
            self.assertIn(f"Agent-Session: {session}", result.stdout)

    def test_installer_rejects_other_global_hook(self) -> None:
        result = self.git("config", "--global", "core.hooksPath", str(self.base / "other-hooks"))
        self.assertEqual(result.returncode, 0)
        result = self.command(self.base, sys.executable, str(INSTALLER), "--destination", str(self.destination))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("different global core.hooksPath", result.stderr)


if __name__ == "__main__":
    unittest.main()
