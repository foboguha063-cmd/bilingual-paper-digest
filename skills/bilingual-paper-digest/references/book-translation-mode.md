# Book Translation Mode

Use this reference when the source is a PDF book, monograph, textbook, dissertation, report, manual, or any long chapter-based document.

## Difference From Paper Mode

Do not force a book into the paper note format. For books, preserve the book's chapter structure and translate in resumable units.

Default book output:

```text
Book Title/
├── 00-目录与说明.md
├── 01-Chapter-title.md
├── 02-Chapter-title.md
└── .bilingual-paper-digest/
    ├── source.jsonl
    ├── source_map.json
    └── translation_units.jsonl
```

## Intake

Before translating:

1. Identify title, author/editor, edition, publisher, year, DOI/ISBN if available.
2. Identify table of contents and chapter boundaries when possible.
3. Decide whether to translate the whole book, selected chapters, or selected pages.
4. Probe whether the PDF is selectable text or scanned.
5. Extract once with `scripts/extract_pdf_structure.py --book`.

## Translation Rules

- Translate chapter by chapter.
- Preserve original chapter and section headings.
- Preserve page numbers in source metadata, but do not clutter every output sentence with page numbers unless requested.
- Preserve footnotes and endnotes when they contain substantive explanatory content; omit purely bibliographic notes unless requested.
- Do not translate copyright pages, index, advertisements, blank pages, or full bibliography unless requested.
- If a chapter is too long, split by section or page range and resume from the last completed unit.
- Never fill an unfinished chapter with a summary.

## Suggested Output Header

```markdown
Book English Title
中文书名/章节题名
作者 / 编者：
出版社：
Year：
ISBN / DOI：
Chapter：
Page range：
```

Then follow `references/bilingual-output-contract.md` for translated prose.

## Resumability

Use `translation_units.jsonl` status values:

- `pending`: not translated
- `translated`: translated but not yet rendered
- `checked`: source-aligned and rendered
- `skipped`: intentionally omitted, with reason

When resuming, translate only `pending` units.
Use `scripts/translation_cache.py apply` before translating a resumed chapter, then `scripts/translation_cache.py update` after the chapter has passed source-alignment review.

## Public-Use Simplicity

For another user, expose only simple requests:

- "Translate chapter 1 of this PDF book."
- "Translate pages 20-45 in bilingual format."
- "Continue translating this book from the last completed section."

Codex should handle extraction, chunking, cache reuse, and output folder organization internally.
