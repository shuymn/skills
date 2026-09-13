# Goal Loop Pattern

Use only the parts that change execution behavior. The target runtime determines command syntax; this pattern determines the task content.

## Objective and boundaries

Specify one durable, user-visible objective and observable final conditions. Include only paths, repro steps, current-state evidence, and task-specific constraints that can change the result. Express behavioral acceptance criteria with EARS where applicable.

Leave implementation choices to the executing agent when the outcome is stable. Resolve material design or approval decisions before drafting runnable work; a prompt cannot invent production, commit, push, or destructive authority.

## Evidence-driven checkpoints

A checkpoint is one coherent risk boundary, acceptance criterion, or failure cluster plus the evidence that closes it. Select checkpoints from dependency order and current evidence rather than fixed file counts or a rigid per-turn schedule.

Ask the executing agent to establish the relevant baseline, make the smallest coherent change, and diagnose and retry in-scope failures until the checkpoint's decisive check passes. An evidence-backed no-change decision can close a checkpoint too.

Use targeted validation within a checkpoint, affected-subsystem checks at its boundary, and the final regression set that proves the outcome. Broaden checks for shared-contract changes or unresolved risks rather than rerunning everything after every edit.

## Progress and completion

Reuse an existing plan or log when durable checkpoint history is needed. Record evidence, material decisions or blockers, remaining final conditions, and the next candidate. Keep runtime Goal state authoritative for execution permission; progress notes do not grant it.

Continue through already-authorized checkpoints until every final condition has current evidence. One checkpoint or a first implementation is not the final gate. Avoid intermediate review pauses unless a new material decision or authority is required.

When safe in-scope work cannot progress without unavailable input or external state, report the blocker and exact resume condition using the runtime's waiting or pause mechanism. Honor runtime continuation limits and human-resume requirements.

## Assemble and prune

Keep the objective, essential context, checkpoint guidance, final conditions, and task-specific boundaries. Include a reporting shape only when the user needs one. Remove any sentence that does not change scope, checkpoint selection, verification, or required output.

## Sources

For current Codex Goal behavior, consult official documentation:

- <https://learn.chatgpt.com/use-cases/follow-goals>
- <https://learn.chatgpt.com/use-cases/iterate-on-difficult-problems>

For instruction design, use concise triggers, branch-specific disclosure, explicit completion, and decision boundaries rather than elaborate recipes:

- <https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra>
