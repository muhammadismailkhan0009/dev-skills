# Layer BDD execution

Configured development flow chooses affected layers, order, and platform skills. This lifecycle owns BDD and approval gates. Never require platform skills to contain these rules.

## Trace behavior to evidence

Map approved behavior IDs to scenarios many-to-many:

- One scenario may prove several behavior IDs.
- One behavior may need several scenarios.
- Every approved behavior needs evidence at most useful boundary.
- Do not duplicate same scenario across layers without distinct boundary risk.

## Execute one layer

For next affected layer:

1. Select approved behaviors layer must prove.
2. Write Given-When-Then scenarios before new or changed behavior.
3. Run scenarios and confirm meaningful failure.
4. Implement minimum behavior using layer skill selected by configured flow.
5. Run scenarios until passing.
6. Remove unnecessary code without changing approved behavior.
7. Run relevant broader checks.
8. Report layer result and stop for approval.

For existing behavior or refactor, confirm existing evidence or add characterization scenario. Do not force artificial failing test.

Tests remain language and platform specific. BDD lifecycle remains here; selected testing skill supplies concrete tools and patterns.

## Layer report

Keep report reviewable:

```text
Layer: domain
Implemented behaviors: B3, B4
Scenarios: selects unknown candidate; excludes known candidate
Result: passing
Material files: [created or materially changed files]
Deviation: none
Awaiting layer approval.
```

Report new assumption or deviation. If it changes observable behavior, stop implementation and return to conceptual revision. If internal only, add it to implementation baseline.

Apply review gates only to materially changed layers. User may approve several completed layers together explicitly. Rejected layer returns to its BDD cycle; later layers remain blocked.
