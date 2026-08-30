---
name: spring-testing
description: Test Spring-based Java backends across domain, application, and infrastructure layers. Use when writing, reviewing, or restructuring tests for business rules, use cases, Spring adapters, persistence, messaging, or HTTP boundaries.
---

# Spring Testing

Choose smallest test scope that proves behavior. Keep tests aligned with production boundaries:

- For business rules and domain objects, read [domain testing](references/domain.md).
- For use cases and orchestration, read [application testing](references/application.md).
- For Spring wiring and external adapters, read [infrastructure testing](references/infrastructure.md).

When a feature crosses multiple infrastructure boundaries, use infrastructure testing's full-feature shape. Separate inbound- and outbound-adapter tests do not verify the complete feature path.

Test observable behavior, contracts, and failure paths. Do not test private methods or reproduce implementation logic inside assertions.

Keep domain and application tests free from Spring unless framework behavior is part of contract. Use Spring context only for infrastructure behavior or wiring that cannot be proven with plain unit tests.
