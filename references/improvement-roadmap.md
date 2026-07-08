# Improvement Roadmap

This roadmap records improvements still worth making after comparing this skill with robust paper-processing skills such as full-paper readers, presentation builders, and academic writing/polishing workflows.

## Implemented

- Sentence-level English-Chinese alignment with tab-indented Chinese lines.
- Explicit fidelity constraints against paragraph compression, review-style paraphrase, invented analytic headings, and unfinished-section summaries.
- Paragraph spacing rule: no blank line within one source paragraph, at least two blank lines between source paragraphs.
- Citation marker preservation near the original phrase.
- Corresponding-author-only team line.
- Obsidian-compatible reference for vault folder, wiki-link, and figure conventions.
- Knowledge-card system for terminology, statistical methods, characterization methods, materials, and bidirectional Obsidian links.
- Knowledge-card deduplication rules for canonical names, aliases, hierarchy, domain boundaries, and merge decisions.
- Minimal examples for text-only and Obsidian-linked outputs.
- Lightweight environment setup and probing scripts for shared installations.
- Structured PDF extraction scripts that create reusable `source.jsonl`, `source_map.json`, and `translation_units.jsonl` artifacts.
- `scripts/check_digest.py` for basic format QA.
- `scripts/check_knowledge_cards.py` for duplicate-title and alias-conflict QA.

## High-Priority Improvements

1. **Metadata extraction helper**
   Add a script that extracts title, DOI, journal, publication dates, article type, author notes, corresponding authors, emails, and affiliations from PDF/HTML text. This would reduce manual errors in the header and team line.

2. **Citation normalization helper**
   Add deterministic cleanup for common PDF extraction forms such as `pain3-5`, `study50`, `(REF. 23)`, `12,13`, superscripts, and author-year references.

3. **Paper-type regression examples**
   Add one small fixture each for review, methods/tool paper, clinical/population study, resource/dataset paper, and materials/device paper. Use them to keep the skill general beyond one field.

4. **Checker expansion**
   Extend `check_digest.py` to detect:
   - non-tab Chinese lines after English lines
   - accidental sentence-pair blank lines
   - reference-list leakage
   - misplaced Box sections
   - invalid or overused Obsidian wiki links
   - missing team/DOI/article-type header fields
   - stronger source-to-output sentence-count drift when a source map is available

5. **Uncertainty notes**
   Add an optional compact `整理说明` section or sidecar file for extraction uncertainty, missing pages, OCR failures, or unresolved corresponding-author ambiguity. Keep it out of the paper note unless requested.

## Medium-Priority Improvements

6. **Obsidian knowledge-link suggester**
   Add a script that scans an Obsidian vault for existing note names and suggests restrained wiki links for recurring materials, statistical methods, characterization methods, diseases, brain regions, datasets, or algorithms.

7. **Batch mode**
   Add a workflow for processing multiple PDFs into one folder with consistent filenames, DOI collision checks, and a summary index.

8. **Supplementary-material policy**
   Define when supplementary methods/results should be appended, summarized, or omitted. Current behavior is conservative but not yet explicit enough for long supplement packages.

9. **Terminology memory implementation**
    Add optional generated term tables per domain so repeated abbreviations, material names, neuroscience terms, and card aliases remain consistent across papers. The table should point to canonical cards rather than replacing the card system.

10. **Knowledge-card extraction helper**
    Add a script that proposes candidate cards from a finished paper note, grouped by term type: material, concept, characterization method, statistical method, disease/brain region, dataset, and algorithm.

## Lower-Priority Improvements

11. **DOCX export**
    Provide optional conversion from Markdown to DOCX while preserving bilingual line pairing for users who need Word review.

12. **HTML preview**
    Provide an optional browser preview only as a secondary artifact. The Markdown file should remain primary.

13. **GitHub CI**
    Add a lightweight CI workflow to run `quick_validate.py` and `check_digest.py` on examples whenever the repository changes.

## Design Constraints

- Do not turn this skill into a full `nature-reader` clone. Its core value is compact sentence-level bilingual notes.
- Do not make figure/table extraction default. Keep it opt-in.
- Do not require a specific local vault path in public-facing docs.
- Do not overfit to one discipline; use paper type and source structure to adapt.
