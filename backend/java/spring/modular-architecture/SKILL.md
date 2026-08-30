---
name: modular-architecture
description: Design or implement modular Java backends using Domain-Driven Design, onion architecture, and Spring Modulith. Use when work spans domain modeling, application and infrastructure boundaries, or module isolation.
---

# Modular Architecture

Implement in order. Finish implementation and tests for each step before next:

1. Read [Spring Modulith rules](references/spring-modulith.md). Create modules, public interfaces, allowed dependencies, and structural verification first.
2. Read [domain rules](references/domain.md). Implement business behavior and plain Java tests covering all stated business requirements.
3. Read [onion architecture rules](references/onion-architecture.md). Implement application use cases and infrastructure adapters, then test both layers.

Architecture: `domain`, `application`, `infrastructure`. Dependencies point inward.

Before implementing each layer, check its planned types and dependencies against the onion boundaries. Before presenting that layer for approval, review the resulting dependency boundary again and fix any leaked infrastructure type, outward dependency, or misplaced orchestration.

For modular monoliths, keep configuration in application-level `shared/configuration`, never inside business modules.
