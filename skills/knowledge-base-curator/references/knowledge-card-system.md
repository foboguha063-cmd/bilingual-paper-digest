# Knowledge Card System

## Contents

- Design, folder taxonomy, identity, deduplication, and hierarchy
- Naming and reusable templates by concept type
- Paper-note links, candidate selection, and output modes

Use this reference when the user asks to extract terminology, statistical methods, named methods, materials, characterization methods, diseases, brain regions, algorithms, datasets, or reusable concepts from a paper into Obsidian knowledge cards.

## Design Model

Use an atomic-note system inspired by Zettelkasten and Obsidian MOC practice:

- One card explains one concept, method, material, statistic, disease, brain region, algorithm, or dataset.
- Paper notes are the evidence trail. Knowledge cards are reusable concept nodes.
- The bidirectional link must be explicit: the paper note links to the card, and the card links back to the paper note under `# **来源论文 / 应用场景**`.
- One concept must have one canonical card. Different names, abbreviations, translations, spelling variants, and paper-specific wording must be recorded as aliases on the canonical card instead of becoming new cards.
- Concepts with parent-child, part-whole, method-family, or subtype relationships must mark those relationships explicitly; do not flatten the knowledge base into unrelated cards.
- Do not create cards for every noun. Create cards only for concepts that are central, repeated, reusable across papers, or necessary for understanding methods/results.

## Folder Taxonomy

Adapt to the target vault. A practical default is:

```text
知识库/
├── 化学概念/
├── 化学物质/
├── 表征测量/
│   ├── 电学与离子导电测试/
│   ├── 力学性能表征/
│   └── 化学结构与分子相互作用表征/
├── 统计方法/
├── 医学与神经科学/
├── 算法与数据方法/
└── 数据集与资源/
```

If the existing vault already uses names such as `材料知识库`, preserve that naming. Do not rename the user's folders.

## Identity, Deduplication, And Hierarchy

Always run a preflight check before creating a card:

1. Search the relevant knowledge folders for existing filenames, first-level headings, aliases, abbreviations, English full names, Chinese names, and common spelling variants.
2. Normalize obvious variants before deciding: case, full-width/half-width punctuation, hyphens, plural forms, Greek-letter spellings, acronym/full-name pairs, and Chinese/English order.
3. If the new term is the same concept as an existing card, update that existing card with a new source backlink and any missing alias. Do not create a second card.
4. If a term has the same surface form but a different meaning, do not merge. Disambiguate with a domain qualifier, e.g. `ACC（前扣带皮层）` versus `ACC（乙酰辅酶A羧化酶）`.
5. If two cards already duplicate the same concept, do not silently add a third card. Report the duplicate and update the most canonical existing card unless the user asks for a manual merge.

Every newly created card should include a compact identity block when aliases or hierarchy matter:

```markdown
## **规范名 / 别名**
- 规范名：
- 别名 / 同义名：
- 不合并：

## **知识层级**
- 所属领域：
- 上级概念：
- 下级概念：
- 同级 / 相关概念：
```

Use these relationships consistently:

- **上级概念**：broader method family, material class, disease category, brain system, algorithm family, or statistical model class.
- **下级概念**：specific subtype, implementation, metric, assay, variant, or named model.
- **同级 / 相关概念**：neighboring concepts that are not parent-child relations.
- **不合并**：nearby names that look similar but must remain separate.

Do not mix the knowledge-card system:

- Keep one primary card location for each canonical concept. Use links for cross-domain relevance instead of duplicating the same card in multiple folders.
- Choose the primary folder by the concept's role in the paper and by the vault's existing convention. For example, `LD score regression` belongs under statistics or genetic-statistical methods, not under the disease folder just because it was used in a disease paper.
- Do not create both a broad parent card and many child cards unless the children are reusable across multiple papers or are technically necessary for understanding the results.
- Link paper notes to the canonical card. When the paper uses an alias, use Obsidian alias display syntax: `[[Canonical Card|surface term in the paper]]`.

## Card Naming

Use concise names that are stable in links:

- English acronym with Chinese full name: `EIS（电化学阻抗谱）`
- Chinese concept with English in parentheses: `螯合（Chelation）`
- Method acronym only when standard and unambiguous: `GWAS`, `LD score regression`
- Material abbreviation when common in the vault: `PVA`, `IP6`, `AA`

Avoid DOI, paper title, or overly long phrase names in card filenames.

## Minimal Card Template

