---
name: skill-discovery
description: Install or repair a shared Codex skill-discovery hook that exposes a compact hierarchical catalog of installed development skills and their references so the model can lazily load only relevant knowledge.
---

# Skill Discovery

Provide durable awareness of available development skills without eagerly loading their full instructions or references.

## Runtime model

The trusted project-local hook injects a compact catalog on `UserPromptSubmit`. The catalog contains lightweight skill descriptions and reference-level routing hints. The model decides which skills apply, reads only selected `SKILL.md` files, then reads only references needed for the current concern.

Do not preload every listed skill or reference. If no listed skill applies, load none.

Existing development skills remain authoritative and unchanged. This discovery layer only makes them reliably visible and lazily selectable.

## Installation and repair

Read `references/installation.md` only when installing, upgrading, or repairing skill-discovery infrastructure.

The source catalog is `references/skill-catalog.md`. The installed hook filters that catalog against skills actually present under `${CODEX_HOME:-$HOME/.codex}/skills` before injection, so unavailable catalog entries do not consume model context.

The executable asset is `hooks/skill_discovery_hook.py`. Do not read it during ordinary repository work unless debugging or upgrading the hook itself.

When hooks are unavailable or untrusted, ordinary skill installation/discovery still works normally; this package is an optional durability layer, not a requirement for the development skills themselves.