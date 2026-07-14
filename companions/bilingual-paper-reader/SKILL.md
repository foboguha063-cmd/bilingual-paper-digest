---
name: bilingual-paper-reader
description: Create source-faithful sentence-level Chinese-English Markdown reading notes from academic papers, journal articles, preprints, conference papers, reviews, methods papers, clinical studies, materials papers, PDFs, DOIs, or pasted article text. Use when the user asks to 整理论文, 整理文献, 双语阅读, 尚书格式, 原文+中文翻译, 按照格式整理这篇论文, or turn a paper into the trained bilingual-paper-digest note format.
---

# Bilingual Paper Reader

Use the installed sibling `../bilingual-paper-digest` as the shared runtime. If it is missing, stop and ask the user to install the root skill.

## Workflow

1. Read `../bilingual-paper-digest/references/bilingual-output-contract.md` before writing.
2. Read `../bilingual-paper-digest/references/paper-type-routing.md` for reviews, methods, clinical, resource, conference, or unfamiliar paper structures.
3. Read `../bilingual-paper-digest/references/pdf-extraction-pipeline.md` only for complex, scanned, long, or resumable PDFs; read `../bilingual-paper-digest/references/translation-memory.md` only when continuing or reusing checked units.
4. Extract the metadata and source structure required by the output contract, then translate retained prose sentence by sentence in source order.
5. Write one Markdown note. Do not add figures, tables, a glossary, full references, knowledge cards, or a separate `题录简介` unless requested.
6. Run `../bilingual-paper-digest/scripts/check_digest.py <output.md>`. When structured units exist, also run `../bilingual-paper-digest/scripts/check_source_alignment.py`.
7. Fix validation errors and report any unfinished section or unresolved extraction risk without inserting a summary into the note.
