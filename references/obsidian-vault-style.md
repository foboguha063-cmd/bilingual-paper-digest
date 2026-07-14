# Obsidian Vault Style

Use this reference when the user asks to write into Obsidian, a literature vault, or a paper-note folder inside a vault. Treat the folder names below as a style pattern that can be adapted to the user's actual vault.

## Vault Layout

Common vault shape:

```text
<vault-root>/
├── 材料论文及笔记/
│   └── figure/
├── 医学论文及笔记/
│   └── figure/
├── 材料知识库/
│   ├── 化学概念/
│   ├── 化学物质/
│   ├── 表征测量/
│   ├── 统计方法/
│   ├── 医学与神经科学/
│   └── 算法与数据方法/
└── .obsidian/
```

Obsidian is configured with:

```json
{
  "alwaysUpdateLinks": true,
  "attachmentFolderPath": "./figure"
}
```

Default output targets:

- Materials, polymers, gels, electrodes, bioelectronics, ion conductors: `材料论文及笔记/`
- Pain, sleep, neuroscience, medicine, clinical papers: `医学论文及笔记/`
- Short concept, material, method, or statistics entries derived from repeated terms: `材料知识库/`

If the field is ambiguous, choose the closest existing paper-note folder and state the chosen path.

## Paper Note Shape

Do not add YAML frontmatter by default. Existing paper notes start directly with title metadata.

Use this top block:

```markdown
Original English Title
中文题名
	关键词1
	关键词2
	研究对象/方法/应用
**团队**：最高级机构_通讯作者 + 境外机构中文名（Official English Name）_Corresponding Author
DOI：https://doi.org/...
Journal Name, year, volume:pages/article number
Received/Revised/Accepted/Published lines if available
Article / Review / Research Article
```

Keep the trained sentence-level bilingual body:

```markdown
English sentence with citation marker in the original location [1].
	对应中文学术翻译。
Second English sentence from the same source paragraph.
	同一原文自然段内的第二句中文翻译。


English sentence from the next source paragraph.
	下一自然段的中文翻译。
```

Do not insert blank lines between sentence pairs from the same source paragraph. Use at least two blank lines between source paragraphs.

## Obsidian Links

Use Obsidian wiki links only when they improve the vault graph.

- Link existing materials and concepts on first meaningful occurrence per major section, not every occurrence.
- Prefer exact existing note names, for example: `[[PVA]]`, `[[IP6]]`, `[[CS]]`, `[[AA]]`, `[[VTF]]`, `[[螯合（Chelation）]]`, `[[Dissipation-induced toughening]]`.
- Do not wrap every technical term in a wiki link.
- Do not invent block IDs such as `^abc123` unless preserving an existing user anchor.
- Do not add personal note callouts such as `<font color="#1f497d">【冒烟小马】</font>` unless the user asks for personal annotations.

If a paper introduces a recurring material/concept that does not yet exist in `材料知识库`, add a final short section only when the user asks for knowledge-base expansion:

```markdown
# 知识库候选词
- [[Term]]：建议新建于 `材料知识库/化学概念/`，原因...
```

Do not create separate knowledge-base notes unless explicitly requested.

For knowledge-card creation, use `references/knowledge-card-system.md`. The paper note should only contain restrained links, while the card contains definition, method logic, boundaries, and source-paper backlinks.

## Images And Media

The trained default is text-only. Do not extract or embed images, tables, videos, figure captions, or table bodies unless the user explicitly asks for Obsidian figure integration.

When figure integration is requested:

- Put media files in the note folder's `figure/` directory.
- Use Obsidian embeds: `![[filename.png]]` or `![[filename.png|360]]`.
- Keep image embeds directly after the sentence that first discusses the figure.
- Keep figure captions short and bilingual only if the user asks for captions.

If the user says "无需整理图片图表" or similar, omit all embeds even though existing vault notes may contain them.

## Folder-Specific Notes

`材料论文及笔记` often links chemical materials and methods back to `材料知识库`. Use restrained links for repeated entities central to the paper.

`医学论文及笔记` currently prioritizes clean bilingual paper structure over knowledge-base expansion. Use fewer wiki links unless the user has already created relevant medical concept notes.

`材料知识库` entries are concise Chinese explanatory notes with application backlinks at the end:

```markdown
# **应用场景**
1.论文或主题[[相关论文笔记]]
```

Do not convert a paper note into a knowledge-base note.

## Final Obsidian Check

Before finishing an Obsidian-targeted note:

- Confirm the file path is under the intended vault folder.
- Confirm the filename is a short Chinese paper title and does not contain DOI punctuation.
- Confirm no YAML frontmatter was added unless requested.
- Confirm wiki links point to meaningful existing or intended notes.
- Confirm image embeds are absent unless explicitly requested.
- Confirm the output remains readable in Obsidian source mode: no HTML styling unless requested.
