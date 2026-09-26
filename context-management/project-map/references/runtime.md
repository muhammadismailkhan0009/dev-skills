# Project Context Runtime

Reduce repository rediscovery, repeated design decisions, and read/search tokens. Maintain two compact durable project-context artifacts:

- `<repo>/.project-map.md` — navigation memory: where relevant behavior, ownership, flows, and sources of truth live.
- `<repo>/.project-decisions.md` — engineering-decision memory: how this project should be structured, implemented, tested, and operated.

The map is a routing cache, not documentation, history, task memory, or source of truth. The decisions file is current engineering policy, not a changelog, ADR history, or task/session memory.

## Hard boundaries

- Keep exactly one `.project-map.md` and one `.project-decisions.md`. Do not create additional indexes, databases, per-module memory files, changelogs, task files, or generated knowledge stores unless another explicit context-management skill owns them.
- Consult the injected/current `.project-map.md` for navigation and `.project-decisions.md` for durable engineering constraints before invoking other development skills or broadly exploring source.
- Except for first-time bootstrap when either file is missing, do not maintain/rewrite project context before or during the primary requested work. Finish the user's requested repository work first; reconcile durable context afterward.
- Current source/config/tests are authoritative for what is actually implemented; explicit current user/team decisions are authoritative for intended engineering policy. Before editing code, read the actual target files even when the map names them.
- Never recursively scan or broadly read the repository merely to enrich or validate project context.
- Map entries require verified current project evidence. Decision entries require an explicit current user/team decision or accepted current project evidence. Omit uncertainty rather than storing guesses.
- Every physical file reference must include its filename extension, e.g. `AuthenticationService.java`, `package.json`, `routes.ts`. Default to the bare filename. Add only the shortest path needed when the filename is ambiguous in the repository or when path context materially improves routing. Do not repeat long physical paths when a filename or short disambiguating path is sufficient. Directory references end in `/`.
- Routes point to physical files or directories, not bare class/interface/method symbols.
- Avoid line numbers, copied code, method bodies, large signatures, raw command output, and exhaustive symbol/file lists.
- Both files are rewritten current knowledge, never append-only logs. Replace stale facts, merge duplicates, and delete low-value entries.
- Never store secrets, credentials, tokens, sensitive values, or private data.
- Map budget: target <= 8 KiB; prune aggressively above 8 KiB; never exceed 12 KiB without explicit user preference.
- Decisions budget: target <= 6 KiB; prune aggressively above 8 KiB; never exceed 12 KiB without explicit user preference.
- Do not duplicate the same fact across both files. Put location/routing knowledge in the map and durable implementation policy in decisions.

## Mandatory preflight

For every repository development task:

1. Resolve the repository root.
2. If `.project-map.md` or `.project-decisions.md` does not exist, bootstrap the missing artifact automatically using the project-map installation reference before invoking another development skill or broadly exploring source.
3. Use hook-injected project context first when available. If hooks are unavailable/untrusted, consult both files directly.
4. Use mapped routes, ownership, flows, and invariants to choose the smallest plausible source shortlist.
5. Apply durable project decisions when choosing architecture, code organization, testing, runtime, tooling, contracts, and project-specific conventions.
6. Perform the user's requested work normally using current source/config/tests and explicit current user decisions as authority.
7. Fall back to repository `rg`/find/listing/reference searches only when the map is insufficient, stale, or exact usages/callers are required.
8. Keep fallback search narrow. Do not read unrelated matches merely to understand the repository generally.
9. Do not rewrite either context file yet. Retain useful navigation knowledge and durable engineering decisions learned during the work for end-of-turn reconciliation.

The map answers **where should I look?** The decisions file answers **how should this project be built?** Repository source/config/tests answer **what is actually implemented now?**

## During the requested work: observe, do not maintain

While analyzing, coding, debugging, testing, reviewing, or otherwise performing the user's requested repository work:

- use the map for navigation;
- trust current source over map contents;
- note useful navigation facts, map misses, stale entries, ownership discoveries, flows, invariants, moves/renames, and source-of-truth files as they become evident;
- note durable engineering decisions established, changed, confirmed, or contradicted during the turn, especially explicit user decisions;
- treat all repository evidence encountered during the turn as eligible, regardless of whether it belongs to the requested feature or changed files;
- do not interrupt the primary task merely to update either context file;
- do not run extra searches solely to improve project context.

If either artifact is stale during the task, follow current source/config/tests and explicit current user direction, then remember the correction for end-of-turn reconciliation.

