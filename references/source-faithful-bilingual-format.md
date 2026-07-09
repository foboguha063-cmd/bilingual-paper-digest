# Source-Faithful Bilingual Format

Use this reference whenever creating or revising a bilingual Markdown paper note, book/chapter translation, or source-aligned academic text output. The goal is source-faithful bilingual rendering, not a digest summary.

## Header Format

Use this shape at the top. Do not add a separate `题录简介` unless the user explicitly asks.

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

## Team Line Rules

- List corresponding authors only. Do not list all authors.
- Identify corresponding authors from correspondence lines, email markers, asterisks, or author notes.
- List only the highest-level institution for each corresponding author. Remove labs, departments, schools, colleges, centers, key laboratories, and units when a parent university/institute/hospital is present.
- For institutions in mainland China, Hong Kong, Macau, or Taiwan: use the Chinese institution name only, without English in parentheses.
- For institutions outside China: provide the Chinese institution name followed by the official English institution name in parentheses.
- Foreign scholars: keep the original English name only. Do not add Chinese transliterations.
- Chinese scholars: write Chinese name first, with English name in parentheses if useful, e.g. `卓敏（Min Zhuo）`.
- Use the existing local style: `机构_作者 + 机构_作者`.

## Body Format

Use sentence-level bilingual pairs within each source paragraph. Write one complete English sentence, then immediately write its tab-indented Chinese translation on the next line. Treat the source paragraph as the grouping unit, and the source sentence as the bilingual alignment unit.

```markdown
First English sentence from the same source paragraph with citations in original positions [1,2].
	第一句对应的中文学术翻译，忠实保留术语、限定语、数字和逻辑关系。
Second English sentence from the same source paragraph.
	第二句对应的中文学术翻译。


First English sentence from the next source paragraph.
	下一自然段第一句对应的中文翻译。
```

Spacing is required only between original source paragraphs: leave at least two blank lines after the final Chinese translation line of one source paragraph before the first English sentence of the next source paragraph starts, or use a clear horizontal rule if the user requests separators. Do not insert blank lines between sentence pairs that belong to the same source paragraph.

Split ordinary prose paragraphs into sentence-by-sentence bilingual pairs, but keep those sentence pairs grouped by their original paragraph. Split at real sentence boundaries, not at PDF line wraps. Preserve headings, list items, equations, and other structural breaks from the source.

Keep headings from the source, for example:

```markdown
# Abstract
# Introduction
# Results / Results and Discussion
# Methods / Experimental Section
# Discussion
# Conclusions
```

For review papers, keep thematic source headings such as `# The ACC within the nociceptive pathway`, `## Anatomy`, etc.

For fidelity, citation placement, omission rules, Box relocation, translation style, and final self-checks, also read `references/translation-fidelity-checklist.md`.
