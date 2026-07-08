#!/usr/bin/env python3
"""Check that translated Markdown retains source sentences from translation units."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SKIP_STATUSES = {"skipped", "omit", "omitted"}


def normalize_text(value: str) -> str:
    value = value.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
    value = re.sub(r"\s+", " ", value.strip())
    return value


def compact_text(value: str) -> str:
    value = normalize_text(value).lower()
    value = re.sub(r"[^\w\u4e00-\u9fff]+", "", value)
    return value


def read_units(path: Path, statuses: set[str] | None) -> list[dict[str, object]]:
    units: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                unit = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
            status = str(unit.get("status", "")).strip()
            if status in SKIP_STATUSES:
                continue
            if statuses and status not in statuses:
                continue
            source = str(unit.get("source_sentence", "")).strip()
            if source:
                units.append(unit)
    return units


def markdown_english_lines(path: Path) -> list[str]:
    lines: list[str] = []
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        if re.match(r"^[-*]\s+", stripped) and re.search(r"[A-Za-z]", stripped):
            lines.append(re.sub(r"^[-*]\s+", "", stripped))
            continue
        if line.startswith(("\t", " ", "#", "|", ">")):
            continue
        if re.search(r"[A-Za-z]", stripped):
            lines.append(stripped)
    return lines


def is_present(source: str, english_blob: str, compact_blob: str) -> bool:
    normalized = normalize_text(source)
    if normalized in english_blob:
        return True
    compact = compact_text(source)
    if len(compact) >= 24 and compact in compact_blob:
        return True
    return False


def check(units_path: Path, markdown_path: Path, statuses: set[str] | None, max_report: int) -> int:
    units = read_units(units_path, statuses)
    english_lines = markdown_english_lines(markdown_path)
    english_blob = "\n".join(normalize_text(line) for line in english_lines)
    compact_blob = compact_text(english_blob)

    missing: list[dict[str, object]] = []
    duplicated: list[str] = []
    seen_sources: dict[str, int] = {}

    for unit in units:
        source = str(unit.get("source_sentence", "")).strip()
        key = compact_text(source)
        seen_sources[key] = seen_sources.get(key, 0) + 1
        if not is_present(source, english_blob, compact_blob):
            missing.append(unit)

    for key, count in seen_sources.items():
        if key and count > 1:
            duplicated.append(key)

    print(f"Units checked: {len(units)}")
    print(f"English lines in Markdown: {len(english_lines)}")
    print(f"Missing source sentences: {len(missing)}")
    print(f"Duplicate source units: {len(duplicated)}")

    if missing:
        print("\nMissing examples:", file=sys.stderr)
        for unit in missing[:max_report]:
            unit_id = unit.get("translation_unit_id")
            page = unit.get("page")
            source = str(unit.get("source_sentence", ""))
            print(f"  - {unit_id} page={page}: {source[:240]}", file=sys.stderr)

    if missing:
        return 1
    return 0


def parse_statuses(value: str | None) -> set[str] | None:
    if not value:
        return None
    return {part.strip() for part in value.split(",") if part.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--units", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument(
        "--statuses",
        default=None,
        help="Optional comma-separated statuses to check, e.g. checked,translated.",
    )
    parser.add_argument("--max-report", type=int, default=20)
    args = parser.parse_args()

    return check(args.units, args.markdown, parse_statuses(args.statuses), args.max_report)


if __name__ == "__main__":
    raise SystemExit(main())
