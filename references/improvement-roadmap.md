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
- `scripts/check_digest.py` for basic format QA.
- `scripts/check_knowledge_cards.py` for duplicate-title and alias-conflict QA.

## High-Priority Improvements

1. **Source map sidecar**
   Add optional `source_map.json` with section, page, paragraph index, extraction confidence, citation markers, and output line ranges. This borrows the strongest traceability idea from full-paper reader workflows without changing the compact Markdown format.

2. **Metadata extraction helper**
   Add a script that extracts title, DOI, journal, publication dates, article type, author notes, corresponding authors, emails, and affiliations from PDF/HTML text. This would reduce manual errors in the header and team line.

3. **Citation normalization helper**
   Add deterministic cleanup for common PDF extraction forms such as `pain3-5`, `study50`, `(REF. 23)`, `12,13`, superscripts, and author-year references.

4. **Paper-type regression examples**
   Add one small fixture each for review, methods/tool paper, clinical/population study, resource/dataset paper, and materials/device paper. Use them to keep the skill general beyond one field.

5. **Checker expansion**
   Extend `check_digest.py` to detect:
   - non-tab Chinese lines after English lines
   - accidental sentence-pair blank lines
   - reference-list leakage
   - misplaced Box sections
   - invalid or overused Obsidian wiki links
   - missing team/DOI/article-type header fields
   - stronger source-to-output sentence-count drift when a source map is available

6. **Uncertainty notes**
   Add an optional compact `整理说明` section or sidecar file for extraction uncertainty, missing pages, OCR failures, or unresolved corresponding-author ambiguity. Keep it out of the paper note unless requested.

## Medium-Priority Improvements

7. **Obsidian knowledge-link suggester**
   Add a script that scans an Obsidian vault for existing note names and suggests restrained wiki links for recurring materials, statistical methods, characterization methods, diseases, brain regions, datasets, or algorithms.

8. **Batch mode**
   Add a workflow for processing multiple PDFs into one folder with consistent filenames, DOI collision checks, and a summary index.

9. **Supplementary-material policy**
   Define when supplementary methods/results should be appended, summarized, or omitted. Current behavior is conservative but not yet explicit enough for long supplement packages.

10. **Terminology memory**
    Add optional generated term tables per domain so repeated abbreviations, material names, neuroscience terms, and card aliases remain consistent across papers. The table should point to canonical cards rather than replacing the card system.

11. **Knowledge-card extraction helper**
    Add a script that proposes candidate cards from a finished paper note, grouped by term type: material, concept, characterization method, statistical method, disease/brain region, dataset, and algorithm.

## Lower-Priority Improvements

12. **DOCX export**
    Provide optional conversion from Markdown to DOCX while preserving bilingual line pairing for users who need Word review.

13. **HTML preview**
    Provide an optional browser preview only as a secondary artifact. The Markdown file should remain primary.

14. **GitHub CI**
    Add a lightweight CI workflow to run `quick_validate.py` and `check_digest.py` on examples whenever the repository changes.

## Design Constraints

- Do not turn this skill into a full `nature-reader` clone. Its core value is compact sentence-level bilingual notes.
- Do not make figure/table extraction default. Keep it opt-in.
- Do not require a specific local vault path in public-facing docs.
- Do not overfit to one discipline; use paper type and source structure to adapt.
