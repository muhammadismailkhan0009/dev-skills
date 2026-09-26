---
name: semantic-organization
description: Organize code by semantic ownership and structural locality so related behavior is easy to find and understand. Use across languages and frameworks when deciding how concepts should be grouped into classes, modules, files, directories, packages, or namespaces.
---

# Semantic Organization

Organize code by meaning, not by arbitrary file size, function count, or a preference for classes versus functions.

A semantic unit may contain multiple related operations when they belong to the same concept. Keep those operations together. Split code when one unit starts owning independently meaningful concepts that can be named and understood separately.

Use the target language's natural structural mechanisms. A semantic unit may be represented by a class, module, file, directory, package, namespace, or a cohesive group of functions. Do not force object-oriented structure where the language or problem does not benefit from it.

Read:
- [semantic grouping](references/semantic-grouping.md) for deciding what belongs together and when to split.
- [structure and navigation](references/structure-and-navigation.md) for filesystem grouping, locality, naming, and low-cognitive-load navigation.

Optimize for this question:

> If I know the concept, can I predict where its behavior belongs?

Prefer explicit semantic names over generic catch-all buckets. Avoid unnecessary fragmentation: related behavior should not be scattered across many files merely to keep files small.

This skill governs code organization within whatever architecture the project uses. It does not decide architectural layers, transport boundaries, framework conventions, or dependency direction; use the relevant architecture/framework skill for those decisions.
