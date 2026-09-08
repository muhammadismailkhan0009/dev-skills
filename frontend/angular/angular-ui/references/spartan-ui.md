# Spartan UI Rules

Use this reference for Angular screen, shared-component, primitive, and styling work.

## Stack baseline

Use:

- Angular
- Tailwind CSS v4
- spartan/ui
- the official `spartan` agent skill when available
- `@spartan-ng/mcp` when the current agent supports MCP

Spartan owns component/API knowledge. This skill owns project-level reuse and composition policy. Do not copy Spartan component documentation into this repository skill.

All setup, inspection, generation, and component placement must be scoped to the actual frontend application root. In a repository that also contains backend or other applications, do not run Angular/Spartan initialization from the repository root unless that repository root is itself the frontend workspace.

## Mandatory UI workflow

Before creating or styling feature UI:

1. Resolve the actual frontend application root.
2. Inspect existing application shared/composed UI that could satisfy the requirement.
3. Inspect the current Spartan project state. When available, use the official `spartan` skill and its read-only project inspection command (`@spartan-ng/cli:info --json`) rather than guessing installed components, versions, paths, or APIs.
4. Prefer an existing application component when it already expresses the application-level responsibility.
5. Otherwise prefer an already-installed Spartan Helm component.
6. If the required standard primitive exists in Spartan but is not installed, add it through the official Spartan CLI instead of reimplementing it.
7. Create a new application shared/composed component only when the behavior or visual composition is application-specific and likely to recur.
8. Keep markup local to a feature only when it is genuinely one-off composition.

Do not recreate standard UI primitives in feature markup/CSS when Spartan or an existing shared component provides them. This includes buttons, inputs, textareas, cards, badges, dialogs, drawers/sheets, dropdowns, selects, tabs, accordions, tooltips, popovers, menus, tables, pagination, form controls, and equivalent primitives.

## Spartan discovery and current APIs

Do not rely on remembered Spartan APIs when a current source is available.

- Use the official `spartan` agent skill for Brain/Helm composition, theming, CLI, forms, icons, and component-specific workflow.
- Use `@spartan-ng/mcp` when configured to retrieve current component documentation, blocks, examples, and API information.
- Use Spartan CLI project inspection before broad UI generation when project state is relevant.
- If the Spartan skill or MCP is unavailable, use the installed component source and official CLI/project configuration as authority rather than inventing an API.

The official agent skill can be installed with:

```bash
npx skills add spartan-ng/spartan
```

The official MCP server is `@spartan-ng/mcp`; agent-specific MCP configuration is outside this skill.

## Project setup

Run setup commands from `<frontend-root>`, meaning the Angular application's own workspace/package root.

Do not reinstall or reinitialize an already-configured frontend. When setting up Spartan for the first time, follow the official CLI workflow appropriate to that frontend workspace.

Typical Angular CLI setup:

```bash
cd <frontend-root>
npm install -D @spartan-ng/cli
ng g @spartan-ng/cli:init
```

Typical Nx setup when the frontend root is an Nx workspace:

```bash
cd <frontend-root>
npm install -D @spartan-ng/cli
npx nx g @spartan-ng/cli:init
```

Add components through the CLI rather than manually recreating their Brain/Helm implementation:

```bash
ng g @spartan-ng/cli:ui <component>
```

or for Nx:

```bash
npx nx g @spartan-ng/cli:ui <component>
```

For machine-readable project inspection use the matching `@spartan-ng/cli:info --json` generator from the same frontend root.

Where generated/copied application UI belongs is governed by `$angular-architecture`. Do not create repository-root UI or library directories merely because a generator has a configurable output path.

## Styling rules

- Use Tailwind CSS v4 and the project's semantic theme/design tokens as the normal styling mechanism.
- Prefer customizing copied Spartan Helm components when the change belongs to the global primitive/design system rather than overriding the same primitive independently in multiple features.
- Avoid large feature-specific CSS files that duplicate utility classes or primitive styles.
- Do not create screen-local button/input/card/etc. styling that should live in a shared or Spartan component.
- Use component CSS only when the required styling cannot be represented cleanly with the established Tailwind/design-system approach or when the project already has a justified local-style convention for that case.
- Do not add arbitrary one-off values when an existing semantic token or established spacing/color/typography convention fits.

## Component boundaries

A feature screen should primarily compose reusable primitives and application components.

Extract a shared application component when repeated markup has a stable application-level responsibility, for example a job summary card, filter bar, empty-state panel, page header, or account menu. Do not extract trivial wrappers merely to increase component count.

Keep business/data orchestration in the owning Angular feature/container layer. Shared UI primitives and presentational components should not acquire unrelated feature-specific state or service dependencies merely for reuse.

## Accessibility and interactive behavior

Prefer Spartan Brain primitives for standard interactive behavior so keyboard interaction, focus management, ARIA behavior, and overlays are not recreated manually. Do not replace an accessible Spartan primitive with custom HTML/JavaScript solely to match a visual design.

## Completion check

Before considering UI work complete:

- verify all UI work remained under the actual frontend application root;
- verify existing shared components were reused where appropriate;
- verify standard primitives use Spartan rather than local reinventions;
- verify any newly added Spartan component came through the supported CLI/current project convention;
- remove duplicated primitive markup/styles;
- extract only repeated application-level compositions with a clear responsibility;
- keep feature-specific CSS minimal;
- use current Spartan skill/MCP/installed source rather than guessed APIs.