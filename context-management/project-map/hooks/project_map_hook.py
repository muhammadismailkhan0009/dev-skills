#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MAP_NAME = ".project-map.md"
DECISIONS_NAME = ".project-decisions.md"
RUNTIME_NAME = "project_map_runtime.md"
STATE_DIR_NAME = "codex-project-map-hook"


def read_input():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def repo_root(cwd):
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            timeout=2,
            check=True,
        )
        return Path(result.stdout.strip())
    except Exception:
        return Path(cwd)


def state_path(data, root):
    session_id = str(data.get("session_id") or "unknown-session").replace("/", "_")
    turn_id = str(data.get("turn_id") or "unknown-turn").replace("/", "_")
    root_key = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:16]
    base = Path(tempfile.gettempdir()) / STATE_DIR_NAME / root_key / session_id
    base.mkdir(parents=True, exist_ok=True)
    return base / f"{turn_id}.active"


def emit(obj):
    json.dump(obj, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def user_prompt_submit(data, root):
    runtime_path = root / ".codex" / "hooks" / RUNTIME_NAME
    map_path = root / MAP_NAME
    decisions_path = root / DECISIONS_NAME

    runtime = read_text(runtime_path)
    project_map = read_text(map_path)
    project_decisions = read_text(decisions_path)

    parts = []
    if runtime:
        parts.append("PROJECT CONTEXT RUNTIME (hook-enforced)\n" + runtime)
    else:
        parts.append(
            "PROJECT CONTEXT RUNTIME MISSING\n"
            "The installed project-map runtime reference is missing or unreadable. Use the installed $project-map skill and its installation reference to repair project-context infrastructure before broad repository exploration."
        )

    if project_map is not None:
        parts.append("CURRENT PROJECT MAP\n" + project_map)
    else:
        parts.append(
            "CURRENT PROJECT MAP MISSING\n"
            "No .project-map.md exists at the repository root. Bootstrap it sparsely using the installed $project-map installation reference before broad repository exploration."
        )

    if project_decisions is not None:
        parts.append("CURRENT PROJECT DECISIONS\n" + project_decisions)
    else:
        parts.append(
            "CURRENT PROJECT DECISIONS MISSING\n"
            "No .project-decisions.md exists at the repository root. Bootstrap the minimal decisions file using the installed $project-map installation reference before broad repository exploration."
        )

    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "\n\n".join(parts),
            }
        }
    )


def post_tool_use(data, root):
    tool_name = str(data.get("tool_name") or "")
    if tool_name in {"update_plan", "spawn_agent", "Agent"}:
        return
    marker = state_path(data, root)
    try:
        marker.write_text(tool_name or "tool", encoding="utf-8")
    except Exception:
        pass


def stop(data, root):
    marker = state_path(data, root)
    if data.get("stop_hook_active"):
        try:
            marker.unlink(missing_ok=True)
        except Exception:
            pass
        return
    if not marker.exists():
        return
    try:
        marker.unlink(missing_ok=True)
    except Exception:
        pass
    emit(
        {
            "decision": "block",
            "reason": (
                "The primary requested work is complete. Before returning the final response, perform the mandatory project-context end-of-turn reconciliation now using the injected PROJECT CONTEXT RUNTIME rules and all durable repository knowledge and engineering decisions learned this turn. Do not perform extra repository exploration solely for context maintenance. Reconcile .project-map.md and .project-decisions.md independently, rewriting either only if its content changes, then return the user's final response."
            ),
        }
    )


def main():
    data = read_input()
    cwd = str(data.get("cwd") or os.getcwd())
    root = repo_root(cwd)
    event = data.get("hook_event_name")
    if event == "UserPromptSubmit":
        user_prompt_submit(data, root)
    elif event == "PostToolUse":
        post_tool_use(data, root)
    elif event == "Stop":
        stop(data, root)


if __name__ == "__main__":
    main()
