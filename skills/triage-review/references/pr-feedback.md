# Collect PR Feedback

Resolve a URL to its owner, repository, and PR number. For a number, resolve the repository with `gh repo view`; with no argument, use `gh pr view` for the current branch. Use explicit repository coordinates in subsequent requests.

Fetch metadata and all pages of changed files and comments:

```bash
gh api repos/<owner>/<repo>/pulls/<number>
gh api --paginate repos/<owner>/<repo>/pulls/<number>/files
gh api --paginate repos/<owner>/<repo>/issues/<number>/comments
gh api --paginate repos/<owner>/<repo>/pulls/<number>/reviews
gh api --paginate repos/<owner>/<repo>/pulls/<number>/comments
```

Read metadata including head repository, branch, and SHA. Confirm the local checkout corresponds to the PR before editing; do not silently switch branches or overwrite local work. Outdated line numbers are hints: locate the current code and verify whether the issue still exists.

Retain comment IDs, URLs, author logins, paths, current/original line positions, and `in_reply_to_id` so findings can be attributed and optional replies can target the correct thread. Include issue-level, review-level, and inline suggestions; avoid counting quoted/repeated claims as separate defects.

Known AI reviewer logins include `Copilot`, `copilot[bot]`, `copilot-pull-request-reviewer[bot]`, `github-copilot`, `gemini-code-assist[bot]`, `google-code-assist`, `google-code-assist[bot]`, `chatgpt-codex-connector[bot]`, and `devin-ai-integration[bot]`. This is not an exhaustive allowlist: verify unfamiliar authors rather than treating every bot as an AI reviewer. Exclude human-authored feedback.

If fetching fails, report the access/API failure rather than claiming no AI comments exist. If collection succeeds but no AI suggestions exist, report that without editing.
