#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NoReturn
from urllib.parse import unquote, urlparse

GITHUB_CLONE_PREFIX = "skill-github-workspace-"
CLONE_TIMEOUT_SECONDS = 30
SAFE_GITHUB_PART = re.compile(r"^[A-Za-z0-9_.-]+$")
SAFE_REF = re.compile(r"^[A-Za-z0-9._/-]+$")
SAFE_DIR_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


def fail(message: str) -> NoReturn:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def parse_github_repo_url(value: str) -> tuple[str, str, list[str] | None]:
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.netloc != "github.com":
        fail("github_clone_workspace only accepts https://github.com URLs.")

    segments = [unquote(segment) for segment in parsed.path.split("/") if segment]
    if any(segment in {".", ".."} or "/" in segment or "\\" in segment for segment in segments):
        fail("GitHub URL path contains unsupported segments.")
    if len(segments) < 2:
        fail("GitHub URL must include owner and repository name.")

    owner = segments[0]
    repo = segments[1].removesuffix(".git")
    if not SAFE_GITHUB_PART.fullmatch(owner) or not SAFE_GITHUB_PART.fullmatch(repo):
        fail("GitHub owner and repository name contain unsupported characters.")

    tree_segments: list[str] | None = None
    path_action = segments[2] if len(segments) >= 3 else None
    if path_action == "blob":
        fail(
            "GitHub blob URLs point to files and are not supported. "
            "Use the repository URL or a /tree/<ref>/<directory> URL instead."
        )
    if path_action == "tree":
        tree_segments = segments[3:]
        if not tree_segments:
            fail("GitHub tree URL must include a ref.")
    elif path_action is not None:
        fail("Only GitHub repository and /tree/<ref>/... URLs are supported.")

    return owner, repo, tree_segments


def sanitize_directory_name(value: str) -> str:
    name = value.strip()
    if not name:
        fail("Directory name must not be empty.")
    if name in {".", ".."} or "/" in name or not SAFE_DIR_NAME.fullmatch(name):
        fail("Directory name may only contain letters, numbers, '.', '_', and '-'.")
    return name


def run_git(args: list[str]) -> str:
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=CLONE_TIMEOUT_SECONDS,
        )
    except subprocess.CalledProcessError as error:
        details = "\n".join(part.strip() for part in [error.stderr, error.stdout] if part.strip())
        fail(details or str(error))
    except subprocess.TimeoutExpired:
        fail(f"git {' '.join(args)} timed out after {CLONE_TIMEOUT_SECONDS} seconds.")
    return result.stdout


def resolve_github_target(repo_url: str, tree_segments: list[str] | None) -> tuple[str | None, list[str]]:
    if tree_segments is None:
        return None, []

    stdout = run_git(["ls-remote", "--heads", "--tags", repo_url])
    refs: set[str] = set()
    for line in stdout.splitlines():
        parts = line.strip().split()
        if len(parts) < 2:
            continue
        ref = parts[1]
        refs.add(re.sub(r"^refs/heads/", "", ref))
        refs.add(re.sub(r"^refs/tags/", "", ref))

    for length in range(len(tree_segments), 0, -1):
        ref = "/".join(tree_segments[:length])
        if ref not in refs:
            continue
        if not SAFE_REF.fullmatch(ref):
            fail("GitHub ref contains unsupported characters.")
        return ref, tree_segments[length:]

    fail(
        "Could not resolve the GitHub tree URL ref. "
        "Use a repository URL or a URL with an existing branch or tag."
    )


def resolve_safe_subpath(root: Path, subpath_segments: list[str]) -> Path:
    for segment in subpath_segments:
        if segment in {"", ".", ".."}:
            fail("GitHub URL path contains unsupported segments.")

    path = (root.joinpath(*subpath_segments) if subpath_segments else root).resolve(strict=True)
    if not path.is_relative_to(root):
        fail(f"GitHub URL path resolves outside the cloned repository: {path}")
    if not path.is_dir():
        fail(f"GitHub URL path is not a directory: {path}")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="Clone a GitHub repository into a temporary workspace.")
    parser.add_argument("url", help="https://github.com/owner/repo or /tree/<ref>/<directory> URL")
    parser.add_argument("--directory-name", help="Optional local clone directory name")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    owner, repo, tree_segments = parse_github_repo_url(args.url)
    directory_name = sanitize_directory_name(args.directory_name or repo)
    display_url = f"https://github.com/{owner}/{repo}"
    repo_url = f"{display_url}.git"

    temp_root = Path(tempfile.mkdtemp(prefix=GITHUB_CLONE_PREFIX)).resolve()
    clone_path = temp_root / directory_name

    try:
        ref, subpath_segments = resolve_github_target(repo_url, tree_segments)
        clone_args = ["clone", "--depth", "1", "--filter=blob:none", "--single-branch"]
        if ref:
            clone_args.extend(["--branch", ref])
        clone_args.extend([repo_url, str(clone_path)])
        run_git(clone_args)

        canonical_clone_path = clone_path.resolve(strict=True)
        registered_path = resolve_safe_subpath(canonical_clone_path, subpath_segments)
    except BaseException:
        shutil.rmtree(temp_root, ignore_errors=True)
        raise

    result = {
        "name": registered_path.name,
        "path": str(registered_path),
        "url": display_url,
        "ref": ref,
        "subPath": "/".join(subpath_segments) or None,
        "tempRoot": str(temp_root),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("Cloned GitHub workspace.")
    print(f"name: {result['name']}")
    print(f"path: {result['path']}")
    print(f"url: {result['url']}")
    if result["ref"]:
        print(f"ref: {result['ref']}")
    if result["subPath"]:
        print(f"subPath: {result['subPath']}")
    print("")
    print("Use the absolute path above when reading, searching, or running read-only commands in this repository.")
    print(f"Cleanup when finished: rm -rf {temp_root}")


if __name__ == "__main__":
    main()
