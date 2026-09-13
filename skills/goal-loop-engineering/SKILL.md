---
name: goal-loop-engineering
description: "Draft or rewrite pi /goal, Codex Goal, or long-running coding-task prompts with checkpoints and verifiable completion."
allowed-tools: [Read, Grep, Glob, Bash]
---

# Goal Loop Engineering

Create a copyable prompt for a future Goal session. Draft only; never create, start, update, or execute the Goal itself.

## Resolve the target and task

Use the user's specified runtime; otherwise use the current harness and available Goal contract. Ask one concise question if the target remains unclear. The model provider does not determine the runtime.

Preserve the intended outcome. Inspect only workspace evidence that can change the prompt; current source and checks take precedence over earlier summaries.

Draft a runnable Goal when the outcome, important constraints, and final verification are stable. If an unresolved architecture, public-contract, or approval decision would materially change the Goal, explain that decision and return a planning-only prompt instead. Use `/plan` only where the target supports it.

## Draft and format

Use [the Goal loop pattern](references/goal-loop-pattern.md) for checkpoint boundaries, evidence, and the final stopping condition. Rely on `AGENTS.md` for standing repository rules.

Select only the relevant output contract:

- **pi with the shuymn/pi-extensions Goal:** Read [the pi Goal format](references/pi-goal-format.md). Its command grammar is part of correctness, not a prose template.
- **Codex Goal:** Return one copyable `/goal` prompt with the objective, necessary context, checkpoint guidance, and completion conditions. Verify official OpenAI documentation when current syntax, behavior, or citations are requested.
- **Other long-running task:** Return a plain task prompt unless the target's command contract is known.

Lead with a short explanation of checkpoint boundaries, then the copyable output in the user's requested language. Before returning it, check that the target can parse it and every final condition has observable evidence. Remove process narration, discoverable command inventories, and repeated rules.
