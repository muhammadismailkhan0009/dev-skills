---
name: angular-ui
description: Build Angular UI with reusable application components, Tailwind CSS v4, and spartan/ui. Use for screens, feature UI, shared components, styling, or UI primitives; prefer existing/shared and Spartan components over handcrafted HTML/CSS.
---

# Angular UI

Build Angular screens by composition, not by recreating UI primitives inside each feature.

Resolve the actual frontend application root before installing, generating, or locating UI code. Angular/Spartan commands and generated components belong to that frontend application, not to an unrelated repository root. Use `$angular-architecture` for ownership and physical placement.

For Angular UI work, read [Spartan UI rules](references/spartan-ui.md). The project UI stack is Angular + Tailwind CSS v4 + spartan/ui. Use the official `$spartan` agent skill and Spartan MCP/CLI for current component knowledge when available; do not duplicate or guess Spartan APIs here.

Reuse in this order:

1. Existing application shared/composed component.
2. Existing installed Spartan Helm component.
3. Add the missing Spartan component through the official CLI.
4. Create a reusable application component when the UI is application-specific and expected to recur.
5. Keep markup feature-local only when it is genuinely one-off composition.

Do not handcraft standard buttons, inputs, cards, dialogs, menus, tables, badges, selects, tabs, overlays, or other primitives when an existing application or Spartan component fits.

Prefer Tailwind utilities and the established design tokens over large feature-specific stylesheets. Component CSS is for styling that cannot be expressed cleanly through the established Tailwind/design-system conventions, not the default way to reproduce a screen.

Before completing a screen, remove duplicated primitive markup/styles and extract repeated application-level compositions that now have a clear reusable responsibility.