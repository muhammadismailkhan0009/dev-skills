---
name: typescript-style
description: Write maintainable TypeScript with explicit types, idiomatic language constructs, predictable module boundaries, and low cognitive overhead. Use for TypeScript implementation in Node, frontend, libraries, CLIs, MCP servers, or framework-agnostic code.
---

# TypeScript Style

Use `$semantic-organization` with this skill.

Prefer TypeScript that is easy to understand from named concepts, exported contracts, and local dependencies. Use TypeScript idiomatically while preserving clear semantic ownership.

Read:
- [modules and files](references/modules-and-files.md) for TypeScript module naming, imports, exports, and ownership rules.
- [types and modeling](references/types-and-modeling.md) for interfaces, type aliases, unions, data modeling, and boundary types.
- [errors and async](references/errors-and-async.md) for asynchronous code, error propagation, validation boundaries, and resource cleanup.

Prefer the simplest TypeScript construct that expresses the design:
- plain objects and type aliases for data;
- discriminated unions for closed alternatives and state machines;
- interfaces or structural types for behavioral contracts and ports;
- cohesive function modules for stateless behavior;
- classes when state, lifecycle, dependencies, or object semantics make them clearer.

A file, class, or module may contain multiple related operations when they represent one coherent concept. Do not split behavior mechanically by function count or file size; use `$semantic-organization` for grouping and splitting decisions.

Do not introduce global catch-all `types/`, `interfaces/`, `models/`, `helpers/`, or `utils/` directories merely to classify syntax. Keep code with the capability, contract, or semantic area that owns it.

Respect the existing project's module system and compiler settings. For new Node projects, prefer modern ESM-compatible TypeScript unless a compatibility requirement calls for CommonJS.
