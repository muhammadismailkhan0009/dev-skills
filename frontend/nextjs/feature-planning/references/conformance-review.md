# Conformance review

Run after every affected layer is approved. Compare frozen baseline against observable implementation and scenario evidence.

Use behavior, not implementation shape, as review unit.

```text
Behavior: B4
Approved: Exclude known vocabulary
Implementation: [owning implementation responsibility]
Evidence: Known-vocabulary exclusion scenario
Status: complete
```

Every behavior gets one status:

- `complete`: implementation and evidence match baseline
- `missing`: approved behavior lacks implementation or evidence
- `drift`: implementation adds or changes observable behavior
- `blocked`: evidence cannot be established

Component, function, class, file, package, query strategy, mapping choice, refactor, or other internal detail is not drift unless it changes observable behavior or an approved assumption.

## Drift decisions

- `accept`: create revised final behavior baseline
- `remove`: remove unapproved behavior through affected layer BDD cycle
- `complete`: implement missing approved behavior through affected layer BDD cycle

Do not mark feature complete while decision is unresolved.

Final output:

```text
Conformance: passed
Behaviors: B1 complete, B2 complete, B3 complete, B4 complete
Missing behavior: none
Additional behavior: none
Unresolved drift: none
```

When review fails, report only affected IDs, concrete mismatch, evidence, and required decision. Do not regenerate implementation plan.