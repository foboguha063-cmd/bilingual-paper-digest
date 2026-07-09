---
name: bilingual-book-reader
description: Translate and organize PDF books, monographs, textbooks, theses, dissertations, long reports, book chapters, or chapter-based long documents into source-faithful sentence-level Chinese-English Markdown. Use when the user asks to 翻译PDF书, 整理这本书, 翻译章节, 书籍双语阅读, chapter translation, book translation, or process a long PDF book with bilingual-paper-digest formatting.
---

# Bilingual Book Reader

Use this companion skill as the narrow entry point for PDF books and long chapter-based documents. It shares the installed sibling root skill at `../bilingual-paper-digest`; if that folder is missing, ask the user to install the repository with `scripts/install_skill.py`.

## Shared Resources

- Read `../bilingual-paper-digest/SKILL.md` for root routing and shared workflow rules.
- Read `../bilingual-paper-digest/references/source-faithful-bilingual-format.md` for the sentence-level bilingual format, citation, omission, and final-check rules.
- Read `../bilingual-paper-digest/references/translation-fidelity-checklist.md` for source-faithfulness, citation placement, omission rules, Box relocation, and final self-check constraints.
- Read `../bilingual-paper-digest/references/book-translation-mode.md` before deciding scope, chapter boundaries, progress manifests, and output organization.
- Read `../bilingual-paper-digest/references/pdf-extraction-pipeline.md` before extracting text from long PDFs, scanned pages, mixed layouts, or OCR-dependent books.
- Read `../bilingual-paper-digest/references/translation-memory.md` before translating or resuming any chapter with many translation units.
- Run `../bilingual-paper-digest/scripts/extract_pdf_structure.py <book.pdf>` for structured extraction when the book is selectable or partially selectable.
- Run `../bilingual-paper-digest/scripts/build_translation_units.py <source.jsonl>` before long chapter translation, caching, or source-alignment checks.
- Run `../bilingual-paper-digest/scripts/check_source_alignment.py` after rendering Markdown when translation units exist.

## Workflow

1. Confirm the requested scope: whole book, selected chapter, selected page range, appendix, or report section.
2. Prefer chapter-by-chapter processing. Do not silently attempt a whole-book translation when the user asked for one chapter.
3. Build or reuse `.bilingual-paper-digest/source.jsonl` and `translation_units.jsonl` for long documents before translating.
4. Use checked translation cache entries only when the source sentence hash matches.
5. Preserve headings, paragraph order, numbered sections, footnotes that behave like prose, and citation markers when present.
6. Omit images, tables, captions, index pages, bibliography, and publisher boilerplate unless the user asks.
7. Report incomplete chapters, OCR uncertainty, skipped pages, or extraction failures in the final chat response rather than inventing summaries.
