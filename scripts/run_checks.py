#!/usr/bin/env python3
"""Run deterministic repository and end-to-end checks."""

from __future__ import annotations

import importlib.util
import json
import re
import runpy
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO / "skills"
SKILL_NAMES = (
    "bilingual-paper-digest",
    "bilingual-paper-reader",
    "bilingual-book-reader",
    "knowledge-base-curator",
)
ROOT_SKILL = SKILLS_ROOT / "bilingual-paper-digest"


def run(command: list[str], expect_failure: bool = False) -> subprocess.CompletedProcess[str]:
    print("+ " + shlex.join(command))
    result = subprocess.run(command, cwd=REPO, text=True, capture_output=True)
    if expect_failure:
        if result.returncode == 0:
            fail("command unexpectedly succeeded: " + shlex.join(command))
        print(f"EXPECTED FAILURE ({result.returncode})")
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="")
        return result
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        fail(f"command failed ({result.returncode}): " + shlex.join(command))
    return result


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def parse_frontmatter(skill: Path) -> tuple[dict[str, str], str]:
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{skill.relative_to(REPO)} must start with YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        fail(f"{skill.relative_to(REPO)} frontmatter is not closed")
    values: dict[str, str] = {}
    current_key = ""
    for line in parts[1].splitlines():
        if line.startswith((" ", "\t")) and current_key:
            values[current_key] += " " + line.strip()
        elif ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            values[current_key] = value.strip()
    return values, parts[2]


