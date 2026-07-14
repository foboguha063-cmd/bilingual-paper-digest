---
name: bilingual-paper-reader
description: Create source-faithful, sentence-aligned English-Chinese Markdown readers for academic papers from PDFs, DOIs, publisher or preprint pages, pasted text, or existing extractions. Use for journal articles, reviews, methods papers, clinical studies, materials or engineering papers, and conference papers when the user asks to read, translate, organize, continue, or audit a paper with original English plus Chinese translation, including 整理论文, 整理文献, 双语阅读, 尚书格式, 原文+中文翻译, or Obsidian literature notes. Do not use for summary-only requests unless source-aligned bilingual output is also requested.
---

# Bilingual Paper Reader

Use this folder as a self-contained runtime. Load only the references needed for the current paper.

## Workflow

1. Read `references/bilingual-output-contract.md` before writing.
2. Read `references/paper-type-routing.md` for reviews, methods, clinical, resource, conference, or unfamiliar structures. Read `references/obsidian-vault-style.md` only inside an Obsidian vault.
3. Read `references/pdf-extraction-pipeline.md` only for complex, scanned, long, or resumable PDFs; read `references/translation-memory.md` only for batch, resume, or checked reuse.
4. Extract the metadata and source structure required by the output contract, then translate retained prose sentence by sentence in source order.
5. For structured work, keep IDs and source hashes unchanged, translate only pending units, run `scripts/check_bilingual_quality.py --units <units.jsonl>`, then render with `scripts/render_bilingual_markdown.py`.
6. Write one Markdown note. Do not add figures, tables, a glossary, full references, knowledge cards, or a separate `题录简介` unless requested.
7. Run `scripts/check_digest.py <output.md>` and, when units exist, `scripts/check_source_alignment.py`. Fix errors and manually review semantic equivalence; report unfinished scope or extraction risk outside the note.
