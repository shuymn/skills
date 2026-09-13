# Reply to AI Review Threads

Post only when explicitly requested for the target PR; reuse existing authorization without asking again. Skip in pasted-feedback mode where no thread is identified. Do not infer posting consent from requests to triage, fix, or report. Do not commit or push merely to obtain a hash for a reply.

Inspect current replies before posting. Preserve user-edited replies and avoid duplicating an existing response. Reply only to the intended outstanding threads. For inline comments, use the thread's root comment ID:

```bash
gh api -X POST repos/<owner>/<repo>/pulls/<number>/comments/<root_comment_id>/replies \
  -f body='<reply body>'
```

Issue-level and review-level comments do not use this inline-reply endpoint. Use the appropriate PR comment mechanism only within the authorized scope, retaining a link to the source comment. Do not resolve threads or edit others' comments without authorization.

Keep replies to verdict, actual fix status, and at most one line of evidence. Include a commit hash only when the fix is actually committed; distinguish local-only from pushed fixes. GitHub links 7+ character hashes, but full-width brackets require spaces: `（ abc1234 ）` rather than `（abc1234）`.

Japanese replies use 常体 (だ・である調). Lead with what changed or why no change was made; omit greetings, thanks, sign-offs, and formulaic filler. Do not claim uncertain suggestions are disproven.

After posting, confirm the result. On an ambiguous API failure, check for an existing reply before retrying. Report any posting failure separately from successful local fixes.
