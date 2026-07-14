#!/usr/bin/env python3
"""Render translated JSONL units into source-faithful bilingual Markdown."""

from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path


SKIP_STATUSES = {"skip", "skipped", "omit", "omitted"}
STRUCTURAL_TYPES = {"heading", "structural"}


def read_units(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
    return records


def group_paragraphs(units: list[dict[str, object]]) -> list[list[dict[str, object]]]:
    groups: OrderedDict[str, list[dict[str, object]]] = OrderedDict()
    for index, unit in enumerate(units, start=1):
        key = str(unit.get("paragraph_id") or unit.get("source_unit_id") or f"unit-{index}")
        groups.setdefault(key, []).append(unit)
    return list(groups.values())


def is_structural(unit: dict[str, object]) -> bool:
    return str(unit.get("unit_type", "")).lower() in STRUCTURAL_TYPES or str(
        unit.get("status", "")
    ).lower() == "structural"


def is_skipped(unit: dict[str, object]) -> bool:
    return str(unit.get("status", "")).lower() in SKIP_STATUSES


def pending_units(group: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        unit
        for unit in group
        if not is_structural(unit)
        and not is_skipped(unit)
        and not str(unit.get("translation", "")).strip()
    ]


def render_group(group: list[dict[str, object]]) -> str:
    lines: list[str] = []
    for unit in group:
        if is_skipped(unit):
            continue
        source = str(unit.get("source_sentence", "")).strip()
        if not source:
            continue
        if is_structural(unit):
            lines.append(source)
            continue
        translation = str(unit.get("translation", "")).strip()
        if not translation:
            raise ValueError(f"pending unit reached renderer: {unit.get('translation_unit_id')}")
        lines.extend((source, "\t" + translation))
    return "\n".join(lines)


def render(
    units: list[dict[str, object]], header: str, partial: bool
) -> tuple[str, int, int, list[dict[str, object]]]:
    groups = group_paragraphs(units)
    first_incomplete = len(groups)
    pending: list[dict[str, object]] = []
    for index, group in enumerate(groups):
        group_pending = pending_units(group)
        if group_pending:
            first_incomplete = index
            pending = group_pending
            break

    if pending and not partial:
        return "", 0, len(groups), pending

    selected = groups[:first_incomplete] if pending else groups
    if pending:
        while selected and all(is_structural(unit) or is_skipped(unit) for unit in selected[-1]):
            selected.pop()

    blocks = [render_group(group) for group in selected]
    blocks = [block for block in blocks if block]
    if header.strip():
        blocks.insert(0, header.strip())
    markdown = "\n\n\n".join(blocks).rstrip() + "\n" if blocks else ""
    return markdown, len(selected), len(groups), pending


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--units", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--header", type=Path, help="Optional Markdown metadata/header file.")
    parser.add_argument(
        "--partial",
        action="store_true",
        help="Render only the fully translated paragraph prefix and stop before the first pending paragraph.",
    )
    args = parser.parse_args()

    units = read_units(args.units)
    header = args.header.read_text(encoding="utf-8") if args.header else ""
    markdown, rendered, total, pending = render(units, header, args.partial)
    if pending and not args.partial:
        print(
            f"Refusing to render: first incomplete paragraph has {len(pending)} pending unit(s).",
            file=sys.stderr,
        )
        for unit in pending[:10]:
            print(
                f"  - {unit.get('translation_unit_id')}: "
                f"{str(unit.get('source_sentence', ''))[:180]}",
                file=sys.stderr,
            )
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(markdown, encoding="utf-8")
    print(f"Wrote {args.out}")
    print(f"Rendered paragraphs: {rendered}/{total}")
    if pending:
        print(f"Stopped before {len(pending)} pending unit(s) in the next paragraph.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