## Admission policy

Admit an entry only if it is likely to prevent a future repository search or unnecessary read.

High-value entries are:

- **Route:** task/concept -> best physical file(s) or area to inspect first.
- **Ownership:** behavior-owning file/module -> responsibility it actually owns.
- **Flow:** important cross-file execution/data path needed to navigate a feature.
- **Boundary/invariant:** non-obvious architectural rule that changes where future work belongs.
- **Source of truth:** file that definitively owns a schema/configuration/contract when that fact prevents repeated hunting.

Be reasonably aggressive about file-level ownership for behavior-owning/routing-important files, but do not summarize every file. File references must include extensions. Prefer `File.ext`; add a short path only when needed to disambiguate or when that path itself carries useful routing information.

Usually reject:

- transient task state, TODO progress, session summaries, or changelog history;
- generic architecture prose or rationale that does not help locate code;
- style rules obvious from surrounding code or enforceable by tools;
- test results, debugging traces, failed experiments, and raw tool output;
- code snippets or facts cheaply visible after opening an already-known target file;
- boilerplate DTOs, exceptions, generated files, trivial adapters, or files whose names already make their role obvious unless they are useful routing targets;
- exhaustive directory trees, every class/function, every caller/reference, or one entry per file by default.

For every candidate line ask: **What future repository search or read is this expected to prevent?** If there is no concrete answer, omit it.

### Admission scoring

Use this internal score when value is unclear. Do not write scores into `.project-map.md`.

- +3 directly routes a likely future task to source.
- +2 identifies non-obvious behavioral ownership.
- +2 can avoid tracing/searching multiple files.
- +1 identifies a non-obvious source of truth or architectural boundary.
- +1 is likely to recur across future work.
- -2 is obvious from the filename/directory name.
- -2 is recoverable with one cheap, narrow search.
- -3 is task-specific, transient, or historical.
- -3 substantially duplicates an existing entry.
- -4 needs verbose explanation to be useful.

Normally admit only candidates scoring **>= 2**. Prefer the highest-value compressed statement when several candidates encode the same routing knowledge.

## Project decisions admission policy

Admit a decision only when forgetting it could cause a future agent to structure, implement, test, integrate, or operate the project differently.

High-value decisions include:

- **Architecture:** chosen boundaries, module/layer conventions, dependency direction, or project-specific architecture constraints.
- **Code organization/style:** durable semantic-grouping, naming, placement, or implementation conventions that are not safely inferable from one nearby file.
- **Testing:** unit/integration/e2e boundaries, mocking policy, test-environment choices, or required real-boundary coverage.
- **Runtime/tooling:** durable module-system, process, build, logging, configuration, packaging, or protocol rules.
- **Contracts/data:** durable schema/API compatibility, persistence, serialization, validation, or migration rules.
- **Project-specific conventions:** explicit user/team decisions that materially constrain future implementation.

Explicit current user decisions are strong admission evidence. Current accepted configuration, tests, and source may also establish or contradict a decision.

Usually reject:

- transient task progress, TODOs, next actions, or session summaries;
- current test pass/fail status, debugging traces, failed experiments, or raw tool output;
- facts whose only value is locating a file (put those in the map);
- obvious language/framework defaults unless this project intentionally chose or deviated from them;
- copied skill text or generic best practices with no project-specific commitment;
- decisions already obsolete or contradicted by current project evidence;
- historical sequences such as “first A, then B, then C” when only C governs current work.

For every candidate ask: **Would forgetting this change how a future agent would implement or review this project?** If no, omit it.

Store current truth, not decision history. When a decision changes, replace the old rule. Preserve a terse rationale only when it prevents likely future reversal or misunderstanding.

## Learn from map misses

A **map miss** occurs when preflight cannot route the task sufficiently and fallback repository exploration is required to discover where relevant behavior lives.

During the primary task, do not stop to maintain the map. At end-of-turn reconciliation, for each meaningful fallback sequence ask:

1. What navigation question was the fallback trying to answer?
2. Did the map lack a route, ownership fact, flow, invariant, or source-of-truth pointer?
3. What is the smallest verified entry that would likely have avoided the same fallback next time?
4. Does that entry pass the admission policy and score?

If yes, include it in the end-of-turn rewrite. Do not record the search transcript or every discovered file.

Classify misses mentally when useful:

