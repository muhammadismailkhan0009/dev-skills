# shadcn UI Rules

Use this reference for Next.js screen, shared-component, primitive, and styling work.

## Stack baseline

Use:

- Next.js / React
- Tailwind CSS v4
- shadcn/ui
- the official `shadcn/ui` agent skill when available
- the official shadcn MCP server when the current agent supports MCP

shadcn owns current component/API/registry knowledge. This skill owns project-level reuse, composition, and placement policy. Do not copy changing shadcn component documentation into this repository skill.

All setup, inspection, generation, and component placement must be scoped to the actual frontend application root. In a repository that also contains backend or other applications, do not initialize shadcn from the repository root unless that root is itself the Next.js application.

## Mandatory UI workflow

Before creating or styling feature UI:

1. Resolve the actual frontend application root.
2. Inspect existing application shared/composed UI that could satisfy the requirement.
3. Inspect current shadcn project state and `components.json`; do not guess aliases, style/base, installed components, or registry configuration.
4. When available, use the official `shadcn/ui` agent skill and current shadcn CLI/MCP/docs to retrieve component knowledge.
5. Prefer an existing application component when it already expresses the application-level responsibility.
6. Otherwise prefer an already-installed shadcn component.
7. If the required standard primitive/component exists in shadcn but is not installed, add it through the official CLI/registry instead of reimplementing it.
8. Create a new application shared/composed component only when the behavior or visual composition is application-specific and likely to recur.
9. Keep markup local to a feature only when it is genuinely one-off composition.

Do not recreate standard UI primitives in feature markup/CSS when shadcn or an existing shared component provides them.

## Current shadcn knowledge

Do not rely on remembered shadcn APIs when a current source is available.

The official agent skill can be installed with the current skills CLI, for example:

```bash
pnpm dlx skills add shadcn/ui
```

Useful current shadcn commands include:

```bash
pnpm dlx shadcn@latest info
pnpm dlx shadcn@latest docs <component>
pnpm dlx shadcn@latest search @shadcn -q "<query>"
pnpm dlx shadcn@latest add <component>
```

The shadcn MCP server can browse/search configured registries and install components. When configured, prefer it for current registry/component discovery instead of inventing component APIs.

Treat `components.json` as authoritative for project aliases and component destinations. Do not force a hard-coded `src/components/ui` location when the project deliberately points shadcn at the architecture's shared UI directory.

## Project setup

Run setup commands from `<frontend-root>`.

Do not reinstall or reinitialize an already-configured frontend. For first-time setup, use the current official shadcn workflow for the installed Next.js/Tailwind versions.

Typical initialization:

```bash
cd <frontend-root>
pnpm dlx shadcn@latest init
```

Before accepting generated paths, ensure `components.json` aliases align with `$nextjs-architecture`. For this architecture, generic application primitives normally belong under the frontend's global shared UI area, e.g. `<frontend-root>/libs/shared/components/ui/`, unless the existing project already has an established equivalent convention.

Do not create repository-root component/library directories merely because a generator accepts configurable output paths.

## Reuse and component ownership

A feature screen should primarily compose reusable primitives and application components.

Examples:

```text
Button / Dialog / Select
→ global shadcn/shared UI primitive

JobCard / SalaryBadge
→ jobs/shared/components

DiscoveryFilters used only by discovery
→ jobs/features/discovery/components
```

Do not move domain-aware components into global shared UI simply because they are visually reusable.

## Styling rules

- Use Tailwind CSS v4 and the project's semantic theme/design tokens as the normal styling mechanism.
- Prefer modifying the owned shadcn component/design-system layer when a change belongs to the global primitive rather than overriding it separately in multiple features.
- Avoid large feature-specific CSS files that duplicate utility classes or primitive styles.
- Do not create screen-local button/input/card/etc. styling that should live in a shared/shadcn component.
- Do not add arbitrary one-off values when an existing semantic token or established spacing/color/typography convention fits.
- Keep global CSS focused on theme/base concerns rather than feature styling.

## Server/client boundaries

Do not add `'use client'` merely because a shadcn component is used. Preserve Server Components wherever possible and let the interactive primitive/component own the smallest necessary client boundary.

Do not make a whole page, layout, or feature client-rendered just to use one interactive control. Use `$nextjs-architecture` server/client boundary rules.

## Accessibility and interactive behavior

Prefer the supported shadcn primitive implementation for standard interaction, keyboard behavior, focus management, ARIA semantics, dialogs, menus, popovers, selects, and overlays rather than recreating those behaviors manually.

## Completion check

Before considering UI work complete:

- verify all UI work remained under the actual frontend application root;
- verify existing shared components were reused where appropriate;
- verify standard primitives use shadcn rather than local reinventions;
- verify newly added components came through the supported CLI/registry/current project convention;
- verify `components.json` aliases and generated paths respect `$nextjs-architecture`;
- remove duplicated primitive markup/styles;
- keep feature-specific styling minimal;
- keep `'use client'` boundaries as small as practical;
- use current shadcn skill/MCP/CLI/docs rather than guessed APIs.