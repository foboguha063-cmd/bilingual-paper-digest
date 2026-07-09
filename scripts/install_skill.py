#!/usr/bin/env python3
"""Install this skill into a local Codex skills directory."""

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
EXCLUDE_NAMES = {
    ".DS_Store",
    ".git",
    ".venv",
    "__pycache__",
    ".bilingual-paper-digest",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp"}


def default_codex_home() -> Path:
    env_home = os.environ.get("CODEX_HOME")
    if env_home:
        return Path(env_home).expanduser()
    return Path.home() / ".codex"


def should_exclude(path: Path) -> bool:
    if path.name in EXCLUDE_NAMES:
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False


def copy_skill(source: Path, destination: Path, clean: bool) -> None:
    if clean and destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():
        if should_exclude(item):
            continue
        target = destination / item.name
        if item.is_dir():
            shutil.copytree(
                item,
                target,
                dirs_exist_ok=True,
                ignore=lambda directory, names: [
                    name for name in names if should_exclude(Path(directory) / name)
                ],
            )
        else:
            shutil.copy2(item, target)


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
        if not source.exists():
            raise SystemExit(f"Companion skill missing: {source}")
        destination = skills_dir / companion
        copy_skill(source, destination, clean)
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
    parser.add_argument("--name", default=DEFAULT_NAME, help="Installed skill folder name.")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Replace the destination folder before installing.",
    )
    parser.add_argument(
        "--with-env",
        choices=("light", "docling"),
        action="append",
        default=[],
        help="Also create the optional runtime in the installed skill. Repeat for multiple profiles.",
    )
    parser.add_argument(
        "--no-companions",
        action="store_true",
        help="Install only the root bilingual-paper-digest skill, without companion entry-point skills.",
    )
    args = parser.parse_args()

    codex_home = args.codex_home.expanduser().resolve()
    skills_dir = codex_home / "skills"
    destination = skills_dir / args.name
    skills_dir.mkdir(parents=True, exist_ok=True)

    install_shared_companions = not args.no_companions and args.name == DEFAULT_NAME
    if not args.no_companions and args.name != DEFAULT_NAME:
        print("Skipping companion skills because --name changes the expected sibling root folder.")

    if destination.resolve() == ROOT.resolve():
        if args.clean:
            raise SystemExit("Refusing to --clean the running skill directory.")
        print(f"Source is already the installed skill: {destination}")
    else:
        copy_skill(ROOT, destination, args.clean)

    setup_environment(destination, list(dict.fromkeys(args.with_env)))

    companion_destinations = []
    if install_shared_companions:
        companion_destinations = install_companions(skills_dir, args.clean)

    print(f"Installed skill: {destination}")
    for companion_destination in companion_destinations:
        print(f"Installed companion: {companion_destination}")
    print("Restart Codex, then ask: 使用 bilingual-paper-reader 整理这篇论文。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
