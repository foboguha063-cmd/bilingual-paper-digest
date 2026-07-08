# PDF Extraction Pipeline

Use this reference before processing PDFs with complex layouts, scanned pages, books, or repeated/batch work.

## Tool Routing

Choose the lightest reliable route:

1. **Ordinary selectable research PDF**
   Use `scripts/extract_pdf_structure.py <paper.pdf>`. It tries PyMuPDF4LLM when available, then falls back to pdfplumber and pypdf.

2. **Two-column or layout-heavy PDF**
   Prefer the light profile with PyMuPDF4LLM. Inspect the extracted `source.jsonl` before translating if column order is uncertain.

3. **Scanned PDF**
   Run OCR first with OCRmyPDF/Tesseract outside the skill, then process the OCR output PDF with `extract_pdf_structure.py`.

4. **Scholarly metadata-heavy paper**
   Use GROBID when available for title, authors, affiliations, DOI, abstract, references, and TEI structure. Do not require GROBID for ordinary text extraction.

5. **Book, dissertation, report, or long chaptered PDF**
   Read `references/book-translation-mode.md`, then extract with `extract_pdf_structure.py --book`.

## Default Commands

Probe the machine:

```bash
python3 scripts/probe_tools.py
```

Extract a paper:

```bash
python3 scripts/extract_pdf_structure.py paper.pdf
python3 scripts/build_translation_units.py .bilingual-paper-digest/source.jsonl
```

Extract selected pages:

```bash
python3 scripts/extract_pdf_structure.py paper.pdf --pages 1-8,12
```

Extract book-like input:

```bash
python3 scripts/extract_pdf_structure.py book.pdf --book
python3 scripts/build_translation_units.py .bilingual-paper-digest/source.jsonl
```

## Output Contract

`source.jsonl` contains reusable text blocks:

```json
{
  "unit_id": "p0001_b001_...",
  "source_file": ".../paper.pdf",
  "page": 1,
  "block_index": 1,
  "kind": "text_block",
  "method": "pdfplumber",
  "text": "..."
}
```

`translation_units.jsonl` contains sentence-like units:

```json
{
  "translation_unit_id": "p0001_b001_..._s001",
  "source_hash": "...",
  "page": 1,
  "source_sentence": "...",
  "translation": "",
  "status": "pending"
}
```

Translate from the structured units when accuracy, resumability, or token efficiency matters.

## Accuracy Rules

- Always inspect extraction quality before translating a long or complex PDF.
- If columns are interleaved, do not translate directly from the broken extraction; switch extractor or inspect rendered pages.
- If scanned text is empty or garbled, OCR first.
- If a page has tables, formulas, or figure captions mixed into the body, remove only the unwanted table/figure material requested by the main skill rules.
- Keep `source_map.json` with the final note when traceability matters.

## Token Efficiency

- Extract once, reuse `source.jsonl`.
- Translate only pending `translation_units.jsonl` units.
- Cache translations by `source_hash`.
- Inject only matched terms from the current block, not the entire knowledge base.
- Use stable prompt prefixes for prompt caching when calling an API.
