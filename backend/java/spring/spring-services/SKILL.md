---
name: spring-services
description: Implement Spring-managed application and infrastructure services. Use when selecting service stereotypes, registering beans, or wiring dependencies in Spring applications.
---

# Spring Services

Use constructor injection. Declare required dependencies as `final`; omit `@Autowired` when the class has one constructor.

## Choose annotations by role

- `@Service`: application service or use-case implementation that orchestrates work.
- `@Repository`: persistence implementation; enables persistence-exception translation.
- `@Component`: infrastructure service without a more specific stereotype, such as an external API adapter or clock implementation.
- `@Configuration(proxyBeanMethods = false)`: explicit bean configuration.
- `@Bean`: third-party types or construction requiring configuration. Prefer this over adding Spring annotations to types not owned by the project.

Do not annotate domain objects. Avoid redundant stereotype combinations and field/setter injection.

## Service pattern

```java
@Service
final class PlaceOrderService implements PlaceOrderUseCase {
    private final OrderRepository orders;
    private final PaymentGateway payments;

    PlaceOrderService(OrderRepository orders, PaymentGateway payments) {
        this.orders = Objects.requireNonNull(orders, "orders");
        this.payments = Objects.requireNonNull(payments, "payments");
    }

    @Override
    public OrderId place(PlaceOrderCommand command) {
        var order = Order.place(command);
        payments.authorize(order.payment());
        orders.save(order);
        return order.id();
    }
}
```

## Infrastructure pattern

```java
@Component
final class HttpPaymentGateway implements PaymentGateway {
    private final PaymentClient client;

    HttpPaymentGateway(PaymentClient client) {
        this.client = Objects.requireNonNull(client, "client");
    }
}
```

```java
@Configuration(proxyBeanMethods = false)
class PaymentConfiguration {
    @Bean
    PaymentClient paymentClient(PaymentProperties properties) {
        return new PaymentClient(properties.baseUrl(), properties.apiKey());
    }
}
```

## `@Value` rules

Prefer type-safe `@ConfigurationProperties` when settings belong together, require validation, or are reused. Use `@Value` only for a small, local scalar value.

Inject it through a constructor or `@Bean` method parameter:

```java
@Bean
PaymentClient paymentClient(
        @Value("${payment.base-url}") URI baseUrl,
        @Value("${payment.connect-timeout:5s}") Duration connectTimeout,
        @Value("${payment.allowed-currencies:USD,EUR}") List<String> allowedCurrencies
) {
    return new PaymentClient(baseUrl, connectTimeout, List.copyOf(allowedCurrencies));
}
```

Define the matching values in `application.yaml`. Use environment variables for deployment-specific values:

```yaml
payment:
  base-url: ${PAYMENT_BASE_URL}
  connect-timeout: ${PAYMENT_CONNECT_TIMEOUT:5s}
  allowed-currencies: ${PAYMENT_ALLOWED_CURRENCIES:USD,EUR}
```

For `@Value` lists, provide a comma-delimited scalar. Spring converts it to `List<T>` when element conversion is supported. Copy the injected list when the consumer should retain an immutable value. Use `@ConfigurationProperties` for nested or structured collections.

To compose a list from independent environment values, use a folded YAML scalar with comma separators:

```yaml
ai:
  api-keys: >-
    ${DEEPSEEK_API_KEY:},
    ${OPENAI_API_KEY:},
    ${GEMINI_API_KEY:}
```

```java
AiClientRegistry(
        @Value("${ai.api-keys}") List<String> apiKeys
) {
    this.apiKeys = apiKeys.stream()
            .map(String::trim)
            .filter(key -> !key.isBlank())
            .toList();
}
```

Keep the commas: YAML folding joins the lines, while Spring uses commas to convert the scalar into list elements. Filter blank elements when environment variables are optional.

- Use `${property.name}` for configuration properties. Avoid SpEL (`#{...}`) unless runtime expression evaluation is actually required.
- Omit a default for required configuration so startup fails when missing. Add `:default` only when the default is safe and intentional.
- Inject into supported target types such as `Duration`, `URI`, numbers, booleans, and enums instead of parsing strings manually.
- Never use `@Value` field injection or attempt to inject static fields.
- Keep property names centralized by concern; do not repeat the same `@Value` expression across services.
- Override properties in tests instead of mutating injected values.

## Dependency rules

- Depend on the narrow interface required by the consumer.
- Keep dependencies explicit; do not fetch beans through `ApplicationContext` or static holders.
- When multiple beans implement one interface, prefer distinct interfaces. Otherwise use `@Qualifier` at both declaration and injection point.
- Use `@Primary` only when one implementation is truly the application-wide default.
- Avoid optional dependencies in constructors. Model optional capabilities explicitly or configure conditional beans.
- Keep services stateless. Do not store request or transaction state in singleton fields.
- Use configuration properties for external settings; do not scatter `@Value` strings through services.
