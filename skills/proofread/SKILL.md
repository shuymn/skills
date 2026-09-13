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

## Procedure

1. **Load the relevant patterns**: Use [the tropes catalog](references/tropes.md). Read the requested categories for a focused review, or the full catalog for a general review.

2. **Read the target text**: Read all target files or accept inline text. For each file, note its purpose (README, blog post, documentation, etc.) — context affects severity. A single "Not X — it's Y" in a 3000-word post is fine; five instances is a problem.

3. **Scan for tropes**: Walk through the text looking for matches against the catalog. For each finding:
   - Identify the trope category and specific pattern
   - Quote the offending passage (keep quotes short — enough to locate, not full paragraphs)
   - Judge binary: **finding** (should fix) or not a finding (skip — do not report)

4. **Draft rewrite suggestions**: For every finding, suggest a concrete rewrite. Preserve the author's meaning while sounding like something a human would actually write. Do not over-polish — imperfect but natural beats pristine but robotic.

5. **Produce the report**: List all findings with rewrite suggestions. Include a count at the top.

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
