---
name: spring-api
description: Build HTTP APIs with Spring MVC annotated controllers. Use for REST endpoints, request and response records, validation, status codes, headers, and API error handling. Do not use for WebFlux or business logic.
---

# Spring API

Build thin HTTP adapters. Controller translates HTTP input into application input, invokes boundary, translates result into HTTP response. Keep business rules, transactions, persistence, and external calls outside controller.

## Controller pattern

```java
@RestController
@RequestMapping(path = "/api/orders", produces = MediaType.APPLICATION_JSON_VALUE)
final class OrderController {
    private final CreateOrder createOrder;
    private final GetOrder getOrder;

    OrderController(CreateOrder createOrder, GetOrder getOrder) {
        this.createOrder = createOrder;
        this.getOrder = getOrder;
    }

    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE)
    ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest request) {
        var order = createOrder.handle(request.toCommand());
        var location = URI.create("/api/orders/" + order.id());
        return ResponseEntity.created(location).body(OrderResponse.from(order));
    }

    @GetMapping("/{orderId}")
    OrderResponse get(@PathVariable UUID orderId) {
        return OrderResponse.from(getOrder.handle(orderId));
    }
}
```

Use HTTP-method annotations: `@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, `@DeleteMapping`. Use class-level `@RequestMapping` for shared path and media type. Never stack multiple mapping annotations on same method.

Use constructor injection. Controller depends on application boundary, not repository or outbound adapter.

## Request and response models

Use API-specific records. Never bind request body directly into domain object or persistence entity.

```java
record CreateOrderRequest(
        @NotBlank String customerId,
        @NotEmpty List<@Valid CreateOrderLineRequest> lines
) {
    CreateOrderCommand toCommand() {
        return new CreateOrderCommand(customerId, lines.stream()
                .map(CreateOrderLineRequest::toCommand)
                .toList());
    }
}

record CreateOrderLineRequest(
        @NotBlank String productId,
        @Positive int quantity
) {
    CreateOrderLineCommand toCommand() {
        return new CreateOrderLineCommand(productId, quantity);
    }
}

record OrderResponse(UUID id, String status) {
    static OrderResponse from(OrderView order) {
        return new OrderResponse(order.id(), order.status());
    }
}
```

Expose stable API fields only. Do not leak internal type names, database columns, lazy associations, stack traces, or exception messages.

## Input binding

- Use `@PathVariable` for resource identity.
- Use `@RequestParam` for filtering, sorting, pagination, and optional modifiers.
- Use `@RequestHeader` only when header is part of endpoint contract.
- Use `@RequestBody` for JSON command payload.
- Declare `consumes` and `produces` when endpoint contract requires exact media type.
- Prefer typed parameters such as `UUID`, enum, `Instant`, and `LocalDate`; let Spring reject conversion failures.
- Never accept unbounded page size, arbitrary sort property, or client-controlled internal class/property path.

## Validation

Put transport-shape constraints on request records. Use Jakarta Validation and `@Valid` for nested objects.

```java
@GetMapping
List<OrderResponse> find(
        @RequestParam(defaultValue = "0") @PositiveOrZero int page,
        @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size
) {
    return findOrders.handle(page, size).stream().map(OrderResponse::from).toList();
}
```

Handle both `MethodArgumentNotValidException` and `HandlerMethodValidationException`. Do not add class-level `@Validated` to MVC controller when using built-in method validation. `@Valid` alone enables nested validation; direct constraints such as `@Min` trigger method validation.

Transport validation checks syntax and shape. Application or domain validates business invariants.

## Response status

- `200 OK`: successful read or update with body.
- `201 Created`: resource created; include `Location`.
- `202 Accepted`: work accepted but not completed.
- `204 No Content`: successful action with no response body.
- `400 Bad Request`: malformed input, binding, or validation failure.
- `404 Not Found`: requested resource does not exist.
- `409 Conflict`: request conflicts with current resource state.

Use `ResponseEntity` when status or headers vary. Return response body directly when status is fixed `200 OK`. Use `@ResponseStatus` only for fixed status. Never return `200 OK` with error payload.

## Error responses

Use one `@RestControllerAdvice`. Translate known exceptions into stable `ProblemDetail` responses. Keep unexpected exceptions mapped to generic `500` response and logged once.

```java
@RestControllerAdvice
final class ApiExceptionHandler {
    @ExceptionHandler(OrderNotFoundException.class)
    ProblemDetail handleNotFound(OrderNotFoundException exception) {
        var problem = ProblemDetail.forStatusAndDetail(
                HttpStatus.NOT_FOUND,
                "Order was not found"
        );
        problem.setTitle("Order not found");
        problem.setType(URI.create("https://example.com/problems/order-not-found"));
        return problem;
    }

    @ExceptionHandler(OrderConflictException.class)
    ProblemDetail handleConflict(OrderConflictException exception) {
        return ProblemDetail.forStatusAndDetail(
                HttpStatus.CONFLICT,
                "Order conflicts with current state"
        );
    }
}
```

Use stable problem `type`, `title`, `status`, and safe `detail`. Add machine-readable extensions only when clients need them. Never reveal SQL, credentials, stack traces, or internal exception class.

## Collection responses

Do not expose Spring `Page` directly as public contract. Map page result into stable response record.

```java
record PageResponse<T>(
        List<T> items,
        int page,
        int size,
        long totalElements,
        int totalPages
) {}
```

Whitelist sort fields and cap page size. Keep pagination semantics consistent across endpoints.

## Rules

- Use plural resource nouns: `/api/orders`, `/api/orders/{orderId}`.
- Model actions as subresources only when action is not natural CRUD operation.
- Keep controller methods small. Mapping plus one application call preferred.
- Keep API models immutable.
- Preserve backward compatibility for published fields and semantics.
- Do not version API until compatibility need exists. When versioning becomes necessary, choose one consistent strategy.
- Do not catch exceptions inside every controller. Central advice owns HTTP error translation.
- Do not return domain entities or JPA entities.
- Test endpoint contract: route, binding, validation, status, headers, JSON shape, error response.

Sources: [Spring MVC annotated controllers](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller.html), [request mappings](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping.html), [validation](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-validation.html), [exception handlers](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-exceptionhandler.html).
