---
name: typescript-style
description: Write maintainable TypeScript with explicit types, small file-based units, predictable module boundaries, and low cognitive overhead. Use for TypeScript implementation in Node, frontend, libraries, CLIs, MCP servers, or framework-agnostic code.
---

# TypeScript Style

Prefer TypeScript that is easy to navigate and understand from filenames, exported contracts, and local dependencies.

Use Java-style file granularity as a readability bias without copying Java ceremony: one primary responsibility per file by default, explicit domain names, and small cohesive implementation units.

Read:
- [modules and files](references/modules-and-files.md) for file decomposition, naming, imports, exports, and module organization.
- [types and modeling](references/types-and-modeling.md) for interfaces, type aliases, unions, data modeling, and boundary types.
- [errors and async](references/errors-and-async.md) for asynchronous code, error propagation, validation boundaries, and resource cleanup.

Prefer the simplest TypeScript construct that expresses the design:
- plain objects and type aliases for data;
- discriminated unions for closed alternatives and state machines;
- interfaces or structural types for behavioral contracts and ports;
- functions for stateless transformations and orchestration when state is unnecessary;
- classes for stateful resources, lifecycle ownership, or naturally object-oriented behavior.

Do not introduce global catch-all `types/`, `interfaces/`, `models/`, `helpers/`, or `utils/` directories merely to classify syntax. Keep code with the capability, contract, or layer that owns it.

Respect the existing project's module system and compiler settings. For new Node projects, prefer modern ESM-compatible TypeScript unless a compatibility requirement calls for CommonJS.
