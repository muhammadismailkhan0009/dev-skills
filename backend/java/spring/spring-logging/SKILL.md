---
name: spring-logging
description: Minimize Spring test logging for LLM-driven development. Use when configuring or running Spring tests so framework, persistence, container, pool, migration, banner, SQL, and debug noise stay suppressed while real test failures remain visible.
---

# Spring Logging

Keep automated Spring test output minimal because test logs are consumed by LLM-driven development workflows.

For every Spring test setup or change that can affect test logging, read [test logging](references/test-logging.md) and enforce its complete suppression baseline. All listed Spring Boot logging, JPA, Logback test, and Maven Surefire settings are mandatory; do not treat duplicated suppression across layers as redundant configuration to remove.

Preserve useful failure evidence: failed test names, assertion failures, exceptions, and relevant stack traces must remain visible. Suppress ambient framework/infrastructure chatter, not diagnostic evidence from an actual failing test.

If a failure cannot be diagnosed under the quiet baseline, temporarily raise only the narrow logger needed for that diagnostic run. Restore the mandatory quiet baseline before completing the work. Never leave broad DEBUG/INFO logging or SQL output enabled after diagnosis.