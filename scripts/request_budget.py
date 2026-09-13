#!/usr/bin/env python3
"""Claude Code hook that enforces the request budget from Task Management in ~/.agents/AGENTS.md.

UserPromptSubmit records when a request starts. PreToolUse denies tool calls once the budget is spent,
except the calls an agent needs to save progress: reading files and editing task files under `delivery/`.
"""
import json
import os
import sys
import time
from pathlib import Path

BUDGET_SECONDS = int(os.environ.get("AGENT_REQUEST_BUDGET_SECONDS", "900"))
STATE_DIR = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "agent-request-budget"
READ_ONLY_TOOLS = {"Read", "Glob", "Grep"}
EDIT_TOOLS = {"Edit", "Write", "MultiEdit"}


def start_file(session_id: str) -> Path:
    return STATE_DIR / f"{session_id}.start"


def record_start(payload: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    start_file(payload["session_id"]).write_text(str(time.time()))


def is_task_file_edit(payload: dict) -> bool:
    if payload.get("tool_name") not in EDIT_TOOLS:
        return False
    path = Path(payload.get("tool_input", {}).get("file_path", ""))
    return "delivery" in path.parts and path.suffix == ".md"


def check_budget(payload: dict) -> None:
    path = start_file(payload["session_id"])
    # No recorded start: the session began before the hook was installed, so there is no budget to enforce.
    if not path.exists():
        return
    elapsed = time.time() - float(path.read_text())
    if elapsed <= BUDGET_SECONDS:
        return
    if payload.get("tool_name") in READ_ONLY_TOOLS or is_task_file_edit(payload):
        return
    reason = (
        f"The request budget of {BUDGET_SECONDS // 60} minutes is spent ({int(elapsed // 60)} minutes elapsed). "
        "STOP starting work. Record the remaining work in the task file under delivery/ "
        "(Read and Edit on task files stay allowed), then report to the developer."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


def main() -> None:
    payload = json.load(sys.stdin)
    event = payload.get("hook_event_name")
    if event == "UserPromptSubmit":
        record_start(payload)
    elif event == "PreToolUse":
        check_budget(payload)


if __name__ == "__main__":
    main()
