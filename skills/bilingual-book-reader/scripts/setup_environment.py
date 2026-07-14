#!/usr/bin/env python3
"""Create a local optional runtime for bilingual-paper-digest."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_FILES = {
    "light": ROOT / "requirements-light.txt",
    "docling": ROOT / "requirements-docling.txt",
}


def venv_python(venv_dir: Path) -> Path:
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def run(command: list[str], dry_run: bool) -> None:
    print("+ " + " ".join(command))
    if not dry_run:
        subprocess.check_call(command)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--venv", type=Path, default=ROOT / ".venv", help="Virtual environment path.")
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILE_FILES),
        action="append",
        default=[],
        help="Dependency profile to install. Repeat for multiple profiles.",
    )
    parser.add_argument("--python", default=sys.executable, help="Python executable used to create the venv.")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running them.")
    args = parser.parse_args()

    venv_dir = args.venv.resolve()
    profiles = list(dict.fromkeys(args.profile or ["light"]))

    if not venv_dir.exists():
        print(f"Creating venv: {venv_dir}")
        run([args.python, "-m", "venv", str(venv_dir)], args.dry_run)

    py = venv_python(venv_dir)
    run([str(py), "-m", "pip", "install", "--upgrade", "pip"], args.dry_run)

    for profile in profiles:
        requirements = PROFILE_FILES[profile]
        run([str(py), "-m", "pip", "install", "-r", str(requirements)], args.dry_run)

    print("\nEnvironment ready.")
    print(f"Python: {py}")
    print(f"Probe:  {py} {ROOT / 'scripts' / 'probe_tools.py'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
