# Knowledge Card System

Use this reference when the user asks to extract terminology, statistical methods, named methods, materials, characterization methods, diseases, brain regions, algorithms, datasets, or reusable concepts from a paper into Obsidian knowledge cards.

## Design Model

Use an atomic-note system inspired by Zettelkasten and Obsidian MOC practice:

- One card explains one concept, method, material, statistic, disease, brain region, algorithm, or dataset.
- Paper notes are the evidence trail. Knowledge cards are reusable concept nodes.
- The bidirectional link must be explicit: the paper note links to the card, and the card links back to the paper note under `# **来源论文 / 应用场景**`.
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
- Do not create broken links for speculative cards unless the user explicitly asks for candidate links.

When producing cards:

- Always link back to the source paper note under `# **来源论文 / 应用场景**`.
- If multiple papers use the same card, append new numbered entries instead of creating duplicate cards.
- If a card already exists, update it conservatively and preserve user-written content.

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

When the user asks for knowledge cards, deliver:

1. The main bilingual paper note.
2. A short list of created or suggested cards.
3. The card files themselves if filesystem editing is requested or implied.

When unsure whether to create files, provide a `# 知识卡片候选` section in the final chat response rather than editing the vault.
