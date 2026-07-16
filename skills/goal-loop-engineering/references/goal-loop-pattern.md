# Goal Loop Pattern

Use only the parts that change execution behavior. A Goal prompt does not need to fill a fixed template.

## Choose `/goal` or `/plan`

Use `/goal` when the desired result, important constraints, and final verification are stable while Codex may choose the implementation path.

Recommend `/plan` first when the user wants to approve the approach before edits, or when an unresolved architecture, public API, migration policy, or product decision would materially change the Goal. Do not turn an open design decision into hidden implementation authority.

## Extract the useful pieces

- **Goal:** One durable, user-visible objective and its final stopping condition.
- **Context:** Only paths, repro steps, current-state evidence, and sources that can change the result.
- **Output:** The checkpoint update and final report the user needs to review.
- **Boundaries:** The one or two task-specific constraints that prevent real damage or scope drift.

Point to `AGENTS.md` instead of copying its durable rules. Do not list standard commands the future agent can discover unless an exact command is contractually required or already verified.

## Define checkpoints

Define one checkpoint as:

> one coherent risk boundary, acceptance criterion, or failure cluster + the smallest required change + the evidence that closes it

Choose checkpoints dynamically from dependency order and current evidence. Combine files only when they share one cause and one validation path. Avoid arbitrary file-count or time-box boundaries.

## Define the per-turn loop

Require each Goal turn to:

1. Read the Goal, authoritative state, and latest progress record.
2. Select one dependency-ready, independently verifiable checkpoint.
3. Establish its baseline and state the proof required.
4. Make one focused change or record an evidence-backed no-change decision.
5. Run the narrowest decisive validation; diagnose and retry within the checkpoint if it fails.
6. Record the result, remaining Goal conditions, and next candidate while leaving the Goal active if the final gate remains unmet.

Do not require user steering between checkpoints unless new authority or a material decision is needed.

## Use a validation ladder

- **Inner loop:** The smallest test, type target, lint rule, query, replay, or smoke check tied to the change.
- **Checkpoint gate:** The affected package or subsystem checks.
- **Cross-cutting gate:** Broader checks only after shared contracts or multiple subsystems change.
- **Final gate:** The complete regression set that proves the Goal outcome.

Do not run the full suite after every edit. Do not advance while the current checkpoint's decisive check is failing.

## Keep progress state small

Reuse an existing plan, implementation log, issue checklist, or task tracker. Record only the checkpoint, evidence, material decision or blocker, remaining conditions, and next candidate.

If no durable file exists, use Goal status unless a long run clearly needs a repo-local handoff artifact. Do not create competing plans or verbose diaries.

## Define completion and blocking

Keep the Goal active after a checkpoint succeeds while any final condition remains unmet. Complete only when every final condition has current evidence; time spent, partial green checks, or one completed checkpoint are insufficient.

Treat the Goal as blocked only when safe in-scope investigation and useful fallbacks cannot progress without external state, new authority, or a material user decision. Name the missing fact or action and the exact resume condition.

## Assemble and prune

Prefer this compact order:

1. `/goal` and the final objective.
2. Relevant source of truth or provisional context.
3. Checkpoint selection and loop.
4. Validation and final stopping condition.
5. Task-specific boundaries.
6. Checkpoint and final reporting shape.

After drafting, remove any sentence that does not clarify the Goal, change how a checkpoint is selected or verified, prevent a likely failure, or define a required output.

## Avoid

- attempting the whole Goal in one turn;
- fixed backlogs that cannot adapt to evidence;
- full regression checks after every small change;
- marking the Goal complete after one checkpoint;
- repeating `AGENTS.md` or generic approval rules;
- inventing production, commit, push, or destructive authority;
- claiming an external check passed when it was not run.

## Official sources

Refresh current product behavior from:

- <https://learn.chatgpt.com/docs/prompting>
- <https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6>
- <https://learn.chatgpt.com/use-cases/follow-goals>
- <https://learn.chatgpt.com/use-cases/iterate-on-difficult-problems>
