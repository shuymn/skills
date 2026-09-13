# Diff and recent-file scope

Use the first applicable mode. Explicit paths, handled in `SKILL.md`, take precedence over all flags.

| Mode | Targets and context |
| --- | --- |
| `--base=<ref>` | Paths and diff from `git diff --name-status -z <ref>...HEAD` and `git diff <ref>...HEAD`; exclude unrelated local changes. |
| `--staged` / `--cached` | Staged paths and staged diff: `git diff --cached --name-status -z` and `git diff --cached`. |
| Default | Union of unstaged, staged, and untracked paths: `git diff --name-status -z`, `git diff --cached --name-status -z`, `git ls-files --others --exclude-standard -z`. Read both diffs and untracked contents. |

When no targets remain and no `--base` was supplied, fall back to the eight most recently modified tracked files by mtime (`git ls-files -z`, then stat/sort). Label them as **recent whole-file targets**, not changed files, and inspect their contents directly. If the fallback is empty, report no scope and stop.

Handle renames and deletions from name-status output; a deleted file is context, not an editable target. Use repository-root-relative paths and preserve filenames safely. Scope selection never authorizes overwriting pre-existing local changes.
