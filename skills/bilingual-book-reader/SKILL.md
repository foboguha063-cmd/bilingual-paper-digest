---
name: bilingual-book-reader
description: Translate book-length academic documents into resumable, source-aligned English-Chinese Markdown organized by chapter. Use for PDF books, monographs, textbooks, theses, dissertations, standards, long reports, selected chapters, or page ranges when the user asks for 翻译PDF书, 整理这本书, 翻译章节, 书籍双语阅读, chapter translation, book translation, or continuation of interrupted work. Preserve headings, paragraphs, notes, citations, numbering, scope, and progress; never replace unfinished source text with a summary.
---

# Bilingual Book Reader

Use this folder as a self-contained runtime. Keep long work resumable and chapter-scoped.

## Workflow

1. Read `references/bilingual-output-contract.md` and `references/book-translation-mode.md`.
2. Read `references/pdf-extraction-pipeline.md` before extracting a PDF and `references/translation-memory.md` before translating or resuming long units.
3. Confirm the requested book, chapter, section, or page range. Do not expand the scope silently.
4. Build or reuse structured source and translation units, then translate only pending units chapter by chapter while preserving headings, paragraph order, notes, citations, and numbered structure.
5. Reuse a checked translation only when its source hash matches. Export bounded pending batches, merge them by ID/hash, and render only complete paragraphs. Never fill an unfinished chapter with a summary.
6. Run `scripts/check_bilingual_quality.py --units <units.jsonl>` and `scripts/check_source_alignment.py`, then manually review semantics and extraction order. Report skipped pages, OCR uncertainty, or incomplete scope.
