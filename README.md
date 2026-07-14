# bilingual-paper-digest

> Source-faithful English–Chinese academic reading, long-document translation, and Obsidian knowledge curation for Agent Skills.

`bilingual-paper-digest` 是一个轻量、可追溯、可恢复的学术双语工作流套件。它面向论文、综述、预印本、书籍、学位论文、长报告和学术知识库，将来源内容整理为保留英文原文的逐句中英对照 Markdown。

它的主要目标不是“快速总结”，而是尽可能维持原文的句子、段落、章节、限定语、否定、数字、单位、统计量、科研标识符和引用位置，并通过确定性脚本暴露漏译、错序和常见数据漂移。

- 当前版本：`1.0.0`
- 规范结构：标准 `skills/<skill-name>/SKILL.md`
- 默认产物：纯文本、逐句对照的 Markdown
- 默认依赖：无；PDF 处理环境按需安装
- 已验证平台：Codex；通用安装器可发现全部四个 Skill

## 主要功能

### 1. 学术论文逐句双语阅读

`bilingual-paper-reader` 用于普通研究论文、综述、方法论文、临床研究、材料与工程论文、会议论文和预印本。

支持输入：

- PDF 文件；
- DOI、出版社页面或预印本页面；
- 用户粘贴的正文；
- 已抽取的 Markdown、文本或 JSONL 单元；
- 需要继续或审计的既有双语笔记。

默认输出：

- 保留英文题名、中文题名、团队、DOI、期刊和发表信息；
- 每个英文原句后紧跟一个制表符缩进的中文译文；
- 保持来源段落、章节标题和论证顺序；
- 不用总结替代未完成的正文；
- 图片、表格、图注、完整参考文献和独立术语表仅在明确请求时加入。

### 2. 书籍与长文档可恢复翻译

`bilingual-book-reader` 用于 PDF 书籍、专著、教材、标准、学位论文、长报告以及指定章节或页码范围。

长文档工作流会：

- 固定用户指定的章节、页码或部分，不静默扩大范围；
- 将来源拆分为带稳定 ID 和 source hash 的句级单元；
- 只导出尚未翻译的有限批次；
- 按 ID 和 source hash 合并译文，防止批次覆盖或错位；
- 只渲染完整段落；
- 保留未完成状态，支持下次继续；
- 绝不使用章节摘要填补未翻译正文。

### 3. Obsidian 学术知识卡片

`knowledge-base-curator` 将论文或笔记中的可复用概念整理为规范知识卡片，包括：

- 专业术语和别名；
- 统计方法；
- 表征与测量方法；
- 材料、化学体系、疾病和脑区；
- 算法、模型和数据集；
- 层级关系、相关概念和来源反链。

它会先扫描已有文件名、H1、aliases、缩写和翻译，维持“一项概念、一张规范卡片”，并尽量合并重复卡片而不是继续制造别名文件。用户已经写入的内容应被保留，文献笔记和通用知识卡片保持为不同类型的产物。

### 4. 组合任务、续译与审计

`bilingual-paper-digest` 是总路由入口，适合以下情况：

- 同一请求同时需要双语论文笔记和知识卡片；
- 长文档需要分批、续译或恢复；
- 既有双语笔记需要检查漏译、重复、错序或数据漂移；
- 需要在论文、书籍、Obsidian 和知识卡片工作流之间协调；
- 用户明确指定 `$bilingual-paper-digest`。

单篇普通论文、单本书或单纯知识卡片任务，应优先调用对应的窄入口，以减少无关上下文。

## 四个 Skill

| Skill | 适用场景 | 主要产物 | 主要验证 |
|---|---|---|---|
| `bilingual-paper-reader` | 论文、综述、预印本、DOI、正文、双语笔记审计 | 单篇逐句双语 Markdown | 格式、数据一致性、来源覆盖与顺序 |
| `bilingual-book-reader` | 书籍、章节、学位论文、标准、长报告 | 章节化、可续译的双语 Markdown | 批次 ID/hash、完整段落、来源对齐 |
| `knowledge-base-curator` | Obsidian 卡片、术语、统计方法、别名、反链 | 规范概念卡片与链接 | 重复身份、层级和必要字段 |
| `bilingual-paper-digest` | 组合任务、续译、批处理、质量审计 | 多工作流协调结果 | 按产物组合相应检查器 |

每个 Skill 都是自包含目录，可以独立安装；它们不再依赖相邻 sibling Skill 才能运行。

## 输出契约

正文采用“一个完整英文原句 + 一个直接对应的中文译文”：

