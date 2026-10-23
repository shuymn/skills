---
name: proofread
description: >-
  Use when asked to review prose for AI writing tropes or mechanical style.
  Reports concrete rewrite suggestions; does not edit files or check grammar or facts.
allowed-tools: [Read, Grep, Glob]
---

## Path Resolution

- `<skill-root>` means the directory containing this `SKILL.md`.
- Resolve `references/...` relative to `<skill-root>`, not the caller's current working directory.

## Not in Scope

- Rewriting text on behalf of the user. This skill diagnoses; the user decides what to fix.
- Grammar, spelling, or factual accuracy checks — use dedicated tools for those.
- Code review or technical correctness.

## Input

- **Target** (required): One or more file paths, or inline text provided in the conversation.
- **Focus** (optional): Specific trope categories to check. Defaults to all categories.

## Review

Check the text against [the tropes catalog](references/tropes.md): the requested categories for a focused review, the full catalog otherwise. Note each file's purpose (README, blog post, documentation), because context sets severity: one "Not X — it's Y" in a 3000-word post is fine; five is a problem.

Report only real findings. Each one names the category and pattern, quotes just enough to locate the passage, and gives a concrete rewrite that keeps the author's meaning and sounds like a person wrote it; imperfect but natural beats pristine but robotic.

## Output Format

```
## Proofread Report: <filename or "inline text">

**Findings**: N

#### <Trope Category> — <Specific Pattern>
> <quoted passage>

Line: <line number or range, if from a file>
Suggestion: <concrete rewrite>

...
```

## Judgment Calls

- **Frequency matters more than presence.** A single em dash or one tricolon is not a finding. Repeated use of the same pattern is.
- **Context matters.** "Let's break this down" in a tutorial aimed at beginners is defensible. The same phrase in a technical RFC for staff engineers is not.
- **Do not flag code or structured data.** Bold-first bullets in a CLI `--help` output or API reference are conventional, not tropes.
- **Be honest, not exhaustive.** If the text is clean, say so. Do not manufacture findings to justify the review.
