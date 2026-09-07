---
name: project-map
description: Repository context management for Codex. Bootstrap/repair project-local project-map hooks when needed; normal turns receive runtime memory-management rules and `.project-map.md` through the installed hook.
---

# Project Map

Maintain one repo-local `.project-map.md` as a compact navigation cache that reduces repository rediscovery and repeated read/search cost.

The implementation is split by lifecycle so installation-only instructions are not loaded on normal repository turns.

## References

- `references/installation.md` — bootstrap, install, upgrade, repair, hook configuration, runtime-copy, trust, and `AGENTS.md` fallback behavior. Read this only when project-map infrastructure is absent, stale, being installed, upgraded, or explicitly repaired.
- `references/runtime.md` — the complete runtime contract for map navigation, admission, map-miss learning, reconciliation, compression, pruning, file-reference rules, and file format. The installed project hook copies this to `<repo>/.codex/hooks/project_map_runtime.md` and injects it automatically on each user prompt.
- `hooks/project_map_hook.py` — executable lifecycle hook asset. Do not read it during ordinary project work unless installing, repairing, debugging, or upgrading the hook itself.

## Normal repository turns

When the trusted project-local hook is installed and working, do not reload the installation reference or this skill for project-map runtime behavior. Use the hook-injected `PROJECT MAP RUNTIME` and `CURRENT PROJECT MAP` context.

The hook is responsible for lifecycle timing; `references/runtime.md` is authoritative for map-quality behavior.

## Bootstrap or repair

If `.project-map.md`, `.codex/hooks/project_map_hook.py`, `.codex/hooks/project_map_runtime.md`, required project-map handlers in `.codex/hooks.json`, or the fallback `AGENTS.md` section is missing/stale, read and follow `references/installation.md`.

If hooks are unavailable or untrusted for the current turn, read `references/runtime.md` directly and follow it as the fallback runtime contract.
