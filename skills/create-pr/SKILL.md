---
name: create-pr
description: Create or update a GitHub pull request from committed changes when the user requests PR publication.
allowed-tools: [Bash, Read, Grep, Glob]
---

# Create or Update a PR

## Interface and routing

- Default: create a PR targeting the repository's default branch, in English.
- `--japanese`: Japanese title/body; keep code identifiers and proper nouns unchanged. Use ですます調 in paragraphs, plain or noun-ending bullets without final `。`.
- `--base=<branch>`: select the target branch.
- `--update`: update the open PR for the current branch, using its existing base unless explicitly overridden. If none exists, report that; do not create one.

For publication, read [publish.md](references/publish.md). If no repository PR template applies, read [pr-templates.md](references/pr-templates.md). Resolve references relative to this skill directory.

## Shared contract

A request to create/update a PR authorizes the necessary normal branch push and requested PR write; do not ask again. A request only to draft or review does not authorize publication. Do not commit uncommitted work, force-push, rewrite history, merge, or change unrelated PRs.

Resolve the repository, head branch, and base before writing. Inspect all commits in `<base>..HEAD` and the PR diff `<base>...HEAD`, using the appropriate remote base ref. Analyze committed changes only; leave uncommitted work untouched. If there are no commits to propose, report that without publishing. If unrelated work makes the requested scope ambiguous, recommend a split without rewriting history yourself.

Use a short, specific title (imperative in English). The body must cover what changed, why, and verification actually performed; disclose unrun checks or limitations rather than inventing results. Include trade-offs, breaking changes, rollout, or review-order hints only when useful. Do not reproduce file lists or commit classifications.

Follow the repository's PR template and checklist format. Remove empty/non-applicable optional sections only when permitted by that template.

Pass raw Markdown to GitHub tools, without backslash-escaping backticks. For `gh`, prefer `--body-file`; use a quoted heredoc when writing the body file to prevent shell expansion. Wrap code/paths containing `@` in backticks to avoid mentions.

After publication, confirm the resulting PR's URL, base, title, and body. Return the URL, whether created or updated, and any verification limits or blockers. If a push succeeded but the PR write failed, report both outcomes.
