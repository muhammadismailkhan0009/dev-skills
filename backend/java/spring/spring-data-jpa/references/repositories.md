# Repositories and Adapters

Keep Spring Data interface package-private beside persistence adapter.

```java
interface SpringDataOrderRepository extends JpaRepository<OrderEntity, OrderEntityId> {
    @EntityGraph(attributePaths = "lines")
    Optional<OrderEntity> findWithLinesById(OrderEntityId id);

    Slice<OrderEntity> findByStatusOrderById(OrderStatusCode status, Pageable pageable);
}
```

Adapter implements application output port and owns mapping:

```java
@Repository
final class JpaOrderRepositoryAdapter implements OrderRepository {
    private final SpringDataOrderRepository repository;
    private final OrderPersistenceMapper mapper;

    @Override
    public Optional<Order> findById(OrderId id) {
        return repository.findWithLinesById(new OrderEntityId(id.value())).map(mapper::toDomain);
    }

    @Override
    public void save(Order order) {
        repository.save(mapper.toEntity(order));
    }
}
```

## Query rules

- Use derived queries for short, unambiguous predicates. Property names are validated at startup.
- Insert `_` to mark a nested-property boundary only when parsing is ambiguous, such as `findByAddress_ZipCode`.
- Avoid reserved-method ambiguity around `findById`, `existsById`, and `deleteById`. Add a descriptive token when querying a non-identifier property named `id`, such as `findOrderById`.
- Use `@Query` with JPQL when derivation becomes hard to read or cannot express the query. Prefer named parameters; use `@Param` unless parameter-name discovery is guaranteed by the build.
- Use `@NativeQuery` only for database-specific capability or measured need. Supply an explicit `countQuery` for paged native or complex queries when Spring cannot safely derive it.
- Fetch required collections deliberately with `@EntityGraph`, fetch join, projection, or dedicated query.
- Never paginate a collection fetch join. Page root IDs or use projection, then load required graph.
- For read-only list and report queries, follow [projection patterns](projections.md); do not hydrate full aggregates unnecessarily.
- Use `Page` only when total count is required. Prefer `Slice` when caller only needs next-page knowledge.
- Use `Window` with keyset scrolling for large or deep result traversal when indexed sort keys are available. Include every sort key in the result.
- Always define deterministic ordering for pagination or scrolling, including a unique tie-breaker.
- Do not combine `Pageable` with `Sort` or `Limit`; `Pageable` already carries both concerns.
- Close `Stream<T>` results with try-with-resources and consume them inside the transaction that owns the persistence context.
- Treat `distinct` deliberately. Derived `countDistinctBy…` usually counts distinct entity IDs, which may equal a normal count; write explicit JPQL when distinct semantics matter.
- Use `@Modifying` only with explicit update/delete `@Query` methods. Return affected row count when useful and account for stale managed entities; request automatic clearing only when discarding pending persistence-context changes is safe.
- Avoid `saveAndFlush` unless following operation requires SQL execution immediately.
- Move queries requiring `EntityManager`, Criteria, JDBC, or substantial dynamic assembly into a custom repository implementation.
- Do not expose JPA entities, `Page`, `Specification`, or `EntityManager` through application port.
