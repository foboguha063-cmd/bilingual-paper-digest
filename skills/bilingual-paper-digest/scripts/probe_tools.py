#!/usr/bin/env python3
"""Probe optional tools for bilingual-paper-digest workflows."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import socket
import sys
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path


PYTHON_MODULES = [
    ("pdfplumber", "baseline PDF text extraction"),
    ("pypdf", "baseline PDF metadata/page extraction"),
    ("fitz", "PyMuPDF fast PDF extraction"),
    ("pymupdf4llm", "layout-aware PDF-to-Markdown extraction"),
    ("docling", "document/book conversion"),
]

BINARIES = [
    ("pdfinfo", "PDF metadata and page count"),
    ("pdftotext", "Poppler text extraction"),
    ("tesseract", "OCR engine"),
    ("ocrmypdf", "OCR scanned PDFs into searchable PDFs"),
    ("java", "required by GROBID server/client workflows"),
]


@dataclass
class ProbeItem:
    name: str
    ok: bool
    kind: str
    detail: str
    path: str | None = None


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def localhost_open(port: int, timeout: float = 0.25) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def grobid_alive(url: str) -> bool:
    try:
        with urllib.request.urlopen(url.rstrip("/") + "/api/isalive", timeout=1.5) as response:
            return response.status == 200 and b"true" in response.read().lower()
    except Exception:
        return False


def probe(grobid_url: str | None) -> dict[str, object]:
    items: list[ProbeItem] = []

    for module, detail in PYTHON_MODULES:
        items.append(ProbeItem(name=module, ok=module_available(module), kind="python", detail=detail))

    for binary, detail in BINARIES:
        path = shutil.which(binary)
        items.append(ProbeItem(name=binary, ok=path is not None, kind="binary", detail=detail, path=path))

    grobid_url = grobid_url or "http://localhost:8070"
    grobid_ok = grobid_alive(grobid_url) if localhost_open(8070) else False
    items.append(ProbeItem(name="grobid", ok=grobid_ok, kind="service", detail=f"GROBID service at {grobid_url}"))

    ok_names = {item.name for item in items if item.ok}
    capabilities = {
        "baseline_pdf": {"ok": {"pdfplumber", "pypdf"} <= ok_names, "needs": ["pdfplumber", "pypdf"]},
        "layout_pdf": {"ok": "pymupdf4llm" in ok_names or "docling" in ok_names, "needs": ["pymupdf4llm or docling"]},
        "scanned_pdf": {"ok": {"tesseract", "ocrmypdf"} <= ok_names, "needs": ["tesseract", "ocrmypdf"]},
        "scholarly_metadata": {"ok": "grobid" in ok_names, "needs": ["running GROBID service"]},
        "book_mode": {"ok": "docling" in ok_names or "pymupdf4llm" in ok_names, "needs": ["docling or pymupdf4llm"]},
    }

    recommendations: list[str] = []
    if not capabilities["baseline_pdf"]["ok"]:
        recommendations.append("Run scripts/setup_environment.py --profile light to install baseline Python dependencies.")
    if not capabilities["layout_pdf"]["ok"]:
        recommendations.append("Install the light profile for pymupdf4llm, or the docling profile for complex books.")
    if not capabilities["scanned_pdf"]["ok"]:
        recommendations.append("For scanned PDFs, install OCRmyPDF and Tesseract with the system package manager.")
    if not capabilities["scholarly_metadata"]["ok"]:
        recommendations.append("For high-quality article metadata, run a GROBID service and set GROBID_URL.")

    return {
        "python": sys.executable,
        "cwd": str(Path.cwd()),
        "items": [asdict(item) for item in items],
        "capabilities": capabilities,
        "recommendations": recommendations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--grobid-url", default=None, help="GROBID service URL, default http://localhost:8070.")
    args = parser.parse_args()

    result = probe(args.grobid_url)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"Python: {result['python']}")
    print("\nTools:")
    for item in result["items"]:
        mark = "OK" if item["ok"] else "--"
        location = f" ({item['path']})" if item.get("path") else ""
        print(f"  {mark} {item['kind']}: {item['name']} - {item['detail']}{location}")

    print("\nCapabilities:")
    for name, value in result["capabilities"].items():
        mark = "OK" if value["ok"] else "--"
        print(f"  {mark} {name} needs {', '.join(value['needs'])}")

    if result["recommendations"]:
        print("\nRecommendations:")
        for recommendation in result["recommendations"]:
            print(f"  - {recommendation}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
