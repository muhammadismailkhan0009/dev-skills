---
name: nextjs-architecture
description: Structure Next.js App Router frontends by business domain and vertical feature ownership. Use when creating, moving, reviewing, or organizing routes, features, shared code, data access, components, server/client boundaries, or cross-feature dependencies.
---

# Next.js Architecture

Organize Next.js code by ownership: domain first, then feature. Keep each feature as a vertical slice containing everything exclusively owned by that feature.

All architecture paths in this skill are relative to the actual frontend application root. Never create repository-root frontend directories merely because this skill is active.

- For physical layout, route composition, feature ownership, promotion to shared, and feature subdirectories, read [directory structure](references/directory-structure.md).
- For allowed dependency direction, feature isolation, domain-shared/global-shared boundaries, and cross-domain access, read [dependency boundaries](references/dependency-boundaries.md).
- For App Router, Server Components, Client Components, Server Actions, Route Handlers, and data-access placement, read [server/client boundaries](references/server-client-boundaries.md).

Use the App Router for new code unless the existing project is intentionally Pages Router. Keep `<frontend-root>/src/app/` thin: Next.js route files, layouts, loading/error boundaries, metadata, providers, and route composition belong there; business feature implementation belongs under `<frontend-root>/libs/<domain>/...`.

Prefer Server Components by default. Add `'use client'` only at the smallest component boundary that genuinely needs browser state, effects, event handlers, or client-only APIs.

Do not create empty architectural directories in advance. Add `components/`, `data-access/`, `util/`, server/client-specific files, or shared areas only when real code needs them.

Use version-matched Next.js documentation when framework behavior matters. Prefer the docs bundled with the installed `next` package and Next.js runtime tooling over remembered APIs. When available, use the official Next.js MCP/dev-loop tooling for runtime verification rather than guessing from source alone.

When UI primitives or styling are involved, also use `$nextjs-ui`; architecture decides ownership and placement, while `$nextjs-ui` decides component reuse and shadcn/Tailwind rules.

When client interaction has meaningful orchestration—multiple phases, branching transitions, async retry/error/success sequencing, shared journey state, or coordination between independent flows—also use `$uiflow`. Do not select `$uiflow` for ordinary local component state or simple handlers where plain React/Next.js is clearer.
