# skills

Personal agent skills managed outside `shuymn/dotfiles`.

Each directory under `skills/` is a skill source directory containing `SKILL.md`
and optional supporting files. Keep support files self-contained in the same
skill directory.

## Skills

### Git Workflow

| Skill | Source | Description |
| --- | --- | --- |
| `commit` | [`skills/commit`](skills/commit/) | Creates meaningful git commits by analyzing changes and committing in logical units. |
| `create-pr` | [`skills/create-pr`](skills/create-pr/) | Reviews committed changes and creates a pull request on GitHub. |
| `triage-review` | [`skills/triage-review`](skills/triage-review/) | Processes AI reviewer feedback and applies only verified fixes. |

### Code Inspection

| Skill | Source | Description |
| --- | --- | --- |
| `github-clone-workspace` | [`skills/github-clone-workspace`](skills/github-clone-workspace/) | Clones public GitHub repository or tree URLs into temporary local workspaces for inspection. |

### Agent Workflow

| Skill | Source | Description |
| --- | --- | --- |
| `goal-loop-engineering` | [`skills/goal-loop-engineering`](skills/goal-loop-engineering/) | Drafts incremental Codex Goal prompts with scoped checkpoints and verifiable stopping conditions. |

### Review And Quality

| Skill | Source | Description |
| --- | --- | --- |
| `adversarial-verify` | [`skills/adversarial-verify`](skills/adversarial-verify/) | Probes target files for vulnerabilities through edge cases, error paths, security boundaries, and concurrency attacks. |
| `audit-agents-md` | [`skills/audit-agents-md`](skills/audit-agents-md/) | Audits and refines a `CLAUDE.md` or `AGENTS.md` file for instruction density, staleness, and effectiveness. |
| `proofread` | [`skills/proofread`](skills/proofread/) | Reviews text for AI writing tropes and mechanical prose patterns, then reports concrete rewrite suggestions. |
| `simplify` | [`skills/simplify`](skills/simplify/) | Simplifies recently changed code by applying only behavior-preserving fixes. |

## Maintenance

See [`docs/skill-lifecycle.md`](docs/skill-lifecycle.md) for adding, changing,
evaluating, and adopting skills.

Run the repository checks after changing skills:

```sh
uv run --with pyyaml python scripts/test_validate_skill_frontmatter.py
uv run --with pyyaml python scripts/validate_skill_frontmatter.py
git diff --check
```
