#!/usr/bin/env python3
"""Materialize self-contained companion skills from the canonical root runtime."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "skills"
CANONICAL = SKILLS / "bilingual-paper-digest"
CONTENT = {
    "bilingual-paper-reader": {
        "references": (
            "bilingual-output-contract.md",
            "book-translation-mode.md",
            "obsidian-vault-style.md",
            "paper-type-routing.md",
            "pdf-extraction-pipeline.md",
            "translation-memory.md",
        ),
        "scripts": (
            "build_translation_units.py",
            "check_bilingual_quality.py",
            "check_digest.py",
            "check_source_alignment.py",
            "extract_pdf_structure.py",
            "probe_tools.py",
            "render_bilingual_markdown.py",
            "setup_environment.py",
            "translation_cache.py",
        ),
        "files": ("requirements-light.txt", "requirements-docling.txt"),
    },
    "bilingual-book-reader": {
        "references": (
            "bilingual-output-contract.md",
            "book-translation-mode.md",
            "pdf-extraction-pipeline.md",
            "translation-memory.md",
        ),
        "scripts": (
            "build_translation_units.py",
            "check_bilingual_quality.py",
            "check_digest.py",
            "check_source_alignment.py",
            "extract_pdf_structure.py",
            "probe_tools.py",
            "render_bilingual_markdown.py",
            "setup_environment.py",
            "translation_cache.py",
        ),
        "files": ("requirements-light.txt", "requirements-docling.txt"),
    },
    "knowledge-base-curator": {
        "references": ("knowledge-card-system.md", "obsidian-vault-style.md"),
        "scripts": ("check_knowledge_cards.py",),
        "files": (),
    },
}


def expected_files(skill: str) -> dict[Path, Path]:
    config = CONTENT[skill]
    pairs: dict[Path, Path] = {}
    for category in ("references", "scripts"):
        for name in config[category]:
            pairs[CANONICAL / category / name] = SKILLS / skill / category / name
    for name in config["files"]:
        pairs[CANONICAL / name] = SKILLS / skill / name
    return pairs


def sync_skill(skill: str, check: bool) -> list[str]:
    errors: list[str] = []
    destination = SKILLS / skill
    pairs = expected_files(skill)
    expected_targets = set(pairs.values())

    for source, target in pairs.items():
        if not source.exists():
            errors.append(f"missing canonical file: {source.relative_to(REPO)}")
            continue
        if check:
            if not target.exists() or target.read_bytes() != source.read_bytes():
                errors.append(f"out of sync: {target.relative_to(REPO)}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    for category in ("references", "scripts"):
        folder = destination / category
        if not folder.exists():
            continue
        for target in folder.iterdir():
            if target.is_file() and target not in expected_targets:
                if check:
                    errors.append(f"unexpected generated file: {target.relative_to(REPO)}")
                else:
                    target.unlink()
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated copies without changing files.")
    args = parser.parse_args()

    errors: list[str] = []
    for skill in CONTENT:
        errors.extend(sync_skill(skill, args.check))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Companion skills are self-contained and synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
