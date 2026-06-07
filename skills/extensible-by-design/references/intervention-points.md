# Intervention Points: Pipeline Hook Design

Extensions should attach to **named stages** in a processing pipeline — not blanket middleware that runs everywhere. Clear stages make precedence predictable for humans and AI authors alike.

## Canonical Pipeline

Most interactive systems decompose into:

```
Input
  → Parse / normalize
  → Route (commands, intents, branches)
  → Enrich context (inject system state, policies)
  → Execute (core action or agent loop)
  → Transform results
  → Persist / emit output
```

Each arrow is a potential **intervention point** — but not every point needs a hook. Design hooks where extension authors naturally ask to intervene.

## Hook Types

| Type | Effect | Example use |
|------|--------|-------------|
| **Transform** | Modify data passing through; pipeline continues | Rewrite user input, redact secrets |
| **Handle** | Consume the event; pipeline stops for this path | Slash command bypasses LLM |
| **Block / gate** | Allow, deny, or defer | Permission check before tool execution |
| **Observe** | Side effect only; no change to flow | Metrics, logging, analytics |
| **Inject** | Add context for downstream stages | Load team policy before agent turn |

Prefer one semantic per hook. "Transform that sometimes handles" confuses authors and breaks precedence docs.

## Precedence Rules

When multiple extensions attach to the same stage, document explicit ordering:

1. **Scope priority** — org > project > user > package (or your domain's equivalent)
2. **Handler beats transform** — if something fully handles an input, later transforms on that path do not run
3. **Fail-closed vs fail-open** — state which hooks block by default (security hooks usually fail-closed)
4. **Provenance for collisions** — disambiguate same-named extensions (`review:1`, `review:2` or source labels)

Publish the precedence table. AI agents authoring extensions need it as much as human developers.

## Stage-by-Stage Guide

### Input / parse

- Transforms: macro expansion, template substitution, PII scrubbing
- Handles: direct commands that should not reach the executor
- *Avoid:* heavy business logic here

### Route

- Branch on intent, command namespace, or feature flags
- Skill / playbook selection often belongs here (match description → load on demand)

### Enrich context

- Inject policies, retrieved docs, session memory summaries
- **Progressive disclosure**: inject summaries; load full artifacts in execute stage when needed

### Execute

- Gates before side effects (tool call, payment, publish)
- Wrap execution with timeouts, retries, sandbox boundaries
- Core loop stays here; extensions observe and gate, not replace the loop silently

### Transform results

- Format output, filter tool results, attach citations
- Safe place for presentation-layer customization

### Persist / emit

- Append to session tree, audit log, webhooks
- Branching / fork / retry metadata often recorded here

## Exploration-Aware Hooks

Systems used by AI benefit from hooks that understand **non-linear work**:

| Operation | Purpose |
|-----------|---------|
| Fork / branch | Copy state from a decision point |
| Rewind | Resume from earlier node without losing sibling branches |
| Compact | Summarize old branches while retaining full history elsewhere |

These are not generic middleware — they are first-class pipeline operations extensions can trigger.

## Self-Modification Loop

For AI-native systems, verify this loop is possible:

```
Author extension → Register / reload → Exercise → Inspect result → Revise
```

"Reload" means different things by system archetype:

- **Interactive session systems** (agent harnesses, REPLs, IDEs): reload means in-process hot-reload at the registration boundary — the extension takes effect in the current session without restart.
- **Batch / trigger systems** (CI/CD pipelines, job queues, request handlers): reload means the next invocation picks up the change — no full redeploy of the orchestrator, but a new run sees the updated extension.

Both archetypes satisfy the principle. The mechanism differs; the test is whether an AI can author, register, exercise, and revise in a single contiguous workflow, not whether the reload is literally in-process.

Hook design affects loop viability:

- Hot reload at registration boundary (not only at process start)
- Session / job state survives reload where safe
- Footguns documented (e.g., replacing a handler mid-execution for interactive systems; stale extension caches for batch systems)

If the loop requires a **full redeploy of the core system**, extensibility is theoretical for agents. But "full redeploy of the orchestrator" is distinct from "next pipeline run picks up new config" — the latter is a valid self-modification loop for batch systems.

## Design Checklist

When adding a new hook:

- [ ] Named stage and single semantic (transform / handle / block / observe / inject)
- [ ] Documented position relative to existing hooks
- [ ] Precedence when multiple extensions register
- [ ] Whether it can short-circuit the pipeline
- [ ] What context is readable / mutable
- [ ] Failure mode (fail-closed or fail-open)
- [ ] Example extension using only public contract

## Anti-Patterns

| Anti-pattern | Problem |
|--------------|---------|
| Global pre/post everywhere | Order unpredictable; debugging nightmare |
| Hidden core branches | Extensions cannot override "special cases" |
| Synchronous-only hooks | Blocks long-running agent work |
| Implicit hook discovery | AI authors cannot find insertion points |
| Same hook for code and instructions | Mixes planes; use separate registration paths |

## Illustrative Mappings (not prescriptions)

| Domain | Input handle | Enrich | Execute gate | Result transform |
|--------|--------------|--------|--------------|------------------|
| E-commerce checkout | Coupon code command | Loyalty tier context | Payment authorization | Receipt template |
| Content moderation | Reporter shortcut | Policy pack load | Publish block | Appeal formatting |
| Data pipeline | Manual replay trigger | Schema version inject | Row-level validation | Dead-letter formatting |

Use these to locate analogous stages in the system under review — do not copy the table literally.
