---
name: bilingual-book-reader
description: Translate and organize PDF books, monographs, textbooks, theses, dissertations, long reports, book chapters, or chapter-based long documents into source-faithful sentence-level Chinese-English Markdown. Use when the user asks to 翻译PDF书, 整理这本书, 翻译章节, 书籍双语阅读, chapter translation, book translation, or continue a long PDF translation in bilingual-paper-digest format.
---

# Bilingual Book Reader

Use the installed sibling `../bilingual-paper-digest` as the shared runtime. If it is missing, stop and ask the user to install the root skill.

## Workflow

1. Read `../bilingual-paper-digest/references/bilingual-output-contract.md` and `../bilingual-paper-digest/references/book-translation-mode.md`.
2. Read `../bilingual-paper-digest/references/pdf-extraction-pipeline.md` before extracting a PDF and `../bilingual-paper-digest/references/translation-memory.md` before translating or resuming long units.
3. Confirm the requested book, chapter, section, or page range. Do not expand the scope silently.
4. Build or reuse structured source and translation units, then translate only pending units chapter by chapter while preserving headings, paragraph order, notes, citations, and numbered structure.
5. Reuse a checked translation only when its source hash matches. Never fill an unfinished chapter with a summary.
6. Run `../bilingual-paper-digest/scripts/check_source_alignment.py` when translation units exist, fix errors, and report skipped pages, OCR uncertainty, or incomplete scope.
