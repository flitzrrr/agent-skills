#!/usr/bin/env python3
"""Track progress of a product description update campaign.

Usage:
    python track_progress.py <catalog.json> [--config product-seo-config.json] [--min-words 200]

Shows overall progress, per-priority breakdown, and a next-action queue.
Priorities are loaded from config; without config all categories are equal.
"""

import json
import sys
import argparse
from collections import defaultdict

DESC_FIELD = "beschreibung"
CAT_FIELD = "kategorieName"
CAT_FIELD_ALT = "kategorie"
SKU_FIELD = "sku"
NAME_FIELD = "name"
STATUS_FIELD = "status"
STATUS_ACTIVE = "aktiv"


def load_priorities(config_path: str | None) -> dict[str, int]:
    """Load priority map from config. Returns {category_name: priority_level}."""
    if not config_path:
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        prio_map = {}
        for level, cats in config.get("priorities", {}).items():
            for cat in cats:
                prio_map[cat] = int(level)
        return prio_map
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_priority(cat_name: str, prio_map: dict[str, int]) -> int:
    if not prio_map:
        return 1  # No config = all equal priority
    return prio_map.get(cat_name, 3)


def main():
    parser = argparse.ArgumentParser(description="Track description update progress")
    parser.add_argument("catalog_path", help="Path to catalog JSON file")
    parser.add_argument("--config", help="Path to product-seo-config.json")
    parser.add_argument("--min-words", "-m", type=int, default=200,
                        help="Word count threshold (default: 200)")
    args = parser.parse_args()

    with open(args.catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    prio_map = load_priorities(args.config)
    products = [p for p in data.get("products", [])
                if p.get(STATUS_FIELD, STATUS_ACTIVE) == STATUS_ACTIVE]

    categories = defaultdict(lambda: {"total": 0, "done": 0, "todo": 0, "products_todo": []})

    for p in products:
        cat = p.get(CAT_FIELD, p.get(CAT_FIELD_ALT, "Unknown"))
        wc = len(p.get(DESC_FIELD, "").split())
        categories[cat]["total"] += 1
        if wc >= args.min_words:
            categories[cat]["done"] += 1
        else:
            categories[cat]["todo"] += 1
            categories[cat]["products_todo"].append({
                SKU_FIELD: p.get(SKU_FIELD, ""),
                NAME_FIELD: p.get(NAME_FIELD, ""),
                "words": wc,
            })

    total_products = len(products)
    total_done = sum(c["done"] for c in categories.values())
    total_todo = total_products - total_done
    pct = total_done * 100 // total_products if total_products > 0 else 0

    bar_len = 40
    filled = bar_len * total_done // total_products if total_products > 0 else 0
    bar = "#" * filled + "-" * (bar_len - filled)

    print(f"{'=' * 70}")
    print(f"PRODUCT DESCRIPTION PROGRESS")
    print(f"{'=' * 70}")
    print(f"\n  [{bar}] {pct}%")
    print(f"  {total_done}/{total_products} products with >={args.min_words} words")
    print(f"  {total_todo} remaining")
    print(f"\n  Estimated effort: ~{total_todo // 6 + 1} batch runs at 5-8 products each")

    # Determine which priority levels exist
    prio_levels = sorted(set(get_priority(name, prio_map) for name in categories))

    for prio in prio_levels:
        prio_cats = [(name, stats) for name, stats in categories.items()
                     if get_priority(name, prio_map) == prio]
        if not prio_cats:
            continue

        prio_total = sum(s["total"] for _, s in prio_cats)
        prio_done = sum(s["done"] for _, s in prio_cats)
        prio_pct = prio_done * 100 // prio_total if prio_total > 0 else 0

        label = f"PRIORITY {prio}" if prio_map else "ALL CATEGORIES"
        print(f"\n{'-' * 70}")
        print(f"{label} -- {prio_done}/{prio_total} done ({prio_pct}%)")
        print(f"{'-' * 70}")
        print(f"{'Category':<45} {'Done':>10} {'Open':>7}")

        for name, stats in sorted(prio_cats, key=lambda x: x[1]["todo"], reverse=True):
            done_str = f"{stats['done']}/{stats['total']}"
            check = " done" if stats["todo"] == 0 else ""
            print(f"  {name:<43} {done_str:>10} {stats['todo']:>5}  {check}")

    # Next action queue
    print(f"\n{'=' * 70}")
    print(f"NEXT ACTIONS")
    print(f"{'=' * 70}")

    shown = 0
    for name, stats in sorted(categories.items(),
                               key=lambda x: (get_priority(x[0], prio_map), -x[1]["todo"])):
        if stats["todo"] == 0:
            continue
        prio = get_priority(name, prio_map)
        label = f"Prio {prio}" if prio_map else ""
        print(f"\n  -> {name} ({label + ', ' if label else ''}{stats['todo']} open):")
        for p in sorted(stats["products_todo"], key=lambda x: x["words"])[:5]:
            print(f"     SKU {p[SKU_FIELD]}: {p[NAME_FIELD]} ({p['words']} words)")
        shown += 1
        if shown >= 5:
            break


if __name__ == "__main__":
    main()
