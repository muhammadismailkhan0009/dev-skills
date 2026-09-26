# Project Context Installation and Repair

Use this reference only when bootstrapping, installing, upgrading, or repairing project-context infrastructure in a repository. Normal repository turns should use the installed runtime reference injected by the project hook instead of re-reading this file.

## Codex lifecycle hook: primary enforcement

For Codex, project hooks are the primary lifecycle mechanism. `AGENTS.md` is only a fallback instruction layer.

On first bootstrap, and whenever project-map hook files/config are missing or stale:

1. Ensure `<repo>/.codex/hooks/` exists.
2. Copy the installed skill asset `${CODEX_HOME:-$HOME/.codex}/skills/project-map/hooks/project_map_hook.py` to `<repo>/.codex/hooks/project_map_hook.py`, replacing only that project-map-owned file when its content differs.
3. Copy the installed runtime reference `${CODEX_HOME:-$HOME/.codex}/skills/project-map/references/runtime.md` to `<repo>/.codex/hooks/project_map_runtime.md`, replacing only that project-map-owned file when its content differs.
4. Ensure `<repo>/.codex/hooks.json` contains exactly one project-map handler for each of `UserPromptSubmit`, `PostToolUse`, and `Stop` using the canonical handlers below.
5. If `hooks.json` already exists, merge/repair only the project-map handlers. Preserve all unrelated hook events, matcher groups, handlers, metadata, and user/project configuration. Never replace the whole file merely to install project-map.
6. Do not duplicate project-map handlers on repeated bootstrap/update.
7. New or changed project hooks require Codex trust review. Do not claim they are active until trusted; tell the user to review/trust them with `/hooks` when needed.

Canonical project-map handlers:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/project_map_hook.py\"",
            "timeout": 5,
            "additionalContextLimit": 12000,
            "statusMessage": "Loading project context"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/project_map_hook.py\"",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/project_map_hook.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

The hook lifecycle is:

- `UserPromptSubmit`: inject the installed runtime contract plus current `.project-map.md` and `.project-decisions.md` into developer context so preflight and memory-maintenance behavior do not depend on the model choosing to read skill files.
- `PostToolUse`: mark that repository/local tool activity occurred during the turn. The hook ignores planning/agent-management-only tools.
- `Stop`: after primary work, force one continuation that applies the runtime end-of-turn reconciliation rules for both durable context artifacts. `stop_hook_active` prevents a reconciliation loop.

The hook must not reason about or rewrite project knowledge itself. It only guarantees lifecycle/context; the runtime reference owns map-quality rules.

## Persist fallback instructions

Ensure root `AGENTS.md` contains the following dedicated fallback section. Hooks are stronger and should be used when trusted, but this keeps the lifecycle understandable and provides a fallback when hooks are unavailable:

```markdown
## Project Context Preflight
Use the project-map lifecycle for repository work. Prefer the trusted project-local Codex hooks when available; otherwise consult `$project-map`, `.project-map.md`, and `.project-decisions.md` before broad repository exploration. Use the map for navigation and decisions for durable engineering constraints. Current source/config/tests and explicit current user direction remain authoritative. Complete the requested repository work before maintaining project context. After repository work is done and before the final response, reconcile both files from durable knowledge learned across the whole turn.
```

If root `AGENTS.md` does not exist, create it with this section. If it exists, add or repair only this dedicated section and preserve all unrelated user/project instructions. Do not duplicate the section. The only project-map-owned durable context artifacts are `.project-map.md` for navigation and `.project-decisions.md` for current engineering decisions.

For non-Codex harnesses, use the equivalent lifecycle mechanism if one exists; otherwise rely on the always-loaded project instruction layer. Do not duplicate project knowledge into those mechanisms.

## Automatic bootstrap

When `.project-map.md` or `.project-decisions.md` is absent, initialize the missing artifact without asking unless the user explicitly forbids repository metadata changes.

Use only cheap evidence already available or cheap to obtain:

- root `README.md` and `AGENTS.md` when present;
- build/workspace manifests such as `pom.xml`, `build.gradle`, `package.json`, `Cargo.toml`, or equivalents;
- top-level directories and at most a shallow directory listing;
- source files that must already be inspected for the current task.

Do not recursively inspect source to make first-time project context comprehensive. Create a sparse, correct `.project-map.md` and a minimal `.project-decisions.md`, install/repair the Codex project hook, copy the runtime reference, repair the fallback `AGENTS.md` section, continue the requested task, and let subsequent turns enrich both artifacts.

Use this minimal decisions bootstrap when no durable project-specific engineering decision is yet known:

```markdown
# Project Decisions

> Durable current engineering decisions. Keep concise and current; this is not a changelog or task/session memory.
```

A sparse correct map and minimal decisions file are better than expensive speculative context.

Bootstrap is the only project-context write allowed before the primary requested work because both artifacts must exist for preflight injection.
