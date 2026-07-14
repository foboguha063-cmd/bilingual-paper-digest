# Translation Memory

## Contents

- Stable source hashes and local memory files
- Terminology injection and cache workflow
- Batch merge, quality review, rendering, and alignment

Use this reference when reducing repeated token use, preserving terminology across papers, or resuming long translations.

## Principle

Never send text for translation again if the exact source unit has already been translated and the user has not requested a revision.

Use stable source hashes:

```json
{
  "source_hash": "sha1...",
  "source_sentence": "...",
  "translation": "...",
  "domain": "materials",
  "status": "checked"
}
```

## Recommended Local Files

Keep runtime memory beside the source document:

```text
.bilingual-paper-digest/
├── translation_cache.jsonl
├── terminology_hits.json
└── translation_units.jsonl
```

Do not commit these files into the skill repository.

## Terminology Injection

Only inject terms that appear in the current source block:

```text
LD score regression = LD score regression
polygenic score = 多基因评分
electrochemical impedance spectroscopy = 电化学阻抗谱
```

Do not paste the entire Obsidian knowledge base into the translation prompt. Use knowledge cards to maintain canonical terms, then pass only matched terms to the translation unit.

## Cache Workflow

1. Build `translation_units.jsonl`.
2. Compute `source_hash` for each unit.
3. Run cache stats:

```bash
python3 scripts/translation_cache.py stats \
  --units .bilingual-paper-digest/translation_units.jsonl \
  --cache .bilingual-paper-digest/translation_cache.jsonl
```

4. Apply checked translations:

```bash
python3 scripts/translation_cache.py apply \
  --units .bilingual-paper-digest/translation_units.jsonl \
  --cache .bilingual-paper-digest/translation_cache.jsonl \
  --out .bilingual-paper-digest/translation_units.cached.jsonl
```

5. Translate only missing or changed units.
6. For long work, export a bounded pending batch:

```bash
python3 scripts/translation_cache.py batch \
  --units .bilingual-paper-digest/translation_units.cached.jsonl \
  --out .bilingual-paper-digest/pending-batch.jsonl \
  --limit 50
```

Keep `translation_unit_id`, `source_hash`, and `source_sentence` unchanged. Fill only `translation` and set `status` to `translated` or `checked`, then merge:

```bash
python3 scripts/translation_cache.py merge \
  --units .bilingual-paper-digest/translation_units.cached.jsonl \
  --batch .bilingual-paper-digest/pending-batch.jsonl
```

7. Update the cache after review:

```bash
python3 scripts/translation_cache.py update \
  --units .bilingual-paper-digest/translation_units.cached.jsonl \
  --cache .bilingual-paper-digest/translation_cache.jsonl
```

## Review Workflow

Use two passes only when quality matters:

1. Translation pass: translate each source sentence faithfully.
2. Alignment pass: compare source and Chinese line for missing numbers, negation, citations, units, and terminology.
3. Run deterministic bilingual checks and render only complete paragraphs:

```bash
python3 scripts/check_bilingual_quality.py \
  --units .bilingual-paper-digest/translation_units.cached.jsonl
python3 scripts/render_bilingual_markdown.py \
  --units .bilingual-paper-digest/translation_units.cached.jsonl \
  --out output.md
```

4. Check source coverage and order:

```bash
python3 scripts/check_source_alignment.py \
  --units .bilingual-paper-digest/translation_units.cached.jsonl \
  --markdown output.md
```

Do not run a free-form "polish" pass because it tends to compress or summarize the source.
