# Goal Loop Pattern

A Goal prompt defines the result and the authority to reach it, rather than an itinerary. Include only guidance that changes execution for this task.

## Completion contract

Separate the completion contract—outcome, acceptance criteria, non-goals, and required quality or compatibility—from the working plan of hypotheses and implementation steps. Adapt the plan to evidence; changes to the contract require user agreement, whether they relax acceptance or expand scope. Regressions introduced by the work and applicable safety requirements remain obligations even when not enumerated in the criteria.

State the essential context and observable final conditions. Express behavioral acceptance criteria with EARS where applicable: “When <event>, the system shall <observable response>.” Pair each condition with evidence that can establish it; a first implementation or a progress report is not evidence of the final outcome.

Include paths, reproduction steps, or constraints when they affect the result. Let the executing agent discover routine commands and choose implementation details from the repository. Name a required check only when its identity matters to acceptance.

## Decision boundaries and persistence

State what the agent may carry through without further approval, within the user's authorization. For implementation work, this can include running the result, inspecting behavior, repairing in-scope failures, and rerunning affected checks. Describe test environments as disposable or isolated only when evidence supports that claim.

Make the stopping boundary explicit: continue until the final conditions are evidenced, or progress requires unavailable input, authorization, access, or an external change. Reserve review pauses for decisions the user actually needs to make, rather than inserting a pause after the first pass. A blocker report should identify what is missing and the exact condition for resuming; independent authorized work can continue.

Carry forward task-specific approval boundaries for destructive actions, production access, publication, or scope expansion. A prompt grants neither new authority nor exceptions to runtime continuation limits. Keep the completion bar intact when verification is blocked; report the gap instead of declaring success.

## Convergence

Select the next action by the remaining gap to the original outcome: an unmet acceptance criterion, uncertainty preventing a completion judgment, or a concrete risk or regression that blocks completion. Research and failed hypotheses count as progress when they reduce that uncertainty. Added code, abstractions, or tests alone do not. Defer cleanup, generalization, and optional improvements that serve none of these purposes.

Reorient when the same failure recurs, designs oscillate, complexity grows without closing a gap, or checks repeat without new evidence. Re-read the original request and completion contract, then compare them with the cumulative diff and current verification evidence—not only the latest patch or progress summary. Identify the stalled assumption and choose a discriminating check, a simpler sufficient approach, or a different hypothesis. Seek user input when the remaining choice needs their authority or judgment.

Distinguish three outcomes: evidenced acceptance means complete; stagnation calls for a changed approach; missing input, authority, or external state means blocked. An iteration or resource limit triggers reassessment or an incomplete handoff, never a success claim. Once the contract is satisfied and required checks pass, report optional improvements separately rather than extending the Goal.

## Checkpoints when useful

Add checkpoints when dependencies, distinct risks, or a long-running handoff need them. Each checkpoint names an intermediate result and the evidence that closes it; the executing agent chooses the work needed to get there. A short, coherent task can use only its final conditions.

Use an existing plan or progress record when durable history is needed. Keep a pointer to the original contract alongside evidence, unresolved conditions, rejected hypotheses and their reasons, and the next action. After a context handoff, recover the contract as well as the local work state; runtime Goal state remains authoritative for execution permission. Create a new record only when the task warrants one.

Match validation to the changed behavior and repository requirements. Broaden or repeat it for new changes, failures, or unresolved risks, rather than requiring a fixed testing ladder at every checkpoint.

## Independent evaluation when warranted

Use a separate evaluation context when drift, unreliable self-evaluation, or task difficulty warrants its cost, rather than after every iteration. Supply the original contract, cumulative diff or resulting artifact, and verification evidence. Evaluate the end-to-end outcome, not just local patch quality.

Require blocking findings to name the violated criterion or invariant and supporting evidence. Keep optional improvements separate from acceptance failures; feedback is not authority to add requirements. An evaluator's approval supplements direct verification rather than replacing it.

## Sources

Consult these for current Codex Goal behavior when the draft depends on runtime details:

- <https://learn.chatgpt.com/use-cases/follow-goals>
- <https://learn.chatgpt.com/use-cases/iterate-on-difficult-problems>

Instruction-design basis: concise triggers, progressive disclosure, outcome-oriented guidance, explicit decision boundaries, and persistence to defined completion:

- <https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra>

Long-running-agent observations: compaction alone is insufficient; external state and behavioral checks help preserve continuity. Iteration can increase complexity without monotonically improving quality, and evaluation scaffolding should match model capability:

- <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
- <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- <https://www.anthropic.com/engineering/harness-design-long-running-apps>

The convergence rules above are a design synthesis of these observations, not a demonstrated guarantee of convergence.
