# Modules and Files

Apply `$semantic-organization` for grouping and splitting decisions. This reference covers TypeScript-specific module/file conventions.

## Semantic modules

A TypeScript file or module may expose multiple functions, types, or methods when they belong to one coherent concept.

For example, a registry may naturally expose:

```text
register
unregister
find
list
refresh
```

from one `skill-registry.ts` module or class.

Do not split each operation into a separate file merely to reduce file size. Split when semantic ownership diverges or a concept grows into independently meaningful sub-concepts.

## Naming

Use names that reveal the concept or capability:

```text
skill-registry.ts
repository-source.ts
filesystem-skill-store.ts
mcp-server.ts
repository-url.ts
```

Avoid vague buckets such as:

```text
helper.ts
common.ts
utils.ts
misc.ts
general-service.ts
```

unless the qualifier genuinely describes one coherent semantic unit.

Use the project's naming convention consistently. In file-based Node projects, kebab-case filenames are preferred when no stronger existing convention exists.

## Classes and function modules

Use whichever representation makes the semantic owner clearest.

A class is natural when a concept owns state, dependencies, identity, or lifecycle.

A cohesive module of functions is natural for stateless behavior such as:

```text
repository-url.ts
├── parse
├── normalize
└── isSupported
```

Do not introduce classes solely to imitate Java syntax, and do not avoid classes merely because equivalent functions are possible.

## Imports and exports

Prefer explicit module boundaries.

- Import from the module that owns a contract.
- Avoid deep imports into another capability's implementation details.
- Avoid barrel files that hide ownership or create dependency cycles.
- Use a small public `index.ts` only when a module intentionally exposes a public surface and the indirection improves navigation.
- Keep side-effect imports rare and obvious.
- Use `import type` when the distinction materially improves runtime/dependency clarity.

## Ownership beats syntax category

Do not create repository-wide buckets merely for TypeScript syntax:

```text
src/
├── types/
├── interfaces/
├── models/
└── utils/
```

Instead keep definitions with the concept, capability, contract, or architectural boundary that owns them.

Promote code outward only after ownership genuinely becomes shared.
