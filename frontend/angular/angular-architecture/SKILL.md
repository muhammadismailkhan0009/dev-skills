---
name: angular-architecture
description: Structure Angular frontends by business domain and vertical feature ownership. Use when creating, moving, reviewing, or organizing Angular features, shared code, data access, components, routes, or cross-feature dependencies.
---

# Angular Architecture

Organize Angular code by ownership: domain first, then feature. Keep each feature as a vertical slice containing everything exclusively owned by that feature.

All architecture paths in this skill are relative to the actual frontend application root. The frontend root owns both its normal Angular `src/` tree and its `libs/` tree. Never create repository-root `apps/` or `libs/` directories merely because this skill is active.

- For physical layout, ownership, promotion to shared, and feature subdirectories, read [directory structure](references/directory-structure.md).
- For allowed dependency direction, feature isolation, domain-shared/global-shared boundaries, and cross-domain access, read [dependency boundaries](references/dependency-boundaries.md).

Keep `<frontend-root>/src/app/` thin: bootstrap composition, root configuration/providers, top-level routing, and application shell concerns belong there; feature behavior belongs under `<frontend-root>/libs/<domain>/...`.

Use standalone Angular for new code. Do not introduce NgModule-oriented structure for new features unless an existing project constraint requires it.

Do not create empty architectural directories in advance. Add `components/`, `data-access/`, `util/`, or shared areas only when real code needs them.

When UI primitives or styling are involved, also use `$angular-ui`; architecture decides ownership and placement, while `$angular-ui` decides component reuse and Spartan/Tailwind rules.