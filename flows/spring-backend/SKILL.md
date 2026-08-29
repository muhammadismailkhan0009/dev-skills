---
name: spring-backend
description: Deliver Spring backend features through feature-planning lifecycle, then select architecture, services, HTTP API, JPA, MapStruct, and testing skills. Use for complete Spring backend features or scoped multi-layer changes.
---

# Spring Backend Flow

Compose atomic skills. Do not duplicate or override their rules. Load only skills needed by requested feature.

This flow defines Spring implementation layers, order, and skill selection only. It does not own feature clarification, behavior approval, BDD lifecycle, review gates, or conformance review.

## Feature lifecycle

For feature request, load `$feature-planning` first and pass this skill as configured development flow.

Before conceptual approval:

- Follow `$feature-planning` only.
- Do not inspect repository.
- Do not load Spring or Java implementation skills.
- Treat layer order and skill list below as later configuration, not planning evidence.

After `$feature-planning` confirms feasibility and freezes implementation baseline, use affected layers and atomic skills below. Return each completed layer to `$feature-planning` for approval gate. Return final implementation to `$feature-planning` for conformance review.

For explicit scoped technical change without feature behavior planning, select matching atomic skill directly.

## Select skills

- Use `$modular-architecture` for module placement, domain model, application use cases, ports, adapters, and dependency direction.
- Use `$spring-services` when adding Spring stereotypes, dependency wiring, bean configuration, or injected values.
- Use `$spring-api` when feature has HTTP controller, request/response models, validation, status codes, or error responses.
- Use `$spring-data-jpa` when feature persists data, changes schema, defines JPA mapping, repository, query, projection, transaction, or Flyway migration.
- Use `$mapstruct` when structural mapping benefits from generated mapper. Skip for one or two obvious constructor calls.
- Use `$spring-testing` for every behavior change. Read only relevant domain, application, or infrastructure testing reference.

If requested work touches one concern only, use matching atomic skill directly. Do not force full flow.

## Layer order

Use only affected layers:

```text
architecture and placement
domain
application
outbound infrastructure
inbound API
Spring wiring
cross-layer verification
```

Configured feature lifecycle decides when each layer starts and stops. This flow supplies matching atomic skill and Spring-specific rules.

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
- Never call feature complete directly. `$feature-planning` owns final conformance decision.
