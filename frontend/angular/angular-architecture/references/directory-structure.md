# Angular Directory Structure

Use a domain-first, vertical-feature structure. Optimize the filesystem for ownership clarity and low navigation cost.

## Top-level shape

```text
apps/
└── <app>/
    └── ...thin application shell...

libs/
├── <domain>/
│   ├── features/
│   │   ├── <feature-a>/
│   │   └── <feature-b>/
│   └── shared/
│       ├── components/
│       ├── data-access/
│       └── util/
└── shared/
    ├── components/
    └── util/
```

Do not expose repetitive `src/lib` nesting as part of the semantic architecture. Keep project paths as shallow and ownership-oriented as the workspace permits.

## Feature ownership

A feature is the vertical slice for one user-facing capability. Everything used exclusively by that feature belongs inside its feature directory, regardless of whether it is UI, state, API access, mapping, types, or helper logic.

Keep the feature's primary screen/container files at the feature root:

```text
libs/jobs/features/discovery/
├── discovery.ts
├── discovery.html
├── discovery.spec.ts
├── discovery.routes.ts
├── components/
├── data-access/
└── util/
```

Do not add another `discovery/` directory around the main feature files.

### `components/`

Use for secondary components owned only by the feature:

```text
components/
├── filters/
│   ├── filters.ts
│   ├── filters.html
│   └── filters.spec.ts
└── result-list/
    ├── result-list.ts
    ├── result-list.html
    └── result-list.spec.ts
```

Do not move a component to shared merely because it is visually reusable in theory. Keep it feature-local until another feature actually needs the same application-level responsibility.

### `data-access/`

Use for feature-owned data/state concerns such as:

- HTTP/API clients and feature-specific backend calls;
- server DTOs and API mapping;
- feature stores/signals/state coordination;
- feature-local caching or browser persistence;
- query/load orchestration tied only to this feature.

Example:

```text
data-access/
├── discovery-api.ts
├── discovery.store.ts
├── discovery.models.ts
└── discovery.mapper.ts
```

Do not put visual components or templates in `data-access/`.

### `util/`

Use only for pure helpers owned by the feature. Do not create the directory until needed. Keep HTTP, Angular state, services, and components out of it.

## Promotion to shared

Placement follows actual reuse:

```text
one feature owns it
→ <domain>/features/<feature>/...

multiple features in the same domain use it
→ <domain>/shared/...

multiple domains genuinely use it
→ libs/shared/...
```

Move code when ownership changes; do not duplicate it across features.

## Domain-shared structure

Code shared by multiple features of one domain remains inside that domain:

```text
libs/jobs/shared/
├── components/
│   └── job-card/
├── data-access/
│   └── jobs-api.ts
└── util/
```

Domain-shared components may speak domain vocabulary such as `Job`, `Salary`, or `ApplicationStatus`.

## Global shared

`libs/shared/` is only for genuinely domain-neutral code:

```text
libs/shared/
├── components/
└── util/
```

Use `shared/components/` for generic application UI/design-system components, including Spartan-derived primitives owned by the application. Use `$angular-ui` for their reuse/styling policy.

Do not create global `models/`, `services/`, `stores/`, or catch-all `common/` directories. Keep types and services with the behavior/contract that owns them.

## Creation rule

Start with the minimum real structure. A small feature may contain only:

```text
features/detail/
├── detail.ts
├── detail.html
└── detail.spec.ts
```

Add subdirectories only when the feature actually gains those concerns. Architecture must reduce navigation ambiguity, not manufacture folder depth.