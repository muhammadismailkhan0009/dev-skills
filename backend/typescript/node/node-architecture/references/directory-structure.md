# Node Directory Structure

Choose the smallest structure that makes ownership and dependency direction obvious.

## Small application: layer first

Use this for a CLI, MCP server, adapter, worker, daemon, or service with one primary capability area.

```text
<node-root>/
├── src/
│   ├── main.ts
│   ├── entrypoints/
│   │   ├── cli/
│   │   ├── mcp/
│   │   ├── http/
│   │   ├── events/
│   │   ├── scheduled/
│   │   └── workers/
│   ├── application/
│   │   └── ports/
│   ├── domain/
│   └── infrastructure/
│       ├── filesystem/
│       ├── database/
│       ├── network/
│       ├── process/
│       └── <external-system>/
├── package.json
└── ...runtime/build configuration...
```

Create only directories that real code needs.

A small CLI might be only:

```text
src/
├── main.ts
├── entrypoints/
│   └── cli/
│       ├── cli.ts
│       ├── install-command.ts
│       └── list-command.ts
├── application/
│   ├── install-skill.ts
│   ├── list-skills.ts
│   └── ports/
│       └── skill-store.ts
├── domain/
│   └── skill.ts
└── infrastructure/
    └── filesystem/
        └── filesystem-skill-store.ts
```

## Process entrypoint vs application entrypoints

`main.ts` is the process entrypoint: Node executes it to bootstrap the application.

`entrypoints/` contains application entrypoints: boundaries through which external events ask the application to perform behavior.

Examples:

```text
entrypoints/
├── cli/
│   ├── cli.ts
│   └── install-command.ts
├── mcp/
│   ├── mcp-server.ts
│   └── install-skill-tool.ts
├── http/
│   └── install-skill-handler.ts
├── events/
│   └── skill-published-handler.ts
├── scheduled/
│   └── refresh-registry.ts
└── workers/
    └── process-install-job.ts
```

Runtime hosts such as `cli.ts` or `mcp-server.ts` configure/register handlers. Individual commands/tools/handlers are the behavioral entrypoints.

## Larger application: module first

When several independently meaningful capabilities emerge, keep ownership local by module:

```text
src/
├── main.ts
├── modules/
│   ├── registry/
│   │   ├── entrypoints/
│   │   ├── application/
│   │   │   └── ports/
│   │   ├── domain/
│   │   └── infrastructure/
│   ├── jobs/
│   │   ├── entrypoints/
│   │   ├── application/
│   │   ├── domain/
│   │   └── infrastructure/
│   └── browser/
│       └── ...
└── shared/
    └── ...
```

Use module-first when global layer directories would force a developer to scan unrelated capabilities to trace one behavior.

Do not create modules merely because several folders exist. A module should represent a coherent business/capability boundary.

## File granularity

Use small file-based units.

Prefer:

```text
entrypoints/mcp/
├── mcp-server.ts
├── list-skills-tool.ts
├── install-skill-tool.ts
└── remove-skill-tool.ts
```

instead of a large `mcp-tools.ts` containing every tool.

Prefer:

```text
application/
├── install-skill.ts
├── remove-skill.ts
└── list-skills.ts
```

instead of an all-purpose `skill-service.ts`.

Do not introduce a directory per file. Group only when a concept owns multiple supporting files.

## Shared code

Keep code local until it is actually reused.

```text
one operation/capability owns it
→ keep local

multiple operations in one module use it
→ module-local shared code

multiple modules genuinely use it
→ src/shared/
```

Do not turn `shared/` into a catch-all.

## Package and executable layout

Keep runtime architecture separate from npm packaging.

For an executable package, `package.json#bin` should point to the built executable entry. Source organization may still use `src/main.ts` or a thin executable wrapper.

Do not put application behavior into a generated `bin/` shim. The shim/process entry starts the application; behavior belongs in entrypoints/application/domain.
