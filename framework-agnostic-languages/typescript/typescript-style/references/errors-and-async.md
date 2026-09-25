# Errors and Async

Keep failure and asynchronous control flow explicit.

## Async

- Use `async`/`await` for readable sequential orchestration.
- Run independent operations concurrently only when their independence is clear.
- Do not create detached promises accidentally.
- If work is intentionally backgrounded, give ownership of errors, shutdown, and lifecycle to a named runtime component.
- Keep concurrency policy near the application/runtime layer that owns it rather than burying it in low-level helpers.

## Errors

Distinguish programming/invariant failures from expected operational or domain failures.

- Domain/application code should not depend on transport-specific error classes.
- Convert filesystem, network, SDK, process, database, and protocol failures at the boundary when application code needs a stable semantic failure.
- Do not catch an error merely to log and rethrow it at every layer.
- Catch where you can add meaning, translate the boundary, recover, or own process-level reporting.

For expected alternatives, a typed result/discriminated union may be clearer than exceptions. Do not wrap every operation in a Result type mechanically.

## Validation

Validate untrusted input at the inbound boundary.

Typical boundaries:
- CLI parsing;
- MCP tool inputs;
- HTTP requests;
- environment/config loading;
- files;
- queue/event messages.

After validation, pass stable application/domain types inward.

## Resource lifecycle

The component that creates or owns a long-lived resource should make its lifecycle clear.

Examples:
- MCP transports;
- child processes;
- sockets;
- database pools;
- file watchers;
- HTTP servers.

Provide explicit startup/shutdown behavior where resources outlive one function call. Handle process termination in the runtime/composition boundary, not inside domain logic.

## Logging

Log at boundaries and operation ownership points where context is meaningful.

Avoid scattering duplicate logging through every layer. Never make core domain behavior depend on a specific logger unless logging is itself part of the domain.
