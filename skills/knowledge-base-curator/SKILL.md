---
name: knowledge-base-curator
description: Create, update, deduplicate, and link canonical Obsidian knowledge cards from academic sources. Use for terminology, statistical methods, characterization methods, materials, diseases, brain regions, algorithms, datasets, aliases, hierarchy, backlinks, or vault cleanup when the user asks to 建立知识卡片, 整理专有名词, 整理统计方法, 建立双向链接, Obsidian 知识库整理, merge aliases, deduplicate cards, or curate paper-derived concepts. Preserve user-authored content and keep literature notes separate from reusable concept cards.
---

# Knowledge Base Curator

Use this folder as a self-contained runtime. Preserve existing user-authored vault content.

## Workflow

1. Read `references/knowledge-card-system.md`; also read `references/obsidian-vault-style.md` when working inside a vault.
2. Scan relevant filenames, H1 titles, aliases, abbreviations, translations, and folders before creating or renaming cards.
3. Maintain one canonical card per concept. Merge aliases into it, preserve user-authored content, and disambiguate identical surface forms with domain qualifiers.
4. Record hierarchy and related concepts without duplicating one card across domains. Add a backlink to each supplied source paper or note.
5. Create only reusable concepts requested or central to the source. For a cards-only request, do not create a bilingual paper note.
6. Run `scripts/check_knowledge_cards.py --strict <paths>`, fix conflicts, and report merges or unresolved duplicates.
