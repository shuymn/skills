---
name: commit
description: Create local Git commits in logical units when the user requests committing changes.
allowed-tools: [Bash, Read, Grep, Glob]
---

# Commit

Commit only on an explicit request (`/commit` or equivalent). Do not push, create PRs, merge, rebase, or rewrite history. An existing request to commit is authorization; do not require a second approval.

## Interface

- `--english` / `--japanese`: subject language; type and scope remain English. Without either, match recent commit subjects, falling back to the user's language and repository context.
- `--branch`: create a descriptive `<type>/<descriptive-name>` branch before staging.
- `--base=<branch>`: with `--branch`, switch to this base before creating the branch; otherwise the base is the current branch. Never discard changes to switch branches.

## Commit contract

Inspect live `git status --short`, `git diff`, `git diff --cached`, and recent commit subjects. Inspect untracked files or their file types too; report any excluded files and why. Preserve unrelated work and pre-existing staging; do not silently include it in a commit outside the requested scope.

Group changes by purpose and independent revertibility. Keep a fix with its regression test; split unrelated fixes or independently useful refactors. A cross-cutting but inseparable change can be one unscoped commit. Ask only if scope or grouping remains materially ambiguous after inspection.

Stage explicit paths, then inspect the full cached diff before each commit. For files containing multiple logical changes, read [partial staging](references/examples.md#partial-staging), relative to this skill directory. Do not commit unrelated staged changes just because they are already in the index.

Use `type(scope): subject` or `type: subject`:
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `build`, `ci`.
- Entire subject line ≤50 characters, no trailing period. English uses lowercase imperative wording; Japanese uses である調 and katakana for technical terms.
- Scope, if present, names one area. Multiple scopes or English `and` signal a grouping review, not an automatic split of an inseparable change.

Run relevant repository checks for the intended changes, reusing valid results when nothing affecting them has changed. Review the staged diff again after any repair or hook modification. Commit each intended unit and verify the resulting commit and remaining status. Continue until the requested scope is committed or a concrete blocker remains.

## Recovery and output

- Never discard work with `git restore`, `git reset`, `git checkout --`, forced checkout/switch, or `git clean` while splitting. If index recovery would alter pre-existing staging, ask for direction unless already authorized.
- For hook failures, inspect the error, repair in-scope local issues, validate, and retry. Never bypass hooks; report failures requiring outside scope or user action.
- For signing failures, report the exact error and stop committing. Do not change signing configuration or bypass signing.
- Report commit hashes and subjects, checks performed, and remaining/excluded changes or blockers. Wrap paths/code containing `@` in backticks in reports.
