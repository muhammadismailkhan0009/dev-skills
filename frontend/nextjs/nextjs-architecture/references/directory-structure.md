# Next.js Directory Structure

Use a domain-first, vertical-feature structure. Optimize the filesystem for ownership clarity and low navigation cost.

## Frontend root

First identify the actual Next.js application root. All paths in this reference are relative to that directory.

Preferred shape:

```text
<frontend-root>/
├── src/
│   └── app/
│       ├── layout.tsx
│       ├── page.tsx
│       └── ...thin route composition...
│
├── libs/
│   ├── <domain>/
│   │   ├── features/
│   │   │   ├── <feature-a>/
│   │   │   └── <feature-b>/
│   │   └── shared/
│   │       ├── components/
│   │       ├── data-access/
│   │       └── util/
│   └── shared/
│       ├── components/
│       └── util/
│
├── public/
├── package.json
├── next.config.*
└── ...frontend configuration...
```

If the repository contains `frontend/` as the Next.js application root, use `frontend/libs/...`, never a sibling repository-root `libs/...`.

## `src/app/` is the routing boundary

Use `src/app/` for Next.js framework entry points and route composition:

- `page.tsx`, `layout.tsx`, `template.tsx`;
- `loading.tsx`, `error.tsx`, `not-found.tsx`;
- route groups and route segments;
- metadata and framework-level providers;
- `route.ts` only when the Next.js application genuinely owns an HTTP endpoint.

Keep route files thin. They should select/compose the owning feature and provide route-specific framework concerns, not become the feature implementation directory.

Example:

```text
<frontend-root>/src/app/(app)/jobs/page.tsx
                         │
                         └── composes/imports
                             <frontend-root>/libs/jobs/features/discovery/
```

Do not duplicate a full feature implementation under `src/app/` merely because the URL has the same name.

## Feature ownership

A feature is the vertical slice for one user-facing capability. Everything used exclusively by that feature belongs inside its feature directory, regardless of whether it is UI, state, API access, mapping, types, server logic, or helper logic.

Keep the feature's primary composition component at the feature root:

```text
<frontend-root>/libs/jobs/features/discovery/
├── discovery.tsx
├── discovery.test.tsx
├── components/
├── data-access/
└── util/
```

Do not add another `discovery/` directory around the main feature files.

### `components/`

Use for secondary React components owned only by the feature:

```text
components/
├── filters/
│   ├── filters.tsx
│   └── filters.test.tsx
└── result-list/
    ├── result-list.tsx
    └── result-list.test.tsx
```

Keep a component feature-local until another feature actually needs the same application-level responsibility.

### `data-access/`

Use for feature-owned data/state concerns such as:

- backend API calls and transport mapping;
- server DTOs and API mapping;
- feature-local query/cache logic;
- client state tied only to this feature;
- server-side loaders/actions owned by this feature;
- browser persistence tied only to this feature.

Example:

```text
data-access/
├── discovery-api.server.ts
├── discovery-state.client.ts
├── discovery.models.ts
└── discovery.mapper.ts
```

Use `.server.*` / `.client.*` suffixes when they materially clarify the runtime boundary. Do not manufacture separate server/client folders for tiny features.

### `util/`

Use only for pure helpers owned by the feature. Do not create the directory until needed. Keep React components, HTTP orchestration, server secrets, and stateful services out of it.

## Promotion to shared

Placement follows actual reuse:

```text
one feature owns it
→ <frontend-root>/libs/<domain>/features/<feature>/...

multiple features in the same domain use it
→ <frontend-root>/libs/<domain>/shared/...

multiple domains genuinely use it
→ <frontend-root>/libs/shared/...
```

Move code when ownership changes; do not duplicate it across features.

## Domain-shared structure

```text
<frontend-root>/libs/jobs/shared/
├── components/
│   └── job-card/
├── data-access/
│   └── jobs-api.server.ts
└── util/
```

Domain-shared components may speak domain vocabulary such as `Job`, `Salary`, or `ApplicationStatus`.

## Global shared

`<frontend-root>/libs/shared/` is only for genuinely domain-neutral code:

```text
<frontend-root>/libs/shared/
├── components/
│   └── ui/
└── util/
```

Use global shared components for generic application UI/design-system code, including shadcn-derived primitives owned by the application. Use `$nextjs-ui` for reuse and styling policy.

Do not create global catch-all `models/`, `services/`, `stores/`, or `common/` directories. Keep types and behavior with the contract/feature that owns them.

## Creation rule

Start with the minimum real structure. A small feature may contain only:

```text
<frontend-root>/libs/<domain>/features/detail/
├── detail.tsx
└── detail.test.tsx
```

Add subdirectories only when the feature actually gains those concerns. Architecture must reduce navigation ambiguity, not manufacture folder depth.