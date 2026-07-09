---
name: bilingual-paper-digest
description: Create Chinese-English academic Markdown notes from papers, reviews, preprints, conference papers, methods papers, clinical studies, materials/engineering articles, PDF books or chapters, and Obsidian knowledge-card workflows in a trained source-faithful bilingual format. Use when the user asks to 整理文献, 整理为上述格式, 尚书格式, 双语整理, 原文+中文翻译, Obsidian 文献整理, PDF 书籍翻译, 知识卡片整理, or asks Codex to process a PDF/DOI/article/book into a bilingual Markdown literature note.
---

# Bilingual Paper Digest

Create a Markdown academic reading note: bibliographic header, sentence-level English-Chinese pairs, tab-indented Chinese academic translation, original citation markers, and optional Obsidian-ready linking or knowledge cards. The default artifact is a compact bilingual note rather than a full reader, slide deck, or summary.

## Bundled Resources

- Read `references/obsidian-vault-style.md` when the user mentions Obsidian, 文献库, vault paths, wiki links, figure folders, or asks to write the note into the local literature library.
- Read `references/knowledge-card-system.md` when the user asks to extract terminology, named methods, statistical methods, materials, diseases, brain regions, algorithms, characterization methods, or reusable concepts as Obsidian knowledge cards.
- Read `references/paper-type-routing.md` before handling unfamiliar disciplines or non-standard papers such as methods, resources, clinical studies, reviews, and conference papers.
- Read `references/pdf-extraction-pipeline.md` before processing PDFs with complex layouts, scanned pages, books, or repeated/batch work.
- Read `references/book-translation-mode.md` when the user asks to translate or organize a PDF book, monograph, textbook, dissertation, report, or long chapter-based document.
- Read `references/translation-memory.md` when reducing token use, reusing previous translations, preserving terminology across runs, or resuming long documents.
- Read `references/environment-and-sharing.md` when setting up this skill for a new machine, another user, or a shared GitHub installation.
- Read `references/skill-suite-routing.md` when deciding how to route paper, book, and knowledge-base tasks; when explaining minimal invocation phrases for other users; or when considering a future split into companion skills.
- Read `references/improvement-roadmap.md` when updating this skill or evaluating remaining gaps.
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

## Header Format

Use this shape at the top. Do not add a separate "题录简介" unless the user explicitly asks.

```markdown
Original English Title
中文题名/短标题
	核心主题1
	核心主题2
	研究对象/机制/应用
**团队**：中文最高级机构_通讯作者 + 境外最高级机构中文名（English Name）_通讯作者
DOI：https://doi.org/...
Journal Name
Published ...
Article / Review
```

### Team Line Rules

- List corresponding authors only. Do not list all authors.
- Identify corresponding authors from correspondence lines, email markers, asterisks, or author notes.
- List only the highest-level institution for each corresponding author. Remove labs, departments, schools, colleges, centers, key laboratories, and units when a parent university/institute/hospital is present.
- For institutions in mainland China, Hong Kong, Macau, or Taiwan: use the Chinese institution name only, without English in parentheses.
- For institutions outside China: provide the Chinese institution name followed by the official English name in parentheses.
- Foreign scholars: keep the original English name only. Do not add Chinese transliterations.
- Chinese scholars: write Chinese name first, with English name in parentheses if useful, e.g. `卓敏（Min Zhuo）`.
- Use the existing local style: `机构_作者 + 机构_作者`.

## Body Format

Use sentence-level bilingual pairs within each source paragraph: write one complete English sentence, then immediately write its tab-indented Chinese translation on the next line. Treat the source paragraph as the grouping unit, and the source sentence as the bilingual alignment unit.

```markdown
First English sentence from the same source paragraph with citations in original positions [1,2].
	第一句对应的中文学术翻译，忠实保留术语、限定语、数字和逻辑关系。
Second English sentence from the same source paragraph.
	第二句对应的中文学术翻译。


First English sentence from the next source paragraph.
	下一自然段第一句对应的中文翻译。
```

Spacing is required only between original source paragraphs: leave at least two blank lines after the final Chinese translation line of one source paragraph before the first English sentence of the next source paragraph starts, or use a clear horizontal rule if the user requests separators. Do not insert blank lines between sentence pairs that belong to the same source paragraph.

Do split ordinary prose paragraphs into sentence-by-sentence bilingual pairs, but keep those sentence pairs grouped by their original paragraph. Split at real sentence boundaries, not at PDF line wraps. Preserve headings, list items, equations, and other structural breaks from the source.

Keep headings from the source:

```markdown
# Abstract
# Introduction
# Results / Results and Discussion
# Methods / Experimental Section
# Discussion
# Conclusions
```

For review papers, keep thematic headings such as `# The ACC within the nociceptive pathway`, `## Anatomy`, etc.

## Fidelity And Completeness

The body is a source-faithful bilingual rendering, not a digest summary. Use these constraints:

