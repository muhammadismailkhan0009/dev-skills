# Configuration and Transactions

Use production migrations as schema authority. Set Hibernate schema generation to validation outside disposable local experiments.

```yaml
spring:
  jpa:
    open-in-view: false
    hibernate.ddl-auto: validate
    generate-ddl: false
    show-sql: false
  datasource:
    url: ${DATABASE_URL}
    username: ${DATABASE_USERNAME}
    password: ${DATABASE_PASSWORD}
```

Put transaction boundary on application use case with `@Transactional`. Use `@Transactional(readOnly = true)` for read use cases. Do not rely on Open Session in View.

## Performance

- Detect N+1 queries through integration tests and SQL metrics, then choose explicit fetch plan.
- Batch writes only when generated-ID strategy and driver support batching.
- Keep transactions short; never perform slow network calls inside DB transaction without explicit consistency need.
- Index columns used by real filters, joins, uniqueness, and stable sorting. Verify with database query plan for important queries.
- Use optimistic locking by default for conflicting aggregate updates. Handle `OptimisticLockingFailureException` at application boundary according to use-case policy.

Test mappings, queries, migrations, constraints, and locking against production database engine through Testcontainers.
