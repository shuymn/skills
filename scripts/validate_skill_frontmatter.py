#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


MAX_DESCRIPTION_LENGTH = 1024
MAX_SKILL_NAME_LENGTH = 64
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
SUPPORT_LINK_PREFIXES = ("references/", "scripts/")


@dataclass(frozen=True)
class ValidationError:
    path: Path
    message: str
    line: int | None = None

    def format(self) -> str:
        location = str(self.path)
        if self.line is not None:
            location = f"{location}:{self.line}"
        return f"{location}: {self.message}"


def repo_root() -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def repo_skill_files() -> list[Path]:
    root = repo_root()
    if root is None:
        return []
    return sorted(root.glob("skills/*/SKILL.md"))


def frontmatter(path: Path) -> tuple[str | None, int | None, ValidationError | None]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None, None, ValidationError(path, "missing YAML frontmatter", 1)

    for index, line in enumerate(lines[1:], start=2):
        if line == "---":
            return "\n".join(lines[1 : index - 1]), index, None

    return None, None, ValidationError(path, "missing closing frontmatter delimiter", 1)


def load_frontmatter(path: Path) -> tuple[dict[str, object] | None, int | None, ValidationError | None]:
    raw, close_line, error = frontmatter(path)
    if error is not None:
        return None, close_line, error

    try:
        parsed = yaml.safe_load(raw or "")
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = mark.line + 2 if mark is not None else None
        problem = getattr(exc, "problem", None) or str(exc)
        return None, close_line, ValidationError(path, f"invalid YAML frontmatter: {problem}", line)

    if not isinstance(parsed, dict):
        return None, close_line, ValidationError(path, "frontmatter must be a YAML mapping", 2)

    return parsed, close_line, None


def without_inline_code(body: str) -> str:
    return re.sub(r"`[^`]*`", lambda match: " " * len(match.group(0)), body)


def link_destination(body: str, start: int) -> tuple[str | None, int]:
    cursor = start
    if cursor < len(body) and body[cursor] == "<":
        end = body.find(">", cursor + 1)
        if end == -1:
            return None, cursor
        return body[cursor + 1 : end], end + 1

    depth = 0
    while cursor < len(body):
        char = body[cursor]
        if char.isspace() and depth == 0:
            break
        if char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                break
            depth -= 1
        cursor += 1

    if cursor == start:
        return None, cursor
    return body[start:cursor], cursor


def markdown_support_links(body: str) -> list[str]:
    links: list[str] = []
    body = without_inline_code(body)
    cursor = 0
    while True:
        start = body.find("](", cursor)
        if start == -1:
            break
        target, cursor = link_destination(body, start + 2)
        if target is None:
            continue
        target = target.split("#", 1)[0]
        if target.startswith(SUPPORT_LINK_PREFIXES):
            links.append(target)
    return links


def validate(path: Path) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if path.name != "SKILL.md":
        return [ValidationError(path, "expected a SKILL.md file")]
    if not path.exists():
        return [ValidationError(path, "file does not exist")]

    parsed, close_line, error = load_frontmatter(path)
    if error is not None:
        return [error]
    assert parsed is not None

    name = parsed.get("name")
    description = parsed.get("description")
    allowed_tools = parsed.get("allowed-tools")

    if not isinstance(name, str) or not name.strip():
        errors.append(ValidationError(path, "frontmatter.name must be a non-empty string", 2))
    elif name != path.parent.name:
        errors.append(
            ValidationError(
                path,
                f"frontmatter.name must match directory name: expected {path.parent.name!r}, got {name!r}",
                2,
            )
        )
    else:
        if len(name) > MAX_SKILL_NAME_LENGTH:
            errors.append(ValidationError(path, f"frontmatter.name must be <= {MAX_SKILL_NAME_LENGTH} characters", 2))
        if not SKILL_NAME_PATTERN.fullmatch(name) or name.startswith("-") or name.endswith("-") or "--" in name:
            errors.append(
                ValidationError(
                    path,
                    "frontmatter.name must use lowercase letters, digits, and single hyphens",
                    2,
                )
            )

    if not isinstance(description, str) or not description.strip():
        errors.append(ValidationError(path, "frontmatter.description must be a non-empty string", 2))
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            ValidationError(
                path,
                f"frontmatter.description must be <= {MAX_DESCRIPTION_LENGTH} characters",
                2,
            )
        )

    if not isinstance(allowed_tools, str | list) or not allowed_tools:
        errors.append(ValidationError(path, "frontmatter.allowed-tools must be a non-empty string or list", 2))
    elif isinstance(allowed_tools, str) and not allowed_tools.strip():
        errors.append(ValidationError(path, "frontmatter.allowed-tools must be a non-empty string or list", 2))
    elif isinstance(allowed_tools, list) and not all(isinstance(tool, str) and tool.strip() for tool in allowed_tools):
        errors.append(ValidationError(path, "frontmatter.allowed-tools list items must be non-empty strings", 2))

    if close_line is not None:
        skill_root = path.parent.resolve()
        body = "\n".join(path.read_text(encoding="utf-8").splitlines()[close_line:])
        for link in markdown_support_links(body):
            target = (path.parent / link).resolve()
            if not target.is_relative_to(skill_root):
                errors.append(ValidationError(path, f"support link escapes skill directory: {link}"))
            elif not target.exists():
                errors.append(ValidationError(path, f"support link does not exist: {link}"))

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate tracked SKILL.md frontmatter.")
    parser.add_argument("paths", nargs="*", type=Path, help="Optional SKILL.md paths to validate")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.paths:
        paths = args.paths
    else:
        paths = repo_skill_files()
        if not paths:
            print("skill validation failed: no skills/*/SKILL.md files found", file=sys.stderr)
            return 1
    paths = sorted(Path(os.fspath(path)) for path in paths)

    errors = [error for path in paths for error in validate(path)]
    if errors:
        print(f"skill validation failed ({len(errors)} errors)", file=sys.stderr)
        for error in errors:
            print(error.format(), file=sys.stderr)
        return 1

    print(f"skill validation ok ({len(paths)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
