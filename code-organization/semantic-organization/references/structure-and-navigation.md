# Structure and Navigation

Use the filesystem to expose semantic ownership and reduce the amount of architecture a reader must reconstruct mentally.

## Directories are semantic containers

A directory may represent a larger concept or capability and contain several related files.

For example:

```text
skills/
├── registry/
├── installation/
└── sources/
```

or:

```text
skills/
├── skill-registry.ts
├── skill-installer.ts
└── skill-source.ts
```

Both are valid. Choose the shape that makes ownership easiest to understand in the target language and at the current scale.

Do not create a directory merely because a file exists. Create one when grouping several related implementation units under a shared concept improves navigation.

## Prefer structural locality

Code that changes together because it belongs to the same concept should usually live near each other.

Avoid scattering one semantic capability across unrelated top-level folders unless architectural boundaries explicitly require it.

## Avoid unnecessary fragmentation

Do not default to one-function-per-file organization.

This:

```text
registry/
├── register.ts
├── unregister.ts
├── find.ts
├── list.ts
└── refresh.ts
```

is usually worse than one cohesive registry module/class when the operations are small and share one semantic owner.

Split further only when parts become independently meaningful or complex enough to form their own concepts.

## Avoid meaningless catch-all directories

Directories such as these provide little navigation value when they mix unrelated concepts:

```text
utils/
helpers/
services/
common/
misc/
```

Prefer semantic directories such as:

```text
registry/
repository/
authentication/
configuration/
mcp/
jobs/
```

A generic directory can still be appropriate when its contents truly share one meaning; judge by semantic ownership, not naming dogma.

## Keep depth proportional to meaning

Do not create nested directories simply to mirror every class or function.

Prefer shallow grouping until a concept becomes complex enough to justify another semantic level.

## Optimize for prediction

A codebase is well organized when a developer can usually answer:

> Where would I expect code for this concept to live?

without searching broadly.

When the answer is unclear, improve names, grouping, or locality before adding more abstraction.
