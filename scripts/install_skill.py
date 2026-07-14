#!/usr/bin/env python3
"""Install one or all bilingual-paper-digest skills into Codex."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO / "skills"
VERSION = (REPO / "VERSION").read_text(encoding="utf-8").strip()
SKILL_NAMES = (
    "bilingual-paper-digest",
    "bilingual-paper-reader",
    "bilingual-book-reader",
    "knowledge-base-curator",
)


def default_codex_home() -> Path:
    value = os.environ.get("CODEX_HOME")
    return Path(value).expanduser() if value else Path.home() / ".codex"


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def copy_skill(source: Path, destination: Path, clean: bool) -> None:
    preserved_venv = destination / ".venv"
    temporary_venv = destination.parent / f".{destination.name}-venv-preserved"
    if not clean and preserved_venv.exists():
        remove_path(temporary_venv)
        preserved_venv.rename(temporary_venv)
    remove_path(destination)
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store"),
    )
    if temporary_venv.exists():
        temporary_venv.rename(preserved_venv)


def setup_environment(destination: Path, profiles: list[str]) -> None:
    if not profiles:
        return
    command = [sys.executable, str(destination / "scripts" / "setup_environment.py")]
    for profile in profiles:
        command.extend(("--profile", profile))
    subprocess.check_call(command)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=default_codex_home())
    parser.add_argument(
        "--skill",
        choices=SKILL_NAMES,
        action="append",
        help="Install only this skill. Repeat to select several; default installs all.",
    )
    parser.add_argument("--clean", action="store_true", help="Also replace an existing optional .venv.")
    parser.add_argument(
        "--with-env",
        choices=("light", "docling"),
        action="append",
        default=[],
        help="Create an optional environment in the root skill (or selected reader).",
    )
    parser.add_argument(
        "--no-companions",
        action="store_true",
        help="Backward-compatible alias for --skill bilingual-paper-digest.",
    )
    args = parser.parse_args()

    if args.no_companions and args.skill:
        parser.error("--no-companions cannot be combined with --skill")
    selected = ["bilingual-paper-digest"] if args.no_companions else (args.skill or list(SKILL_NAMES))
    selected = list(dict.fromkeys(selected))
    skills_dir = args.codex_home.expanduser().resolve() / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    installed: list[Path] = []
    for name in selected:
        source = SOURCE_ROOT / name
        if not (source / "SKILL.md").exists():
            raise SystemExit(f"Skill source missing: {source}")
        destination = skills_dir / name
        if destination.resolve() == source.resolve():
            print(f"Source is already installed: {destination}")
        else:
            copy_skill(source, destination, args.clean)
        installed.append(destination)

    if args.with_env:
        environment_target = next(
            (
                path
                for path in installed
                if (path / "scripts" / "setup_environment.py").exists()
            ),
            None,
        )
        if environment_target is None:
            raise SystemExit("Selected skill has no optional PDF environment.")
        setup_environment(environment_target, list(dict.fromkeys(args.with_env)))

    for destination in installed:
        print(f"Installed: {destination}")
    print(f"Suite version: {VERSION}")
    print("Restart Codex, then ask: 使用 bilingual-paper-reader 整理这篇论文。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
