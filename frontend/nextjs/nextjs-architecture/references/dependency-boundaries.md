# Next.js Dependency Boundaries

Use ownership boundaries to keep features isolated and shared code reusable without turning `shared/` into a dumping ground.

All paths in this reference are relative to the actual frontend application root. `libs/...` means `<frontend-root>/libs/...`.

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

If two features need the same responsibility, promote it to the domain's `shared/` area rather than importing one feature from another.

## Domain-shared rules

`<frontend-root>/libs/<domain>/shared/` may depend on:

- coherent code inside the same domain-shared area;
- global shared code.

It must not depend on any domain feature.

## Global shared rules

`<frontend-root>/libs/shared/` must remain domain-neutral.

```text
<frontend-root>/libs/shared/components
  ✗→ jobs
  ✗→ auth
  ✗→ applications
```

Global shared components/utilities must not acquire business-domain dependencies.

## App Router shell

`<frontend-root>/src/app/` may depend on feature entry points and shared code because it is the outer composition/routing layer.

Do not reverse this dependency. Domain features should not import route files, route groups, layouts, or other `src/app/` internals. If framework-specific information must enter a feature, pass it through props/contracts or an explicit adapter at the route boundary.

## Cross-domain access

Do not reach into another domain's internals. When one domain genuinely needs another domain's capability, expose a deliberate public contract or compose the domains at an owning feature/app boundary.

Do not create broad shared services merely to bypass domain boundaries.

## Types follow ownership

Do not centralize TypeScript interfaces into a global `models/` directory. Keep DTOs, view types, state types, and domain-specific contracts with the feature/data-access/shared area that owns them. Promote a type only when its ownership truly broadens.

## Server/client constraints are also dependency constraints

A client module must never import server-only code, secrets, filesystem/database access, or server-only dependencies. Server modules may compose client components through supported React/Next.js boundaries, but do not make shared modules client-only merely for convenience.

Use [server/client boundaries](server-client-boundaries.md) when runtime ownership is involved.

## Enforcement

When path aliases, ESLint boundaries, package rules, or equivalent tooling can encode these directions, prefer enforceable rules over prose. Keep enforcement aligned with the actual domain/feature/shared model; do not introduce extra architectural layers solely for lint configuration.