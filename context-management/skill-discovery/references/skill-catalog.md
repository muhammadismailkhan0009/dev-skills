# Skill Discovery Catalog

Use this catalog before substantial repository work to identify applicable development skills. It is a discovery index, not the skill rules themselves.

Load only skills relevant to the current task. Read a selected skill's `SKILL.md` before applying it, then load only the reference files needed for the current concern according to that skill. Do not preload every skill or every reference. If no skill applies, load none.

## $feature-planning
Complete feature lifecycle: conceptual behavior approval, targeted feasibility inspection, frozen baseline, layer-gated BDD execution, and final conformance review.

References:
- `conceptual-planning.md` — behavior clarification and conceptual approval before repository inspection.
- `feasibility-and-baseline.md` — targeted code inspection, feasibility reconciliation, and baseline freeze.
- `layer-bdd-execution.md` — approved layer-by-layer BDD implementation and gates.
- `conformance-review.md` — final behavior-to-baseline conformance review.

## $angular-ui
Build Angular screens and shared UI through composition using Tailwind CSS v4 and spartan/ui. Reuse existing application components first, then installed or newly added Spartan primitives; avoid screen-local reinvention of standard controls and large handcrafted CSS.

References:
- `spartan-ui.md` — mandatory reuse order, Spartan skill/MCP/CLI discovery, Tailwind styling policy, component boundaries, and completion checks.

## $mapstruct
Compile-time Java structural mappings among domain models, persistence entities, commands, and DTOs. Use for mapping configuration and deterministic conversion only; not business logic or external calls.

## $modular-architecture
Modular Java backend architecture using DDD, onion architecture, and Spring Modulith; use for domain modeling, module boundaries, application/infrastructure separation, and dependency direction.

References:
- `spring-modulith.md` — module boundaries, public interfaces, allowed dependencies, and structural verification.
- `domain.md` — domain entities, value objects, typed identity, invariants, and plain-Java domain behavior.
- `onion-architecture.md` — application/use-case and infrastructure boundaries, ports/adapters, and inward dependencies.

## $spring-api
Spring MVC HTTP adapters: REST controllers, request/response records, validation, status codes, headers, pagination contracts, and API error handling. Not WebFlux or business logic.

## $spring-data-jpa
Spring Data JPA persistence adapters: entities, mappings, repositories, queries, transactions, migrations, projections, and persistence configuration.

References:
- `entity-mapping.md` — entities, relationships, aggregate IDs, locking, and domain/persistence mapping.
- `repositories.md` — Spring Data repositories, query methods, pagination, and persistence adapters.
- `projections.md` — interface, record DTO, and dynamic projections; use after repository guidance when projections are involved.
- `flyway.md` — schema migrations and migration testing.
- `configuration.md` — transactions, persistence performance, and JPA configuration.

## $spring-services
Spring-managed application/infrastructure services: stereotypes, constructor injection, bean registration, configuration properties/values, qualifiers, and dependency wiring.

## $spring-logging
Minimize Spring test output for LLM-driven development by suppressing framework, persistence, container, pool, migration, banner, SQL, and debug noise while retaining actual test failure evidence. The complete test suppression baseline is mandatory whenever Spring tests are configured or run.

References:
- `test-logging.md` — mandatory Spring Boot, JPA/Hibernate, `logback-test.xml`, and Maven Surefire test-log suppression baseline plus narrow temporary diagnostic logging rules.

## $spring-testing
Spring Java backend testing by architectural boundary: domain behavior, application/use-case orchestration, Spring wiring, persistence, messaging, HTTP, and cross-layer infrastructure verification.

References:
- `domain.md` — plain-Java business-rule and domain-object tests.
- `application.md` — use-case and orchestration tests.
- `infrastructure.md` — Spring wiring, adapters, persistence/integration, and full-feature infrastructure tests.

## $spring-backend
Flow skill for complete Spring backend features and cross-layer changes. Coordinates `$feature-planning`, `$modular-architecture`, `$spring-testing`, `$spring-data-jpa`, `$spring-services`, `$spring-api`, and `$mapstruct` in the appropriate order; use atomic skills directly for scoped single-concern work.