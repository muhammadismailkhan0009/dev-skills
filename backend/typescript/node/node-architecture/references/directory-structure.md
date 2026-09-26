# Node Directory Structure

Choose the smallest structure that makes ownership and dependency direction obvious. Apply `$semantic-organization` within each architectural area.

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

A small CLI might be:

```text
src/
├── main.ts
├── entrypoints/
│   └── cli/
│       ├── cli.ts
│       └── skill-command.ts
├── application/
│   ├── skill-registry.ts
│   └── ports/
│       └── skill-store.ts
├── domain/
│   └── skill.ts
└── infrastructure/
    └── filesystem/
        └── filesystem-skill-store.ts
```

Here `skill-command.ts` may own several related CLI operations, and `skill-registry.ts` may expose several related application operations, as long as each remains semantically cohesive.

## Process entrypoint vs application entrypoints

`main.ts` is the process entrypoint: Node executes it to bootstrap the application.

`entrypoints/` contains application entrypoints: boundaries through which external events ask the application to perform behavior.

Examples:

```text
entrypoints/
├── cli/
│   ├── cli.ts
│   └── skill-command.ts
├── mcp/
│   ├── mcp-server.ts
│   ├── skill-tools.ts
│   └── repository-tools.ts
├── http/
│   └── skill-handler.ts
├── events/
│   └── skill-events.ts
├── scheduled/
│   └── registry-refresh.ts
└── workers/
    └── install-jobs.ts
```

Runtime hosts such as `cli.ts` or `mcp-server.ts` configure/register handlers. A handler file may group several related operations when they share one semantic owner.

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

## Semantic grouping inside layers

Architectural layers answer where a responsibility belongs. Semantic organization answers how related implementation inside that boundary should be grouped.

For example:

```text
entrypoints/mcp/
├── mcp-server.ts
├── skill-tools.ts
└── repository-tools.ts

application/
├── skill-registry.ts
└── repository-source.ts
```

A file/class/module may contain several related operations. Do not create `install-skill.ts`, `remove-skill.ts`, `list-skills.ts`, and `refresh-skills.ts` by default when one cohesive `SkillRegistry` concept naturally owns them.

Split only when semantic ownership diverges or one concept develops meaningful sub-concepts. File length or function count alone is not a split criterion.

## Shared code

Keep code local until it is actually reused.

```text
one concept/capability owns it
→ keep local

multiple concepts in one module use it
→ module-local shared code

multiple modules genuinely use it
→ src/shared/
```

Do not turn `shared/` into a catch-all.

## Package and executable layout

Keep runtime architecture separate from npm packaging.

For an executable package, `package.json#bin` should point to the built executable entry. Source organization may still use `src/main.ts` or a thin executable wrapper.

Do not put application behavior into a generated `bin/` shim. The shim/process entry starts the application; behavior belongs in entrypoints/application/domain.
