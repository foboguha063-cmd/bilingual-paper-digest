# bilingual-paper-digest

`bilingual-paper-digest` 是一个面向用户固定文献笔记格式的中英文双语整理 skill。它把 PDF、DOI、论文正文或补充材料整理为紧凑的 Markdown 文献笔记，并可按 `/Users/jisufeima/Documents/文献库` 的 Obsidian 文献库体系写入材料或医学论文笔记目录。

## 安装

把整个仓库目录复制到 Codex skills 目录即可：

```bash
mkdir -p ~/.codex/skills
cp -R bilingual-paper-digest ~/.codex/skills/
```

如果是从 GitHub 克隆：

```bash
git clone <your-repo-url> bilingual-paper-digest
cp -R bilingual-paper-digest ~/.codex/skills/
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
- 保留原文引用编号位置，并把抽取出的上标编号统一整理为 `[1]` 这类形式。
- 同一原文段落内句对之间不空行，不同原文段落之间保留清晰空行。
- Box 类旁栏内容统一移动到文档末尾。
- Obsidian 模式下按现有 `材料论文及笔记`、`医学论文及笔记`、`材料知识库` 体系处理路径、wiki 链接和 `figure/` 资源约定。
- 提供 `scripts/check_digest.py` 对双语句对、段落空行、禁用章节、图片嵌入和 Box 位置进行格式质检。

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
- trained bilingual Markdown paper notes

## 格式规则

每一句英文原文后必须立即跟对应中文翻译，中文行使用制表符缩进。同一原文自然段内的句对之间不插入空行；不同原文自然段之间至少保留两个空行。

团队行只列通讯作者。中国境内大学或研究机构只写中文最高级机构名；非中国境内机构写中文机构名并在括号中保留官方英文名。国外学者不额外音译中文姓名；中国学者应尽量写中文姓名。

## 资源结构

```text
references/obsidian-vault-style.md  # Obsidian 文献库规则
examples/minimal-paper-note.md      # 纯文本标准样例
examples/obsidian-material-note.md  # Obsidian 材料论文样例
scripts/check_digest.py             # 格式质检脚本
```

## 与 `nature-reader` 的区别

`nature-reader` 适合生成带来源锚点、图文对应和 assets 的完整论文 reader。`bilingual-paper-digest` 只负责生成用户训练过的紧凑双语 Markdown 文献笔记。
