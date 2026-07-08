---
name: bilingual-paper-digest
description: Create Chinese-English academic Markdown reading notes from papers in the user's trained format. Use when the user asks to 整理文献, 整理为上述格式, 尚书格式, 双语整理, 原文+中文翻译, or asks Codex to process a PDF/DOI/article into a bilingual Markdown literature note that matches the local paper-note style.
---

# Bilingual Paper Digest

Create a Markdown paper note that imitates the user's established folder style: bibliographic header, sentence-level English-Chinese pairs, tab-indented Chinese academic translation, original citation markers, and no figure/table extraction.

## Core Workflow

1. Read the source paper completely enough to identify title, authors, affiliations, journal, DOI, publication date, article type, sections, boxes, and references.
2. If the source is a PDF, use PDF extraction tools. For two-column review PDFs, inspect extraction order and clean mixed columns, sidebars, headers, footers, author affiliations, figure captions, and references.
3. Create or update one `.md` file in the user's working folder unless they specify another path.
4. Preserve the source section flow for main text. Move all Box-style side content to the document end.
5. Do not summarize instead of translating. Translate sentence by sentence while preserving the source paragraph boundaries and technical detail.

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
- Translate for meaning while preserving hedging: `may`, `suggest`, `it is likely`, `has been shown`.
- Preserve abbreviations and define them naturally where the original does: `anterior cingulate cortex (ACC)` -> `前扣带皮层（ACC）`.
- Preserve gene/protein/receptor/channel names, formulas, units, Greek letters, and experimental terms.
- Do not over-polish into a summary. Keep the source's evidence chain and paragraph sequence.

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
