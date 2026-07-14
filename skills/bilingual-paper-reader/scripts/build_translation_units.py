#!/usr/bin/env python3
"""Build resumable sentence-level translation units from source.jsonl."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


PROTECTED_PERIOD = "\ue000"
SENTENCE_BOUNDARY = re.compile(
    r"(?P<end>[.!?。！？](?:[\"'”’)\]]|\s*\[(?:\d[\d,;\s–—-]*)\])*)"
    r"\s+(?=(?:[\"'“‘(]|\w|[\u4e00-\u9fff]))"
)
ABBREVIATION = re.compile(
    r"\b(?:e\.g|i\.e|Fig|Figs|Eq|Eqs|Ref|Refs|Dr|Prof|Mr|Mrs|Ms|"
    r"vs|cf|approx|resp|No|Nos|Vol|pp|p)\.",
    flags=re.IGNORECASE,
)
INITIAL = re.compile(r"\b([A-Z])\.(?=\s+[A-Z][A-Za-z-]+)")
ET_AL = re.compile(r"\b(?:et|Et)\s+al\.(?=\s+(?:[a-z0-9(\[]))")
INITIALISM = re.compile(r"\b(?:[A-Za-z]\.){2,}(?=\s+(?:[a-z0-9(\[]))")
MARKDOWN_HEADING = re.compile(r"^#{1,6}\s+\S")


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []

    if PROTECTED_PERIOD in text:
        raise ValueError("source text contains the reserved sentence-splitting marker")

    protected = re.sub(r"(?<=\d)\.(?=\d)", PROTECTED_PERIOD, text)
    protected = ABBREVIATION.sub(
        lambda match: match.group(0).replace(".", PROTECTED_PERIOD), protected
    )
    protected = ET_AL.sub(lambda match: match.group(0).replace(".", PROTECTED_PERIOD), protected)
    protected = INITIALISM.sub(lambda match: match.group(0).replace(".", PROTECTED_PERIOD), protected)
    protected = INITIAL.sub(lambda match: match.group(0).replace(".", PROTECTED_PERIOD), protected)
    marked = SENTENCE_BOUNDARY.sub(lambda match: match.group("end") + "\n", protected)
    parts = [part.replace(PROTECTED_PERIOD, ".").strip() for part in marked.splitlines() if part.strip()]
    return parts or [text]


def unit_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_jsonl", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    source_jsonl = args.source_jsonl.expanduser().resolve()
    out = args.out or (source_jsonl.parent / "translation_units.jsonl")

    count = 0
    paragraph_index = 0
    with source_jsonl.open("r", encoding="utf-8") as src, out.open("w", encoding="utf-8") as dst:
        for line in src:
            if not line.strip():
                continue
            record = json.loads(line)
            text = str(record.get("text", ""))
            paragraph_index += 1
            paragraph_id = str(record.get("paragraph_id") or record["unit_id"])
            is_heading = bool(MARKDOWN_HEADING.fullmatch(re.sub(r"\s+", " ", text.strip())))
            sentences = [re.sub(r"\s+", " ", text.strip())] if is_heading else split_sentences(text)
            sentence_count = len(sentences)
            for sentence_index, sentence in enumerate(sentences, start=1):
                unit = {
                    "translation_unit_id": f"{record['unit_id']}_s{sentence_index:03d}",
                    "source_unit_id": record["unit_id"],
                    "paragraph_id": paragraph_id,
                    "paragraph_index": paragraph_index,
                    "source_hash": unit_hash(sentence),
                    "source_file": record.get("source_file"),
                    "page": record.get("page"),
                    "block_index": record.get("block_index"),
                    "sentence_index": sentence_index,
                    "sentence_count": sentence_count,
                    "unit_type": "heading" if is_heading else "sentence",
                    "source_sentence": sentence,
                    "translation": "",
                    "status": "structural" if is_heading else "pending",
                }
                dst.write(json.dumps(unit, ensure_ascii=False) + "\n")
                count += 1

    print(f"Wrote {out}")
    print(f"Translation units: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
