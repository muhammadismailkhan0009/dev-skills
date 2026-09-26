---
name: node-architecture
description: Structure TypeScript/Node backends, CLIs, MCP servers, workers, daemons, and other non-frontend runtimes with obvious entrypoints, inward dependency flow, and low cognitive overhead. Use when creating, moving, reviewing, or organizing Node application code.
---

# Node Architecture

Use `$semantic-organization` and `$typescript-style` with this skill.

Optimize the codebase so a developer can answer four questions directly from the filesystem:

1. What starts the process? → `main.ts`
2. What can invoke application behavior? → `entrypoints/`
3. Where is application orchestration? → `application/`
4. How does the application reach external systems? → `infrastructure/`

Treat CLI commands, MCP tools, HTTP handlers, event consumers, scheduled jobs, workers, and filesystem watchers as the same architectural concept: inbound entrypoints.

Default dependency direction:

```text
outside event
    ↓
entrypoints
    ↓
application
    ↓
domain

application output ports
    ↓
infrastructure
```

Read:
- [directory structure](references/directory-structure.md) for small-project and module-first layouts, semantic grouping within those boundaries, and growth rules.
- [dependency boundaries](references/dependency-boundaries.md) for entrypoint/application/domain/infrastructure responsibilities and allowed dependencies.
- [runtime boundaries](references/runtime-boundaries.md) for process startup, CLI, MCP, HTTP, workers, events, schedules, stdio, signals, and lifecycle ownership.

Keep `main.ts` as the composition root: construct dependencies, wire adapters, select/start the runtime, and own top-level shutdown/error handling. Do not place business behavior there.

Do not create empty architectural directories in advance. A small application may omit `domain/` when it has no meaningful domain rules, or omit `ports/` until an outward dependency needs an application-owned contract.

For one small capability, use layer-first structure. When the application contains multiple independently meaningful capabilities, switch to module-first structure with the same layers inside each module.

Within each architectural area, group implementation by semantic ownership rather than mechanically by function or file size. A class, module, or directory may contain multiple related operations when they form one coherent concept.

The navigation invariant is:

```text
entrypoints/<runtime>/<handler-or-group>
    → application/<use-case-or-semantic-unit>
    → domain
    → application port
    → infrastructure/<adapter>
```

For any externally triggered behavior, this path should be easy to trace. If it is not, reduce indirection or move responsibilities until it is.
