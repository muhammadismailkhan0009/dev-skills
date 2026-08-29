# Feasibility and baseline

Start only after explicit conceptual approval.

## Targeted inspection

Inspect only code needed to answer whether approved behavior fits current system. Use configured development flow to identify relevant code and possible layers. Invoke no production-generation step yet.

Check:

- Existing relevant behavior flow
- Available application and domain boundaries
- Required data or dependency availability
- Constraints that may change observable behavior
- Affected implementation layers

Do not produce file inventory, class plan, pseudocode, implementation task list, or second planning essay.

## Feasibility output

When approved behavior fits:

```text
Feasibility: confirmed
Affected layers: domain, service, JPA, API
Relevant existing flow: VocabularyCandidateExtraction
Material conflict: none
```

When adjustment is required:

```text
Feasibility: adjustment required
Conflict: [specific conflict]
Affected behavior: B4
Proposed correction: [compact correction]
```

If internal execution changes but observable behavior remains identical, keep approved diagram. Record internal correction in implementation baseline.

If behavior, failure path, side effect, inclusion, exclusion, or material assumption changes, create revised diagram and return to conceptual approval.

## Freeze baseline

After `Feasibility: confirmed`, freeze:

- Approved diagram and revision
- Material assumptions
- Inclusions and exclusions
- Affected layers
- Relevant existing flow
- Approved internal feasibility corrections

Configured development flow owns storage location. If it defines none, keep baseline as explicit conversation artifact. Never invent repository path during language-agnostic lifecycle.

No implementation begins before baseline exists.
