# Skill Lifecycle

This repository keeps personal agent skills as editable source under
`skills/<skill-name>/`. Keep the distribution shape simple until the install
tooling is verified to support nested category directories.

## Add a Skill

1. Create `skills/<skill-name>/SKILL.md`.
2. Set `name:` to exactly `<skill-name>`.
3. Write `description:` as the trigger contract:
   - Use `Use when ...` for skills that should auto-trigger from task shape.
   - Use `Invoke ONLY when ...` for meta skills that should run only on explicit request.
4. Put supporting material under the same skill directory, usually
   `references/` or `scripts/`.
5. Add the skill to the catalog in `README.md`.

## Change a Skill

1. Keep edits inside the target `skills/<skill-name>/` directory unless the
   change is shared repo tooling or catalog text.
2. If the body links to `references/...` or `scripts/...`, keep the target file
   self-contained inside that skill directory.
3. Run the repository checks after changing skills.

## Evaluate a Skill

Most edits only need static validation. Add `evals/` only when a skill is
high-risk or repeatedly misfires.

Good candidates for evals:

- Skills that create commits, pull requests, or other durable side effects.
- Skills that decide whether to apply reviewer feedback.
- Skills with known near-miss trigger failures.

Keep eval scenarios skill-local:

```text
skills/<skill-name>/
├── SKILL.md
└── evals/
    ├── eval.yaml
    └── tasks/
        ├── typical.yaml
        └── edge.yaml
```

## Adopt External Ideas

Before copying an external skill or workflow into this repo:

1. Confirm the task is recurring, not a one-off.
2. Check whether an existing local skill already covers it.
3. Prefer adapting the smallest useful idea over importing a full framework.
4. Record rejected candidates or rejected patterns in this document when the
   reason is likely to recur.

## Verification

After changing skills or repository skill tooling:

```sh
uv run --with pyyaml python scripts/test_validate_skill_frontmatter.py
uv run --with pyyaml python scripts/validate_skill_frontmatter.py
git diff --check
```

Installing or reinstalling skills is intentionally outside the default
maintenance flow. Do it only when the user explicitly asks for installation.
