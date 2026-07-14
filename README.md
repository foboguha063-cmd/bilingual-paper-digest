# bilingual-paper-digest

面向学术资料的中英双语 Markdown Skill 套件。它把论文、PDF 书籍或章节整理为逐句对照的忠实译文，也可按需维护 Obsidian 文献笔记与知识卡片。

## 安装

```bash
git clone https://github.com/foboguha063-cmd/bilingual-paper-digest.git
cd bilingual-paper-digest
python3 scripts/install_skill.py
```

安装器默认写入 `$CODEX_HOME/skills` 或 `~/.codex/skills`，并安装四个入口：

| 入口 | 用途 |
|---|---|
| `bilingual-paper-digest` | 总路由、组合任务、续译与质量检查 |
| `bilingual-paper-reader` | 论文、综述、预印本、DOI 或正文的双语笔记 |
| `bilingual-book-reader` | PDF 书籍、章节、学位论文和长报告翻译 |
| `knowledge-base-curator` | Obsidian 知识卡片、别名合并、去重与双向链接 |

只安装根入口：

```bash
python3 scripts/install_skill.py --no-companions
```

彻底替换旧安装（包括可选 `.venv`）：

```bash
python3 scripts/install_skill.py --clean
```

普通更新会同步 Skill 运行文件、清除旧版嵌套 companions，并保留已安装的 `.venv`。

## 使用

安装后重启 Codex，直接使用自然语言：

```text
使用 bilingual-paper-reader 整理这篇论文。
使用 bilingual-book-reader 翻译这本 PDF 书的第 1 章。
使用 knowledge-base-curator 从这篇文献建立 Obsidian 知识卡片。
使用 bilingual-paper-digest 检查这份双语笔记是否漏译。
```

默认产物是纯文本 Markdown：每句英文原文后紧跟一行制表符缩进的中文翻译；同一原文段落内不插空行，不同原文段落之间保留清晰间隔。Skill 保留原文顺序、限定语、否定、数据、单位、统计结果、技术细节和引用位置，不用总结替代未完成的翻译。

图片、表格、图注、Glossary、致谢、作者贡献、利益冲突、出版商声明和完整参考文献默认省略；用户明确要求时再处理。

## 轻量结构

```text
SKILL.md                              # 总路由与默认流程
agents/openai.yaml                    # UI 元数据
references/
  bilingual-output-contract.md        # 唯一的双语输出权威契约
  paper-type-routing.md               # 非标准论文类型路由
  book-translation-mode.md            # 书籍/章节组织与续译
  pdf-extraction-pipeline.md           # 复杂 PDF 抽取
  translation-memory.md               # 哈希缓存与续译
  obsidian-vault-style.md              # Vault 路径、链接和媒体规则
  knowledge-card-system.md             # 知识卡片、层级与去重
scripts/                               # 抽取、缓存和验证运行脚本
companions/                            # 三个窄入口的仓库源码
examples/                              # 仅供回归测试，不进入安装结果
```

根 `SKILL.md` 只做路由；每个任务仅加载对应参考文件。安装器不会把 README、CI、测试样例、安装器、仓库检查脚本或嵌套 companion 源码复制进根 Skill。

## 可选 PDF 环境

基础使用不要求本仓库自带虚拟环境。处理复杂版式、长书或需要结构化抽取时可安装轻量依赖：

```bash
python3 scripts/install_skill.py --with-env light
```

需要 Docling 时：

```bash
python3 scripts/install_skill.py --with-env docling
```

检查本机 PDF、OCR、GROBID 和长文档能力：

```bash
python3 scripts/probe_tools.py
```

扫描件仍需操作系统层面的 OCRmyPDF 与 Tesseract；它们不会由 Skill 自动安装。

## 开发检查

修改 Skill、参考资料、脚本、样例或安装器后运行：

```bash
python3 scripts/run_checks.py
```

该检查验证 frontmatter、引用路径、Python 语法、双语样例、知识卡片、翻译缓存、源文对齐，以及轻量安装结果。

## 与 nature-reader 的边界

`nature-reader` 适合生成带来源锚点、图文对应和 assets 的完整论文 reader；`bilingual-paper-digest` 默认生成紧凑、纯文本、逐句对照的双语 Markdown。
