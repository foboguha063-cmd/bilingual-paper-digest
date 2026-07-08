# bilingual-paper-digest

`bilingual-paper-digest` 是一个面向学术论文阅读笔记的中英文双语整理 skill。它把 PDF、DOI、论文正文、预印本、会议论文或补充材料整理为紧凑的 Markdown 文献笔记，适用于研究论文、综述、方法论文、临床研究、材料与工程论文等多数常见学术文献。

## 安装

推荐使用仓库自带安装脚本。它会把 skill 安装到 `$CODEX_HOME/skills` 或 `~/.codex/skills`，并自动排除 `.git`、`.venv`、PDF 抽取缓存等不应复制的文件：

```bash
git clone https://github.com/foboguha063-cmd/bilingual-paper-digest.git
cd bilingual-paper-digest
python3 scripts/install_skill.py
```

如果希望同时安装轻量 PDF 处理环境：

```bash
python3 scripts/install_skill.py --with-env light
```

手工安装也可以：

```bash
mkdir -p ~/.codex/skills
rsync -a --delete --exclude='.git' --exclude='.venv' --exclude='.bilingual-paper-digest' bilingual-paper-digest/ ~/.codex/skills/bilingual-paper-digest/
```

可选：在当前仓库中安装轻量 PDF 增强环境，用于更稳定的 PDF 抽取、分块和 token 估算：

```bash
python3 scripts/setup_environment.py --profile light
.venv/bin/python scripts/probe_tools.py
```

若只想检查当前机器可用能力：

```bash
python3 scripts/probe_tools.py
```

安装后重启 Codex，使用类似下面的自然语言触发：

```text
按照 bilingual-paper-digest 整理这篇文献。
```

## 功能

该 skill 会生成符合训练格式的 Markdown 文献笔记，包含：

- 无单独 `题录简介` 的题名和题录头部。
- 只统计通讯作者的团队行，并按机构所在地区决定是否标注英文机构名。
- 每句英文原文后紧跟一行制表符缩进的中文学术翻译。
- 忠实保留原文句序、段落顺序、限定语、否定、数据、单位、统计结果和技术细节，不把段落改写成总结。
- 保留原文引用编号位置，并把抽取出的上标编号统一整理为 `[1]` 这类形式。
- 同一原文段落内句对之间不空行，不同原文段落之间保留清晰空行。
- Box 类旁栏内容统一移动到文档末尾。
- Obsidian 模式下按目标 vault 的文件夹、wiki 链接和 `figure/` 资源约定处理。
- 可选生成专有名词、统计方法、表征方法、材料/试剂、疾病/脑区/算法等知识卡片，并建立论文笔记与知识卡片之间的双向链接。
- 知识卡片使用规范名、别名、上下级关系和来源论文回链，建卡前需扫描既有卡片，避免同一概念重复建卡或跨文件夹混杂。
- 按论文类型调整章节处理策略，覆盖研究论文、综述、方法、资源/数据集、临床/人群研究、会议论文等。
- 可选使用结构化 PDF 管线，将 PDF 预先抽取为 `.bilingual-paper-digest/source.jsonl` 和 `translation_units.jsonl`，减少重复 token 消耗并提高对齐检查能力。
- 可选使用 `translation_cache.jsonl` 复用已检查译文，并用源文对齐脚本检查漏译。
- 提供 `scripts/check_digest.py` 对双语句对、段落空行、禁用章节、图片嵌入和 Box 位置进行格式质检；提供 `scripts/check_knowledge_cards.py` 检查知识卡片标题重复和别名冲突。

## 主要产物

- 一个 `.md` 文献笔记文件，默认写入用户当前工作文件夹或用户指定路径。

除非用户明确要求，该 skill 不整理图片、图表、图注、表格正文、Glossary、致谢、作者贡献、利益冲突、出版商声明或完整参考文献列表。若用户明确要求 Obsidian 图文集成，则资源应放在对应笔记目录的 `figure/` 文件夹中，并用 Obsidian `![[...]]` 语法引用。

## 触发短语

当用户提出以下需求时使用该 skill：

- 整理文献
- 整理为上述格式
- 尚书格式
- 双语整理
- 原文+中文翻译
- 按照这个 Skill 整理这篇文献
- 翻译并整理这本 PDF 书
- 从这篇文献建立 Obsidian 知识卡片
- trained bilingual Markdown paper notes

给其他使用者时，可以只让他们使用这些最短提示：

```text
使用 bilingual-paper-digest 整理这篇论文。
```

```text
使用 bilingual-paper-digest 翻译并整理这本 PDF 书的第 1 章。
```

```text
使用 bilingual-paper-digest 从这篇文献中建立 Obsidian 知识卡片。
```

## 格式规则

每一句英文原文后必须立即跟对应中文翻译，中文行使用制表符缩进。同一原文自然段内的句对之间不插入空行；不同原文自然段之间至少保留两个空行。

团队行只列通讯作者。中国境内大学或研究机构只写中文最高级机构名；非中国境内机构写中文机构名并在括号中保留官方英文名。国外学者不额外音译中文姓名；中国学者应尽量写中文姓名。

## 资源结构

```text
references/obsidian-vault-style.md  # Obsidian 文献库规则
references/knowledge-card-system.md # 术语/方法/统计知识卡片规则
references/paper-type-routing.md    # 不同论文类型的整理策略
references/pdf-extraction-pipeline.md # PDF 抽取与工具路由
references/book-translation-mode.md # PDF 书籍/长文档翻译模式
references/translation-memory.md    # 术语注入、缓存与续译规则
references/environment-and-sharing.md # 新机器安装与共享使用说明
references/skill-suite-routing.md   # 总 Skill 与论文/书籍/知识库模块路由
references/improvement-roadmap.md   # 后续改进点与优先级
examples/minimal-paper-note.md      # 纯文本标准样例
examples/obsidian-material-note.md  # Obsidian 材料论文样例
examples/knowledge-card-term.md     # 专有名词知识卡样例
examples/knowledge-card-statistics.md # 统计方法知识卡样例
scripts/setup_environment.py        # 创建轻量可选运行环境
scripts/install_skill.py            # 安装/更新到本机 Codex skills 目录
scripts/probe_tools.py              # 检测 PDF/OCR/书籍模式可用能力
scripts/extract_pdf_structure.py    # PDF -> source.jsonl/source_map.json
scripts/build_translation_units.py  # source.jsonl -> translation_units.jsonl
scripts/translation_cache.py        # 翻译缓存复用、更新和统计
scripts/check_source_alignment.py   # 结构化源文与 Markdown 对齐检查
scripts/check_digest.py             # 格式质检脚本
scripts/check_knowledge_cards.py    # 知识卡片去重与别名冲突检查
```

## 与 `nature-reader` 的区别

`nature-reader` 适合生成带来源锚点、图文对应和 assets 的完整论文 reader。`bilingual-paper-digest` 只负责生成用户训练过的紧凑双语 Markdown 文献笔记。
