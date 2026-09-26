---
name: project-map
description: Repository context management for Codex. Bootstrap/repair project-local context hooks when needed; normal turns receive runtime rules plus `.project-map.md` navigation memory and `.project-decisions.md` engineering decisions through the installed hook.
---

# Project Map

Maintain two compact repo-local durable context artifacts: `.project-map.md` for navigation/routing knowledge and `.project-decisions.md` for current project-specific engineering decisions that should survive new chats.

The implementation is split by lifecycle so installation-only instructions are not loaded on normal repository turns.

## References

- `references/installation.md` — bootstrap, install, upgrade, repair, hook configuration, runtime-copy, trust, and `AGENTS.md` fallback behavior. Read this only when project-map infrastructure is absent, stale, being installed, upgraded, or explicitly repaired.
- `references/runtime.md` — the complete runtime contract for navigation memory, engineering-decision memory, admission, reconciliation, compression, pruning, and file formats. The installed project hook copies this to `<repo>/.codex/hooks/project_map_runtime.md` and injects it automatically on each user prompt.
- `hooks/project_map_hook.py` — executable lifecycle hook asset. Do not read it during ordinary project work unless installing, repairing, debugging, or upgrading the hook itself.

## Normal repository turns

When the trusted project-local hook is installed and working, do not reload the installation reference or this skill for project-context runtime behavior. Use the hook-injected runtime, `CURRENT PROJECT MAP`, and `CURRENT PROJECT DECISIONS` context.

The hook is responsible for lifecycle timing; `references/runtime.md` is authoritative for both map-quality and decision-memory behavior.

## Bootstrap or repair

If `.project-map.md`, `.project-decisions.md`, `.codex/hooks/project_map_hook.py`, `.codex/hooks/project_map_runtime.md`, required project-map handlers in `.codex/hooks.json`, or the fallback `AGENTS.md` section is missing/stale, read and follow `references/installation.md`.

If hooks are unavailable or untrusted for the current turn, read `references/runtime.md` directly and follow it as the fallback runtime contract.
