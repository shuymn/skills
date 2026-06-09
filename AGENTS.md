# AGENTS.md

## Repo-Specific Rules

- Edit skills directly under `skills/<skill-name>/**`.
- Keep each skill self-contained: resolve `references/**`, `scripts/**`, and other support files relative to the directory containing that skill's `SKILL.md`.
- After changing skills, run `uv run --with pyyaml python scripts/test_validate_skill_frontmatter.py`, `uv run --with pyyaml python scripts/validate_skill_frontmatter.py`, then check whitespace/conflict markers with `git diff --check`.
- Do not install or reinstall skills from this repository unless the user explicitly asks for that action.
- Runtime system/plugin skills outside this repository are intentionally unmanaged.
