---
name: goal-loop-engineering
description: "Drafts copyable GPT-5.6 Sol and Codex Goal prompts that turn a software-engineering objective into incremental checkpoints with validation loops, approval boundaries, durable progress, and verifiable completion. Use when the user asks to create or rewrite a `/goal`, Codex Goal prompt, Loop Engineering prompt, or long-running coding-task prompt that should progress across multiple bounded Goal turns."
allowed-tools: [Read, Grep, Glob, Bash]
---

# Goal Loop Engineering

Create a prompt for a future Codex Goal session. Never create, start, update, or execute the Goal itself.

## Workflow

1. Resolve the requested result from current evidence.
   - Preserve the user's natural wording and intended outcome.
   - When a workspace is available, inspect only the code, plans, work logs, git state, and checks that can change the prompt.
   - Treat earlier summaries as provisional; current source and test results win.

2. Check Goal readiness.
   - Draft `/goal` directly when the outcome, important constraints, and final verification are clear enough for autonomous implementation.
   - When an unresolved architecture, public-contract, or approval decision would materially change the Goal, recommend `/plan` first instead of burying that decision inside a long-running Goal.

3. Design one durable Goal and its checkpoint loop.
   - State one user-visible objective and one observable final stopping condition.
   - Limit each Goal turn to one coherent risk boundary, acceptance criterion, or failure cluster plus targeted validation.
   - Select checkpoints dynamically from dependency order and current evidence.
   - Reuse an existing plan or work log; avoid creating competing progress artifacts.

4. Draft with [the Goal loop pattern](references/goal-loop-pattern.md).
   - Keep ordinary checkpoints narrow and reserve broad regression gates for cross-cutting or final checkpoints.
   - Rely on `AGENTS.md` for durable repository rules. Repeat only task-specific boundaries that prevent a real failure or unintended action.
   - Make clear that completing one checkpoint does not complete the Goal.

5. Prune the prompt.
   - Keep only the Goal, context that changes the work, required output, important boundaries, checkpoint rule, and completion evidence.
   - Remove generic process narration, discoverable command inventories, repeated prohibitions, and examples that do not change behavior.
   - Confirm failures trigger diagnosis and retry within the checkpoint rather than premature completion or blocking.

## Output

Lead with one short explanation of the partitioning decision, then return one copyable prompt in the user's requested language. Start it with `/goal` when Goal is ready. If `/plan` must come first, explain the missing decision and return the smallest useful plan prompt instead.

When the user asks for current Codex syntax, behavior, or citations, verify the official OpenAI documentation rather than relying on the bundled reference alone.
