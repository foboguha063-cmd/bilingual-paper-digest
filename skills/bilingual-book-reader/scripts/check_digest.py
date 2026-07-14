#!/usr/bin/env python3
"""Check bilingual-paper-digest Markdown notes for the trained format."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


BAD_HEADINGS = {
    "glossary",
    "references",
    "reference",
    "acknowledgements",
    "acknowledgments",
}

ADDED_SUMMARY_HEADING_PATTERNS = (
    r"^#+\s*(中文)?(总结|概要|概述|主要内容|核心观点|核心发现|机制总结|临床意义)\s*$",
    r"^#+\s*(key\s+takeaways?|takeaways?|main\s+points?|key\s+points?|brief\s+summary)\s*$",
)

SUMMARY_META_PATTERNS = (
    r"^\t?(本节|该段|这一段|这一节|该部分)(主要|总体|简要)?(说明|介绍|讨论|总结|概述)",
    r"^\t?以下(是|为).*(总结|概述|要点|翻译)",
    r"^\t?(this\s+section|this\s+paragraph)\s+(mainly\s+)?(summarizes|discusses|describes)",
    r"^\t?the\s+following\s+(is|are).*(summary|takeaways?)",
)


def is_heading(line: str) -> bool:
    return bool(re.match(r"^#{1,6}\s+\S", line))


def is_image(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("![") or stripped.startswith("![[")


def looks_like_added_summary_heading(line: str) -> bool:
    stripped = line.strip()
    lower = stripped.lower()
    return any(re.search(pattern, lower, flags=re.IGNORECASE) for pattern in ADDED_SUMMARY_HEADING_PATTERNS)


def looks_like_summary_meta_line(line: str) -> bool:
    stripped = line.strip()
    return any(re.search(pattern, stripped, flags=re.IGNORECASE) for pattern in SUMMARY_META_PATTERNS)


def is_structural(line: str, allow_images: bool) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if is_heading(stripped):
        return True
    if stripped.startswith("|"):
        return True
    if stripped.startswith("```"):
        return True
    if allow_images and is_image(stripped):
        return True
    return False


def looks_like_chinese_translation(line: str) -> bool:
    return line.startswith("\t")


def looks_like_english_source(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if line.startswith((" ", "\t")):
        return False
    if is_heading(stripped):
        return False
    if stripped.startswith(("**团队**", "DOI", "Published", "Received", "Revised", "Accepted")):
        return False
    return bool(re.search(r"[A-Za-z]", stripped))


def check(path: Path, allow_images: bool) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    first_heading_index = next((i for i, line in enumerate(lines) if is_heading(line.strip())), len(lines))

    if any("题录简介" in line for line in lines):
        errors.append("contains forbidden heading/text: 题录简介")

    if not any(line.startswith("**团队**：") for line in lines[:40]):
        errors.append("missing team line near top: **团队**：")

    if not any(line.startswith(("DOI：", "DOI:")) for line in lines[:50]):
        errors.append("missing DOI line near top")

    in_fence = False
    last_conclusion = -1
    first_box = -1

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        lower = stripped.lower().strip("# ")

        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if is_heading(stripped):
            normalized = re.sub(r"[^a-z]", "", lower)
            if normalized in BAD_HEADINGS:
                errors.append(f"line {idx}: forbidden heading '{stripped}'")
            if looks_like_added_summary_heading(stripped):
                errors.append(f"line {idx}: added summary/analysis heading is not allowed: '{stripped}'")
            if "conclusion" in lower or "conclusions" in lower:
                last_conclusion = idx
            if lower.startswith("box"):
                first_box = first_box if first_box != -1 else idx

        if is_image(stripped) and not allow_images:
            errors.append(f"line {idx}: image/embed syntax is not allowed in text-only mode")

        if looks_like_summary_meta_line(line):
            errors.append(f"line {idx}: possible summary/paraphrase metacommentary; translate the source sentence directly")

    if first_box != -1 and last_conclusion != -1 and first_box < last_conclusion:
        errors.append("Box section appears before Conclusions")

    for i, line in enumerate(lines):
        if i < first_heading_index:
            continue
        idx = i + 1
        if not looks_like_english_source(line):
            continue

        j = i + 1
        if j >= len(lines):
            errors.append(f"line {idx}: English source line has no following Chinese translation")
            continue

        if lines[j].strip() == "":
            errors.append(f"line {idx}: blank line between English sentence and Chinese translation")
            continue

        if not looks_like_chinese_translation(lines[j]):
            errors.append(f"line {idx}: next line is not tab-indented Chinese translation")

    for i, line in enumerate(lines[:-1]):
        if i < first_heading_index:
            continue
        if line.strip() != "":
            continue
        prev = lines[i - 1] if i > 0 else ""
        next_line = lines[i + 1]
        if prev.startswith("\t") and looks_like_english_source(next_line):
            before_blank = i - 2 >= 0 and lines[i - 1].strip() == ""
            after_blank = i + 2 < len(lines) and lines[i + 2].strip() == ""
            if not before_blank and not after_blank:
                errors.append(
                    f"line {i + 1}: only one blank line between source paragraphs; use at least two"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path, nargs="+")
    parser.add_argument(
        "--allow-images",
        action="store_true",
        help="Allow Obsidian image/media embeds for figure-enabled notes.",
    )
    args = parser.parse_args()

    failed = False
    for path in args.markdown:
        errors = check(path, args.allow_images)
        if errors:
            failed = True
            print(f"{path}: FAIL", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print(f"{path}: OK")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
