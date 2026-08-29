# Entity Mapping

Keep JPA model in `infrastructure/persistence`. Domain model remains plain Java. Persistence entities represent database shape; mapper translates complete aggregates at adapter boundary.

## Typed primary key

Represent aggregate ID as embeddable persistence value and use `@EmbeddedId`.

```java
@Embeddable
record OrderEntityId(
        @Column(name = "id", nullable = false, updatable = false)
        UUID value
) implements Serializable {
    OrderEntityId {
        Objects.requireNonNull(value, "value");
    }
}
```

ID generation belongs outside persistence entity when domain/application owns identity. Map domain ID explicitly to persistence ID.

## Composite primary keys

Use composite key only when database identity genuinely consists of multiple columns. JPA supports `@IdClass` and `@EmbeddedId`.

### `@IdClass`

Use `@IdClass` when entity frequently queries or exposes individual key fields. Key field names and Java types must match between ID class and entity.

```java
public final class EnrollmentEntityId implements Serializable {
    private UUID studentId;
    private UUID courseId;

    public EnrollmentEntityId() {}

    public EnrollmentEntityId(UUID studentId, UUID courseId) {
        this.studentId = Objects.requireNonNull(studentId, "studentId");
        this.courseId = Objects.requireNonNull(courseId, "courseId");
    }

    @Override
    public boolean equals(Object other) {
        return this == other
                || other instanceof EnrollmentEntityId that
                && Objects.equals(studentId, that.studentId)
                && Objects.equals(courseId, that.courseId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(studentId, courseId);
    }
}
```

```java
@Entity
@Table(name = "enrollments")
@IdClass(EnrollmentEntityId.class)
class EnrollmentEntity {
    @Id
    @Column(name = "student_id", nullable = false, updatable = false)
    private UUID studentId;

    @Id
    @Column(name = "course_id", nullable = false, updatable = false)
    private UUID courseId;

    protected EnrollmentEntity() {}
}
```

`@IdClass` duplicates key declarations but keeps JPQL paths flat, such as `enrollment.studentId`.

### `@EmbeddedId`

Prefer `@EmbeddedId` when composite identity is treated as one value. Use record for embeddable key.

```java
@Embeddable
public record EnrollmentEntityId(
        @Column(name = "student_id", nullable = false, updatable = false) UUID studentId,
        @Column(name = "course_id", nullable = false, updatable = false) UUID courseId
) implements Serializable {
    public EnrollmentEntityId {
        Objects.requireNonNull(studentId, "studentId");
        Objects.requireNonNull(courseId, "courseId");
    }
}
```

```java
@Entity
@Table(name = "enrollments")
class EnrollmentEntity {
    @EmbeddedId
    private EnrollmentEntityId id;

    protected EnrollmentEntity() {}
}
```

`@EmbeddedId` avoids duplicate key declarations. JPQL traverses key object, such as `enrollment.id.studentId`.

For both forms, key type must be public, serializable, immutable in practice, and implement value equality. Do not use relationships or generated mutable values inside composite key. Spring Data repository ID type is composite key class.

## Aggregate entity

Define table and every column explicitly. Provide protected no-argument constructor for JPA and package-private constructor containing all required persistence state.

```java
@Entity
@Table(name = "orders")
class OrderEntity {
    @EmbeddedId
    private OrderEntityId id;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private OrderStatusCode status;

    @Embedded
    @AttributeOverrides({
            @AttributeOverride(name = "amount", column = @Column(name = "total_amount", nullable = false)),
            @AttributeOverride(name = "currency", column = @Column(name = "total_currency", nullable = false, length = 3))
    })
    private MoneyColumns total;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    @OrderColumn(name = "line_position")
    private List<OrderLineEntity> lines = new ArrayList<>();

    protected OrderEntity() {}

    OrderEntity(OrderEntityId id, OrderStatusCode status, MoneyColumns total) {
        this.id = Objects.requireNonNull(id, "id");
        this.status = Objects.requireNonNull(status, "status");
        this.total = Objects.requireNonNull(total, "total");
    }

    void replaceLines(Collection<OrderLineEntity> replacement) {
        lines.clear();
        replacement.forEach(this::addLine);
    }

    private void addLine(OrderLineEntity line) {
        line.attachTo(this);
        lines.add(line);
    }
}
```

Persistence methods maintain association consistency only. Business behavior stays in domain objects.

## Embedded values

Use `@Embeddable` for columns that form one persistence concept. Validate required constructor inputs. Override column names at embedding site so schema remains explicit.

```java
@Embeddable
record MoneyColumns(BigDecimal amount, String currency) {
    MoneyColumns {
        Objects.requireNonNull(amount, "amount");
        Objects.requireNonNull(currency, "currency");
    }
}
```

## Mapping rules

- Use `jakarta.persistence` annotations.
- Prefer records for embeddable IDs and value mappings. Validate required components in compact constructor.
- Embeddable records do not need a no-argument constructor; JPA entities still do.
- Use `EnumType.STRING`; use `AttributeConverter` for stable database codes when Java enum names may change.
- Default associations to `LAZY`. Map only relationships required to persist aggregate.
- Use cascade and orphan removal only for children whose lifecycle belongs to aggregate root.
- Keep mutable collection field private; never return it directly.
- Maintain both sides of bidirectional relationship in one helper.
- Use `@OrderColumn` only when collection order is business-significant and must round-trip.
- Avoid entity callbacks for domain behavior, event publication, or external calls.
- Avoid Lombok `@Data` on entities; generated equality, hash code, and `toString` can traverse lazy associations.
- Keep embedded ID components immutable. Record equality and hash code provide value semantics.
- Map explicitly or with MapStruct. Mapper must preserve identity, required state, children, and meaningful ordering.
