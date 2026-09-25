# Runtime Boundaries

Node applications can have many runtime shapes. Treat them consistently.

## `main.ts`: process bootstrap

`main.ts` answers:
- what runtime starts;
- what concrete adapters are constructed;
- how dependencies are wired;
- how startup/shutdown is owned;
- what top-level failure policy applies.

Keep it boring.

Typical flow:

```text
process starts
→ load/validate configuration
→ construct infrastructure adapters
→ construct application operations
→ construct/register inbound entrypoints
→ start runtime
→ own shutdown/top-level error handling
```

Do not implement business behavior in `main.ts`.

## CLI

A CLI command is an inbound entrypoint, equivalent to a web controller.

```text
shell / npx
→ CLI runtime
→ command handler
→ application use case
→ domain / output ports
```

CLI entrypoints own:
- argument/option parsing;
- CLI-specific validation;
- mapping to application input;
- terminal formatting;
- exit-code mapping.

Keep command handlers thin. Do not make Commander/yargs/other parser types part of the application API.

## MCP

An MCP tool or other behavior-triggering MCP handler is an inbound entrypoint.

```text
MCP client
→ MCP transport/server
→ tool handler
→ application use case
→ domain / output ports
```

Keep MCP SDK request/response types at the entrypoint boundary.

If the application also acts as an MCP client toward another system, that client is outbound infrastructure instead:

```text
application port
→ infrastructure/mcp/<client-adapter>
→ remote MCP server
```

The same protocol can therefore appear on either side; direction determines placement.

## HTTP

HTTP handlers/controllers are inbound entrypoints.

Keep framework request/response objects out of application/domain code. Map and delegate at the boundary.

## Events and queues

A message/event consumer is an inbound entrypoint.

```text
broker/event
→ consumer handler
→ application operation
```

Broker clients used to publish outbound messages are infrastructure implementations of application ports.

Keep acknowledgement/retry/dead-letter mechanics in the runtime/infrastructure boundary unless application semantics explicitly require them.

## Scheduled work

A cron/scheduler callback is an inbound entrypoint.

```text
scheduler tick
→ scheduled handler
→ application operation
```

The schedule expression/runtime registration belongs to the entrypoint/runtime boundary. The operation itself belongs to application.

## Workers and job processors

A worker process still has:
- a process bootstrap (`main.ts` or a dedicated process entry);
- a runtime host;
- job handlers as application entrypoints.

If a package intentionally has multiple executable processes, make each process bootstrap explicit, for example:

```text
src/
├── main.ts
├── worker-main.ts
└── ...
```

or a clear `src/processes/` directory when several exist. Do not hide process startup inside arbitrary implementation modules.

## Filesystem watchers and streams

External events from a watcher, stdin stream, socket, or similar source enter through an entrypoint handler.

The adapter translating raw runtime events to application calls belongs at the boundary; domain/application code should not depend on Node event-emitter, stream, or watcher implementation types unless the runtime abstraction is intentionally part of the application contract.

## Stdout and stderr

For CLI programs, stdout/stderr are protocol surfaces.

- Put intended command output on stdout.
- Put diagnostics/logging on stderr when stdout may be machine-consumed.
- For stdio MCP servers, never pollute protocol stdout with logs; route diagnostics to stderr or configured logging.

## Configuration and environment

Read environment variables and config files at startup/boundaries. Validate them once and pass typed configuration inward.

Do not scatter `process.env` access through application/domain code.

## Signals and shutdown

The process/composition boundary owns OS signals and orderly shutdown.

Long-lived resources should expose an explicit close/stop lifecycle when necessary. Shutdown may close:
- MCP transports;
- HTTP servers;
- database pools;
- sockets;
- child processes;
- file watchers.

Do not make domain behavior responsible for process signals.

## Multiple runtimes over one application

A Node package may expose the same application capability through several runtimes:

```text
CLI command ─┐
MCP tool ────┼──→ application use case
HTTP route ──┘
```

This is desirable when the capability is genuinely the same. Keep runtime-specific concerns in each entrypoint and reuse the application operation.
