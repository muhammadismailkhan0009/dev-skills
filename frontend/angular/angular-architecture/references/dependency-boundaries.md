# Angular Dependency Boundaries

Use ownership boundaries to keep features isolated and shared code reusable without turning `shared/` into a dumping ground.

All paths in this reference are relative to the actual frontend application root. `libs/...` means `<frontend-root>/libs/...`; never interpret it as a repository-root sibling of the frontend application.

## Direction

```text
<frontend-root>/src/app
   ↓
<frontend-root>/libs/<domain>/features
   ↓
<frontend-root>/libs/<domain>/shared
   ↓
<frontend-root>/libs/shared
```

A lower/shared layer must never depend back on a feature that consumes it.

## Feature rules

A feature may depend on:

- files inside the same feature;
- its own domain's `shared/` code;
- global `<frontend-root>/libs/shared/` code;
- explicitly public cross-domain contracts when such coupling is intentional.

A feature must not import another feature's internal files directly.

```text
<frontend-root>/libs/jobs/features/discovery
  ✗→ <frontend-root>/libs/jobs/features/detail/internal-component
```

If two features need the same responsibility, promote that responsibility to the domain's `shared/` area rather than importing one feature from another.

## Domain-shared rules

`<frontend-root>/libs/<domain>/shared/` may depend on:

- other coherent code inside the same domain-shared area;
- global shared code.

It must not depend on any domain feature:

```text
<frontend-root>/libs/jobs/shared
  ✗→ <frontend-root>/libs/jobs/features/discovery
```

Domain-shared code may remain domain-aware. Do not promote it globally merely to make an import convenient.

## Global shared rules

`<frontend-root>/libs/shared/` must remain domain-neutral.

```text
<frontend-root>/libs/shared/components
  ✗→ jobs
  ✗→ auth
  ✗→ applications
```

Global shared components/utilities must not acquire business-domain dependencies.

## App shell

`<frontend-root>/src/app/` may compose feature entry points, root routes, providers, application configuration, and shell-level concerns. Keep business behavior, feature state, feature data access, and feature-specific components out of the app shell.

## Cross-domain access

Do not reach into another domain's internals. When one domain genuinely needs another domain's capability, expose a deliberate public contract or compose the domains at an owning feature/app boundary.

Do not create broad shared services merely to bypass domain boundaries.

## Types follow ownership

Do not centralize TypeScript interfaces into a global `models/` directory. Keep DTOs, view types, state types, and domain-specific contracts with the feature/data-access/shared area that owns them. Promote a type only when its ownership truly broadens.

## Enforcement

When the frontend workspace uses Nx boundary tags or equivalent lint rules, encode these directions so invalid imports fail automatically rather than relying only on prose. Keep enforcement aligned with the actual domain/feature/shared ownership model; do not introduce extra architectural layers solely for lint configuration.