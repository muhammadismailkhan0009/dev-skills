# Flyway

Use Flyway as schema authority with Hibernate `ddl-auto: validate`.

## Dependencies

Add Flyway core and the database-specific module. Replace the PostgreSQL module when using another database.

```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-database-postgresql</artifactId>
</dependency>
```

## Configuration

```yaml
spring:
  flyway:
    enabled: true
    baseline-on-migrate: true
    baseline-version: 0 # Use 1 when integrating Flyway into an existing system.
    locations: classpath:db/migration
```

## Migration

Place migrations in `src/main/resources/db/migration`. Use `V<version>__<description>.sql` and never edit an applied migration.

`V1__create_orders.sql`:

```sql
create table orders (
    id uuid primary key,
    status varchar(32) not null,
    total_amount decimal(19, 2) not null,
    total_currency varchar(3) not null
);
```

Adapt SQL types to the selected database. Test the migration chain from an empty production-engine database with Testcontainers.
