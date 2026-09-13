---
name: simplify
description: "Simplify changed code or specified files without changing behavior. Use for cleanup, deduplication, reuse, or practical efficiency improvements."
allowed-tools: [Bash, Read, Edit, Write, Grep, Glob, Agent]
---

# Simplify

Apply verified internal simplifications; preserve behavior and public APIs. Prefer clarity over fewer lines. Do not add features, speculative abstractions, or stylistic-only churn.

## Mode and scope

- `--report-only`, or a request to review/propose rather than edit: report findings without edits.
- Otherwise, a cleanup request authorizes in-scope local edits; do not ask for the same approval again.
- Explicit file paths are whole-file targets; do not infer scope from unrelated Git changes.
- Without explicit paths, read [scope selection](references/scope.md) for diff flags and the recent-file fallback.
- Preserve unrelated local edits. Tiny adjacent changes required to preserve behavior must be explained before editing; material scope expansion needs approval. Commits and PRs are separate actions.

## Review and apply

Inspect relevant code and consider all three lenses:

| Lens | Look for |
| --- | --- |
| Reuse | Existing utilities, components, or constants that replace duplicated or bespoke logic without distorting their contracts. |
| Quality | Redundant state, needless branching, copy-paste variants, and over-clever code. Remove obsolete guards or compatibility paths only when current specifications, code, and tests establish that they are irrelevant or unreachable. Preserve comments explaining business rules, external quirks, or real constraints. |
| Efficiency | Avoidable computation, calls, fetches, parsing, or allocation with practical impact. Parallelize only when ordering and side effects remain safe. |

Review directly for small scopes. Delegate independent areas or lenses when scope, risk, or uncertainty warrants another reviewer; use read-only delegates with the exact scope, relevant evidence, and user constraints. Retrieve omitted diff sections rather than treating truncated context as complete.

Verify each finding against the code before applying it. Skip false positives and changes whose behavioral equivalence cannot be established. Resolve disagreements conservatively. Apply the smallest supported change, not every suggestion.

Run relevant tests, type/lint/format checks and repository-required validation for the changed behavior. Investigate failures and repair those caused by this pass without weakening assertions or expanding scope. Report unrelated failures or unavailable checks as limitations.

## Result

In the user's language, report changed paths and reasons, material findings skipped (or would-apply findings in report-only mode), and validation commands/results. If nothing merits changing, say so; no quota of edits or findings is required.
