---
name: angular-architecture
description: Structure Angular/Nx frontends by business domain and vertical feature ownership. Use when creating, moving, reviewing, or organizing Angular features, shared code, data access, components, routes, or cross-feature dependencies.
---

# Angular Architecture

Organize Angular code by ownership: domain first, then feature. Keep each feature as a vertical slice containing everything exclusively owned by that feature.

- For physical layout, ownership, promotion to shared, and feature subdirectories, read [directory structure](references/directory-structure.md).
- For allowed dependency direction, feature isolation, domain-shared/global-shared boundaries, and cross-domain access, read [dependency boundaries](references/dependency-boundaries.md).

Keep the deployable Angular app thin: bootstrap, root configuration/providers, top-level routing, and global styles belong in the app; feature behavior belongs under domain libraries.

Use standalone Angular for new code. Do not introduce NgModule-oriented structure for new features unless an existing project constraint requires it.

Do not create empty architectural directories in advance. Add `components/`, `data-access/`, `util/`, or shared areas only when real code needs them.

When UI primitives or styling are involved, also use `$angular-ui`; architecture decides ownership and placement, while `$angular-ui` decides component reuse and Spartan/Tailwind rules.