- **Route miss:** concept/task language did not point to the right source.
- **Ownership miss:** area was known but behavior-owning file was unclear.
- **Flow miss:** one file was known but important cross-file traversal still had to be rediscovered.
- **Stale-map miss:** an existing route/ownership/flow no longer matched source.
- **Novel exploration:** genuinely new knowledge with little expected reuse; usually do not store it.

The goal is for repeated work to pay progressively less repository-rediscovery cost.

## Compression by ownership

Prefer dense behavioral ownership over multiple descriptive facts.

Collapse facts such as:

```text
AuthenticationService.java handles login
AuthenticationService.java handles logout
AuthenticationService.java coordinates refresh tokens
```

into:

```text
`AuthenticationService.java` — login/logout/refresh orchestration
```

Rules:

- Group closely related responsibilities owned by the same file into one terse line.
- Keep distinctions only when they route future tasks differently.
- Prefer `File.ext — ownership` over sentences explaining implementation. If duplicate filenames make that ambiguous, use the shortest disambiguating path, e.g. `authentication/TokenService.java`, not the full physical path by default.
- Prefer one route to a behavior-owning file over lists of adjacent files.
- Keep a flow only when its sequence itself prevents future tracing.
- If a route and ownership line duplicate each other, keep both only when the route adds useful user-language aliases or traversal order.

Compression must preserve retrieval value, not prose completeness.

## Mandatory end-of-turn reconciliation and rewrite

After the user's requested repository work for the current prompt is complete, but before sending the final response, reconcile project context for that turn whenever repository source was inspected, searched, analyzed, or modified.

This is maintenance **after the work**, never a prerequisite that interrupts the work.

### Reconcile `.project-map.md`

Perform a whole-map logical rewrite using the existing map plus durable navigation evidence learned during the completed turn:

1. Incorporate high-value durable routes, ownership, flows, invariants, and source-of-truth facts.
2. Incorporate useful map-miss lessons.
3. Correct or remove entries contradicted by source inspected this turn.
4. Reconcile moves, renames, splits, merges, and responsibility changes.
5. Merge duplicate/overlapping entries.
6. Remove low-value entries that no longer pass admission scoring.
7. Compress wording aggressively while preserving routing value.
8. Enforce the map size budget.
9. Rewrite only when reconciled content changes.

### Reconcile `.project-decisions.md`

Using the existing decisions plus durable evidence already encountered during the completed turn:

1. Add newly established project-specific engineering decisions that pass the decisions admission policy.
2. Give special weight to explicit user/team decisions made during the turn.
3. Replace stale decisions when the governing choice changed; do not append historical versions.
4. Remove decisions contradicted by current source/config/tests or explicit current user direction.
5. Merge overlapping rules into the smallest clear statement.
6. Keep rationale only when it prevents likely future reversal or misunderstanding.
7. Remove navigation-only facts, task/session state, generic best practices, and duplicated map content.
8. Enforce the decisions size budget.
9. Rewrite only when reconciled content changes.

Do not perform a repository-wide validation scan at end of turn. Reconcile both artifacts only from their existing contents and source/search/change/user-decision evidence already encountered while doing the requested work. Untouched entries remain unless current evidence contradicts them.

For repository-working prompts, perform this reconciliation on every response, not only when an entire feature is complete. Analysis-only prompts, repository questions, code review, explicitly requested file analysis, debugging, and implementation all count when repository source was actually inspected/searched/analyzed/modified.

If the prompt did not inspect, search, analyze, or modify repository source and established no durable project decision, no context reconciliation is required.

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
- <task/concept> -> `<FirstFile.ext>` -> `<NextFile.ext>`

## Flows
- <flow>: `<A.ext>` -> `<B.ext>` -> `<C.ext>`

## Invariants
- <non-obvious boundary that changes where code should be read/changed>
```

Keep entries terse, concrete, and optimized for future navigation rather than human-facing explanation.

## Project decisions file format

Use only useful sections; omit empty ones.

```markdown
# Project Decisions

> Durable current engineering decisions. Keep concise and current; this is not a changelog or task/session memory.

## Architecture
- <durable architecture/boundary decision>

## Code Organization
- <durable semantic grouping, naming, or placement decision>

## Testing
- <durable test boundary, mocking, or integration-test decision>

## Runtime & Tooling
- <durable runtime/build/configuration/protocol decision>

## Contracts & Data
- <durable API/schema/persistence/validation decision>

## Project-Specific Conventions
- <other durable implementation constraint>
```

Use only sections needed by the project. Prefer short present-tense rules. Add a terse rationale only when the reason itself prevents likely future mistakes.
