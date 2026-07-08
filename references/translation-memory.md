# Translation Memory

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
3. Look up `source_hash` in `translation_cache.jsonl`.
4. Reuse checked translations.
5. Translate only missing or changed units.
6. Append new checked translations to the cache.

## Review Workflow

Use two passes only when quality matters:

1. Translation pass: translate each source sentence faithfully.
2. Alignment pass: compare source and Chinese line for missing numbers, negation, citations, units, and terminology.

Do not run a free-form "polish" pass because it tends to compress or summarize the source.
