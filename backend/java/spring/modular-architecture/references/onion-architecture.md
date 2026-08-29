# Onion Architecture Rules

- `domain`: business behavior and rules. Depends on no outer layer.
- `application`:
  - `use_cases`: application orchestration and transaction boundaries.
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
- Map transport, persistence, and vendor models at infrastructure boundary. Never pass them into domain.
- Add ports only when an outer capability crosses inward boundary or substitution has business value.
- Reject cyclic dependencies between layers and modules.



## Implementation tests

- Application tests exercise use cases with test doubles for output ports. Verify orchestration, domain results, persistence calls, and failure paths without loading Spring context.
- Infrastructure tests verify adapters against real boundary behavior: web contracts, persistence mappings and queries, message mapping, and external-client translation.
- Use focused Spring test slices or integration tests only where framework wiring or external boundary behavior matters.
- Test observable behavior, not private methods or package structure.
