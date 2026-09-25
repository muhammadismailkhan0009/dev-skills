# Types and Modeling

Use TypeScript's type system to make contracts and state explicit without creating Java-style ceremony.

## Data

Prefer `type`, interfaces, and readonly object shapes for data.

Use domain names rather than transport-shaped names when the data belongs to the domain.

Keep transport, vendor, persistence, and protocol models at their boundaries. Map them before they enter inner application/domain code.

## Interface vs type

Use either consistently according to intent rather than arbitrary rules.

Good bias:
- `interface` for behavioral contracts or ports that implementations satisfy;
- `type` for data composition, unions, mapped types, aliases, and closed alternatives.

Do not create an interface solely because a Java equivalent would have one.

## Closed alternatives

Prefer discriminated unions when a value has a known finite set of states or outcomes.

They are especially useful for:
- command results;
- parsing outcomes;
- lifecycle state;
- protocol state;
- domain state transitions;
- recoverable error/result models.

Require exhaustive handling where practical.

## Unknown input

Treat external input as `unknown` until validated or narrowed.

External input includes:
- CLI arguments;
- environment variables;
- JSON;
- MCP payloads;
- HTTP requests;
- file contents;
- message payloads;
- third-party SDK responses when runtime guarantees are insufficient.

Avoid `any` as an escape hatch. If `any` is unavoidable at a library boundary, contain it at that boundary and convert to a safe internal type immediately.

## Nullability and optional values

Model absence deliberately.

- Do not use optional fields when a field is always required after validation.
- Prefer explicit states over clusters of unrelated optional booleans/fields when combinations matter.
- Narrow nullable values at boundaries instead of scattering defensive checks through core logic.

## Behavioral contracts

Ports and abstractions should describe capability, not implementation.

Prefer:

```text
SkillStore
RemoteSkillSource
ProcessLauncher
Clock
```

over implementation-shaped contracts such as:

```text
FileSystemServiceInterface
AxiosClientInterface
NodeProcessManagerInterface
```

Add an abstraction when a dependency crosses an architectural boundary or substitution/testing has real value; do not add interfaces mechanically around every class.
