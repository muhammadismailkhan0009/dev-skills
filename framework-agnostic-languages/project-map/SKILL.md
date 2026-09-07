---
name: project-map
description: Maintain and use a tiny repo-local `.project-map.md` as a code-navigation cache. Use when file, module, ownership, or execution-flow location is unclear; before broad repository search/read exploration; after substantive work reveals durable navigation knowledge; or when the map needs bootstrap or compaction. Skip map lookup when the exact target file/symbol is already known.
---

# Project Map

Reduce repository rediscovery and read/search tokens. Maintain exactly one navigation file at `<repo>/.project-map.md`.

The map is a routing cache, not documentation, history, task memory, or source of truth.

## Hard boundaries

- Keep exactly one `.project-map.md`. Do not create indexes, databases, per-module memory files, changelogs, task files, or generated knowledge stores.
- Current source is authoritative. Before editing code, read the actual target files even when the map names them.
- Never recursively scan or broadly read the repository merely to enrich the map.
- Record only verified facts supported by current project evidence. Omit uncertainty rather than storing guesses.
- Use repo-relative paths. Avoid line numbers, copied code, method bodies, large signatures, raw command output, and exhaustive symbol/file lists.
- The map is rewritten knowledge, never an append-only log. Replace stale facts, merge duplicates, and delete low-value entries.
- Never store secrets, credentials, tokens, sensitive values, or private data.
- Target <= 8 KiB. Compact before 12 KiB; exceed that only when the user explicitly prefers coverage over token cost.

## Before repository exploration

1. If the user/current context already identifies the exact target file or symbol, skip `.project-map.md` and inspect that source directly.
2. If `.project-map.md` exists and location/ownership is unclear, search it first with a few task/domain terms. Read only the matching section when practical; read the whole file when it is already tiny.
3. Treat mapped paths/symbols as a shortlist. Inspect current source for the candidates that matter.
4. Fall back to repository `rg`/find/listing/reference searches only when the map is missing, insufficient, stale, or the task requires exact usages/callers.
5. Keep fallback search narrow. Do not read unrelated matches just to understand the repository generally.

The map answers **where should I look?** Repository search answers **what exactly exists now?**

## Bootstrap

When the user asks to initialize/bootstrap the map and it does not exist:

1. Use only cheap evidence: root `README`/`AGENTS` when present, build/workspace manifests, top-level directories, and at most a shallow directory listing.
2. Do not recursively inspect source to make the first map comprehensive.
3. Create `.project-map.md` with only confirmed high-level routing information.
4. Leave unknown areas absent. Let later real tasks enrich the map opportunistically.

A sparse correct map is better than an expensive complete map.

## Maintain after substantive work

At task completion, update `.project-map.md` only when the work produced durable navigation knowledge or invalidated an existing entry. Reuse evidence already inspected for the task; do not launch a new discovery pass just to update the map.

Admit an entry only if it is likely to prevent a future search/read. High-value entries are:

- **Route:** task/concept -> best file, symbol, or area to inspect first.
- **Ownership:** file/module -> responsibility it actually owns.
- **Flow:** important cross-file execution/data path needed to navigate a feature.
- **Boundary/invariant:** non-obvious architectural rule that changes where future work belongs.
- **Source of truth:** a file that definitively owns a schema/configuration/contract when that fact prevents repeated hunting.

Usually reject:

- transient task state, TODO progress, session summaries, or changelog history;
- generic architecture prose or rationale that does not help locate code;
- style rules obvious from surrounding code or enforceable by tools;
- test results, debugging traces, failed experiments, and raw tool output;
- code snippets or facts cheaply visible after opening an already-known target file;
- exhaustive directory trees, every class/function, every caller/reference, or one entry per file by default.

For every candidate line ask: **What future repository search or read is this expected to prevent?** If there is no concrete answer, omit it.

## Staleness and compaction

When source contradicts the map, trust source and correct the map if the fact remains useful. When files move or responsibilities change, replace affected entries rather than preserving history.

When compacting, prefer in this order:

1. remove stale entries;
2. remove facts obvious from names or already-known target files;
3. merge duplicate routes/ownership statements;
4. shorten prose to path + responsibility/relationship;
5. remove the least reusable details.

Do not sacrifice a high-value route merely to preserve low-value coverage.

## File format

Use only useful sections; omit empty ones.

```markdown
# Project Map

> Navigation cache. Source files are authoritative.

## Project
<one sentence: what this repository is>

## Routes
- <task/concept> -> `<path>` (`Symbol`) -> <optional next path/symbol>

## Areas
- `<path-or-directory>` — <responsibility>; start: `Symbol` or `<file>`

## Flows
- <flow>: `A` -> `B` -> `C`

## Invariants
- <non-obvious boundary that changes where code should be read/changed>
```

Keep entries terse, concrete, and optimized for future navigation rather than human-facing explanation.