```markdown
# Abstract
The intervention did not reduce mortality at 28 days [1-3].
	该干预并未降低28天死亡率[1-3]。
However, the confidence interval remained wide.
	然而，置信区间仍然较宽。


The secondary analysis included 245 participants.
	次要分析纳入了245名参与者。
```

核心约束：

- 不按 PDF 视觉换行切句；
- 不合并多个英文句子为一个中文总结；
- 保留否定、限定范围、不确定性和语气强度；
- 保留样本量、剂量、时间点、单位、统计量和实验条件；
- 保留引用在相应短语或分句附近的位置；
- 不擅自添加“核心发现”“临床意义”等来源中不存在的分析标题；
- 无法完成时停在最后一个完整段落，并在笔记外报告剩余范围。

详细格式由各 Skill 的 `references/bilingual-output-contract.md` 定义。

## 精准性与质量检查

套件使用多层验证，不把“格式正确”误称为“翻译语义已经证明正确”。

| 检查器 | 检查内容 | 不能证明的内容 |
|---|---|---|
| `check_digest.py` | 英中行对应、缩进、段落间隔、禁止标题、默认媒体规则 | 中译文是否准确表达原义 |
| `check_bilingual_quality.py` | 数字、单位、引用、比较符号、否定标记、希腊字母、科研标识符 | 上下文歧义、术语选择和完整语义等价 |
| `check_source_alignment.py` | 来源句是否遗漏、重复或错序 | 中文译文的文风和专业判断 |
| `check_knowledge_cards.py` | 卡片身份冲突、别名、层级和必要字段 | 概念关系是否具有领域权威性 |

最终交付仍需人工或模型复核：

- 专业术语在具体学科中的译法；
- 否定范围、因果关系和比较对象；
- PDF 多栏、脚注、公式和侧栏的抽取顺序；
- OCR 产生的字符错误；
- 自动脚本无法判断的语义遗漏。

## 可恢复流水线

普通、文本清晰的短论文可以直接翻译。复杂 PDF、书籍、批处理或需要审计的任务使用结构化流水线：

```text
PDF / source text
    ↓
source.jsonl                 reusable source blocks
    ↓
translation_units.jsonl      sentence units + paragraph IDs + source hashes
    ↓
translation cache            exact checked reuse
    ↓
pending-batch.jsonl          bounded untranslated batch
    ↓
merge by unit ID/hash        safe resume without overwriting source
    ↓
deterministic quality check
    ↓
Markdown renderer            complete output or complete-paragraph prefix
    ↓
source alignment check
```

严格渲染模式在出现未翻译单元时拒绝生成最终文件；`--partial` 只输出第一个未完成段落之前的完整前缀。

## PDF 与来源路由

套件按照“最轻但足够可靠”的原则选择抽取方式：

| 来源情况 | 默认路径 |
|---|---|
| 可复制文字的普通论文 PDF | PyMuPDF4LLM，失败后回退到 pdfplumber 或 pypdf |
| 双栏、版式复杂或 Markdown 结构重要 | PyMuPDF4LLM，并检查 `source.jsonl` 顺序 |
| 扫描 PDF | 先用 OCRmyPDF/Tesseract OCR，再进入普通抽取流程 |
| 元数据要求高的学术论文 | 在可用时使用 GROBID；普通抽取不强制依赖它 |
| 长书、学位论文或复杂报告 | 轻量抽取，或显式选择可选 Docling 路径 |

抽取清单会记录：

- 来源文件；
- 使用的抽取方法；
- 页数和选定页码；
- 文本块数和字符数；
- PDF 元数据；
- 检测到的 DOI；
- 疑似扫描件或文本不完整风险；
- 回退过程和错误信息。

来源文档、网页内容、元数据和缓存均被视为不可信数据；Skill 不会执行嵌入在来源中的指令。

## 快速安装

使用开放 Agent Skills CLI 查看仓库中的四个 Skill：

```bash
npx skills add foboguha063-cmd/bilingual-paper-digest --list
```

安装单篇论文入口到 Codex：

```bash
npx skills add foboguha063-cmd/bilingual-paper-digest \
  --skill bilingual-paper-reader \
  -g -a codex -y
```

安装全部 Skill：

```bash
npx skills add foboguha063-cmd/bilingual-paper-digest \
  --skill '*' \
  -g -a codex -y
```

更新已安装 Skill：

```bash
npx skills update bilingual-paper-reader -g -y
```

