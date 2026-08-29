---
name: feature-planning
description: Plan and deliver features through behavior approval, targeted feasibility inspection, layer-gated BDD, and final conformance review. Use for complete feature work driven by an installed development flow. Keep lifecycle language and platform agnostic.
---

# Feature Planning

Own complete feature lifecycle. Platform skills define implementation rules only. Configured development flow supplies relevant layers, their order, and available skills.

```text
request
clarification
behavior flow
conceptual approval
targeted inspection
feasibility reconciliation
frozen baseline
layer BDD and approval gates
conformance review
feature complete
```

## Hard boundaries

- Before conceptual approval, never inspect repository, search code, read project files, inspect Git, or invoke platform skills.
- Before approval, reason only from request, clarification answers, explicit project constraints, and configured development flow.
- Use only development flow already supplied or installed. Never scan repository to discover one.
- Read configured flow only for process constraints, layer vocabulary, and later skill availability. Ignore technical implementation guidance during behavior planning.
- Never choose classes, files, framework annotations, storage mappings, or tests during conceptual planning.
- Never implement before feasibility is confirmed and baseline frozen.
- Keep BDD, orchestration, approval gates, and conformance here. Never push them into language, framework, architecture, adapter, or testing skills.

## Run lifecycle

1. Read [conceptual planning](references/conceptual-planning.md). Stop for conceptual approval.
2. After approval only, read [feasibility and baseline](references/feasibility-and-baseline.md). Inspect relevant code narrowly. Stop if behavior needs adjustment.
3. After feasibility confirmation, read [layer BDD execution](references/layer-bdd-execution.md). Implement only affected layers from configured development flow. Stop after each material layer for approval.
4. After all approved layers, read [conformance review](references/conformance-review.md). Compare observable behavior against frozen baseline.

Do not skip gates because implementation looks small. User may explicitly approve multiple gates together.

## State rules

- Diagram starts as draft.
- Explicit conceptual approval freezes behavior revision.
- Any observable behavior change invalidates approval and creates new draft revision.
- Formatting or internal execution change does not create behavior revision.
- Feasibility confirmation freezes implementation baseline.
- Layer rejection returns only that layer to BDD cycle.
- Feature completes only after conformance review has no unresolved drift or missing behavior.
