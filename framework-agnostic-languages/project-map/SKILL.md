---
name: project-map
description: Use at the start of every repository development task, before any other development skill or broad code exploration. Maintain and consult a tiny repo-local `.project-map.md` that routes concepts to files, ownership, flows, and invariants; automatically bootstrap it when absent, update it reactively as durable navigation knowledge changes, and aggressively reconcile/prune it before substantive task completion.
---

# Project Map

Reduce repository rediscovery and read/search tokens. Maintain exactly one navigation cache at `<repo>/.project-map.md`.

The map is a routing cache, not documentation, history, task memory, or source of truth.

## Hard boundaries

- Keep exactly one `.project-map.md`. Do not create indexes, databases, per-module memory files, changelogs, task files, or generated knowledge stores.
- Consult `.project-map.md` before invoking other development skills or broadly exploring source.
- Current source is authoritative. Before editing code, read the actual target files even when the map names them.
- Never recursively scan or broadly read the repository merely to enrich the map.
- Record only verified facts supported by current project evidence. Omit uncertainty rather than storing guesses.
- Use repo-relative paths. Every file reference must include its filename extension, e.g. `AuthenticationService.java`, `package.json`, `routes.ts`; directory references end in `/`.
- Avoid line numbers, copied code, method bodies, large signatures, raw command output, and exhaustive symbol/file lists.
- The map is rewritten knowledge, never an append-only log. Replace stale facts, merge duplicates, and delete low-value entries.
- Never store secrets, credentials, tokens, sensitive values, or private data.
- Target <= 8 KiB. Compact before 12 KiB; exceed that only when the user explicitly prefers coverage over token cost.

## Mandatory preflight

For every repository development task:

1. Resolve the repository root.
2. If `.project-map.md` does not exist, bootstrap it automatically before invoking another development skill or broadly exploring source.
3. Consult `.project-map.md` first. Search it with a few task/domain terms when that is cheaper than reading the whole file; read the whole file when already tiny.
4. Use mapped routes, ownership, flows, and invariants to choose the smallest plausible source shortlist.
5. Inspect current source for the candidates that matter.
6. Fall back to repository `rg`/find/listing/reference searches only when the map is insufficient, stale, or exact usages/callers are required.
7. Keep fallback search narrow. Do not read unrelated matches merely to understand the repository generally.

The map answers **where should I look?** Repository search answers **what exactly exists now?**

## Automatic bootstrap

When `.project-map.md` is absent, initialize it without asking unless the user explicitly forbids repository metadata changes.

Use only cheap evidence already available or cheap to obtain:

- root `README.md` and `AGENTS.md` when present;
- build/workspace manifests such as `pom.xml`, `build.gradle`, `package.json`, `Cargo.toml`, or equivalents;
- top-level directories and at most a shallow directory listing;
- source files that must already be inspected for the current task.

Do not recursively inspect source to make the first map comprehensive. Create a sparse, correct `.project-map.md`, continue the requested task, and let real work enrich it.

A sparse correct map is better than an expensive complete map.

## Reactive maintenance

Maintain the map during substantive work whenever current source establishes or changes a high-value navigation fact. Do not wait for the end if continuing the task with stale routing could cause wrong or redundant exploration.

Update at natural knowledge/change boundaries, not after every read. Typical triggers:

- a file is confirmed to own a behavior or architectural responsibility;
- a better route to a recurring concept is discovered;
- an important cross-file flow becomes clear;
- a non-obvious boundary/invariant is verified;
- a source-of-truth file is identified;
- implementation moves, renames, splits, merges, or changes an existing mapped responsibility/flow.

Reuse evidence already inspected for the task. Never launch a new discovery pass solely to improve the map.

Prefer targeted replacement/merge over append. If new knowledge supersedes an existing entry, rewrite the old entry immediately.

## Admission policy

Admit an entry only if it is likely to prevent a future repository search or unnecessary read.

High-value entries are:

- **Route:** task/concept -> best file, symbol, or area to inspect first.
- **Ownership:** behavior-owning file/module -> responsibility it actually owns.
- **Flow:** important cross-file execution/data path needed to navigate a feature.
- **Boundary/invariant:** non-obvious architectural rule that changes where future work belongs.
- **Source of truth:** file that definitively owns a schema/configuration/contract when that fact prevents repeated hunting.

Be reasonably aggressive about file-level ownership for behavior-owning/routing-important files, but do not summarize every file. File names must include extensions.

Usually reject:

- transient task state, TODO progress, session summaries, or changelog history;
- generic architecture prose or rationale that does not help locate code;
- style rules obvious from surrounding code or enforceable by tools;
- test results, debugging traces, failed experiments, and raw tool output;
- code snippets or facts cheaply visible after opening an already-known target file;
- boilerplate DTOs, exceptions, generated files, trivial adapters, or files whose names already make their role obvious unless they are useful routing targets;
- exhaustive directory trees, every class/function, every caller/reference, or one entry per file by default.

For every candidate line ask: **What future repository search or read is this expected to prevent?** If there is no concrete answer, omit it.

## Completion reconciliation and aggressive pruning

Before the final response for any substantive repository task, feature, bug fix, or refactor, reconcile `.project-map.md` if it exists. This is the mandatory end-of-task maintenance point.

1. Reconcile entries touched by knowledge or code changes in the current task.
2. Add any high-value durable routes/ownership/flows/invariants learned but not yet recorded.
3. Remove or replace stale entries invalidated by current source.
4. Merge duplicate or overlapping entries.
5. Remove low-value facts that do not clearly prevent future exploration.
6. Compress wording while preserving routing information.
7. If the map exceeds 8 KiB, prune aggressively toward the target. Never allow it past 12 KiB without explicit user preference.

Do not perform a repository-wide validation scan at completion. Reconcile from source and changes already inspected during the task. If an untouched map entry might be stale but was not verified, leave it unless current evidence contradicts it.

Also prune immediately when the file crosses the size budget or obvious duplication/staleness is encountered mid-task.

## File format

Use only useful sections; omit empty ones.

```markdown
# Project Map

> Navigation cache. Source files are authoritative.

## Project
<one sentence: what this repository is>

## Areas
- `<path-or-directory>/` — <responsibility>; start: `<EntryFile.ext>`

## Ownership
<area>/
- `<BehaviorOwner.ext>` — <owned behavior/responsibility>
- `<OtherOwner.ext>` — <owned behavior/responsibility>

## Routes
- <task/concept> -> `<FirstFile.ext>` (`OptionalSymbol`) -> `<NextFile.ext>`

## Flows
- <flow>: `<A.ext>` -> `<B.ext>` -> `<C.ext>`

## Invariants
- <non-obvious boundary that changes where code should be read/changed>
```

Keep entries terse, concrete, and optimized for future navigation rather than human-facing explanation.