仓库使用标准 Agent Skills 目录布局，可被 [Vercel Skills CLI](https://github.com/vercel-labs/skills) 发现。当前自动化验证主要针对 Codex；其他实现同一 Skill 规范的 Agent 应自行运行对应的安装与行为测试。

## 本地安装器

克隆仓库后，也可以使用不依赖 Node.js 的本地安装器：

```bash
git clone https://github.com/foboguha063-cmd/bilingual-paper-digest.git
cd bilingual-paper-digest
python3 scripts/install_skill.py
```

常用选项：

```bash
# 只安装一个入口
python3 scripts/install_skill.py --skill bilingual-book-reader

# 只安装总路由入口
python3 scripts/install_skill.py --no-companions

# 彻底替换，包括旧的可选 .venv
python3 scripts/install_skill.py --clean

# 安装轻量 PDF 环境
python3 scripts/install_skill.py --with-env light

# 安装可选 Docling 环境
python3 scripts/install_skill.py --with-env docling
```

普通更新会同步 Skill 文件、删除旧文件并保留已有 `.venv`。

## 使用示例

安装后重启 Agent，然后直接使用自然语言或显式 Skill 名称：

```text
使用 $bilingual-paper-reader 将这篇论文整理为逐句中英对照 Markdown，并检查数字和引用。

使用 $bilingual-book-reader 翻译这本 PDF 的第 3 章，从上次未完成的位置继续。

使用 $knowledge-base-curator 从这篇论文建立统计方法和材料知识卡片，并合并已有别名。

使用 $bilingual-paper-digest 审计这份双语笔记是否漏译，再把核心术语链接到现有 Obsidian 卡片。
```

如果用户只需要三句话摘要，而不需要原文对照，应使用普通总结工作流，不必触发本套件。

## 轻量化设计

- 四个 `SKILL.md` 合计不足 100 行，只保存路由、核心流程和完成条件；
- 详细格式和变体放入按需读取的 `references/`；
- 重复、脆弱或需要确定性的操作使用纯 Python 脚本；
- 默认不创建虚拟环境；
- 文本或已有 Markdown 工作流不要求第三方 Python 包；
- `light` 配置仅包含 pypdf、pdfplumber 和 pymupdf4llm；
- Docling、OCR 和 GROBID 均为可选增强能力；
- 四个自包含 Skill 的运行文件合计保持在 600 KB 预算以内。

自包含文件通过 `scripts/sync_skills.py` 从总路由运行时同步，并由测试检查字节一致性，减少多份副本漂移。

## 仓库结构

```text
skills/
  bilingual-paper-digest/       # 总路由、全部 references 与运行时
  bilingual-paper-reader/       # 独立论文双语入口
  bilingual-book-reader/        # 独立长文档入口
  knowledge-base-curator/       # 独立知识卡片入口
scripts/
  install_skill.py              # Codex 本地安装与更新
  sync_skills.py                # 同步自包含运行文件
  run_checks.py                 # 全量结构与行为回归
examples/                       # 输出格式与知识卡片样例
tests/                          # 黄金输出和 PDF fixture
evals/                          # 后续行为级前向测试场景
VERSION                         # 语义版本
```

## 测试与验证

修改 Skill、reference、脚本、安装器或样例后运行：

```bash
python3 scripts/sync_skills.py
python3 scripts/run_checks.py
npx skills add . --list
```

当前回归覆盖：

- 四个 Skill 的 frontmatter、名称、描述和 UI 元数据；
- reference 路径和自包含文件同步；
- Python 语法；
- 学术缩写、小数、`et al.`、`U.S.` 和句界；
- 黄金双语 Markdown 输出；
- 错误数字、漏引用和否定反转的失败案例；
- translation cache、批次导出、hash 合并和中断恢复；
- 严格渲染与完整段落前缀；
- 真实文本 PDF、DOI 和 PDF 元数据抽取；
- 全套安装、单 Skill 安装、更新及 `.venv` 保留；
- 600 KB 自包含运行预算；
- GitHub Actions 自动检查。

## 能力边界

- 确定性检查可以发现明显不一致，但不能证明翻译在所有学科语境下完全正确；
- 扫描件必须先经过 OCR，低质量 OCR 仍需人工核对；
- 双栏、复杂公式、脚注、Box 和侧栏可能需要检查渲染页面；
- 图片、表格、图注、完整参考文献、致谢和出版商声明默认省略；
- 需要图文对应、逐块来源锚点和完整 assets 的 reader，可考虑使用 `nature-reader`；
- 尚未把行为评估场景接入多代理自动前向测试。

这些限制会被明确报告，不会用看似完整的总结掩盖未处理范围。
