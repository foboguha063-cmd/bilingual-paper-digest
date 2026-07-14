#!/usr/bin/env python3
"""Check Obsidian knowledge cards for duplicate titles and alias conflicts."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CARD_MARKER = "# **来源论文 / 应用场景**"


@dataclass
class Card:
    path: Path
    title: str
    aliases: list[str]
    has_identity: bool
    has_hierarchy: bool


def normalize(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("（", "(").replace("）", ")")
    value = re.sub(r"\[\[([^]|]+)(?:\|[^]]+)?\]\]", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"^(规范名|别名\s*/\s*同义名|同义名|aliases?|name)\s*[:：]\s*", "", value)
    value = re.sub(r"[\s_\-–—/]+", "", value)
    value = re.sub(r"[()（）\[\]【】,，;；:：.。]", "", value)
    return value


def split_aliases(value: str) -> list[str]:
    value = re.sub(r"^-\s*", "", value.strip())
    value = re.sub(r"^(规范名|别名\s*/\s*同义名|同义名|aliases?|name)\s*[:：]\s*", "", value)
    parts = re.split(r"[;；、，,]", value)
    return [part.strip() for part in parts if part.strip()]


def iter_markdown(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.suffix.lower() == ".md":
            files.append(path)
    return files


def parse_card(path: Path) -> Card | None:
    text = path.read_text(encoding="utf-8")
    if CARD_MARKER not in text:
        return None

    lines = text.splitlines()
    title = ""
    aliases: list[str] = []
    in_identity = False
    has_identity = False
    has_hierarchy = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not title:
            title = stripped[2:].strip()
            continue

        if stripped.startswith("## "):
            in_identity = "别名" in stripped or "规范名" in stripped
            has_identity = has_identity or in_identity
            has_hierarchy = has_hierarchy or "知识层级" in stripped
            continue

        if in_identity and stripped.startswith("-"):
            item = re.sub(r"^-\s*", "", stripped)
            if item.startswith("不合并"):
                continue
            aliases.extend(split_aliases(stripped))

    if not title:
        return None

    clean_aliases: list[str] = []
    seen: set[str] = set()
    for alias in aliases:
        key = normalize(alias)
        if not key or key in seen:
            continue
        seen.add(key)
        clean_aliases.append(alias)

    return Card(path=path, title=title, aliases=clean_aliases, has_identity=has_identity, has_hierarchy=has_hierarchy)


def check(cards: list[Card], strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    titles: dict[str, list[Card]] = {}
    aliases: dict[str, list[Card]] = {}

    for card in cards:
        title_key = normalize(card.title)
        titles.setdefault(title_key, []).append(card)
        aliases.setdefault(title_key, []).append(card)

        for alias in card.aliases:
            alias_key = normalize(alias)
            aliases.setdefault(alias_key, []).append(card)

        if strict and not card.has_identity:
            errors.append(f"{card.path}: missing identity section: ## **规范名 / 别名**")
        elif not card.has_identity:
            warnings.append(f"{card.path}: missing identity section")

        if strict and not card.has_hierarchy:
            errors.append(f"{card.path}: missing hierarchy section: ## **知识层级**")
        elif not card.has_hierarchy:
            warnings.append(f"{card.path}: missing hierarchy section")

    for same_title in titles.values():
        unique_paths = {card.path for card in same_title}
        if len(unique_paths) > 1:
            paths = ", ".join(str(path) for path in sorted(unique_paths))
            errors.append(f"duplicate canonical title after normalization: {same_title[0].title} -> {paths}")

    for alias_key, matched_cards in aliases.items():
        unique_titles = {card.title for card in matched_cards}
        if len(unique_titles) > 1:
            paths = ", ".join(f"{card.title} ({card.path})" for card in matched_cards)
            errors.append(f"alias/title conflict '{alias_key}' points to multiple cards: {paths}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", type=Path, nargs="+", help="Knowledge-card files or directories to check.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail when a card lacks identity or hierarchy sections.",
    )
    args = parser.parse_args()

    cards = [card for path in iter_markdown(args.paths) if (card := parse_card(path))]
    if not cards:
        print("No knowledge cards found.", file=sys.stderr)
        return 1

    errors, warnings = check(cards, args.strict)

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        print("Knowledge-card check: FAIL", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"Knowledge-card check: OK ({len(cards)} card(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
