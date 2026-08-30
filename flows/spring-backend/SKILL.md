---
name: spring-backend
description: Arrange atomic skills for complete Spring backend features and cross-layer changes.
---

# Spring Backend Flow

This skill only arranges atomic skills. Each invoked skill owns its implementation and verification rules.

For complete features, start with `$feature-planning`. During its approved implementation layers, invoke affected skills in this order:

1. `$modular-architecture` before every affected layer of a cross-layer feature.
2. `$spring-testing` with each behavior-changing layer.
3. Layer-specific implementation skills:
   - Domain and application: `$modular-architecture`.
   - Outbound persistence: `$spring-data-jpa`, then `$spring-services` when Spring wiring changes.
   - Inbound HTTP: `$spring-api`, then `$spring-services` when Spring wiring changes.
   - Structural mapping: `$mapstruct` alongside the layer that owns the mapping.
4. `$spring-testing` for cross-layer verification.
5. Return to `$feature-planning` for remaining lifecycle gates and completion.

For a scoped single-concern change, invoke only its matching atomic skill and `$spring-testing` when behavior changes.
