#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from pathlib import Path

CATALOG_NAME = "skill_catalog.md"
SECTION_PATTERN = re.compile(r"^## \$(\S+)\s*$")


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


def codex_skills_dir():
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    return codex_home / "skills"


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def filter_catalog(catalog, skills_dir):
    preamble = []
    sections = []
    current_name = None
    current_lines = []

    for line in catalog.splitlines():
        match = SECTION_PATTERN.match(line)
        if match:
            if current_name is not None:
                sections.append((current_name, current_lines))
            current_name = match.group(1)
            current_lines = [line]
        elif current_name is None:
            preamble.append(line)
        else:
            current_lines.append(line)

    if current_name is not None:
        sections.append((current_name, current_lines))

    installed_sections = []
    for name, lines in sections:
        if (skills_dir / name / "SKILL.md").is_file():
            installed_sections.append("\n".join(lines).rstrip())

    parts = ["\n".join(preamble).rstrip()]
    if installed_sections:
        parts.extend(installed_sections)
    else:
        parts.append("No catalogued development skills are currently installed.")
    return "\n\n".join(part for part in parts if part)


def emit(obj):
    json.dump(obj, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


def user_prompt_submit(root):
    catalog_path = root / ".codex" / "hooks" / CATALOG_NAME
    catalog = read_text(catalog_path)

    if catalog is None:
        context = (
            "SKILL DISCOVERY CATALOG MISSING\n"
            "The project-local skill catalog is missing or unreadable. Use the installed $skill-discovery skill and its installation reference to repair skill-discovery infrastructure."
        )
    else:
        filtered = filter_catalog(catalog, codex_skills_dir())
        context = "SKILL DISCOVERY (hook-injected)\n" + filtered

    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        }
    )


def main():
    data = read_input()
    if data.get("hook_event_name") != "UserPromptSubmit":
        return
    cwd = str(data.get("cwd") or os.getcwd())
    user_prompt_submit(repo_root(cwd))


if __name__ == "__main__":
    main()
