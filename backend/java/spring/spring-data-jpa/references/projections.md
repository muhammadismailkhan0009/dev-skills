# Projections

Use projections for adapter-local read models when a use case needs only selected columns. Keep projection types inside persistence infrastructure and map them to application-owned result types before crossing the adapter boundary.

## Closed interface projection

Use a closed interface for a small derived query when accessor names exactly match entity properties.

```java
interface OrderSummaryView {
    UUID getId();
    OrderStatusCode getStatus();
}

interface SpringDataOrderRepository extends JpaRepository<OrderEntity, OrderEntityId> {
    Slice<OrderSummaryView> findByStatusOrderById(
            OrderStatusCode status,
            Pageable pageable
    );
}
```

Nested projection accessors are supported, but traversing a nested property materializes its join. Prefer a flat purpose-built query when that join would fetch unnecessary data. Use nullable wrappers such as `Optional<T>` only for genuinely nullable projected values.

Avoid open projections using `@Value` and SpEL: Spring Data cannot optimize selected columns when any entity property might be referenced. A default method combining already projected accessors is acceptable for trivial formatting.

## Record DTO projection

Prefer a record for a stable, explicit read model with value semantics.

```java
record OrderSummaryRow(UUID id, OrderStatusCode status, BigDecimal total) {}

interface SpringDataOrderRepository extends JpaRepository<OrderEntity, OrderEntityId> {
    @Query("""
            select new com.example.orders.infrastructure.persistence.OrderSummaryRow(
                o.id.value, o.status, o.total.amount
            )
            from OrderEntity o
            where o.status = :status
            order by o.id.value
            """)
    Slice<OrderSummaryRow> findSummaries(
            @Param("status") OrderStatusCode status,
            Pageable pageable
    );
}
```

JPQL constructor expressions require the projection's fully qualified class name. The selected values, order, and types must match its canonical constructor. For a derived DTO projection, Spring Data discovers fields from that single constructor; records naturally satisfy this requirement.

## Dynamic projection

Use dynamic projection only when one predicate genuinely serves multiple adapter-local result shapes.

```java
<T> List<T> findByStatus(OrderStatusCode status, Class<T> type);
```

Call with an entity, interface projection, or DTO type. If the `Class` value must also be used as a query argument, declare it as `Class<?>`; a matching `Class<T>` is consumed as the dynamic projection selector and is unavailable to JPQL or SpEL.

## Native query projection

- Return a DTO directly only when selected column order and types match its constructor.
- When columns require aliases, conversion, or reshaping, define `@SqlResultSetMapping` and reference it with `@NativeQuery(resultSetMapping = "...")`.
- Keep native projection SQL and mappings together in persistence infrastructure.

## Constraints

- Do not override a base repository method solely with a projection return type; base methods still execute as base methods.
- Do not use an entity superclass or an interface implemented by the entity as a projection; that materializes the entity.
- Do not expose persistence projection interfaces or rows through application ports.
- Select only fields needed by the use case, with deterministic ordering for paged results.
- Test projection queries against the real database engine because constructor, alias, join, and native mapping errors are integration concerns.
