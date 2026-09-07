#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MAP_NAME = ".project-map.md"
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


def user_prompt_submit(data, root):
    map_path = root / MAP_NAME
    if map_path.exists():
        try:
            content = map_path.read_text(encoding="utf-8")
        except Exception:
            return
        context = (
            "PROJECT MAP PREFLIGHT (hook-enforced)\n"
            "The current repository project map is injected below. Use it for routing before broad repository exploration. "
            "Current source remains authoritative. Do not maintain the map during the primary requested work. "
            "After repository work is complete, end-of-turn reconciliation is mandatory when source was inspected, searched, analyzed, or modified.\n\n"
            + content
        )
    else:
        context = (
            "PROJECT MAP PREFLIGHT (hook-enforced)\n"
            "No .project-map.md exists at the repository root. Before broad repository exploration, bootstrap it using the installed $project-map skill, "
            "then perform the requested work. Keep bootstrap sparse and source-authoritative."
        )
    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
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
                "The primary requested work is complete. Before returning the final response, perform the mandatory $project-map end-of-turn reconciliation now. "
                "Reconcile the whole logical .project-map.md using all durable navigation knowledge learned from every repository file/search/tool result encountered this turn, "
                "regardless of whether it belongs to the requested feature. Do not perform extra repository exploration solely for the map. "
                "Apply the project-map admission, compression, pruning, and stale-entry rules. Routes must reference physical files with filename extensions; "
                "use bare File.ext by default and only the shortest disambiguating path when necessary. Rewrite the map only if its reconciled content changes. "
                "After reconciliation, return the user's final response."
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