def check_skill_structure() -> None:
    version = (REPO / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("VERSION must use semantic versioning")
    if (REPO / "SKILL.md").exists():
        fail("repository root must not contain SKILL.md; standard installers should discover skills/*")
    discovered = sorted(path.parent.name for path in SKILLS_ROOT.glob("*/SKILL.md"))
    if discovered != sorted(SKILL_NAMES):
        fail(f"unexpected skill set: {discovered}")

    for name in SKILL_NAMES:
        skill_dir = SKILLS_ROOT / name
        skill = skill_dir / "SKILL.md"
        values, body = parse_frontmatter(skill)
        if values.get("name") != name:
            fail(f"{skill.relative_to(REPO)} frontmatter name must be {name}")
        if not values.get("description"):
            fail(f"{skill.relative_to(REPO)} description is required")
        if set(values) != {"name", "description"}:
            fail(f"{skill.relative_to(REPO)} frontmatter must contain only name and description")
        if len(body.splitlines()) > 120:
            fail(f"{skill.relative_to(REPO)} exceeds the lightweight 120-line limit")
        if "[TODO" in body or "TODO:" in body:
            fail(f"{skill.relative_to(REPO)} contains template TODO text")
        metadata = skill_dir / "agents" / "openai.yaml"
        if not metadata.exists() or f"${name}" not in metadata.read_text(encoding="utf-8"):
            fail(f"{metadata.relative_to(REPO)} must reference ${name}")
        if name != "bilingual-paper-digest" and "../bilingual-paper-digest" in skill.read_text(encoding="utf-8"):
            fail(f"{name} still depends on a sibling skill")


def referenced_paths(text: str) -> set[str]:
    paths: set[str] = set()
    for match in re.finditer(r"`([^`]+)`", text):
        content = match.group(1).strip()
        if not content:
            continue
        token = content.split()[0].rstrip(".,;:")
        if token.startswith(("references/", "scripts/", "requirements-")):
            paths.add(token)
    return paths


def check_references() -> None:
    for name in SKILL_NAMES:
        skill_dir = SKILLS_ROOT / name
        markdown_files = [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]
        for markdown in markdown_files:
            text = markdown.read_text(encoding="utf-8")
            for relative in referenced_paths(text):
                if not (skill_dir / relative).exists():
                    fail(f"{markdown.relative_to(REPO)} references missing {relative}")
            if markdown.parent.name == "references" and len(text.splitlines()) > 100:
                first_lines = "\n".join(text.splitlines()[:35]).lower()
                if "## contents" not in first_lines:
                    fail(f"long reference needs a Contents section: {markdown.relative_to(REPO)}")


def check_generated_skills() -> None:
    run([sys.executable, "scripts/sync_skills.py", "--check"])


def check_python() -> None:
    for script in sorted(REPO.glob("scripts/*.py")) + sorted(SKILLS_ROOT.glob("*/scripts/*.py")):
        print(f"compile {script.relative_to(REPO)}")
        compile(script.read_text(encoding="utf-8"), str(script), "exec")


def check_sentence_boundaries() -> None:
    namespace = runpy.run_path(str(ROOT_SKILL / "scripts" / "build_translation_units.py"))
    split_sentences = namespace["split_sentences"]
    cases = {
        "This is sentence one. This is sentence two.": 2,
        "Results were significant (P < 0.05). However, the effect was small.": 2,
        "Smith et al. reported the result. It was replicated.": 2,
        "The U.S. population was studied. Results were stable.": 2,
        "The finding was reported by Smith et al. This result was replicated.": 2,
    }
    for text, expected in cases.items():
        actual = len(split_sentences(text))
        if actual != expected:
            fail(f"sentence boundary regression: expected {expected}, got {actual}: {text}")


def check_requirements() -> None:
    for requirement_file in SKILLS_ROOT.glob("*/requirements-*.txt"):
        for line in requirement_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "<" not in stripped:
                fail(f"dependency lacks an upper compatibility bound: {requirement_file.relative_to(REPO)}: {stripped}")


def check_eval_scenarios() -> None:
    path = REPO / "evals" / "scenarios.jsonl"
    prompts: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        record = json.loads(line)
        prompt = str(record.get("prompt", "")).strip()
        expected = record.get("expected_skill")
        if not prompt or prompt in prompts:
            fail(f"{path.relative_to(REPO)}:{line_number} has an empty or duplicate prompt")
        if expected is not None and expected not in SKILL_NAMES:
            fail(f"{path.relative_to(REPO)}:{line_number} has unknown expected_skill")
        if not record.get("must_preserve"):
            fail(f"{path.relative_to(REPO)}:{line_number} needs observable invariants")
        prompts.add(prompt)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def create_text_pdf(path: Path) -> None:
    content = b"BT /F1 12 Tf 72 720 Td (Fixture DOI 10.1234/test.2026. Results were significant.) Tj ET"
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream",
        b"<< /Title (Academic Fixture) /Author (Bilingual Paper Digest) >>",
    ]
    payload = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, body in enumerate(objects, start=1):
        offsets.append(len(payload))
        payload.extend(f"{number} 0 obj\n".encode("ascii"))
        payload.extend(body)
        payload.extend(b"\nendobj\n")
    xref = len(payload)
    payload.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    payload.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    payload.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R /Info 6 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(payload)


def smoke_real_pdf_extraction() -> None:
    if importlib.util.find_spec("pypdf") is None:
        print("SKIP real PDF extraction smoke: optional pypdf is not installed")
        return
    with tempfile.TemporaryDirectory(prefix="bpd-pdf-") as temporary:
        tmp = Path(temporary)
        pdf = tmp / "fixture.pdf"
        output = tmp / "extracted"
        create_text_pdf(pdf)
        run(
            [
                sys.executable,
                str(ROOT_SKILL / "scripts" / "extract_pdf_structure.py"),
                str(pdf),
                "--method",
                "pypdf",
                "--out-dir",
                str(output),
            ]
        )
        records = read_jsonl(output / "source.jsonl")
        manifest = json.loads((output / "source_map.json").read_text(encoding="utf-8"))
        if not records or "Results were significant" not in str(records[0].get("text", "")):
            fail("real PDF smoke did not extract the expected text")
        if manifest.get("detected_doi") != "10.1234/test.2026":
            fail("real PDF smoke did not detect the fixture DOI")
        metadata = manifest.get("document_metadata", {})
        if not isinstance(metadata, dict) or metadata.get("Title") != "Academic Fixture":
            fail("real PDF smoke did not preserve PDF metadata")


