#!/usr/bin/env python3
"""Run repository-level checks for bilingual-paper-digest."""

from __future__ import annotations

import json
import py_compile
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPANION_SKILLS = (
    "bilingual-paper-reader",
    "bilingual-book-reader",
    "knowledge-base-curator",
)
EXPECTED_ROOT_RUNTIME = {
    "SKILL.md",
    "agents",
    "references",
    "requirements-docling.txt",
    "requirements-light.txt",
    "scripts",
}
EXCLUDED_INSTALL_ENTRIES = {
    ".git",
    ".github",
    ".gitignore",
    ".bilingual-paper-digest",
    "README.md",
    "companions",
    "examples",
}
EXCLUDED_INSTALL_SCRIPTS = {"install_skill.py", "run_checks.py"}


def run(command: list[str]) -> None:
    print("+ " + shlex.join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def parse_frontmatter(skill: Path) -> tuple[dict[str, str], str]:
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{skill.relative_to(ROOT)} must start with YAML frontmatter")

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail(f"{skill.relative_to(ROOT)} frontmatter is not closed")

    frontmatter = parts[1]
    values: dict[str, str] = {}
    current_key = ""
    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) and current_key:
            values[current_key] += " " + line.strip()
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        values[current_key] = value.strip()
    return values, parts[2]


def validate_skill_frontmatter(skill: Path, expected_name: str) -> None:
    values, body = parse_frontmatter(skill)
    display_path = skill.relative_to(ROOT)
    if values.get("name") != expected_name:
        fail(f"{display_path} frontmatter name must be {expected_name}")
    if not values.get("description"):
        fail(f"{display_path} frontmatter description is required")
    extra_keys = sorted(set(values) - {"name", "description"})
    if extra_keys:
        fail(f"{display_path} has unsupported frontmatter keys: {', '.join(extra_keys)}")
    if "[TODO" in body or "TODO:" in body:
        fail(f"{display_path} still contains template TODO text")
    if len(body.splitlines()) > 500:
        fail(f"{display_path} body exceeds 500 lines")


def check_skill_frontmatter() -> None:
    validate_skill_frontmatter(ROOT / "SKILL.md", "bilingual-paper-digest")
    for companion in COMPANION_SKILLS:
        validate_skill_frontmatter(ROOT / "companions" / companion / "SKILL.md", companion)


def referenced_paths(markdown: str) -> set[Path]:
    paths: set[Path] = set()
    for match in re.finditer(r"`([^`]+)`", markdown):
        content = match.group(1).strip()
        if not content:
            continue
        token = content.split()[0]
        token = token.rstrip(".,;:")
        if token.startswith("../bilingual-paper-digest/"):
            token = token.removeprefix("../bilingual-paper-digest/")
        if token == "SKILL.md" or token.startswith(
            ("references/", "examples/", "scripts/", "companions/", "requirements-")
        ):
            paths.add(ROOT / token)
    return paths


def check_referenced_resources() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    text += "\n" + (ROOT / "README.md").read_text(encoding="utf-8")
    for reference in sorted((ROOT / "references").glob("*.md")):
        text += "\n" + reference.read_text(encoding="utf-8")
    for companion in COMPANION_SKILLS:
        text += "\n" + (ROOT / "companions" / companion / "SKILL.md").read_text(encoding="utf-8")
    missing = sorted(path.relative_to(ROOT) for path in referenced_paths(text) if not path.exists())
    if missing:
        fail("Referenced resources do not exist: " + ", ".join(map(str, missing)))


def check_companion_metadata() -> None:
    root_metadata = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if "$bilingual-paper-digest" not in root_metadata:
        fail("Root openai.yaml default_prompt must mention $bilingual-paper-digest")
    for companion in COMPANION_SKILLS:
        skill_dir = ROOT / "companions" / companion
        if not (skill_dir / "SKILL.md").exists():
            fail(f"Companion missing SKILL.md: {companion}")
        metadata = skill_dir / "agents" / "openai.yaml"
        if not metadata.exists():
            fail(f"Companion missing agents/openai.yaml: {companion}")
        metadata_text = metadata.read_text(encoding="utf-8")
        if f"${companion}" not in metadata_text:
            fail(f"Companion openai.yaml default_prompt must mention ${companion}")


def check_gitignore() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in (".venv/", ".bilingual-paper-digest/", "translation_cache.jsonl"):
        if pattern not in gitignore:
            fail(f".gitignore missing runtime artifact pattern: {pattern}")


def check_scripts_compile() -> None:
    for script in sorted((ROOT / "scripts").glob("*.py")):
        print(f"py_compile {script.relative_to(ROOT)}")
        py_compile.compile(str(script), doraise=True)


