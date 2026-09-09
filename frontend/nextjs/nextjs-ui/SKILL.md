---
name: nextjs-ui
description: Build Next.js/React UI with reusable application components, Tailwind CSS v4, and shadcn/ui. Use for screens, feature UI, shared components, styling, or UI primitives; prefer existing/shared and shadcn components over handcrafted primitives.
---

# Next.js UI

Build Next.js screens by composition, not by recreating UI primitives inside each feature.

Resolve the actual frontend application root before installing, generating, or locating UI code. shadcn commands and generated components belong to that frontend application, not to an unrelated repository root. Use `$nextjs-architecture` for ownership and physical placement.

For Next.js UI work, read [shadcn UI rules](references/shadcn-ui.md). The project UI stack is Next.js/React + Tailwind CSS v4 + shadcn/ui. Use the official shadcn agent skill, CLI, docs command, and shadcn MCP for current component knowledge when available; do not duplicate or guess current shadcn APIs here.

Reuse in this order:

1. Existing application shared/composed component.
2. Existing installed shadcn component/primitives.
3. Add the missing shadcn component through the official CLI/registry.
4. Create a reusable application component when the UI is application-specific and expected to recur.
5. Keep markup feature-local only when it is genuinely one-off composition.

Do not handcraft standard buttons, inputs, cards, dialogs, menus, tables, badges, selects, tabs, overlays, form controls, or equivalent primitives when an existing application or shadcn component fits.

Prefer Tailwind utilities and the established semantic design tokens over large feature-specific stylesheets. Keep global styling/design-system changes in the shared UI layer rather than overriding the same primitive independently in multiple features.

Before completing a screen, remove duplicated primitive markup/styles, keep client boundaries as small as practical, and extract repeated application-level compositions that now have a clear reusable responsibility.