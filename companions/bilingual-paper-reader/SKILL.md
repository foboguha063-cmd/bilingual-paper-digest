---
name: bilingual-paper-reader
description: Create source-faithful sentence-level Chinese-English Markdown reading notes from academic papers, journal articles, preprints, conference papers, reviews, methods papers, clinical studies, materials papers, PDFs, DOIs, or pasted article text. Use when the user asks to 整理论文, 整理文献, 双语阅读, 尚书格式, 原文+中文翻译, 按照格式整理这篇论文, or turn a paper into the trained bilingual-paper-digest note format.
---

# Bilingual Paper Reader

Use this companion skill as the narrow entry point for ordinary academic papers. It shares the installed sibling root skill at `../bilingual-paper-digest`; if that folder is missing, ask the user to install the repository with `scripts/install_skill.py`.

## Shared Resources

- Read `../bilingual-paper-digest/SKILL.md` for root routing and shared workflow rules.
- Read `../bilingual-paper-digest/references/source-faithful-bilingual-format.md` for the required header, team-line, sentence-pair, citation, omission, Box, and final-check rules.
- Read `../bilingual-paper-digest/references/translation-fidelity-checklist.md` for source-faithfulness, citation placement, omission rules, Box relocation, and final self-check constraints.
- Read `../bilingual-paper-digest/references/paper-type-routing.md` before writing a note for reviews, methods/tool papers, clinical studies, resource/data papers, conference papers, or unfamiliar disciplines.
- Read `../bilingual-paper-digest/references/pdf-extraction-pipeline.md` before processing PDFs with complex layouts, scanned pages, poor extraction, or repeated/batch work.
- Read `../bilingual-paper-digest/references/translation-memory.md` when resuming a long paper or reusing checked translations.
- Run `../bilingual-paper-digest/scripts/check_digest.py <output.md>` after drafting when filesystem access is available.
- Run `../bilingual-paper-digest/scripts/check_source_alignment.py` when the paper was processed through translation units.

## Workflow

1. Treat the task as a paper note, not a book translation or knowledge-card extraction, unless the user explicitly asks for those additional outputs.
2. Extract enough source metadata to fill the trained header and identify corresponding authors.
3. Preserve the paper's section flow and translate sentence by sentence from the source text.
4. Keep original paragraph boundaries: no blank lines inside one source paragraph; clear blank spacing between source paragraphs.
5. Do not include figures, tables, standalone glossary, full references, or a separate 题录简介 unless the user asks.
6. Move Box-style side content to the end of the note.
7. Stop at the last fully translated paragraph if the paper cannot be completed in one pass; report unfinished sections in the final chat response instead of summarizing them inside the note.
