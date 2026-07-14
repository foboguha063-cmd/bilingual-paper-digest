# Paper Type Routing

Use this reference before processing unfamiliar disciplines or non-standard article structures.

## Intake

Identify both source type and paper type before drafting:

- Source type: selectable PDF, scanned PDF, publisher HTML, DOI/arXiv page, pasted text, supplementary material, or existing notes.
- Paper type: standard research article, review/perspective, methods/tool paper, resource/dataset paper, clinical/population study, conference paper, materials/engineering performance paper, or short communication.

Do not let the note become a summary. The output remains sentence-level English followed by tab-indented Chinese.

## Standard Research Article

Keep the source order:

`Abstract -> Introduction -> Results / Results and Discussion -> Discussion -> Methods / Experimental Section -> Conclusions`

Translate all substantive prose. Omit references, acknowledgements, author contributions, and figure/table bodies unless requested.

## Review Or Perspective

Preserve thematic headings instead of forcing IMRaD.

- Move Box/sidebar content to the end.
- Keep conceptual definitions only when they appear as ordinary prose.
- Omit standalone Glossary sections unless the user explicitly asks for them.
- Retain review-style cross-references such as `BOX 1`, `FIG. 2`, and `TABLE 1` inside prose sentences.

## Methods Or Tool Paper

Keep enough methods detail for reuse:

- Preserve algorithm, protocol, data-processing, parameter, software, and validation details.
- Preserve equations, pseudocode descriptions, datasets, baselines, and metrics.
- Do not collapse method steps into high-level Chinese summaries.

## Resource Or Dataset Paper

Keep the evidence chain around:

- cohort/sample/source description
- data-generation workflow
- quality control
- accessibility/repository statements when central to reuse
- validation and benchmark results

Omit full data-availability boilerplate only if it is not needed for understanding the resource.

## Clinical Or Population Study

Preserve:

- participant or cohort definition
- inclusion/exclusion logic
- endpoints, phenotypes, covariates, statistical models, confidence intervals, and effect sizes
- ethics or consent details only when central to interpreting the work

Translate cautiously. Do not turn association language into causal language.

## Materials, Chemistry, Engineering, And Device Papers

Preserve:

- composition, synthesis/fabrication, processing conditions, and sample names
- characterization methods and units
- mechanical/electrical/biological performance metrics
- control samples and comparison baselines
- application demonstrations

Use existing material/concept wiki links only when Obsidian mode is requested.

## Conference Or AI/Algorithm Paper

Preserve:

- task definition, datasets, model names, loss/objective, training/evaluation setup
- baselines, ablations, metrics, and statistical or benchmark claims
- limitations and failure cases

Keep math notation and code identifiers intact.

## Extraction Failure Handling

If PDF extraction is weak:

- inspect rendered pages for title, author notes, section order, citations, boxes, and paragraph boundaries
- mark uncertain citation placement rather than silently guessing
- keep a short final note in chat about unresolved extraction risks

If the paper is too long:

- process section by section into the same Markdown file
- mark unprocessed sections clearly
- do not switch to summary-only mode
