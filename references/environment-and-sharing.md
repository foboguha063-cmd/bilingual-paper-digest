# Environment And Sharing

Use this reference when installing the skill on a new machine, preparing it for another user, or diagnosing why PDF extraction quality differs between machines.

## Installation Model

Keep the skill portable:

- Commit only scripts, references, examples, and small requirement files.
- Do not commit `.venv/`, extracted PDF caches, OCR outputs, or translated work products.
- Install optional runtime dependencies into a local `.venv/` or another user-controlled environment.
- Treat heavy tools such as OCRmyPDF, Tesseract, Docling, and GROBID as optional capabilities, not required baseline dependencies.

## Quick Start For Another User

After cloning the skill:

```bash
git clone https://github.com/foboguha063-cmd/bilingual-paper-digest.git
cd bilingual-paper-digest
python3 scripts/install_skill.py --with-env light
```

This installs the root `bilingual-paper-digest` skill plus the companion entry-point skills `bilingual-paper-reader`, `bilingual-book-reader`, and `knowledge-base-curator`. Restart Codex and ask:

```text
使用 bilingual-paper-reader 整理这篇论文。
```

The root `SKILL.md` is intentionally short. Detailed output rules live in `references/source-faithful-bilingual-format.md` and `references/translation-fidelity-checklist.md`, so ordinary routing loads fewer tokens while paper/book tasks still get the strict bilingual formatting contract.

If the user wants to inspect environment capability in the installed copy:

```bash
~/.codex/skills/bilingual-paper-digest/.venv/bin/python ~/.codex/skills/bilingual-paper-digest/scripts/probe_tools.py
```

Manual fallback:

```bash
mkdir -p ~/.codex/skills
rsync -a --delete --exclude='.git' --exclude='.venv' --exclude='.bilingual-paper-digest' bilingual-paper-digest/ ~/.codex/skills/bilingual-paper-digest/
cd ~/.codex/skills/bilingual-paper-digest
python3 scripts/setup_environment.py --profile light
```

## Profiles

- `light`: installs PyMuPDF, PyMuPDF4LLM, and tiktoken. Use this for ordinary papers, complex selectable PDFs, basic book extraction, and token planning.
- `docling`: installs Docling. Use this for long books, reports, EPUB-like documents, and documents where layout conversion matters. This can be heavy.

Run multiple profiles only when needed:

```bash
python3 scripts/setup_environment.py --profile light --profile docling
```

## Optional System Tools

These are not installed by the skill because they depend on the operating system:

- OCRmyPDF + Tesseract: required for scanned PDFs.
- Poppler tools such as `pdfinfo` and `pdftotext`: useful for page count and fallback extraction.
- Java + GROBID service: useful for scholarly metadata, references, authors, affiliations, and TEI output.

Use `scripts/probe_tools.py` to inspect availability before deciding on a workflow.

## User-Friendly Workflow

For non-technical users, keep the workflow to three commands:

```bash
git clone https://github.com/foboguha063-cmd/bilingual-paper-digest.git
cd bilingual-paper-digest
python3 scripts/install_skill.py --with-env light
```

The user should not need to understand Docling, GROBID, OCRmyPDF, tiktoken, or the internal root-router design to use the default paper-note workflow. They can invoke the narrow companion skill that matches the task.

Use root-only installation only for debugging:

```bash
python3 scripts/install_skill.py --no-companions
```

For updates after a repository pull, run:

```bash
git pull
python3 scripts/install_skill.py --clean
```

Use `--with-env light` again only if the installed environment is missing or stale.

Before sharing a changed version, run:

```bash
python3 scripts/run_checks.py
```

This check is intentionally standard-library only. It validates the skill metadata, referenced resources, examples, knowledge cards, translation cache behavior, source-alignment behavior, and installer behavior without requiring PDF libraries.

## Runtime Artifacts

When processing a PDF, write temporary artifacts next to the source document:

```text
.bilingual-paper-digest/
├── source.jsonl
├── source_map.json
├── translation_units.jsonl
├── terminology_hits.json
└── translation_cache.jsonl
```

These files let future runs resume without re-extracting the PDF or retranslating unchanged source units.
