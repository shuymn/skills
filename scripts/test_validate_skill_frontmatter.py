#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_skill_frontmatter.py")


class ValidateSkillFrontmatterTest(unittest.TestCase):
    def run_validator(self, *paths: Path, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *(str(path) for path in paths)],
            check=False,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def write_skill(self, root: Path, name: str, body: str) -> Path:
        skill_dir = root / name
        skill_dir.mkdir()
        path = skill_dir / "SKILL.md"
        path.write_text(body, encoding="utf-8")
        return path

    def write_skill_with_notes(self, root: Path, body: str) -> Path:
        skill_dir = root / "example-skill"
        skill_dir.mkdir()
        (skill_dir / "references").mkdir()
        (skill_dir / "references" / "notes.md").write_text("# Notes\n", encoding="utf-8")
        path = skill_dir / "SKILL.md"
        path.write_text(body, encoding="utf-8")
        return path

    def test_accepts_valid_skill_with_support_link(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            skill = self.write_skill_with_notes(
                Path(raw_dir),
                """---
name: example-skill
description: "Use when a description contains: a colon."
allowed-tools: [Read]
---

See [notes](references/notes.md).
""",
            )

            result = self.run_validator(skill)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("skill validation ok (1 files)", result.stdout)

    def test_rejects_invalid_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            skill = self.write_skill(
                Path(raw_dir),
                "broken-skill",
                """---
name: broken-skill
description: Use when a description contains: an unquoted colon.
---
""",
            )

            result = self.run_validator(skill)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid YAML frontmatter", result.stderr)

    def test_rejects_name_that_does_not_match_directory(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            skill = self.write_skill(
                Path(raw_dir),
                "actual-name",
                """---
name: other-name
description: Use when testing directory mismatch.
---
""",
            )

            result = self.run_validator(skill)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("frontmatter.name must match directory name", result.stderr)

    def test_rejects_missing_support_link(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            skill = self.write_skill(
                Path(raw_dir),
                "example-skill",
                """---
name: example-skill
description: Use when testing missing links.
allowed-tools: [Read]
---

See [missing](references/missing.md).
""",
            )

            result = self.run_validator(skill)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("support link does not exist: references/missing.md", result.stderr)

    def test_rejects_default_run_with_no_discovered_skills(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            result = self.run_validator(cwd=root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no skills/*/SKILL.md files found", result.stderr)

    def test_rejects_support_link_that_escapes_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            root = Path(raw_dir)
            (root / "outside.md").write_text("# Outside\n", encoding="utf-8")
            skill = self.write_skill(
                root,
                "example-skill",
                """---
name: example-skill
description: Use when testing escaping links.
allowed-tools: [Read]
---

See [outside](references/../../outside.md).
""",
            )

            result = self.run_validator(skill)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("support link escapes skill directory: references/../../outside.md", result.stderr)

    def test_accepts_support_link_with_title_and_angle_destination(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            skill = self.write_skill_with_notes(
                Path(raw_dir),
                """---
name: example-skill
description: Use when testing practical Markdown links.
allowed-tools: [Read]
---

See [notes](references/notes.md "Notes") and [again](<references/notes.md>).
""",
            )

            result = self.run_validator(skill)

            self.assertEqual(result.returncode, 0, result.stderr)

    def test_ignores_support_like_link_inside_inline_code(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            skill = self.write_skill(
                Path(raw_dir),
                "example-skill",
                """---
name: example-skill
description: Use when testing inline code links.
allowed-tools: [Read]
---

Do not validate `[missing](references/missing.md)` inside code.
""",
            )

            result = self.run_validator(skill)

            self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_invalid_name_syntax(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            skill = self.write_skill(
                Path(raw_dir),
                "Bad_Name",
                """---
name: Bad_Name
description: Use when testing invalid names.
allowed-tools: [Read]
---
""",
            )

            result = self.run_validator(skill)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("frontmatter.name must use lowercase letters", result.stderr)

    def test_rejects_missing_allowed_tools(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            skill = self.write_skill(
                Path(raw_dir),
                "example-skill",
                """---
name: example-skill
description: Use when testing missing allowed tools.
---
""",
            )

            result = self.run_validator(skill)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("frontmatter.allowed-tools must be a non-empty string or list", result.stderr)

    def test_rejects_invalid_allowed_tools_list_item(self) -> None:
        with tempfile.TemporaryDirectory() as raw_dir:
            skill = self.write_skill(
                Path(raw_dir),
                "example-skill",
                """---
name: example-skill
description: Use when testing invalid allowed tools.
allowed-tools: [Read, 1]
---
""",
            )

            result = self.run_validator(skill)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("frontmatter.allowed-tools list items must be non-empty strings", result.stderr)


if __name__ == "__main__":
    unittest.main()