def smoke_golden_pipeline() -> None:
    translations = {
        "Results were significant (P < 0.05).": "结果具有统计学显著性（P < 0.05）。",
        "However, the effect was not observed at 2.5 mg [1-3].": "然而，在2.5 mg时未观察到该效应[1-3]。",
        "Smith et al. measured IL-6 and p53 expression.": "Smith等测量了IL-6和p53的表达。",
        "The 95% CI was 1.2-2.4.": "95% CI为1.2-2.4。",
    }
    script = ROOT_SKILL / "scripts"
    with tempfile.TemporaryDirectory(prefix="bpd-golden-") as temporary:
        tmp = Path(temporary)
        units_path = tmp / "units.jsonl"
        translated_path = tmp / "translated.jsonl"
        note_path = tmp / "note.md"
        cache_path = tmp / "cache.jsonl"
        cached_path = tmp / "cached.jsonl"

        run(
            [
                sys.executable,
                str(script / "build_translation_units.py"),
                "tests/fixtures/academic-source.jsonl",
                "--out",
                str(units_path),
            ]
        )
        units = read_jsonl(units_path)
        if len(units) != 4 or [unit.get("sentence_count") for unit in units] != [2, 2, 2, 2]:
            fail("sentence splitter did not create two sentences for each fixture paragraph")
        if len({unit.get("paragraph_id") for unit in units}) != 2:
            fail("translation units lost paragraph identity")

        for unit in units:
            sentence = str(unit.get("source_sentence", ""))
            unit["translation"] = translations[sentence]
            unit["status"] = "checked"
        write_jsonl(translated_path, units)

        run([sys.executable, str(script / "check_bilingual_quality.py"), "--units", str(translated_path)])
        run(
            [
                sys.executable,
                str(script / "render_bilingual_markdown.py"),
                "--units",
                str(translated_path),
                "--out",
                str(note_path),
            ]
        )
        expected = (REPO / "tests" / "golden" / "academic-note-body.md").read_text(encoding="utf-8")
        if note_path.read_text(encoding="utf-8") != expected:
            fail("rendered bilingual Markdown differs from the golden output")
        run(
            [
                sys.executable,
                str(script / "check_source_alignment.py"),
                "--units",
                str(translated_path),
                "--markdown",
                str(note_path),
            ]
        )

        bad_units = json.loads(json.dumps(units))
        bad_units[1]["translation"] = "然而，在5 mg时观察到该效应。"
        bad_path = tmp / "bad.jsonl"
        write_jsonl(bad_path, bad_units)
        run(
            [sys.executable, str(script / "check_bilingual_quality.py"), "--units", str(bad_path)],
            expect_failure=True,
        )

        run(
            [
                sys.executable,
                str(script / "translation_cache.py"),
                "update",
                "--units",
                str(translated_path),
                "--cache",
                str(cache_path),
            ]
        )
        run(
            [
                sys.executable,
                str(script / "translation_cache.py"),
                "apply",
                "--units",
                str(units_path),
                "--cache",
                str(cache_path),
                "--out",
                str(cached_path),
            ]
        )
        if not all(str(unit.get("translation", "")).strip() for unit in read_jsonl(cached_path)):
            fail("translation cache did not restore all checked units")


