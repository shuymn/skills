---
name: goal-loop-engineering
description: "Draft or rewrite pi /goal, Codex Goal, or long-running coding-task prompts."
allowed-tools: [Read, Grep, Glob, Bash]
---

# Goal Loop Engineering

Return a copyable prompt for a future session. Drafting does not authorize starting, updating, or executing the Goal.

## Shape the task

Preserve the user's outcome and define observable completion before prescribing a process. Use [the Goal loop pattern](references/goal-loop-pattern.md) to specify the completion contract, decision boundaries, and convergence guidance. Leave implementation strategy and work sequencing to the executing agent unless the task requires a particular order.

Use the requested runtime, or the current harness when it identifies the target unambiguously; the model provider is not the runtime. Inspect workspace evidence only where it affects the draft. Ask about missing decisions that materially change scope, public behavior, authority, or the output contract. Leave ordinary implementation choices open. If a prerequisite decision prevents a runnable Goal, return a planning-only prompt identifying the decision and the evidence needed to resolve it.

## Select the output contract

- **pi with the shuymn/pi-extensions Goal:** Read [the pi Goal format](references/pi-goal-format.md) for its command grammar and execution boundaries.
- **Codex Goal:** Return one copyable `/goal` prompt. Consult official documentation when current command syntax or runtime behavior needs confirmation; the pattern reference links to starting points.
- **Other long-running task:** Return a plain task prompt unless its command contract is known. Use a planning command only when the target supports it.

## Deliver

Return the prompt in the user's requested language, with a short explanation only for a material assumption or boundary. It is ready when the target can parse it, every completion condition has observable evidence, its authorization matches the request, and it distinguishes completion from stagnation or blocked work. Keep necessary context inside the copyable output or behind a reachable document pointer; rely on repository instructions for standing rules.
