#!/usr/bin/env python3
"""Check deterministic fidelity signals in English-Chinese translation pairs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


CJK = re.compile(r"[\u3400-\u9fff]")
CITATION = re.compile(r"\[(\d+(?:\s*[,;–—-]\s*\d+)*)\]")
NUMBER = re.compile(r"(?<![A-Za-z0-9.])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][-+]?\d+)?%?")
UNIT_AFTER_NUMBER = re.compile(
    r"[-+]?(?:\d+(?:\.\d+)?)(?:\s*)(%|°C|°F|μg|µg|mg|kg|ng|g|"
    r"μm|µm|mm|cm|nm|km|mL|ml|L|μl|µl|mmol|μmol|µmol|mol|"
    r"μM|µM|mM|M|ms|min|h|s|Hz|kHz|MHz|Pa|kPa|MPa|GPa|mV|V|mA|A|mW|W|rpm)(?![A-Za-z])"
)
IDENTIFIER = re.compile(
    r"(?<![A-Za-z0-9])(?:[A-Z]{2,}[A-Z0-9-]*|[A-Za-z]+-\d+[A-Za-z0-9+-]*|"
    r"[A-Za-z]+[A-Za-z0-9+-]*\d[A-Za-z0-9+-]*)(?![A-Za-z0-9])"
)
COMPARATOR = re.compile(r"(?:<=|>=|!=|=|<|>|\u2264|\u2265|≈|±)")
GREEK = re.compile(r"[α-ωΑ-Ω]")
EN_NEGATION = re.compile(
    r"\b(?:no|not|never|neither|nor|without|lack(?:s|ed|ing)?|absen(?:t|ce)|"
    r"fail(?:s|ed|ing|ure)?|unable|unlikely|cannot|can't|didn't|doesn't|don't|"
    r"wasn't|weren't|isn't|aren't|unchanged|unaffected|undetectable|"
    r"insignificant|nonsignificant|non[-\s])\b",
    flags=re.IGNORECASE,
)
ZH_NEGATION = re.compile(r"(?:不|无|未|非|否|没有|缺乏|不能|无法|并非|不太可能)")
SKIP_STATUSES = {"skip", "skipped", "omit", "omitted", "structural"}


def normalize_symbol(value: str) -> str:
    return (
        value.replace("−", "-")
        .replace("–", "-")
        .replace("—", "-")
        .replace("µ", "μ")
        .replace(",", "")
        .strip()
    )


def without_citations(value: str) -> str:
    return CITATION.sub("", value)


def counters(value: str) -> dict[str, Counter[str]]:
    plain = without_citations(value)
    identifier_values = IDENTIFIER.findall(plain)
    numeric_plain = IDENTIFIER.sub("", plain)
    return {
        "citations": Counter(normalize_symbol(match) for match in CITATION.findall(value)),
        "numbers": Counter(normalize_symbol(match) for match in NUMBER.findall(numeric_plain)),
        "units": Counter(normalize_symbol(match) for match in UNIT_AFTER_NUMBER.findall(plain)),
        "identifiers": Counter(match.casefold() for match in identifier_values),
        "comparators": Counter(normalize_symbol(match) for match in COMPARATOR.findall(plain)),
        "greek": Counter(match for match in GREEK.findall(plain)),
    }


def counter_delta(source: Counter[str], translation: Counter[str]) -> tuple[list[str], list[str]]:
    missing = sorted((source - translation).elements())
    extra = sorted((translation - source).elements())
    return missing, extra


def read_unit_pairs(path: Path) -> list[tuple[str, str, str]]:
    pairs: list[tuple[str, str, str]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                unit = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
            status = str(unit.get("status", "")).lower()
            unit_type = str(unit.get("unit_type", "")).lower()
            if status in SKIP_STATUSES or unit_type in {"heading", "structural"}:
                continue
            source = str(unit.get("source_sentence", "")).strip()
            translation = str(unit.get("translation", "")).strip()
            label = str(unit.get("translation_unit_id") or f"line {line_number}")
            if source:
                pairs.append((label, source, translation))
    return pairs


def looks_like_source(line: str) -> bool:
    stripped = line.strip()
    if not stripped or line.startswith(("\t", " ", "#", "|", ">")):
        return False
    if stripped.startswith(("**团队**", "DOI", "Published", "Received", "Revised", "Accepted")):
        return False
    return bool(re.search(r"[A-Za-z]", stripped))


def read_markdown_pairs(path: Path) -> list[tuple[str, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    first_heading = next((i for i, line in enumerate(lines) if line.lstrip().startswith("#")), len(lines))
    pairs: list[tuple[str, str, str]] = []
    in_fence = False
    for index, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or index < first_heading or not looks_like_source(line):
            continue
        translation = lines[index + 1].lstrip("\t").strip() if index + 1 < len(lines) and lines[index + 1].startswith("\t") else ""
        pairs.append((f"line {index + 1}", line.strip(), translation))
    return pairs


def review_pair(label: str, source: str, translation: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not translation:
        return [f"{label}: missing Chinese translation"], []
    if len(re.findall(r"[A-Za-z]", source)) >= 5 and not CJK.search(translation):
        errors.append(f"{label}: translation contains no Chinese characters")

    source_values = counters(source)
    translated_values = counters(translation)
    for category in ("citations", "numbers", "units", "identifiers", "comparators", "greek"):
        missing, extra = counter_delta(source_values[category], translated_values[category])
        if missing:
            errors.append(f"{label}: missing {category}: {', '.join(missing)}")
        if extra:
            severity = errors if category == "citations" else warnings
            severity.append(f"{label}: extra {category}: {', '.join(extra)}")

    if EN_NEGATION.search(source) and not ZH_NEGATION.search(translation):
        errors.append(f"{label}: source negation has no clear Chinese negation marker")
    if not EN_NEGATION.search(source) and ZH_NEGATION.search(translation):
        warnings.append(f"{label}: translation adds a negation marker; review semantic polarity")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--units", type=Path)
    source.add_argument("--markdown", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    parser.add_argument("--report", type=Path, help="Optional JSON report path.")
    args = parser.parse_args()

    pairs = read_unit_pairs(args.units) if args.units else read_markdown_pairs(args.markdown)
    errors: list[str] = []
    warnings: list[str] = []
    for label, source_text, translation in pairs:
        pair_errors, pair_warnings = review_pair(label, source_text, translation)
        errors.extend(pair_errors)
        warnings.extend(pair_warnings)

    report = {"pairs_checked": len(pairs), "errors": errors, "warnings": warnings}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {args.report}")

    print(f"Pairs checked: {len(pairs)}")
    print(f"Errors: {len(errors)}; warnings: {len(warnings)}")
    for message in errors:
        print(f"ERROR: {message}", file=sys.stderr)
    for message in warnings:
        print(f"WARNING: {message}", file=sys.stderr)
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
