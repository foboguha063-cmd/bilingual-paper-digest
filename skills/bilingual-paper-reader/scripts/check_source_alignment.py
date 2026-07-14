#!/usr/bin/env python3
"""Check that translated Markdown retains source sentences from translation units."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path


SKIP_STATUSES = {"skip", "skipped", "omit", "omitted", "structural"}


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
            unit_type = str(unit.get("unit_type", "")).strip().lower()
            if status in SKIP_STATUSES or unit_type in {"heading", "structural"}:
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


def check(units_path: Path, markdown_path: Path, statuses: set[str] | None, max_report: int) -> int:
    units = read_units(units_path, statuses)
    english_lines = markdown_english_lines(markdown_path)
    missing: list[dict[str, object]] = []
    expected_keys = [compact_text(str(unit.get("source_sentence", ""))) for unit in units]
    observed_keys = [compact_text(line) for line in english_lines]
    expected_counts = Counter(expected_keys)
    observed_counts = Counter(observed_keys)
    positions: dict[str, deque[int]] = defaultdict(deque)
    for index, key in enumerate(observed_keys):
        if key:
            positions[key].append(index)

    matched_positions: list[int] = []
    matched_units: list[dict[str, object]] = []
    for unit, key in zip(units, expected_keys):
        if key and positions[key]:
            matched_positions.append(positions[key].popleft())
            matched_units.append(unit)
        else:
            missing.append(unit)

    duplicated = sorted(
        key
        for key, expected_count in expected_counts.items()
        if key and observed_counts[key] > expected_count
    )
    order_errors: list[tuple[dict[str, object], int, int]] = []
    previous = -1
    for unit, position in zip(matched_units, matched_positions):
        if position < previous:
            order_errors.append((unit, previous, position))
        previous = max(previous, position)

    print(f"Units checked: {len(units)}")
    print(f"English lines in Markdown: {len(english_lines)}")
    print(f"Missing source sentences: {len(missing)}")
    print(f"Duplicated rendered source sentences: {len(duplicated)}")
    print(f"Source-order errors: {len(order_errors)}")

    if missing:
        print("\nMissing examples:", file=sys.stderr)
        for unit in missing[:max_report]:
            unit_id = unit.get("translation_unit_id")
            page = unit.get("page")
            source = str(unit.get("source_sentence", ""))
            print(f"  - {unit_id} page={page}: {source[:240]}", file=sys.stderr)

    if duplicated:
        print("\nDuplicated rendered examples:", file=sys.stderr)
        for key in duplicated[:max_report]:
            print(
                f"  - expected={expected_counts[key]} rendered={observed_counts[key]}: {key[:180]}",
                file=sys.stderr,
            )

    if order_errors:
        print("\nOut-of-order examples:", file=sys.stderr)
        for unit, previous_position, position in order_errors[:max_report]:
            print(
                f"  - {unit.get('translation_unit_id')}: rendered position {position} "
                f"after {previous_position}",
                file=sys.stderr,
            )

    if missing or duplicated or order_errors:
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
