---
name: mapstruct
description: Configure compile-time Java mappings with MapStruct. Use for domain models, persistence entities, commands, or DTOs. Do not use for business logic or external calls.
---

# MapStruct

Use MapStruct for structural conversion only. Keep business decisions, validation, persistence access, external calls outside mappers.

## Maven setup

```xml
<dependency>
    <groupId>org.mapstruct</groupId>
    <artifactId>mapstruct</artifactId>
    <version>${mapstruct.version}</version>
</dependency>
```

Add processor to compiler plugin. Without processor, mapper implementations do not generate.

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <annotationProcessorPaths>
            <path>
                <groupId>org.mapstruct</groupId>
                <artifactId>mapstruct-processor</artifactId>
                <version>${mapstruct.version}</version>
            </path>
        </annotationProcessorPaths>
    </configuration>
</plugin>
```

Use stable version compatible with project Java version. Add other processors only when project needs them.

## Shared configuration

```java
@MapperConfig(
        componentModel = MappingConstants.ComponentModel.SPRING,
        injectionStrategy = InjectionStrategy.CONSTRUCTOR,
        unmappedTargetPolicy = ReportingPolicy.ERROR
)
interface MappingConfiguration {}
```

Use default component model without DI container. Inject Spring mappers. Do not use `Mappers.getMapper` with Spring component model.

## Essential patterns

### Basic mapper

```java
@Mapper(config = MappingConfiguration.class, uses = OrderLineMapper.class)
interface OrderMapper {
    @Mapping(target = "id", source = "id.value")
    @Mapping(target = "total", source = "total.amount")
    OrderResponse toResponse(Order source);

    List<OrderResponse> toResponses(Collection<Order> source);
}
```

Same-name properties map implicitly. Declare mappings when names differ, source is nested, or target is intentionally ignored. Records map through canonical constructor.

### Renamed, nested, ignored, constant values

```java
@Mapping(target = "customerName", source = "customer.name")
@Mapping(target = "createdAt", source = "submittedAt")
@Mapping(target = "status", constant = "PENDING")
@Mapping(target = "internalNote", ignore = true)
OrderResponse toResponse(Order source);
```

Use `constant` for fixed target value. Use `defaultValue` for simple fallback when source property is null. Keep intentional omissions visible.

For allowlisted output, use explicit mode:

```java
@BeanMapping(ignoreByDefault = true)
@Mapping(target = "id", source = "id.value")
@Mapping(target = "name", source = "name")
OrderSummary toSummary(Order source);
```

Use `ignoreByDefault` for deliberately narrow output, not normal mapping. Only declared fields map.

### Flattening and nesting

```java
@Mapping(target = ".", source = "customer")
@Mapping(target = ".", source = "address")
@Mapping(target = "name", source = "customer.name")
CustomerView toView(CustomerAggregate source);
```

Use `target = "."` to flatten nested bean into current target. Resolve collisions explicitly. For deep mapping, prefer focused nested mapper over many fragile dotted paths.

### Multiple sources

```java
@Mapping(target = "id", source = "order.id")
@Mapping(target = "requestedBy", source = "actor.username")
OrderCommand toCommand(OrderRequest order, Actor actor);
```

Qualify ambiguous property with parameter name. MapStruct returns null only when every source parameter is null. Define explicit behavior when contract differs.

Map whole source parameter when target field needs source object:

```java
@Mapping(target = "volume", source = "source")
FishTankVolumeDto toVolume(FishTank source);
```

### Custom mapper methods

Use interface default method for small handwritten conversion. Use abstract mapper class when mapper needs fields or broader custom implementation. Generated mapping calls compatible handwritten method automatically.

```java
@Mapper(config = MappingConfiguration.class)
interface CustomerMapper {
    CustomerResponse toResponse(Customer source);

    default String map(CustomerName name) {
        return name == null ? null : name.value();
    }
}
```

### Conversions and qualifiers

```java
@Mapper(config = MappingConfiguration.class)
interface MoneyMapper {
    @Named("minorUnits")
    default long toMinorUnits(Money money) {
        return money.amount().movePointRight(money.currency().getDefaultFractionDigits()).longValueExact();
    }
}

@Mapper(config = MappingConfiguration.class, uses = MoneyMapper.class)
interface OrderMapper {
    @Mapping(target = "totalMinorUnits", source = "total", qualifiedByName = "minorUnits")
    OrderResponse toResponse(Order source);
}
```

Use `uses` for focused child/value mappers. Use qualifiers when same source and target types have multiple conversions. Prefer custom qualifier annotations over `@Named` when refactoring safety matters. Keep conversions deterministic, side-effect free.

MapStruct supports common primitive, wrapper, string, enum, date, and number conversions. Use `dateFormat` or `numberFormat` when representation is contract-defined. Avoid silent narrowing; add checked conversion when overflow or precision matters.

### Collections and maps

```java
OrderLineResponse toResponse(OrderLine source);

