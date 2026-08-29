# Domain Rules

- Store each domain object by role:
  - `domain/aggregates`: aggregate roots and aggregate composition.
  - `domain/entities`: identity-bearing domain objects that are not aggregate roots.
  - `domain/value_objects`: values, typed IDs, decisions, and domain enums.
  - `domain/domain_services`: domain services, policies, and specifications.
  - `domain/domain_events`: domain events.
  - `domain/factories`: domain factories when creation does not belong on domain object.
  - `domain/exceptions`: rejected business operations.
- Do not create empty directories or place domain objects directly in `domain`.
- Use Java records for domain objects where suitable. Keep components immutable; return new valid records for state changes.
- Keep domain plain Java. No Spring, JPA, HTTP, messaging, or infrastructure dependencies.
- Test domain behavior and invariants with plain Java unit tests. Do not start Spring context or external infrastructure.
