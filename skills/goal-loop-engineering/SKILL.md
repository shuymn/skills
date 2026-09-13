---
name: goal-loop-engineering
description: "Use when asked to draft or rewrite a Codex /goal or long-running coding-task prompt with incremental checkpoints and verifiable completion. Does not execute the Goal."
allowed-tools: [Read, Grep, Glob, Bash]
---

# Goal Loop Engineering

Create a prompt for a future Codex Goal session. Never create, start, update, or execute the Goal itself.

## Resolve the task

Preserve the user's intended outcome. Inspect only workspace evidence that can change the prompt; current source and checks take precedence over earlier summaries.

Draft `/goal` when the outcome, important constraints, and final verification are clear enough for autonomous implementation. If an unresolved architecture, public-contract, or approval decision would materially change the Goal, explain the decision and recommend `/plan` first.

## Draft the prompt

Use [the Goal loop pattern](references/goal-loop-pattern.md) to specify:

- One user-visible objective and an observable final stopping condition.
- Evidence-driven checkpoints with targeted validation and in-scope diagnosis and retry.
- A durable progress record, reusing an existing plan or log where available.
- Task-specific boundaries; rely on `AGENTS.md` for standing repository rules.

Completing one checkpoint does not complete the Goal. Continue until the final conditions have evidence or progress requires unavailable input, authority, or external state. Do not introduce review pauses between already-authorized checkpoints.

Remove generic process narration, discoverable command inventories, repeated prohibitions, and details that do not change execution.

## Output

Lead with a short explanation of the checkpoint boundaries, then return one copyable prompt in the user's requested language. Start with `/goal` when ready; otherwise explain the missing decision and return the smallest useful `/plan` prompt.

When asked for current Codex syntax, behavior, or citations, verify official OpenAI documentation rather than relying on the bundled reference alone.
