# Skill Discovery Installation and Repair

Use this reference only when bootstrapping, installing, upgrading, or repairing project-local skill-discovery infrastructure. Normal repository turns should rely on the trusted hook-injected catalog.

## Install or repair

1. Resolve the repository root.
2. Ensure `<repo>/.codex/hooks/` exists.
3. Copy `${CODEX_HOME:-$HOME/.codex}/skills/skill-discovery/hooks/skill_discovery_hook.py` to `<repo>/.codex/hooks/skill_discovery_hook.py`, replacing only that skill-discovery-owned file when content differs.
4. Copy `${CODEX_HOME:-$HOME/.codex}/skills/skill-discovery/references/skill-catalog.md` to `<repo>/.codex/hooks/skill_catalog.md`, replacing only that skill-discovery-owned file when content differs.
5. Ensure `<repo>/.codex/hooks.json` contains exactly one skill-discovery `UserPromptSubmit` handler using the canonical handler below.
6. If `hooks.json` already exists, merge/repair only the skill-discovery handler. Preserve all unrelated hook events, matcher groups, handlers, metadata, and project/user configuration. In particular, preserve project-map handlers when present.
7. Do not duplicate the skill-discovery handler on repeated installation or repair.
8. New or changed project hooks require Codex trust review. Do not claim the hook is active until trusted; tell the user to review/trust it with `/hooks` when needed.

Canonical handler:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/skill_discovery_hook.py\"",
            "timeout": 5,
            "additionalContextLimit": 6000,
            "statusMessage": "Loading skill catalog"
          }
        ]
      }
    ]
  }
}
```

If `UserPromptSubmit` already has other matcher groups, append or repair only the group containing the exact project-local `skill_discovery_hook.py` command. Never replace the whole event array.

## Runtime behavior

The hook reads `<repo>/.codex/hooks/skill_catalog.md`, checks `${CODEX_HOME:-$HOME/.codex}/skills/<skill>/SKILL.md` for each catalog entry, and injects only entries whose skills are actually installed.

The injected catalog is a semantic menu. It tells the model which skills and references exist but does not load their full contents. The model must select applicable skills, read their `SKILL.md`, and then load only references relevant to the current concern according to those skills. It may load additional skills/references later if the task evolves.

Do not add `PostToolUse` or `Stop` handlers for skill discovery. This component guarantees awareness at prompt start; selected skill instructions and normal agent reasoning govern the rest of the turn.

## Portability

Do not modify the development skills to depend on this hook. They must remain normally installable and usable by agents without Codex hook support. When hooks are unavailable or untrusted, skill discovery falls back to the agent's native skill mechanism.