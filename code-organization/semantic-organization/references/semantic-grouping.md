# Semantic Grouping

Group code around coherent concepts and capabilities.

## Semantic-name test

For a class, module, file, directory, package, or namespace, ask:

> Can one meaningful semantic name describe almost everything inside this unit?

If yes, the grouping is probably coherent.

If no, the unit probably contains multiple concepts that should be separated.

## Multiple operations may belong together

A semantic unit may expose many operations when those operations belong to the same concept.

For example:

```text
SkillRegistry
├── register
├── unregister
├── find
├── list
└── refresh
```

This is cohesive because every operation belongs to the registry concept.

Do not split these into separate files merely because there are several functions or methods.

## Representation is language-dependent

Use the structure that is natural for the target language and problem.

A concept may be represented as:

- a class with related methods;
- a module exporting related functions;
- a file containing a cohesive set of functions and types;
- a directory containing several related implementation units;
- a package or namespace containing a larger semantic area.

Object orientation is one option, not a requirement.

Classes are especially natural when a concept owns state, dependencies, identity, or lifecycle. Cohesive function modules are often clearer for stateless behavior.

## Split on semantic divergence

Split when a unit starts owning independently meaningful concepts.

For example, a `SkillRegistry` that registers, removes, finds, and lists skills is cohesive. If it also starts parsing GitHub URLs, formatting terminal output, spawning child processes, and managing MCP transports, those behaviors have different semantic owners.

The trigger to split is not:

- line count;
- number of methods;
- number of functions;
- an arbitrary maximum file size.

The trigger is loss of semantic cohesion.

## Avoid generic semantic buckets

Names such as these often indicate missing ownership:

```text
Utils
Helpers
Common
Misc
GeneralService
Manager
```

They are not forbidden, but use them only when the name genuinely describes a coherent concept. Prefer names that reveal what the unit owns.

## Keep tightly related details local

Do not extract tiny helpers, internal mappings, or implementation details when doing so makes the concept harder to understand as a whole.

Locality is valuable. A reader should not need to jump across many files to understand one cohesive behavior.