List<OrderLineResponse> toResponses(List<OrderLine> source);
```

Declare element and collection methods. MapStruct generates iteration and reuses matching element method. Null collection returns null by default. Use `NullValueMappingStrategy.RETURN_DEFAULT` only when contract requires empty collection.

Maps follow same pattern:

```java
@MapMapping(valueDateFormat = "yyyy-MM-dd")
Map<String, String> toResponse(Map<Long, LocalDate> source);
```

MapStruct converts each key and value. Declare format or qualifier when implicit conversion does not express contract.

### Enums

```java
@ValueMapping(source = "IN_PROGRESS", target = "PROCESSING")
@ValueMapping(source = MappingConstants.ANY_REMAINING, target = "UNKNOWN")
OrderStatusResponse toResponse(OrderStatus source);
```

Same-name constants map automatically. Declare renamed values. Use catch-all only when target contract tolerates unmatched or new source values. Otherwise, let compilation expose incomplete mapping.

Use `@EnumMapping` name transformation only for systematic prefix, suffix, or case differences. Prefer explicit `@ValueMapping` when exceptions exist.

### Inverse mapping

```java
@Mapping(target = "customerName", source = "customer.name")
OrderResponse toResponse(Order source);

@InheritInverseConfiguration(name = "toResponse")
Order toDomain(OrderResponse source);
```

Use inverse inheritance only for symmetric conversion. Constants, expressions, defaults, ignored properties are not reliably reversible. Map those explicitly.

### Partial updates and presence checks

```java
@BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
void apply(UpdateCustomerCommand source, @MappingTarget CustomerEntity target);
```

Use `IGNORE` when null means “not provided.” Do not use when null means “clear value.” Model absence separately when both meanings exist. Review collection behavior: configured strategy may replace, clear, or append.

Use condition for presence rule beyond null:

```java
@Condition
default boolean hasText(String value) {
    return value != null && !value.isBlank();
}
```

Keep condition narrow. Qualify it when not every matching property should use same rule.

### Context parameters

```java
OrderResponse toResponse(Order source, @Context Locale locale);
```

Use `@Context` for caller-supplied state needed by custom mapping, factory, or lifecycle method. Declare same context through called mapping methods. Never use it to hide persistence or network access. Caller must not pass null when context callbacks dereference it; MapStruct adds no context null check.

### Polymorphic mappings

```java
@SubclassMapping(source = CardPayment.class, target = CardPaymentResponse.class)
@SubclassMapping(source = BankPayment.class, target = BankPaymentResponse.class)
PaymentResponse toResponse(Payment source);
```

Use `@SubclassMapping` for closed, intentional subtype conversion. Decide unknown-subtype behavior explicitly. Do not combine subclass mapping with update methods.

### Object creation

MapStruct uses accessible constructors and supported builders. Records use canonical constructors. Use `@ObjectFactory` when construction needs factory:

```java
@ObjectFactory
CustomerEntity create(CreateCustomerCommand source) {
    return new CustomerEntity(source.id());
}
```

Factory handles construction only. Business decisions stay in application or domain code.

### Before and after hooks

Use `@BeforeMapping` or `@AfterMapping` only for mapper-local technical adjustments. Callback may live in mapper, `uses` type, or context type.

```java
@AfterMapping
default void normalize(@MappingTarget CustomerResponse target) {
    target.setDisplayName(target.getDisplayName().trim());
}
```

Prefer named conversion method when one property needs change. Never perform persistence writes or external calls from callback.

### Mapping reuse

Use `@MapperConfig` for shared component model, injection strategy, reporting policy, reusable prototypes. Use `@InheritConfiguration` when create/update methods share method mappings. Avoid broad inheritance hiding contract differences.

Custom meta-annotations can compose repeated `@Mapping` declarations. Use only when participating source and target types share stable property contract; errors hide composition context. Prefer `@InheritConfiguration` for type-safe reuse.

## Rules

- Fail compilation for unmapped target properties. Use `ignore = true` only for intentional omission.
- Prefer explicit methods over complex `expression = "java(...)"`. Move non-trivial conversion into named helper or dedicated mapper.
- Use `defaultExpression` or `expression` only for small Java expression. MapStruct validates expression during generated-code compilation, not annotation processing.
- Use `@MappingTarget` only for intentional updates. Set null-property behavior explicitly.
- Null source normally returns null. Override only when contract requires other result.
- Do not expose persistence entities merely to avoid mapping.
- Compile project so annotation processing runs. Never edit generated mapper.
- Inspect generated code when null behavior, constructor selection, collection handling, or chosen conversion is unclear.
- Test custom conversions, qualifiers, factories, asymmetric inverse mappings, partial-update/null behavior. Skip tests for trivial generated field copies.

Source: [MapStruct stable reference guide](https://mapstruct.org/documentation/stable/reference/html/).
