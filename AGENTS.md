# AGENTS.md

## Repo-Specific Rules

- Edit skills directly under `skills/<skill-name>/**`.
- Keep each skill self-contained: resolve `references/**`, `scripts/**`, and other support files relative to the directory containing that skill's `SKILL.md`.
- After changing skills, check for whitespace/conflict markers with `git diff --check`, then run `skills add "$(pwd)/skills" -g -y -a codex -a claude-code --skill '*'`.
- Runtime system/plugin skills outside this repository are intentionally unmanaged.
