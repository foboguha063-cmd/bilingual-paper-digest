# Translation Fidelity Checklist

Use this reference together with `references/source-faithful-bilingual-format.md` whenever creating or revising bilingual Markdown output.

## Fidelity And Completeness

The body is a source-faithful bilingual rendering. Use these constraints:

- Preserve every substantive source sentence in the selected main text sections. Do not merge several source sentences into one English line or one Chinese summary.
- Preserve the original paragraph order and local argument order. Do not move background, results, limitations, or mechanisms to make a smoother narrative.
- Preserve hedging, scope, negation, contrast, causality, uncertainty, statistics, sample sizes, doses, time points, units, species, model names, and experimental conditions.
- Do not replace a paragraph with phrases such as `the authors mainly state`, `this section discusses`, `in summary`, `overall`, `本文主要说明`, `该段主要介绍`, or `总结来说` unless that metacommentary appears in the source sentence itself.
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
- Confirm no added summary sections, analytic headings, `main idea` sentences, or paragraph-level Chinese paraphrases have replaced source sentences.
- Confirm dense results/methods sentences retain all numbers, units, sample sizes, conditions, statistical terms, and limitations from the original sentence.
- For PDFs processed through the structured pipeline, confirm `.bilingual-paper-digest/source.jsonl` or `translation_units.jsonl` exists and that the Markdown was rendered from retained source sentences rather than directly from an untracked PDF impression.
- For structured PDF/book workflows, run `scripts/check_source_alignment.py` on the final Markdown unless sections were intentionally omitted; if omissions are intended, mark those translation units as `skipped` before checking.
- If knowledge cards were created or updated, confirm each concept has one canonical card, alternate names are listed as aliases, parent/child relationships are marked, and cross-domain concepts are linked instead of duplicated across folders.
- Run `scripts/check_digest.py` on the output when filesystem access is available, and fix any reported errors before finalizing.
- Run `scripts/check_knowledge_cards.py` on created/updated knowledge cards or the target card root when filesystem access is available, and fix duplicate-title or alias-conflict findings before finalizing.