- Preserve every substantive source sentence in the selected main text sections. Do not merge several source sentences into one English line or one Chinese summary.
- Preserve the original paragraph order and local argument order. Do not move background, results, limitations, or mechanisms to make a smoother narrative.
- Preserve hedging, scope, negation, contrast, causality, uncertainty, statistics, sample sizes, doses, time points, units, species, model names, and experimental conditions.
- Do not replace a paragraph with phrases such as "the authors mainly state", "this section discusses", "in summary", "overall", "本文主要说明", "该段主要介绍", or "总结来说" unless that metacommentary appears in the source sentence itself.
- Do not add analytic headings such as `研究背景`, `核心发现`, `机制总结`, or `临床意义` unless they are literal source headings. Keep source headings instead.
- Do not infer conclusions, mechanisms, clinical meanings, or limitations beyond what the sentence states.
- Do not convert ordinary prose into bullets, tables, or thematic summaries unless the source itself uses that structure.
- If extraction order is uncertain or a paragraph is incomplete, inspect the rendered PDF/source page. Mark unresolved extraction uncertainty in the final chat response, not by inventing a summary inside the note.
- If space or time prevents full processing, stop at the last fully translated source paragraph and report the remaining sections as unfinished. Never fill unfinished sections with summaries.

Self-check after drafting each section:

1. Compare the output against the extracted source text for that section.
2. Confirm each retained English source sentence has exactly one immediate tab-indented Chinese translation.
3. Confirm no source paragraph has been collapsed into a "main idea" sentence.
4. Confirm numbers, citations, qualifiers, and negative statements have not been dropped.
5. Rewrite any paragraph that reads like a Chinese explanation rather than a line-by-line translation.

## Citations

Keep reference markers in the same location as the source text, not merely at the end of the sentence.

- Convert superscript or extracted citation numbers to bracket form: `pain3-5` -> `pain [3-5]`.
- Preserve location near the supported phrase or clause:
  - Source-like: `chronic pain3-5` -> `chronic pain [3-5]`
  - Source-like: `S1 (REF. 23)` -> `S1 (REF. [23])`
  - Source-like: `One study50 reported` -> `One study [50] reported`
  - Source-like: `one laboratory88 but disputed by another89` -> `one laboratory [88] but disputed by another [89]`
- Do not create a reference list unless the user asks.
- If exact citation placement is uncertain because PDF extraction is poor, inspect the rendered page or source text and place the marker as close as possible to its original phrase.

## What To Omit

Unless explicitly requested, omit:

- standalone `Glossary` sections and side glossary definitions
- figure images, table images, screenshots, and media
- figure captions and table captions
- extracted table bodies
- acknowledgements, author contributions, competing interests, publisher boilerplate
- full References list

Retain ordinary in-text mentions such as `(FIG. 1)`, `(TABLE 1)`, or `(BOX 1)` if they appear inside a prose sentence.

For Obsidian notes, do not add wiki links, images, personal annotation blocks, or knowledge-base candidate sections unless the user asks for those features or the vault style reference says they are appropriate for the requested mode.

## Boxes And Side Content

Move Box content to the end of the Markdown after `# Conclusions`.

Use:

```markdown
# Box 附录
# Box 1 | Original box title
English box text with citations in original positions [69].
	对应中文翻译。
Next English box sentence.
	下一句中文翻译。
```

Preserve Box titles and translate the Box body in the same sentence-level original-plus-tabbed-Chinese format. Do not leave boxes in the middle of the main section flow.

## Translation Style

- Use formal academic Chinese.
- Translate the source sentence; do not explain, interpret, or summarize it.
- Translate for meaning while preserving hedging: `may`, `suggest`, `it is likely`, `has been shown`.
- Preserve abbreviations and define them naturally where the original does: `anterior cingulate cortex (ACC)` -> `前扣带皮层（ACC）`.
- Preserve gene/protein/receptor/channel names, formulas, units, Greek letters, and experimental terms.
- Do not over-polish into a summary or rewrite the prose into a smoother review paragraph. Keep the source's evidence chain and paragraph sequence.

## Final Check

Before responding:

- Confirm the Markdown has no `题录简介` unless requested.
- Confirm no standalone `# Glossary`.
- Confirm Box sections are after the main conclusions.
- Confirm foreign scholar names are not transliterated into Chinese.
- Confirm Chinese scholars have Chinese names when known.
- Confirm citation markers remain close to original source positions.
- Confirm there are no image/table embed syntaxes or extracted reference lists.
- Confirm each English sentence is followed immediately by its tab-indented Chinese translation.
- Confirm sentence pairs from the same source paragraph are adjacent, with no extra blank lines between them.
- Confirm there are clear blank lines or separators between source paragraphs.
- Confirm no added summary sections, analytic headings, "main idea" sentences, or paragraph-level Chinese paraphrases have replaced source sentences.
- Confirm dense results/methods sentences retain all numbers, units, sample sizes, conditions, statistical terms, and limitations from the original sentence.
- For PDFs processed through the structured pipeline, confirm `.bilingual-paper-digest/source.jsonl` or `translation_units.jsonl` exists and that the Markdown was rendered from retained source sentences rather than directly from an untracked PDF impression.
- For structured PDF/book workflows, run `scripts/check_source_alignment.py` on the final Markdown unless sections were intentionally omitted; if omissions are intended, mark those translation units as `skipped` before checking.
- If knowledge cards were created or updated, confirm each concept has one canonical card, alternate names are listed as aliases, parent/child relationships are marked, and cross-domain concepts are linked instead of duplicated across folders.
- Run `scripts/check_digest.py` on the output when filesystem access is available, and fix any reported errors before finalizing.
- Run `scripts/check_knowledge_cards.py` on created/updated knowledge cards or the target card root when filesystem access is available, and fix duplicate-title or alias-conflict findings before finalizing.
