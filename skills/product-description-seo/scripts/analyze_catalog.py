#!/usr/bin/env python3
"""Analyze a JSON product catalog for thin or missing descriptions.

Usage:
    python analyze_catalog.py <catalog.json> [--category <name>] [--min-words 200]

Shows per-category stats, identifies the thinnest descriptions,
and exports batch-ready JSON when filtering by category.
"""

import json
import sys
import argparse
from collections import defaultdict

# Default field names (override via config)
DESC_FIELD = "beschreibung"
CAT_FIELD = "kategorieName"
CAT_FIELD_ALT = "kategorie"
SKU_FIELD = "sku"
NAME_FIELD = "name"
STATUS_FIELD = "status"
STATUS_ACTIVE = "aktiv"


def count_words(text: str) -> int:
    if not text or not text.strip():
        return 0
    return len(text.split())


def analyze(catalog_path: str, category_filter: str | None = None, min_words: int = 200):
    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    products = data.get("products", [])
    products = [p for p in products if p.get(STATUS_FIELD, STATUS_ACTIVE) == STATUS_ACTIVE]

    if category_filter:
        cf = category_filter.lower()
        products = [p for p in products
                    if cf in p.get(CAT_FIELD_ALT, "").lower()
                    or cf in p.get(CAT_FIELD, "").lower()
                    or p.get(CAT_FIELD_ALT, "").lower() == cf
                    or p.get(CAT_FIELD, "").lower() == cf]

    if not products:
        print("No matching products found.")
        all_cats = sorted(set(
            p.get(CAT_FIELD, p.get(CAT_FIELD_ALT, "?"))
            for p in data.get("products", [])
        ))
        if all_cats:
            print("Available categories:")
            for c in all_cats:
                print(f"  - {c}")
        return

    categories = defaultdict(list)
    for p in products:
        cat = p.get(CAT_FIELD, p.get(CAT_FIELD_ALT, "Unknown"))
        wc = count_words(p.get(DESC_FIELD, ""))
        categories[cat].append({
            SKU_FIELD: p.get(SKU_FIELD, ""),
            NAME_FIELD: p.get(NAME_FIELD, ""),
            "word_count": wc,
            DESC_FIELD: p.get(DESC_FIELD, ""),
        })

    total = len(products)
    below_threshold = sum(1 for p in products if count_words(p.get(DESC_FIELD, "")) < min_words)

    print(f"{'=' * 70}")
    print(f"CATALOG DESCRIPTION ANALYSIS")
    print(f"{'=' * 70}")
    print(f"Active products:       {total}")
    print(f"Below {min_words} words:       {below_threshold} ({below_threshold * 100 // total}%)")
    print(f"Above {min_words} words:       {total - below_threshold} ({(total - below_threshold) * 100 // total}%)")
    print()

    print(f"{'Category':<45} {'Count':>5} {'Avg Words':>9} {'< {}'.format(min_words):>7}")
    print(f"{'-' * 45} {'-' * 5} {'-' * 9} {'-' * 7}")

    sorted_cats = sorted(categories.items(),
                         key=lambda x: sum(p["word_count"] for p in x[1]) / len(x[1]))

    for cat_name, prods in sorted_cats:
        avg_wc = sum(p["word_count"] for p in prods) / len(prods)
        below = sum(1 for p in prods if p["word_count"] < min_words)
        print(f"{cat_name:<45} {len(prods):>5} {avg_wc:>9.1f} {below:>7}")

    # Thinnest descriptions
    print(f"\n{'=' * 70}")
    print(f"THINNEST DESCRIPTIONS (Top 20)")
    print(f"{'=' * 70}")

    all_products = []
    for cat_name, prods in categories.items():
        for p in prods:
            p["_category"] = cat_name
            all_products.append(p)

    all_products.sort(key=lambda x: x["word_count"])

    for i, p in enumerate(all_products[:20]):
        print(f"\n{i + 1}. {p[NAME_FIELD]} (SKU {p[SKU_FIELD]}) — {p['_category']}")
        print(f"   Words: {p['word_count']}")
        desc = p[DESC_FIELD]
        desc_preview = desc[:120] + "..." if len(desc) > 120 else (desc or "(empty)")
        print(f'   Text: "{desc_preview}"')

    # JSON export when filtering by category
    if category_filter:
        print(f"\n{'=' * 70}")
        print(f"BATCH-READY JSON (Category: {category_filter})")
        print(f"{'=' * 70}")
        export = [{SKU_FIELD: p[SKU_FIELD], NAME_FIELD: p[NAME_FIELD],
                    DESC_FIELD: p[DESC_FIELD], "word_count": p["word_count"]}
                  for p in all_products]
        print(json.dumps(export, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Analyze catalog descriptions")
    parser.add_argument("catalog_path", help="Path to catalog JSON file")
    parser.add_argument("--category", "-c", help="Filter by category name (fuzzy match)")
    parser.add_argument("--min-words", "-m", type=int, default=200,
                        help="Minimum word count threshold (default: 200)")
    args = parser.parse_args()
    analyze(args.catalog_path, args.category, args.min_words)


if __name__ == "__main__":
    main()