Use this for most cards. Do not add YAML frontmatter unless the user asks for Obsidian Properties.

```markdown
# 名称（Abbreviation / English）

## **规范名 / 别名**
- 规范名：
- 别名 / 同义名：
- 不合并：

## **知识层级**
- 所属领域：
- 上级概念：
- 下级概念：
- 同级 / 相关概念：

## **定义**
一句到三句说明它是什么。

## **核心思想**
说明机制、数学逻辑、材料作用或方法目的。

## **输入 / 输出**
- 输入：
- 输出：

## **关键参数 / 指标**
- 参数1：
- 参数2：

## **适用场景**
- 适用于：
- 不适用于：

## **解释边界**
- 常见误读：
- 需要注意：

## **相关概念**
- [[相关概念1]]
- [[相关方法2]]

# **来源论文 / 应用场景**
1. [[论文笔记标题]]：该论文中如何使用该概念。
```

If a section is irrelevant, omit it rather than filling generic text.

## Statistical Method Card

For statistics cards, include enough context to prevent misuse:

```markdown
# 方法名称（English name）

## **规范名 / 别名**
- 规范名：
- 别名 / 同义名：
- 不合并：

## **知识层级**
- 所属领域：统计方法
- 上级概念：
- 下级概念：
- 同级 / 相关概念：

## **定义**
说明该统计方法回答什么问题。

## **适用问题**
- 研究问题类型：
- 数据类型：
- 常见论文语境：

## **核心假设**
- 假设1：
- 假设2：

## **输入 / 输出**
- 输入：
- 输出：

## **关键结果如何解读**
- 效应量：
- p 值 / 置信区间 / 校正后 p 值：
- 多重比较：

## **常见误读**
- 相关不等于因果。
- 统计显著不等于效应重要。

## **相关方法**
- [[线性回归]]
- [[FDR校正]]

# **来源论文 / 应用场景**
1. [[论文笔记标题]]：该论文中该方法用于什么分析。
```

For clinical, genetic, and neuroimaging papers, prioritize cards for methods such as GWAS, LD score regression, PGS, Mendelian randomization, FDR/FWER correction, mediation analysis, mixed-effects models, Cox regression, logistic regression, permutation testing, and network-based statistics.

## Material Or Chemistry Card

Keep:

- chemical identity and abbreviation
- structure or functional groups when relevant
- properties
- role in materials or devices
- safety/biocompatibility only when paper-relevant
- application backlinks

## Characterization Or Measurement Card

Keep:

- what the method measures
- physical principle
- output data form
- units
- extractable parameters
- what can and cannot be concluded
- typical interpretation in the paper's field

## Paper Note Linking Rules

When producing the paper note:

- Link a card on the first meaningful occurrence in a major section, not every occurrence.
- Link only central reusable concepts.
- Keep the English sentence readable. Prefer `poly(vinyl alcohol) ([[PVA]])` or `GWAS ([[GWAS]])` only when Obsidian mode is requested.
- Link to canonical card titles, not transient aliases. If the source uses a different term, use `[[Canonical Card|source term]]`.
- Do not create broken links for speculative cards unless the user explicitly asks for candidate links.

When producing cards:

- Search for an existing canonical card before writing a new file.
- Always link back to the source paper note under `# **来源论文 / 应用场景**`.
- If multiple papers use the same card, append new numbered entries instead of creating duplicate cards.
- If a card already exists, update it conservatively and preserve user-written content.
- If a concept fits multiple domains, keep one canonical card and add related links rather than copying the card into multiple folders.

## Candidate Selection

Create or suggest a card when at least one is true:

- The term appears repeatedly and is central to the paper's claim or method.
- The term is needed to understand a figure, metric, statistical result, or mechanism.
- The term appears in multiple papers in the vault.
- The user explicitly asks to build a knowledge base from this paper.

Do not create cards for:

- routine nouns that are clear from context
- one-off reagent names not reused
- every figure label
- author names, journals, or institutions
- reference-list-only terms

## Output Modes

For a cards-only request, deliver only the relevant cards and a compact change report. Do not create a bilingual paper note unless the user also requests one.

For a combined paper-note and knowledge-card request, deliver:

1. The main bilingual paper note.
2. A short list of created or suggested cards.
3. The card files themselves if filesystem editing is requested or implied.
4. A short note about merged aliases or skipped duplicates when relevant.

When filesystem editing is not authorized or the target vault is unavailable, provide card candidates in the final response instead of editing files.