def smoke_batch_resume() -> None:
    script = ROOT_SKILL / "scripts"
    translations = {
        "Results were significant (P < 0.05).": "结果具有统计学显著性（P < 0.05）。",
        "However, the effect was not observed at 2.5 mg [1-3].": "然而，在2.5 mg时未观察到该效应[1-3]。",
    }
    with tempfile.TemporaryDirectory(prefix="bpd-resume-") as temporary:
        tmp = Path(temporary)
        units = tmp / "units.jsonl"
        batch = tmp / "batch.jsonl"
        partial = tmp / "partial.md"
        strict = tmp / "strict.md"
        run(
            [
                sys.executable,
                str(script / "build_translation_units.py"),
                "tests/fixtures/academic-source.jsonl",
                "--out",
                str(units),
            ]
        )
        run(
            [
                sys.executable,
                str(script / "translation_cache.py"),
                "batch",
                "--units",
                str(units),
                "--out",
                str(batch),
                "--limit",
                "2",
            ]
        )
        batch_records = read_jsonl(batch)
        for unit in batch_records:
            unit["translation"] = translations[str(unit["source_sentence"])]
            unit["status"] = "translated"
        write_jsonl(batch, batch_records)
        run(
            [
                sys.executable,
                str(script / "translation_cache.py"),
                "merge",
                "--units",
                str(units),
                "--batch",
                str(batch),
            ]
        )
        run(
            [
                sys.executable,
                str(script / "render_bilingual_markdown.py"),
                "--units",
                str(units),
                "--out",
                str(strict),
            ],
            expect_failure=True,
        )
        run(
            [
                sys.executable,
                str(script / "render_bilingual_markdown.py"),
                "--units",
                str(units),
                "--out",
                str(partial),
                "--partial",
            ]
        )
        partial_text = partial.read_text(encoding="utf-8")
        if "Smith et al." in partial_text or "2.5 mg" not in partial_text:
            fail("partial renderer did not stop at the first incomplete paragraph")


def relative_files(root: Path) -> dict[Path, bytes]:
    files: dict[Path, bytes] = {}
    for path in root.rglob("*"):
        if not path.is_file() or ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        files[path.relative_to(root)] = path.read_bytes()
    return files


def smoke_installer() -> None:
    with tempfile.TemporaryDirectory(prefix="bpd-install-") as temporary:
        codex_home = Path(temporary) / "all"
        run([sys.executable, "scripts/install_skill.py", "--codex-home", str(codex_home), "--clean"])
        installed_root = codex_home / "skills"
        if sorted(path.name for path in installed_root.iterdir()) != sorted(SKILL_NAMES):
            fail("installer did not install the four standard skill entries")
        for name in SKILL_NAMES:
            if relative_files(installed_root / name) != relative_files(SKILLS_ROOT / name):
                fail(f"installed files differ from source skill: {name}")

        preserved = installed_root / "bilingual-paper-digest" / ".venv" / "preserved.txt"
        preserved.parent.mkdir()
        preserved.write_text("keep", encoding="utf-8")
        stale = installed_root / "bilingual-paper-digest" / "stale.txt"
        stale.write_text("remove", encoding="utf-8")
        run([sys.executable, "scripts/install_skill.py", "--codex-home", str(codex_home)])
        if not preserved.exists() or stale.exists():
            fail("installer update did not preserve .venv or remove stale files")

        single_home = Path(temporary) / "single"
        run(
            [
                sys.executable,
                "scripts/install_skill.py",
                "--codex-home",
                str(single_home),
                "--skill",
                "bilingual-paper-reader",
            ]
        )
        single_root = single_home / "skills"
        if [path.name for path in single_root.iterdir()] != ["bilingual-paper-reader"]:
            fail("single-skill installation installed unexpected entries")
        if not (single_root / "bilingual-paper-reader" / "scripts" / "check_digest.py").exists():
            fail("standalone paper reader lacks its validator")


def check_examples() -> None:
    run(
        [
            sys.executable,
            str(ROOT_SKILL / "scripts" / "check_digest.py"),
            "examples/minimal-paper-note.md",
            "examples/obsidian-material-note.md",
        ]
    )
    run(
        [
            sys.executable,
            str(ROOT_SKILL / "scripts" / "check_knowledge_cards.py"),
            "--strict",
            "examples/knowledge-card-term.md",
            "examples/knowledge-card-statistics.md",
        ]
    )


def check_lightweight() -> None:
    total = sum(len(content) for name in SKILL_NAMES for content in relative_files(SKILLS_ROOT / name).values())
    print(f"Self-contained suite size: {total} bytes")
    if total > 600_000:
        fail("installed four-skill suite exceeds the 600 KB lightweight budget")


def main() -> int:
    check_skill_structure()
    check_references()
    check_generated_skills()
    check_python()
    check_sentence_boundaries()
    check_requirements()
    check_eval_scenarios()
    check_examples()
    smoke_golden_pipeline()
    smoke_batch_resume()
    smoke_real_pdf_extraction()
    smoke_installer()
    check_lightweight()
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
