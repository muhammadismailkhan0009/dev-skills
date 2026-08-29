# Spring Modulith Implementations

Use Spring Modulith to make business-module boundaries explicit and executable.

## Module implementation

- Put each bounded context directly below application base package.
- Inside each module, use `domain`, `application`, and `infrastructure`; keep domain objects in their prescribed plural subpackages.
- Put all Spring configuration and dependency wiring in application-level `shared/configuration`, outside business modules. Do not create module-local configuration packages.
- Use Java records for domain entities and value objects. Keep JPA entities in `infrastructure/persistence`, separate from domain records.
- Keep infrastructure implementation types package-private where possible. Domain types used across role packages must be public, but only module APIs or named interfaces may be consumed by other modules.
- Declare allowed cross-module API packages with `@NamedInterface`.
- Prefer events for reactions that do not require synchronous consistency.
- Never access another module's repositories, entities, or internal services.
- Keep module dependency graph acyclic.

```text
shared/
  configuration/
orders/
  domain/
  application/
  infrastructure/
```

Declare module and named interface with `package-info.java`:

```java
@ApplicationModule(allowedDependencies = "inventory :: api")
package com.example.shop.orders;

import org.springframework.modulith.ApplicationModule;
```

```java
@NamedInterface("api")
package com.example.shop.inventory.api;

import org.springframework.modulith.NamedInterface;
```

Publish ordinary domain event through Spring application boundary:

```java
@Service
class PlaceOrder {
    private final ApplicationEventPublisher events;

    @Transactional
    OrderId place(PlaceOrderCommand command) {
        Order order = Order.place(command);
        events.publishEvent(new OrderPlaced(order.id()));
        return order.id();
    }
}
```

Handle event after originating transaction completes:

```java
@Component
class ReserveInventory {
    @ApplicationModuleListener
    void on(OrderPlaced event) {
        // invoke inventory use case
    }
}
```

## Structural verification

Keep verification test in application base package:

```java
class ModularityTest {
    private final ApplicationModules modules =
            ApplicationModules.of(ShopApplication.class);

    @Test
    void verifiesModuleBoundaries() {
        modules.verify();
    }
}
```

Use `ApplicationModuleTest` for module-scoped integration tests:

```java
@ApplicationModuleTest
class OrdersModuleTest {
    @Test
    void publishesOrderPlaced(Scenario scenario) {
        scenario.stimulate(() -> placeOrder.place(command()))
                .andWaitForEventOfType(OrderPlaced.class)
                .toArrive();
    }
}
```

Use `Documenter` only when generated module diagrams or canvases are requested. Run `ApplicationModules.verify()` in CI so illegal dependencies and cycles fail build.

Adapt package names, module APIs, transactions, and test fixtures to project. Confirm annotations and test APIs against project's Spring Modulith version before implementation.
