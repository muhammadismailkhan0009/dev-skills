# Onion Architecture Rules

- `domain`: business behavior and rules. Depends on no outer layer.
- `application`:
  - `use_cases`: job checks, branching, sequencing, application orchestration, and transaction boundaries.
  - `ports/in`: use-case contracts.
  - `ports/out`: persistence and external-capability contracts owned by application.
  - `mappers`: classes/interfaces (use MapStruct) for converting between domain objects and application objects. These should not be public.
- `infrastructure`:
  - `web`: controllers, requests, responses, and web mapping.
  - `persistence`: JPA entities, repositories, and domain mapping.
  - `messaging`: publishers, listeners, and message mapping.
  - `mappers`: classes/interfaces (use MapStruct) for converting between infrastructure objects and application objects or domain objects. These should not be public.
- `shared/configuration`: all Spring configuration and dependency wiring shared by application. Keep configuration outside business modules.
- Dependencies point inward: application depends on domain; infrastructure depends on application and domain contracts.
- Application depends on domain and its own ports, never on infrastructure types or implementations.
- Inbound adapters may authenticate callers, map inbound data and caller identity to an application input, delegate once to an input port, and map the application result to a response. Keep job checks, policy decisions, branching, sequencing, and transactions in application use cases.
- Map transport, persistence, and vendor models at infrastructure boundary. Never pass them into domain.
- Add ports only when an outer capability crosses inward boundary or substitution has business value.
- Reject cyclic dependencies between layers and modules.

## Dependency-boundary review

Run this review before each implementation layer starts and again before that layer is presented for approval:

- Planned and implemented dependencies point inward.
- Application code imports no infrastructure, transport, persistence, or vendor type.
- Application orchestration uses output ports for persistence and external capabilities.
- Inbound adapters contain only authentication, mapping, one application delegation, and response mapping.
- Job checks, branching, sequencing, and transaction ownership remain in application.

## Implementation tests

- Application tests exercise use cases with test doubles for output ports. Verify orchestration, domain results, persistence calls, and failure paths without loading Spring context.
- Infrastructure tests verify adapters against real boundary behavior: web contracts, persistence mappings and queries, message mapping, and external-client translation.
- Use focused Spring test slices or integration tests only where framework wiring or external boundary behavior matters.
- Test observable behavior, not private methods or package structure.
