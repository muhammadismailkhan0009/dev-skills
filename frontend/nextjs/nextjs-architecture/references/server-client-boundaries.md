# Next.js Server/Client Boundaries

Use current, version-matched Next.js documentation as authority for framework behavior. Prefer the docs bundled with the installed `next` package and current Next.js runtime tooling over remembered APIs.

## Default to Server Components

With the App Router, treat components as server-capable by default. Add `'use client'` only when the component genuinely needs browser-only behavior such as:

- React client state or effects;
- DOM/browser APIs;
- event handlers requiring client execution;
- client-only libraries;
- interactive state that cannot remain below the current boundary.

Do not add `'use client'` to a page, layout, feature root, or shared component merely because one descendant is interactive. Extract the smallest interactive child instead.

```text
Server feature/page
├── server-rendered content
└── Client interactive component
```

Keep the client graph as small as practical.

## Data fetching

Prefer server-side data access when the data is needed for initial rendering and does not require browser lifecycle/state. Keep credentials, service tokens, filesystem access, database access, and server-only dependencies outside client modules.

Use client-side fetching/state when the behavior genuinely depends on browser interaction, live client state, optimistic UI, polling, or another client requirement.

Do not fetch the same data independently on server and client without a specific reason.

Feature-owned API calls and mappings belong in the feature's `data-access/` area. Use `.server.*` or `.client.*` suffixes when they make the runtime boundary materially clearer.

## Server Actions

Treat Server Actions as framework entry/adaptor functions, not as a replacement for feature structure.

A Server Action may:

- validate/normalize action input;
- call feature-owned server data/application logic;
- trigger supported cache/revalidation/navigation behavior;
- return the action result expected by the UI.

Do not accumulate unrelated business rules, transport mappings, or large orchestration directly in action files merely because the action runs on the server.

Keep secrets and server-only dependencies behind server-only modules.

## Route Handlers

Create `route.ts` only when the Next.js application genuinely owns an HTTP endpoint or backend-for-frontend concern.

When the product already has a dedicated backend API, do not create redundant Next.js proxy endpoints merely to hide normal frontend API calls. A Route Handler/BFF is justified when the frontend server must own concerns such as:

- server-only credentials;
- secure cookie/session mediation;
- response aggregation/transformation that belongs to the web application;
- webhooks or Next.js-owned endpoints;
- a deliberate same-origin backend-for-frontend boundary.

Keep domain business logic in the owning backend/domain layer rather than silently moving it into Next.js.

## Serializable boundaries

When a Server Component passes data to a Client Component, keep the boundary explicit and pass data compatible with the supported React/Next.js serialization model. Do not pass server-only objects, live database handles, request objects, or non-transferable implementation details into client components.

## Shared components

Do not mark global shared UI as client-only by default. If a primitive/component needs client behavior, that component may own the boundary, but server-safe shared components should remain usable from Server Components.

Avoid convenience barrel files that accidentally pull server-only and client-only modules into the same import surface.

## Framework knowledge and runtime verification

When available:

- use the installed Next.js version's bundled documentation under `node_modules/next/dist/docs/`;
- respect project-generated Next.js agent guidance such as `AGENTS.md` / `CLAUDE.md` when present;
- use `next-devtools-mcp` / the running Next.js MCP endpoint for runtime errors, route state, Server Actions, logs, and framework diagnostics;
- use official Next.js workflow skills such as `next-dev-loop` when installed and relevant.

Do not copy changing Next.js API documentation into this repository skill. This skill owns architectural policy; Next.js owns current framework behavior.