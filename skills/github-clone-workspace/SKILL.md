---
name: github-clone-workspace
description: Clones public GitHub repository or /tree/<ref>/<directory> URLs into temporary local workspaces for code inspection. Use when the user provides a GitHub repo/tree URL and local read/search/bash inspection would help, especially when github_clone_workspace tool behavior is needed in runtimes without that tool.
allowed-tools: [Bash, Read, Grep, Glob]
---

## Path Resolution

`<skill-root>` is the directory containing this `SKILL.md`. Resolve `scripts/...` relative to it, not the caller's current working directory.

# GitHub Clone Workspace

## Scope

Use this skill to clone a public GitHub repository into a temporary directory, then inspect it locally with read/search/bash tools. This is a skill version of the `github_clone_workspace` capability from the `add-dir` pi extension.

Supported URLs:

- `https://github.com/owner/repo`
- `https://github.com/owner/repo/tree/<ref>/<directory>`

Unsupported URLs:

- `/blob/...` file URLs
- SSH URLs such as `git@github.com:owner/repo.git`
- non-GitHub hosts

## Workflow

1. Run the bundled script:

   ```sh
   python <skill-root>/scripts/github_clone_workspace.py 'https://github.com/owner/repo'
   ```

   Optional local clone directory name:

   ```sh
   python <skill-root>/scripts/github_clone_workspace.py 'https://github.com/owner/repo/tree/main/packages/app' --directory-name repo-copy
   ```

2. Read the printed `path:` value.
3. Use that absolute path for subsequent `Read`, `Grep`, `Glob`, or read-only `Bash` commands such as `find`/`ls`.
4. Tell the user the registered workspace name/path you used.
5. When finished, run the printed cleanup command. If using `--json`, remove the printed `tempRoot` path.

## Behavior

The script:

- clones with `git clone --depth 1 --filter=blob:none --single-branch`;
- resolves `/tree/<ref>/<directory>` refs using `git ls-remote --heads --tags`;
- registers the tree subdirectory as the effective inspection path;
- rejects unsafe owner/repo/ref values and unsafe `--directory-name` values;
- rejects URL subpaths that escape the cloned repository or do not resolve to directories;
- times out git operations after 30 seconds;
- does not fetch submodules.

## Error Handling

- If a `/blob/` URL is provided, explain that file URLs are unsupported and ask for the repository URL or a `/tree/<ref>/<directory>` URL.
- If `git ls-remote` or `git clone` fails because the repository is private or inaccessible, tell the user this skill only supports public repositories unless their local git credentials already permit access.
- If the script exits with an error, report the exact error and stop rather than guessing a path.
