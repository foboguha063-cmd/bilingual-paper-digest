---
name: knowledge-base-curator
description: Build, update, deduplicate, and link Obsidian knowledge cards from academic papers, notes, terminology lists, statistical methods, characterization methods, materials, diseases, brain regions, algorithms, datasets, or reusable concepts. Use when the user asks to 建立知识卡片, 整理专有名词, 整理统计方法, 建立双向链接, Obsidian 知识库整理, merge aliases, deduplicate cards, or curate paper-derived concept cards.
---

# Knowledge Base Curator

Use this companion skill as the narrow entry point for Obsidian knowledge-card work. It shares the installed sibling root skill at `../bilingual-paper-digest`; if that folder is missing, ask the user to install the repository with `scripts/install_skill.py`.

## Shared Resources

- Read `../bilingual-paper-digest/references/knowledge-card-system.md` before creating, updating, merging, or linking cards.
- Read `../bilingual-paper-digest/references/obsidian-vault-style.md` when working inside a local Obsidian vault or deciding filenames, folders, and wiki-link style.
- Read `../bilingual-paper-digest/SKILL.md` only if the task also requires a bilingual paper note.
- Run `../bilingual-paper-digest/scripts/check_knowledge_cards.py --strict <card-files-or-root>` after creating or updating cards when filesystem access is available.

## Workflow

1. Scan the target vault or card folders before creating cards. Check filenames, H1 titles, aliases, and related folders.
2. Create one canonical card per concept. Put alternate names, abbreviations, spelling variants, and Chinese/English variants in aliases instead of making duplicates.
3. Mark parent/child relationships for hierarchical concepts, and link cross-domain concepts instead of mixing unrelated card systems.
4. Keep paper notes and knowledge cards distinct. Literature notes cite and translate a paper; knowledge cards define reusable concepts and link back to source papers.
5. Create cards only for reusable terms, methods, materials, statistical approaches, datasets, algorithms, diseases, brain regions, or characterization methods.
6. Add source backlinks to the originating paper note or source file.
7. If a candidate concept conflicts with an existing card, update or propose merging into the canonical card instead of creating a new one.
