# Dependency Boundaries

The architecture separates inbound invocation from outbound implementation.

## `entrypoints`

Inbound adapters. They receive an external event and invoke application behavior.

Examples:
- CLI commands;
- MCP tools/resources/prompts when they trigger behavior;
- HTTP handlers/controllers;
- queue/event consumers;
- scheduled-task handlers;
- worker job handlers;
- filesystem watcher callbacks.

Entrypoints may:
- parse and validate transport input;
- authenticate/authorize when that concern belongs to the transport boundary;
- map transport data to application input;
- invoke one application operation or a small explicit orchestration boundary;
- map the result to transport output/exit code/protocol response.

Entrypoints must not own core business rules, persistence policy, vendor-specific workflow, or multi-step application orchestration.

## `application`

Own use cases and orchestration.

Application code may:
- sequence domain operations;
- coordinate output ports;
- define transaction/work boundaries;
- choose application-level branching and policy;
- return stable application results.

Application defines output ports for capabilities it needs from the outside world.

Examples:

```text
SkillStore
RemoteSkillSource
ProcessLauncher
Clock
RegistryClient
```

Application must not import concrete filesystem, database, HTTP client, MCP SDK, CLI parser, or vendor implementation types.

## `domain`

Own business concepts, rules, invariants, and behavior that make sense independently of Node/runtime libraries.

Domain depends on no outer layer.

Not every CLI/tool requires a rich domain. If the program is primarily orchestration with no meaningful business rules, keep it simple instead of inventing domain objects.

## `infrastructure`

Outbound adapters and technical integrations used by the application.

Examples:
- filesystem;
- database;
- HTTP/network clients;
- GitHub or other vendor APIs;
- child processes;
- sockets/WebSockets;
- persistence;
- external MCP clients.

Infrastructure implements application-owned ports where a stable inward-facing contract is useful.

Keep SDK/vendor models inside infrastructure. Map them to application/domain types at the boundary.

## Dependency direction

Allowed direction:

```text
entrypoints ───────→ application ───────→ domain
                         │
                         │ owns ports
                         ▼
                   infrastructure
                   implements ports
```

At compile/import level, infrastructure may depend inward on application/domain contracts. Application does not depend on infrastructure implementations.

The composition root (`main.ts`) is allowed to know concrete implementations because its job is wiring.

## Cross-entrypoint reuse

Do not duplicate application logic when the same capability is exposed through multiple transports.

Example:

```text
CLI install command ─┐
                     ├──→ InstallSkill
MCP install tool ────┤
                     │
HTTP endpoint ───────┘
```

Each entrypoint owns only transport mapping. `InstallSkill` owns the operation.

## Boundary review

For any externally triggered behavior, trace:

```text
entrypoint
→ application operation
→ domain behavior
→ output port
→ infrastructure adapter
```

Check:
- the entrypoint is thin;
- orchestration is in application;
- domain contains no runtime/vendor dependency;
- application imports no concrete infrastructure;
- protocol/vendor types do not leak inward;
- the path is obvious from filenames and directories;
- no generic service/helper layer obscures the flow.
