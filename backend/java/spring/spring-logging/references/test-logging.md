# Spring Test Logging Suppression

The purpose of this baseline is to keep Spring test output extremely small for LLM-driven development while retaining actual test failure evidence.

All configuration below is mandatory for Spring test environments. Do not remove one suppression layer because another appears to cover the same logger or behavior. The combined baseline intentionally suppresses noise through Spring Boot configuration, Logback test configuration, JPA/Hibernate settings, and Maven Surefire.

## Mandatory Spring Boot test configuration

The effective test configuration must include:

```yaml
debug: false

logging:
  level:
    root: ERROR
    org.springframework: ERROR
    org.springframework.test: ERROR
    org.springframework.boot: ERROR
    org.springframework.security: ERROR
    org.hibernate: ERROR
    org.hibernate.SQL: OFF
    org.testcontainers: ERROR
    com.zaxxer.hikari: ERROR
    org.flywaydb: ERROR

spring:
  main:
    banner-mode: off
  jpa:
    show-sql: false
    properties:
      hibernate:
        format_sql: false
```

Keep these settings test-scoped. Prefer the project's established test configuration convention, such as `src/test/resources/application.yml` or an already-established test profile. What matters is that this exact suppression baseline is effective for test execution.

`spring.jpa.show-sql: false` is mandatory even with `org.hibernate.SQL: OFF`; SQL printing must not escape the normal logging suppression path. `hibernate.format_sql: false` is also mandatory so diagnostic SQL does not become unnecessarily verbose if SQL logging is temporarily enabled.

## Mandatory `logback-test.xml`

Tests must use a test-specific Logback configuration with the following baseline:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} %-5level %logger{36} -- %msg%n</pattern>
        </encoder>
    </appender>

    <logger name="org.springframework" level="ERROR"/>
    <logger name="org.springframework.test" level="ERROR"/>
    <logger name="org.springframework.boot" level="ERROR"/>
    <logger name="org.springframework.security" level="ERROR"/>
    <logger name="org.hibernate" level="ERROR"/>
    <logger name="org.hibernate.SQL" level="OFF"/>
    <logger name="org.testcontainers" level="ERROR"/>
    <logger name="com.zaxxer.hikari" level="ERROR"/>
    <logger name="org.flywaydb" level="ERROR"/>

    <root level="ERROR">
        <appender-ref ref="CONSOLE"/>
    </root>
</configuration>
```

Use `logback-test.xml` rather than weakening production logging configuration. Keep the console pattern compact; do not add thread names, process IDs, application metadata, or other ambient fields unless a concrete diagnostic requirement makes them necessary.

## Mandatory Maven Surefire suppression

The Maven Surefire plugin configuration must set Spring debug mode off for test execution:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <systemPropertyVariables>
            <debug>false</debug>
        </systemPropertyVariables>
    </configuration>
</plugin>
```

If the project already configures `maven-surefire-plugin`, merge this property into the existing plugin configuration. Do not create a duplicate Surefire plugin declaration.

## Runtime rules

A passing test run should contain almost no framework or infrastructure chatter. Preserve Maven/JUnit/Surefire failure information, including failed test names, assertion failures, exceptions, and useful stack traces.

Do not permanently enable broad `DEBUG` or `INFO` logging to diagnose a test. If the quiet baseline is insufficient:

1. Identify the narrow subsystem implicated by the failure.
2. Temporarily raise only that logger for the diagnostic run, for example a specific Hibernate, Spring Security, application, or integration logger.
3. Diagnose and fix the problem.
4. Restore the complete mandatory suppression baseline before completing the task.

Never leave `debug: true`, `spring.jpa.show-sql: true`, Hibernate SQL logging, broad framework debug logging, or equivalent verbose diagnostics enabled after the diagnostic run.

Do not suppress or redirect actual failure evidence merely to reduce tokens. The goal is to eliminate ambient noise so the remaining output is high-signal, not to make failing tests opaque.