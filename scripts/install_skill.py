#!/usr/bin/env python3
"""Install the minimal bilingual-paper-digest runtime into Codex skills."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NAME = "bilingual-paper-digest"
COMPANION_ROOT = ROOT / "companions"
COMPANION_SKILLS = (
    "bilingual-paper-reader",
    "bilingual-book-reader",
    "knowledge-base-curator",
)
ROOT_RUNTIME_FILES = (
    "SKILL.md",
    "requirements-light.txt",
    "requirements-docling.txt",
)
ROOT_RUNTIME_DIRS = ("agents", "references")
ROOT_RUNTIME_SCRIPTS = (
    "build_translation_units.py",
    "check_digest.py",
    "check_knowledge_cards.py",
    "check_source_alignment.py",
    "extract_pdf_structure.py",
    "probe_tools.py",
    "setup_environment.py",
    "translation_cache.py",
)
REPOSITORY_ONLY_ENTRIES = (
    ".git",
    ".github",
    ".gitignore",
    "README.md",
    "companions",
    "examples",
)


def default_codex_home() -> Path:
    env_home = os.environ.get("CODEX_HOME")
    return Path(env_home).expanduser() if env_home else Path.home() / ".codex"


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def prepare_destination(destination: Path, clean: bool) -> None:
    if clean:
        remove_path(destination)
    destination.mkdir(parents=True, exist_ok=True)


def replace_path(source: Path, destination: Path) -> None:
    remove_path(destination)
    if source.is_dir():
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".DS_Store"),
        )
    else:
        shutil.copy2(source, destination)


def copy_root_skill(destination: Path, clean: bool) -> None:
    """Sync only files needed by an installed skill, preserving an existing .venv."""
    prepare_destination(destination, clean)

    for name in REPOSITORY_ONLY_ENTRIES:
        remove_path(destination / name)

    for name in ROOT_RUNTIME_FILES:
        replace_path(ROOT / name, destination / name)
    for name in ROOT_RUNTIME_DIRS:
        replace_path(ROOT / name, destination / name)

    scripts_destination = destination / "scripts"
    remove_path(scripts_destination)
    scripts_destination.mkdir()
    for name in ROOT_RUNTIME_SCRIPTS:
        shutil.copy2(ROOT / "scripts" / name, scripts_destination / name)


def copy_companion(source: Path, destination: Path, clean: bool) -> None:
    prepare_destination(destination, clean)
    replace_path(source / "SKILL.md", destination / "SKILL.md")
    replace_path(source / "agents", destination / "agents")


def setup_environment(destination: Path, profiles: list[str]) -> None:
    if not profiles:
        return
    command = [sys.executable, str(destination / "scripts" / "setup_environment.py")]
    for profile in profiles:
        command.extend(["--profile", profile])
    subprocess.check_call(command)


def install_companions(skills_dir: Path, clean: bool) -> list[Path]:
    installed: list[Path] = []
    for companion in COMPANION_SKILLS:
        source = COMPANION_ROOT / companion
        if not (source / "SKILL.md").exists():
            raise SystemExit(f"Companion skill missing: {source}")
        destination = skills_dir / companion
        copy_companion(source, destination, clean)
        installed.append(destination)
    return installed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=default_codex_home(),
        help="Codex home directory. Defaults to $CODEX_HOME or ~/.codex.",
    )
    parser.add_argument("--name", default=DEFAULT_NAME, help="Installed root skill folder name.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Replace destinations completely, including an existing optional .venv.",
    )
    parser.add_argument(
        "--with-env",
        choices=("light", "docling"),
        action="append",
        default=[],
        help="Create an optional runtime in the installed root. Repeat for multiple profiles.",
    )
    parser.add_argument(
        "--no-companions",
        action="store_true",
        help="Install only the root router without the three narrow entry points.",
    )
    args = parser.parse_args()

    codex_home = args.codex_home.expanduser().resolve()
    skills_dir = codex_home / "skills"
    destination = skills_dir / args.name
    skills_dir.mkdir(parents=True, exist_ok=True)

    install_shared_companions = not args.no_companions and args.name == DEFAULT_NAME
    if not args.no_companions and args.name != DEFAULT_NAME:
        print("Skipping companions because --name changes their expected sibling root folder.")

    if destination.resolve() == ROOT.resolve():
        if args.clean:
            raise SystemExit("Refusing to --clean the running repository.")
        print(f"Source is already the installed root: {destination}")
    else:
        copy_root_skill(destination, args.clean)

    setup_environment(destination, list(dict.fromkeys(args.with_env)))
    companion_destinations = (
        install_companions(skills_dir, args.clean) if install_shared_companions else []
    )

    print(f"Installed root: {destination}")
    for companion_destination in companion_destinations:
        print(f"Installed companion: {companion_destination}")
    print("Restart Codex, then ask: 使用 bilingual-paper-reader 整理这篇论文。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
