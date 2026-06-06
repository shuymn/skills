# skills

Personal agent skills managed outside `shuymn/dotfiles`.

Each directory under `skills/` is a skill source directory containing `SKILL.md` and optional supporting files. Install them into configured agent runtimes with `skills add "$(pwd)/skills" -g -y -a codex -a claude-code --skill '*'`.
