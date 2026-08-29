---
name: spring-backend
description: Build or change modular Spring backends by composing architecture, services, HTTP API, JPA, MapStruct, and testing skills. Use when work spans multiple backend concerns or implements complete backend feature.
---

# Spring Backend Flow

Compose atomic skills. Do not duplicate or override their rules. Load only skills needed by requested feature.

## Select skills

- Use `$modular-architecture` for module placement, domain model, application use cases, ports, adapters, and dependency direction.
- Use `$spring-services` when adding Spring stereotypes, dependency wiring, bean configuration, or injected values.
- Use `$spring-api` when feature has HTTP controller, request/response models, validation, status codes, or error responses.
- Use `$spring-data-jpa` when feature persists data, changes schema, defines JPA mapping, repository, query, projection, transaction, or Flyway migration.
- Use `$mapstruct` when structural mapping benefits from generated mapper. Skip for one or two obvious constructor calls.
- Use `$spring-testing` for every behavior change. Read only relevant domain, application, or infrastructure testing reference.

If requested work touches one concern only, use matching atomic skill directly. Do not force full flow.

## Implement feature

1. Read request and existing code. Identify module, behavior, inbound boundary, outbound boundaries, and observable result.
2. Load `$modular-architecture`. Place feature and define contracts before framework implementation.
3. Implement domain behavior with plain Java. Add domain tests when business rules change.
4. Implement application use case and ports. Add application tests with fakes and Mockito as appropriate.
5. Load only adapter skills required by feature:
   - HTTP: `$spring-api`
   - persistence: `$spring-data-jpa`
   - generated mapping: `$mapstruct`
6. Load `$spring-services` when wiring implementation into Spring.
7. Load `$spring-testing`. Add focused infrastructure tests for each real adapter. Add full-feature test when change crosses complete feature path.
8. Run smallest relevant tests first, then broader project verification.

## Feature paths

### HTTP feature without persistence

Use:

```text
modular-architecture
spring-api
spring-services
spring-testing
```

### Persistence feature without HTTP

Use:

```text
modular-architecture
spring-data-jpa
spring-services
spring-testing
```

### Full HTTP and persistence feature

Use:

```text
modular-architecture
spring-api
spring-data-jpa
spring-services
spring-testing
```

Add `mapstruct` only when mapping complexity warrants it.

## Constraints

- Preserve existing project conventions unless requested change replaces them.
- Keep domain plain Java.
- Keep transport and persistence models at infrastructure boundary.
- Keep application boundary independent from Spring MVC, JPA, and MapStruct types.
- Never create repository, controller, mapper, configuration, or migration feature does not need.
- Never load every skill by default. Choose from actual change surface.
- Follow atomic skill when this flow gives no detailed rule.
- When atomic rules conflict, preserve architecture dependency direction and user instruction; report unresolved conflict.
- Finish behavior and relevant tests before calling feature complete.
