# Publish to GitHub

## Resolve the target

Use live Git state and GitHub metadata, not cached command snapshots. Confirm the current branch, repository remote, and intended head repository (including fork ownership). A detached HEAD or ambiguous destination needs resolution before pushing.

For creation, use `--base` or the repository default branch. `git symbolic-ref --short refs/remotes/origin/HEAD` can identify the local remote-default ref; if missing or stale, use GitHub repository metadata. Fetch the relevant remote refs when needed before analyzing the committed range.

For `--update`, find the open PR matching the current head repository and branch. For example, use `gh pr view` in an unambiguous repository or query open PRs with the owner-qualified head. Resolve multiple matches before writing. Use the existing PR base unless the user supplied `--base`; that explicit flag also authorizes updating the PR base. Do not silently substitute the default branch.

Inspect the existing PR body before updating so that required template fields and still-relevant manually supplied context are retained. Summarize all current commits against the selected base, not just the most recent push.

## Create

Prepare content before pushing. Push only the intended branch to its verified head remote, normally with `git push -u <remote> <branch>`. No force push; a rejection is a blocker to investigate, not authorization to overwrite remote work.

Use `gh pr create --repo <owner/repo> --head <head> --base <base> --title <title> --body-file <file>` or the equivalent GitHub tool with explicit head, base, title, and raw Markdown body. If an open PR already exists, report it instead of silently switching to update mode or creating a duplicate.

## Update

Confirm the PR exists before pushing. Push the intended branch normally, then use `gh pr edit <number> --repo <owner/repo> --title <title> --body-file <file>` or an equivalent GitHub update tool. Include a base update only when explicitly requested. If no open PR exists, stop without creating one.

## Failures

Do not repeatedly issue a create/write after a timeout without checking whether it succeeded. Re-read remote state first to avoid duplicates. Report authentication, branch protection, or access blockers without changing configuration or bypassing protections.
