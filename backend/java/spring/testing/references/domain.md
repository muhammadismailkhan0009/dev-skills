# Domain Testing

Use JUnit 5 for test lifecycle and parameterization. Use AssertJ for fluent assertions. Keep tests in Arrange–Act–Assert shape, with one behavior per test.

## JUnit 5 structure and lifecycle

Use lifecycle hooks when setup is genuinely shared. Keep behavior-specific values inside each test.

```java
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class OrderTest {
    private Currency currency;
    private Order order;

    @BeforeAll
    void createSharedFixture() {
        currency = Currency.getInstance("EUR");
    }

    @BeforeEach
    void createFreshOrder() {
        order = Order.empty(currency);
    }

    @Nested
    class Confirmation {
        @Test
        void rejects_empty_order() {
            assertThatThrownBy(order::confirm)
                    .isInstanceOf(EmptyOrderException.class);
        }
    }
}
```

- `@BeforeEach`: create fresh mutable fixtures used by most tests.
- `@AfterEach`: release per-test resources or verify shared test-double state. Omit when no cleanup exists.
- `@BeforeAll` and `@AfterAll`: manage expensive class-scoped fixtures. Methods must be `static` unless class uses `@TestInstance(PER_CLASS)`.
- `@Nested`: group scenarios sharing context. Nested test classes must be non-static.
- `@DisplayName`: use only when method and nested-class names cannot express behavior clearly.
- `@Tag`: mark meaningful suites such as `slow`; do not replace normal test organization with tags.
- `@Disabled`: temporary last resort. Include reason and tracking issue.
- `@Timeout`: use only for a real time limit; do not use it to hide blocking or concurrency defects.

Never share mutable domain state between tests. `@BeforeAll` fixtures must be immutable or recreated before mutation.

## Basic pattern

```java
import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

class OrderTest {
    @Test
    void confirms_order_with_total_price() {
        var order = Order.draft(new OrderLine("book", 2, Money.euros("12.50")));

        var confirmed = order.confirm();

        assertThat(confirmed.status()).isEqualTo(OrderStatus.CONFIRMED);
        assertThat(confirmed.total()).isEqualTo(Money.euros("25.00"));
    }
}
```

Prefer one object assertion when several properties describe one outcome:

```java
assertThat(confirmed)
        .extracting(Order::status, Order::total)
        .containsExactly(OrderStatus.CONFIRMED, Money.euros("25.00"));
```

## Rejected behavior

Use AssertJ exception assertions. Check domain exception type and stable structured details.

```java
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@Test
void rejects_confirmation_of_empty_order() {
    var order = Order.empty();

    assertThatThrownBy(order::confirm)
            .isInstanceOf(EmptyOrderException.class)
            .extracting("orderId")
            .isEqualTo(order.id());
}
```

Use `assertThatCode(...).doesNotThrowAnyException()` only when absence of failure is behavior being specified. Otherwise assert resulting state or return value.

## Parameterized rules

Use `@ParameterizedTest` for a rule exercised by meaningful input cases. Give each case a readable name.

```java
import static org.assertj.core.api.Assertions.assertThat;

import java.util.stream.Stream;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

@ParameterizedTest(name = "{0}")
@MethodSource("discountCases")
void calculates_discount(String caseName, Money subtotal, CustomerType type, Money expected) {
    assertThat(Discount.calculate(subtotal, type)).isEqualTo(expected);
}

static Stream<Arguments> discountCases() {
    return Stream.of(
            Arguments.of("regular customer", Money.euros("100"), CustomerType.REGULAR, Money.ZERO),
            Arguments.of("premium customer", Money.euros("100"), CustomerType.PREMIUM, Money.euros("10"))
    );
}
```

Use `@ValueSource`, `@EnumSource`, or `@CsvSource` when clearer than `@MethodSource`.

## Test fixtures

Start with direct construction. Introduce a test-data builder when valid setup becomes noisy. Give builder meaningful defaults and override only values relevant to test.

```java
var order = anOrder()
        .withStatus(OrderStatus.CONFIRMED)
        .withTotal(Money.euros("25.00"))
        .build();
```

For time, IDs, or randomness, inject deterministic collaborators and use fixed values in tests.

## Constraints

- Keep tests deterministic. Pass clocks, ID generators, and random sources as controlled dependencies when domain behavior depends on them.
- Assert exact business error types and stable domain details, not incidental exception text.
- Do not mock value objects, entities, or aggregates.
- Do not assert internal method calls or private implementation details.
- Do not duplicate production calculations in expected-value logic. Use explicit examples with known outcomes.
- Do not weaken production visibility solely for tests.
- Prefer behavior names such as `rejects_order_when_credit_limit_is_exceeded`.
