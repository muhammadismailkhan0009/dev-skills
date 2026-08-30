# Infrastructure Testing

Use JUnit 5, AssertJ, Spring Boot test support, and Testcontainers. Exercise real serialization, mappings, framework configuration, protocols, and storage behavior.

Use three test shapes:

1. Outbound adapter: real adapter with real or local dependency.
2. Inbound adapter: real controller, listener, or tool with mocked application boundary.
3. Full feature: real inbound adapter, application, domain, outbound adapter, and real or local dependencies.

Full-feature test is required whenever one feature crosses multiple infrastructure boundaries. This includes paths such as:

```text
inbound adapter -> application -> persistence adapter -> database
```

Outbound- and inbound-adapter tests remain useful boundary checks, but their combined presence is insufficient to declare such a feature verified. Feature verification must also exercise complete path through real Spring wiring without internal mocks.

## Outbound adapter

Start real dependency through Testcontainers or another reproducible local implementation. Wire real adapter to it. Never mock client, repository, serializer, driver, or protocol used by adapter.

```java
@SpringBootTest(classes = OrderPersistenceTestConfiguration.class)
@Import(TestContainersConfiguration.class)
class JpaOrderRepositoryAdapterTest {
    @Autowired
    private JpaOrderRepositoryAdapter adapter;

    @Test
    void stores_and_loads_order() {
        var order = anOrder().withStatus(CONFIRMED).build();

        adapter.save(order);

        assertThat(adapter.findById(order.id()))
                .contains(order);
    }
}
```

Apply same pattern to brokers, caches, object stores, search engines, and HTTP APIs. Prefer real service container. When third-party service cannot run locally, use protocol-level stub server such as WireMock and send real HTTP through production client.

Verify:

- Domain-to-external mapping and round trips.
- Queries, constraints, migrations, indexes, and transactions.
- Serialization, headers, routing, and acknowledgements.
- Timeout, unavailable dependency, malformed response, and error translation.

## Inbound adapter

Load real inbound adapter and framework components. Mock application input port at boundary. Assert incoming protocol maps to exact application command and response.

### HTTP controller

```java
@WebMvcTest(ConfirmOrderController.class)
class ConfirmOrderControllerTest {
    @Autowired
    private MockMvc mvc;

    @MockitoBean
    private ConfirmOrderUseCase useCase;

    @Test
    void confirms_order() throws Exception {
        var id = "order-123";
        when(useCase.confirm(new ConfirmOrderCommand(new OrderId(id))))
                .thenReturn(new ConfirmOrderResult(new OrderId(id), CONFIRMED));

        mvc.perform(post("/orders/{id}/confirmation", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("CONFIRMED"));

        verify(useCase).confirm(new ConfirmOrderCommand(new OrderId(id)));
    }
}
```

For message listeners, send real serialized message through listener container or test binder, then verify application input port receives exact command. For CLI, MCP, or tool adapters, invoke real adapter through its public transport entrypoint and mock only application input port.

Verify validation, authentication, deserialization, mapping, status or acknowledgement, error response, and application-boundary call.

## Full feature

Start complete Spring context plus all required real/local dependencies. Enter through real inbound transport. Keep application, domain, outbound adapters, database, broker, and local external services real. Do not mock components inside feature path.

Use this shape as mandatory cross-boundary evidence when request expects inbound-to-dependency behavior, including MCP-, HTTP-, message-, or CLI-to-database flows. Do not stop after separate inbound and outbound tests pass.

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Import(TestContainersConfiguration.class)
class ConfirmOrderFeatureTest {
    @Autowired
    private TestRestTemplate http;

    @Autowired
    private JdbcTemplate jdbc;

    @Test
    void confirms_order_end_to_end() {
        var id = insertDraftOrder(jdbc);

        var response = http.postForEntity(
                "/orders/{id}/confirmation", null, ConfirmOrderResponse.class, id);

        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody().status()).isEqualTo("CONFIRMED");
        assertThat(storedStatus(jdbc, id)).isEqualTo("CONFIRMED");
    }
}
```

Assert result at externally observable boundaries: HTTP response, stored data, published message, generated file, or local service state. Cover successful path and highest-value integration failures.

## Dependency setup

- For Spring integration tests, prefer containers managed as Spring beans. They start before application beans, stop after dependent beans, and remain valid for cached application contexts.
- Use JUnit `@Testcontainers` and static `@Container` fields for vanilla JUnit tests or isolated Spring contexts. Non-static containers restart for every test method. Avoid JUnit-managed containers when Spring may reuse cached context after container stops.
- Use pinned container images compatible with production.
- Prefer `@ServiceConnection`; use `@DynamicPropertySource` when automatic connection metadata is unavailable.
- Apply production migrations rather than test-only schema creation.
- Use reproducible local service emulators only when real service cannot run locally.
- Seed minimum data required by scenario. Give every test isolated identifiers.
- Wait for asynchronous observable outcome with bounded polling; never use arbitrary sleeps.

Declare shared Spring-managed containers in test configuration:

```java
@TestConfiguration(proxyBeanMethods = false)
class TestContainersConfiguration {
    @Bean
    @ServiceConnection
    PostgreSQLContainer<?> postgres() {
        return new PostgreSQLContainer<>("postgres:17-alpine");
    }
}
```

Import configuration into relevant tests with `@Import(TestContainersConfiguration.class)`. `@ServiceConnection` supplies typed connection details that override connection properties. Add `spring-boot-testcontainers` as test dependency.

For `GenericContainer`, provide service name because Spring Boot cannot infer connection type from bean return type:

```java
@Bean
@ServiceConnection(name = "redis")
GenericContainer<?> redis() {
    return new GenericContainer<>("redis:7-alpine");
}
```

When no service connection factory exists, register container values with static `@DynamicPropertySource`:

```java
@DynamicPropertySource
static void dependencyProperties(DynamicPropertyRegistry registry) {
    registry.add("external.orders.base-url", ordersContainer::getBaseUrl);
}
```

For reusable static container declarations shared by multiple tests, put them in an interface and import it through `@ImportTestcontainers` on test configuration.

## Constraints

- Do not mock outbound dependency in outbound adapter or full-feature tests.
- Mock only application boundary in inbound adapter tests.
- Never declare a multi-boundary feature verified without a passing full-feature test covering its complete path.
- Do not replace production mappings, serializers, clients, migrations, or configuration with test-only alternatives.
- Do not assert private calls or internal implementation structure.
- Keep tests deterministic, independent, and runnable in CI.
- Reset state between tests through transactions, truncation, isolated schemas, or unique resources.
- Test through real connection used by production adapter whenever dependency can run locally.
