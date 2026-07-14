#!/usr/bin/env python3
"""Apply and update JSONL translation cache files."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
    return records


def write_jsonl(path: Path, records: Iterable[dict[str, object]]) -> int:
    count = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    return count


def cache_index(cache_records: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    index: dict[str, dict[str, object]] = {}
    for record in cache_records:
        source_hash = str(record.get("source_hash", ""))
        translation = str(record.get("translation", "")).strip()
        if source_hash and translation:
            index[source_hash] = record
    return index


def apply_cache(units_path: Path, cache_path: Path, out_path: Path, statuses: set[str]) -> int:
    units = read_jsonl(units_path)
    cache = cache_index(read_jsonl(cache_path))
    hits = 0
    output: list[dict[str, object]] = []

    for unit in units:
        source_hash = str(unit.get("source_hash", ""))
        cached = cache.get(source_hash)
        if cached and str(unit.get("translation", "")).strip() == "":
            unit["translation"] = cached.get("translation", "")
            unit["status"] = cached.get("status", "cached")
            unit["cache_hit"] = True
            hits += 1
        elif cached and str(unit.get("status", "")) in statuses:
            unit["cache_hit"] = True
        else:
            unit["cache_hit"] = False
        output.append(unit)

    write_jsonl(out_path, output)
    print(f"Wrote {out_path}")
    print(f"Cache hits: {hits}/{len(units)}")
    return 0


def update_cache(units_path: Path, cache_path: Path, statuses: set[str]) -> int:
    units = read_jsonl(units_path)
    existing_records = read_jsonl(cache_path)
    index = cache_index(existing_records)
    added = 0
    updated = 0
    now = datetime.now(timezone.utc).isoformat()

    for unit in units:
        source_hash = str(unit.get("source_hash", ""))
        source_sentence = str(unit.get("source_sentence", "")).strip()
        translation = str(unit.get("translation", "")).strip()
        status = str(unit.get("status", "")).strip() or "translated"
        if not source_hash or not source_sentence or not translation:
            continue
        if statuses and status not in statuses:
            continue

        cache_record = {
            "source_hash": source_hash,
            "source_sentence": source_sentence,
            "translation": translation,
            "status": status,
            "updated_at": now,
            "source_file": unit.get("source_file"),
            "page": unit.get("page"),
        }
        if source_hash in index:
            index[source_hash].update(cache_record)
            updated += 1
        else:
            index[source_hash] = cache_record
            added += 1

    sorted_records = sorted(index.values(), key=lambda record: str(record.get("source_hash", "")))
    write_jsonl(cache_path, sorted_records)
    print(f"Wrote {cache_path}")
    print(f"Added: {added}; updated: {updated}; total cache entries: {len(sorted_records)}")
    return 0


def show_stats(units_path: Path, cache_path: Path) -> int:
    units = read_jsonl(units_path)
    cache = cache_index(read_jsonl(cache_path))
    total = len(units)
    hit_count = sum(1 for unit in units if str(unit.get("source_hash", "")) in cache)
    translated = sum(1 for unit in units if str(unit.get("translation", "")).strip())
    pending = total - translated
    print(f"Units: {total}")
    print(f"Cache entries: {len(cache)}")
    print(f"Cache coverage: {hit_count}/{total}")
    print(f"Translated units: {translated}")
    print(f"Pending units: {pending}")
    return 0


def export_pending_batch(units_path: Path, out_path: Path, limit: int) -> int:
    units = read_jsonl(units_path)
    pending = [
        unit
        for unit in units
        if not str(unit.get("translation", "")).strip()
        and str(unit.get("status", "")).lower() not in {"skip", "skipped", "omit", "omitted", "structural"}
        and str(unit.get("unit_type", "")).lower() not in {"heading", "structural"}
    ][:limit]
    write_jsonl(out_path, pending)
    print(f"Wrote {out_path}")
    print(f"Pending batch: {len(pending)} unit(s); limit: {limit}")
    return 0


def merge_batch(units_path: Path, batch_path: Path, out_path: Path) -> int:
    units = read_jsonl(units_path)
    batch = read_jsonl(batch_path)
    by_id = {
        str(unit.get("translation_unit_id", "")): unit
        for unit in units
        if str(unit.get("translation_unit_id", ""))
    }
    seen: set[str] = set()
    merged = 0

    for candidate in batch:
        unit_id = str(candidate.get("translation_unit_id", ""))
        if not unit_id or unit_id in seen:
            raise SystemExit(f"duplicate or missing translation_unit_id in batch: {unit_id!r}")
        seen.add(unit_id)
        target = by_id.get(unit_id)
        if target is None:
            raise SystemExit(f"batch unit does not exist in source units: {unit_id}")
        if str(candidate.get("source_hash", "")) != str(target.get("source_hash", "")):
            raise SystemExit(f"source hash changed for batch unit: {unit_id}")
        translation = str(candidate.get("translation", "")).strip()
        if not translation:
            continue
        target["translation"] = translation
        target["status"] = str(candidate.get("status", "")).strip() or "translated"
        merged += 1

    temporary = out_path.with_suffix(out_path.suffix + ".tmp")
    write_jsonl(temporary, units)
    temporary.replace(out_path)
    print(f"Wrote {out_path}")
    print(f"Merged translations: {merged}/{len(batch)}")
    return 0


def parse_statuses(value: str) -> set[str]:
    return {part.strip() for part in value.split(",") if part.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    apply_parser = subparsers.add_parser("apply", help="Fill pending units from cache.")
    apply_parser.add_argument("--units", type=Path, required=True)
    apply_parser.add_argument("--cache", type=Path, required=True)
    apply_parser.add_argument("--out", type=Path, required=True)
    apply_parser.add_argument("--statuses", default="checked,translated,cached")

    update_parser = subparsers.add_parser("update", help="Append/update cache from translated units.")
    update_parser.add_argument("--units", type=Path, required=True)
    update_parser.add_argument("--cache", type=Path, required=True)
    update_parser.add_argument("--statuses", default="checked,translated,cached")

    stats_parser = subparsers.add_parser("stats", help="Report cache coverage.")
    stats_parser.add_argument("--units", type=Path, required=True)
    stats_parser.add_argument("--cache", type=Path, required=True)

    batch_parser = subparsers.add_parser("batch", help="Export the next pending translation batch.")
    batch_parser.add_argument("--units", type=Path, required=True)
    batch_parser.add_argument("--out", type=Path, required=True)
    batch_parser.add_argument("--limit", type=int, default=50)

    merge_parser = subparsers.add_parser("merge", help="Merge a translated batch back into all units.")
    merge_parser.add_argument("--units", type=Path, required=True)
    merge_parser.add_argument("--batch", type=Path, required=True)
    merge_parser.add_argument("--out", type=Path)

    args = parser.parse_args()

    try:
        if args.command == "apply":
            return apply_cache(args.units, args.cache, args.out, parse_statuses(args.statuses))
        if args.command == "update":
            return update_cache(args.units, args.cache, parse_statuses(args.statuses))
        if args.command == "stats":
            return show_stats(args.units, args.cache)
        if args.command == "batch":
            if args.limit < 1:
                raise SystemExit("--limit must be at least 1")
            return export_pending_batch(args.units, args.out, args.limit)
        if args.command == "merge":
            return merge_batch(args.units, args.batch, args.out or args.units)
    except BrokenPipeError:
        return 1
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
