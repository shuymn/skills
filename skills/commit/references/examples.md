# Grouping and Partial Staging

## Grouping examples

- Keep a bug fix and the test protecting it together: `fix(auth): handle null user sessions`.
- Split an independently useful refactor from a new feature; keep supporting changes together when splitting would leave a broken intermediate state.
- Separate unrelated bug fixes even when they touch one file.
- Use one unscoped commit for an inseparable cross-cutting change: `feat: centralize request validation`.

## Partial staging

Use an editable patch when only part of a file belongs in the current commit. Start from the unstaged diff so existing index contents are not replaced.

```bash
# Use a unique temporary file; substitute actual target paths.
patch=$(mktemp)
git diff -- path/to/file > "$patch"
```

Edit the patch to retain only the intended hunks. If splitting within a hunk, preserve valid patch context and line counts. Then validate and apply to the index only:

```bash
git apply --check --cached "$patch"
git apply --cached "$patch"
git diff --cached
git diff
```

If validation fails, correct or regenerate the patch from the current diff and retry; a malformed patch alone is not a reason to stop for approval. Do not fall back to staging the whole file or discarding working-tree content. If correcting an already-applied patch would affect pre-existing staging or ownership is unclear, ask for direction. Remove only the temporary files you created when finished.
