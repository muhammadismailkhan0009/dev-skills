# Application Testing

Use JUnit 5, AssertJ, and Mockito. Test use cases through public input ports without Spring context. Combine stateful in-memory fakes with mocks based on port behavior:

- Use fakes for repositories and stores where tests read and assert state.
- Use Mockito for outbound notifications, publishers, gateways, and other interaction-based ports.

## In-memory fake pattern

Keep fake small and contract-compatible. Store real domain objects and expose only setup or inspection helpers needed by tests.

```java
final class InMemoryOrderRepository implements OrderRepository {
    private final Map<OrderId, Order> orders = new HashMap<>();

    @Override
    public Optional<Order> findById(OrderId id) {
        return Optional.ofNullable(orders.get(id));
    }

    @Override
    public void save(Order order) {
        orders.put(order.id(), order);
    }

    void given(Order order) {
        orders.put(order.id(), order);
    }

    Order stored(OrderId id) {
        return orders.get(id);
    }
}
```

Assert resulting fake state with AssertJ:

```java
@Test
void confirms_and_stores_order() {
    var repository = new InMemoryOrderRepository();
    var order = anOrder().withStatus(DRAFT).build();
    repository.given(order);
    var useCase = new ConfirmOrderService(repository, eventPublisher);

    var result = useCase.confirm(order.id());

    assertThat(result.status()).isEqualTo(CONFIRMED);
    assertThat(repository.stored(order.id()).status()).isEqualTo(CONFIRMED);
}
```

## Mockito pattern

Use Mockito JUnit 5 extension. Mock ports, not domain objects or use case under test.

```java
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class ConfirmOrderServiceTest {
    private final InMemoryOrderRepository repository = new InMemoryOrderRepository();

    @Mock
    private OrderEventPublisher eventPublisher;

    private ConfirmOrderService useCase;

    @BeforeEach
    void setUp() {
        useCase = new ConfirmOrderService(repository, eventPublisher);
    }

    @Test
    void publishes_event_after_confirmation() {
        var order = anOrder().withStatus(DRAFT).build();
        repository.given(order);

        var result = useCase.confirm(order.id());

        assertThat(result.status()).isEqualTo(CONFIRMED);
        verify(eventPublisher).publish(new OrderConfirmed(order.id()));
    }

    @Test
    void does_not_publish_when_order_is_missing() {
        var missingId = new OrderId("missing");

        assertThatThrownBy(() -> useCase.confirm(missingId))
                .isInstanceOf(OrderNotFoundException.class);
        verify(eventPublisher, never()).publish(any());
    }
}
```

Stub with `when(...).thenReturn(...)` only when mock must supply input. Verify exact arguments when interaction is contract. Use `ArgumentCaptor` only when value cannot be asserted directly.

## Failure pattern

For failures, assert exception or result and absence of forbidden effects:

```java
assertThatThrownBy(() -> useCase.confirm(order.id()))
        .isInstanceOf(OrderAlreadyConfirmedException.class);

assertThat(repository.stored(order.id())).isEqualTo(order);
verify(eventPublisher, never()).publish(any());
```

## Constraints

- Keep controller DTOs, JPA entities, and vendor SDK types out of application tests.
- Mock external ports, not domain objects or use case under test.
- Avoid broad `any()` matchers when exact command or persisted value matters.
- Capture arguments only when direct equality assertions are insufficient.
- Do not verify every call. Verify only interactions representing application behavior.
- Do not make fake behavior more permissive than real port contract.
- Share fake implementation across tests only when it remains small, deterministic, and generally useful.
- Do not test Spring annotations with unit tests.
- Test transaction rollback, proxy behavior, or security annotations with focused Spring integration tests instead.

Use fixed clocks and deterministic IDs where use cases create time-dependent or generated values.
