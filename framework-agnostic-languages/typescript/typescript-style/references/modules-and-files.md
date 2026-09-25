# Modules and Files

Optimize the filesystem for direct navigation and low reconstruction cost.

## File granularity

Prefer one primary responsibility per source file.

Good defaults:
- one meaningful class, component, adapter, use case, or contract per file;
- one cohesive family of tiny pure helpers per file when they are inseparable;
- filenames should reveal the concept or operation they contain;
- split a file when understanding one responsibility requires reading unrelated logic.

Prefer:

```text
application/
├── install-skill.ts
├── remove-skill.ts
└── list-skills.ts
```

over:

```text
application/
└── skill-service.ts
```

when the service file would contain several independently understandable operations.

Do not split mechanically by line count. Tiny, tightly coupled details can remain local when extracting them would increase navigation cost.

## Avoid directory-per-file ceremony

Prefer:

```text
mcp/
├── list-skills-tool.ts
├── install-skill-tool.ts
└── remove-skill-tool.ts
```

instead of creating one directory around every file.

Create a subdirectory when a concept owns multiple supporting files such as tests, fixtures, child components, mappings, or protocol-specific helpers.

## Naming

Use names that describe domain or application intent:

```text
install-skill.ts
skill-store.ts
filesystem-skill-store.ts
github-skill-source.ts
install-skill-tool.ts
```

Avoid vague buckets and names such as:

```text
manager.ts
service.ts
helper.ts
common.ts
utils.ts
misc.ts
```

unless the qualifier makes the responsibility precise.

Use the project's naming convention consistently. In file-based Node projects, kebab-case filenames are preferred when no stronger existing convention exists.

## Imports and exports

Prefer explicit module boundaries.

- Import from the module that owns a contract.
- Avoid deep imports into another capability's implementation details.
- Avoid barrel files that hide ownership or create dependency cycles.
- Use a small public `index.ts` only when a module intentionally exposes a public surface and the indirection improves navigation.
- Keep side-effect imports rare and obvious.
- Use `import type` when the distinction materially improves runtime/dependency clarity.

## Ownership beats syntax category

Do not create repository-wide buckets for TypeScript syntax:

```text
src/
├── types/
├── interfaces/
├── models/
└── utils/
```

Instead keep definitions with their owner:

```text
domain/
├── skill.ts
└── skill-source.ts

application/
├── install-skill.ts
└── ports/
    └── skill-store.ts

infrastructure/
└── mcp/
    └── install-skill-input.ts
```

Promote code outward only after ownership genuinely becomes shared.
