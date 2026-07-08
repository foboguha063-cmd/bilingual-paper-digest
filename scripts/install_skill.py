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
    args = parser.parse_args()

    codex_home = args.codex_home.expanduser().resolve()
    destination = codex_home / "skills" / args.name
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.resolve() == ROOT.resolve():
        if args.clean:
            raise SystemExit("Refusing to --clean the running skill directory.")
        print(f"Source is already the installed skill: {destination}")
    else:
        copy_skill(ROOT, destination, args.clean)

    setup_environment(destination, list(dict.fromkeys(args.with_env)))

    print(f"Installed skill: {destination}")
    print("Restart Codex, then ask: 使用 bilingual-paper-digest 整理这篇文献。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
