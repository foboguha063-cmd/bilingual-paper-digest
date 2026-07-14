#!/usr/bin/env python3
"""Extract PDF text into reusable JSONL source blocks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def parse_pages(value: str | None) -> set[int] | None:
    if not value:
        return None
    pages: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            start_page, end_page = int(start), int(end)
            if start_page < 1 or end_page < start_page:
                raise ValueError(f"invalid page range: {part}")
            pages.update(range(start_page, end_page + 1))
        else:
            page = int(part)
            if page < 1:
                raise ValueError(f"invalid page number: {part}")
            pages.add(page)
    return pages


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_blocks(text: str) -> list[str]:
    text = clean_text(text)
    if not text:
        return []
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    if len(blocks) <= 1:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if len(lines) > 1:
            return [" ".join(lines)]
    return blocks


def safe_metadata(raw: object) -> dict[str, object]:
    if not raw:
        return {}
    try:
        items = dict(raw).items()
    except (TypeError, ValueError):
        return {}
    metadata: dict[str, object] = {}
    for key, value in items:
        normalized_key = str(key).lstrip("/")
        if value is None or isinstance(value, (str, int, float, bool)):
            metadata[normalized_key] = value
        else:
            metadata[normalized_key] = str(value)
    return metadata


def detect_doi(records: list[dict[str, object]]) -> str | None:
    prefix = "\n".join(str(record.get("text", "")) for record in records[:20])[:30000]
    match = re.search(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", prefix, flags=re.IGNORECASE)
    return match.group(0).rstrip(".,;)") if match else None


def stable_id(source: Path, page: int, block_index: int, text: str) -> str:
    digest = hashlib.sha1(f"{source}:{page}:{block_index}:{text}".encode("utf-8")).hexdigest()[:12]
    return f"p{page:04d}_b{block_index:03d}_{digest}"


def extract_with_pdfplumber(pdf: Path, pages: set[int] | None) -> tuple[list[dict[str, object]], dict[str, object]]:
    import pdfplumber

    records: list[dict[str, object]] = []
    with pdfplumber.open(str(pdf)) as document:
        page_count = len(document.pages)
        document_metadata = safe_metadata(document.metadata)
        for zero_index, page in enumerate(document.pages):
            page_number = zero_index + 1
            if pages and page_number not in pages:
                continue
            text = page.extract_text(x_tolerance=1, y_tolerance=3) or ""
            for block_index, block in enumerate(split_blocks(text), start=1):
                records.append(
                    {
                        "unit_id": stable_id(pdf, page_number, block_index, block),
                        "source_file": str(pdf),
                        "page": page_number,
                        "block_index": block_index,
                        "kind": "text_block",
                        "method": "pdfplumber",
                        "text": block,
                    }
                )
    return records, {
        "page_count": page_count,
        "method": "pdfplumber",
        "document_metadata": document_metadata,
    }


def extract_with_pypdf(pdf: Path, pages: set[int] | None) -> tuple[list[dict[str, object]], dict[str, object]]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf))
    records: list[dict[str, object]] = []
    for zero_index, page in enumerate(reader.pages):
        page_number = zero_index + 1
        if pages and page_number not in pages:
            continue
        text = page.extract_text() or ""
        for block_index, block in enumerate(split_blocks(text), start=1):
            records.append(
                {
                    "unit_id": stable_id(pdf, page_number, block_index, block),
                    "source_file": str(pdf),
                    "page": page_number,
                    "block_index": block_index,
                    "kind": "text_block",
                    "method": "pypdf",
                    "text": block,
                }
            )
    return records, {
        "page_count": len(reader.pages),
        "method": "pypdf",
        "document_metadata": safe_metadata(reader.metadata),
    }


def extract_with_pymupdf4llm(pdf: Path, pages: set[int] | None) -> tuple[list[dict[str, object]], dict[str, object]]:
    import pymupdf4llm

    kwargs: dict[str, object] = {}
    if pages:
        kwargs["pages"] = [page - 1 for page in sorted(pages)]
    kwargs["page_chunks"] = True
    chunks = pymupdf4llm.to_markdown(str(pdf), **kwargs)
    records: list[dict[str, object]] = []
    page_count = None
    document_metadata: dict[str, object] = {}
    for chunk in chunks:
        metadata = dict(chunk.get("metadata", {}))
        if not document_metadata:
            document_metadata = safe_metadata(metadata)
        page_number = metadata.get("page_number")
        page_count = metadata.get("page_count", page_count)
        markdown = str(chunk.get("text", ""))
        for block_index, block in enumerate(split_blocks(markdown), start=1):
            records.append(
                {
                    "unit_id": stable_id(pdf, int(page_number or 0), block_index, block),
                    "source_file": str(pdf),
                    "page": page_number,
                    "block_index": block_index,
                    "kind": "markdown_block",
                    "method": "pymupdf4llm",
                    "text": block,
                }
            )
    return records, {
        "page_count": page_count,
        "method": "pymupdf4llm",
        "document_metadata": document_metadata,
    }


def extract_with_docling(pdf: Path, pages: set[int] | None) -> tuple[list[dict[str, object]], dict[str, object]]:
    if pages:
        raise ValueError("Docling mode does not support --pages; use a light extractor for page ranges")
    from docling.document_converter import DocumentConverter

    result = DocumentConverter().convert(str(pdf))
    markdown = result.document.export_to_markdown()
    records = [
        {
            "unit_id": stable_id(pdf, 0, block_index, block),
            "source_file": str(pdf),
            "page": None,
            "block_index": block_index,
            "kind": "markdown_block",
            "method": "docling",
            "text": block,
        }
        for block_index, block in enumerate(split_blocks(markdown), start=1)
    ]
    return records, {"page_count": None, "method": "docling", "document_metadata": {}}


def choose_method(method: str) -> list[str]:
    if method != "auto":
        return [method]
    return ["pymupdf4llm", "pdfplumber", "pypdf", "docling"]


def write_jsonl(path: Path, records: Iterable[dict[str, object]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out-dir", type=Path, default=None, help="Default: PDF parent/.bilingual-paper-digest")
    parser.add_argument(
        "--method",
        choices=["auto", "pymupdf4llm", "pdfplumber", "pypdf", "docling"],
        default="auto",
    )
    parser.add_argument("--pages", help="Page range like 1-5,8,10.")
    parser.add_argument("--book", action="store_true", help="Mark extraction as book-mode input.")
    args = parser.parse_args()

    pdf = args.pdf.expanduser().resolve()
    if not pdf.exists():
        print(f"PDF not found: {pdf}", file=sys.stderr)
        return 2

    out_dir = args.out_dir or (pdf.parent / ".bilingual-paper-digest")
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        pages = parse_pages(args.pages)
    except ValueError as exc:
        parser.error(str(exc))

    errors: list[str] = []
    records: list[dict[str, object]] = []
    metadata: dict[str, object] = {}

    for method in choose_method(args.method):
        try:
            if method == "pymupdf4llm":
                records, metadata = extract_with_pymupdf4llm(pdf, pages)
            elif method == "pdfplumber":
                records, metadata = extract_with_pdfplumber(pdf, pages)
            elif method == "pypdf":
                records, metadata = extract_with_pypdf(pdf, pages)
            elif method == "docling":
                records, metadata = extract_with_docling(pdf, pages)
            if records:
                break
            errors.append(f"{method}: extracted no text")
        except Exception as exc:
            errors.append(f"{method}: {type(exc).__name__}: {exc}")

    if not records:
        manifest_path = out_dir / "source_map.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "source_file": str(pdf),
                    "status": "extraction_failed",
                    "selected_pages": sorted(pages) if pages else None,
                    "warnings": errors,
                    "recommended_action": "Run OCRmyPDF/Tesseract when the PDF is scanned, then retry.",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print("No text extracted. Try OCRmyPDF/Tesseract for scanned PDFs.", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    source_jsonl = out_dir / "source.jsonl"
    count = write_jsonl(source_jsonl, records)
    char_count = sum(len(str(record.get("text", ""))) for record in records)
    extracted_pages = {record.get("page") for record in records if record.get("page") is not None}
    average_chars = char_count / max(1, len(extracted_pages))

    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_file": str(pdf),
        "source_jsonl": str(source_jsonl),
        "method": metadata.get("method"),
        "page_count": metadata.get("page_count"),
        "selected_pages": sorted(pages) if pages else None,
        "book_mode": bool(args.book),
        "block_count": count,
        "char_count": char_count,
        "average_chars_per_extracted_page": round(average_chars, 1),
        "likely_scanned_or_incomplete": average_chars < 80,
        "detected_doi": detect_doi(records),
        "document_metadata": metadata.get("document_metadata", {}),
        "warnings": errors,
    }
    manifest_path = out_dir / "source_map.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote {source_jsonl}")
    print(f"Wrote {manifest_path}")
    print(f"Blocks: {count}; chars: {char_count}; method: {manifest['method']}")
    if errors:
        print("Fallback notes:")
        for error in errors:
            print(f"  - {error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
