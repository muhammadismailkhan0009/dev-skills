---
name: spring-data-jpa
description: Implement Spring Data JPA persistence adapters for modular Spring backends. Use when creating or changing JPA entities, mappings, repositories, queries, transactions, migrations, or persistence adapters.
---

# Spring Data JPA

Keep persistence implementation in infrastructure. Domain objects remain plain Java and persistence-ignorant.

- For entities, relationships, IDs, locking, and domain mapping, read [entity mapping](references/entity-mapping.md).
- For Spring Data repositories, query methods, pagination, and adapter implementation, read [repositories](references/repositories.md).
- For interface, record DTO, and dynamic projections, read [projections](references/projections.md) after the repository guidance.
- For Flyway schema migrations and migration testing, read [Flyway](references/flyway.md).
- For transactions, performance, and configuration, read [configuration](references/configuration.md).

Create Spring Data repositories only for persistence aggregate roots. Expose application-owned output ports inward; keep `JpaRepository`, JPA entities, and projections inside persistence adapter.
