---
name: bilingual-paper-digest
description: Create Chinese-English academic Markdown notes from papers, reviews, preprints, conference papers, methods papers, clinical studies, materials/engineering articles, PDF books or chapters, and Obsidian knowledge-card workflows in a trained source-faithful bilingual format. Use when the user asks to 整理文献, 整理为上述格式, 尚书格式, 双语整理, 原文+中文翻译, Obsidian 文献整理, PDF 书籍翻译, 知识卡片整理, or asks Codex to process a PDF/DOI/article/book into a bilingual Markdown literature note.
---

# Bilingual Paper Digest

Create a Markdown academic reading note: bibliographic header, sentence-level English-Chinese pairs, tab-indented Chinese academic translation, original citation markers, and optional Obsidian-ready linking or knowledge cards. The default artifact is a compact bilingual note rather than a full reader, slide deck, or summary.

## Bundled Resources

- Read `references/obsidian-vault-style.md` when the user mentions Obsidian, 文献库, vault paths, wiki links, figure folders, or asks to write the note into the local literature library.
- Read `references/source-faithful-bilingual-format.md` when creating or revising any bilingual paper note, book/chapter translation, or source-aligned Markdown output.
- Read `references/translation-fidelity-checklist.md` with the source-faithful format reference when checking translation completeness, citation placement, omission rules, Box relocation, and final output quality.
- Read `references/knowledge-card-system.md` when the user asks to extract terminology, named methods, statistical methods, materials, diseases, brain regions, algorithms, characterization methods, or reusable concepts as Obsidian knowledge cards.
- Read `references/paper-type-routing.md` before handling unfamiliar disciplines or non-standard papers such as methods, resources, clinical studies, reviews, and conference papers.
- Read `references/pdf-extraction-pipeline.md` before processing PDFs with complex layouts, scanned pages, books, or repeated/batch work.
- Read `references/book-translation-mode.md` when the user asks to translate or organize a PDF book, monograph, textbook, dissertation, report, or long chapter-based document.
- Read `references/translation-memory.md` when reducing token use, reusing previous translations, preserving terminology across runs, or resuming long documents.
- Read `references/environment-and-sharing.md` when setting up this skill for a new machine, another user, or a shared GitHub installation.
- Read `references/skill-suite-routing.md` when deciding how to route paper, book, and knowledge-base tasks; when explaining minimal invocation phrases for other users; or when considering a future split into companion skills.
- Read `references/improvement-roadmap.md` when updating this skill or evaluating remaining gaps.
- Use `companions/` only when installing or updating the narrow entry-point skills `bilingual-paper-reader`, `bilingual-book-reader`, and `knowledge-base-curator`; normal paper processing should not load companion files.
- Use `examples/minimal-paper-note.md` as the compact text-only output model.
- Use `examples/obsidian-material-note.md` as the Obsidian material-paper model with restrained wiki links.
- Run `scripts/probe_tools.py` when environment capability is uncertain.
- Run `scripts/extract_pdf_structure.py <paper.pdf>` before long, complex, scanned, or book-like PDF work so source text is captured once and reused from `.bilingual-paper-digest/source.jsonl`.
- Run `scripts/build_translation_units.py <source.jsonl>` when sentence-level batching, cache reuse, or stricter source-output alignment is needed.
- Run `scripts/translation_cache.py apply/update/stats` when resuming long translations or avoiding repeated token use for unchanged source sentences.
- Run `scripts/check_source_alignment.py --units <translation_units.jsonl> --markdown <output.md>` when the Markdown should be proven against structured source units.
- Run `scripts/install_skill.py` when installing this repository into another user's local Codex skills directory.
- Run `scripts/run_checks.py` after changing the skill, scripts, examples, or shared installation behavior.
- Run `scripts/check_digest.py <output.md>` after creating or revising a text-only note. Use `--allow-images` only when the user explicitly requests figure/media integration.
- Run `scripts/check_knowledge_cards.py <card-files-or-card-root>` after creating or updating knowledge cards when filesystem access is available; use `--strict` for newly created card files.

## Core Workflow

1. Route the task first: paper note, book/chapter translation, Obsidian literature note, knowledge-card extraction, or format/source-alignment checking. Use `references/skill-suite-routing.md` for ambiguous multi-part requests.
2. Read the source document completely enough to identify title, authors, affiliations, venue, DOI/ISBN if present, publication date, document type, sections, boxes, and references.
3. If the source is a PDF, choose the extraction route first. For ordinary selectable PDFs, use available PDF text extraction; for complex or repeated work, run `scripts/extract_pdf_structure.py`; for scanned PDFs, OCR first; for books, follow `references/book-translation-mode.md`.
4. Classify the paper type before writing the note. Use `references/paper-type-routing.md` if the structure is not a standard research article.
5. Create or update one `.md` file in the user's working folder unless they specify another path.
6. If writing into an Obsidian vault, follow `references/obsidian-vault-style.md` for folder choice, filename, wiki links, and attachment behavior.
7. If the user asks for knowledge cards or bidirectional links, follow `references/knowledge-card-system.md`; before creating any card, scan existing card filenames, H1 titles, aliases, and related folders so aliases merge into existing canonical cards instead of creating duplicates.
8. Preserve the source section flow for main text. Move all Box-style side content to the document end.
9. Do not summarize, compress, paraphrase into review-style prose, or replace source sentences with extracted "main ideas". Translate sentence by sentence while preserving the source paragraph boundaries, argument order, qualifiers, numbers, and technical detail.

## Output Contract

For every bilingual note or translation output, read and follow `references/source-faithful-bilingual-format.md`. That reference is the authority for the header, team line, paragraph spacing, sentence-level bilingual pairing, citation-marker placement, omitted sections, Box relocation, translation fidelity, and final self-checks.

The default output is a text-only Markdown file. Unless the user explicitly asks otherwise, omit images, tables, captions, standalone glossaries, acknowledgements, author contribution sections, competing interests, publisher boilerplate, and full reference lists.

## Essential Constraints

- Do not add a separate `题录简介` unless the user asks for it.
- List corresponding authors only, not all authors.
- For China-based institutions, use only the Chinese highest-level institution name. For institutions outside China, use Chinese institution name plus official English name in parentheses.
- Do not transliterate foreign scholar names into Chinese. Use known Chinese names for Chinese scholars when available.
- Keep each English source sentence immediately followed by exactly one tab-indented Chinese translation.
- Keep sentence pairs from the same source paragraph adjacent, with no blank lines between pairs.
- Insert blank lines or separators only between original source paragraphs.
- Preserve citation markers near their original phrase or clause, using bracket form such as `[1]`.
- Move Box-style side content to the end of the Markdown.
- Do not summarize, collapse, paraphrase into "main ideas", or add analytic headings that do not exist in the source.

## Final Check

Before responding, run available validators when filesystem access permits:

- `scripts/check_digest.py <output.md>` for text-only bilingual notes.
- `scripts/check_source_alignment.py --units <translation_units.jsonl> --markdown <output.md>` for structured PDF/book workflows.
- `scripts/check_knowledge_cards.py <card-files-or-card-root>` for created or updated knowledge cards.

If a validator cannot be run, state that clearly in the final response and manually check the corresponding constraints from `references/source-faithful-bilingual-format.md`.
