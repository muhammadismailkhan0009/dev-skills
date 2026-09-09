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

## $angular-architecture
Structure Angular/Nx frontends by business domain and vertical feature ownership. Use when creating, moving, reviewing, or organizing features, shared code, components, routes, data access, state, or dependency boundaries.

References:
- `directory-structure.md` — domain/feature layout, feature-root files, `components/`, `data-access/`, `util/`, promotion to domain/global shared, and minimal-folder rules.
- `dependency-boundaries.md` — allowed feature/domain/shared dependency direction, feature isolation, cross-domain contracts, type ownership, and enforceable Nx boundaries.

## $angular-ui
Build Angular screens and shared UI through composition using Tailwind CSS v4 and spartan/ui. Reuse existing application components first, then installed or newly added Spartan primitives; avoid screen-local reinvention of standard controls and large handcrafted CSS.

References:
- `spartan-ui.md` — mandatory reuse order, Spartan skill/MCP/CLI discovery, Tailwind styling policy, component boundaries, and completion checks.

## $nextjs-architecture
Structure Next.js App Router frontends by business domain and vertical feature ownership. Keep `src/app/` as a thin routing/composition boundary, place feature slices under the frontend root's `libs/`, and preserve explicit Server/Client Component boundaries.

References:
- `directory-structure.md` — frontend-root layout, thin App Router route files, feature-root files, `components/`, `data-access/`, `util/`, and promotion to domain/global shared.
- `dependency-boundaries.md` — app/feature/domain-shared/global-shared dependency direction, feature isolation, cross-domain contracts, type ownership, and server/client dependency constraints.
- `server-client-boundaries.md` — Server Components by default, minimal `'use client'` boundaries, data fetching, Server Actions, Route Handlers, server-only concerns, and version-matched Next.js runtime/docs guidance.

## $nextjs-ui
Build Next.js/React screens and shared UI through composition using Tailwind CSS v4 and shadcn/ui. Reuse existing application components first, then installed or newly added shadcn components; keep client boundaries small and avoid handcrafted standard primitives.

References:
- `shadcn-ui.md` — mandatory reuse order, `components.json` ownership, official shadcn skill/MCP/CLI/docs workflow, Tailwind styling policy, component placement, server/client UI boundaries, and completion checks.

## $uiflow
Use `@myriadcodelabs/uiflow` for React/Next.js interactions that have meaningful orchestration: multiple UI phases, branching transitions, async retry/error/success sequencing, shared journey state, or coordination between independent flows. Do not use it for ordinary local component state, simple forms/handlers, or server-rendered content where plain React/Next.js is clearer.

References:
- `core-api-and-runtime.md` — `defineFlow`, `FlowRunner`, domain/internal state, UI/action steps, action rendering, channels, transition behavior, and runtime caveats.
- `flow-design.md` — applicability decision, cohesive flow boundaries, parent/child composition, output/action discipline, state ownership, channels, render discipline, and simplicity rules.
- `nextjs-integration.md` — App Router client boundary, server-provided initial data, UIFlow action steps versus Next.js Server Actions, data fetching, errors, and channels.
- `testing.md` — user-level flow behavior, action rendering, channels, state ownership, and avoiding redundant library-contract tests in consumers.

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
