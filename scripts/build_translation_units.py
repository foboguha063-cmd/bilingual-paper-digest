#!/usr/bin/env python3
"""Build sentence-level translation units from source.jsonl."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


SENTENCE_END = re.compile(r"(?<=[.!?。！？])\s+(?=[A-Z0-9(])")


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    if len(text) < 320:
        return [text]
    parts = [part.strip() for part in SENTENCE_END.split(text) if part.strip()]
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
    with source_jsonl.open("r", encoding="utf-8") as src, out.open("w", encoding="utf-8") as dst:
        for line in src:
            if not line.strip():
                continue
            record = json.loads(line)
            text = str(record.get("text", ""))
            for sentence_index, sentence in enumerate(split_sentences(text), start=1):
                unit = {
                    "translation_unit_id": f"{record['unit_id']}_s{sentence_index:03d}",
                    "source_unit_id": record["unit_id"],
                    "source_hash": unit_hash(sentence),
                    "source_file": record.get("source_file"),
                    "page": record.get("page"),
                    "block_index": record.get("block_index"),
                    "sentence_index": sentence_index,
                    "source_sentence": sentence,
                    "translation": "",
                    "status": "pending",
                }
                dst.write(json.dumps(unit, ensure_ascii=False) + "\n")
                count += 1

    print(f"Wrote {out}")
    print(f"Translation units: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