def smoke_translation_cache_and_alignment() -> None:
    with tempfile.TemporaryDirectory(prefix="bpd-check-") as tmp:
        tmp_path = Path(tmp)
        units_path = tmp_path / "units.jsonl"
        cache_path = tmp_path / "translation_cache.jsonl"
        cached_path = tmp_path / "units.cached.jsonl"
        updated_cache_path = tmp_path / "translation_cache.updated.jsonl"
        note_path = tmp_path / "note.md"

        units = [
            {
                "translation_unit_id": "U0001",
                "page": 1,
                "source_hash": "hash-1",
                "source_sentence": "Leaf-inspired eutectic skins show robust wet adhesion [1].",
                "translation": "",
                "status": "pending",
            },
            {
                "translation_unit_id": "U0002",
                "page": 1,
                "source_hash": "hash-2",
                "source_sentence": "They maintain fatigue resistance under repeated deformation.",
                "translation": "它们在重复变形下保持抗疲劳性。",
                "status": "checked",
            },
        ]
        cache = [
            {
                "source_hash": "hash-1",
                "source_sentence": units[0]["source_sentence"],
                "translation": "叶启发的共晶皮肤表现出稳健的湿态黏附性[1]。",
                "status": "checked",
            }
        ]

        for path, records in ((units_path, units), (cache_path, cache)):
            with path.open("w", encoding="utf-8") as handle:
                for record in records:
                    handle.write(json.dumps(record, ensure_ascii=False) + "\n")

        note_path.write_text(
            "\n".join(
                [
                    "Leaf-inspired eutectic skins show robust wet adhesion [1].",
                    "\t叶启发的共晶皮肤表现出稳健的湿态黏附性[1]。",
                    "- They maintain fatigue resistance under repeated deformation.",
                    "\t它们在重复变形下保持抗疲劳性。",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        run(
            [
                sys.executable,
                "scripts/translation_cache.py",
                "apply",
                "--units",
                str(units_path),
                "--cache",
                str(cache_path),
                "--out",
                str(cached_path),
            ]
        )
        cached_records = [json.loads(line) for line in cached_path.read_text(encoding="utf-8").splitlines()]
        if not cached_records[0].get("translation"):
            fail("translation_cache.py apply did not fill cached translation")

        run(
            [
                sys.executable,
                "scripts/translation_cache.py",
                "update",
                "--units",
                str(cached_path),
                "--cache",
                str(updated_cache_path),
            ]
        )
        run(
            [
                sys.executable,
                "scripts/check_source_alignment.py",
                "--units",
                str(units_path),
                "--markdown",
                str(note_path),
                "--statuses",
                "pending,checked",
            ]
        )


def smoke_installer() -> None:
    with tempfile.TemporaryDirectory(prefix="bpd-install-") as tmp:
        codex_home = Path(tmp)
        run([sys.executable, "scripts/install_skill.py", "--codex-home", str(codex_home), "--clean"])
        installed = codex_home / "skills" / "bilingual-paper-digest"
        if not (installed / "SKILL.md").exists():
            fail("install_skill.py did not install SKILL.md")
        installed_entries = {path.name for path in installed.iterdir()}
        if installed_entries != EXPECTED_ROOT_RUNTIME:
            fail(f"Unexpected installed root entries: {sorted(installed_entries)}")
        for excluded in EXCLUDED_INSTALL_ENTRIES:
            if (installed / excluded).exists():
                fail(f"install_skill.py copied repository-only entry: {excluded}")
        for excluded in EXCLUDED_INSTALL_SCRIPTS:
            if (installed / "scripts" / excluded).exists():
                fail(f"install_skill.py copied repository-only script: {excluded}")
        for companion in COMPANION_SKILLS:
            companion_dir = codex_home / "skills" / companion
            if not (companion_dir / "SKILL.md").exists():
                fail(f"install_skill.py did not install companion: {companion}")
            companion_entries = {path.name for path in companion_dir.iterdir()}
            if companion_entries != {"SKILL.md", "agents"}:
                fail(f"Unexpected installed companion entries for {companion}: {sorted(companion_entries)}")
            sibling_root = companion_dir.parent / "bilingual-paper-digest" / "SKILL.md"
            if not sibling_root.exists():
                fail(f"Installed companion cannot find sibling root skill: {companion}")

        preserved = installed / ".venv" / "preserved.txt"
        preserved.parent.mkdir()
        preserved.write_text("keep", encoding="utf-8")
        (installed / "README.md").write_text("stale", encoding="utf-8")
        (installed / "references" / "stale.md").write_text("stale", encoding="utf-8")
        run([sys.executable, "scripts/install_skill.py", "--codex-home", str(codex_home)])
        if not preserved.exists():
            fail("Normal installer update removed the optional .venv")
        if (installed / "README.md").exists() or (installed / "references" / "stale.md").exists():
            fail("Normal installer update did not remove stale repository-owned files")


def main() -> int:
    check_skill_frontmatter()
    check_referenced_resources()
    check_companion_metadata()
    check_gitignore()
    check_scripts_compile()
    run([sys.executable, "scripts/check_digest.py", "examples/minimal-paper-note.md", "examples/obsidian-material-note.md"])
    run(
        [
            sys.executable,
            "scripts/check_knowledge_cards.py",
            "--strict",
            "examples/knowledge-card-term.md",
            "examples/knowledge-card-statistics.md",
        ]
    )
    smoke_translation_cache_and_alignment()
    smoke_installer()
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
