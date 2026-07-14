# Bilingual Output Contract

Use this reference for every bilingual paper note, chapter translation, or source-aligned academic Markdown output. Render the source faithfully; do not turn it into a digest summary.

## Header

For papers, use this compact shape and omit unavailable fields. Do not add a separate `题录简介` unless requested.

```markdown
Original English Title
中文题名/短标题
	核心主题1
	核心主题2
	研究对象/机制/应用
**团队**：最高级机构_通讯作者 + 境外机构中文名（Official English Name）_Corresponding Author
DOI：https://doi.org/...
Journal Name
Published ...
Article / Review
```

List corresponding authors only. Use the highest-level institution and remove subordinate labs, departments, schools, centers, and units when a parent institution is available.

- For institutions in mainland China, Hong Kong, Macau, or Taiwan, use the Chinese institution name only.
- For institutions outside China, use the Chinese name followed by the official English name in parentheses.
- Keep foreign scholars' original names without Chinese transliteration.
- Use Chinese names for Chinese scholars when known; add the English form only when useful.
- Keep the local `机构_作者 + 机构_作者` style.

For books, follow the metadata header and file organization in `references/book-translation-mode.md` instead of forcing paper metadata.

## Body

Write one complete English source sentence followed immediately by exactly one tab-indented Chinese translation. Keep sentence pairs from one source paragraph adjacent; insert at least two blank lines only between source paragraphs.

```markdown
# Abstract
First source sentence with its citation near the supported phrase [1].
	第一句对应的中文学术翻译，并保留引用位置[1]。
Second source sentence from the same paragraph.
	同一原文段落的第二句译文。


First sentence from the next source paragraph.
	下一原文段落的第一句译文。
```

Split on real sentence boundaries, not PDF line wraps. Preserve source headings, lists, equations, paragraph order, and local argument order. Use the source's section structure rather than adding headings such as `核心发现`, `机制总结`, or `临床意义`.

## Fidelity

- Preserve every substantive sentence in the selected scope; do not merge several sentences into one English line or one Chinese summary.
- Preserve hedging, scope, negation, contrast, causality, uncertainty, sample sizes, doses, time points, units, species, model names, statistics, and experimental conditions.
- Translate into formal academic Chinese without explaining, interpreting, or strengthening the claim.
- Preserve abbreviations, gene/protein names, formulas, Greek letters, math, and code identifiers.
- Do not convert prose into bullets, tables, or thematic summaries unless the source uses that structure.
- If extraction order or wording is uncertain, inspect the rendered source page. Do not guess.
- If the requested scope cannot be completed, stop after the last fully translated paragraph and report the remainder outside the note.

## Citations

Keep markers close to the phrase or clause they support. Normalize extracted numeric citations to bracket form when needed, for example `pain3-5` to `pain [3-5]` or `One study50` to `One study [50]`. Do not create a reference list unless requested.

## Default Omissions

Unless requested, omit figure and table media, captions, table bodies, standalone glossaries, full reference lists, acknowledgements, author contributions, competing interests, and publisher boilerplate. Retain ordinary prose mentions such as `(FIG. 1)` or `(BOX 1)`.

Move Box/sidebar content after the main text under `# Box 附录`, preserve each Box title, and translate its prose using the same sentence-pair format.

## Final Review

Before delivery:

1. Confirm every retained English sentence has one immediate tab-indented Chinese translation.
2. Compare against the source for missing sentences, numbers, units, qualifiers, negation, and citations.
3. Confirm paragraph spacing and source heading order.
4. Confirm excluded sections, media, and added summaries are absent unless requested.
5. Confirm Box content is at the end.
6. Run `scripts/check_digest.py <output.md>` and fix errors. When structured units exist, also run `scripts/check_source_alignment.py` after marking intentional omissions as `skipped`.
